#!/usr/bin/env
# Copyright (c) 2012-2013 Mitch Garnaat http://garnaat.org/
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
import base64
import datetime
import io
import json
import time

import botocore.auth
import botocore.credentials
from botocore.awsrequest import AWSRequest
from botocore.compat import HTTPHeaders, parse_qs, urlsplit
from tests import mock, unittest


class BaseTestWithFixedDate(unittest.TestCase):
    def setUp(self):
        self.fixed_date = datetime.datetime(
            2014, 3, 10, 17, 2, 55, 0, tzinfo=datetime.timezone.utc
        )
        self.datetime_patch = mock.patch('botocore.auth.datetime.datetime')
        self.datetime_mock = self.datetime_patch.start()
        self.datetime_mock.now.return_value = self.fixed_date
        self.datetime_mock.strptime.return_value = self.fixed_date

    def tearDown(self):
        self.datetime_patch.stop()


class TestHMACV1(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        access_key = '44CF9590006BF252F707'
        secret_key = 'OtxrzxIsfpFjA7SwPzILwy8Bw21TLhquhboDYROV'
        self.credentials = botocore.credentials.Credentials(
            access_key, secret_key
        )
        self.hmacv1 = botocore.auth.HmacV1Auth(self.credentials, None, None)
        self.date_mock = mock.patch('botocore.auth.formatdate')
        self.formatdate = self.date_mock.start()
        self.formatdate.return_value = 'Thu, 17 Nov 2005 18:49:58 GMT'

    def tearDown(self):
        self.date_mock.stop()

    def test_put(self):
        headers = {
            'Date': 'Thu, 17 Nov 2005 18:49:58 GMT',
            'Content-Md5': 'c8fdb181845a4ca6b8fec737b3581d76',
            'Content-Type': 'text/html',
            'X-Amz-Meta-Author': 'foo@bar.com',
            'X-Amz-Magic': 'abracadabra',
        }
        http_headers = HTTPHeaders.from_dict(headers)
        split = urlsplit('/quotes/nelson')
        cs = self.hmacv1.canonical_string('PUT', split, http_headers)
        expected_canonical = (
            "PUT\nc8fdb181845a4ca6b8fec737b3581d76\ntext/html\n"
            "Thu, 17 Nov 2005 18:49:58 GMT\nx-amz-magic:abracadabra\n"
            "x-amz-meta-author:foo@bar.com\n/quotes/nelson"
        )
        expected_signature = 'jZNOcbfWmD/A/f3hSvVzXZjM2HU='
        self.assertEqual(cs, expected_canonical)
        sig = self.hmacv1.get_signature('PUT', split, http_headers)
        self.assertEqual(sig, expected_signature)

    def test_duplicate_headers(self):
        pairs = [
            ('Date', 'Thu, 17 Nov 2005 18:49:58 GMT'),
            ('Content-Md5', 'c8fdb181845a4ca6b8fec737b3581d76'),
            ('Content-Type', 'text/html'),
            ('X-Amz-Meta-Author', 'bar@baz.com'),
            ('X-Amz-Meta-Author', 'foo@bar.com'),
            ('X-Amz-Magic', 'abracadabra'),
        ]

        http_headers = HTTPHeaders.from_pairs(pairs)
        split = urlsplit('/quotes/nelson')
        sig = self.hmacv1.get_signature('PUT', split, http_headers)
        self.assertEqual(sig, 'kIdMxyiYB+F+83zYGR6sSb3ICcE=')

    def test_query_string(self):
        split = urlsplit('/quotes/nelson?uploads')
        pairs = [('Date', 'Thu, 17 Nov 2005 18:49:58 GMT')]
        sig = self.hmacv1.get_signature(
            'PUT', split, HTTPHeaders.from_pairs(pairs)
        )
        self.assertEqual(sig, 'P7pBz3Z4p3GxysRSJ/gR8nk7D4o=')

    def test_bucket_operations(self):
        # Check that the standard operations on buckets that are
        # specified as query strings end up in the canonical resource.
        operations = (
            'acl',
            'cors',
            'lifecycle',
            'policy',
            'notification',
            'logging',
            'tagging',
            'requestPayment',
            'versioning',
            'website',
            'object-lock',
        )
        for operation in operations:
            url = f'/quotes?{operation}'
            split = urlsplit(url)
            cr = self.hmacv1.canonical_resource(split)
            self.assertEqual(cr, f'/quotes?{operation}')

    def test_sign_with_token(self):
        credentials = botocore.credentials.Credentials(
            access_key='foo', secret_key='bar', token='baz'
        )
        auth = botocore.auth.HmacV1Auth(credentials)
        request = AWSRequest()
        request.headers['Date'] = 'Thu, 17 Nov 2005 18:49:58 GMT'
        request.headers['Content-Type'] = 'text/html'
        request.method = 'PUT'
        request.url = 'https://s3.amazonaws.com/bucket/key'
        auth.add_auth(request)
        self.assertIn('Authorization', request.headers)
        # We're not actually checking the signature here, we're
        # just making sure the auth header has the right format.
        self.assertTrue(request.headers['Authorization'].startswith('AWS '))

    def test_resign_with_token(self):
        credentials = botocore.credentials.Credentials(
            access_key='foo', secret_key='bar', token='baz'
        )
        auth = botocore.auth.HmacV1Auth(credentials)
        request = AWSRequest()
        request.headers['Date'] = 'Thu, 17 Nov 2005 18:49:58 GMT'
        request.headers['Content-Type'] = 'text/html'
        request.method = 'PUT'
        request.url = 'https://s3.amazonaws.com/bucket/key'

        auth.add_auth(request)
        original_auth = request.headers['Authorization']
        # Resigning the request shouldn't change the authorization
        # header.  We are also ensuring that the date stays the same
        # because we're mocking out the formatdate() call.  There's
        # another unit test that verifies we use the latest time
        # when we sign the request.
        auth.add_auth(request)
        self.assertEqual(
            request.headers.get_all('Authorization'), [original_auth]
        )

    def test_resign_uses_most_recent_date(self):
        dates = [
            'Thu, 17 Nov 2005 18:49:58 GMT',
            'Thu, 17 Nov 2014 20:00:00 GMT',
        ]
        self.formatdate.side_effect = dates

        request = AWSRequest()
        request.headers['Content-Type'] = 'text/html'
        request.method = 'PUT'
        request.url = 'https://s3.amazonaws.com/bucket/key'

        self.hmacv1.add_auth(request)
        original_date = request.headers['Date']

        self.hmacv1.add_auth(request)
        modified_date = request.headers['Date']

        # Each time we sign a request, we make another call to formatdate()
        # so we should have a different date header each time.
        self.assertEqual(original_date, dates[0])
        self.assertEqual(modified_date, dates[1])


class TestSigV2(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        access_key = 'foo'
        secret_key = 'bar'
        self.credentials = botocore.credentials.Credentials(
            access_key, secret_key
        )
        self.signer = botocore.auth.SigV2Auth(self.credentials)
        self.time_patcher = mock.patch.object(
            botocore.auth.time, 'gmtime', mock.Mock(wraps=time.gmtime)
        )
        mocked_time = self.time_patcher.start()
        mocked_time.return_value = time.struct_time(
            [2014, 6, 20, 8, 40, 23, 4, 171, 0]
        )

    def tearDown(self):
        self.time_patcher.stop()

    def test_put(self):
        request = mock.Mock()
        request.url = '/'
        request.method = 'POST'
        params = {'Foo': '\u2713'}
        result = self.signer.calc_signature(request, params)
        self.assertEqual(
            result,
            ('Foo=%E2%9C%93', 'VCtWuwaOL0yMffAT8W4y0AFW3W4KUykBqah9S40rB+Q='),
        )

    def test_fields(self):
        request = AWSRequest()
        request.url = '/'
        request.method = 'POST'
        request.data = {'Foo': '\u2713'}
        self.signer.add_auth(request)
        self.assertEqual(request.data['AWSAccessKeyId'], 'foo')
        self.assertEqual(request.data['Foo'], '\u2713')
        self.assertEqual(request.data['Timestamp'], '2014-06-20T08:40:23Z')
        self.assertEqual(
            request.data['Signature'],
            'Tiecw+t51tok4dTT8B4bg47zxHEM/KcD55f2/x6K22o=',
        )
        self.assertEqual(request.data['SignatureMethod'], 'HmacSHA256')
        self.assertEqual(request.data['SignatureVersion'], '2')

    def test_resign(self):
        # Make sure that resigning after e.g. retries works
        request = AWSRequest()
        request.url = '/'
        request.method = 'POST'
        params = {
            'Foo': '\u2713',
            'Signature': 'VCtWuwaOL0yMffAT8W4y0AFW3W4KUykBqah9S40rB+Q=',
        }
        result = self.signer.calc_signature(request, params)
        self.assertEqual(
            result,
            ('Foo=%E2%9C%93', 'VCtWuwaOL0yMffAT8W4y0AFW3W4KUykBqah9S40rB+Q='),
        )

    def test_get(self):
        request = AWSRequest()
        request.url = '/'
        request.method = 'GET'
        request.params = {'Foo': '\u2713'}
        self.signer.add_auth(request)
        self.assertEqual(request.params['AWSAccessKeyId'], 'foo')
        self.assertEqual(request.params['Foo'], '\u2713')
        self.assertEqual(request.params['Timestamp'], '2014-06-20T08:40:23Z')
        self.assertEqual(
            request.params['Signature'],
            'Un97klqZCONP65bA1+Iv4H3AcB2I40I4DBvw5ZERFPw=',
        )
        self.assertEqual(request.params['SignatureMethod'], 'HmacSHA256')
        self.assertEqual(request.params['SignatureVersion'], '2')


class TestSigV3(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.access_key = 'access_key'
        self.secret_key = 'secret_key'
        self.credentials = botocore.credentials.Credentials(
            self.access_key, self.secret_key
        )
        self.auth = botocore.auth.SigV3Auth(self.credentials)
        self.date_mock = mock.patch('botocore.auth.formatdate')
        self.formatdate = self.date_mock.start()
        self.formatdate.return_value = 'Thu, 17 Nov 2005 18:49:58 GMT'

    def tearDown(self):
        self.date_mock.stop()

    def test_signature_with_date_headers(self):
        request = AWSRequest()
        request.headers = {'Date': 'Thu, 17 Nov 2005 18:49:58 GMT'}
        request.url = 'https://route53.amazonaws.com'
        self.auth.add_auth(request)
        self.assertEqual(
            request.headers['X-Amzn-Authorization'],
            (
                'AWS3-HTTPS AWSAccessKeyId=access_key,Algorithm=HmacSHA256,'
                'Signature=M245fo86nVKI8rLpH4HgWs841sBTUKuwciiTpjMDgPs='
            ),
        )

    def test_resign_with_token(self):
        credentials = botocore.credentials.Credentials(
            access_key='foo', secret_key='bar', token='baz'
        )
        auth = botocore.auth.SigV3Auth(credentials)
        request = AWSRequest()
        request.headers['Date'] = 'Thu, 17 Nov 2005 18:49:58 GMT'
        request.method = 'PUT'
        request.url = 'https://route53.amazonaws.com/'
        auth.add_auth(request)
        original_auth = request.headers['X-Amzn-Authorization']
        # Resigning the request shouldn't change the authorization
        # header.
        auth.add_auth(request)
        self.assertEqual(
            request.headers.get_all('X-Amzn-Authorization'), [original_auth]
        )


class TestS3SigV4Auth(BaseTestWithFixedDate):
    AuthClass = botocore.auth.S3SigV4Auth
    maxDiff = None

    def setUp(self):
        super().setUp()
        self.credentials = botocore.credentials.Credentials(
            access_key='foo', secret_key='bar', token='baz'
        )
        self.auth = self.AuthClass(self.credentials, 'ec2', 'eu-central-1')
        self.request = AWSRequest(data=io.BytesIO(b"foo bar baz"))
        self.request.method = 'PUT'
        self.request.url = 'https://s3.eu-central-1.amazonaws.com/'

        self.client_config = mock.Mock()
        self.s3_config = {}
        self.client_config.s3 = self.s3_config

        self.request.context = {'client_config': self.client_config}

    def test_resign_with_content_hash(self):
        self.auth.add_auth(self.request)
        original_auth = self.request.headers['Authorization']

        self.auth.add_auth(self.request)
        self.assertEqual(
            self.request.headers.get_all('Authorization'), [original_auth]
        )

    def test_signature_is_not_normalized(self):
        request = AWSRequest()
        request.url = 'https://s3.amazonaws.com/bucket/foo/./bar/../bar'
        request.method = 'GET'
        credentials = botocore.credentials.Credentials(
            'access_key', 'secret_key'
        )
        auth = self.AuthClass(credentials, 's3', 'us-east-1')
        auth.add_auth(request)
        self.assertTrue(
            request.headers['Authorization'].startswith('AWS4-HMAC-SHA256')
        )

    def test_query_string_params_in_urls(self):
        if not hasattr(self.AuthClass, 'canonical_query_string'):
            raise unittest.SkipTest(
                f'{self.AuthClass.__name__} does not expose interim steps'
            )

        request = AWSRequest()
        request.url = (
            'https://s3.amazonaws.com/bucket?'
            'marker=%C3%A4%C3%B6%C3%BC-01.txt&prefix'
        )
        request.data = {'Action': 'MyOperation'}
        request.method = 'GET'

        # Check that the canonical query string is correct formatting
        # by ensuring that query string paramters that are added to the
        # canonical query string are correctly formatted.
        cqs = self.auth.canonical_query_string(request)
        self.assertEqual('marker=%C3%A4%C3%B6%C3%BC-01.txt&prefix=', cqs)

    def _test_blocklist_header(self, header, value):
        request = AWSRequest()
        request.url = 'https://s3.amazonaws.com/bucket/foo'
        request.method = 'PUT'
        request.headers[header] = value
        credentials = botocore.credentials.Credentials(
            'access_key', 'secret_key'
        )
        auth = self.AuthClass(credentials, 's3', 'us-east-1')
        auth.add_auth(request)
        self.assertNotIn(header, request.headers['Authorization'])

    def test_blocklist_expect_headers(self):
        self._test_blocklist_header('expect', '100-continue')

    def test_blocklist_trace_id(self):
        self._test_blocklist_header(
            'x-amzn-trace-id', 'Root=foo;Parent=bar;Sampleid=1'
        )

    def test_blocklist_user_agent_header(self):
        self._test_blocklist_header('user-agent', 'botocore/1.4.11')

    def test_blocklist_transfer_encoding_header(self):
        self._test_blocklist_header('transfer-encoding', 'chunked')

    def test_uses_sha256_if_config_value_is_true(self):
        self.client_config.s3['payload_signing_enabled'] = True
        self.auth.add_auth(self.request)
        sha_header = self.request.headers['X-Amz-Content-SHA256']
        self.assertNotEqual(sha_header, 'UNSIGNED-PAYLOAD')

    def test_does_not_use_sha256_if_config_value_is_false(self):
        self.client_config.s3['payload_signing_enabled'] = False
        self.auth.add_auth(self.request)
        sha_header = self.request.headers['X-Amz-Content-SHA256']
        self.assertEqual(sha_header, 'UNSIGNED-PAYLOAD')

    def test_uses_sha256_if_md5_unset(self):
        self.request.context['has_streaming_input'] = True
        self.auth.add_auth(self.request)
        sha_header = self.request.headers['X-Amz-Content-SHA256']
        self.assertNotEqual(sha_header, 'UNSIGNED-PAYLOAD')

    def test_uses_sha256_if_not_https(self):
        self.request.context['has_streaming_input'] = True
        self.request.headers.add_header('Content-MD5', 'foo')
        self.request.url = 'http://s3.amazonaws.com/bucket'
        self.auth.add_auth(self.request)
        sha_header = self.request.headers['X-Amz-Content-SHA256']
        self.assertNotEqual(sha_header, 'UNSIGNED-PAYLOAD')

    def test_uses_sha256_if_not_streaming_upload(self):
        self.request.context['has_streaming_input'] = False
        self.request.headers.add_header('Content-MD5', 'foo')
        self.request.url = 'https://s3.amazonaws.com/bucket'
        self.auth.add_auth(self.request)
        sha_header = self.request.headers['X-Amz-Content-SHA256']
        self.assertNotEqual(sha_header, 'UNSIGNED-PAYLOAD')

    def test_does_not_use_sha256_if_md5_set(self):
        self.request.context['has_streaming_input'] = True
        self.request.headers.add_header('Content-MD5', 'foo')
        self.auth.add_auth(self.request)
        sha_header = self.request.headers['X-Amz-Content-SHA256']
        self.assertEqual(sha_header, 'UNSIGNED-PAYLOAD')

    def test_does_not_use_sha256_if_checksum_set(self):
        self.request.context['has_streaming_input'] = True
        self.request.context['checksum'] = {
            'request_algorithm': {
                'in': 'header',
                'name': 'x-amz-checksum-sha256',
                'algorithm': 'sha256',
            }
        }
        self.request.headers.add_header('X-Amz-Checksum-sha256', 'foo')
        self.auth.add_auth(self.request)
        sha_header = self.request.headers['X-Amz-Content-SHA256']
        self.assertEqual(sha_header, 'UNSIGNED-PAYLOAD')

    def test_does_not_use_sha256_if_context_config_set(self):
        self.request.context['payload_signing_enabled'] = False
        self.request.headers.add_header('Content-MD5', 'foo')
        self.auth.add_auth(self.request)
        sha_header = self.request.headers['X-Amz-Content-SHA256']
        self.assertEqual(sha_header, 'UNSIGNED-PAYLOAD')

    def test_sha256_if_context_set_on_http(self):
        self.request.context['payload_signing_enabled'] = False
        self.request.headers.add_header('Content-MD5', 'foo')
        self.request.url = 'http://s3.amazonaws.com/bucket'
        self.auth.add_auth(self.request)
        sha_header = self.request.headers['X-Amz-Content-SHA256']
        self.assertNotEqual(sha_header, 'UNSIGNED-PAYLOAD')

    def test_sha256_if_context_set_without_md5(self):
        self.request.context['payload_signing_enabled'] = False
        self.request.url = 'https://s3.amazonaws.com/bucket'
        self.auth.add_auth(self.request)
        sha_header = self.request.headers['X-Amz-Content-SHA256']
        self.assertNotEqual(sha_header, 'UNSIGNED-PAYLOAD')


class TestSigV4(unittest.TestCase):
    def setUp(self):
        self.credentials = botocore.credentials.Credentials(
            access_key='foo', secret_key='bar'
        )

    def create_signer(self, service_name='myservice', region='us-west-2'):
        auth = botocore.auth.SigV4Auth(self.credentials, service_name, region)
        return auth

    def test_canonical_query_string(self):
        request = AWSRequest()
        request.url = (
            'https://search-testdomain1-j67dwxlet67gf7ghwfmik2c67i.us-west-2.'
            'cloudsearch.amazonaws.com/'
            '2013-01-01/search?format=sdk&pretty=true&'
            'q.options=%7B%22defaultOperator%22%3A%20%22and%22%2C%20%22'
            'fields%22%3A%5B%22directors%5E10%22%5D%7D&q=George%20Lucas'
        )
        request.method = 'GET'
        auth = self.create_signer('cloudsearchdomain', 'us-west-2')
        actual = auth.canonical_query_string(request)
        # Here 'q' should come before 'q.options'.
        expected = (
            "format=sdk&pretty=true&q=George%20Lucas&q.options=%7B%22"
            "defaultOperator%22%3A%20%22and%22%2C%20%22fields%22%3A%5B"
            "%22directors%5E10%22%5D%7D"
        )
        self.assertEqual(actual, expected)

    def test_thread_safe_timestamp(self):
        request = AWSRequest()
        request.url = (
            'https://search-testdomain1-j67dwxlet67gf7ghwfmik2c67i.us-west-2.'
            'cloudsearch.amazonaws.com/'
            '2013-01-01/search?format=sdk&pretty=true&'
            'q.options=%7B%22defaultOperator%22%3A%20%22and%22%2C%20%22'
            'fields%22%3A%5B%22directors%5E10%22%5D%7D&q=George%20Lucas'
        )
        request.method = 'GET'
        auth = self.create_signer('cloudsearchdomain', 'us-west-2')
        with mock.patch.object(
            botocore.auth.datetime,
            'datetime',
            mock.Mock(wraps=datetime.datetime),
        ) as mock_datetime:
            original_now = datetime.datetime(
                2014, 1, 1, 0, 0, tzinfo=datetime.timezone.utc
            )

            mock_datetime.now.return_value = original_now
            # Go through the add_auth process once. This will attach
            # a timestamp to the request at the beginning of auth.
            auth.add_auth(request)
            self.assertEqual(request.context['timestamp'], '20140101T000000Z')
            # Ensure the date is in the Authorization header
            self.assertIn('20140101', request.headers['Authorization'])
            # Now suppose the utc time becomes the next day all of a sudden
            mock_datetime.now.return_value = datetime.datetime(
                2014, 1, 2, 0, 0, tzinfo=datetime.timezone.utc
            )
            # Smaller methods like the canonical request and string_to_sign
            # should  have the timestamp attached to the request in their
            # body and not what the time is now mocked as. This is to ensure
            # there is no mismatching in timestamps when signing.
            cr = auth.canonical_request(request)
            self.assertIn('x-amz-date:20140101T000000Z', cr)
            self.assertNotIn('x-amz-date:20140102T000000Z', cr)

            sts = auth.string_to_sign(request, cr)
            self.assertIn('20140101T000000Z', sts)
            self.assertNotIn('20140102T000000Z', sts)

    def test_payload_is_binary_file(self):
        request = AWSRequest()
        request.data = io.BytesIO('\u2713'.encode())
        request.url = 'https://amazonaws.com'
        auth = self.create_signer()
        payload = auth.payload(request)
        self.assertEqual(
            payload,
            '1dabba21cdad44541f6b15796f8d22978fc7ea10c46aeceeeeb66c23b3ac7604',
        )

    def test_payload_is_bytes_type(self):
        request = AWSRequest()
        request.data = '\u2713'.encode()
        request.url = 'https://amazonaws.com'
        auth = self.create_signer()
        payload = auth.payload(request)
        self.assertEqual(
            payload,
            '1dabba21cdad44541f6b15796f8d22978fc7ea10c46aeceeeeb66c23b3ac7604',
        )

    def test_payload_not_signed_if_disabled_in_context(self):
        request = AWSRequest()
        request.data = '\u2713'.encode()
        request.url = 'https://amazonaws.com'
        request.context['payload_signing_enabled'] = False
        auth = self.create_signer()
        payload = auth.payload(request)
        self.assertEqual(payload, 'UNSIGNED-PAYLOAD')

    def test_content_sha256_set_if_payload_signing_disabled(self):
        request = AWSRequest()
        request.data = io.BytesIO('\u2713'.encode())
        request.url = 'https://amazonaws.com'
        request.context['payload_signing_enabled'] = False
        request.method = 'PUT'
        auth = self.create_signer()
        auth.add_auth(request)
        sha_header = request.headers['X-Amz-Content-SHA256']
        self.assertEqual(sha_header, 'UNSIGNED-PAYLOAD')

    def test_collapse_multiple_spaces(self):
        auth = self.create_signer()
        original = HTTPHeaders()
        original['foo'] = 'double  space'
        headers = auth.canonical_headers(original)
        self.assertEqual(headers, 'foo:double space')

    def test_trims_leading_trailing_spaces(self):
        auth = self.create_signer()
        original = HTTPHeaders()
        original['foo'] = '  leading  and  trailing  '
        headers = auth.canonical_headers(original)
        self.assertEqual(headers, 'foo:leading and trailing')

    def test_strips_http_default_port(self):
        request = AWSRequest()
        request.url = 'http://s3.us-west-2.amazonaws.com:80/'
        request.method = 'GET'
        auth = self.create_signer('s3', 'us-west-2')
        actual = auth.headers_to_sign(request)['host']
        expected = 's3.us-west-2.amazonaws.com'
        self.assertEqual(actual, expected)

    def test_strips_https_default_port(self):
        request = AWSRequest()
        request.url = 'https://s3.us-west-2.amazonaws.com:443/'
        request.method = 'GET'
        auth = self.create_signer('s3', 'us-west-2')
        actual = auth.headers_to_sign(request)['host']
        expected = 's3.us-west-2.amazonaws.com'
        self.assertEqual(actual, expected)

    def test_strips_http_auth(self):
        request = AWSRequest()
        request.url = 'https://username:password@s3.us-west-2.amazonaws.com/'
        request.method = 'GET'
        auth = self.create_signer('s3', 'us-west-2')
        actual = auth.headers_to_sign(request)['host']
        expected = 's3.us-west-2.amazonaws.com'
        self.assertEqual(actual, expected)

    def test_strips_default_port_and_http_auth(self):
        request = AWSRequest()
        request.url = 'http://username:password@s3.us-west-2.amazonaws.com:80/'
        request.method = 'GET'
        auth = self.create_signer('s3', 'us-west-2')
        actual = auth.headers_to_sign(request)['host']
        expected = 's3.us-west-2.amazonaws.com'
        self.assertEqual(actual, expected)


class TestSigV4Resign(BaseTestWithFixedDate):
    maxDiff = None
    AuthClass = botocore.auth.SigV4Auth

    def setUp(self):
        super().setUp()
        self.credentials = botocore.credentials.Credentials(
            access_key='foo', secret_key='bar', token='baz'
        )
        self.auth = self.AuthClass(self.credentials, 'ec2', 'us-west-2')
        self.request = AWSRequest()
        self.request.method = 'PUT'
        self.request.url = 'https://ec2.amazonaws.com/'

    def test_resign_request_with_date(self):
        self.request.headers['Date'] = 'Thu, 17 Nov 2005 18:49:58 GMT'
        self.auth.add_auth(self.request)
        original_auth = self.request.headers['Authorization']

        self.auth.add_auth(self.request)
        self.assertEqual(
            self.request.headers.get_all('Authorization'), [original_auth]
        )

    def test_sigv4_without_date(self):
        self.auth.add_auth(self.request)
        original_auth = self.request.headers['Authorization']

        self.auth.add_auth(self.request)
        self.assertEqual(
            self.request.headers.get_all('Authorization'), [original_auth]
        )


class BasePresignTest(unittest.TestCase):
    def get_parsed_query_string(self, request):
        query_string_dict = parse_qs(urlsplit(request.url).query)
        # Also, parse_qs sets each value in the dict to be a list, but
        # because we know that we won't have repeated keys, we simplify
        # the dict and convert it back to a single value.
        for key in query_string_dict:
            query_string_dict[key] = query_string_dict[key][0]
        return query_string_dict


class TestS3SigV2Presign(BasePresignTest):
    def setUp(self):
        self.access_key = 'access_key'
        self.secret_key = 'secret_key'
        self.credentials = botocore.credentials.Credentials(
            self.access_key, self.secret_key
        )
        self.expires = 3000
        self.auth = botocore.auth.HmacV1QueryAuth(
            self.credentials, expires=self.expires
        )

        self.current_epoch_time = 1427427247.465591
        self.time_patch = mock.patch('time.time')
        self.time_mock = self.time_patch.start()
        self.time_mock.return_value = self.current_epoch_time

        self.request = AWSRequest()
        self.bucket = 'mybucket'
        self.key = 'myobject'
        self.path = f'https://s3.amazonaws.com/{self.bucket}/{self.key}'
        self.request.url = self.path
        self.request.method = 'GET'

    def tearDown(self):
        self.time_patch.stop()
        super().tearDown()

    def test_presign_with_query_string(self):
        self.request.url = (
            'https://foo-bucket.s3.amazonaws.com/image.jpg'
            '?response-content-disposition='
            'attachment%3B%20filename%3D%22download.jpg%22'
        )
        self.auth.add_auth(self.request)
        query_string = self.get_parsed_query_string(self.request)
        # We should have still kept the response-content-disposition
        # in the query string.
        self.assertIn('response-content-disposition', query_string)
        self.assertEqual(
            query_string['response-content-disposition'],
            'attachment; filename="download.jpg"',
        )
        # But we should have also added the parts from the signer.
        self.assertEqual(query_string['AWSAccessKeyId'], self.access_key)

    def test_presign_no_headers(self):
        self.auth.add_auth(self.request)
        self.assertTrue(self.request.url.startswith(self.path + '?'))
        query_string = self.get_parsed_query_string(self.request)
        self.assertEqual(query_string['AWSAccessKeyId'], self.access_key)
        self.assertEqual(
            query_string['Expires'],
            str(int(self.current_epoch_time) + self.expires),
        )
        self.assertEqual(
            query_string['Signature'], 'ZRSgywstwIruKLTLt/Bcrf9H1K4='
        )

    def test_presign_with_x_amz_headers(self):
        self.request.headers['x-amz-security-token'] = 'foo'
        self.request.headers['x-amz-acl'] = 'read-only'
        self.auth.add_auth(self.request)
        query_string = self.get_parsed_query_string(self.request)
        self.assertEqual(query_string['x-amz-security-token'], 'foo')
        self.assertEqual(query_string['x-amz-acl'], 'read-only')
        self.assertEqual(
            query_string['Signature'], '5oyMAGiUk1E5Ry2BnFr6cIS3Gus='
        )

    def test_presign_with_content_headers(self):
        self.request.headers['content-type'] = 'txt'
        self.request.headers['content-md5'] = 'foo'
        self.auth.add_auth(self.request)
        query_string = self.get_parsed_query_string(self.request)
        self.assertEqual(query_string['content-type'], 'txt')
        self.assertEqual(query_string['content-md5'], 'foo')
        self.assertEqual(
            query_string['Signature'], '/YQRFdQGywXP74WrOx2ET/RUqz8='
        )

    def test_presign_with_unused_headers(self):
        self.request.headers['user-agent'] = 'botocore'
        self.auth.add_auth(self.request)
        query_string = self.get_parsed_query_string(self.request)
        self.assertNotIn('user-agent', query_string)
        self.assertEqual(
            query_string['Signature'], 'ZRSgywstwIruKLTLt/Bcrf9H1K4='
        )


class TestSigV4Presign(BasePresignTest):
    maxDiff = None
    AuthClass = botocore.auth.SigV4QueryAuth

    def setUp(self):
        self.access_key = 'access_key'
        self.secret_key = 'secret_key'
        self.credentials = botocore.credentials.Credentials(
            self.access_key, self.secret_key
        )
        self.service_name = 'myservice'
        self.region_name = 'myregion'
        self.auth = self.AuthClass(
            self.credentials, self.service_name, self.region_name, expires=60
        )
        self.datetime_patcher = mock.patch.object(
            botocore.auth.datetime,
            'datetime',
            mock.Mock(wraps=datetime.datetime),
        )
        mocked_datetime = self.datetime_patcher.start()
        mocked_datetime.now.return_value = datetime.datetime(
            2014, 1, 1, 0, 0, tzinfo=datetime.timezone.utc
        )

    def tearDown(self):
        self.datetime_patcher.stop()
        super().tearDown()

    def test_presign_no_params(self):
        request = AWSRequest()
        request.method = 'GET'
        request.url = 'https://ec2.us-east-1.amazonaws.com/'
        self.auth.add_auth(request)
        query_string = self.get_parsed_query_string(request)
        self.assertEqual(
            query_string,
            {
                'X-Amz-Algorithm': 'AWS4-HMAC-SHA256',
                'X-Amz-Credential': (
                    'access_key/20140101/myregion/myservice/aws4_request'
                ),
                'X-Amz-Date': '20140101T000000Z',
                'X-Amz-Expires': '60',
                'X-Amz-Signature': (
                    'c70e0bcdb4cd3ee324f71c78195445b878'
                    '8315af0800bbbdbbb6d05a616fb84c'
                ),
                'X-Amz-SignedHeaders': 'host',
            },
        )

    def test_operation_params_before_auth_params(self):
        # The spec is picky about this.
        request = AWSRequest()
        request.method = 'GET'
        request.url = 'https://ec2.us-east-1.amazonaws.com/?Action=MyOperation'
        self.auth.add_auth(request)
        # Verify auth params come after the existing params.
        self.assertIn('?Action=MyOperation&X-Amz', request.url)

    def test_operation_params_before_auth_params_in_body(self):
        request = AWSRequest()
        request.method = 'GET'
        request.url = 'https://ec2.us-east-1.amazonaws.com/'
        request.data = {'Action': 'MyOperation'}
        self.auth.add_auth(request)
        # Same situation, the params from request.data come before the auth
        # params in the query string.
        self.assertIn('?Action=MyOperation&X-Amz', request.url)

    def test_operation_params_before_auth_params_in_params(self):
        request = AWSRequest()
        request.method = 'GET'
        request.url = 'https://ec2.us-east-1.amazonaws.com/'
        request.params = {'Action': 'MyOperation'}
        self.auth.add_auth(request)
        # Same situation, the params from request.param come before the
        # auth params in the query string.
        self.assertIn('?Action=MyOperation&X-Amz', request.url)

    def test_request_params_not_duplicated_in_prepare(self):
        """
        params should be moved to query string in add_auth
        and not rewritten at the end with request.prepare()
        """
        request = AWSRequest(
            method='GET',
            url='https://ec2.us-east-1.amazonaws.com/',
            params={'Action': 'MyOperation'},
        )
        self.auth.add_auth(request)
        self.assertIn('?Action=MyOperation&X-Amz', request.url)
        prep = request.prepare()
        assert not prep.url.endswith('Action=MyOperation')

    def test_presign_with_spaces_in_param(self):
        request = AWSRequest()
        request.method = 'GET'
        request.url = 'https://ec2.us-east-1.amazonaws.com/'
        request.data = {'Action': 'MyOperation', 'Description': 'With Spaces'}
        self.auth.add_auth(request)
        # Verify we encode spaces as '%20, and we don't use '+'.
        self.assertIn('Description=With%20Spaces', request.url)

    def test_presign_with_empty_param_value(self):
        request = AWSRequest()
        request.method = 'POST'
        # actual URL format for creating a multipart upload
        request.url = 'https://s3.amazonaws.com/mybucket/mykey?uploads'
        self.auth.add_auth(request)
        # verify that uploads param is still in URL
        self.assertIn('uploads', request.url)

    def test_s3_sigv4_presign(self):
        auth = botocore.auth.S3SigV4QueryAuth(
            self.credentials, self.service_name, self.region_name, expires=60
        )
        request = AWSRequest()
        request.method = 'GET'
        request.url = (
            'https://s3.us-west-2.amazonaws.com/mybucket/keyname/.bar'
        )
        auth.add_auth(request)
        query_string = self.get_parsed_query_string(request)
        # We use a different payload:
        self.assertEqual(auth.payload(request), 'UNSIGNED-PAYLOAD')
        # which will result in a different X-Amz-Signature:
        self.assertEqual(
            query_string,
            {
                'X-Amz-Algorithm': 'AWS4-HMAC-SHA256',
                'X-Amz-Credential': (
                    'access_key/20140101/myregion/myservice/aws4_request'
                ),
                'X-Amz-Date': '20140101T000000Z',
                'X-Amz-Expires': '60',
                'X-Amz-Signature': (
                    'ac1b8b9e47e8685c5c963d75e35e8741d55251'
                    'cd955239cc1efad4dc7201db66'
                ),
                'X-Amz-SignedHeaders': 'host',
            },
        )

    def test_presign_with_security_token(self):
        self.credentials.token = 'security-token'
        auth = botocore.auth.S3SigV4QueryAuth(
            self.credentials, self.service_name, self.region_name, expires=60
        )
        request = AWSRequest()
        request.method = 'GET'
        request.url = 'https://ec2.us-east-1.amazonaws.com/'
        auth.add_auth(request)
        query_string = self.get_parsed_query_string(request)
        self.assertEqual(
            query_string['X-Amz-Security-Token'], 'security-token'
        )

    def test_presign_where_body_is_json_bytes(self):
        request = AWSRequest()
        request.method = 'GET'
        request.url = 'https://myservice.us-east-1.amazonaws.com/'
        request.data = b'{"Param": "value"}'
        self.auth.add_auth(request)
        query_string = self.get_parsed_query_string(request)
        expected_query_string = {
            'X-Amz-Algorithm': 'AWS4-HMAC-SHA256',
            'X-Amz-Credential': (
                'access_key/20140101/myregion/myservice/aws4_request'
            ),
            'X-Amz-Expires': '60',
            'X-Amz-Date': '20140101T000000Z',
            'X-Amz-Signature': (
                '8e1d372d168d532313ce6df8f64a7dc51d'
                'e6f312a9cfba6e5b345d8a771e839c'
            ),
            'X-Amz-SignedHeaders': 'host',
            'Param': 'value',
        }
        self.assertEqual(query_string, expected_query_string)

    def test_presign_where_body_is_json_string(self):
        request = AWSRequest()
        request.method = 'GET'
        request.url = 'https://myservice.us-east-1.amazonaws.com/'
        request.data = '{"Param": "value"}'
        self.auth.add_auth(request)
        query_string = self.get_parsed_query_string(request)
        expected_query_string = {
            'X-Amz-Algorithm': 'AWS4-HMAC-SHA256',
            'X-Amz-Credential': (
                'access_key/20140101/myregion/myservice/aws4_request'
            ),
            'X-Amz-Expires': '60',
            'X-Amz-Date': '20140101T000000Z',
            'X-Amz-Signature': (
                '8e1d372d168d532313ce6df8f64a7dc51d'
                'e6f312a9cfba6e5b345d8a771e839c'
            ),
            'X-Amz-SignedHeaders': 'host',
            'Param': 'value',
        }
        self.assertEqual(query_string, expected_query_string)

    def test_presign_content_type_form_encoded_not_signed(self):
        request = AWSRequest()
        request.method = 'GET'
        request.url = 'https://myservice.us-east-1.amazonaws.com/'
        request.headers['Content-Type'] = (
            'application/x-www-form-urlencoded; charset=utf-8'
        )
        self.auth.add_auth(request)
        query_string = self.get_parsed_query_string(request)
        signed_headers = query_string.get('X-Amz-SignedHeaders')
        self.assertNotIn('content-type', signed_headers)


class BaseS3PresignPostTest(unittest.TestCase):
    def setUp(self):
        self.access_key = 'access_key'
        self.secret_key = 'secret_key'
        self.credentials = botocore.credentials.Credentials(
            self.access_key, self.secret_key
        )

        self.service_name = 'myservice'
        self.region_name = 'myregion'

        self.bucket = 'mybucket'
        self.key = 'mykey'
        self.policy = {
            "expiration": "2007-12-01T12:00:00.000Z",
            "conditions": [
                {"acl": "public-read"},
                {"bucket": self.bucket},
                ["starts-with", "$key", self.key],
            ],
        }
        self.fields = {
            'key': self.key,
            'acl': 'public-read',
        }

        self.request = AWSRequest()
        self.request.url = f'https://s3.amazonaws.com/{self.bucket}'
        self.request.method = 'POST'

        self.request.context['s3-presign-post-fields'] = self.fields
        self.request.context['s3-presign-post-policy'] = self.policy


class TestS3SigV2Post(BaseS3PresignPostTest):
    def setUp(self):
        super().setUp()
        self.auth = botocore.auth.HmacV1PostAuth(self.credentials)

        self.current_epoch_time = 1427427247.465591
        self.time_patch = mock.patch('time.time')
        self.time_mock = self.time_patch.start()
        self.time_mock.return_value = self.current_epoch_time

    def tearDown(self):
        self.time_patch.stop()
        super().tearDown()

    def test_presign_post(self):
        self.auth.add_auth(self.request)
        result_fields = self.request.context['s3-presign-post-fields']
        self.assertEqual(
            result_fields['AWSAccessKeyId'], self.credentials.access_key
        )

        result_policy = json.loads(
            base64.b64decode(result_fields['policy']).decode('utf-8')
        )
        self.assertEqual(
            result_policy['expiration'], '2007-12-01T12:00:00.000Z'
        )
        self.assertEqual(
            result_policy['conditions'],
            [
                {"acl": "public-read"},
                {"bucket": "mybucket"},
                ["starts-with", "$key", "mykey"],
            ],
        )
        self.assertIn('signature', result_fields)

    def test_presign_post_with_security_token(self):
        self.credentials.token = 'my-token'
        self.auth = botocore.auth.HmacV1PostAuth(self.credentials)
        self.auth.add_auth(self.request)
        result_fields = self.request.context['s3-presign-post-fields']
        self.assertEqual(result_fields['x-amz-security-token'], 'my-token')

    def test_empty_fields_and_policy(self):
        self.request = AWSRequest()
        self.request.url = f'https://s3.amazonaws.com/{self.bucket}'
        self.request.method = 'POST'
        self.auth.add_auth(self.request)

        result_fields = self.request.context['s3-presign-post-fields']
        self.assertEqual(
            result_fields['AWSAccessKeyId'], self.credentials.access_key
        )
        result_policy = json.loads(
            base64.b64decode(result_fields['policy']).decode('utf-8')
        )
        self.assertEqual(result_policy['conditions'], [])
        self.assertIn('signature', result_fields)


class TestS3SigV4Post(BaseS3PresignPostTest):
    def setUp(self):
        super().setUp()
        self.auth = botocore.auth.S3SigV4PostAuth(
            self.credentials, self.service_name, self.region_name
        )
        self.datetime_patcher = mock.patch.object(
            botocore.auth.datetime,
            'datetime',
            mock.Mock(wraps=datetime.datetime),
        )
        mocked_datetime = self.datetime_patcher.start()
        mocked_datetime.now.return_value = datetime.datetime(
            2014, 1, 1, 0, 0, tzinfo=datetime.timezone.utc
        )

    def tearDown(self):
        self.datetime_patcher.stop()
        super().tearDown()

    def test_presign_post(self):
        self.auth.add_auth(self.request)
        result_fields = self.request.context['s3-presign-post-fields']
        self.assertEqual(result_fields['x-amz-algorithm'], 'AWS4-HMAC-SHA256')
        self.assertEqual(
            result_fields['x-amz-credential'],
            'access_key/20140101/myregion/myservice/aws4_request',
        )
        self.assertEqual(result_fields['x-amz-date'], '20140101T000000Z')

        result_policy = json.loads(
            base64.b64decode(result_fields['policy']).decode('utf-8')
        )
        self.assertEqual(
            result_policy['expiration'], '2007-12-01T12:00:00.000Z'
        )
        self.assertEqual(
            result_policy['conditions'],
            [
                {"acl": "public-read"},
                {"bucket": "mybucket"},
                ["starts-with", "$key", "mykey"],
                {"x-amz-algorithm": "AWS4-HMAC-SHA256"},
                {
                    "x-amz-credential": "access_key/20140101/myregion/myservice/aws4_request"
                },
                {"x-amz-date": "20140101T000000Z"},
            ],
        )
        self.assertIn('x-amz-signature', result_fields)

    def test_presign_post_with_security_token(self):
        self.credentials.token = 'my-token'
        self.auth = botocore.auth.S3SigV4PostAuth(
            self.credentials, self.service_name, self.region_name
        )
        self.auth.add_auth(self.request)
        result_fields = self.request.context['s3-presign-post-fields']
        self.assertEqual(result_fields['x-amz-security-token'], 'my-token')

    def test_empty_fields_and_policy(self):
        self.request = AWSRequest()
        self.request.url = f'https://s3.amazonaws.com/{self.bucket}'
        self.request.method = 'POST'
        self.auth.add_auth(self.request)

        result_fields = self.request.context['s3-presign-post-fields']
        self.assertEqual(result_fields['x-amz-algorithm'], 'AWS4-HMAC-SHA256')
        self.assertEqual(
            result_fields['x-amz-credential'],
            'access_key/20140101/myregion/myservice/aws4_request',
        )
        self.assertEqual(result_fields['x-amz-date'], '20140101T000000Z')

        result_policy = json.loads(
            base64.b64decode(result_fields['policy']).decode('utf-8')
        )
        self.assertEqual(
            result_policy['conditions'],
            [
                {"x-amz-algorithm": "AWS4-HMAC-SHA256"},
                {
                    "x-amz-credential": "access_key/20140101/myregion/myservice/aws4_request"
                },
                {"x-amz-date": "20140101T000000Z"},
            ],
        )
        self.assertIn('x-amz-signature', result_fields)
