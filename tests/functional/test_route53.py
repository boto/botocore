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
from botocore.stub import Stubber

class TestRoute53Pagination(unittest.TestCase):
    def setUp(self):
        self.session = botocore.session.get_session()
        self.client = self.session.create_client('route53', 'us-west-2')
        self.stubber = Stubber(self.client)
        # response has required fields
        self.response = {
            'HostedZones': [],
            'Marker': '',
            'IsTruncated': True,
            'MaxItems': '1'
        }
        self.operation_name = 'list_hosted_zones'

    def test_paginate_with_max_items_int(self):
        # Route53 has a string type for MaxItems.  We need to ensure that this
        # still works with integers as the cli auto converts the page size
        # argument to an integer.
        self.stubber.add_response(self.operation_name, self.response)
        paginator = self.client.get_paginator('list_hosted_zones')
        with self.stubber:
            config={'PageSize': 1}
            results = list(paginator.paginate(PaginationConfig=config))
            self.assertTrue(len(results) >= 0)

    def test_paginate_with_max_items_str(self):
        # Route53 has a string type for MaxItems.  We need to ensure that this
        # still works with strings as that's the expected type for this key.
        self.stubber.add_response(self.operation_name, self.response)
        paginator = self.client.get_paginator('list_hosted_zones')
        with self.stubber:
            config={'PageSize': '1'}
            results = list(paginator.paginate(PaginationConfig=config))
            self.assertTrue(len(results) >= 0)
