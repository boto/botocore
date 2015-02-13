# Copyright (c) 2012-2013 Mitch Garnaat http://garnaat.org/
# Copyright 2012-2014 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

import functools
import logging
import threading
from botocore.exceptions import MissingParametersError
from botocore.exceptions import UnknownParameterError
from botocore.exceptions import NoRegionError
from botocore.paginate import DeprecatedPaginator
from botocore.signers import RequestSigner
from botocore import serialize
from botocore import BotoCoreObject, xform_name

from botocore.validate import ParamValidator
from botocore.exceptions import ParamValidationError


logger = logging.getLogger(__name__)


class Operation(BotoCoreObject):

    _DEFAULT_PAGINATOR_CLS = DeprecatedPaginator

    def __init__(self, service, op_data, model, paginator_cls=None):
        self.input = {}
        self.output = {}
        self._model = model
        BotoCoreObject.__init__(self, **op_data)
        self.service = service
        if self.service:
            self.session = self.service.session
        else:
            self.session = None
        self.type = 'operation'
        self._params = None
        if paginator_cls is None:
            paginator_cls = self._DEFAULT_PAGINATOR_CLS
        self._paginator_cls = paginator_cls
        self._lock = threading.Lock()

    def __repr__(self):
        return 'Operation:%s' % self.name

    @property
    def model(self):
        return self._model

    @property
    def output_shape(self):
        return self._model.output_shape

    @property
    def signature_version(self):
        return self.service.signature_version

    def _get_signature_version_and_region(self, endpoint, service_model):
        # An endpoint-aware signature version and region check
        scoped_config = self.session.get_scoped_config()
        resolver = self.session.get_component('endpoint_resolver')
        scheme = endpoint.host.split(':')[0]
        if endpoint.region_name is None:
            raise NoRegionError(env_var='region')
        endpoint_config = resolver.construct_endpoint(
                service_model.endpoint_prefix,
                endpoint.region_name, scheme=scheme)
        # Region name override from endpoint
        region_name = endpoint_config.get('properties', {}).get(
            'credentialScope', {}).get('region', endpoint.region_name)
        # Signature version override from endpoint
        signature_version = self.service.signature_version
        if 'signatureVersion' in endpoint_config.get('properties', {}):
            signature_version = endpoint_config['properties']\
                                               ['signatureVersion']

        # Signature overrides from a configuration file
        if scoped_config is not None:
            service_config = scoped_config.get(service_model.endpoint_prefix)
            if service_config is not None and isinstance(service_config, dict):
                override = service_config.get('signature_version')
                if override:
                    logger.debug(
                        "Switching signature version for service %s "
                         "to version %s based on config file override.",
                         service_model.endpoint_prefix, override)
                    signature_version = override

        return signature_version, region_name

    def call(self, endpoint, **kwargs):
        logger.debug("%s called with kwargs: %s", self, kwargs)
        # It probably seems a little weird to be firing two different
        # events here.  The reason is that the first event is fired
        # with the parameters exactly as supplied.  The second event
        # is fired with the built parameters.  Generally, it's easier
        # to manipulate the former but at times, like with ReST operations
        # that build an XML or JSON payload, you have to wait for
        # build_parameters to do it's job and the latter is necessary.
        event = self.session.create_event('before-parameter-build',
                                          self.service.endpoint_prefix,
                                          self.name)
        self.session.emit(event, endpoint=endpoint,
                          model=self.model,
                          params=kwargs)
        request_dict = self.build_parameters(**kwargs)

        service_name = self.service.service_name
        service_model = self.session.get_service_model(service_name)

        signature_version, region_name = \
            self._get_signature_version_and_region(
                endpoint, service_model)

        credentials = self.session.get_credentials()
        event_emitter = self.session.get_component('event_emitter')
        signer = RequestSigner(service_model.service_name,
                               region_name, service_model.signing_name,
                               signature_version, credentials,
                               event_emitter)

        event = self.session.create_event('before-call',
                                          self.service.endpoint_prefix,
                                          self.name)
        # The operation kwargs is being passed in kwargs to support
        # handlers that still depend on this value.  Eventually
        # everything should move over to the model/endpoint args.
        self.session.emit(event, endpoint=endpoint,
                          model=self.model,
                          params=request_dict,
                          operation=self,
                          request_signer=signer)

        # Here we register to the specific request-created event
        # for this operation. Since it's possible to run the same
        # operation in multiple threads, we used a lock to prevent
        # issues. It's possible a request will be signed more than
        # once. Once the request has been made, we unregister the
        # handler.
        def request_created(request, **kwargs):
            # This first check lets us quickly determine when
            # a request has already been signed without needing
            # to acquire the lock.
            if not getattr(request, '_is_signed', False):
                with self._lock:
                    if not getattr(request, '_is_signed', False):
                        signer.sign(self.name, request)
                        request._is_signed = True

        event_emitter.register('request-created.{0}.{1}'.format(
            self.service.endpoint_prefix, self.name), request_created)

        try:
            response = endpoint.make_request(self.model, request_dict)
        finally:
            event_emitter.unregister('request-created.{0}.{1}'.format(
                self.service.endpoint_prefix, self.name), request_created)

        event = self.session.create_event('after-call',
                                          self.service.endpoint_prefix,
                                          self.name)
        self.session.emit(event,
                          http_response=response[0],
                          model=self.model,
                          operation=self,
                          parsed=response[1])
        return response

    @property
    def pagination(self):
        try:
            return self._load_pagination_config()
        except Exception as e:
            return {}

    @property
    def can_paginate(self):
        try:
            self._load_pagination_config()
        except Exception as e:
            return False
        return True

    def paginate(self, endpoint, **kwargs):
        """Iterate over the responses of an operation.

        This will return an iterator with each element
        being a tuple of (``http_response``, ``parsed_response``).
        If the operation does not paginate, a ``TypeError`` will
        be raised.  You can check if an operation can be paginated
        by using the ``can_paginate`` arg.
        """
        if not self.can_paginate:
            raise TypeError("Operation cannot be paginated: %s" % self)
        config = self._load_pagination_config()
        paginator = self._paginator_cls(self, config)
        return paginator.paginate(endpoint, **kwargs)

    def _load_pagination_config(self):
        loader = self.session.get_component('data_loader')
        api_version = self.service.api_version
        config = loader.load_data('aws/%s/%s.paginators' %
                                  (self.service.service_name, api_version))
        return config['pagination'][self.name]

    @property
    def params(self):
        raise RuntimeError(
            "Attempted to access removed parameter objects in botocore.")
        if self._params is None:
            self._params = self._create_parameter_objects()
        return self._params

    def _create_parameter_objects(self):
        """
        Build the list of Parameter objects for this operation.
        """
        logger.debug("Creating parameter objects for: %s", self)
        params = []
        return params

    def _find_payload(self):
        """
        Searches the parameters for an operation to find the payload
        parameter, if it exists.  Returns that param or None.
        """
        payload = None
        for param in self.params:
            if hasattr(param, 'payload') and param.payload:
                payload = param
                break
        return payload

    def build_parameters(self, **kwargs):
        """
        Returns a dictionary containing the kwargs for the
        given operation formatted as required to pass to the service
        in a request.
        """
        protocol = self._model.metadata['protocol']
        input_shape = self._model.input_shape
        if input_shape is not None:
            self._convert_kwargs_to_correct_casing(kwargs)
            validator = ParamValidator()
            errors = validator.validate(kwargs, self._model.input_shape)
            if errors.has_errors():
                raise ParamValidationError(report=errors.generate_report())
        serializer = serialize.create_serializer(protocol)
        request_dict = serializer.serialize_to_request(kwargs, self._model)
        return request_dict

    def _convert_kwargs_to_correct_casing(self, kwargs):
        # XXX: This will be removed in botocore 1.0, but we should
        # support snake casing for now.
        # First we're going to build a map of snake_casing -> service casing
        actual_casing = list(self._model.input_shape.members)
        mapping = {}
        for key in actual_casing:
            transformed = xform_name(key)
            if key != transformed:
                mapping[xform_name(key)] = key
        # Look for anything in the user provided kwargs that is in the mapping
        # dict and convert appropriately.
        for key in list(kwargs):
            if key in mapping:
                # TODO: add a pending deprecation warning.
                value = kwargs[key]
                kwargs[mapping[key]] = value
                del kwargs[key]

    def _check_for_unknown_params(self, kwargs):
        valid_names = [p.py_name for p in self.params]
        for key in kwargs:
            if key not in valid_names:
                raise UnknownParameterError(name=key, operation=self,
                                            choices=', '.join(valid_names))

    def is_streaming(self):
        # TODO: add deprecation warning
        return self._model.has_streaming_output

    @property
    def has_streaming_output(self):
        return self._model.has_streaming_output
