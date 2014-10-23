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

from tests import unittest, BaseSessionTest, create_session

from mock import Mock, patch, sentinel
from botocore.vendored.requests import ConnectionError
import six

from botocore.endpoint import get_endpoint, Endpoint, DEFAULT_TIMEOUT
from botocore.endpoint import EndpointCreator
from botocore.auth import SigV4Auth
from botocore.session import Session
from botocore.exceptions import UnknownServiceStyle
from botocore.exceptions import UnknownSignatureVersionError


def request_dict():
    return {
        'headers': {},
        'body': '',
        'url_path': '/',
        'query_string': '',
        'method': 'POST',
    }


class RecordStreamResets(six.StringIO):
    def __init__(self, value):
        six.StringIO.__init__(self, value)
        self.total_resets = 0

    def seek(self, where):
        self.total_resets += 1
        six.StringIO.seek(self, where)


class TestGetEndpoint(unittest.TestCase):
    def setUp(self):
        self.environ = {}
        self.environ_patch = patch('os.environ', self.environ)
        self.environ_patch.start()

    def tearDown(self):
        self.environ_patch.stop()

    def create_mock_service(self, service_type, signature_version='v2'):
        service = Mock()
        service.type = service_type
        service.signature_version = signature_version
        return service

    def test_auth_is_properly_created_for_endpoint(self):
        service = self.create_mock_service('query', signature_version='v4')
        endpoint = get_endpoint(service, 'us-west-2',
                                'https://service.region.amazonaws.com')
        self.assertIsInstance(endpoint.auth, SigV4Auth)

    def test_unknown_auth_handler(self):
        service = self.create_mock_service('query', signature_version='v5000')
        with self.assertRaises(UnknownSignatureVersionError):
            endpoint = get_endpoint(service, 'us-west-2',
                                    'https://service.region.amazonaws.com')

    def test_signature_version_is_none(self):
        # If signature_version is set to None, we don't assign any auth classes
        # to the endpoint.
        service = self.create_mock_service('query', signature_version=None)
        # Verify we have a signature_version attr and that it's None.  This is
        # a different case from not having the 'signature_version' at all.
        self.assertIsNone(service.signature_version)
        endpoint = get_endpoint(service, 'us-west-2',
                                'https://service.region.amazonaws.com')
        self.assertIsNone(endpoint.auth)

    def test_get_endpoint_default_verify_ssl(self):
        service = self.create_mock_service('query')
        endpoint = get_endpoint(service, 'us-west-2',
                                'https://service.region.amazonaws.com')
        self.assertTrue(endpoint.verify)

    def test_verify_ssl_can_be_disabled(self):
        service = self.create_mock_service('query')
        endpoint = get_endpoint(service, 'us-west-2',
                                'https://service.region.amazonaws.com',
                                verify=False)
        self.assertFalse(endpoint.verify)

    def test_verify_ssl_can_specify_cert_bundle(self):
        service = self.create_mock_service('query')
        endpoint = get_endpoint(service, 'us-west-2',
                                'https://service.region.amazonaws.com',
                                verify='/path/cacerts.pem')
        self.assertEqual(endpoint.verify, '/path/cacerts.pem')

    def test_honor_cert_bundle_env_var(self):
        self.environ['REQUESTS_CA_BUNDLE'] = '/env/cacerts.pem'
        service = self.create_mock_service('query')
        endpoint = get_endpoint(service, 'us-west-2',
                                'https://service.region.amazonaws.com')
        self.assertEqual(endpoint.verify, '/env/cacerts.pem')

    def test_env_ignored_if_explicitly_passed(self):
        self.environ['REQUESTS_CA_BUNDLE'] = '/env/cacerts.pem'
        service = self.create_mock_service('query')
        endpoint = get_endpoint(service, 'us-west-2',
                                'https://service.region.amazonaws.com',
                                verify='/path/cacerts.pem')
        # /path/cacerts.pem wins over the value from the env var.
        self.assertEqual(endpoint.verify, '/path/cacerts.pem')


class TestEndpointBase(unittest.TestCase):

    def setUp(self):
        self.service = Mock()
        self.service.session.user_agent.return_value = 'botocore-test'
        self.service.session.emit_first_non_none_response.return_value = None
        self.op = Mock()
        self.op.has_streaming_output = False
        self.signature_version = True
        self.auth = Mock()
        self.event_emitter = Mock()
        self.event_emitter.emit.return_value = []
        self.endpoint = Endpoint(
            'us-west-2', 'https://ec2.us-west-2.amazonaws.com/',
            auth=self.auth, user_agent='botoore', signature_version='v4',
            endpoint_prefix='ec2', event_emitter=self.event_emitter)
        self.http_session = Mock()
        self.http_session.send.return_value = sentinel.HTTP_RETURN_VALUE
        self.endpoint.http_session = self.http_session
        self.get_response_patch = patch('botocore.response.get_response')
        self.get_response = self.get_response_patch.start()

    def tearDown(self):
        self.get_response_patch.stop()


class TestEndpointFeatures(TestEndpointBase):

    def test_timeout_can_be_specified(self):
        timeout_override = 120
        self.endpoint.timeout = timeout_override
        self.endpoint.make_request(self.op, request_dict())
        kwargs = self.http_session.send.call_args[1]
        self.assertEqual(kwargs['timeout'], timeout_override)

    def test_make_request_with_proxies(self):
        proxies = {'http': 'http://localhost:8888'}
        self.endpoint.proxies = proxies
        self.endpoint.make_request(self.op, request_dict())
        prepared_request = self.http_session.send.call_args[0][0]
        self.http_session.send.assert_called_with(
            prepared_request, verify=True, stream=False,
            proxies=proxies, timeout=DEFAULT_TIMEOUT)


    def test_make_request_with_no_auth(self):
        self.endpoint.auth = None
        self.endpoint.make_request(self.op, request_dict())

        # http_session should be used to send the request.
        self.assertTrue(self.http_session.send.called)
        prepared_request = self.http_session.send.call_args[0][0]
        self.assertNotIn('Authorization', prepared_request.headers)


class TestRetryInterface(TestEndpointBase):
    def setUp(self):
        super(TestRetryInterface, self).setUp()
        self.retried_on_exception = None

    def max_attempts_retry_handler(self, attempts, **kwargs):
        # Simulate a max requests of 3.
        self.total_calls += 1
        if attempts == 3:
            return None
        else:
            # Returning anything non-None will trigger a retry,
            # but 0 here is so that time.sleep(0) happens.
            return 0

    def connection_error_handler(self, attempts, caught_exception, **kwargs):
        self.total_calls += 1
        if attempts == 3:
            return None
        elif isinstance(caught_exception, ConnectionError):
            # Returning anything non-None will trigger a retry,
            # but 0 here is so that time.sleep(0) happens.
            return 0
        else:
            return None

    def test_retry_events_are_emitted(self):
        op = Mock()
        op.name = 'DescribeInstances'
        self.endpoint.make_request(op, request_dict())
        call_args = self.event_emitter.emit.call_args
        self.assertEqual(call_args[0][0],
                         'needs-retry.ec2.DescribeInstances')

    def test_retry_events_can_alter_behavior(self):
        op = Mock()
        op.name = 'DescribeInstances'
        self.event_emitter.emit.side_effect = [
            [], # For initially preparing request
            [(None, 0)],  # Check if retry needed. Retry needed.
            [],  # For preparing the request again
            [(None, None)]  # Check if retry needed. Retry not needed.
        ]
        self.endpoint.make_request(op, request_dict())
        call_args = self.event_emitter.emit.call_args_list
        self.assertEqual(self.event_emitter.emit.call_count, 4)
        # Check that all of the events are as expected.
        self.assertEqual(call_args[0][0][0],
                         'before-auth.ec2')
        self.assertEqual(call_args[1][0][0],
                         'needs-retry.ec2.DescribeInstances')
        self.assertEqual(call_args[2][0][0],
                         'before-auth.ec2')
        self.assertEqual(call_args[3][0][0],
                         'needs-retry.ec2.DescribeInstances')

    def test_retry_on_socket_errors(self):
        op = Mock()
        op.name = 'DescribeInstances'
        self.event_emitter.emit.side_effect = [
            [], # For initially preparing request
            [(None, 0)],  # Check if retry needed. Retry needed.
            [],  # For preparing the request again
            [(None, None)]  # Check if retry needed. Retry not needed.
        ]
        self.http_session.send.side_effect = ConnectionError()
        self.endpoint.make_request(op, request_dict())
        call_args = self.event_emitter.emit.call_args_list
        self.assertEqual(self.event_emitter.emit.call_count, 4)
        # Check that all of the events are as expected.
        self.assertEqual(call_args[0][0][0],
                         'before-auth.ec2')
        self.assertEqual(call_args[1][0][0],
                         'needs-retry.ec2.DescribeInstances')
        self.assertEqual(call_args[2][0][0],
                         'before-auth.ec2')
        self.assertEqual(call_args[3][0][0],
                         'needs-retry.ec2.DescribeInstances')


class TestS3ResetStreamOnRetry(TestEndpointBase):
    def setUp(self):
        super(TestS3ResetStreamOnRetry, self).setUp()

    def max_attempts_retry_handler(self, attempts, **kwargs):
        # Simulate a max requests of 3.
        self.total_calls += 1
        if attempts == 3:
            return None
        else:
            # Returning anything non-None will trigger a retry,
            # but 0 here is so that time.sleep(0) happens.
            return 0

    def test_reset_stream_on_retry(self):
        op = Mock()
        body = RecordStreamResets('foobar')
        op.name = 'PutObject'
        op.has_streaming_output = True
        request = request_dict()
        request['body'] = body
        self.event_emitter.emit.side_effect = [
            [(None, 0)],  # Prepare initial request.
            [(None, 0)],  # Check if retry needed. Needs Retry.
            [(None, 0)],  # Prepare request again.
            [(None, 0)],  # Check if retry needed again. Needs Retry.
            [(None, 0)],  # Prepare request again.
            [(None, None)], # Finally emit no rety is needed.
        ]
        self.endpoint.make_request(op, request)
        self.assertEqual(body.total_resets, 2)


class TestEndpointCreator(unittest.TestCase):
    def setUp(self):
        self.service_model = Mock(
            endpoint_prefix='ec2', signature_version='v2',
            signing_name='ec2')

    def test_endpoint_resolver_with_configured_region_name(self):
        resolver = Mock()
        resolver.construct_endpoint.return_value = {
            'uri': 'https://endpoint.url', 'properties': {}
        }
        creator = EndpointCreator(resolver, 'us-west-2',
                                  Mock(), Mock(), 'user-agent')
        endpoint = creator.create_endpoint(self.service_model)
        self.assertEqual(endpoint.host, 'https://endpoint.url')

    def test_endpoint_resolver_uses_credential_scope(self):
        resolver = Mock()
        resolver_region_override = 'us-east-1'
        resolver.construct_endpoint.return_value = {
            'uri': 'https://endpoint.url',
            'properties': {
                'credentialScope': {
                    'region': resolver_region_override,
                }
            }
        }
        original_region_name = 'us-west-2'
        creator = EndpointCreator(resolver, original_region_name,
                                  Mock(), Mock(), 'user-agent')
        endpoint = creator.create_endpoint(self.service_model)
        self.assertEqual(endpoint.region_name, 'us-east-1')

    def test_endpoint_resolver_uses_signature_version(self):
        resolver = Mock()
        resolver.construct_endpoint.return_value = {
            'uri': 'https://endpoint.url',
            'properties': {
                # Setting a signatureVersion in the properties
                # back of an endpoint heuristic will override
                # any other value when constructing an endpoint.
                'signatureVersion': 'v4',
            }
        }
        creator = EndpointCreator(resolver, 'us-west-2',
                                  Mock(), Mock(), 'user-agent')
        endpoint = creator.create_endpoint(self.service_model)
        self.assertIsInstance(endpoint.auth, SigV4Auth)
