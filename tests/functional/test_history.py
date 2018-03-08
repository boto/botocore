from contextlib import contextmanager

import mock

from tests import BaseSessionTest
from botocore.history import BaseHistoryHandler
from botocore.history import HistoryRecorderScope
from botocore.history import get_global_history_recorder


class RecordingHandler(BaseHistoryHandler):
    def __init__(self):
        self.recorded_calls = []

    def emit(self, event_type, payload, source):
        self.recorded_calls.append((event_type, payload, source))


class BaseHistoryRecorderTest(BaseSessionTest):
    def setUp(self):
        super(BaseHistoryRecorderTest, self).setUp()
        self.client = self.session.create_client('s3', 'us-west-2')
        self.s3_response_body = (
            '<ListAllMyBucketsResult '
            '    xmlns="http://s3.amazonaws.com/doc/2006-03-01/">'
            '  <Owner>'
            '    <ID>d41d8cd98f00b204e9800998ecf8427e</ID>'
            '    <DisplayName>foo</DisplayName>'
            '  </Owner>'
            '  <Buckets>'
            '    <Bucket>'
            '      <Name>bar</Name>'
            '      <CreationDate>1912-06-23T22:57:02.000Z</CreationDate>'
            '    </Bucket>'
            '  </Buckets>'
            '</ListAllMyBucketsResult>'
        ).encode('utf-8')
        self.recording_handler = RecordingHandler()
        self.history_recorder = get_global_history_recorder()
        self.history_recorder.enable()

    @contextmanager
    def patch_http_layer(self, response, status_code=200):
        with mock.patch('botocore.endpoint.Session.send') as send:
            send.return_value = mock.Mock(status_code=status_code,
                                          headers={},
                                          content=response)
            yield send


class TestRecordStatementsInjections(BaseHistoryRecorderTest):
    def setUp(self):
        super(TestRecordStatementsInjections, self).setUp()
        self.history_recorder.add_handler(self.recording_handler)

    def _get_all_events_of_type(self, event_type):
        recorded_calls = self.recording_handler.recorded_calls
        matching = [call for call in recorded_calls
                    if call[0] == event_type]
        return matching

    def test_does_record_api_call(self):
        with self.patch_http_layer(self.s3_response_body):
            self.client.list_buckets()

        api_call_events = self._get_all_events_of_type('API_CALL')
        self.assertEqual(len(api_call_events), 1)
        event = api_call_events[0]
        event_type, payload, source = event
        self.assertEqual(payload, {
                'operation': u'ListBuckets',
                'params': {},
                'service': 's3'
        })
        self.assertEqual(source, 'BOTOCORE')

    def test_does_record_http_request(self):
        with self.patch_http_layer(self.s3_response_body):
            self.client.list_buckets()

        http_request_events = self._get_all_events_of_type('HTTP_REQUEST')
        self.assertEqual(len(http_request_events), 1)
        event = http_request_events[0]
        event_type, payload, source = event

        method = payload['method']
        self.assertEqual(method, u'GET')

        # The header values vary too much per request to verify them here.
        # Instead just check the presense of each expected header.
        headers = payload['headers']
        for expected_header in ['Authorization', 'User-Agent', 'X-Amz-Date',
                                'X-Amz-Content-SHA256']:
            self.assertIn(expected_header, headers)

        body = payload['body']
        self.assertIsNone(body)

        streaming = payload['streaming']
        self.assertEquals(streaming, False)

        url = payload['url']
        self.assertEquals(url, 'https://s3.us-west-2.amazonaws.com/')

        self.assertEqual(source, 'BOTOCORE')

    def test_does_record_http_response(self):
        with self.patch_http_layer(self.s3_response_body):
            self.client.list_buckets()

        http_response_events = self._get_all_events_of_type('HTTP_RESPONSE')
        self.assertEqual(len(http_response_events), 1)
        event = http_response_events[0]
        event_type, payload, source = event

        self.assertEqual(payload, {
                'status_code': 200,
                'headers': {},
                'streaming': False,
                'body': self.s3_response_body,
                'context': {'operation_name': 'ListBuckets'}
            }
        )
        self.assertEqual(source, 'BOTOCORE')

    def test_does_record_parsed_response(self):
        with self.patch_http_layer(self.s3_response_body):
            self.client.list_buckets()

        parsed_response_events = self._get_all_events_of_type(
            'PARSED_RESPONSE')
        self.assertEqual(len(parsed_response_events), 1)
        event = parsed_response_events[0]
        event_type, payload, source = event

        # Given that the request contains headers with a user agent string
        # a date and a signature we need to disassemble the call and manually
        # assert the interesting bits since mock can only assert if the args
        # all match exactly.
        owner = payload['Owner']
        self.assertEqual(owner, {
            'DisplayName': 'foo',
            'ID': 'd41d8cd98f00b204e9800998ecf8427e'
        })

        buckets = payload['Buckets']
        self.assertEqual(len(buckets), 1)
        bucket = buckets[0]
        self.assertEqual(bucket['Name'], 'bar')

        metadata = payload['ResponseMetadata']
        self.assertEqual(metadata, {
            'HTTPHeaders': {},
            'HTTPStatusCode': 200,
            'RetryAttempts': 0
        })


class TestScopedClientEvents(BaseHistoryRecorderTest):
    def setUp(self):
        super(TestScopedClientEvents, self).setUp()
        self.expected_client_call_events = [
            'API_CALL',
            'HTTP_REQUEST',
            'HTTP_RESPONSE',
            'PARSED_RESPONSE'
        ]

    def get_recorded_events(self, recording_handler):
        return [
            call[0] for call in recording_handler.recorded_calls
        ]

    def test_captures_client_events_with_scope(self):
        history_scope = HistoryRecorderScope()
        self.history_recorder.add_scope(history_scope)
        history_scope.register_client(self.client)
        history_scope.add_handler(self.recording_handler)

        with self.patch_http_layer(self.s3_response_body):
            self.client.list_buckets()

        self.assertEqual(
            self.get_recorded_events(self.recording_handler),
            self.expected_client_call_events
        )

    def test_ignores_client_events_not_registered_to_scope(self):
        history_scope = HistoryRecorderScope()
        self.history_recorder.add_scope(history_scope)
        history_scope.add_handler(self.recording_handler)

        with self.patch_http_layer(self.s3_response_body):
            self.client.list_buckets()

        self.assertEqual(
            self.get_recorded_events(self.recording_handler),
            []
        )

    def test_differentiates_between_clients_registered_to_scope(self):
        history_scope = HistoryRecorderScope()
        self.history_recorder.add_scope(history_scope)
        history_scope.register_client(self.client)
        history_scope.add_handler(self.recording_handler)

        with self.patch_http_layer(self.s3_response_body):
            self.client.list_buckets()

        self.assertEqual(
            self.get_recorded_events(self.recording_handler),
            self.expected_client_call_events
        )

        other_client = self.session.create_client('s3', 'us-west-2')
        with self.patch_http_layer(self.s3_response_body):
            other_client.list_buckets()

        # The events from the recorder should be the same as before
        # which sourced from the original client call as this new client
        # is not registered to the scope.
        self.assertEqual(
            self.get_recorded_events(self.recording_handler),
            self.expected_client_call_events
        )

    def test_captures_multiple_client_events_in_same_scope(self):
        history_scope = HistoryRecorderScope()
        self.history_recorder.add_scope(history_scope)
        history_scope.register_client(self.client)
        history_scope.add_handler(self.recording_handler)

        with self.patch_http_layer(self.s3_response_body):
            self.client.list_buckets()

        other_client = self.session.create_client('s3', 'us-west-2')
        history_scope.register_client(other_client)
        with self.patch_http_layer(self.s3_response_body):
            other_client.list_buckets()

        # Both clients are registered to the scope so both of their calls
        # should have been recorded.
        self.assertEqual(
            self.get_recorded_events(self.recording_handler),
            self.expected_client_call_events + self.expected_client_call_events
        )
