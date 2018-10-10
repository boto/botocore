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
import socket
from tests import unittest

from mock import Mock, patch, sentinel
from botocore.vendored.requests import ConnectionError

from botocore.compat import six
from botocore.awsrequest import AWSRequest
from botocore.endpoint import Endpoint, DEFAULT_TIMEOUT
from botocore.endpoint import EndpointCreator
from botocore.exceptions import EndpointConnectionError
from botocore.exceptions import ConnectionClosedError
from botocore.httpsession import URLLib3Session
from botocore.model import OperationModel, ServiceId


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

    def seek(self, where, whence=0):
        self.total_resets += 1
        six.StringIO.seek(self, where, whence)


class TestEndpointBase(unittest.TestCase):

    def setUp(self):
        self.op = Mock()
        self.op.has_streaming_output = False
        self.op.has_event_stream_output = False
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

    def test_make_request_with_context(self):
        r = request_dict()
        r['context'] = {'signing': {'region': 'us-west-2'}}
        with patch('botocore.endpoint.Endpoint.prepare_request') as prepare:
            self.endpoint.make_request(self.op, r)
        request = prepare.call_args[0][0]
        self.assertEqual(request.context['signing']['region'], 'us-west-2')

class TestRetryInterface(TestEndpointBase):
    def setUp(self):
        super(TestRetryInterface, self).setUp()
        self.retried_on_exception = None
        self._operation = Mock(spec=OperationModel)
        self._operation.service_model.service_id = ServiceId('ec2')

    def test_retry_events_are_emitted(self):
        op = self._operation
        op.name = 'DescribeInstances'
        op.metadata = {'protocol': 'query'}
        op.has_streaming_output = False
        op.has_event_stream_output = False
        self.endpoint.make_request(op, request_dict())
        call_args = self.event_emitter.emit.call_args
        self.assertEqual(call_args[0][0],
                         'needs-retry.ec2.DescribeInstances')

    def test_retry_events_can_alter_behavior(self):
        op = self._operation
        op.name = 'DescribeInstances'
        op.metadata = {'protocol': 'json'}
        op.has_event_stream_output = False
        self.event_emitter.emit.side_effect = [
            [(None, None)],    # Request created.
            [(None, None)],    # Request sent.
            [(None, 0)],       # Check if retry needed. Retry needed.
            [(None, None)],    # Request created.
            [(None, None)],    # Request sent.
            [(None, None)]     # Check if retry needed. Retry not needed.
        ]
        self.endpoint.make_request(op, request_dict())
        call_args = self.event_emitter.emit.call_args_list
        self.assertEqual(self.event_emitter.emit.call_count, 6)
        # Check that all of the events are as expected.
        self.assertEqual(call_args[0][0][0],
                         'request-created.ec2.DescribeInstances')
        self.assertEqual(call_args[1][0][0],
                         'before-send.ec2.DescribeInstances')
        self.assertEqual(call_args[2][0][0],
                         'needs-retry.ec2.DescribeInstances')
        self.assertEqual(call_args[3][0][0],
                         'request-created.ec2.DescribeInstances')
        self.assertEqual(call_args[4][0][0],
                         'before-send.ec2.DescribeInstances')
        self.assertEqual(call_args[5][0][0],
                         'needs-retry.ec2.DescribeInstances')

    def test_retry_on_socket_errors(self):
        op = self._operation
        op.name = 'DescribeInstances'
        op.has_event_stream_output = False
        self.event_emitter.emit.side_effect = [
            [(None, None)],    # Request created.
            [(None, None)],    # Request sent.
            [(None, 0)],       # Check if retry needed. Retry needed.
            [(None, None)],    # Request created
            [(None, None)],    # Request sent.
            [(None, None)]     # Check if retry needed. Retry not needed.
        ]
        self.http_session.send.side_effect = ConnectionError()
        with self.assertRaises(ConnectionError):
            self.endpoint.make_request(op, request_dict())
        call_args = self.event_emitter.emit.call_args_list
        self.assertEqual(self.event_emitter.emit.call_count, 6)
        # Check that all of the events are as expected.
        self.assertEqual(call_args[0][0][0],
                         'request-created.ec2.DescribeInstances')
        self.assertEqual(call_args[1][0][0],
                         'before-send.ec2.DescribeInstances')
        self.assertEqual(call_args[2][0][0],
                         'needs-retry.ec2.DescribeInstances')
        self.assertEqual(call_args[3][0][0],
                         'request-created.ec2.DescribeInstances')
        self.assertEqual(call_args[4][0][0],
                         'before-send.ec2.DescribeInstances')
        self.assertEqual(call_args[5][0][0],
                         'needs-retry.ec2.DescribeInstances')

    def test_retry_attempts_added_to_response_metadata(self):
        op = Mock(name='DescribeInstances')
        op.metadata = {'protocol': 'query'}
        op.has_event_stream_output = False
        self.event_emitter.emit.side_effect = [
            [(None, None)],    # Request created.
            [(None, None)],    # Request sent
            [(None, 0)],       # Check if retry needed. Retry needed.
            [(None, None)],    # Request created.
            [(None, None)],    # Request sent
            [(None, None)]     # Check if retry needed. Retry not needed.
        ]
        parser = Mock()
        parser.parse.return_value = {'ResponseMetadata': {}}
        self.factory.return_value.create_parser.return_value = parser
        response = self.endpoint.make_request(op, request_dict())
        self.assertEqual(response[1]['ResponseMetadata']['RetryAttempts'], 1)

    def test_retry_attempts_is_zero_when_not_retried(self):
        op = Mock(name='DescribeInstances', metadata={'protocol': 'query'})
        op.has_event_stream_output = False
        self.event_emitter.emit.side_effect = [
            [(None, None)],    # Request created.
            [(None, None)],    # Request sent.
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
        op.has_event_stream_output = False
        op.metadata = {'protocol': 'rest-xml'}
        request = request_dict()
        request['body'] = body
        self.event_emitter.emit.side_effect = [
            [(None, None)],   # Request created.
            [(None, None)],   # Request sent.
            [(None, 0)],      # Check if retry needed. Needs Retry.
            [(None, None)],   # Request created.
            [(None, None)],   # Request sent.
            [(None, 0)],      # Check if retry needed again. Needs Retry.
            [(None, None)],   # Request created.
            [(None, None)],   # Request sent.
            [(None, None)],   # Finally emit no rety is needed.
        ]
        self.endpoint.make_request(op, request)
        # 2 seeks for the resets and 6 (2 per creation) for content-length
        self.assertEqual(body.total_resets, 8)


class TestEventStreamBody(TestEndpointBase):

    def test_event_stream_body_is_streaming(self):
        self.op.has_event_stream_output = True
        request = request_dict()
        self.endpoint.make_request(self.op, request)
        sent_request = self.http_session.send.call_args[0][0]
        self.assertTrue(sent_request.stream_output)


class TestEndpointCreator(unittest.TestCase):
    def setUp(self):
        self.service_model = Mock(
            endpoint_prefix='ec2', signature_version='v2',
            signing_name='ec2')
        self.environ = {}
        self.environ_patch = patch('os.environ', self.environ)
        self.environ_patch.start()
        self.creator = EndpointCreator(Mock())
        self.mock_session = Mock(spec=URLLib3Session)

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
            endpoint_url='https://example.com',
            http_session_cls=self.mock_session)
        session_args = self.mock_session.call_args[1]
        self.assertEqual(session_args.get('timeout'), DEFAULT_TIMEOUT)

    def test_create_endpoint_with_customized_timeout(self):
        endpoint = self.creator.create_endpoint(
            self.service_model, region_name='us-west-2',
            endpoint_url='https://example.com', timeout=123,
            http_session_cls=self.mock_session)
        session_args = self.mock_session.call_args[1]
        self.assertEqual(session_args.get('timeout'), 123)

    def test_get_endpoint_default_verify_ssl(self):
        endpoint = self.creator.create_endpoint(
            self.service_model, region_name='us-west-2',
            endpoint_url='https://example.com',
            http_session_cls=self.mock_session)
        session_args = self.mock_session.call_args[1]
        self.assertTrue(session_args.get('verify'))

    def test_verify_ssl_can_be_disabled(self):
        endpoint = self.creator.create_endpoint(
            self.service_model, region_name='us-west-2',
            endpoint_url='https://example.com', verify=False,
            http_session_cls=self.mock_session)
        session_args = self.mock_session.call_args[1]
        self.assertFalse(session_args.get('verify'))

    def test_verify_ssl_can_specify_cert_bundle(self):
        endpoint = self.creator.create_endpoint(
            self.service_model, region_name='us-west-2',
            endpoint_url='https://example.com', verify='/path/cacerts.pem',
            http_session_cls=self.mock_session)
        session_args = self.mock_session.call_args[1]
        self.assertEqual(session_args.get('verify'), '/path/cacerts.pem')

    def test_client_cert_can_specify_path(self):
        client_cert = '/some/path/cert'
        endpoint = self.creator.create_endpoint(
            self.service_model, region_name='us-west-2',
            endpoint_url='https://example.com', client_cert=client_cert,
            http_session_cls=self.mock_session)
        session_args = self.mock_session.call_args[1]
        self.assertEqual(session_args.get('client_cert'), '/some/path/cert')

    def test_honor_cert_bundle_env_var(self):
        self.environ['REQUESTS_CA_BUNDLE'] = '/env/cacerts.pem'
        endpoint = self.creator.create_endpoint(
            self.service_model, region_name='us-west-2',
            endpoint_url='https://example.com',
            http_session_cls=self.mock_session)
        session_args = self.mock_session.call_args[1]
        self.assertEqual(session_args.get('verify'), '/env/cacerts.pem')

    def test_env_ignored_if_explicitly_passed(self):
        self.environ['REQUESTS_CA_BUNDLE'] = '/env/cacerts.pem'
        endpoint = self.creator.create_endpoint(
            self.service_model, region_name='us-west-2',
            endpoint_url='https://example.com', verify='/path/cacerts.pem',
            http_session_cls=self.mock_session)
        session_args = self.mock_session.call_args[1]
        # /path/cacerts.pem wins over the value from the env var.
        self.assertEqual(session_args.get('verify'), '/path/cacerts.pem')

    def test_can_specify_max_pool_conns(self):
        endpoint = self.creator.create_endpoint(
            self.service_model, region_name='us-west-2',
            endpoint_url='https://example.com',
            max_pool_connections=100,
            http_session_cls=self.mock_session,
        )
        session_args = self.mock_session.call_args[1]
        self.assertEqual(session_args.get('max_pool_connections'), 100)

    def test_socket_options(self):
        socket_options = [(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)]
        self.creator.create_endpoint(
            self.service_model, region_name='us-west-2',
            endpoint_url='https://example.com',
            http_session_cls=self.mock_session, socket_options=socket_options)
        session_args = self.mock_session.call_args[1]
        self.assertEqual(session_args.get('socket_options'), socket_options)
