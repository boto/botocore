# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
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

import datetime
from unittest.mock import patch

import pytest
from dateutil.tz import tzlocal

from tests import ClientHTTPStubber


class TestDisableS3ExpressAuth:
    BUCKET_NAME = 'mybucket--usw2-az1--x-s3'
    CREATE_SESSION_BODY = b'<?xml version="1.0" encoding="UTF-8"?>\n<CreateSessionResult><Credentials><AccessKeyId>test-key</AccessKeyId><Expiration>2024-12-31T23:59:59Z</Expiration><SecretAccessKey>test-secret</SecretAccessKey><SessionToken>test-token</SessionToken></Credentials></CreateSessionResult>'
    LIST_OBJECTS_BODY = b'<?xml version="1.0" encoding="UTF-8"?>\n<ListBucketResult xmlns="http://s3.amazonaws.com/doc/2006-03-01/"><Name>mybucket--usw2-az1--x-s3</Name><Prefix/><KeyCount>0</KeyCount><MaxKeys>1000</MaxKeys><EncodingType>url</EncodingType><IsTruncated>false</IsTruncated></ListBucketResult>'

    @pytest.fixture
    def fixed_datetime(self):
        return datetime.datetime(2024, 11, 30, 23, 59, 59, tzinfo=tzlocal())

    def test_s3_express_auth_disabled(
        self, patched_session, monkeypatch, fixed_datetime
    ):
        auth_type = None

        def get_auth_type(
            signing_name, region_name, signature_version, context, **kwargs
        ):
            nonlocal auth_type
            auth_type = context.get('auth_type', None)

        patched_session.register(
            'choose-signer.s3.ListObjectsV2', get_auth_type
        )
        monkeypatch.setenv('AWS_S3_DISABLE_EXPRESS_SESSION_AUTH', 'true')

        with patch('botocore.credentials.datetime') as mocked_datetime:
            mocked_datetime.datetime.now.return_value = fixed_datetime
            s3_client = patched_session.create_client(
                's3', region_name='us-west-2'
            )

            with ClientHTTPStubber(s3_client, strict=True) as http_stubber:
                http_stubber.add_response(
                    status=200, body=self.LIST_OBJECTS_BODY
                )
                s3_client.list_objects_v2(Bucket=self.BUCKET_NAME)

                assert len(http_stubber.requests) == 1

        is_s3_express = auth_type == 'v4-s3express'
        assert not is_s3_express

    def test_s3_express_auth_enabled(
        self, patched_session, monkeypatch, fixed_datetime
    ):
        auth_type = None

        def get_auth_type(
            signing_name, region_name, signature_version, context, **kwargs
        ):
            nonlocal auth_type
            auth_type = context.get('auth_type', None)

        patched_session.register(
            'choose-signer.s3.ListObjectsV2', get_auth_type
        )
        monkeypatch.setenv('AWS_S3_DISABLE_EXPRESS_SESSION_AUTH', 'false')

        with patch('botocore.credentials.datetime') as mocked_datetime:
            mocked_datetime.datetime.now.return_value = fixed_datetime
            s3_client = patched_session.create_client(
                's3', region_name='us-west-2'
            )

            with ClientHTTPStubber(s3_client, strict=True) as http_stubber:
                http_stubber.add_response(
                    status=200, body=self.CREATE_SESSION_BODY
                )
                http_stubber.add_response(
                    status=200, body=self.LIST_OBJECTS_BODY
                )
                s3_client.list_objects_v2(Bucket=self.BUCKET_NAME)

                assert len(http_stubber.requests) == 2

        is_s3_express = auth_type == 'v4-s3express'
        assert is_s3_express
