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
import re

from tests import temporary_file
from tests import unittest, mock, BaseSessionTest, create_session, ClientHTTPStubber
from nose.tools import assert_equal

import botocore.session
from botocore.config import Config
from botocore.compat import datetime, urlsplit, parse_qs
from botocore.exceptions import ParamValidationError, ClientError
from botocore.exceptions import InvalidS3UsEast1RegionalEndpointConfigError
from botocore.parsers import ResponseParserError
from botocore import UNSIGNED


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
        self.http_stubber = ClientHTTPStubber(self.client)


class BaseS3ClientConfigurationTest(BaseSessionTest):
    def setUp(self):
        super(BaseS3ClientConfigurationTest, self).setUp()
        self.region = 'us-west-2'

    def create_s3_client(self, **kwargs):
        client_kwargs = {
            'region_name': self.region
        }
        client_kwargs.update(kwargs)
        return self.session.create_client('s3', **client_kwargs)

    def set_config_file(self, fileobj, contents):
        fileobj.write(contents)
        fileobj.flush()
        self.environ['AWS_CONFIG_FILE'] = fileobj.name


class TestS3ClientConfigResolution(BaseS3ClientConfigurationTest):
    def test_no_s3_config(self):
        client = self.create_s3_client()
        self.assertIsNone(client.meta.config.s3)

    def test_client_s3_dualstack_handles_uppercase_true(self):
        with temporary_file('w') as f:
            self.set_config_file(
                f,
                '[default]\n'
                's3 = \n'
                '    use_dualstack_endpoint = True'
            )
            client = self.create_s3_client()
            self.assertEqual(
                client.meta.config.s3['use_dualstack_endpoint'], True)

    def test_client_s3_dualstack_handles_lowercase_true(self):
        with temporary_file('w') as f:
            self.set_config_file(
                f,
                '[default]\n'
                's3 = \n'
                '    use_dualstack_endpoint = true'
            )
            client = self.create_s3_client()
            self.assertEqual(
                client.meta.config.s3['use_dualstack_endpoint'], True)

    def test_client_s3_accelerate_handles_uppercase_true(self):
        with temporary_file('w') as f:
            self.set_config_file(
                f,
                '[default]\n'
                's3 = \n'
                '    use_accelerate_endpoint = True'
            )
            client = self.create_s3_client()
            self.assertEqual(
                client.meta.config.s3['use_accelerate_endpoint'], True)

    def test_client_s3_accelerate_handles_lowercase_true(self):
        with temporary_file('w') as f:
            self.set_config_file(
                f,
                '[default]\n'
                's3 = \n'
                '    use_accelerate_endpoint = true'
            )
            client = self.create_s3_client()
            self.assertEqual(
                client.meta.config.s3['use_accelerate_endpoint'], True)

    def test_client_payload_signing_enabled_handles_uppercase_true(self):
        with temporary_file('w') as f:
            self.set_config_file(
                f,
                '[default]\n'
                's3 = \n'
                '    payload_signing_enabled = True'
            )
            client = self.create_s3_client()
            self.assertEqual(
                client.meta.config.s3['payload_signing_enabled'], True)

    def test_client_payload_signing_enabled_handles_lowercase_true(self):
        with temporary_file('w') as f:
            self.set_config_file(
                f,
                '[default]\n'
                's3 = \n'
                '    payload_signing_enabled = true'
            )
            client = self.create_s3_client()
            self.assertEqual(
                client.meta.config.s3['payload_signing_enabled'], True)

    def test_includes_unmodeled_s3_config_vars(self):
        with temporary_file('w') as f:
            self.set_config_file(
                f,
                '[default]\n'
                's3 = \n'
                '    unmodeled = unmodeled_val'
            )
            client = self.create_s3_client()
            self.assertEqual(
                client.meta.config.s3['unmodeled'], 'unmodeled_val')

    def test_mixed_modeled_and_unmodeled_config_vars(self):
        with temporary_file('w') as f:
            self.set_config_file(
                f,
                '[default]\n'
                's3 = \n'
                '    payload_signing_enabled = true\n'
                '    unmodeled = unmodeled_val'
            )
            client = self.create_s3_client()
            self.assertEqual(
                client.meta.config.s3,
                {
                    'payload_signing_enabled': True,
                    'unmodeled': 'unmodeled_val'
                }
            )

    def test_use_arn_region(self):
        self.environ['AWS_S3_USE_ARN_REGION'] = 'true'
        client = self.create_s3_client()
        self.assertEqual(
            client.meta.config.s3,
            {
                'use_arn_region': True,
            }
        )

    def test_use_arn_region_config_var(self):
        with temporary_file('w') as f:
            self.set_config_file(
                f,
                '[default]\n'
                's3_use_arn_region = true'
            )
            client = self.create_s3_client()
            self.assertEqual(
                client.meta.config.s3,
                {
                    'use_arn_region': True,
                }
            )

    def test_use_arn_region_nested_config_var(self):
        with temporary_file('w') as f:
            self.set_config_file(
                f,
                '[default]\n'
                's3 = \n'
                '    use_arn_region = true'
            )
            client = self.create_s3_client()
            self.assertEqual(
                client.meta.config.s3,
                {
                    'use_arn_region': True,
                }
            )

    def test_use_arn_region_is_case_insensitive(self):
        self.environ['AWS_S3_USE_ARN_REGION'] = 'True'
        client = self.create_s3_client()
        self.assertEqual(
            client.meta.config.s3,
            {
                'use_arn_region': True,
            }
        )

    def test_use_arn_region_env_var_overrides_config_var(self):
        self.environ['AWS_S3_USE_ARN_REGION'] = 'false'
        with temporary_file('w') as f:
            self.set_config_file(
                f,
                '[default]\n'
                's3 = \n'
                '    use_arn_region = true'
            )
            client = self.create_s3_client()
        self.assertEqual(
            client.meta.config.s3,
            {
                'use_arn_region': False,
            }
        )

    def test_client_config_use_arn_region_overrides_env_var(self):
        self.environ['AWS_S3_USE_ARN_REGION'] = 'true'
        client = self.create_s3_client(
            config=Config(
                s3={'use_arn_region': False}
            )
        )
        self.assertEqual(
            client.meta.config.s3,
            {
                'use_arn_region': False,
            }
        )

    def test_client_config_use_arn_region_overrides_config_var(self):
        with temporary_file('w') as f:
            self.set_config_file(
                f,
                '[default]\n'
                's3 = \n'
                '    use_arn_region = true'
            )
            client = self.create_s3_client(
                config=Config(
                    s3={'use_arn_region': False}
                )
            )
        self.assertEqual(
            client.meta.config.s3,
            {
                'use_arn_region': False,
            }
        )

    def test_use_arn_region_is_case_insensitive(self):
        self.environ['AWS_S3_USE_ARN_REGION'] = 'True'
        client = self.create_s3_client()
        self.assertEqual(
            client.meta.config.s3,
            {
                'use_arn_region': True,
            }
        )


    def test_us_east_1_regional_env_var(self):
        self.environ['AWS_S3_US_EAST_1_REGIONAL_ENDPOINT'] = 'regional'
        client = self.create_s3_client()
        self.assertEqual(
            client.meta.config.s3,
            {
                'us_east_1_regional_endpoint': 'regional',
            }
        )

    def test_us_east_1_regional_config_var(self):
        with temporary_file('w') as f:
            self.set_config_file(
                f,
                '[default]\n'
                's3_us_east_1_regional_endpoint = regional'
            )
            client = self.create_s3_client()
            self.assertEqual(
                client.meta.config.s3,
                {
                    'us_east_1_regional_endpoint': 'regional',
                }
            )

    def test_us_east_1_regional_nested_config_var(self):
        with temporary_file('w') as f:
            self.set_config_file(
                f,
                '[default]\n'
                's3 = \n'
                '    us_east_1_regional_endpoint = regional'
            )
            client = self.create_s3_client()
            self.assertEqual(
                client.meta.config.s3,
                {
                    'us_east_1_regional_endpoint': 'regional',
                }
            )

    def test_us_east_1_regional_env_var_overrides_config_var(self):
        self.environ['AWS_S3_US_EAST_1_REGIONAL_ENDPOINT'] = 'regional'
        with temporary_file('w') as f:
            self.set_config_file(
                f,
                '[default]\n'
                's3 = \n'
                '    us_east_1_regional_endpoint = legacy'
            )
            client = self.create_s3_client()
        self.assertEqual(
            client.meta.config.s3,
            {
                'us_east_1_regional_endpoint': 'regional',
            }
        )

    def test_client_config_us_east_1_regional_overrides_env_var(self):
        self.environ['AWS_S3_US_EAST_1_REGIONAL_ENDPOINT'] = 'regional'
        client = self.create_s3_client(
            config=Config(
                s3={'us_east_1_regional_endpoint': 'legacy'}
            )
        )
        self.assertEqual(
            client.meta.config.s3,
            {
                'us_east_1_regional_endpoint': 'legacy',
            }
        )

    def test_client_config_us_east_1_regional_overrides_config_var(self):
        with temporary_file('w') as f:
            self.set_config_file(
                f,
                '[default]\n'
                's3 = \n'
                '    us_east_1_regional_endpoint = legacy'
            )
            client = self.create_s3_client(
                config=Config(
                    s3={'us_east_1_regional_endpoint': 'regional'}
                )
            )
        self.assertEqual(
            client.meta.config.s3,
            {
                'us_east_1_regional_endpoint': 'regional',
            }
        )

    def test_client_validates_us_east_1_regional(self):
        with self.assertRaises(InvalidS3UsEast1RegionalEndpointConfigError):
            self.create_s3_client(
                config=Config(
                    s3={'us_east_1_regional_endpoint': 'not-valid'}
                )
            )

    def test_client_region_defaults_to_us_east_1(self):
        client = self.create_s3_client(region_name=None)
        self.assertEqual(client.meta.region_name, 'us-east-1')

    def test_client_region_remains_us_east_1(self):
        client = self.create_s3_client(region_name='us-east-1')
        self.assertEqual(client.meta.region_name, 'us-east-1')

    def test_client_region_remains_aws_global(self):
        client = self.create_s3_client(region_name='aws-global')
        self.assertEqual(client.meta.region_name, 'aws-global')

    def test_client_region_defaults_to_aws_global_for_regional(self):
        self.environ['AWS_S3_US_EAST_1_REGIONAL_ENDPOINT'] = 'regional'
        client = self.create_s3_client(region_name=None)
        self.assertEqual(client.meta.region_name, 'aws-global')

    def test_client_region_remains_us_east_1_for_regional(self):
        self.environ['AWS_S3_US_EAST_1_REGIONAL_ENDPOINT'] = 'regional'
        client = self.create_s3_client(region_name='us-east-1')
        self.assertEqual(client.meta.region_name, 'us-east-1')

    def test_client_region_remains_aws_global_for_regional(self):
        self.environ['AWS_S3_US_EAST_1_REGIONAL_ENDPOINT'] = 'regional'
        client = self.create_s3_client(region_name='aws-global')
        self.assertEqual(client.meta.region_name, 'aws-global')


class TestS3Copy(BaseS3OperationTest):

    def create_s3_client(self, **kwargs):
        client_kwargs = {
            'region_name': self.region
        }
        client_kwargs.update(kwargs)
        return self.session.create_client('s3', **client_kwargs)

    def create_stubbed_s3_client(self, **kwargs):
        client = self.create_s3_client(**kwargs)
        http_stubber = ClientHTTPStubber(client)
        http_stubber.start()
        return client, http_stubber

    def test_s3_copy_object_with_empty_response(self):
        self.client, self.http_stubber = self.create_stubbed_s3_client(
            region_name='us-east-1'
        )

        empty_body = b''
        complete_body = (
            b'<?xml version="1.0" encoding="UTF-8"?>\n\n'
            b'<CopyObjectResult '
            b'xmlns="http://s3.amazonaws.com/doc/2006-03-01/">'
            b'<LastModified>2020-04-21T21:03:31.000Z</LastModified>'
            b'<ETag>&quot;s0mEcH3cK5uM&quot;</ETag></CopyObjectResult>'
        )

        self.http_stubber.add_response(status=200, body=empty_body)
        self.http_stubber.add_response(status=200, body=complete_body)
        response = self.client.copy_object(
            Bucket='bucket',
            CopySource='other-bucket/test.txt',
            Key='test.txt',
        )

        # Validate we retried and got second body
        self.assertEquals(len(self.http_stubber.requests), 2)
        self.assertEquals(response['ResponseMetadata']['HTTPStatusCode'], 200)
        self.assertTrue('CopyObjectResult' in response)

    def test_s3_copy_object_with_incomplete_response(self):
        self.client, self.http_stubber = self.create_stubbed_s3_client(
            region_name='us-east-1'
        )

        incomplete_body = b'<?xml version="1.0" encoding="UTF-8"?>\n\n\n'
        self.http_stubber.add_response(status=200, body=incomplete_body)
        with self.assertRaises(ResponseParserError):
            self.client.copy_object(
                Bucket='bucket',
                CopySource='other-bucket/test.txt',
                Key='test.txt',
            )


class TestAccesspointArn(BaseS3ClientConfigurationTest):
    _V4_AUTH_REGEX = re.compile(
        r'AWS4-HMAC-SHA256 '
        r'Credential=\w+/\d+/'
        r'(?P<signing_region>[a-z0-9-]+)/'
    )

    def setUp(self):
        super(TestAccesspointArn, self).setUp()
        self.client, self.http_stubber = self.create_stubbed_s3_client()

    def create_stubbed_s3_client(self, **kwargs):
        client = self.create_s3_client(**kwargs)
        http_stubber = ClientHTTPStubber(client)
        http_stubber.start()
        return client, http_stubber

    def assert_signing_region(self, request, expected_region):
        auth_header = request.headers['Authorization'].decode('utf-8')
        actual_region = self._V4_AUTH_REGEX.match(
            auth_header).group('signing_region')
        self.assertEqual(expected_region, actual_region)

    def assert_signing_region_in_url(self, url, expected_region):
        qs_components = parse_qs(urlsplit(url).query)
        self.assertIn(expected_region, qs_components['X-Amz-Credential'][0])

    def test_missing_region_in_arn(self):
        accesspoint_arn = (
            'arn:aws:s3::123456789012:accesspoint:myendpoint'
        )
        with self.assertRaises(botocore.exceptions.ParamValidationError):
            self.client.list_objects(Bucket=accesspoint_arn)

    def test_missing_account_id_in_arn(self):
        accesspoint_arn = (
            'arn:aws:s3:us-west-2::accesspoint:myendpoint'
        )
        with self.assertRaises(botocore.exceptions.ParamValidationError):
            self.client.list_objects(Bucket=accesspoint_arn)

    def test_missing_accesspoint_name_in_arn(self):
        accesspoint_arn = (
            'arn:aws:s3:us-west-2:123456789012:accesspoint'
        )
        with self.assertRaises(botocore.exceptions.ParamValidationError):
            self.client.list_objects(Bucket=accesspoint_arn)

    def test_accesspoint_includes_asterisk(self):
        accesspoint_arn = (
            'arn:aws:s3:us-west-2:123456789012:accesspoint:*'
        )
        with self.assertRaises(botocore.exceptions.ParamValidationError):
            self.client.list_objects(Bucket=accesspoint_arn)

    def test_accesspoint_includes_dot(self):
        accesspoint_arn = (
            'arn:aws:s3:us-west-2:123456789012:accesspoint:my.endpoint'
        )
        with self.assertRaises(botocore.exceptions.ParamValidationError):
            self.client.list_objects(Bucket=accesspoint_arn)

    def test_accesspoint_arn_contains_subresources(self):
        accesspoint_arn = (
            'arn:aws:s3:us-west-2:123456789012:accesspoint:myendpoint:object'
        )
        with self.assertRaises(botocore.exceptions.ParamValidationError):
            self.client.list_objects(Bucket=accesspoint_arn)

    def test_accesspoint_arn_with_custom_endpoint(self):
        accesspoint_arn = (
            'arn:aws:s3:us-west-2:123456789012:accesspoint:myendpoint'
        )
        self.client, _ = self.create_stubbed_s3_client(
            endpoint_url='https://custom.com')
        with self.assertRaises(
                botocore.exceptions.
                UnsupportedS3AccesspointConfigurationError):
            self.client.list_objects(Bucket=accesspoint_arn)

    def test_accesspoint_arn_with_s3_accelerate(self):
        accesspoint_arn = (
            'arn:aws:s3:us-west-2:123456789012:accesspoint:myendpoint'
        )
        self.client, _ = self.create_stubbed_s3_client(
            config=Config(s3={'use_accelerate_endpoint': True}))
        with self.assertRaises(
                botocore.exceptions.
                UnsupportedS3AccesspointConfigurationError):
            self.client.list_objects(Bucket=accesspoint_arn)

    def test_accesspoint_arn_cross_partition(self):
        accesspoint_arn = (
            'arn:aws:s3:us-west-2:123456789012:accesspoint:myendpoint'
        )
        self.client, _ = self.create_stubbed_s3_client(
            region_name='cn-north-1')
        with self.assertRaises(
                botocore.exceptions.
                UnsupportedS3AccesspointConfigurationError):
            self.client.list_objects(Bucket=accesspoint_arn)

    def test_accesspoint_arn_cross_partition_use_client_region(self):
        accesspoint_arn = (
            'arn:aws:s3:us-west-2:123456789012:accesspoint:myendpoint'
        )
        self.client, _ = self.create_stubbed_s3_client(
            region_name='cn-north-1',
            config=Config(s3={'use_accelerate_endpoint': True})
        )
        with self.assertRaises(
                botocore.exceptions.
                UnsupportedS3AccesspointConfigurationError):
            self.client.list_objects(Bucket=accesspoint_arn)

    def test_signs_with_arn_region(self):
        accesspoint_arn = (
            'arn:aws:s3:us-west-2:123456789012:accesspoint:myendpoint'
        )
        self.client, self.http_stubber = self.create_stubbed_s3_client(
            region_name='us-east-1')
        self.http_stubber.add_response()
        self.client.list_objects(Bucket=accesspoint_arn)
        self.assert_signing_region(self.http_stubber.requests[0], 'us-west-2')

    def test_signs_with_client_region_when_use_arn_region_false(self):
        accesspoint_arn = (
            'arn:aws:s3:us-west-2:123456789012:accesspoint:myendpoint'
        )
        self.client, self.http_stubber = self.create_stubbed_s3_client(
            region_name='us-east-1',
            config=Config(s3={'use_arn_region': False})
        )
        self.http_stubber.add_response()
        self.client.list_objects(Bucket=accesspoint_arn)
        self.assert_signing_region(self.http_stubber.requests[0], 'us-east-1')

    def test_presign_signs_with_arn_region(self):
        accesspoint_arn = (
            'arn:aws:s3:us-west-2:123456789012:accesspoint:myendpoint'
        )
        self.client, _ = self.create_stubbed_s3_client(
            region_name='us-east-1',
            config=Config(signature_version='s3v4')
        )
        url = self.client.generate_presigned_url(
            'get_object', {'Bucket': accesspoint_arn, 'Key': 'mykey'})
        self.assert_signing_region_in_url(url, 'us-west-2')

    def test_presign_signs_with_client_region_when_use_arn_region_false(self):
        accesspoint_arn = (
            'arn:aws:s3:us-west-2:123456789012:accesspoint:myendpoint'
        )
        self.client, _ = self.create_stubbed_s3_client(
            region_name='us-east-1',
            config=Config(
                signature_version='s3v4', s3={'use_arn_region': False}
            )
        )
        url = self.client.generate_presigned_url(
            'get_object', {'Bucket': accesspoint_arn, 'Key': 'mykey'})
        self.assert_signing_region_in_url(url, 'us-east-1')


class TestOnlyAsciiCharsAllowed(BaseS3OperationTest):
    def test_validates_non_ascii_chars_trigger_validation_error(self):
        self.http_stubber.add_response()
        with self.http_stubber:
            with self.assertRaises(ParamValidationError):
                self.client.put_object(
                    Bucket='foo', Key='bar', Metadata={
                        'goodkey': 'good', 'non-ascii': u'\u2713'})


class TestS3GetBucketLifecycle(BaseS3OperationTest):
    def test_multiple_transitions_returns_one(self):
        response_body = (
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
        s3 = self.session.create_client('s3')
        with ClientHTTPStubber(s3) as http_stubber:
            http_stubber.add_response(body=response_body)
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
        s3 = self.session.create_client('s3')
        with ClientHTTPStubber(s3) as http_stubber:
            http_stubber.add_response(status=500, body=non_xml_content)
            http_stubber.add_response()
            response = s3.put_object(Bucket='mybucket', Key='mykey', Body=b'foo')
            # The first response should have been retried even though the xml is
            # invalid and eventually return the 200 response.
            self.assertEqual(response['ResponseMetadata']['HTTPStatusCode'], 200)
            self.assertEqual(len(http_stubber.requests), 2)


class TestS3SigV4(BaseS3OperationTest):
    def setUp(self):
        super(TestS3SigV4, self).setUp()
        self.client = self.session.create_client(
            's3', self.region, config=Config(signature_version='s3v4'))
        self.http_stubber = ClientHTTPStubber(self.client)
        self.http_stubber.add_response()

    def get_sent_headers(self):
        return self.http_stubber.requests[0].headers

    def test_content_md5_set(self):
        with self.http_stubber:
            self.client.put_object(Bucket='foo', Key='bar', Body='baz')
        self.assertIn('content-md5', self.get_sent_headers())

    def test_content_sha256_set_if_config_value_is_true(self):
        config = Config(signature_version='s3v4', s3={
            'payload_signing_enabled': True
        })
        self.client = self.session.create_client(
            's3', self.region, config=config)
        self.http_stubber = ClientHTTPStubber(self.client)
        self.http_stubber.add_response()
        with self.http_stubber:
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
        self.http_stubber = ClientHTTPStubber(self.client)
        self.http_stubber.add_response()
        with self.http_stubber:
            self.client.put_object(Bucket='foo', Key='bar', Body='baz')
        sent_headers = self.get_sent_headers()
        sha_header = sent_headers.get('x-amz-content-sha256')
        self.assertEqual(sha_header, b'UNSIGNED-PAYLOAD')

    def test_content_sha256_set_if_md5_is_unavailable(self):
        with mock.patch('botocore.auth.MD5_AVAILABLE', False):
            with mock.patch('botocore.utils.MD5_AVAILABLE', False):
                with self.http_stubber:
                    self.client.put_object(Bucket='foo', Key='bar', Body='baz')
        sent_headers = self.get_sent_headers()
        unsigned = 'UNSIGNED-PAYLOAD'
        self.assertNotEqual(sent_headers['x-amz-content-sha256'], unsigned)
        self.assertNotIn('content-md5', sent_headers)



class TestCanSendIntegerHeaders(BaseSessionTest):

    def test_int_values_with_sigv4(self):
        s3 = self.session.create_client(
            's3', config=Config(signature_version='s3v4'))
        with ClientHTTPStubber(s3) as http_stubber:
            http_stubber.add_response()
            s3.upload_part(Bucket='foo', Key='bar', Body=b'foo',
                           UploadId='bar', PartNumber=1, ContentLength=3)
            headers = http_stubber.requests[0].headers
            # Verify that the request integer value of 3 has been converted to
            # string '3'.  This also means we've made it pass the signer which
            # expects string values in order to sign properly.
            self.assertEqual(headers['Content-Length'], b'3')


class TestRegionRedirect(BaseS3OperationTest):
    def setUp(self):
        super(TestRegionRedirect, self).setUp()
        self.client = self.session.create_client(
            's3', 'us-west-2', config=Config(
                signature_version='s3v4',
                s3={'addressing_style': 'path'},
            ))
        self.http_stubber = ClientHTTPStubber(self.client)

        self.redirect_response = {
            'status': 301,
            'headers': {'x-amz-bucket-region': 'eu-central-1'},
            'body': (
                b'<?xml version="1.0" encoding="UTF-8"?>\n'
                b'<Error>'
                b'    <Code>PermanentRedirect</Code>'
                b'    <Message>The bucket you are attempting to access must be'
                b'        addressed using the specified endpoint. Please send '
                b'        all future requests to this endpoint.'
                b'    </Message>'
                b'    <Bucket>foo</Bucket>'
                b'    <Endpoint>foo.s3.eu-central-1.amazonaws.com</Endpoint>'
                b'</Error>'
            )
        }
        self.bad_signing_region_response = {
            'status': 400,
            'headers': {'x-amz-bucket-region': 'eu-central-1'},
            'body': (
                b'<?xml version="1.0" encoding="UTF-8"?>'
                b'<Error>'
                b'  <Code>AuthorizationHeaderMalformed</Code>'
                b'  <Message>the region us-west-2 is wrong; '
                b'expecting eu-central-1</Message>'
                b'  <Region>eu-central-1</Region>'
                b'  <RequestId>BD9AA1730D454E39</RequestId>'
                b'  <HostId></HostId>'
                b'</Error>'
            )
        }
        self.success_response = {
            'status': 200,
            'headers': {},
            'body': (
                b'<?xml version="1.0" encoding="UTF-8"?>\n'
                b'<ListBucketResult>'
                b'    <Name>foo</Name>'
                b'    <Prefix></Prefix>'
                b'    <Marker></Marker>'
                b'    <MaxKeys>1000</MaxKeys>'
                b'    <EncodingType>url</EncodingType>'
                b'    <IsTruncated>false</IsTruncated>'
                b'</ListBucketResult>'
            )
        }

    def test_region_redirect(self):
        self.http_stubber.add_response(**self.redirect_response)
        self.http_stubber.add_response(**self.success_response)
        with self.http_stubber:
            response = self.client.list_objects(Bucket='foo')
        self.assertEqual(response['ResponseMetadata']['HTTPStatusCode'], 200)
        self.assertEqual(len(self.http_stubber.requests), 2)

        initial_url = ('https://s3.us-west-2.amazonaws.com/foo'
                       '?encoding-type=url')
        self.assertEqual(self.http_stubber.requests[0].url, initial_url)

        fixed_url = ('https://s3.eu-central-1.amazonaws.com/foo'
                     '?encoding-type=url')
        self.assertEqual(self.http_stubber.requests[1].url, fixed_url)

    def test_region_redirect_cache(self):
        self.http_stubber.add_response(**self.redirect_response)
        self.http_stubber.add_response(**self.success_response)
        self.http_stubber.add_response(**self.success_response)

        with self.http_stubber:
            first_response = self.client.list_objects(Bucket='foo')
            second_response = self.client.list_objects(Bucket='foo')

        self.assertEqual(
            first_response['ResponseMetadata']['HTTPStatusCode'], 200)
        self.assertEqual(
            second_response['ResponseMetadata']['HTTPStatusCode'], 200)

        self.assertEqual(len(self.http_stubber.requests), 3)
        initial_url = ('https://s3.us-west-2.amazonaws.com/foo'
                       '?encoding-type=url')
        self.assertEqual(self.http_stubber.requests[0].url, initial_url)

        fixed_url = ('https://s3.eu-central-1.amazonaws.com/foo'
                     '?encoding-type=url')
        self.assertEqual(self.http_stubber.requests[1].url, fixed_url)
        self.assertEqual(self.http_stubber.requests[2].url, fixed_url)

    def test_resign_request_with_region_when_needed(self):

        # Create a client with no explicit configuration so we can
        # verify the default behavior.
        client = self.session.create_client('s3', 'us-west-2')
        with ClientHTTPStubber(client) as http_stubber:
            http_stubber.add_response(**self.bad_signing_region_response)
            http_stubber.add_response(**self.success_response)
            first_response = client.list_objects(Bucket='foo')
            self.assertEqual(
                first_response['ResponseMetadata']['HTTPStatusCode'], 200)

            self.assertEqual(len(http_stubber.requests), 2)
            initial_url = ('https://foo.s3.us-west-2.amazonaws.com/'
                           '?encoding-type=url')
            self.assertEqual(http_stubber.requests[0].url, initial_url)

            fixed_url = ('https://foo.s3.eu-central-1.amazonaws.com/'
                         '?encoding-type=url')
            self.assertEqual(http_stubber.requests[1].url, fixed_url)

    def test_resign_request_in_us_east_1(self):
        region_headers = {'x-amz-bucket-region': 'eu-central-1'}

        # Verify that the default behavior in us-east-1 will redirect
        client = self.session.create_client('s3', 'us-east-1')
        with ClientHTTPStubber(client) as http_stubber:
            http_stubber.add_response(status=400)
            http_stubber.add_response(status=400, headers=region_headers)
            http_stubber.add_response(headers=region_headers)
            http_stubber.add_response()
            response = client.head_object(Bucket='foo', Key='bar')
            self.assertEqual(response['ResponseMetadata']['HTTPStatusCode'], 200)

            self.assertEqual(len(http_stubber.requests), 4)
            initial_url = ('https://foo.s3.amazonaws.com/bar')
            self.assertEqual(http_stubber.requests[0].url, initial_url)

            fixed_url = ('https://foo.s3.eu-central-1.amazonaws.com/bar')
            self.assertEqual(http_stubber.requests[-1].url, fixed_url)

    def test_resign_request_in_us_east_1_fails(self):
        region_headers = {'x-amz-bucket-region': 'eu-central-1'}

        # Verify that the final 400 response is propagated
        # back to the user.
        client = self.session.create_client('s3', 'us-east-1')
        with ClientHTTPStubber(client) as http_stubber:
            http_stubber.add_response(status=400)
            http_stubber.add_response(status=400, headers=region_headers)
            http_stubber.add_response(headers=region_headers)
            # The final request still fails with a 400.
            http_stubber.add_response(status=400)
            with self.assertRaises(ClientError) as e:
                client.head_object(Bucket='foo', Key='bar')
            self.assertEqual(len(http_stubber.requests), 4)

    def test_no_region_redirect_for_accesspoint(self):
        self.http_stubber.add_response(**self.redirect_response)
        accesspoint_arn = (
            'arn:aws:s3:us-west-2:123456789012:accesspoint:myendpoint'
        )
        with self.http_stubber:
            try:
                self.client.list_objects(Bucket=accesspoint_arn)
            except self.client.exceptions.ClientError as e:
                self.assertEqual(
                    e.response['Error']['Code'], 'PermanentRedirect')
            else:
                self.fail('PermanentRedirect error should have been raised')


class TestGeneratePresigned(BaseS3OperationTest):
    def assert_is_v2_presigned_url(self, url):
        qs_components = parse_qs(urlsplit(url).query)
        # Assert that it looks like a v2 presigned url by asserting it does
        # not have a couple of the v4 qs components and assert that it has the
        # v2 Signature component.
        self.assertNotIn('X-Amz-Credential', qs_components)
        self.assertNotIn('X-Amz-Algorithm', qs_components)
        self.assertIn('Signature', qs_components)

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

    def test_default_presign_uses_sigv2(self):
        url = self.client.generate_presigned_url(ClientMethod='list_buckets')
        self.assertNotIn('Algorithm=AWS4-HMAC-SHA256', url)

    def test_sigv4_presign(self):
        config = Config(signature_version='s3v4')
        client = self.session.create_client('s3', self.region, config=config)
        url = client.generate_presigned_url(ClientMethod='list_buckets')
        self.assertIn('Algorithm=AWS4-HMAC-SHA256', url)

    def test_sigv2_presign(self):
        config = Config(signature_version='s3')
        client = self.session.create_client('s3', self.region, config=config)
        url = client.generate_presigned_url(ClientMethod='list_buckets')
        self.assertNotIn('Algorithm=AWS4-HMAC-SHA256', url)

    def test_uses_sigv4_for_unknown_region(self):
        client = self.session.create_client('s3', 'us-west-88')
        url = client.generate_presigned_url(ClientMethod='list_buckets')
        self.assertIn('Algorithm=AWS4-HMAC-SHA256', url)

    def test_default_presign_sigv4_in_sigv4_only_region(self):
        client = self.session.create_client('s3', 'us-east-2')
        url = client.generate_presigned_url(ClientMethod='list_buckets')
        self.assertIn('Algorithm=AWS4-HMAC-SHA256', url)

    def test_presign_unsigned(self):
        config = Config(signature_version=botocore.UNSIGNED)
        client = self.session.create_client('s3', 'us-east-2', config=config)
        url = client.generate_presigned_url(ClientMethod='list_buckets')
        self.assertEqual(
            'https://s3.us-east-2.amazonaws.com/', url)

    def test_presign_url_with_ssec(self):
        config = Config(signature_version='s3')
        client = self.session.create_client('s3', 'us-east-1', config=config)
        url = client.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': 'mybucket',
                'Key': 'mykey',
                'SSECustomerKey': 'a' * 32,
                'SSECustomerAlgorithm': 'AES256'
            }
        )
        # The md5 of the sse-c key will be injected when parameters are
        # built so it should show up in the presigned url as well.
        self.assertIn(
            'x-amz-server-side-encryption-customer-key-md5=', url
        )

    def test_presign_s3_accelerate(self):
        config = Config(signature_version=botocore.UNSIGNED,
                        s3={'use_accelerate_endpoint': True})
        client = self.session.create_client('s3', 'us-east-1', config=config)
        url = client.generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': 'mybucket', 'Key': 'mykey'}
        )
        # The url should be the accelerate endpoint
        self.assertEqual(
            'https://mybucket.s3-accelerate.amazonaws.com/mykey', url)

    def test_presign_post_s3_accelerate(self):
        config = Config(signature_version=botocore.UNSIGNED,
                        s3={'use_accelerate_endpoint': True})
        client = self.session.create_client('s3', 'us-east-1', config=config)
        parts = client.generate_presigned_post(
            Bucket='mybucket', Key='mykey')
        # The url should be the accelerate endpoint
        expected = {
            'fields': {'key': 'mykey'},
            'url': 'https://mybucket.s3-accelerate.amazonaws.com/'
        }
        self.assertEqual(parts, expected)

    def test_presign_uses_v2_for_aws_global(self):
        client = self.session.create_client('s3', 'aws-global')
        url = client.generate_presigned_url(
            'get_object', {'Bucket': 'mybucket', 'Key': 'mykey'})
        self.assert_is_v2_presigned_url(url)

    def test_presign_uses_v2_for_default_region_with_us_east_1_regional(self):
        config = Config(s3={'us_east_1_regional_endpoint': 'regional'})
        client = self.session.create_client('s3', config=config)
        url = client.generate_presigned_url(
            'get_object', {'Bucket': 'mybucket', 'Key': 'mykey'})
        self.assert_is_v2_presigned_url(url)

    def test_presign_uses_v2_for_aws_global_with_us_east_1_regional(self):
        config = Config(s3={'us_east_1_regional_endpoint': 'regional'})
        client = self.session.create_client('s3', 'aws-global', config=config)
        url = client.generate_presigned_url(
            'get_object', {'Bucket': 'mybucket', 'Key': 'mykey'})
        self.assert_is_v2_presigned_url(url)

    def test_presign_uses_v2_for_us_east_1(self):
        client = self.session.create_client('s3', 'us-east-1')
        url = client.generate_presigned_url(
            'get_object', {'Bucket': 'mybucket', 'Key': 'mykey'})
        self.assert_is_v2_presigned_url(url)

    def test_presign_uses_v2_for_us_east_1_with_us_east_1_regional(self):
        config = Config(s3={'us_east_1_regional_endpoint': 'regional'})
        client = self.session.create_client('s3', 'us-east-1', config=config)
        url = client.generate_presigned_url(
            'get_object', {'Bucket': 'mybucket', 'Key': 'mykey'})
        self.assert_is_v2_presigned_url(url)

def test_checksums_included_in_expected_operations():
    """Validate expected calls include Content-MD5 header"""

    t = S3ChecksumCases(_verify_checksum_in_headers)
    yield t.case('put_bucket_tagging',
            {"Bucket": "foo", "Tagging":{"TagSet":[]}})
    yield t.case('put_bucket_lifecycle',
            {"Bucket": "foo", "LifecycleConfiguration":{"Rules":[]}})
    yield t.case('put_bucket_lifecycle_configuration',
            {"Bucket": "foo", "LifecycleConfiguration":{"Rules":[]}})
    yield t.case('put_bucket_cors',
            {"Bucket": "foo", "CORSConfiguration":{"CORSRules": []}})
    yield t.case('delete_objects',
            {"Bucket": "foo", "Delete": {"Objects": [{"Key": "bar"}]}})
    yield t.case('put_bucket_replication',
            {"Bucket": "foo",
             "ReplicationConfiguration": {"Role":"", "Rules": []}})
    yield t.case('put_bucket_acl',
            {"Bucket": "foo", "AccessControlPolicy":{}})
    yield t.case('put_bucket_logging',
            {"Bucket": "foo",
             "BucketLoggingStatus":{}})
    yield t.case('put_bucket_notification',
            {"Bucket": "foo", "NotificationConfiguration":{}})
    yield t.case('put_bucket_policy',
            {"Bucket": "foo", "Policy": "<bucket-policy>"})
    yield t.case('put_bucket_request_payment',
            {"Bucket": "foo", "RequestPaymentConfiguration":{"Payer": ""}})
    yield t.case('put_bucket_versioning',
            {"Bucket": "foo", "VersioningConfiguration":{}})
    yield t.case('put_bucket_website',
            {"Bucket": "foo",
             "WebsiteConfiguration":{}})
    yield t.case('put_object_acl',
            {"Bucket": "foo", "Key": "bar", "AccessControlPolicy":{}})
    yield t.case('put_object_legal_hold',
            {"Bucket": "foo", "Key": "bar", "LegalHold":{"Status": "ON"}})
    yield t.case('put_object_retention',
            {"Bucket": "foo", "Key": "bar",
             "Retention":{"RetainUntilDate":"2020-11-05"}})
    yield t.case('put_object_lock_configuration',
            {"Bucket": "foo", "ObjectLockConfiguration":{}})


def _verify_checksum_in_headers(operation, operation_kwargs):
    environ = {}
    with mock.patch('os.environ', environ):
        environ['AWS_ACCESS_KEY_ID'] = 'access_key'
        environ['AWS_SECRET_ACCESS_KEY'] = 'secret_key'
        environ['AWS_CONFIG_FILE'] = 'no-exist-foo'
        session = create_session()
        session.config_filename = 'no-exist-foo'
        client = session.create_client('s3')
        with ClientHTTPStubber(client) as stub:
            stub.add_response()
            call = getattr(client, operation)
            call(**operation_kwargs)
            assert 'Content-MD5' in stub.requests[-1].headers


def test_correct_url_used_for_s3():
    # Test that given various sets of config options and bucket names,
    # we construct the expect endpoint url.
    t = S3AddressingCases(_verify_expected_endpoint_url)

    # The default behavior for sigv2. DNS compatible buckets
    yield t.case(region='us-west-2', bucket='bucket', key='key',
                 signature_version='s3',
                 expected_url='https://bucket.s3.us-west-2.amazonaws.com/key')
    yield t.case(region='us-east-1', bucket='bucket', key='key',
                 signature_version='s3',
                 expected_url='https://bucket.s3.amazonaws.com/key')
    yield t.case(region='us-west-1', bucket='bucket', key='key',
                 signature_version='s3',
                 expected_url='https://bucket.s3.us-west-1.amazonaws.com/key')
    yield t.case(region='us-west-1', bucket='bucket', key='key',
                 signature_version='s3', is_secure=False,
                 expected_url='http://bucket.s3.us-west-1.amazonaws.com/key')

    # Virtual host addressing is independent of signature version.
    yield t.case(region='us-west-2', bucket='bucket', key='key',
                 signature_version='s3v4',
                 expected_url=(
                     'https://bucket.s3.us-west-2.amazonaws.com/key'))
    yield t.case(region='us-east-1', bucket='bucket', key='key',
                 signature_version='s3v4',
                 expected_url='https://bucket.s3.amazonaws.com/key')
    yield t.case(region='us-west-1', bucket='bucket', key='key',
                 signature_version='s3v4',
                 expected_url=(
                     'https://bucket.s3.us-west-1.amazonaws.com/key'))
    yield t.case(region='us-west-1', bucket='bucket', key='key',
                 signature_version='s3v4', is_secure=False,
                 expected_url=(
                     'http://bucket.s3.us-west-1.amazonaws.com/key'))
    yield t.case(
        region='us-west-1', bucket='bucket-with-num-1', key='key',
        signature_version='s3v4', is_secure=False,
        expected_url='http://bucket-with-num-1.s3.us-west-1.amazonaws.com/key')

    # Regions outside of the 'aws' partition.
    # These should still default to virtual hosted addressing
    # unless explicitly configured otherwise.
    yield t.case(region='cn-north-1', bucket='bucket', key='key',
                 signature_version='s3v4',
                 expected_url=(
                     'https://bucket.s3.cn-north-1.amazonaws.com.cn/key'))
    # This isn't actually supported because cn-north-1 is sigv4 only,
    # but we'll still double check that our internal logic is correct
    # when building the expected url.
    yield t.case(region='cn-north-1', bucket='bucket', key='key',
                 signature_version='s3',
                 expected_url=(
                     'https://bucket.s3.cn-north-1.amazonaws.com.cn/key'))
    # If the request is unsigned, we should have the default
    # fix_s3_host behavior which is to use virtual hosting where
    # possible but fall back to path style when needed.
    yield t.case(region='cn-north-1', bucket='bucket', key='key',
                 signature_version=UNSIGNED,
                 expected_url=(
                     'https://bucket.s3.cn-north-1.amazonaws.com.cn/key'))
    yield t.case(region='cn-north-1', bucket='bucket.dot', key='key',
                 signature_version=UNSIGNED,
                 expected_url=(
                     'https://s3.cn-north-1.amazonaws.com.cn/bucket.dot/key'))

    # And of course you can explicitly specify which style to use.
    virtual_hosting = {'addressing_style': 'virtual'}
    yield t.case(region='cn-north-1', bucket='bucket', key='key',
                 signature_version=UNSIGNED,
                 s3_config=virtual_hosting,
                 expected_url=(
                     'https://bucket.s3.cn-north-1.amazonaws.com.cn/key'))
    path_style = {'addressing_style': 'path'}
    yield t.case(region='cn-north-1', bucket='bucket', key='key',
                 signature_version=UNSIGNED,
                 s3_config=path_style,
                 expected_url=(
                     'https://s3.cn-north-1.amazonaws.com.cn/bucket/key'))

    # If you don't have a DNS compatible bucket, we use path style.
    yield t.case(
        region='us-west-2', bucket='bucket.dot', key='key',
        expected_url='https://s3.us-west-2.amazonaws.com/bucket.dot/key')
    yield t.case(
        region='us-east-1', bucket='bucket.dot', key='key',
        expected_url='https://s3.amazonaws.com/bucket.dot/key')
    yield t.case(
        region='us-east-1', bucket='BucketName', key='key',
        expected_url='https://s3.amazonaws.com/BucketName/key')
    yield t.case(
        region='us-west-1', bucket='bucket_name', key='key',
        expected_url='https://s3.us-west-1.amazonaws.com/bucket_name/key')
    yield t.case(
        region='us-west-1', bucket='-bucket-name', key='key',
        expected_url='https://s3.us-west-1.amazonaws.com/-bucket-name/key')
    yield t.case(
        region='us-west-1', bucket='bucket-name-', key='key',
        expected_url='https://s3.us-west-1.amazonaws.com/bucket-name-/key')
    yield t.case(
        region='us-west-1', bucket='aa', key='key',
        expected_url='https://s3.us-west-1.amazonaws.com/aa/key')
    yield t.case(
        region='us-west-1', bucket='a'*64, key='key',
        expected_url=('https://s3.us-west-1.amazonaws.com/%s/key' % ('a' * 64))
    )

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
        expected_url='https://bucket.s3.us-west-2.amazonaws.com/key')
    yield t.case(
        region='eu-central-1', bucket='bucket', key='key',
        s3_config=virtual_hosting,
        expected_url='https://bucket.s3.eu-central-1.amazonaws.com/key')
    yield t.case(
        region='us-east-1', bucket='bucket', key='key',
        s3_config=virtual_hosting,
        customer_provided_endpoint='https://foo.amazonaws.com',
        expected_url='https://bucket.foo.amazonaws.com/key')
    yield t.case(
        region='unknown', bucket='bucket', key='key',
        s3_config=virtual_hosting,
        expected_url='https://bucket.s3.unknown.amazonaws.com/key')

    # Test us-gov with virtual addressing.
    yield t.case(
        region='us-gov-west-1', bucket='bucket', key='key',
        s3_config=virtual_hosting,
        expected_url='https://bucket.s3.us-gov-west-1.amazonaws.com/key')

    yield t.case(
        region='us-gov-west-1', bucket='bucket', key='key',
        signature_version='s3',
        expected_url='https://bucket.s3.us-gov-west-1.amazonaws.com/key')
    yield t.case(
        region='fips-us-gov-west-1', bucket='bucket', key='key',
        signature_version='s3',
        expected_url='https://bucket.s3-fips-us-gov-west-1.amazonaws.com/key')


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
    yield t.case(
        region='unknown', bucket='bucket', key='key',
        s3_config=path_style,
        expected_url='https://s3.unknown.amazonaws.com/bucket/key')

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
    # Provided endpoints still get recognized as accelerate endpoints.
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
    yield t.case(
        region='us-east-1', bucket='bucket', key='key',
        # s3-accelerate must be the first part of the url.
        customer_provided_endpoint='https://foo.s3-accelerate.amazonaws.com',
        expected_url='https://foo.s3-accelerate.amazonaws.com/bucket/key')
    yield t.case(
        region='us-east-1', bucket='bucket', key='key',
        # The endpoint must be an Amazon endpoint.
        customer_provided_endpoint='https://s3-accelerate.notamazon.com',
        expected_url='https://s3-accelerate.notamazon.com/bucket/key')
    yield t.case(
        region='us-east-1', bucket='bucket', key='key',
        # Extra components must be whitelisted.
        customer_provided_endpoint='https://s3-accelerate.foo.amazonaws.com',
        expected_url='https://s3-accelerate.foo.amazonaws.com/bucket/key')
    yield t.case(
        region='unknown', bucket='bucket', key='key',
        s3_config=use_accelerate,
        expected_url='https://bucket.s3-accelerate.amazonaws.com/key')
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
        s3_config=use_dualstack, signature_version='s3',
        # Still default to virtual hosted when possible on sigv2.
        expected_url='https://bucket.s3.dualstack.us-east-1.amazonaws.com/key')
    yield t.case(
        region=None, bucket='bucket', key='key',
        s3_config=use_dualstack,
        # Uses us-east-1 for no region set.
        expected_url='https://bucket.s3.dualstack.us-east-1.amazonaws.com/key')
    yield t.case(
        region='aws-global', bucket='bucket', key='key',
        s3_config=use_dualstack,
        # Pseudo-regions should not have any special resolving logic even when
        # the endpoint won't work as we do not have the metadata to know that
        # a region does not support dualstack. So just format it based on the
        # region name.
        expected_url=(
            'https://bucket.s3.dualstack.aws-global.amazonaws.com/key'))
    yield t.case(
        region='us-west-2', bucket='bucket', key='key',
        s3_config=use_dualstack, signature_version='s3',
        # Still default to virtual hosted when possible on sigv2.
        expected_url='https://bucket.s3.dualstack.us-west-2.amazonaws.com/key')
    yield t.case(
        region='us-east-1', bucket='bucket', key='key',
        s3_config=use_dualstack, signature_version='s3v4',
        expected_url='https://bucket.s3.dualstack.us-east-1.amazonaws.com/key')
    yield t.case(
        region='us-west-2', bucket='bucket', key='key',
        s3_config=use_dualstack, signature_version='s3v4',
        expected_url='https://bucket.s3.dualstack.us-west-2.amazonaws.com/key')
    yield t.case(
        region='unknown', bucket='bucket', key='key',
        s3_config=use_dualstack, signature_version='s3v4',
        expected_url='https://bucket.s3.dualstack.unknown.amazonaws.com/key')
    # Non DNS compatible buckets use path style for dual stack.
    yield t.case(
        region='us-west-2', bucket='bucket.dot', key='key',
        s3_config=use_dualstack,
        # Still default to virtual hosted when possible.
        expected_url=(
            'https://s3.dualstack.us-west-2.amazonaws.com/bucket.dot/key'))
    # Supports is_secure (use_ssl=False in create_client()).
    yield t.case(
        region='us-west-2', bucket='bucket.dot', key='key', is_secure=False,
        s3_config=use_dualstack,
        # Still default to virtual hosted when possible.
        expected_url=(
            'http://s3.dualstack.us-west-2.amazonaws.com/bucket.dot/key'))

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

    # Accelerate + dual stack
    use_accelerate_dualstack = {
        'use_accelerate_endpoint': True,
        'use_dualstack_endpoint': True,
    }
    yield t.case(
        region='us-east-1', bucket='bucket', key='key',
        s3_config=use_accelerate_dualstack,
        expected_url=(
            'https://bucket.s3-accelerate.dualstack.amazonaws.com/key'))
    yield t.case(
        # Region is ignored with S3 accelerate.
        region='us-west-2', bucket='bucket', key='key',
        s3_config=use_accelerate_dualstack,
        expected_url=(
            'https://bucket.s3-accelerate.dualstack.amazonaws.com/key'))
    # Only s3-accelerate overrides a customer endpoint.
    yield t.case(
        region='us-east-1', bucket='bucket', key='key',
        s3_config=use_dualstack,
        customer_provided_endpoint='https://s3-accelerate.amazonaws.com',
        expected_url=(
            'https://bucket.s3-accelerate.amazonaws.com/key'))
    yield t.case(
        region='us-east-1', bucket='bucket', key='key',
        # Dualstack is whitelisted.
        customer_provided_endpoint=(
            'https://s3-accelerate.dualstack.amazonaws.com'),
        expected_url=(
            'https://bucket.s3-accelerate.dualstack.amazonaws.com/key'))
    yield t.case(
        region='us-east-1', bucket='bucket', key='key',
        # Even whitelisted parts cannot be duplicated.
        customer_provided_endpoint=(
            'https://s3-accelerate.dualstack.dualstack.amazonaws.com'),
        expected_url=(
            'https://s3-accelerate.dualstack.dualstack'
            '.amazonaws.com/bucket/key'))
    yield t.case(
        region='us-east-1', bucket='bucket', key='key',
        # More than two extra parts is not allowed.
        customer_provided_endpoint=(
            'https://s3-accelerate.dualstack.dualstack.dualstack'
            '.amazonaws.com'),
        expected_url=(
            'https://s3-accelerate.dualstack.dualstack.dualstack.amazonaws.com'
            '/bucket/key'))
    yield t.case(
        region='us-east-1', bucket='bucket', key='key',
        # Extra components must be whitelisted.
        customer_provided_endpoint='https://s3-accelerate.foo.amazonaws.com',
        expected_url='https://s3-accelerate.foo.amazonaws.com/bucket/key')
    yield t.case(
        region='us-east-1', bucket='bucket', key='key',
        s3_config=use_accelerate_dualstack, is_secure=False,
        # Note we're using http://  because is_secure=False.
        expected_url=(
            'http://bucket.s3-accelerate.dualstack.amazonaws.com/key'))
    # Use virtual even if path is specified for s3 accelerate because
    # path style will not work with S3 accelerate.
    use_accelerate_dualstack['addressing_style'] = 'path'
    yield t.case(
        region='us-east-1', bucket='bucket', key='key',
        s3_config=use_accelerate_dualstack,
        expected_url=(
            'https://bucket.s3-accelerate.dualstack.amazonaws.com/key'))

    # Access-point arn cases
    accesspoint_arn = (
        'arn:aws:s3:us-west-2:123456789012:accesspoint:myendpoint'
    )
    yield t.case(
        region='us-west-2', bucket=accesspoint_arn, key='key',
        expected_url=(
            'https://myendpoint-123456789012.s3-accesspoint.'
            'us-west-2.amazonaws.com/key'
        )
    )
    yield t.case(
        region='us-west-2', bucket=accesspoint_arn, key='key',
        s3_config={'use_arn_region': True},
        expected_url=(
            'https://myendpoint-123456789012.s3-accesspoint.'
            'us-west-2.amazonaws.com/key'
        )
    )
    yield t.case(
        region='us-west-2', bucket=accesspoint_arn, key='myendpoint/key',
        expected_url=(
            'https://myendpoint-123456789012.s3-accesspoint.'
            'us-west-2.amazonaws.com/myendpoint/key'
        )
    )
    yield t.case(
        region='us-west-2', bucket=accesspoint_arn, key='foo/myendpoint/key',
        expected_url=(
            'https://myendpoint-123456789012.s3-accesspoint.'
            'us-west-2.amazonaws.com/foo/myendpoint/key'
        )
    )
    yield t.case(
        # Note: The access-point arn has us-west-2 and the client's region is
        # us-east-1, for the default case the access-point arn region is used.
        region='us-east-1', bucket=accesspoint_arn, key='key',
        expected_url=(
            'https://myendpoint-123456789012.s3-accesspoint.'
            'us-west-2.amazonaws.com/key'
        )
    )
    yield t.case(
        region='us-east-1', bucket=accesspoint_arn, key='key',
        s3_config={'use_arn_region': False},
        expected_url=(
            'https://myendpoint-123456789012.s3-accesspoint.'
            'us-east-1.amazonaws.com/key'
        )
    )
    yield t.case(
        region='s3-external-1', bucket=accesspoint_arn, key='key',
        expected_url=(
            'https://myendpoint-123456789012.s3-accesspoint.'
            'us-west-2.amazonaws.com/key'
        )
    )
    yield t.case(
        region='s3-external-1', bucket=accesspoint_arn, key='key',
        s3_config={'use_arn_region': False},
        expected_url=(
            'https://myendpoint-123456789012.s3-accesspoint.'
            's3-external-1.amazonaws.com/key'
        )
    )
    yield t.case(
        region='aws-global', bucket=accesspoint_arn, key='key',
        expected_url=(
            'https://myendpoint-123456789012.s3-accesspoint.'
            'us-west-2.amazonaws.com/key'
        )
    )
    yield t.case(
        region='aws-global', bucket=accesspoint_arn, key='key',
        s3_config={'use_arn_region': False},
        expected_url=(
            'https://myendpoint-123456789012.s3-accesspoint.'
            'aws-global.amazonaws.com/key'
        )
    )
    yield t.case(
        region='unknown', bucket=accesspoint_arn, key='key',
        s3_config={'use_arn_region': False},
        expected_url=(
            'https://myendpoint-123456789012.s3-accesspoint.'
            'unknown.amazonaws.com/key'
        )
    )
    yield t.case(
        region='unknown', bucket=accesspoint_arn, key='key',
        s3_config={'use_arn_region': True},
        expected_url=(
            'https://myendpoint-123456789012.s3-accesspoint.'
            'us-west-2.amazonaws.com/key'
        )
    )
    accesspoint_arn_cn = (
        'arn:aws-cn:s3:cn-north-1:123456789012:accesspoint:myendpoint'
    )
    yield t.case(
        region='cn-north-1', bucket=accesspoint_arn_cn, key='key',
        expected_url=(
            'https://myendpoint-123456789012.s3-accesspoint.'
            'cn-north-1.amazonaws.com.cn/key'
        )
    )
    yield t.case(
        region='cn-northwest-1', bucket=accesspoint_arn_cn, key='key',
        expected_url=(
            'https://myendpoint-123456789012.s3-accesspoint.'
            'cn-north-1.amazonaws.com.cn/key'
        )
    )
    yield t.case(
        region='cn-northwest-1', bucket=accesspoint_arn_cn, key='key',
        s3_config={'use_arn_region': False},
        expected_url=(
            'https://myendpoint-123456789012.s3-accesspoint.'
            'cn-northwest-1.amazonaws.com.cn/key'
        )
    )
    accesspoint_arn_gov = (
        'arn:aws-us-gov:s3:us-gov-east-1:123456789012:accesspoint:myendpoint'
    )
    yield t.case(
        region='us-gov-east-1', bucket=accesspoint_arn_gov, key='key',
        expected_url=(
            'https://myendpoint-123456789012.s3-accesspoint.'
            'us-gov-east-1.amazonaws.com/key'
        )
    )
    yield t.case(
        region='fips-us-gov-west-1', bucket=accesspoint_arn_gov, key='key',
        expected_url=(
            'https://myendpoint-123456789012.s3-accesspoint.'
            'us-gov-east-1.amazonaws.com/key'
        )
    )
    yield t.case(
        region='fips-us-gov-west-1', bucket=accesspoint_arn_gov, key='key',
        s3_config={'use_arn_region': False},
        expected_url=(
            'https://myendpoint-123456789012.s3-accesspoint.'
            'fips-us-gov-west-1.amazonaws.com/key'
        )
    )

    yield t.case(
        region='us-west-2', bucket=accesspoint_arn, key='key', is_secure=False,
        expected_url=(
            'http://myendpoint-123456789012.s3-accesspoint.'
            'us-west-2.amazonaws.com/key'
        )
    )
    # Dual-stack with access-point arn
    yield t.case(
        # Note: The access-point arn has us-west-2 and the client's region is
        # us-east-1, for the default case the access-point arn region is used.
        region='us-east-1', bucket=accesspoint_arn, key='key',
        s3_config={
            'use_dualstack_endpoint': True,
        },
        expected_url=(
            'https://myendpoint-123456789012.s3-accesspoint.dualstack.'
            'us-west-2.amazonaws.com/key'
        )
    )
    yield t.case(
        region='us-east-1', bucket=accesspoint_arn, key='key',
        s3_config={
            'use_dualstack_endpoint': True,
            'use_arn_region': False
        },
        expected_url=(
            'https://myendpoint-123456789012.s3-accesspoint.dualstack.'
            'us-east-1.amazonaws.com/key'
        )
    )
    yield t.case(
        region='us-gov-east-1', bucket=accesspoint_arn_gov, key='key',
        s3_config={
            'use_dualstack_endpoint': True,
        },
        expected_url=(
            'https://myendpoint-123456789012.s3-accesspoint.dualstack.'
            'us-gov-east-1.amazonaws.com/key'
        )
    )

    # None of the various s3 settings related to paths should affect what
    # endpoint to use when an access-point is provided.
    yield t.case(
        region='us-west-2', bucket=accesspoint_arn, key='key',
        s3_config={'adressing_style': 'auto'},
        expected_url=(
            'https://myendpoint-123456789012.s3-accesspoint.'
            'us-west-2.amazonaws.com/key'
        )
    )
    yield t.case(
        region='us-west-2', bucket=accesspoint_arn, key='key',
        s3_config={'adressing_style': 'virtual'},
        expected_url=(
            'https://myendpoint-123456789012.s3-accesspoint.'
            'us-west-2.amazonaws.com/key'
        )
    )
    yield t.case(
        region='us-west-2', bucket=accesspoint_arn, key='key',
        s3_config={'adressing_style': 'path'},
        expected_url=(
            'https://myendpoint-123456789012.s3-accesspoint.'
            'us-west-2.amazonaws.com/key'
        )
    )

    # Use us-east-1 regional endpoint cases: regional
    us_east_1_regional_endpoint = {
        'us_east_1_regional_endpoint': 'regional'
    }
    yield t.case(
        region='us-east-1', bucket='bucket', key='key',
        s3_config=us_east_1_regional_endpoint,
        expected_url=(
            'https://bucket.s3.us-east-1.amazonaws.com/key'))
    yield t.case(
        region='us-west-2', bucket='bucket', key='key',
        s3_config=us_east_1_regional_endpoint,
        expected_url=(
            'https://bucket.s3.us-west-2.amazonaws.com/key'))
    yield t.case(
        region=None, bucket='bucket', key='key',
        s3_config=us_east_1_regional_endpoint,
        expected_url=(
            'https://bucket.s3.amazonaws.com/key'))
    yield t.case(
        region='unknown', bucket='bucket', key='key',
        s3_config=us_east_1_regional_endpoint,
        expected_url=(
            'https://bucket.s3.unknown.amazonaws.com/key'))
    yield t.case(
        region='us-east-1', bucket='bucket', key='key',
        s3_config={
            'us_east_1_regional_endpoint': 'regional',
            'use_dualstack_endpoint': True,
        },
        expected_url=(
            'https://bucket.s3.dualstack.us-east-1.amazonaws.com/key'))
    yield t.case(
        region='us-east-1', bucket='bucket', key='key',
        s3_config={
            'us_east_1_regional_endpoint': 'regional',
            'use_accelerate_endpoint': True,
        },
        expected_url=(
            'https://bucket.s3-accelerate.amazonaws.com/key'))
    yield t.case(
        region='us-east-1', bucket='bucket', key='key',
        s3_config={
            'us_east_1_regional_endpoint': 'regional',
            'use_accelerate_endpoint': True,
            'use_dualstack_endpoint': True,
        },
        expected_url=(
            'https://bucket.s3-accelerate.dualstack.amazonaws.com/key'))

    # Use us-east-1 regional endpoint cases: legacy
    us_east_1_regional_endpoint_legacy = {
        'us_east_1_regional_endpoint': 'legacy'
    }
    yield t.case(
        region='us-east-1', bucket='bucket', key='key',
        s3_config=us_east_1_regional_endpoint_legacy,
        expected_url=(
            'https://bucket.s3.amazonaws.com/key'))

    yield t.case(
        region=None, bucket='bucket', key='key',
        s3_config=us_east_1_regional_endpoint_legacy,
        expected_url=(
            'https://bucket.s3.amazonaws.com/key'))

    yield t.case(
        region='unknown', bucket='bucket', key='key',
        s3_config=us_east_1_regional_endpoint_legacy,
        expected_url=(
            'https://bucket.s3.unknown.amazonaws.com/key'))


class BaseTestCase:
    def __init__(self, verify_function):
        self._verify = verify_function

    def case(self, **kwargs):
        return self._verify, kwargs


class S3AddressingCases(BaseTestCase):
    def case(self, region=None, bucket='bucket', key='key',
             s3_config=None, is_secure=True, customer_provided_endpoint=None,
             expected_url=None, signature_version=None):
        return (
            self._verify, region, bucket, key, s3_config, is_secure,
            customer_provided_endpoint, expected_url, signature_version
        )


class S3ChecksumCases(BaseTestCase):
    def case(self, operation, operation_args):
        return self._verify, operation, operation_args


def _verify_expected_endpoint_url(region, bucket, key, s3_config,
                                  is_secure=True,
                                  customer_provided_endpoint=None,
                                  expected_url=None, signature_version=None):
    environ = {}
    with mock.patch('os.environ', environ):
        environ['AWS_ACCESS_KEY_ID'] = 'access_key'
        environ['AWS_SECRET_ACCESS_KEY'] = 'secret_key'
        environ['AWS_CONFIG_FILE'] = 'no-exist-foo'
        environ['AWS_SHARED_CREDENTIALS_FILE'] = 'no-exist-foo'
        session = create_session()
        session.config_filename = 'no-exist-foo'
        config = Config(
            signature_version=signature_version,
            s3=s3_config
        )
        s3 = session.create_client('s3', region_name=region, use_ssl=is_secure,
                                   config=config,
                                   endpoint_url=customer_provided_endpoint)
        with ClientHTTPStubber(s3) as http_stubber:
            http_stubber.add_response()
            s3.put_object(Bucket=bucket, Key=key, Body=b'bar')
            assert_equal(http_stubber.requests[0].url, expected_url)


def _create_s3_client(region, is_secure, endpoint_url, s3_config,
                      signature_version):
    environ = {}
    with mock.patch('os.environ', environ):
        environ['AWS_ACCESS_KEY_ID'] = 'access_key'
        environ['AWS_SECRET_ACCESS_KEY'] = 'secret_key'
        environ['AWS_CONFIG_FILE'] = 'no-exist-foo'
        environ['AWS_SHARED_CREDENTIALS_FILE'] = 'no-exist-foo'
        session = create_session()
        session.config_filename = 'no-exist-foo'
        config = Config(
            signature_version=signature_version,
            s3=s3_config
        )
        s3 = session.create_client('s3', region_name=region, use_ssl=is_secure,
                                   config=config,
                                   endpoint_url=endpoint_url)
        return s3


def test_addressing_for_presigned_urls():
    # See TestGeneratePresigned for more detailed test cases
    # on presigned URLs.  Here's we're just focusing on the
    # adddressing mode used for presigned URLs.
    # We special case presigned URLs due to backwards
    # compatibility.
    t = S3AddressingCases(_verify_presigned_url_addressing)

    # us-east-1, or the "global" endpoint. A signature version of
    # None means the user doesn't have signature version configured.
    yield t.case(region='us-east-1', bucket='bucket', key='key',
                 signature_version=None,
                 expected_url='https://bucket.s3.amazonaws.com/key')
    yield t.case(region='us-east-1', bucket='bucket', key='key',
                 signature_version='s3',
                 expected_url='https://bucket.s3.amazonaws.com/key')
    yield t.case(region='us-east-1', bucket='bucket', key='key',
                 signature_version='s3v4',
                 expected_url='https://bucket.s3.amazonaws.com/key')
    yield t.case(region='us-east-1', bucket='bucket', key='key',
                 signature_version='s3v4',
                 s3_config={'addressing_style': 'path'},
                 expected_url='https://s3.amazonaws.com/bucket/key')

    # A region that supports both 's3' and 's3v4'.
    yield t.case(region='us-west-2', bucket='bucket', key='key',
                 signature_version=None,
                 expected_url='https://bucket.s3.amazonaws.com/key')
    yield t.case(region='us-west-2', bucket='bucket', key='key',
                 signature_version='s3',
                 expected_url='https://bucket.s3.amazonaws.com/key')
    yield t.case(region='us-west-2', bucket='bucket', key='key',
                 signature_version='s3v4',
                 expected_url='https://bucket.s3.amazonaws.com/key')
    yield t.case(region='us-west-2', bucket='bucket', key='key',
                 signature_version='s3v4',
                 s3_config={'addressing_style': 'path'},
                 expected_url='https://s3.us-west-2.amazonaws.com/bucket/key')

    # An 's3v4' only region.
    yield t.case(region='us-east-2', bucket='bucket', key='key',
                 signature_version=None,
                 expected_url='https://bucket.s3.amazonaws.com/key')
    yield t.case(region='us-east-2', bucket='bucket', key='key',
                 signature_version='s3',
                 expected_url='https://bucket.s3.amazonaws.com/key')
    yield t.case(region='us-east-2', bucket='bucket', key='key',
                 signature_version='s3v4',
                 expected_url='https://bucket.s3.amazonaws.com/key')
    yield t.case(region='us-east-2', bucket='bucket', key='key',
                 signature_version='s3v4',
                 s3_config={'addressing_style': 'path'},
                 expected_url='https://s3.us-east-2.amazonaws.com/bucket/key')

    # Dualstack endpoints
    yield t.case(
        region='us-west-2', bucket='bucket', key='key',
        signature_version=None,
        s3_config={'use_dualstack_endpoint': True},
        expected_url='https://bucket.s3.dualstack.us-west-2.amazonaws.com/key')
    yield t.case(
        region='us-west-2', bucket='bucket', key='key',
        signature_version='s3',
        s3_config={'use_dualstack_endpoint': True},
        expected_url='https://bucket.s3.dualstack.us-west-2.amazonaws.com/key')
    yield t.case(
        region='us-west-2', bucket='bucket', key='key',
        signature_version='s3v4',
        s3_config={'use_dualstack_endpoint': True},
        expected_url='https://bucket.s3.dualstack.us-west-2.amazonaws.com/key')

    # Accelerate
    yield t.case(region='us-west-2', bucket='bucket', key='key',
                 signature_version=None,
                 s3_config={'use_accelerate_endpoint': True},
                 expected_url='https://bucket.s3-accelerate.amazonaws.com/key')

    # A region that we don't know about.
    yield t.case(region='us-west-50', bucket='bucket', key='key',
                 signature_version=None,
                 expected_url='https://bucket.s3.amazonaws.com/key')

    # Customer provided URL results in us leaving the host untouched.
    yield t.case(region='us-west-2', bucket='bucket', key='key',
                 signature_version=None,
                 customer_provided_endpoint='https://foo.com/',
                 expected_url='https://foo.com/bucket/key')

    # Access-point
    accesspoint_arn = (
        'arn:aws:s3:us-west-2:123456789012:accesspoint:myendpoint'
    )
    yield t.case(
        region='us-west-2', bucket=accesspoint_arn, key='key',
        expected_url=(
            'https://myendpoint-123456789012.s3-accesspoint.'
            'us-west-2.amazonaws.com/key'
        )
    )
    yield t.case(
        region='us-east-1', bucket=accesspoint_arn, key='key',
        s3_config={'use_arn_region': False},
        expected_url=(
            'https://myendpoint-123456789012.s3-accesspoint.'
            'us-east-1.amazonaws.com/key'
        )
    )

    # Use us-east-1 regional endpoint configuration cases
    us_east_1_regional_endpoint = {
        'us_east_1_regional_endpoint': 'regional'
    }
    yield t.case(
        region='us-east-1', bucket='bucket', key='key',
        s3_config=us_east_1_regional_endpoint, signature_version='s3',
        expected_url=(
            'https://bucket.s3.us-east-1.amazonaws.com/key'))
    yield t.case(
        region='us-east-1', bucket='bucket', key='key',
        s3_config=us_east_1_regional_endpoint, signature_version='s3v4',
        expected_url=(
            'https://bucket.s3.us-east-1.amazonaws.com/key'))


def _verify_presigned_url_addressing(region, bucket, key, s3_config,
                                     is_secure=True,
                                     customer_provided_endpoint=None,
                                     expected_url=None,
                                     signature_version=None):
    s3 = _create_s3_client(region=region, is_secure=is_secure,
                           endpoint_url=customer_provided_endpoint,
                           s3_config=s3_config,
                           signature_version=signature_version)
    url = s3.generate_presigned_url(
        'get_object', {'Bucket': bucket, 'Key': key})
    # We're not trying to verify the params for URL presigning,
    # those are tested elsewhere.  We just care about the hostname/path.
    parts = urlsplit(url)
    actual = '%s://%s%s' % parts[:3]
    assert_equal(actual, expected_url)
