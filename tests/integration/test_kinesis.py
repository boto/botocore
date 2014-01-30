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

from tests import unittest
import itertools

import botocore.session


class TestKinesis(unittest.TestCase):
    def setUp(self):
        self.session = botocore.session.get_session()
        self.service = self.session.get_service('kinesis')
        self.endpoint = self.service.get_endpoint('us-east-1')

    def test_list_streams(self):
        operation = self.service.get_operation('ListStreams')
        http, parsed = operation.call(self.endpoint)
        self.assertEqual(http.status_code, 200)
        self.assertIn('StreamNames', parsed)


if __name__ == '__main__':
    unittest.main()
