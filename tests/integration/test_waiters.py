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
from tests import unittest, random_chars

from nose.plugins.attrib import attr

import botocore.session
from botocore.exceptions import WaiterError
import json

# This is the same test as above, except using the client interface.


@attr('slow')
class TestWaiterForDynamoDB(unittest.TestCase):
    def setUp(self):
        self.session = botocore.session.get_session()
        self.client = self.session.create_client('dynamodb', 'us-west-2')

    def test_create_table_and_wait(self):
        table_name = 'botocoretest-%s' % random_chars(10)
        self.client.create_table(
            TableName=table_name,
            ProvisionedThroughput={"ReadCapacityUnits": 5,
                                   "WriteCapacityUnits": 5},
            KeySchema=[{"AttributeName": "foo", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "foo",
                                   "AttributeType": "S"}])
        self.addCleanup(self.client.delete_table, TableName=table_name)
        waiter = self.client.get_waiter('table_exists')
        waiter.wait(TableName=table_name)
        parsed = self.client.describe_table(TableName=table_name)
        self.assertEqual(parsed['Table']['TableStatus'], 'ACTIVE')


@attr('slow')
class TestWaiterForStepfunctions(unittest.TestCase):
    def setUp(self):
        self.session = botocore.session.get_session()
        self.client = self.session.create_client('stepfunctions', 'us-west-2')

        self.sts_client = self.session.create_client('sts')
        self.iam_client = self.session.create_client('iam')
        account_id = self.sts_client.get_caller_identity()['Account']
        self.role_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {
                        "AWS": "arn:aws:iam::%s:root" % account_id
                    },
                    "Action": "sts:AssumeRole"
                }
            ]
         }


    def test_waiter_execution_succeeded(self):

        role = self.iam_client.create_role(RoleName = 'test-role-stepfunction-1',AssumeRolePolicyDocument = json.dumps(self.role_policy))
        definition = {
            "Comment": "Test Step Function",
            "StartAt": "Hello",
            "States": {
                "Hello": {
                    "Type": "Pass",
                    "Result": "Hello",
                    "Next": "World"
                },
                "World": {
                    "Type": "Pass",
                    "Result": "World",
                    "Next": "Wait"
                },
                "Wait": {
                    "Comment": "A Wait state delays the state machine from continuing for a specified time.",
                    "Type": "Wait",
                    "Seconds": 3,
                    "End": True
                }
            }
        }

        stepfunction_response = self.client.create_state_machine(
            name='botocoretest-statemachine',
            definition=json.dumps(definition),
            roleArn=role['Role']['Arn']
        )

        stateMachineArn = stepfunction_response['stateMachineArn']

        stepfunction_execute_response = self.client.start_execution(
            stateMachineArn=stateMachineArn, input=json.dumps('{"Comments":"Hello World"}'))
        executionArn = stepfunction_execute_response['executionArn']

        waiter = self.client.get_waiter('execution_complete')
        waiter.wait(executionArn=executionArn)

        response = self.client.describe_execution(executionArn=executionArn)
        # Cleanup
        self.iam_client.delete_role(RoleName=role['Role']['RoleName'])
        self.assertEqual(response['status'], 'SUCCEEDED')
        self.client.delete_state_machine(stateMachineArn=stateMachineArn)
        

    def test_waiter_execution_failed(self):

        role = self.iam_client.create_role(RoleName = 'test-role-stepfunction-2',AssumeRolePolicyDocument = json.dumps(self.role_policy))
        # A Step Machine with a fail state
        definition = {
            "Comment": "Test Step Function",
            "StartAt": "Hello",
            "States": {
                "Hello": {
                    "Type": "Pass",
                    "Result": "Hello",
                    "Next": "World"
                },
                "World": {
                    "Type": "Pass",
                    "Result": "World",
                    "Next": "Wait"
                },
                "Wait": {
                    "Comment": "A Wait state delays the state machine from continuing for a specified time.",
                    "Type": "Fail",
                }
            }
        }
        stepfunction_response = self.client.create_state_machine(
            name='botocoretest-statemachine-fail',
            definition=json.dumps(definition),
            roleArn=role['Role']['Arn']
        )
        stateMachineArn = stepfunction_response['stateMachineArn']

        stepfunction_execute_response = self.client.start_execution(
            stateMachineArn=stateMachineArn, input=json.dumps('{"Comments":"Hello World"}'))
        executionArn = stepfunction_execute_response['executionArn']
        waiter = self.client.get_waiter('execution_complete')
        with self.assertRaises(WaiterError):
            waiter.wait(executionArn=executionArn)

        response = self.client.describe_execution(executionArn=executionArn)
        # Cleanup
        self.iam_client.delete_role(RoleName=role['Role']['RoleName'])
        self.assertEqual(response['status'], 'FAILED')
        self.client.delete_state_machine(stateMachineArn=stateMachineArn)
        

    def test_waiter_execution_aborted(self):

        role = self.iam_client.create_role(RoleName = 'test-role-stepfunction-3',AssumeRolePolicyDocument = json.dumps(self.role_policy))
        definition = {
            "Comment": "Test Step Function",
            "StartAt": "Hello",
            "States": {
                "Hello": {
                    "Type": "Pass",
                    "Result": "Hello",
                    "Next": "World"
                },
                "World": {
                    "Type": "Pass",
                    "Result": "World",
                    "Next": "Wait"
                },
                "Wait": {
                    "Comment": "A Wait state delays the state machine from continuing for a specified time.",
                    "Type": "Wait",
                    "Seconds": 3,
                    "End": True
                }
            }
        }

        stepfunction_response = self.client.create_state_machine(
            name='botocoretest-statemachine-abort',
            definition=json.dumps(definition),
            roleArn=role['Role']['Arn']
        )

        stateMachineArn = stepfunction_response['stateMachineArn']

        stepfunction_execute_response = self.client.start_execution(
            stateMachineArn=stateMachineArn, input=json.dumps('{"Comments":"Hello World"}'))
        executionArn = stepfunction_execute_response['executionArn']

        # Aborting the state machine
        self.client.stop_execution(executionArn=executionArn)

        waiter = self.client.get_waiter('execution_complete')
        with self.assertRaises(WaiterError):
            waiter.wait(executionArn=executionArn)

        response = self.client.describe_execution(executionArn=executionArn)
        # Cleanup
        self.iam_client.delete_role(RoleName=role['Role']['RoleName'])
        self.assertEqual(response['status'], 'ABORTED')
        self.client.delete_state_machine(stateMachineArn=stateMachineArn)
        


class TestCanGetWaitersThroughClientInterface(unittest.TestCase):
    def test_get_ses_waiter(self):
        # We're checking this because ses is not the endpoint prefix
        # for the service, it's email.  We want to make sure this does
        # not affect the lookup process.
        session = botocore.session.get_session()
        client = session.create_client('ses', 'us-east-1')
        # If we have at least one waiter in the list, we know that we have
        # actually loaded the waiters and this test has passed.
        self.assertTrue(len(client.waiter_names) > 0)


class TestMatchersWithErrors(unittest.TestCase):
    def setUp(self):
        self.session = botocore.session.get_session()
        self.client = self.session.create_client(
            'ec2', region_name='us-west-2')

    def test_dont_search_on_error_responses(self):
        """Test that InstanceExists can handle a nonexistent instance."""
        waiter = self.client.get_waiter('instance_exists')
        waiter.config.max_attempts = 1
        with self.assertRaises(WaiterError):
            waiter.wait(InstanceIds=['i-12345'])
