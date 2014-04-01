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

import unittest
import itertools

import botocore.session


class TestRDSPagination(unittest.TestCase):
    def setUp(self):
        self.session = botocore.session.get_session()
        self.service = self.session.get_service('route53')
        self.endpoint = self.service.get_endpoint('us-west-2')

    def test_paginate_with_max_items(self):
        # Route53 has a string type for MaxItems.  We need to ensure that this
        # still works without any issues.
        operation = self.service.get_operation('ListHostedZones')
        results = list(operation.paginate(self.endpoint, max_items='1'))
        self.assertTrue(len(results) >= 0)


if __name__ == '__main__':
    unittest.main()
