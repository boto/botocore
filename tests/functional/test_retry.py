# Copyright 2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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
from tests import BaseSessionTest, mock

from botocore.exceptions import ClientError
from botocore.config import Config


class TestRetry(BaseSessionTest):
    def setUp(self):
        super(TestRetry, self).setUp()
        self.region = 'us-west-2'

    def add_n_retryable_responses(self, mock_send, num_responses):
        responses = []
        for _ in range(num_responses):
            http_response = mock.Mock()
            http_response.status_code = 500
            http_response.headers = {}
            http_response.content = b'{}'
            responses.append(http_response)
        mock_send.side_effect = responses

    def test_can_override_max_attempts(self):
        client = self.session.create_client(
            'dynamodb', self.region, config=Config(
                retries={'max_attempts': 1}))
        with mock.patch('botocore.endpoint.Session.send') as mock_send:
            self.add_n_retryable_responses(mock_send, 2)
            with self.assertRaisesRegexp(
                    ClientError, 'reached max retries: 1'):
                client.list_tables()
            self.assertEqual(mock_send.call_count, 2)

    def test_do_not_attempt_retries(self):
        client = self.session.create_client(
            'dynamodb', self.region, config=Config(
                retries={'max_attempts': 0}))
        with mock.patch('botocore.endpoint.Session.send') as mock_send:
            self.add_n_retryable_responses(mock_send, 1)
            with self.assertRaisesRegexp(
                    ClientError, 'reached max retries: 0'):
                client.list_tables()
            self.assertEqual(mock_send.call_count, 1)
