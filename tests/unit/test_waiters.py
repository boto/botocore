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
from tests import BaseSessionTest, unittest
from botocore import endpoint
from botocore.exceptions import WaiterError
from botocore.waiter import Waiter

import mock


class TestLegacyWaiters(BaseSessionTest):

    def setUp(self):
        super(TestLegacyWaiters, self).setUp()
        self.fake_responses = []
        self.sleep_patch = mock.patch('time.sleep')
        self.sleep_patch.start()

    def tearDown(self):
        super(TestLegacyWaiters, self).tearDown()
        self.sleep_patch.stop()

    def create_endpoint_with_fake_responses(self, responses):
        m = mock.Mock(spec=endpoint.Endpoint)
        fake_responses = []
        for status_code, parsed in responses:
            fake_http_response = mock.Mock()
            fake_http_response.status_code = status_code
            fake_responses.append((fake_http_response, parsed))
        m.make_request.side_effect = \
                lambda operation, params: fake_responses.pop(0)
        return m

    def test_create_waiter_multiple_times(self):
        service = self.session.get_service('ec2')
        instance_running = service.get_waiter('InstanceRunning', mock.Mock())
        instance_running2 = service.get_waiter('InstanceRunning', mock.Mock())
        self.assertEqual(instance_running.name, instance_running2.name)

    def test_wait_success_case(self):
        service = self.session.get_service('ec2')
        endpoint = self.create_endpoint_with_fake_responses([
            (200, {'Reservations': [
                {'Instances': [{'State': {'Name': 'starting'}}]}]}),
            (200, {'Reservations': [
                {'Instances': [{'State': {'Name': 'running'}}]}]}),
        ])
        instance_running = service.get_waiter('InstanceRunning', endpoint)
        instance_running.wait(InstanceIds=['i-1234'])
        # endpoint.make_request should be called twice, once for starting
        # once for running.
        self.assertEqual(endpoint.make_request.call_count, 2)

    def test_no_acceptor_state_reached(self):
        service = self.session.get_service('ec2')
        single_response = (
            200, {'Reservations': [
                {'Instances': [{'State': {'Name': 'starting'}}]}]})
        # The instance is always in a starting state.
        # This should cause the waiter to fail.
        endpoint = self.create_endpoint_with_fake_responses(
            [single_response] * 100)
        instance_running = service.get_waiter('InstanceRunning', endpoint)
        with self.assertRaises(WaiterError):
            instance_running.wait(InstanceIds=['i-1234'])

    def test_fast_fail_acceptor_matched(self):
        service = self.session.get_service('ec2')
        endpoint = self.create_endpoint_with_fake_responses([
            (200, {'Reservations': [
                {'Instances': [{'State': {'Name': 'starting'}}]}]}),
            # If the state hits 'terminating' then we just fail fast.
            (200, {'Reservations': [
                {'Instances': [{'State': {'Name': 'terminated'}}]}]}),
        ])
        instance_running = service.get_waiter('InstanceRunning', endpoint)
        with self.assertRaises(WaiterError):
            instance_running.wait(InstanceIds=['i-1234'])

    def test_acceptor_with_error_type(self):
        # For reference, we're testing this:
        #
        # "TableNotExists": {
        #   "extends": "__TableState",
        #   "success_type": "error",
        #   "success_value": "ResourceNotFoundException"
        # }
        service = self.session.get_service('dynamodb')
        endpoint = self.create_endpoint_with_fake_responses([
            (200, {'Table': {'TableStatus': 'DELETING'}}),
            (400, {'Error': {'Code': 'ResourceNotFoundException'}}),
            # This is just to test that we never actually make a third
            # call, we should stop once we hit the 400 response above.
            (200, {'Table': {'TableStatus': 'DELETING'}}),
        ])
        table_not_exists = service.get_waiter('TableNotExists', endpoint)
        table_not_exists.wait(TableName='mytable')
        # Called twice, once for DELETING, once for ResourceNotFoundException.
        self.assertEqual(endpoint.make_request.call_count, 2)

    def test_acceptor_with_bad_jmespath(self):
        service = self.session.get_service('ec2')
        # The jmespath expression is Reservations[].Instances[].State.Name
        # We're going to change the response so that the jmespath
        # expression will never match, and return a None value.
        single_response = (
            200, {'NOTRESERVATIONS': [
                {'NOTINSTANCES': [{'State': {'Name': 'starting'}}]}]})
        endpoint = self.create_endpoint_with_fake_responses(
            [single_response] * 100)
        instance_running = service.get_waiter('InstanceRunning', endpoint)
        # We should fail because we never match the output.
        with self.assertRaises(WaiterError):
            instance_running.wait(InstanceIds=['i-1234'])


class TestWaiters(unittest.TestCase):
    def test_waiter_exists(self):
        waiter_config = {
            "success": {
                "path": "Table.TableStatus",
                "type": "output",
                "value": [
                    "ACTIVE"
                ]
            },
            # Setting an interval of 0 so we don't have to
            # mock out time.sleep() calls.
            "interval": 0,
            "ignore_errors": [
                "ResourceNotFoundException"
            ],
            "operation": "DescribeTable",
            "max_attempts": 25
        }
        describe_table = mock.Mock()
        describe_table.side_effect = [
            {'Table': {'TableStatus': 'CREATING'}},
            {'Table': {'TableStatus': 'ACTIVE'}},
        ]
        w = Waiter('TableExists', describe_table, waiter_config)
        w.wait(TableName='mytable')
        self.assertEqual(describe_table.call_count, 2)
