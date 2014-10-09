# Copyright 2014 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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
import time
import random
from tests import unittest

import botocore.session
from botocore.client import ClientError


class TestBucketWithVersions(unittest.TestCase):
    def setUp(self):
        self.session = botocore.session.get_session()
        self.client = self.session.create_client('s3', region_name='us-west-2')
        self.bucket_name = 'botocoretest%s-%s' % (
            int(time.time()), random.randint(1, 1000000))

    def extract_version_ids(self, versions):
        version_ids = []
        for marker in versions['DeleteMarkers']:
            version_ids.append(marker['VersionId'])
        for version in versions['Versions']:
            version_ids.append(version['VersionId'])
        return version_ids

    def test_create_versioned_bucket(self):
        # Verifies we can:
        # 1. Create a bucket
        # 2. Enable versioning
        # 3. Put an Object
        # 4. Delete the object
        # 5. Delete all the versions
        # 6. Delete the bucket
        self.client.create_bucket(Bucket=self.bucket_name)
        self.client.put_bucket_versioning(
            Bucket=self.bucket_name,
            VersioningConfiguration={"Status": "Enabled"})
        self.client.put_object(Bucket=self.bucket_name,
                               Key='testkey',
                               Body=b'bytes body')
        response = self.client.get_object(
            Bucket=self.bucket_name, Key='testkey')
        self.assertEqual(response['Body'].read(), b'bytes body')
        self.client.delete_object(Bucket=self.bucket_name, Key='testkey')
        # Object does not exist anymore.
        with self.assertRaises(ClientError):
            self.client.get_object(Bucket=self.bucket_name, Key='testkey')
        versions = self.client.list_object_versions(Bucket=self.bucket_name)
        version_ids = self.extract_version_ids(versions)
        self.assertEqual(len(version_ids), 2)
        for version_id in version_ids:
            self.client.delete_object(
                Bucket=self.bucket_name,
                Key='testkey',
                VersionId=version_id)
        self.client.delete_bucket(Bucket=self.bucket_name)
        # The bucket should no longer exist:
        with self.assertRaises(ClientError):
            self.client.head_bucket(Bucket=self.bucket_name)
