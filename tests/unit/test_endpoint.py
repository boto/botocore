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

from botocore.endpoint import get_endpoint, QueryEndpoint, JSONEndpoint, \
    RestEndpoint
from botocore.auth import SigV4Auth
from botocore.session import Session
from botocore.exceptions import UnknownServiceStyle
from botocore.exceptions import UnknownSignatureVersionError
from botocore.payload import Payload


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

    def test_get_query(self):
        service = self.create_mock_service('query')
        endpoint = get_endpoint(service, 'us-west-2',
                                'https://service.region.amazonaws.com')
        self.assertIsInstance(endpoint, QueryEndpoint)

    def test_get_json(self):
        service = self.create_mock_service('json')
        endpoint = get_endpoint(service, 'us-west-2',
                                'https://service.region.amazonaws.com')
        self.assertIsInstance(endpoint, JSONEndpoint)

    def test_get_rest_xml(self):
        service = self.create_mock_service('rest-xml')
        endpoint = get_endpoint(service, 'us-west-2',
                                'https://service.region.amazonaws.com')
        self.assertIsInstance(endpoint, RestEndpoint)

    def test_get_rest_json(self):
        service = self.create_mock_service('rest-json')
        endpoint = get_endpoint(service, 'us-west-2',
                                'https://service.region.amazonaws.com')
        self.assertIsInstance(endpoint, RestEndpoint)

    def test_unknown_service(self):
        service = self.create_mock_service('rest-query-xml-json')
        with self.assertRaises(UnknownServiceStyle):
            endpoint = get_endpoint(service, 'us-west-2',
                                    'https://service.region.amazonaws.com')

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

    def test_omitted_auth_handler(self):
        service = self.create_mock_service('query', signature_version=None)
        del service.signature_version
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
        self.op.is_streaming.return_value = False
        self.signature_version = True
        self.auth = Mock()
        self.endpoint = self.ENDPOINT_CLASS(
            self.service, 'us-west-2', 'https://ec2.us-west-2.amazonaws.com/',
            auth=self.auth)
        self.http_session = Mock()
        self.http_session.send.return_value = sentinel.HTTP_RETURN_VALUE
        self.endpoint.http_session = self.http_session
        self.get_response_patch = patch('botocore.response.get_response')
        self.get_response = self.get_response_patch.start()

    def tearDown(self):
        self.get_response_patch.stop()


class TestQueryEndpoint(TestEndpointBase):
    ENDPOINT_CLASS = QueryEndpoint

    def test_make_request(self):
        self.endpoint.make_request(self.op, {})
        # Should have authenticated the request
        self.assertTrue(self.auth.add_auth.called)
        request = self.auth.add_auth.call_args[1]['request']
        # http_session should be used to send the request.
        self.assertTrue(self.http_session.send.called)
        prepared_request = self.http_session.send.call_args[0][0]
        self.http_session.send.assert_called_with(
            prepared_request, verify=True, stream=False,
            proxies={})
        self.get_response.assert_called_with(self.service.session,
            self.op, sentinel.HTTP_RETURN_VALUE)

    def test_make_request_with_proxies(self):
        proxies = {'http': 'http://localhost:8888'}
        self.endpoint.proxies = proxies
        self.endpoint.make_request(self.op, {})
        prepared_request = self.http_session.send.call_args[0][0]
        self.http_session.send.assert_called_with(
            prepared_request, verify=True, stream=False,
            proxies=proxies)

    def test_make_request_with_no_auth(self):
        self.endpoint.auth = None
        self.endpoint.make_request(self.op, {})

        # http_session should be used to send the request.
        self.assertTrue(self.http_session.send.called)
        prepared_request = self.http_session.send.call_args[0][0]
        self.assertNotIn('Authorization', prepared_request.headers)


class TestQueryEndpointAnonymousOp(TestQueryEndpoint):

    def setUp(self):
        super(TestQueryEndpointAnonymousOp, self).setUp()
        self.op.signature_version = None

    def test_make_request(self):
        self.endpoint.make_request(self.op, {})
        # Should have authenticated the request
        self.assertFalse(self.auth.add_auth.called)
        # http_session should be used to send the request.
        self.assertTrue(self.http_session.send.called)
        prepared_request = self.http_session.send.call_args[0][0]
        self.http_session.send.assert_called_with(
            prepared_request, verify=True, stream=False,
            proxies={})
        self.get_response.assert_called_with(self.service.session,
            self.op, sentinel.HTTP_RETURN_VALUE)


class TestJSONEndpoint(TestEndpointBase):
    ENDPOINT_CLASS = JSONEndpoint

    def test_make_request(self):
        self.endpoint.make_request(self.op, {})
        self.assertTrue(self.auth.add_auth.called)
        self.assertTrue(self.http_session.send.called)
        prepared_request = self.http_session.send.call_args[0][0]
        self.http_session.send.assert_called_with(
            prepared_request, verify=True, stream=False,
            proxies={})


class TestJSONEndpointAnonymousOp(TestJSONEndpoint):

    def setUp(self):
        super(TestJSONEndpointAnonymousOp, self).setUp()
        self.op.signature_version = None

    def test_make_request(self):
        self.endpoint.make_request(self.op, {})
        self.assertFalse(self.auth.add_auth.called)
        self.assertTrue(self.http_session.send.called)
        prepared_request = self.http_session.send.call_args[0][0]
        self.http_session.send.assert_called_with(
            prepared_request, verify=True, stream=False,
            proxies={})


class TestRestEndpoint(TestEndpointBase):
    ENDPOINT_CLASS = RestEndpoint

    def test_make_request(self):
        self.op.http = {'uri': '/foo', 'method': 'POST'}
        self.endpoint.make_request(self.op, {
            'headers': {}, 'uri_params': {}, 'payload': None})
        self.assertTrue(self.auth.add_auth.called)
        prepared_request = self.http_session.send.call_args[0][0]
        self.http_session.send.assert_called_with(
            prepared_request, verify=True, stream=False,
            proxies={})


class TestRestEndpointAnonymousOp(TestRestEndpoint):

    def setUp(self):
        super(TestRestEndpointAnonymousOp, self).setUp()
        self.op.signature_version = None

    def test_make_request(self):
        self.op.http = {'uri': '/foo', 'method': 'POST'}
        self.endpoint.make_request(self.op, {
            'headers': {}, 'uri_params': {}, 'payload': None})
        self.assertFalse(self.auth.add_auth.called)
        prepared_request = self.http_session.send.call_args[0][0]
        self.http_session.send.assert_called_with(
            prepared_request, verify=True, stream=False,
            proxies={})


class TestRetryInterface(BaseSessionTest):
    def setUp(self):
        super(TestRetryInterface, self).setUp()
        self.total_calls = 0
        self.auth = Mock()
        self.session = create_session(include_builtin_handlers=False)
        self.service = Mock()
        self.service.endpoint_prefix = 'ec2'
        self.service.session = self.session
        self.endpoint = QueryEndpoint(
            self.service, 'us-west-2', 'https://ec2.us-west-2.amazonaws.com/',
            auth=self.auth)
        self.http_session = Mock()
        self.endpoint.http_session = self.http_session
        self.get_response_patch = patch('botocore.response.get_response')
        self.get_response = self.get_response_patch.start()
        self.retried_on_exception = None

    def tearDown(self):
        self.get_response_patch.stop()

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
        emitted_events = []
        self.session.register('needs-retry.ec2.DescribeInstances',
                              lambda **kwargs: emitted_events.append(kwargs))
        op = Mock()
        op.name = 'DescribeInstances'
        self.endpoint.make_request(op, {})
        self.assertEqual(len(emitted_events), 1)
        self.assertEqual(emitted_events[0]['event_name'],
                         'needs-retry.ec2.DescribeInstances')

    def test_retry_events_can_alter_behavior(self):
        self.session.register('needs-retry.ec2.DescribeInstances',
                              self.max_attempts_retry_handler)
        op = Mock()
        op.name = 'DescribeInstances'
        self.endpoint.make_request(op, {})
        self.assertEqual(self.total_calls, 3)

    def test_retry_on_socket_errors(self):
        self.session.register('needs-retry.ec2.DescribeInstances',
                              self.connection_error_handler)
        op = Mock()
        op.name = 'DescribeInstances'
        self.http_session.send.side_effect = ConnectionError()
        self.endpoint.make_request(op, {})
        self.assertEqual(self.total_calls, 3)


class TestResetStreamOnRetry(unittest.TestCase):
    def setUp(self):
        super(TestResetStreamOnRetry, self).setUp()
        self.total_calls = 0
        self.auth = Mock()
        self.session = create_session(include_builtin_handlers=False)
        self.service = Mock()
        self.service.endpoint_prefix = 's3'
        self.service.session = self.session
        self.endpoint = RestEndpoint(
            self.service, 'us-east-1', 'https://s3.amazonaws.com/',
            auth=self.auth)
        self.http_session = Mock()
        self.endpoint.http_session = self.http_session
        self.get_response_patch = patch('botocore.response.get_response')
        self.get_response = self.get_response_patch.start()
        self.retried_on_exception = None

    def tearDown(self):
        self.get_response_patch.stop()

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
        # It doesn't really matter what the operation is, we will
        # check in general if we're
        self.session.register('needs-retry.s3.PutObject',
                              self.max_attempts_retry_handler)
        op = Mock()
        payload = Payload()
        payload.literal_value = RecordStreamResets('foobar')
        op.name = 'PutObject'
        op.http = {'uri': '', 'method': 'POST'}
        self.endpoint.make_request(op, {'headers': {}, 'payload': payload})
        self.assertEqual(self.total_calls, 3)
        self.assertEqual(payload.literal_value.total_resets, 2)


class TestRestEndpoint(unittest.TestCase):

    def test_encode_uri_params_unicode(self):
        uri = '/{foo}/{bar}'
        operation = Mock()
        operation.http = {'uri': uri}
        params = {'uri_params': {'foo': u'\u2713', 'bar': 'bar'}}
        endpoint = RestEndpoint(Mock(), None, None, None)
        built_uri = endpoint.build_uri(operation, params)
        self.assertEqual(built_uri, '/%E2%9C%93/bar?')

    def test_quote_uri_safe_key(self):
        uri = '/{foo}/{bar}'
        operation = Mock()
        operation.http = {'uri': uri}
        params = {'uri_params': {'foo': 'foo', 'bar': 'bar~'}}
        endpoint = RestEndpoint(Mock(), None, None, None)
        built_uri = endpoint.build_uri(operation, params)
        self.assertEqual(built_uri, '/foo/bar~?')


if __name__ == '__main__':
    unittest.main()
