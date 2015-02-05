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

import logging

from .endpoint import EndpointCreator
from .operation import Operation
from .exceptions import ServiceNotInRegionError, NoRegionError
from .exceptions import UnknownEndpointError
from .model import ServiceModel, OperationModel
from .translate import denormalize_waiters
from . import waiter


logger = logging.getLogger(__name__)
NOT_SET = object()


class Service(object):
    """
    A service, such as Elastic Compute Cloud (EC2).

    :ivar api_version: A string containing the API version this service
        is using.
    :ivar name: The full name of the service.
    :ivar service_name: The canonical name of the service.
    :ivar regions: A dict where each key is a region name and the
        optional value is an endpoint for that region.
    :ivar protocols: A list of protocols supported by the service.
    """

    def __init__(self, session, provider, service_name,
                 path='/', port=None, api_version=None):
        self.timestamp_format = 'iso8601'
        sdata = session.get_service_data(
            service_name,
            api_version=None
        )
        self._model = session.get_service_model(service_name)
        self.__dict__.update(sdata)
        self._operations_data = self.__dict__.pop('operations')
        self._operations = None
        self.session = session
        self.provider = provider
        self.path = path
        self.port = port
        self.cli_name = service_name
        # The name the service was set with can be different
        # than the endpoint prefix (for now). For example
        # elb == service name,
        # elasticloadbalancing == endpoint_prefix
        # If we want to retrieve resources on disk, it will be
        # grouped by the service name, so we need to expose this
        # as an attribute for client obejcts.
        self.service_name = service_name
        self._signature_version = NOT_SET
        self._has_custom_signature_version = False
        # Not all services have a top level documentation key,
        # so we'll add one if needed.
        if 'documentation' not in self.__dict__:
            self.documentation = ''

    @property
    def service_full_name(self):
        return self._model.metadata['serviceFullName']

    @property
    def endpoint_prefix(self):
        return self._model.metadata['endpointPrefix']

    @property
    def global_endpoint(self):
        return self._model.metadata.get('globalEndpoint')

    @property
    def target_prefix(self):
        return self._model.metadata['targetPrefix']

    @property
    def type(self):
        return self._model.metadata['protocol']

    @property
    def api_version(self):
        return self._model.metadata['apiVersion']

    @property
    def signature_version(self):
        if self._signature_version is NOT_SET:
            signature_version = self._model.metadata.get('signatureVersion')
            self._signature_version = signature_version
            self._has_custom_signature_version = False
        return self._signature_version

    @signature_version.setter
    def signature_version(self, value):
        self._signature_version = value
        self._has_custom_signature_version = True

    def _create_operation_objects(self):
        logger.debug("Creating operation objects for: %s", self)
        operations = []
        for operation_name in self._operations_data:
            data = self._operations_data[operation_name]
            data['name'] = operation_name
            model = self._model.operation_model(operation_name)
            op = Operation(self, data, model)
            operations.append(op)
        return operations

    def __repr__(self):
        return 'Service(%s)' % self.endpoint_prefix

    @property
    def operations(self):
        if self._operations is None:
            self._operations = self._create_operation_objects()
        return self._operations

    def get_endpoint(self, region_name=None, is_secure=True,
                     endpoint_url=None, verify=None):
        """
        Return the Endpoint object for this service in a particular
        region.

        :type region_name: str
        :param region_name: The name of the region.

        :type is_secure: bool
        :param is_secure: True if you want the secure (HTTPS) endpoint.

        :type endpoint_url: str
        :param endpoint_url: You can explicitly override the default
            computed endpoint name with this parameter.  If this arg is
            provided then neither ``region_name`` nor ``is_secure``
            is used in building the final ``endpoint_url``.
            ``region_name`` can still be useful for services that require
            a region name independent of the endpoint_url (for example services
            that use Signature Version 4, which require a region name for
            use in the signature calculation).

        """
        resolver = self.session.get_component('endpoint_resolver')
        region = self.session.get_config_variable('region')
        event_emitter = self.session.get_component('event_emitter')
        response_parser_factory = self.session.get_component(
            'response_parser_factory')
        user_agent= self.session.user_agent()
        endpoint_creator = EndpointCreator(resolver, region, event_emitter,
                                           user_agent)
        kwargs = {'service_model': self._model, 'region_name': region_name,
                  'is_secure': is_secure, 'endpoint_url': endpoint_url,
                  'verify': verify,
                  'response_parser_factory': response_parser_factory}
        if self._has_custom_signature_version:
            kwargs['signature_version'] = self.signature_version

        return endpoint_creator.create_endpoint(**kwargs)

    def get_operation(self, operation_name):
        """
        Find an Operation object for a given operation_name.  The name
        provided can be the original camel case name, the Python name or
        the CLI name.

        :type operation_name: str
        :param operation_name: The name of the operation.
        """
        for operation in self.operations:
            op_names = (operation.name, operation.py_name, operation.cli_name)
            if operation_name in op_names:
                return operation
        return None

    def get_waiter(self, waiter_name, endpoint):
        try:
            config = self._load_waiter_config()
        except Exception as e:
            raise ValueError("Waiter does not exist: %s" % waiter_name)
        return waiter.create_waiter_from_legacy(waiter_name, config,
                                                self, endpoint)

    def _load_waiter_config(self):
        loader = self.session.get_component('data_loader')
        api_version = self.api_version
        config = loader.load_data('aws/%s/%s.waiters' % (
            self.service_name, api_version))
        return config


def get_service(session, service_name, provider, api_version=None):
    """
    Return a Service object for a given provider name and service name.

    :type service_name: str
    :param service_name: The name of the service.

    :type provider: Provider
    :param provider: The Provider object associated with the session.
    """
    logger.debug("Creating service object for: %s", service_name)
    return Service(session, provider, service_name)
