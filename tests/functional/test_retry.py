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
import contextlib
import json
from tests import BaseSessionTest, mock, ClientHTTPStubber

from botocore.exceptions import ClientError
from botocore.config import Config


class BaseRetryTest(BaseSessionTest):
    def setUp(self):
        super(BaseRetryTest, self).setUp()
        self.region = 'us-west-2'
        self.sleep_patch = mock.patch('time.sleep')
        self.sleep_patch.start()

    def tearDown(self):
        super(BaseRetryTest, self).tearDown()
        self.sleep_patch.stop()

    @contextlib.contextmanager
    def assert_will_retry_n_times(self, client, num_retries,
                                  status=500, body=b'{}'):
        num_responses = num_retries + 1
        if not isinstance(body, bytes):
            body = json.dumps(body).encode()
        with ClientHTTPStubber(client) as http_stubber:
            for _ in range(num_responses):
                http_stubber.add_response(status=status, body=body)
            with self.assertRaisesRegex(
                    ClientError, 'reached max retries: %s' % num_retries):
                yield
            self.assertEqual(len(http_stubber.requests), num_responses)


class TestLegacyRetry(BaseRetryTest):
    def test_can_override_max_attempts(self):
        client = self.session.create_client(
            'dynamodb', self.region, config=Config(
                retries={'max_attempts': 1}))
        with self.assert_will_retry_n_times(client, 1):
            client.list_tables()

    def test_do_not_attempt_retries(self):
        client = self.session.create_client(
            'dynamodb', self.region, config=Config(
                retries={'max_attempts': 0}))
        with self.assert_will_retry_n_times(client, 0):
            client.list_tables()

    def test_setting_max_attempts_does_not_set_for_other_clients(self):
        # Make one client with max attempts configured.
        self.session.create_client(
            'codecommit', self.region, config=Config(
                retries={'max_attempts': 1}))

        # Make another client that has no custom retry configured.
        client = self.session.create_client('codecommit', self.region)
        # It should use the default max retries, which should be four retries
        # for this service.
        with self.assert_will_retry_n_times(client, 4):
            client.list_repositories()

    def test_service_specific_defaults_do_not_mutate_general_defaults(self):
        # This tests for a bug where if you created a client for a service
        # with specific retry configurations and then created a client for
        # a service whose retry configurations fallback to the general
        # defaults, the second client would actually use the defaults of
        # the first client.

        # Make a dynamodb client. It's a special case client that is
        # configured to a make a maximum of 10 requests (9 retries).
        client = self.session.create_client('dynamodb', self.region)
        with self.assert_will_retry_n_times(client, 9):
            client.list_tables()

        # A codecommit client is not a special case for retries. It will at
        # most make 5 requests (4 retries) for its default.
        client = self.session.create_client('codecommit', self.region)
        with self.assert_will_retry_n_times(client, 4):
            client.list_repositories()

    def test_set_max_attempts_on_session(self):
        self.session.set_default_client_config(
            Config(retries={'max_attempts': 1}))
        # Max attempts should be inherited from the session.
        client = self.session.create_client('codecommit', self.region)
        with self.assert_will_retry_n_times(client, 1):
            client.list_repositories()

    def test_can_clobber_max_attempts_on_session(self):
        self.session.set_default_client_config(
            Config(retries={'max_attempts': 1}))
        # Max attempts should override the session's configured max attempts.
        client = self.session.create_client(
            'codecommit', self.region, config=Config(
                retries={'max_attempts': 0}))
        with self.assert_will_retry_n_times(client, 0):
            client.list_repositories()


class TestRetriesV2(BaseRetryTest):
    def create_client_with_retry_mode(self, service, retry_mode,
                                      max_attempts=None):
        retries = {'mode': retry_mode}
        if max_attempts is not None:
            retries['total_max_attempts'] = max_attempts
        client = self.session.create_client(
            service, self.region, config=Config(retries=retries))
        return client

    def test_standard_mode_has_default_3_retries(self):
        client = self.create_client_with_retry_mode(
            'dynamodb', retry_mode='standard')
        with self.assert_will_retry_n_times(client, 2):
            client.list_tables()

    def test_standard_mode_can_configure_max_attempts(self):
        client = self.create_client_with_retry_mode(
            'dynamodb', retry_mode='standard', max_attempts=5)
        with self.assert_will_retry_n_times(client, 4):
            client.list_tables()

    def test_no_retry_needed_standard_mode(self):
        client = self.create_client_with_retry_mode(
            'dynamodb', retry_mode='standard')
        with ClientHTTPStubber(client) as http_stubber:
            http_stubber.add_response(status=200, body=b'{}')
            client.list_tables()

    def test_standard_mode_retry_throttling_error(self):
        client = self.create_client_with_retry_mode(
            'dynamodb', retry_mode='standard')
        error_body = {
            "__type": "ThrottlingException",
            "message": "Error"
        }
        with self.assert_will_retry_n_times(client, 2,
                                            status=400,
                                            body=error_body):
            client.list_tables()

    def test_standard_mode_retry_transient_error(self):
        client = self.create_client_with_retry_mode(
            'dynamodb', retry_mode='standard')
        with self.assert_will_retry_n_times(client, 2, status=502):
            client.list_tables()

    def test_adaptive_mode_still_retries_errors(self):
        # Verify that adaptive mode is just adding on to standard mode.
        client = self.create_client_with_retry_mode(
            'dynamodb', retry_mode='adaptive')
        with self.assert_will_retry_n_times(client, 2):
            client.list_tables()

    def test_adaptive_mode_retry_transient_error(self):
        client = self.create_client_with_retry_mode(
            'dynamodb', retry_mode='adaptive')
        with self.assert_will_retry_n_times(client, 2, status=502):
            client.list_tables()

    def test_can_exhaust_default_retry_quota(self):
        # Quota of 500 / 5 retry costs == 100 retry attempts
        # 100 retry attempts / 2 retries per API call == 50 client calls
        client = self.create_client_with_retry_mode(
            'dynamodb', retry_mode='standard')
        for i in range(50):
            with self.assert_will_retry_n_times(client, 2, status=502):
                client.list_tables()
        # Now on the 51th attempt we should see quota errors, which we can
        # verify by looking at the request metadata.
        with ClientHTTPStubber(client) as http_stubber:
            http_stubber.add_response(status=502, body=b'{}')
            with self.assertRaises(ClientError) as e:
                client.list_tables()
        self.assertTrue(
            e.exception.response['ResponseMetadata'].get('RetryQuotaReached')
        )
