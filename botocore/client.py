from botocore.model import ServiceModel
from botocore.exceptions import ParamValidationError
from botocore.exceptions import DataNotFoundError
from botocore.exceptions import OperationNotPageableError
from botocore import xform_name
from botocore.paginate import Paginator
import botocore.validate
import botocore.serialize
from botocore import credentials


class ClientError(Exception):
    MSG_TEMPLATE = (
        'An error occurred ({error_code}) when calling the {operation_name} '
        'operation: {error_message}')

    def __init__(self, error_response, operation_name):
        msg = self.MSG_TEMPLATE.format(
            error_code=error_response['Error']['Code'],
            error_message=error_response['Error']['Message'],
            operation_name=operation_name)
        super(ClientError, self).__init__(msg)
        self.response = error_response


class ClientCreator(object):
    """Creates client objects for a service."""
    def __init__(self, loader, endpoint_creator):
        self._loader = loader
        self._endpoint_creator = endpoint_creator

    def create_client(self, service_name, region_name, is_secure=True,
                      endpoint_url=None, verify=None,
                      aws_access_key_id=None, aws_secret_access_key=None,
                      aws_session_token=None):
        service_model = self._load_service_model(service_name)
        cls = self.create_client_class(service_name)
        client_args = self._get_client_args(
            service_model, region_name, is_secure, endpoint_url,
            verify, aws_access_key_id, aws_secret_access_key,
            aws_session_token)
        return cls(**client_args)

    def create_client_class(self, service_name):
        service_model = self._load_service_model(service_name)
        methods = self._create_methods(service_model)
        py_name_to_operation_name = self._create_name_mapping(service_model)
        self._add_pagination_methods(service_model, methods,
                                     py_name_to_operation_name)
        cls = type(service_name, (BaseClient,), methods)
        return cls

    def _add_pagination_methods(self, service_model, methods, name_mapping):
        loader = self._loader

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
            # Note that the 'self' in this method refers to the self on
            # BaseClient, not on ClientCreator.
            if not self.can_paginate(operation_name):
                raise OperationNotPageableError(operation_name=operation_name)
            else:
                actual_operation_name = name_mapping[operation_name]
                paginator = Paginator(
                    getattr(self, operation_name),
                    self._cache['page_config'][actual_operation_name])
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
                    page_config = loader.load_data('aws/%s/%s.paginators' % (
                        service_model.endpoint_prefix,
                        service_model.api_version))['pagination']
                    self._cache['page_config'] = page_config
                except DataNotFoundError:
                    self._cache['page_config'] = {}
            actual_operation_name = name_mapping[operation_name]
            return actual_operation_name in self._cache['page_config']

        methods['get_paginator'] = get_paginator
        methods['can_paginate'] = can_paginate

    def _load_service_model(self, service_name):
        json_model = self._loader.load_service_model('aws/%s' % service_name)
        service_model = ServiceModel(json_model)
        return service_model

    def _get_client_args(self, service_model, region_name, is_secure,
                         endpoint_url, verify, aws_access_key_id,
                         aws_secret_access_key, aws_session_token):
        # A client needs:
        #
        # * serializer
        # * endpoint
        # * response parser
        protocol = service_model.metadata['protocol']
        serializer = botocore.serialize.create_serializer(
            protocol, include_validation=True)
        creds = None
        if aws_secret_access_key is not None:
            creds = credentials.Credentials(
                access_key=aws_access_key_id,
                secret_key=aws_secret_access_key,
                token=aws_session_token)
        endpoint = self._endpoint_creator.create_endpoint(
            service_model, region_name, is_secure=is_secure,
            endpoint_url=endpoint_url, verify=verify,
            credentials=creds)
        response_parser = botocore.parsers.create_parser(protocol)
        return {
            'serializer': serializer,
            'endpoint': endpoint,
            'response_parser': response_parser
        }

    def _create_methods(self, service_model):
        op_dict = {}
        for operation_name in service_model.operation_names:
            py_operation_name = xform_name(operation_name)
            op_dict[py_operation_name] = self._create_api_method(
                py_operation_name, operation_name, service_model)
        return op_dict

    def _create_name_mapping(self, service_model):
        # py_name -> OperationName
        mapping = {}
        for operation_name in service_model.operation_names:
            py_operation_name = xform_name(operation_name)
            mapping[py_operation_name] = operation_name
        return mapping

    def _create_api_method(self, py_operation_name, operation_name,
                           service_model):
        def _api_call(self, **kwargs):
            operation_model = service_model.operation_model(operation_name)
            request_dict = self._serializer.serialize_to_request(
                kwargs, operation_model)

            http, parsed_response = self._endpoint.make_request(
                operation_model, request_dict)
            if http.status_code >= 300:
                raise ClientError(parsed_response, operation_name)
            else:
                return parsed_response

        _api_call.__name__ = str(py_operation_name)
        # TODO: docstrings.
        return _api_call


class BaseClient(object):

    def __init__(self, serializer, endpoint, response_parser):
        self._serializer = serializer
        self._endpoint = endpoint
        self._response_parser = response_parser
        self._cache = {}
