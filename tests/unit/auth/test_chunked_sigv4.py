from tests import unittest
from botocore.auth import S3SigV4ChunkedAuth
from botocore.auth import EMPTY_SHA256_HASH
from botocore.credentials import Credentials
from botocore.awsrequest import AWSRequest

import datetime
import hashlib
import hmac
import mock

class TestSigV4Chunked(unittest.TestCase):
    SECRET_KEY = "wJalrXUtnFEMI/K7MDENG+bPxRfiCYEXAMPLEKEY"
    ACCESS_KEY = 'AKIDEXAMPLE'
    CHUNK_META = ';chunk_signature=\r\n\r\n'
    CHUNK_META_LEN = len(CHUNK_META) + 256 / 4

    class FakeFile(object):
        def __init__(self, length):
            self.length = length

        def read(self, chunk):
            return 'A' * chunk

        def __len__(self):
            return self.length

    def setUp(self):
        self.datetime_now = datetime.datetime(2016, 8, 11, 11, 27)
        self.credentials = Credentials(self.ACCESS_KEY, self.SECRET_KEY)
        self.timestamp = self.datetime_now.strftime('%Y%m%dT%H%M%SZ')

    def _scope(self, region):
        return '%s/%s/s3/aws4_request' % (
            self.datetime_now.strftime('%Y%m%d'), region)

    @staticmethod
    def _get_auth_parts(auth_header):
        auth_parts = auth_header[len('AWS4-HMAC-SHA256 '):].split(',')
        return dict([part.strip().split('=') for part in auth_parts])

    @mock.patch('botocore.auth.datetime.datetime')
    def _test_chunked_upload(self,
            data, expected_chunks, expected_auth_signature, datetime_mock):
        datetime_mock.utcnow.return_value = self.datetime_now

        region = 'us-east-1'
        # Pre-computed request signature
        meta_length = self.CHUNK_META_LEN * 2 + 1 + len(hex(len(data))[2:])
        encoded_length = len(data) + meta_length
        signed_headers = [
            'content-encoding',
            'content-length',
            'host',
            'x-amz-content-sha256',
            'x-amz-date',
            'x-amz-decoded-content-length'
        ]

        headers = {'Content-Length': str(len(data))}
        req = AWSRequest('PUT', 'https://s3.amazonaws.com/test-bucket/key',
                         data=data,
                         headers=headers)

        auth = S3SigV4ChunkedAuth(self.credentials, 's3', region)
        auth.add_auth(req)

        self.assertEqual(
            len(data), int(req.headers['X-Amz-Decoded-Content-Length']))
        self.assertEqual(encoded_length, int(req.headers['Content-Length']))
        self.assertEqual('aws-chunked', req.headers['Content-Encoding'])
        self.assertEqual('STREAMING-AWS4-HMAC-SHA256-PAYLOAD',
                         req.headers['X-Amz-Content-SHA256'])
        self.assertTrue(
            req.headers['Authorization'].startswith('AWS4-HMAC-SHA256'))
        auth_parts = self._get_auth_parts(req.headers['Authorization'])
        self.assertEqual(self.ACCESS_KEY + '/' + self._scope(region),
                         auth_parts['Credential'])
        self.assertEqual(';'.join(signed_headers), auth_parts['SignedHeaders'])
        self.assertEqual(expected_auth_signature, auth_parts['Signature'])

        offset = 0
        chunks = 0
        while offset < encoded_length:
            chunk = req.data[offset:]
            meta = chunk.split('\r\n')[0]
            chunk_length, chunk_signature = meta.split(';')
            key, chunk_signature = chunk_signature.split('=')
            self.assertEqual(key, 'chunk-signature')

            expected_length, expected_chunk_signature = expected_chunks[chunks]
            self.assertEqual(expected_length, int(chunk_length, 16))
            self.assertEqual(expected_chunk_signature, chunk_signature)
            offset += len(chunk)
            chunks += 1

    def test_auth_headers(self):
        data = self.FakeFile(10)
        # Pre-computed request signature
        expected_auth_signature = \
            '6c856c1a224fc741eab72a36af7c8bb358436838bdcd86ab27910176e7097e75'
        expected_chunks = [
            (len(data),
            '7a2b06e6ee4a9f41b6bcdb08395929c6b39f4fd1036a95f009cb6e5f2d8235db'),
            (0,
            '37e72b3755e13b8165f51f797c6bbfde1ebc315f2faef0434ea3932af6a58780')
        ]
        self._test_chunked_upload(
            data, expected_chunks, expected_auth_signature)

    def test_multi_read_upload(self):
        '''Test an upload where we have to issue multiple reads'''
        class FixedSizeSource(object):
            def __init__(self, length, read_size):
                self.read_size = read_size
                self.length = length

            def __len__(self):
                return self.length

            def read(self, size):
                return self.read_size * 'A'

        data = FixedSizeSource(1024, 256)
        expected_auth_signature = \
            'fc561b15be2a591341b7b7b678eeeb05917518f45f45761ffcdcaa92186279fa'
        expected_chunks = [
            (len(data),
            '356d851e711ffc62e57bf25423ade389e52992855e37f0249080ad91432e8ba8'),
            (0,
            'eabbb8bda2dee016da251605aa81a6b8c71730023192219f580bf932df712078')
        ]
        self._test_chunked_upload(
            data, expected_chunks, expected_auth_signature)

    def test_partial_read(self):
        '''Test an upload where we have to issue multiple reads'''
        class EmptySource(object):
            def __init__(self, length):
                self.length = length

            def __len__(self):
                return self.length

            def read(self, size):
                return ''

        data = EmptySource(1024)
        expected_auth_signature = \
            'fc561b15be2a591341b7b7b678eeeb05917518f45f45761ffcdcaa92186279fa'
        with self.assertRaises(RuntimeError) as cm:
            self._test_chunked_upload(data, [], expected_auth_signature)
        self.assertEqual('Not enough content', cm.exception.message)
