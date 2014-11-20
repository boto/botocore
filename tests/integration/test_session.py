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
from tests import unittest

import botocore.session


class TestCanChangeParsing(unittest.TestCase):
    def setUp(self):
        self.session = botocore.session.get_session()

    def test_can_change_timestamp_parsing(self):
        # This is an example of what a library such as the AWS CLI
        # could do to alter the parsing behavior of botocore.
        factory = self.session.get_component('response_parser_factory')
        # We'll be explicit here and type convert to a str().
        factory.set_parser_defaults(timestamp_parser=lambda x: str(x))

        # Now if we get a response with timestamps in the model, they
        # will be returned as strings. We're testing service/operation
        # objects, but we should also add a test for clients.
        s3 = self.session.get_service('s3')
        endpoint = s3.get_endpoint('us-west-2')
        http, parsed = s3.get_operation('ListBuckets').call(endpoint)
        dates = [bucket['CreationDate'] for bucket in parsed['Buckets']]
        self.assertTrue(all(isinstance(date, str) for date in dates))
