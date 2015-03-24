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

from tests import unittest

from mock import Mock, patch
from botocore.vendored.requests import ConnectionError

from botocore.compat import six
from botocore.awsrequest import AWSRequest
from botocore.endpoint import get_endpoint, Endpoint, DEFAULT_TIMEOUT
from botocore.endpoint import EndpointCreator
from botocore.endpoint import PreserveAuthSession
from botocore.endpoint import RequestCreator
from botocore.exceptions import EndpointConnectionError
from botocore.exceptions import BaseEndpointResolverError


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
        self.op = Mock()
        self.op.has_streaming_output = False
        self.op.metadata = {'protocol': 'json'}
        self.event_emitter = Mock()
        self.event_emitter.emit.return_value = []
        self.factory_patch = patch(
            'botocore.parsers.ResponseParserFactory')
        self.factory = self.factory_patch.start()
        self.endpoint = Endpoint(
            'us-west-2', 'https://ec2.us-west-2.amazonaws.com/',
            user_agent='botoore', endpoint_prefix='ec2',
            event_emitter=self.event_emitter)
        self.http_session = Mock()
        self.http_session.send.return_value = Mock(
            status_code=200, headers={}, content=b'{"Foo": "bar"}',
        )
        self.endpoint.http_session = self.http_session

    def tearDown(self):
        self.factory_patch.stop()


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

    def test_make_request_no_signature_version(self):
        self.endpoint = Endpoint(
            'us-west-2', 'https://ec2.us-west-2.amazonaws.com/',
            user_agent='botoore',
            endpoint_prefix='ec2', event_emitter=self.event_emitter)
        self.endpoint.http_session = self.http_session

        self.endpoint.make_request(self.op, request_dict())

        # http_session should be used to send the request.
        self.assertTrue(self.http_session.send.called)
        prepared_request = self.http_session.send.call_args[0][0]
        self.assertNotIn('Authorization', prepared_request.headers)

    def test_make_request_injects_better_dns_error_msg(self):
        self.endpoint = Endpoint(
            'us-west-2', 'https://ec2.us-west-2.amazonaws.com/',
            user_agent='botoore',
            endpoint_prefix='ec2', event_emitter=self.event_emitter)
        self.endpoint.http_session = self.http_session
        fake_request = Mock(url='https://ec2.us-west-2.amazonaws.com')
        self.http_session.send.side_effect = ConnectionError(
            "Fake gaierror(8, node or host not known)", request=fake_request)
        with self.assertRaisesRegexp(EndpointConnectionError,
                                     'Could not connect'):
            self.endpoint.make_request(self.op, request_dict())


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
        op.metadata = {'protocol': 'query'}
        op.has_streaming_output = False
        self.endpoint.make_request(op, request_dict())
        call_args = self.event_emitter.emit.call_args
        self.assertEqual(call_args[0][0],
                         'needs-retry.ec2.DescribeInstances')

    def test_retry_events_can_alter_behavior(self):
        op = Mock()
        op.name = 'DescribeInstances'
        op.metadata = {'protocol': 'json'}
        self.event_emitter.emit.side_effect = [
            [(None, None)],    # Request created.
            [(None, 0)],       # Check if retry needed. Retry needed.
            [(None, None)],    # Request created.
            [(None, None)]     # Check if retry needed. Retry not needed.
        ]
        self.endpoint.make_request(op, request_dict())
        call_args = self.event_emitter.emit.call_args_list
        self.assertEqual(self.event_emitter.emit.call_count, 4)
        # Check that all of the events are as expected.
        self.assertEqual(call_args[0][0][0],
                         'request-created.ec2.DescribeInstances')
        self.assertEqual(call_args[1][0][0],
                         'needs-retry.ec2.DescribeInstances')
        self.assertEqual(call_args[2][0][0],
                         'request-created.ec2.DescribeInstances')
        self.assertEqual(call_args[3][0][0],
                         'needs-retry.ec2.DescribeInstances')

    def test_retry_on_socket_errors(self):
        op = Mock()
        op.name = 'DescribeInstances'
        self.event_emitter.emit.side_effect = [
            [(None, None)],    # Request created.
            [(None, 0)],       # Check if retry needed. Retry needed.
            [(None, None)],    # Request created
            [(None, None)]     # Check if retry needed. Retry not needed.
        ]
        self.http_session.send.side_effect = ConnectionError()
        with self.assertRaises(ConnectionError):
            self.endpoint.make_request(op, request_dict())
        call_args = self.event_emitter.emit.call_args_list
        self.assertEqual(self.event_emitter.emit.call_count, 4)
        # Check that all of the events are as expected.
        self.assertEqual(call_args[0][0][0],
                         'request-created.ec2.DescribeInstances')
        self.assertEqual(call_args[1][0][0],
                         'needs-retry.ec2.DescribeInstances')
        self.assertEqual(call_args[2][0][0],
                         'request-created.ec2.DescribeInstances')
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
        op.metadata = {'protocol': 'rest-xml'}
        request = request_dict()
        request['body'] = body
        self.event_emitter.emit.side_effect = [
            [(None, None)],   # Request created.
            [(None, 0)],      # Check if retry needed. Needs Retry.
            [(None, None)],   # Request created.
            [(None, 0)],      # Check if retry needed again. Needs Retry.
            [(None, None)],   # Request created.
            [(None, None)],   # Finally emit no rety is needed.
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
                                  Mock(), 'user-agent')
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
                                  Mock(), 'user-agent')
        endpoint = creator.create_endpoint(self.service_model)
        self.assertEqual(endpoint.region_name, 'us-east-1')

    def test_resolver_no_uses_cred_scope_with_endpoint_url(self):
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
                                  Mock(), 'user-agent')
        endpoint = creator.create_endpoint(self.service_model,
                                           endpoint_url='https://foo')
        self.assertEqual(endpoint.region_name, 'us-west-2')

    def test_resolver_uses_cred_scope_with_endpoint_url_and_no_region(self):
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
        original_region_name = None
        creator = EndpointCreator(resolver, original_region_name,
                                  Mock(), 'user-agent')
        endpoint = creator.create_endpoint(self.service_model,
                                           endpoint_url='https://foo')
        self.assertEqual(endpoint.region_name, resolver_region_override)

    def test_create_endpoint_with_endpoint_resolver_exception(self):
        resolver = Mock()
        resolver.construct_endpoint.side_effect = BaseEndpointResolverError()
        creator = EndpointCreator(resolver, 'us-west-2',
                                  Mock(), 'user-agent')
        with self.assertRaises(BaseEndpointResolverError):
            creator.create_endpoint(self.service_model)

    def test_create_endpoint_with_endpoint_url_and_resolver_exception(self):
        resolver = Mock()
        resolver.construct_endpoint.side_effect = BaseEndpointResolverError()
        creator = EndpointCreator(resolver, 'us-west-2',
                                  Mock(), 'user-agent')
        endpoint = creator.create_endpoint(self.service_model,
                                           endpoint_url='https://foo')
        self.assertEqual(endpoint.host, 'https://foo')


class TestAWSSession(unittest.TestCase):
    def test_auth_header_preserved_from_s3_redirects(self):
        request = AWSRequest()
        request.url = 'https://bucket.s3.amazonaws.com/'
        request.method = 'GET'
        request.headers['Authorization'] = 'original auth header'
        prepared_request = request.prepare()

        fake_response = Mock()
        fake_response.headers = {
            'location': 'https://bucket.s3-us-west-2.amazonaws.com'}
        fake_response.url = request.url
        fake_response.status_code = 307
        fake_response.is_permanent_redirect = False
        # This line is needed to disable the cookie handling
        # code in requests.
        fake_response.raw._original_response = None

        success_response = Mock()
        success_response.raw._original_response = None
        success_response.is_redirect = False
        success_response.status_code = 200
        session = PreserveAuthSession()
        session.send = Mock(return_value=success_response)

        list(session.resolve_redirects(
            fake_response, prepared_request, stream=False))

        redirected_request = session.send.call_args[0][0]
        # The Authorization header for the newly sent request should
        # still have our original Authorization header.
        self.assertEqual(
            redirected_request.headers['Authorization'],
            'original auth header')


class TestRequestCreator(unittest.TestCase):
    def setUp(self):
        self.request_creator = RequestCreator()
        self.user_agent = 'botocore/1.0'
        self.endpoint_url = 'https://s3.amazonaws.com'
        self.base_request_dict = {
            'body': '',
            'headers': {},
            'method': u'GET',
            'query_string': '',
            'url_path': '/'
        }

    def create_request(self, request_dict, endpoint_url=None,
                       user_agent=None):
        self.base_request_dict.update(request_dict)
        if user_agent is None:
            user_agent = self.user_agent
        if endpoint_url is None:
            endpoint_url = self.endpoint_url
        return self.request_creator.create_request_object(
            self.base_request_dict, user_agent, endpoint_url)

    def test_create_request_object_for_get(self):
        request_dict = {
            'method': u'GET',
            'url_path': '/'
        }
        request = self.create_request(
            request_dict, endpoint_url='https://s3.amazonaws.com')
        self.assertEqual(request.method, 'GET')
        self.assertEqual(request.url, 'https://s3.amazonaws.com/')
        self.assertEqual(request.headers['User-Agent'], self.user_agent)

    def test_query_string_serialized_to_url(self):
        request_dict = {
            'method': u'GET',
            'query_string': {u'prefix': u'foo'},
            'url_path': u'/mybucket'
        }
        request = self.create_request(request_dict)
        self.assertEqual(
            request.url,
            'https://s3.amazonaws.com/mybucket?prefix=foo')

    def test_url_path_combined_with_endpoint_url(self):
        # This checks the case where a user specifies and
        # endpoint_url that has a path component, and the
        # serializer gives us a request_dict that has a url
        # component as well (say from a rest-* service).
        request_dict = {
            'query_string': {u'prefix': u'foo'},
            'url_path': u'/mybucket'
        }
        endpoint_url = 'https://custom.endpoint/foo/bar'
        request = self.create_request(request_dict, endpoint_url)
        self.assertEqual(
            request.url,
            'https://custom.endpoint/foo/bar/mybucket?prefix=foo')

    def test_url_path_with_trailing_slash(self):
        self.assertEqual(
            self.create_request(
                {'url_path': u'/mybucket'},
                endpoint_url='https://custom.endpoint/foo/bar/').url,
            'https://custom.endpoint/foo/bar/mybucket')

    def test_url_path_is_slash(self):
        self.assertEqual(
            self.create_request(
                {'url_path': u'/'},
                endpoint_url='https://custom.endpoint/foo/bar/').url,
            'https://custom.endpoint/foo/bar/')

    def test_url_path_is_slash_with_endpoint_url_no_slash(self):
        self.assertEqual(
            self.create_request(
                {'url_path': u'/'},
                endpoint_url='https://custom.endpoint/foo/bar').url,
            'https://custom.endpoint/foo/bar')

    def test_custom_endpoint_with_query_string(self):
        self.assertEqual(
            self.create_request(
                {'url_path': u'/baz', 'query_string': {'x': 'y'}},
                endpoint_url='https://custom.endpoint/foo/bar?foo=bar').url,
            'https://custom.endpoint/foo/bar/baz?foo=bar&x=y')
