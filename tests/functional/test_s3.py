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
from botocore.exceptions import ParamValidationError


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
            self.client.put_object(Bucket='foo', Key='bar',
                                Metadata={'goodkey': 'good',
                                          'non-ascii': u'\u2713'})

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
