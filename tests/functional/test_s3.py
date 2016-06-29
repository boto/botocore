# Copyright 2015 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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
from tests import unittest, mock, BaseSessionTest

import botocore.session
from botocore.config import Config
from botocore.compat import six
from botocore.exceptions import ParamValidationError, ClientError
from botocore.stub import Stubber


class TestS3BucketValidation(unittest.TestCase):
    def test_invalid_bucket_name_raises_error(self):
        session = botocore.session.get_session()
        s3 = session.create_client('s3')
        with self.assertRaises(ParamValidationError):
            s3.put_object(Bucket='adfgasdfadfs/bucket/name',
                          Key='foo', Body=b'asdf')


class BaseS3OperationTest(BaseSessionTest):
    def setUp(self):
        super(BaseS3OperationTest, self).setUp()
        self.region = 'us-west-2'
        self.client = self.session.create_client(
            's3', self.region)
        self.session_send_patch = mock.patch('botocore.endpoint.Session.send')
        self.http_session_send_mock = self.session_send_patch.start()

    def tearDown(self):
        super(BaseSessionTest, self).tearDown()
        self.session_send_patch.stop()


class TestOnlyAsciiCharsAllowed(BaseS3OperationTest):
    def test_validates_non_ascii_chars_trigger_validation_error(self):
        self.http_session_send_mock.return_value = mock.Mock(status_code=200,
                                                             headers={},
                                                             content=b'')
        with self.assertRaises(ParamValidationError):
            self.client.put_object(
                Bucket='foo', Key='bar', Metadata={
                    'goodkey': 'good', 'non-ascii': u'\u2713'})


class TestS3GetBucketLifecycle(BaseS3OperationTest):
    def test_multiple_transitions_returns_one(self):
        http_response = mock.Mock()
        http_response.status_code = 200
        http_response.content = (
            '<?xml version="1.0" ?>'
            '<LifecycleConfiguration xmlns="http://s3.amazonaws.'
            'com/doc/2006-03-01/">'
            '	<Rule>'
            '		<ID>transitionRule</ID>'
            '		<Prefix>foo</Prefix>'
            '		<Status>Enabled</Status>'
            '		<Transition>'
            '			<Days>40</Days>'
            '			<StorageClass>STANDARD_IA</StorageClass>'
            '		</Transition>'
            '		<Transition>'
            '			<Days>70</Days>'
            '			<StorageClass>GLACIER</StorageClass>'
            '		</Transition>'
            '	</Rule>'
            '	<Rule>'
            '		<ID>noncurrentVersionRule</ID>'
            '		<Prefix>bar</Prefix>'
            '		<Status>Enabled</Status>'
            '		<NoncurrentVersionTransition>'
            '			<NoncurrentDays>40</NoncurrentDays>'
            '			<StorageClass>STANDARD_IA</StorageClass>'
            '		</NoncurrentVersionTransition>'
            '		<NoncurrentVersionTransition>'
            '			<NoncurrentDays>70</NoncurrentDays>'
            '			<StorageClass>GLACIER</StorageClass>'
            '		</NoncurrentVersionTransition>'
            '	</Rule>'
            '</LifecycleConfiguration>'
        ).encode('utf-8')
        http_response.headers = {}
        self.http_session_send_mock.return_value = http_response
        s3 = self.session.create_client('s3')
        response = s3.get_bucket_lifecycle(Bucket='mybucket')
        # Each Transition member should have at least one of the
        # transitions provided.
        self.assertEqual(
            response['Rules'][0]['Transition'],
            {'Days': 40, 'StorageClass': 'STANDARD_IA'}
        )
        self.assertEqual(
            response['Rules'][1]['NoncurrentVersionTransition'],
            {'NoncurrentDays': 40, 'StorageClass': 'STANDARD_IA'}
        )


class TestS3PutObject(BaseS3OperationTest):
    def test_500_error_with_non_xml_body(self):
        # Note: This exact test case may not be applicable from
        # an integration standpoint if the issue is fixed in the future.
        #
        # The issue is that:
        # S3 returns a 200 response but the received response from urllib3 has
        # a 500 status code and the headers are in the body of the
        # the response. Botocore will try to parse out the error body as xml,
        # but the body is invalid xml because it is full of headers.
        # So instead of blowing up on an XML parsing error, we
        # should at least use the 500 status code because that can be
        # retried.
        #
        # We are unsure of what exactly causes the response to be mangled
        # but we expect it to be how 100 continues are handled.
        non_xml_content = (
            'x-amz-id-2: foo\r\n'
            'x-amz-request-id: bar\n'
            'Date: Tue, 06 Oct 2015 03:20:38 GMT\r\n'
            'ETag: "a6d856bc171fc6aa1b236680856094e2"\r\n'
            'Content-Length: 0\r\n'
            'Server: AmazonS3\r\n'
        ).encode('utf-8')
        http_500_response = mock.Mock()
        http_500_response.status_code = 500
        http_500_response.content = non_xml_content
        http_500_response.headers = {}

        success_response = mock.Mock()
        success_response.status_code = 200
        success_response.content = b''
        success_response.headers = {}

        self.http_session_send_mock.side_effect = [
            http_500_response, success_response
        ]
        s3 = self.session.create_client('s3')
        response = s3.put_object(Bucket='mybucket', Key='mykey', Body=b'foo')
        # The first response should have been retried even though the xml is
        # invalid and eventually return the 200 response.
        self.assertEqual(response['ResponseMetadata']['HTTPStatusCode'], 200)


class TestS3SigV4(BaseS3OperationTest):
    def setUp(self):
        super(TestS3SigV4, self).setUp()
        self.client = self.session.create_client(
            's3', self.region, config=Config(signature_version='s3v4'))
        self.response_mock = mock.Mock()
        self.response_mock.content = b''
        self.response_mock.headers = {}
        self.response_mock.status_code = 200
        self.http_session_send_mock.return_value = self.response_mock

    def get_sent_headers(self):
        return self.http_session_send_mock.mock_calls[0][1][0].headers

    def test_content_md5_set(self):
        self.client.put_object(Bucket='foo', Key='bar', Body='baz')
        self.assertIn('content-md5', self.get_sent_headers())

    def test_content_sha256_set_if_config_value_is_true(self):
        config = Config(signature_version='s3v4', s3={
            'payload_signing_enabled': True
        })
        self.client = self.session.create_client(
            's3', self.region, config=config)
        self.client.put_object(Bucket='foo', Key='bar', Body='baz')
        sent_headers = self.get_sent_headers()
        sha_header = sent_headers.get('x-amz-content-sha256')
        self.assertNotEqual(sha_header, b'UNSIGNED-PAYLOAD')

    def test_content_sha256_not_set_if_config_value_is_false(self):
        config = Config(signature_version='s3v4', s3={
            'payload_signing_enabled': False
        })
        self.client = self.session.create_client(
            's3', self.region, config=config)
        self.client.put_object(Bucket='foo', Key='bar', Body='baz')
        sent_headers = self.get_sent_headers()
        sha_header = sent_headers.get('x-amz-content-sha256')
        self.assertEqual(sha_header, b'UNSIGNED-PAYLOAD')

    def test_content_sha256_set_if_md5_is_unavailable(self):
        with mock.patch('botocore.auth.MD5_AVAILABLE', False):
            with mock.patch('botocore.handlers.MD5_AVAILABLE', False):
                self.client.put_object(Bucket='foo', Key='bar', Body='baz')
        sent_headers = self.get_sent_headers()
        unsigned = 'UNSIGNED-PAYLOAD'
        self.assertNotEqual(sent_headers['x-amz-content-sha256'], unsigned)
        self.assertNotIn('content-md5', sent_headers)


class BaseS3AddressingStyle(BaseSessionTest):
    def setUp(self):
        super(BaseS3AddressingStyle, self).setUp()
        self.http_response = mock.Mock()
        self.http_response.status_code = 200
        self.http_response.headers = {}
        self.http_response.content = b''


class TestCustomEndpointUrl(BaseS3AddressingStyle):
    def test_provided_endpoint_url_is_not_mutated(self):
        s3 = self.session.create_client('s3', endpoint_url='https://foo.com')
        with mock.patch('botocore.endpoint.Session.send') as mock_send:
            mock_send.return_value = self.http_response
            s3.put_object(Bucket='mybucket', Key='mykey', Body='mybody')
            request_sent = mock_send.call_args[0][0]
            self.assertEqual(
                'https://foo.com/mybucket/mykey', request_sent.url)


class TestVirtualHostStyle(BaseS3AddressingStyle):
    def test_default_endpoint_for_virtual_addressing(self):
        s3 = self.session.create_client(
            's3', config=Config(s3={'addressing_style': 'virtual'}))
        with mock.patch('botocore.endpoint.Session.send') \
                as mock_send:
            mock_send.return_value = self.http_response
            s3.put_object(Bucket='mybucket', Key='mykey', Body='mybody')
            request_sent = mock_send.call_args[0][0]
            self.assertEqual(
                'https://mybucket.s3.amazonaws.com/mykey', request_sent.url)

    def test_provided_endpoint_url_for_virtual_addressing(self):
        s3 = self.session.create_client(
            's3', config=Config(s3={'addressing_style': 'virtual'}),
            endpoint_url='https://foo.amazonaws.com')
        with mock.patch('botocore.endpoint.Session.send') \
                as mock_send:
            mock_send.return_value = self.http_response
            s3.put_object(Bucket='mybucket', Key='mykey', Body='mybody')
            request_sent = mock_send.call_args[0][0]
            self.assertEqual(
                'https://mybucket.foo.amazonaws.com/mykey', request_sent.url)

    def test_us_gov_with_virtual_addressing(self):
        s3 = self.session.create_client(
            's3', region_name='us-gov-west-1',
            config=Config(s3={'addressing_style': 'virtual'}))
        with mock.patch('botocore.endpoint.Session.send') \
                as mock_send:
            mock_send.return_value = self.http_response
            s3.put_object(Bucket='mybucket', Key='mykey', Body='mybody')
            request_sent = mock_send.call_args[0][0]
            self.assertEqual(
                'https://mybucket.s3-us-gov-west-1.amazonaws.com/mykey',
                request_sent.url)


class TestPathHostStyle(BaseS3AddressingStyle):
    def test_default_endpoint_for_path_addressing(self):
        s3 = self.session.create_client(
            's3', config=Config(s3={'addressing_style': 'path'}))
        with mock.patch('botocore.endpoint.Session.send') \
                as mock_send:
            mock_send.return_value = self.http_response
            s3.put_object(Bucket='mybucket', Key='mykey', Body='mybody')
            request_sent = mock_send.call_args[0][0]
            self.assertEqual(
                'https://s3.amazonaws.com/mybucket/mykey', request_sent.url)

    def test_provided_endpoint_url_for_path_addressing(self):
        s3 = self.session.create_client(
            's3', config=Config(s3={'addressing_style': 'path'}),
            endpoint_url='https://foo.amazonaws.com')
        with mock.patch('botocore.endpoint.Session.send') \
                as mock_send:
            mock_send.return_value = self.http_response
            s3.put_object(Bucket='mybucket', Key='mykey', Body='mybody')
            request_sent = mock_send.call_args[0][0]
            self.assertEqual(
                'https://foo.amazonaws.com/mybucket/mykey', request_sent.url)


class TestCanSendIntegerHeaders(BaseSessionTest):

    def test_int_values_with_sigv4(self):
        s3 = self.session.create_client(
            's3', config=Config(signature_version='s3v4'))
        with mock.patch('botocore.endpoint.Session.send') as mock_send:
            mock_send.return_value = mock.Mock(status_code=200,
                                               content=b'',
                                               headers={})
            s3.upload_part(Bucket='foo', Key='bar', Body=b'foo',
                           UploadId='bar', PartNumber=1, ContentLength=3)
            headers = mock_send.call_args[0][0].headers
            # Verify that the request integer value of 3 has been converted to
            # string '3'.  This also means we've made it pass the signer which
            # expects string values in order to sign properly.
            self.assertEqual(headers['Content-Length'], '3')


class TestS3Accelerate(BaseS3AddressingStyle):
    def assert_uses_accelerate_endpoint_correctly(
            self, client, expecting_https=True):
        # The host should be s3-accelerate.amazonaws.com
        expected_endpoint = (
            'https://mybucket.s3-accelerate.amazonaws.com/mykey')
        if not expecting_https:
            expected_endpoint = (
                'http://mybucket.s3-accelerate.amazonaws.com/mykey')

        with mock.patch('botocore.endpoint.Session.send') \
                as mock_send:
            mock_send.return_value = self.http_response
            client.put_object(Bucket='mybucket', Key='mykey', Body='mybody')
            request_sent = mock_send.call_args[0][0]
            self.assertEqual(expected_endpoint, request_sent.url)

    def test_s3_accelerate_with_config(self):
        s3 = self.session.create_client(
            's3', config=Config(s3={'use_accelerate_endpoint': True}))
        self.assert_uses_accelerate_endpoint_correctly(s3)

    def test_s3_accelerate_using_https_endpoint(self):
        s3 = self.session.create_client(
            's3', endpoint_url='https://s3-accelerate.amazonaws.com')
        self.assert_uses_accelerate_endpoint_correctly(s3)

    def test_s3_accelerate_using_http_endpoint(self):
        s3 = self.session.create_client(
            's3', endpoint_url='http://s3-accelerate.amazonaws.com')
        self.assert_uses_accelerate_endpoint_correctly(s3, False)

    def test_s3_accelerate_with_no_ssl(self):
        s3 = self.session.create_client(
            's3', config=Config(s3={'use_accelerate_endpoint': True}),
            use_ssl=False)
        self.assert_uses_accelerate_endpoint_correctly(s3, False)

    def test_s3_accelerate_even_with_virtual_specified(self):
        s3 = self.session.create_client(
            's3', config=Config(
                s3={'use_accelerate_endpoint': True,
                    'addressing_style': 'path'}))
        # Even if path is specified as the addressing style, use virtual
        # because path style will **not** work with S3 Accelerate
        self.assert_uses_accelerate_endpoint_correctly(s3)


class TestRegionRedirect(BaseS3OperationTest):
    def setUp(self):
        super(TestRegionRedirect, self).setUp()
        self.client = self.session.create_client(
            's3', 'us-west-2', config=Config(signature_version='s3v4'))

        self.redirect_response = mock.Mock()
        self.redirect_response.headers = {
            'x-amz-bucket-region': 'eu-central-1'
        }
        self.redirect_response.status_code = 301
        self.redirect_response.content = (
            b'<?xml version="1.0" encoding="UTF-8"?>\n'
            b'<Error>'
            b'    <Code>PermanentRedirect</Code>'
            b'    <Message>The bucket you are attempting to access must be '
            b'        addressed using the specified endpoint. Please send all '
            b'        future requests to this endpoint.'
            b'    </Message>'
            b'    <Bucket>foo</Bucket>'
            b'    <Endpoint>foo.s3.eu-central-1.amazonaws.com</Endpoint>'
            b'</Error>')

        self.success_response = mock.Mock()
        self.success_response.headers = {}
        self.success_response.status_code = 200
        self.success_response.content = (
            b'<?xml version="1.0" encoding="UTF-8"?>\n'
            b'<ListBucketResult>'
            b'    <Name>foo</Name>'
            b'    <Prefix></Prefix>'
            b'    <Marker></Marker>'
            b'    <MaxKeys>1000</MaxKeys>'
            b'    <EncodingType>url</EncodingType>'
            b'    <IsTruncated>false</IsTruncated>'
            b'</ListBucketResult>')

    def test_region_redirect(self):
        self.http_session_send_mock.side_effect = [
            self.redirect_response, self.success_response]
        response = self.client.list_objects(Bucket='foo')
        self.assertEqual(response['ResponseMetadata']['HTTPStatusCode'], 200)
        self.assertEqual(self.http_session_send_mock.call_count, 2)

        calls = [c[0][0] for c in self.http_session_send_mock.call_args_list]
        initial_url = ('https://s3-us-west-2.amazonaws.com/foo'
                       '?encoding-type=url')
        self.assertEqual(calls[0].url, initial_url)

        fixed_url = ('https://s3.eu-central-1.amazonaws.com/foo'
                     '?encoding-type=url')
        self.assertEqual(calls[1].url, fixed_url)

    def test_region_redirect_cache(self):
        self.http_session_send_mock.side_effect = [
            self.redirect_response, self.success_response,
            self.success_response]

        first_response = self.client.list_objects(Bucket='foo')
        self.assertEqual(
            first_response['ResponseMetadata']['HTTPStatusCode'], 200)
        second_response = self.client.list_objects(Bucket='foo')
        self.assertEqual(
            second_response['ResponseMetadata']['HTTPStatusCode'], 200)

        self.assertEqual(self.http_session_send_mock.call_count, 3)
        calls = [c[0][0] for c in self.http_session_send_mock.call_args_list]
        initial_url = ('https://s3-us-west-2.amazonaws.com/foo'
                       '?encoding-type=url')
        self.assertEqual(calls[0].url, initial_url)

        fixed_url = ('https://s3.eu-central-1.amazonaws.com/foo'
                     '?encoding-type=url')
        self.assertEqual(calls[1].url, fixed_url)
        self.assertEqual(calls[2].url, fixed_url)


class TestGeneratePresigned(BaseS3OperationTest):
    def test_generate_unauthed_url(self):
        config = Config(signature_version=botocore.UNSIGNED)
        client = self.session.create_client('s3', self.region, config=config)
        url = client.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': 'foo',
                'Key': 'bar'
            })
        self.assertEqual(url, 'https://foo.s3.amazonaws.com/bar')

    def test_generate_unauthed_post(self):
        config = Config(signature_version=botocore.UNSIGNED)
        client = self.session.create_client('s3', self.region, config=config)
        parts = client.generate_presigned_post(Bucket='foo', Key='bar')
        expected = {
            'fields': {'key': 'bar'},
            'url': 'https://foo.s3.amazonaws.com/'
        }
        self.assertEqual(parts, expected)
