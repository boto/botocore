# Copyright 2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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
from datetime import datetime

import mock

from tests import BaseSessionTest
from tests import assert_url_equal
from botocore.stub import Stubber


class TestSTSPresignedUrl(BaseSessionTest):
    def setUp(self):
        super(TestSTSPresignedUrl, self).setUp()
        self.client = self.session.create_client('sts', 'us-west-2')
        # Makes sure that no requests will go through
        self.stubber = Stubber(self.client)
        self.stubber.activate()

    def test_presigned_url_contains_no_content_type(self):
        timestamp = datetime(2017, 3, 22, 0, 0)
        with mock.patch('botocore.auth.datetime') as _datetime:
            _datetime.datetime.utcnow.return_value = timestamp
            url = self.client.generate_presigned_url('get_caller_identity', {})

        # There should be no 'content-type' in x-amz-signedheaders
        expected_url = (
            'https://sts.amazonaws.com/?Action=GetCallerIdentity&'
            'Version=2011-06-15&X-Amz-Algorithm=AWS4-HMAC-SHA256&'
            'X-Amz-Credential=access_key%2F20170322%2Fus-east-1%2Fsts%2F'
            'aws4_request&X-Amz-Date=20170322T000000Z&X-Amz-Expires=3600&'
            'X-Amz-SignedHeaders=host&X-Amz-Signature=767845d2ee858069a598d5f'
            '8b497b75c7d57356885b1b3dba46dbbc0fc62bf5a'
        )
        assert_url_equal(url, expected_url)
