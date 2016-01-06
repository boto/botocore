# Copyright 2014 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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
import copy
import logging

import botocore.serialize
import botocore.validate
from botocore import waiter, xform_name
from botocore.awsrequest import prepare_request_dict
from botocore.compat import OrderedDict
from botocore.endpoint import EndpointCreator, DEFAULT_TIMEOUT
from botocore.exceptions import ClientError, DataNotFoundError
from botocore.exceptions import OperationNotPageableError
from botocore.exceptions import InvalidS3AddressingStyleError
from botocore.hooks import first_non_none_response
from botocore.model import ServiceModel
from botocore.paginate import Paginator
from botocore.signers import RequestSigner
from botocore.utils import CachedProperty
from botocore.utils import get_service_module_name
from botocore.utils import fix_s3_host
from botocore.utils import switch_to_virtual_host_style
from botocore.docs.docstring import ClientMethodDocstring
from botocore.docs.docstring import PaginatorDocstring


logger = logging.getLogger(__name__)


class ClientCreator(object):
    """Creates client objects for a service."""
    def __init__(self, loader, endpoint_resolver, user_agent, event_emitter,
                 retry_handler_factory, retry_config_translator,
                 response_parser_factory=None):
        self._loader = loader
        self._endpoint_resolver = endpoint_resolver
        self._user_agent = user_agent
        self._event_emitter = event_emitter
        self._retry_handler_factory = retry_handler_factory
        self._retry_config_translator = retry_config_translator
        self._response_parser_factory = response_parser_factory

    def create_client(self, service_name, region_name, is_secure=True,
                      endpoint_url=None, verify=None,
                      credentials=None, scoped_config=None,
                      api_version=None,
                      client_config=None):
        service_model = self._load_service_model(service_name, api_version)
        cls = self._create_client_class(service_name, service_model)
        client_args = self._get_client_args(
            service_model, region_name, is_secure, endpoint_url,
            verify, credentials, scoped_config, client_config)
        return cls(**client_args)

    def create_client_class(self, service_name, api_version=None):
        service_model = self._load_service_model(service_name, api_version)
        return self._create_client_class(service_name, service_model)

    def _create_client_class(self, service_name, service_model):
        class_attributes = self._create_methods(service_model)
        py_name_to_operation_name = self._create_name_mapping(service_model)
        class_attributes['_PY_TO_OP_NAME'] = py_name_to_operation_name
        bases = [BaseClient]
        self._event_emitter.emit('creating-client-class.%s' % service_name,
                                 class_attributes=class_attributes,
                                 base_classes=bases)
        class_name = get_service_module_name(service_model)
        cls = type(str(class_name), tuple(bases), class_attributes)
        return cls

    def _load_service_model(self, service_name, api_version=None):
        json_model = self._loader.load_service_model(service_name, 'service-2',
                                                     api_version=api_version)
        service_model = ServiceModel(json_model, service_name=service_name)
        self._register_retries(service_model)
        return service_model

    def _register_retries(self, service_model):
        endpoint_prefix = service_model.endpoint_prefix

        # First, we load the entire retry config for all services,
        # then pull out just the information we need.
        original_config = self._loader.load_data('_retry')
        if not original_config:
            return

        retry_config = self._retry_config_translator.build_retry_config(
            endpoint_prefix, original_config.get('retry', {}),
            original_config.get('definitions', {}))

        logger.debug("Registering retry handlers for service: %s",
                     service_model.service_name)
        handler = self._retry_handler_factory.create_retry_handler(
            retry_config, endpoint_prefix)
        unique_id = 'retry-config-%s' % endpoint_prefix
        self._event_emitter.register('needs-retry.%s' % endpoint_prefix,
                                     handler, unique_id=unique_id)

    def _get_signature_version_and_region(self, service_model, region_name,
                                          is_secure, scoped_config,
                                          endpoint_url):
        # Get endpoint heuristic overrides before creating the
        # request signer.
        resolver = self._endpoint_resolver
        scheme = 'https' if is_secure else 'http'
        endpoint_config = resolver.construct_endpoint(
            service_model.endpoint_prefix, region_name, scheme=scheme)

        # Signature version override from endpoint.
        signature_version = service_model.signature_version
        if 'signatureVersion' in endpoint_config.get('properties', {}):
            signature_version = endpoint_config[
                'properties']['signatureVersion']

        # Signature overrides from a configuration file.
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

        # Determine the region name as well
        region_name = self._determine_region_name(
            endpoint_config, region_name, endpoint_url)

        return signature_version, region_name

    def _determine_region_name(self, endpoint_config, region_name=None,
                               endpoint_url=None):
        # This is a helper function to determine region name to use.
        # It will take into account whether the user passes in a region
        # name, whether there is a rule in the endpoint JSON, or
        # an endpoint url was provided.

        # We only support the credentialScope.region in the properties
        # bag right now, so if it's available, it will override the
        # provided region name.
        region_name_override = endpoint_config['properties'].get(
            'credentialScope', {}).get('region')

        if endpoint_url is not None:
            # If an endpoint_url is provided, do not use region name
            # override if a region was provided by the user.
            if region_name is not None:
                region_name_override = None

        if region_name_override is not None:
            # Letting the heuristics rule override the region_name
            # allows for having a default region of something like us-west-2
            # for IAM, but we still will know to use us-east-1 for sigv4.
            region_name = region_name_override

        return region_name

    def _inject_s3_configuration(self, config_kwargs, scoped_config,
                                 client_config):
        s3_configuration = None

        # Check the scoped config first
        if scoped_config is not None:
            s3_configuration = scoped_config.get('s3')

        # Next specfic client config values takes precedence over
        # specific values in the scoped config.
        if client_config is not None:
            if client_config.s3 is not None:
                if s3_configuration is None:
                    s3_configuration = client_config.s3
                else:
                    # The current s3_configuration dictionary may be
                    # from a source that only should be read from so
                    # we want to be safe and just make a copy of it to modify
                    # before it actually gets updated.
                    s3_configuration = s3_configuration.copy()
                    s3_configuration.update(client_config.s3)

        config_kwargs['s3'] = s3_configuration

    def _resolve_verify_value(self, provided_verify_value, scoped_config):
        # If a user provides a value for "verify" then we don't do anything.
        # We always use explicit values provided.
        if provided_verify_value is not None:
            return provided_verify_value
        elif scoped_config is not None:
            return scoped_config.get('ca_bundle')

    def _get_client_args(self, service_model, region_name, is_secure,
                         endpoint_url, verify, credentials,
                         scoped_config, client_config):

        protocol = service_model.metadata['protocol']
        serializer = botocore.serialize.create_serializer(
            protocol, include_validation=True)

        event_emitter = copy.copy(self._event_emitter)

        response_parser = botocore.parsers.create_parser(protocol)

        verify = self._resolve_verify_value(verify, scoped_config)
        # Determine what region the user provided either via the
        # region_name argument or the client_config.
        if region_name is None:
            if client_config and client_config.region_name is not None:
                region_name = client_config.region_name

        # Based on what the user provided use the scoped config file
        # to determine if the region is going to change and what
        # signature should be used.
        signature_version, region_name = \
            self._get_signature_version_and_region(
                service_model, region_name, is_secure, scoped_config,
                endpoint_url)

        # Override the signature if the user specifies it in the client
        # config.
        if client_config and client_config.signature_version is not None:
            signature_version = client_config.signature_version

        # Override the user agent if specified in the client config.
        user_agent = self._user_agent
        if client_config is not None:
            if client_config.user_agent is not None:
                user_agent = client_config.user_agent
            if client_config.user_agent_extra is not None:
                user_agent += ' %s' % client_config.user_agent_extra

        signer = RequestSigner(service_model.service_name, region_name,
                               service_model.signing_name,
                               signature_version, credentials,
                               event_emitter)

        # Create a new client config to be passed to the client based
        # on the final values. We do not want the user to be able
        # to try to modify an existing client with a client config.
        config_kwargs = dict(
            region_name=region_name, signature_version=signature_version,
            user_agent=user_agent)
        if client_config is not None:
            config_kwargs.update(
                connect_timeout=client_config.connect_timeout,
                read_timeout=client_config.read_timeout)

        # Add any additional s3 configuration for client
        self._inject_s3_configuration(
            config_kwargs, scoped_config, client_config)

        new_config = Config(**config_kwargs)

        endpoint_creator = EndpointCreator(self._endpoint_resolver,
                                           region_name, event_emitter)
        endpoint = endpoint_creator.create_endpoint(
            service_model, region_name, is_secure=is_secure,
            endpoint_url=endpoint_url, verify=verify,
            response_parser_factory=self._response_parser_factory,
            timeout=(new_config.connect_timeout, new_config.read_timeout))

        return {
            'serializer': serializer,
            'endpoint': endpoint,
            'response_parser': response_parser,
            'event_emitter': event_emitter,
            'request_signer': signer,
            'service_model': service_model,
            'loader': self._loader,
            'client_config': new_config
        }

    def _create_methods(self, service_model):
        op_dict = {}
        for operation_name in service_model.operation_names:
            py_operation_name = xform_name(operation_name)
            op_dict[py_operation_name] = self._create_api_method(
                py_operation_name, operation_name, service_model)
        return op_dict

    def _create_name_mapping(self, service_model):
        # py_name -> OperationName, for every operation available
        # for a service.
        mapping = {}
        for operation_name in service_model.operation_names:
            py_operation_name = xform_name(operation_name)
            mapping[py_operation_name] = operation_name
        return mapping

    def _create_api_method(self, py_operation_name, operation_name,
                           service_model):
        def _api_call(self, *args, **kwargs):
            # We're accepting *args so that we can give a more helpful
            # error message than TypeError: _api_call takes exactly
            # 1 argument.
            if args:
                raise TypeError(
                    "%s() only accepts keyword arguments." % py_operation_name)
            # The "self" in this scope is referring to the BaseClient.
            return self._make_api_call(operation_name, kwargs)

        _api_call.__name__ = str(py_operation_name)

        # Add the docstring to the client method
        operation_model = service_model.operation_model(operation_name)
        docstring = ClientMethodDocstring(
            operation_model=operation_model,
            method_name=operation_name,
            event_emitter=self._event_emitter,
            method_description=operation_model.documentation,
            example_prefix='response = client.%s' % py_operation_name,
            include_signature=False
        )
        _api_call.__doc__ = docstring
        return _api_call


class BaseClient(object):

    # This is actually reassigned with the py->op_name mapping
    # when the client creator creates the subclass.  This value is used
    # because calls such as client.get_paginator('list_objects') use the
    # snake_case name, but we need to know the ListObjects form.
    # xform_name() does the ListObjects->list_objects conversion, but
    # we need the reverse mapping here.
    _PY_TO_OP_NAME = {}

    def __init__(self, serializer, endpoint, response_parser,
                 event_emitter, request_signer, service_model, loader,
                 client_config):
        self._serializer = serializer
        self._endpoint = endpoint
        self._response_parser = response_parser
        self._request_signer = request_signer
        self._cache = {}
        self._loader = loader
        self._client_config = client_config
        self.meta = ClientMeta(event_emitter, self._client_config,
                               endpoint.host, service_model,
                               self._PY_TO_OP_NAME)
        self._register_handlers()

    def _register_handlers(self):
        # Register the handler required to sign requests.
        self.meta.events.register('request-created.%s' %
                                  self.meta.service_model.endpoint_prefix,
                                  self._request_signer.handler)

        # If the virtual host addressing style is being forced,
        # switch the default fix_s3_host handler for the more general
        # switch_to_virtual_host_style handler that does not have opt out
        # cases (other than throwing an error if the name is DNS incompatible)
        if self.meta.config.s3 is None:
            s3_addressing_style = None
        else:
            s3_addressing_style = self.meta.config.s3.get('addressing_style')

        if s3_addressing_style == 'path':
            self.meta.events.unregister('before-sign.s3', fix_s3_host)
        elif s3_addressing_style == 'virtual':
            self.meta.events.unregister('before-sign.s3', fix_s3_host)
            self.meta.events.register(
                'before-sign.s3', switch_to_virtual_host_style)

    @property
    def _service_model(self):
        return self.meta.service_model

    def _make_api_call(self, operation_name, api_params):
        request_context = {}
        operation_model = self._service_model.operation_model(operation_name)
        request_dict = self._convert_to_request_dict(
            api_params, operation_model, context=request_context)

        handler, event_response = self.meta.events.emit_until_response(
            'before-call.{endpoint_prefix}.{operation_name}'.format(
                endpoint_prefix=self._service_model.endpoint_prefix,
                operation_name=operation_name),
            model=operation_model, params=request_dict,
            request_signer=self._request_signer, context=request_context)

        if event_response is not None:
            http, parsed_response = event_response
        else:
            http, parsed_response = self._endpoint.make_request(
                operation_model, request_dict)

        self.meta.events.emit(
            'after-call.{endpoint_prefix}.{operation_name}'.format(
                endpoint_prefix=self._service_model.endpoint_prefix,
                operation_name=operation_name),
            http_response=http, parsed=parsed_response,
            model=operation_model, context=request_context
        )

        if http.status_code >= 300:
            raise ClientError(parsed_response, operation_name)
        else:
            return parsed_response

    def _convert_to_request_dict(self, api_params, operation_model,
                                 context=None):
        # Given the API params provided by the user and the operation_model
        # we can serialize the request to a request_dict.
        operation_name = operation_model.name

        # Emit an event that allows users to modify the parameters at the
        # beginning of the method. It allows handlers to modify existing
        # parameters or return a new set of parameters to use.
        responses = self.meta.events.emit(
            'provide-client-params.{endpoint_prefix}.{operation_name}'.format(
                endpoint_prefix=self._service_model.endpoint_prefix,
                operation_name=operation_name),
            params=api_params, model=operation_model, context=context)
        api_params = first_non_none_response(responses, default=api_params)

        event_name = (
            'before-parameter-build.{endpoint_prefix}.{operation_name}')
        self.meta.events.emit(
            event_name.format(
                endpoint_prefix=self._service_model.endpoint_prefix,
                operation_name=operation_name),
            params=api_params, model=operation_model, context=context)

        request_dict = self._serializer.serialize_to_request(
            api_params, operation_model)
        prepare_request_dict(request_dict, endpoint_url=self._endpoint.host,
                             user_agent=self._client_config.user_agent)
        return request_dict

    def get_paginator(self, operation_name):
        """Create a paginator for an operation.

        :type operation_name: string
        :param operation_name: The operation name.  This is the same name
            as the method name on the client.  For example, if the
            method name is ``create_foo``, and you'd normally invoke the
            operation as ``client.create_foo(**kwargs)``, if the
            ``create_foo`` operation can be paginated, you can use the
            call ``client.get_paginator("create_foo")``.

        :raise OperationNotPageableError: Raised if the operation is not
            pageable.  You can use the ``client.can_paginate`` method to
            check if an operation is pageable.

        :rtype: L{botocore.paginate.Paginator}
        :return: A paginator object.

        """
        if not self.can_paginate(operation_name):
            raise OperationNotPageableError(operation_name=operation_name)
        else:
            actual_operation_name = self._PY_TO_OP_NAME[operation_name]

            # Create a new paginate method that will serve as a proxy to
            # the underlying Paginator.paginate method. This is needed to
            # attach a docstring to the method.
            def paginate(self, **kwargs):
                return Paginator.paginate(self, **kwargs)

            paginator_config = self._cache['page_config'][
                actual_operation_name]
            # Add the docstring for the paginate method.
            paginate.__doc__ = PaginatorDocstring(
                paginator_name=actual_operation_name,
                event_emitter=self.meta.events,
                service_model=self.meta.service_model,
                paginator_config=paginator_config,
                include_signature=False
            )

            # Rename the paginator class based on the type of paginator.
            paginator_class_name = str('%s.Paginator.%s' % (
                get_service_module_name(self.meta.service_model),
                actual_operation_name))

            # Create the new paginator class
            documented_paginator_cls = type(
                paginator_class_name, (Paginator,), {'paginate': paginate})

            paginator = documented_paginator_cls(
                getattr(self, operation_name),
                paginator_config)
            return paginator

    def can_paginate(self, operation_name):
        """Check if an operation can be paginated.

        :type operation_name: string
        :param operation_name: The operation name.  This is the same name
            as the method name on the client.  For example, if the
            method name is ``create_foo``, and you'd normally invoke the
            operation as ``client.create_foo(**kwargs)``, if the
            ``create_foo`` operation can be paginated, you can use the
            call ``client.get_paginator("create_foo")``.

        :return: ``True`` if the operation can be paginated,
            ``False`` otherwise.

        """
        if 'page_config' not in self._cache:
            try:
                page_config = self._loader.load_service_model(
                    self._service_model.service_name,
                    'paginators-1',
                    self._service_model.api_version)['pagination']
                self._cache['page_config'] = page_config
            except DataNotFoundError:
                self._cache['page_config'] = {}
        actual_operation_name = self._PY_TO_OP_NAME[operation_name]
        return actual_operation_name in self._cache['page_config']

    def _get_waiter_config(self):
        if 'waiter_config' not in self._cache:
            try:
                waiter_config = self._loader.load_service_model(
                    self._service_model.service_name,
                    'waiters-2',
                    self._service_model.api_version)
                self._cache['waiter_config'] = waiter_config
            except DataNotFoundError:
                self._cache['waiter_config'] = {}
        return self._cache['waiter_config']

    def get_waiter(self, waiter_name):
        config = self._get_waiter_config()
        if not config:
            raise ValueError("Waiter does not exist: %s" % waiter_name)
        model = waiter.WaiterModel(config)
        mapping = {}
        for name in model.waiter_names:
            mapping[xform_name(name)] = name
        if waiter_name not in mapping:
            raise ValueError("Waiter does not exist: %s" % waiter_name)

        return waiter.create_waiter_with_client(
            mapping[waiter_name], model, self)

    @CachedProperty
    def waiter_names(self):
        """Returns a list of all available waiters."""
        config = self._get_waiter_config()
        if not config:
            return []
        model = waiter.WaiterModel(config)
        # Waiter configs is a dict, we just want the waiter names
        # which are the keys in the dict.
        return [xform_name(name) for name in model.waiter_names]


class ClientMeta(object):
    """Holds additional client methods.

    This class holds additional information for clients.  It exists for
    two reasons:

        * To give advanced functionality to clients
        * To namespace additional client attributes from the operation
          names which are mapped to methods at runtime.  This avoids
          ever running into collisions with operation names.

    """

    def __init__(self, events, client_config, endpoint_url, service_model,
                 method_to_api_mapping):
        self.events = events
        self._client_config = client_config
        self._endpoint_url = endpoint_url
        self._service_model = service_model
        self._method_to_api_mapping = method_to_api_mapping

    @property
    def service_model(self):
        return self._service_model

    @property
    def region_name(self):
        return self._client_config.region_name

    @property
    def endpoint_url(self):
        return self._endpoint_url

    @property
    def config(self):
        return self._client_config

    @property
    def method_to_api_mapping(self):
        return self._method_to_api_mapping


class Config(object):
    """Advanced configuration for Botocore clients.

    :type region_name: str
    :param region_name: The region to use in instantiating the client

    :type signature_version: str
    :param signature_version: The signature version when signing requests.

    :type user_agent: str
    :param user_agent: The value to use in the User-Agent header.

    :type user_agent_extra: str
    :param user_agent_extra: The value to append to the current User-Agent
        header value.

    :type connect_timeout: int
    :param connect_timeout: The time in seconds till a timeout exception is
        thrown when attempting to make a connection. The default is 60
        seconds.

    :type read_timeout: int
    :param read_timeout: The time in seconds till a timeout exception is
        thrown when attempting to read from a connection. The default is
        60 seconds.

    :type s3: dict
    :param s3: A dictionary of s3 specific configurations.
        Valid keys are:
            * 'addressing_style' -- Refers to the style in which to address
              s3 endpoints. Values must be a string that equals:
                  * auto -- Addressing style is chosen for user. Depending
                            on the configuration of client, the endpoint
                            may be addressed in the virtual or the path
                            style. Note that this is the default behavior if
                            no style is specified.
                  * virtual -- Addressing style is always virtual. The name of
                               the bucket must be DNS compatible or an
                               exception will be thrown. Endpoints will be
                               addressed as such: mybucket.s3.amazonaws.com
                  * path -- Addressing style is always by path. Endpoints will
                            be addressed as such: s3.amazonaws.com/mybucket
    """
    OPTION_DEFAULTS = OrderedDict([
        ('region_name', None),
        ('signature_version', None),
        ('user_agent', None),
        ('user_agent_extra', None),
        ('connect_timeout', DEFAULT_TIMEOUT),
        ('read_timeout', DEFAULT_TIMEOUT),
        ('s3', None)
    ])

    def __init__(self, *args, **kwargs):
        self._user_provided_options = self._record_user_provided_options(
            args, kwargs)

        # Merge the user_provided options onto the default options
        config_vars = copy.copy(self.OPTION_DEFAULTS)
        config_vars.update(self._user_provided_options)

        # Set the attributes based on the config_vars
        for key, value in config_vars.items():
            setattr(self, key, value)

        # Validate the s3 options
        self._validate_s3_configuration(self.s3)

    def _record_user_provided_options(self, args, kwargs):
        option_order = list(self.OPTION_DEFAULTS)
        user_provided_options = {}

        # Iterate through the kwargs passed through to the constructor and
        # map valid keys to the dictionary
        for key, value in kwargs.items():
            if key in self.OPTION_DEFAULTS:
                user_provided_options[key] = value
            # The key must exist in the available options
            else:
                raise TypeError(
                    'Got unexpected keyword argument \'%s\'' % key)

        # The number of args should not be longer than the allowed
        # options
        if len(args) > len(option_order):
            raise TypeError(
                'Takes at most %s arguments (%s given)' % (
                    len(option_order), len(args)))

        # Iterate through the args passed through to the constructor and map
        # them to appropriate keys.
        for i, arg in enumerate(args):
            # If it a kwarg was specified for the arg, then error out
            if option_order[i] in user_provided_options:
                raise TypeError(
                    'Got multiple values for keyword argument \'%s\'' % (
                        option_order[i]))
            user_provided_options[option_order[i]] = arg

        return user_provided_options

    def _validate_s3_configuration(self, s3):
        if s3 is not None:
            addressing_style = s3.get('addressing_style')
            if addressing_style not in ['virtual', 'auto', 'path', None]:
                raise InvalidS3AddressingStyleError(
                    s3_addressing_style=addressing_style)

    def merge(self, other_config):
        """Merges the config object with another config object

        This will merge in all non-default values from the provided config
        and return a new config object

        :type other_config: botocore.client.Config
        :param other config: Another config object to merge with. The values
            in the provided config object will take precedence in the merging

        :rtype: botocore.client.Config
        :returns: A config object built from the merged values of both
            config objects.
        """
        # Make a copy of the current attributes in the config object.
        config_options = copy.copy(self._user_provided_options)

        # Merge in the user provided options from the other config
        config_options.update(other_config._user_provided_options)

        # Return a new config object with the merged properties.
        return Config(**config_options)
