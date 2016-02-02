# Copyright 2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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
from collections import deque
from botocore.validate import validate_parameters
from botocore.exceptions import ParamValidationError, StubResponseError
from botocore.vendored.requests.models import Response


class Stubber(object):
    """
    This class will allow you to stub out requests so you don't have to hit
    an endpoint to write tests. Responses are returned first in, first out.
    If operations are called out of order, or are called with no remaining
    queued responses, an error will be raised.

    Example::
        import datetime
        import botocore.session
        from botocore.stub import Stubber


        s3 = botocore.session.get_session().create_client('s3')
        stubber = Stubber(s3)

        response = {
            'IsTruncated': False,
            'Name': 'test-bucket',
            'MaxKeys': 1000, 'Prefix': '',
            'Contents': [{
                'Key': 'test.txt',
                'ETag': '"abc123"',
                'StorageClass': 'STANDARD',
                'LastModified': datetime.datetime(2016, 1, 20, 22, 9),
                'Owner': {'ID': 'abc123', 'DisplayName': 'myname'},
                'Size': 14814
            }],
            'EncodingType': 'url',
            'ResponseMetadata': {
                'RequestId': 'abc123',
                'HTTPStatusCode': 200,
                'HostId': 'abc123'
            },
            'Marker': ''
        }

        stubber.add_response('list_objects', response)
        stubber.activate()

        service_response = s3.list_objects(Bucket='test-bucket')
        assert service_response == response
    """
    def __init__(self, client):
        """
        :param client: The client to add your stubs to.
        """
        self.client = client
        self._event_id = 'boto_stubber'
        self._queue = deque()

    def activate(self):
        """
        Activates the stubber on the client
        """
        self.client.meta.events.register(
                'before-call.*.*',
                self._get_response_handler,
                unique_id=self._event_id)

    def deactivate(self):
        """
        Deactivates the stubber on the client
        """
        self.client.meta.events.unregister(
                'before-call.*.*',
                self._get_response_handler,
                unique_id=self._event_id)

    def add_response(self, method, service_response):
        """
        Adds a service response to the response queue. This will be validated
        against the service model to ensure correctness. It should be noted,
        however, that while missing attributes are often considered correct,
        your code may not function properly if you leave them out. Therefore
        you should always fill in every value you see in a typical response for
        your particular request.

        :param method: The name of the client method to stub.
        :type method: str

        :param service_response: A dict response stub. Provided parameters will
            be validated against the service model.
        :type service_response: dict
        """
        self._add_response(method, service_response)

    def _add_response(self, method, service_response, http_response=None):
        if not hasattr(self.client, method):
            raise ValueError(
                "Client %s does not have method: %s"
                % (self.client.meta.service_model.service_name, method))

        if http_response is None:
            http_response = Response()
            http_response.status_code = 200
            http_response.reason = 'OK'

        operation_name = self.client.meta.method_to_api_mapping.get(method)
        self._validate_response(operation_name, service_response)

        response = (operation_name, (http_response, service_response))
        self._queue.append(response)

    def add_client_error(self, method, service_error_code='',
                         service_message='', http_status_code=400):
        """
        Adds a ClientError to the response queue.

        :param method: The name of the service method to return the error on.
        :type method: str

        :param service_error_code: The service error code to return,
                                   e.g. NoSuchBucket
        :type service_error_code: str

        :param service_message: The service message to return, e.g.
                        'The specified bucket does not exist.'
        :type service_message: str

        :param http_status_code: The HTTP status code to return, e.g. 404, etc
        :type http_status_code: int
        """
        http_response = Response()
        http_response.status_code = http_status_code

        # We don't look to the model to build this because the caller would need
        # to know the details of what the HTTP body would need to look like.
        parsed_response = {
            'ResponseMetadata': {'HTTPStatusCode': http_status_code},
            'Error': {
                'Message': service_message,
                'Code': service_error_code
            }
        }

        operation_name = self.client.meta.method_to_api_mapping.get(method)
        response = (operation_name, (http_response, parsed_response))
        self._queue.append(response)

    def assert_no_pending_responses(self):
        """
        Asserts that all expected calls were made.
        """
        remaining = len(self._queue)
        if remaining != 0:
            raise AssertionError("%d responses remaining in queue." % remaining)

    def _get_response_handler(self, model, params, **kwargs):
        if not self._queue:
            raise StubResponseError(
                operation_name=model.name,
                reason='Unexpected API Call: called with parameters %s' %
                       params)

        name, response = self._queue.popleft()
        if name != model.name:
            raise StubResponseError(
                operation_name=model.name,
                reason='Operation mismatch: found response for %s.' % name)

        return response

    def _validate_response(self, operation_name, service_response):
        service_model = self.client.meta.service_model
        operation_model = service_model.operation_model(operation_name)
        output_shape = operation_model.output_shape

        # Remove ResponseMetadata so that the validator doesn't attempt to
        # perform validation on it.
        response = service_response
        if 'ResponseMetadata' in response:
            response = copy.copy(service_response)
            del response['ResponseMetadata']

        if output_shape is not None:
            validate_parameters(response, output_shape)
        elif response:
            # If the output shape is None, that means the response should be
            # empty apart from ResponseMetadata
            raise ParamValidationError(
                report="Service response should only contain ResponseMetadata.")
