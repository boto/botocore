# Copyright 2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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
from botocore.stub import Stubber, ANY
import botocore.session


class TestIdempotencyToken(unittest.TestCase):
    def setUp(self):
        self.function_name = 'purchase_scheduled_instances'
        self.region = 'us-west-2'
        self.session = botocore.session.get_session()
        self.client = self.session.create_client(
            'ec2', self.region)
        self.stubber = Stubber(self.client)
        self.service_response = {}
        self.params_seen = []

        # Record all the parameters that get seen
        self.client.meta.events.register_first(
            'before-call.*.*',
            self.collect_params,
            unique_id='TestIdempotencyToken')

    def collect_params(self, model, params, *args, **kwargs):
        self.params_seen.extend(params['body'].keys())

    def test_provided_idempotency_token(self):
        expected_params = {
            'PurchaseRequests': [
                {'PurchaseToken': 'foo',
                 'InstanceCount': 123}],
            'ClientToken': ANY
        }
        self.stubber.add_response(
            self.function_name, self.service_response, expected_params)

        with self.stubber:
            self.client.purchase_scheduled_instances(
                PurchaseRequests=[{'PurchaseToken': 'foo',
                                   'InstanceCount': 123}],
                ClientToken='foobar')
            self.assertIn('ClientToken', self.params_seen)

    def test_insert_idempotency_token(self):
        expected_params = {
            'PurchaseRequests': [
                {'PurchaseToken': 'foo',
                 'InstanceCount': 123}],
        }

        self.stubber.add_response(
            self.function_name, self.service_response, expected_params)

        with self.stubber:
            self.client.purchase_scheduled_instances(
                PurchaseRequests=[{'PurchaseToken': 'foo',
                                   'InstanceCount': 123}])
            self.assertIn('ClientToken', self.params_seen)
