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

from mock import Mock, patch, sentinel
from botocore.vendored.requests import ConnectionError

from botocore.compat import six
from botocore.awsrequest import AWSRequest
from botocore.endpoint import Endpoint, DEFAULT_TIMEOUT
from botocore.endpoint import EndpointCreator
from botocore.endpoint import BotocoreHTTPSession
from botocore.exceptions import EndpointConnectionError
from botocore.exceptions import ConnectionClosedError


def request_dict():
    return {
        'headers': {},
        'body': '',
        'url_path': '/',
        'query_string': '',
        'method': 'POST',
        'url': 'https://example.com',
        'context': {}
    }


class RecordStreamResets(six.StringIO):
    def __init__(self, value):
        six.StringIO.__init__(self, value)
        self.total_resets = 0

    def seek(self, where):
        self.total_resets += 1
        six.StringIO.seek(self, where)


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
            'https://ec2.us-west-2.amazonaws.com/',
            endpoint_prefix='ec2',
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
        self.endpoint.make_request(self.op, request_dict())

        # http_session should be used to send the request.
        self.assertTrue(self.http_session.send.called)
        prepared_request = self.http_session.send.call_args[0][0]
        self.assertNotIn('Authorization', prepared_request.headers)

    def test_make_request_injects_better_dns_error_msg(self):
        fake_request = Mock(url='https://ec2.us-west-2.amazonaws.com')
        self.http_session.send.side_effect = ConnectionError(
            "Fake gaierror(8, node or host not known)", request=fake_request)
        with self.assertRaisesRegexp(EndpointConnectionError,
                                     'Could not connect'):
            self.endpoint.make_request(self.op, request_dict())

    def test_make_request_injects_better_bad_status_line_error_msg(self):
        fake_request = Mock(url='https://ec2.us-west-2.amazonaws.com')
        self.http_session.send.side_effect = ConnectionError(
            """'Connection aborted.', BadStatusLine("''",)""",
            request=fake_request)
        with self.assertRaisesRegexp(ConnectionClosedError,
                                     'Connection was closed'):
            self.endpoint.make_request(self.op, request_dict())

    def test_make_request_with_context(self):
        r = request_dict()
        r['context'] = {'signing': {'region': 'us-west-2'}}
        with patch('botocore.endpoint.Endpoint.prepare_request') as prepare:
            self.endpoint.make_request(self.op, r)
        request = prepare.call_args[0][0]
        self.assertEqual(request.context['signing']['region'], 'us-west-2')

    def test_can_specify_max_pool_connections(self):
        endpoint = Endpoint('https://ec2.us-west-2.amazonaws.com', 'ec2',
                            self.event_emitter, max_pool_connections=50)
        # We can look in endpoint.http_session.adapters[0]._pool_maxsize,
        # but that feels like testing too much implementation detail.
        self.assertEqual(endpoint.max_pool_connections, 50)

    def test_can_specify_proxies(self):
        proxies = {'http': 'http://foo.bar:1234'}
        endpoint = Endpoint('https://ec2.us-west-2.amazonaws.com', 'ec2',
                            self.event_emitter, proxies=proxies)
        self.assertEqual(endpoint.proxies, proxies)


class TestRetryInterface(TestEndpointBase):
    def setUp(self):
        super(TestRetryInterface, self).setUp()
        self.retried_on_exception = None

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

    def test_retry_attempts_added_to_response_metadata(self):
        op = Mock(name='DescribeInstances')
        op.metadata = {'protocol': 'query'}
        self.event_emitter.emit.side_effect = [
            [(None, None)],    # Request created.
            [(None, 0)],       # Check if retry needed. Retry needed.
            [(None, None)],    # Request created.
            [(None, None)]     # Check if retry needed. Retry not needed.
        ]
        parser = Mock()
        parser.parse.return_value = {'ResponseMetadata': {}}
        self.factory.return_value.create_parser.return_value = parser
        response = self.endpoint.make_request(op, request_dict())
        self.assertEqual(response[1]['ResponseMetadata']['RetryAttempts'], 1)

    def test_retry_attempts_is_zero_when_not_retried(self):
        op = Mock(name='DescribeInstances', metadata={'protocol': 'query'})
        self.event_emitter.emit.side_effect = [
            [(None, None)],    # Request created.
            [(None, None)],    # Check if retry needed. Retry needed.
        ]
        parser = Mock()
        parser.parse.return_value = {'ResponseMetadata': {}}
        self.factory.return_value.create_parser.return_value = parser
        response = self.endpoint.make_request(op, request_dict())
        self.assertEqual(response[1]['ResponseMetadata']['RetryAttempts'], 0)


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
        self.environ = {}
        self.environ_patch = patch('os.environ', self.environ)
        self.environ_patch.start()
        self.creator = EndpointCreator(Mock())

    def tearDown(self):
        self.environ_patch.stop()

    def test_creates_endpoint_with_configured_url(self):
        endpoint = self.creator.create_endpoint(
            self.service_model, region_name='us-east-1',
            endpoint_url='https://endpoint.url')
        self.assertEqual(endpoint.host, 'https://endpoint.url')

    def test_create_endpoint_with_default_timeout(self):
        endpoint = self.creator.create_endpoint(
            self.service_model, region_name='us-west-2',
            endpoint_url='https://example.com')
        self.assertEqual(endpoint.timeout, DEFAULT_TIMEOUT)

    def test_create_endpoint_with_customized_timeout(self):
        endpoint = self.creator.create_endpoint(
            self.service_model, region_name='us-west-2',
            endpoint_url='https://example.com', timeout=123)
        self.assertEqual(endpoint.timeout, 123)

    def test_get_endpoint_default_verify_ssl(self):
        endpoint = self.creator.create_endpoint(
            self.service_model, region_name='us-west-2',
            endpoint_url='https://example.com')
        self.assertTrue(endpoint.verify)

    def test_verify_ssl_can_be_disabled(self):
        endpoint = self.creator.create_endpoint(
            self.service_model, region_name='us-west-2',
            endpoint_url='https://example.com', verify=False)
        self.assertFalse(endpoint.verify)

    def test_verify_ssl_can_specify_cert_bundle(self):
        endpoint = self.creator.create_endpoint(
            self.service_model, region_name='us-west-2',
            endpoint_url='https://example.com', verify='/path/cacerts.pem')
        self.assertEqual(endpoint.verify, '/path/cacerts.pem')

    def test_honor_cert_bundle_env_var(self):
        self.environ['REQUESTS_CA_BUNDLE'] = '/env/cacerts.pem'
        endpoint = self.creator.create_endpoint(
            self.service_model, region_name='us-west-2',
            endpoint_url='https://example.com')
        self.assertEqual(endpoint.verify, '/env/cacerts.pem')

    def test_env_ignored_if_explicitly_passed(self):
        self.environ['REQUESTS_CA_BUNDLE'] = '/env/cacerts.pem'
        endpoint = self.creator.create_endpoint(
            self.service_model, region_name='us-west-2',
            endpoint_url='https://example.com', verify='/path/cacerts.pem')
        # /path/cacerts.pem wins over the value from the env var.
        self.assertEqual(endpoint.verify, '/path/cacerts.pem')

    def test_can_specify_max_pool_conns(self):
        endpoint = self.creator.create_endpoint(
            self.service_model, region_name='us-west-2',
            endpoint_url='https://example.com',
            max_pool_connections=100
        )
        self.assertEqual(endpoint.max_pool_connections, 100)


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
        session = BotocoreHTTPSession()
        session.send = Mock(return_value=success_response)

        list(session.resolve_redirects(
            fake_response, prepared_request, stream=False))

        redirected_request = session.send.call_args[0][0]
        # The Authorization header for the newly sent request should
        # still have our original Authorization header.
        self.assertEqual(
            redirected_request.headers['Authorization'],
            'original auth header')

    def test_max_pool_conns_injects_custom_adapter(self):
        http_adapter_cls = Mock(return_value=sentinel.HTTP_ADAPTER)
        session = BotocoreHTTPSession(max_pool_connections=20,
                                      http_adapter_cls=http_adapter_cls)
        http_adapter_cls.assert_called_with(pool_maxsize=20)
        self.assertEqual(session.adapters['https://'], sentinel.HTTP_ADAPTER)
        self.assertEqual(session.adapters['http://'], sentinel.HTTP_ADAPTER)
