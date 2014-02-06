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

import unittest
import itertools

import botocore.session


class TestEC2(unittest.TestCase):
    def setUp(self):
        self.session = botocore.session.get_session()

    def test_can_make_request(self):
        # Basic smoke test to ensure we can talk to ec2.
        service = self.session.get_service('ec2')
        endpoint = service.get_endpoint('us-west-2')
        operation = service.get_operation('DescribeAvailabilityZones')
        http, result = operation.call(endpoint)
        zones = list(sorted(a['ZoneName'] for a in result['AvailabilityZones']))
        self.assertEqual(zones, ['us-west-2a', 'us-west-2b', 'us-west-2c'])


class TestEC2Pagination(unittest.TestCase):
    def setUp(self):
        self.session = botocore.session.get_session()
        self.service = self.session.get_service('ec2')
        self.endpoint = self.service.get_endpoint('us-west-2')

    def test_can_paginate(self):
        # Using an operation that we know will paginate.
        operation = self.service.get_operation('DescribeReservedInstancesOfferings')
        generator = operation.paginate(self.endpoint)
        results = list(itertools.islice(generator, 0, 3))
        self.assertEqual(len(results), 3)
        self.assertTrue(results[0][1]['NextToken'] != results[1][1]['NextToken'])


if __name__ == '__main__':
    unittest.main()
