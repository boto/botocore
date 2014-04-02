#!/usr/bin/env python
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

from tests import BaseSessionTest
import botocore.session


class TestCloudTrailOperations(BaseSessionTest):

    def setUp(self):
        super(TestCloudTrailOperations, self).setUp()
        self.cloudtrail = self.session.get_service('cloudtrail')

    def test_cloudtrail_create_subscription(self):
        op = self.cloudtrail.get_operation('CreateTrail')
        kwargs = {
            "name": "name",
            "s3_bucket_name": "s3bucketname",
            "s3_key_prefix": "s3keyprefix",
            "sns_topic_name": "snstopicname",
            "include_global_service_events": True
        }
        params = op.build_parameters(**kwargs)
        result = {
            'Name': 'name',
            'S3BucketName': 's3bucketname',
            'S3KeyPrefix': 's3keyprefix',
            'SnsTopicName': 'snstopicname',
            'IncludeGlobalServiceEvents': True,
        }
        self.assertEqual(params, result)
