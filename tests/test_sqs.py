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
import botocore.session
from tests import unittest


class TestSqs(unittest.TestCase):
    # As SQS has migrated from AwsQuery to AwsJson,
    # SQS has to assure 100% backwards compatibility.

    QUEUE_NAME = 'botocore-integ-test-queue'

    def setUp(self):
        self.session = botocore.session.get_session()
        self.client = self.session.create_client('sqs', 'us-west-2')
        # There's no error if the queue already exists so we don't
        # need to catch any exceptions here.
        self.client.create_queue(QueueName=self.QUEUE_NAME)

    def test_can_throw_exception_with_correct_error_type(self):
        try:
            self.client.delete_queue(QueueUrl='foo-nonexistant-queue')
        except Exception as e:
            assert issubclass(
                type(e), self.client.exceptions.QueueDoesNotExist
            ), (
                f"Expected an exception of type "
                f"exception.QueueDoesNotExist, "
                f"but got {type(e)}"
            )
            assert (
                e.response['Error']['Code']
                == 'AWS.SimpleQueueService.NonExistentQueue'
            )
            assert e.response['ResponseMetadata']['HTTPStatusCode'] == 400
            assert (
                e.response['Error']['Message']
                == 'The specified queue does not exist.'
            )


if __name__ == '__main__':
    unittest.main()
