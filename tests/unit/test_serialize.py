"""Additional tests for request serialization.

While there are compliance tests in tests/unit/protocols where
the majority of the request serialization/response parsing is tested,
this test module contains additional tests that go above and beyond the
spec.  This can happen for a number of reasons:

* We are testing python specific behavior that doesn't make sense as a
  compliance test.
* We are testing behavior that is not strictly part of the spec.  These
  may result in a a coverage gap that would otherwise be untested.

"""
import base64
import datetime
import dateutil.tz
from tests import unittest

from botocore.model import ServiceModel
from botocore import serialize


class TestBinaryTypes(unittest.TestCase):

    def setUp(self):
        self.model = {
            'metadata': {'protocol': 'query', 'apiVersion': '2014-01-01'},
            'documentation': '',
            'operations': {
                'TestOperation': {
                    'name': 'TestOperation',
                    'http': {
                        'method': 'POST',
                        'requestUri': '/',
                    },
                    'input': {'shape': 'InputShape'},
                }
            },
            'shapes': {
                'InputShape': {
                    'type': 'structure',
                    'members': {
                        'Blob': {'shape': 'BlobType'},
                    }
                },
                'BlobType': {
                    'type': 'blob',
                }
            }
        }
        self.service_model = ServiceModel(self.model)

    def serialize_to_request(self, input_params):
        request_serializer = serialize.create_serializer(
            self.service_model.metadata['protocol'])
        return request_serializer.serialize_to_request(
            input_params, self.service_model.operation_model('TestOperation'))

    def assert_serialized_blob_equals(self, request, blob_bytes):
        # This method handles all the details of the base64 decoding.
        encoded = base64.b64encode(blob_bytes)
        # Now the serializers actually have the base64 encoded contents
        # as str types so we need to decode back.  We know that this is
        # ascii so it's safe to use the ascii encoding.
        expected = encoded.decode('ascii')
        self.assertEqual(request['body']['Blob'], expected)

    def test_blob_accepts_bytes_type(self):
        body = b'bytes body'
        request = self.serialize_to_request(input_params={'Blob': body})

    def test_blob_accepts_str_type(self):
        body = u'ascii text'
        request = self.serialize_to_request(input_params={'Blob': body})
        self.assert_serialized_blob_equals(
            request, blob_bytes=body.encode('ascii'))

    def test_blob_handles_unicode_chars(self):
        body = u'\u2713'
        request = self.serialize_to_request(input_params={'Blob': body})
        self.assert_serialized_blob_equals(
            request, blob_bytes=body.encode('utf-8'))


class TestTimestamps(unittest.TestCase):
    def setUp(self):
        self.model = {
            'metadata': {'protocol': 'query', 'apiVersion': '2014-01-01'},
            'documentation': '',
            'operations': {
                'TestOperation': {
                    'name': 'TestOperation',
                    'http': {
                        'method': 'POST',
                        'requestUri': '/',
                    },
                    'input': {'shape': 'InputShape'},
                }
            },
            'shapes': {
                'InputShape': {
                    'type': 'structure',
                    'members': {
                        'Timestamp': {'shape': 'TimestampType'},
                    }
                },
                'TimestampType': {
                    'type': 'timestamp',
                }
            }
        }
        self.service_model = ServiceModel(self.model)

    def serialize_to_request(self, input_params):
        request_serializer = serialize.create_serializer(
            self.service_model.metadata['protocol'])
        return request_serializer.serialize_to_request(
            input_params, self.service_model.operation_model('TestOperation'))

    def test_accepts_datetime_object(self):
        request = self.serialize_to_request(
            {'Timestamp': datetime.datetime(2014, 1, 1, 12, 12, 12,
                                            tzinfo=dateutil.tz.tzutc())})
        self.assertEqual(request['body']['Timestamp'], '2014-01-01T12:12:12Z')

    def test_accepts_naive_datetime_object(self):
        request = self.serialize_to_request(
            {'Timestamp': datetime.datetime(2014, 1, 1, 12, 12, 12)})
        self.assertEqual(request['body']['Timestamp'], '2014-01-01T12:12:12Z')

    def test_accepts_iso_8601_format(self):
        request = self.serialize_to_request({'Timestamp': '2014-01-01T12:12:12Z'})
        self.assertEqual(request['body']['Timestamp'], '2014-01-01T12:12:12Z')

    def test_accepts_timestamp_without_tz_info(self):
        # If a timezone/utc is not specified, assume they meant
        # UTC.  This is also the previous behavior from older versions
        # of botocore so we want to make sure we preserve this behavior.
        request = self.serialize_to_request({'Timestamp': '2014-01-01T12:12:12'})
        self.assertEqual(request['body']['Timestamp'], '2014-01-01T12:12:12Z')

    def test_microsecond_timestamp_without_tz_info(self):
        request = self.serialize_to_request(
            {'Timestamp': '2014-01-01T12:12:12.123456'})
        self.assertEqual(request['body']['Timestamp'],
                         '2014-01-01T12:12:12.123456Z')
