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
from tests import unittest, mock, BaseSessionTest, create_session
import os
import nose
from nose.tools import assert_equal

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



def test_correct_url_used_for_s3():
    # Test that given various sets of config options and bucket names,
    # we construct the expect endpoint url.
    t = S3AddressingCases(_verify_expected_endpoint_url)

    # The default behavior.  DNS compatible buckets
    yield t.case(region='us-west-2', bucket='bucket', key='key',
                 expected_url='https://bucket.s3.amazonaws.com/key')
    yield t.case(region='us-east-1', bucket='bucket', key='key',
                 expected_url='https://bucket.s3.amazonaws.com/key')
    yield t.case(region='us-west-1', bucket='bucket', key='key',
                 expected_url='https://bucket.s3.amazonaws.com/key')
    yield t.case(region='us-west-1', bucket='bucket', key='key',
                 is_secure=False,
                 expected_url='http://bucket.s3.amazonaws.com/key')

    # If you don't have a DNS compatible bucket, we use path style.
    yield t.case(
        region='us-west-2', bucket='bucket.dot', key='key',
        expected_url='https://s3-us-west-2.amazonaws.com/bucket.dot/key')
    yield t.case(
        region='us-east-1', bucket='bucket.dot', key='key',
        expected_url='https://s3.amazonaws.com/bucket.dot/key')

    # Custom endpoint url should always be used.
    yield t.case(
        customer_provided_endpoint='https://my-custom-s3/',
        bucket='foo', key='bar',
        expected_url='https://my-custom-s3/foo/bar')
    yield t.case(
        customer_provided_endpoint='https://my-custom-s3/',
        bucket='bucket.dots', key='bar',
        expected_url='https://my-custom-s3/bucket.dots/bar')
    # Doesn't matter what region you specify, a custom endpoint url always
    # wins.
    yield t.case(
        customer_provided_endpoint='https://my-custom-s3/',
        region='us-west-2', bucket='foo', key='bar',
        expected_url='https://my-custom-s3/foo/bar')

    # Explicitly configuring "virtual" addressing_style.
    virtual_hosting = {'addressing_style': 'virtual'}
    yield t.case(
        region='us-east-1', bucket='bucket', key='key',
        s3_config=virtual_hosting,
        expected_url='https://bucket.s3.amazonaws.com/key')
    yield t.case(
        region='us-west-2', bucket='bucket', key='key',
        s3_config=virtual_hosting,
        expected_url='https://bucket.s3-us-west-2.amazonaws.com/key')
    yield t.case(
        region='eu-central-1', bucket='bucket', key='key',
        s3_config=virtual_hosting,
        expected_url='https://bucket.s3.eu-central-1.amazonaws.com/key')
    yield t.case(
        region='us-east-1', bucket='bucket', key='key',
        s3_config=virtual_hosting,
        customer_provided_endpoint='https://foo.amazonaws.com',
        expected_url='https://bucket.foo.amazonaws.com/key')

    # Test us-gov with virtual addressing.
    yield t.case(
        region='us-gov-west-1', bucket='bucket', key='key',
        s3_config=virtual_hosting,
        expected_url='https://bucket.s3-us-gov-west-1.amazonaws.com/key')

    # Test path style addressing.
    path_style = {'addressing_style': 'path'}
    yield t.case(
        region='us-east-1', bucket='bucket', key='key',
        s3_config=path_style,
        expected_url='https://s3.amazonaws.com/bucket/key')
    yield t.case(
        region='us-east-1', bucket='bucket', key='key',
        s3_config=path_style,
        customer_provided_endpoint='https://foo.amazonaws.com/',
        expected_url='https://foo.amazonaws.com/bucket/key')


    # S3 accelerate
    use_accelerate = {'use_accelerate_endpoint': True}
    yield t.case(
        region='us-east-1', bucket='bucket', key='key',
        s3_config=use_accelerate,
        expected_url='https://bucket.s3-accelerate.amazonaws.com/key')
    yield t.case(
        # region is ignored with S3 accelerate.
        region='us-west-2', bucket='bucket', key='key',
        s3_config=use_accelerate,
        expected_url='https://bucket.s3-accelerate.amazonaws.com/key')
    yield t.case(
        region='us-east-1', bucket='bucket', key='key',
        customer_provided_endpoint='https://s3-accelerate.amazonaws.com',
        expected_url='https://bucket.s3-accelerate.amazonaws.com/key')
    yield t.case(
        region='us-east-1', bucket='bucket', key='key',
        customer_provided_endpoint='http://s3-accelerate.amazonaws.com',
        expected_url='http://bucket.s3-accelerate.amazonaws.com/key')
    yield t.case(
        region='us-east-1', bucket='bucket', key='key',
        s3_config=use_accelerate, is_secure=False,
        # Note we're using http://  because is_secure=False.
        expected_url='http://bucket.s3-accelerate.amazonaws.com/key')
    # Use virtual even if path is specified for s3 accelerate because
    # path style will not work with S3 accelerate.
    yield t.case(
        region='us-east-1', bucket='bucket', key='key',
        s3_config={'use_accelerate_endpoint': True,
                   'addressing_style': 'path'},
        expected_url='https://bucket.s3-accelerate.amazonaws.com/key')

    # S3 dual stack endpoints.
    use_dualstack = {'use_dualstack_endpoint': True}
    yield t.case(
        region='us-east-1', bucket='bucket', key='key',
        s3_config=use_dualstack,
        # Still default to virtual hosted when possible.
        expected_url='https://bucket.s3.dualstack.us-east-1.amazonaws.com/key')
    yield t.case(
        region='us-west-2', bucket='bucket', key='key',
        s3_config=use_dualstack,
        # Still default to virtual hosted when possible.
        expected_url='https://bucket.s3.dualstack.us-west-2.amazonaws.com/key')
    # Non DNS compatible buckets use path style for dual stack.
    yield t.case(
        region='us-west-2', bucket='bucket.dot', key='key',
        s3_config=use_dualstack,
        # Still default to virtual hosted when possible.
        expected_url='https://s3.dualstack.us-west-2.amazonaws.com/bucket.dot/key')
    # Supports is_secure (use_ssl=False in create_client()).
    yield t.case(
        region='us-west-2', bucket='bucket.dot', key='key', is_secure=False,
        s3_config=use_dualstack,
        # Still default to virtual hosted when possible.
        expected_url='http://s3.dualstack.us-west-2.amazonaws.com/bucket.dot/key')

    # Is path style is requested, we should use it, even if the bucket is
    # DNS compatible.
    force_path_style = {
        'use_dualstack_endpoint': True,
        'addressing_style': 'path',
    }
    yield t.case(
        region='us-west-2', bucket='bucket', key='key',
        s3_config=force_path_style,
        # Still default to virtual hosted when possible.
        expected_url='https://s3.dualstack.us-west-2.amazonaws.com/bucket/key')


class S3AddressingCases(object):
    def __init__(self, verify_function):
        self._verify = verify_function

    def case(self, region=None, bucket='bucket', key='key',
             s3_config=None, is_secure=True, customer_provided_endpoint=None,
             expected_url=None):
        return (
            self._verify, region, bucket, key, s3_config, is_secure,
            customer_provided_endpoint, expected_url
        )


def _verify_expected_endpoint_url(region, bucket, key, s3_config,
                                  is_secure=True,
                                  customer_provided_endpoint=None,
                                  expected_url=None):
    http_response = mock.Mock()
    http_response.status_code = 200
    http_response.headers = {}
    http_response.content = b''
    environ = {}
    with mock.patch('os.environ', environ):
        environ['AWS_ACCESS_KEY_ID'] = 'access_key'
        environ['AWS_SECRET_ACCESS_KEY'] = 'secret_key'
        environ['AWS_CONFIG_FILE'] = 'no-exist-foo'
        session = create_session()
        session.config_filename = 'no-exist-foo'
        config = None
        if s3_config is not None:
            config = Config(s3=s3_config)
        s3 = session.create_client('s3', region_name=region, use_ssl=is_secure,
                                   config=config,
                                   endpoint_url=customer_provided_endpoint)
        with mock.patch('botocore.endpoint.Session.send') as mock_send:
            mock_send.return_value = http_response
            s3.put_object(Bucket=bucket,
                          Key=key, Body=b'bar')
            request_sent = mock_send.call_args[0][0]
            assert_equal(request_sent.url, expected_url)
