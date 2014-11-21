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
