# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Temporary test suite for updated credential refresh behavior.

These tests validate the updated credential refresh behavior, which is
currently gated behind the DEFAULT_NEW_CREDENTIAL_REFRESH flag and not
yet available to external users. Once the changes are validated
internally and released publicly, the classes below will replace the
corresponding classes in test_credentials.py and the standalone tests
will be added to test_credentials.py. This file will then be removed.

Mirror policy for GA migration:
- use ``pass`` when the original class is unchanged on the new path
- subclass the original class when all original tests still apply and we
  only need additive flag-on coverage
- fully copy the class when the new path needs removals or replacements,
  so this file is the GA-ready replacement
"""

import operator
import os
import threading
from datetime import datetime, timedelta, timezone

import pytest
from dateutil.tz import tzlocal

from botocore import credentials, utils
from botocore.awsrequest import AWSResponse
from botocore.compat import json
from botocore.exceptions import (
    ClientError,
    ConnectionClosedError,
    ConnectTimeoutError,
    CredentialRetrievalError,
    InvalidIMDSEndpointError,
    LoginInvalidCachedTokenError,
    MetadataRetrievalError,
    ReadTimeoutError,
    RefreshNonRecoverableError,
    SSOTokenLoadError,
    UnauthorizedSSOTokenError,
)
from tests import (
    BaseEnvVar,
    IntegerRefresher,
    RawResponse,
    mock,
    unittest,
)
from tests.unit import test_credentials

DATE = datetime(2021, 12, 10, 0, 0, 0, tzinfo=timezone.utc)
DT_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
CREDENTIAL_REFRESH_TEST_CASES_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'credential_refresh',
    'credential-refresh-tests.json',
)


@pytest.fixture(autouse=True)
def _enable_new_credential_refresh(monkeypatch):
    monkeypatch.setattr(credentials, 'DEFAULT_NEW_CREDENTIAL_REFRESH', True)
    monkeypatch.setattr(utils, 'DEFAULT_NEW_CREDENTIAL_REFRESH', True)


# ---------------------------------------------------------------------------
# Replacement classes: these mirror the classes in test_credentials.py with
# assertions updated for the new credential refresh behavior.
# ---------------------------------------------------------------------------


class TestRefreshableCredentials(BaseEnvVar):
    def setUp(self):
        super().setUp()
        self.refresher = mock.Mock()
        self.future_time = datetime.now(tzlocal()) + timedelta(hours=24)
        self.expiry_time = datetime.now(tzlocal()) - timedelta(minutes=30)
        self.metadata = {
            'access_key': 'NEW-ACCESS',
            'secret_key': 'NEW-SECRET',
            'token': 'NEW-TOKEN',
            'expiry_time': self.future_time.isoformat(),
            'role_name': 'rolename',
        }
        self.refresher.return_value = self.metadata
        self.mock_time = mock.Mock(return_value=datetime.now(tzlocal()))
        self.creds = credentials.RefreshableCredentials(
            'ORIGINAL-ACCESS',
            'ORIGINAL-SECRET',
            'ORIGINAL-TOKEN',
            self.expiry_time,
            self.refresher,
            'iam-role',
            time_fetcher=self.mock_time,
        )

    def test_refresh_needed(self):
        # The expiry time was set for 30 minutes ago, so if we
        # say the current time is now(), then we should need
        # a refresh.
        self.mock_time.return_value = datetime.now(tzlocal())
        self.assertTrue(self.creds.refresh_needed())
        # We should refresh creds, if we try to access "access_key"
        # or any of the cred vars.
        self.assertEqual(self.creds.access_key, 'NEW-ACCESS')
        self.assertEqual(self.creds.secret_key, 'NEW-SECRET')
        self.assertEqual(self.creds.token, 'NEW-TOKEN')

    def test_no_expiration(self):
        creds = credentials.RefreshableCredentials(
            'ORIGINAL-ACCESS',
            'ORIGINAL-SECRET',
            'ORIGINAL-TOKEN',
            None,
            self.refresher,
            'iam-role',
            time_fetcher=self.mock_time,
        )
        self.assertFalse(creds.refresh_needed())

    def test_no_refresh_needed(self):
        # The expiry time was 30 minutes ago, let's say it's an hour
        # ago currently.  That would mean we don't need a refresh.
        self.mock_time.return_value = datetime.now(tzlocal()) - timedelta(
            minutes=60
        )
        self.assertTrue(not self.creds.refresh_needed())

        self.assertEqual(self.creds.access_key, 'ORIGINAL-ACCESS')
        self.assertEqual(self.creds.secret_key, 'ORIGINAL-SECRET')
        self.assertEqual(self.creds.token, 'ORIGINAL-TOKEN')

    def test_get_credentials_set(self):
        # We need to return a consistent set of credentials to use during the
        # signing process.
        self.mock_time.return_value = datetime.now(tzlocal()) - timedelta(
            minutes=60
        )
        self.assertTrue(not self.creds.refresh_needed())
        credential_set = self.creds.get_frozen_credentials()
        self.assertEqual(credential_set.access_key, 'ORIGINAL-ACCESS')
        self.assertEqual(credential_set.secret_key, 'ORIGINAL-SECRET')
        self.assertEqual(credential_set.token, 'ORIGINAL-TOKEN')

    def test_refresh_returns_empty_dict(self):
        # An empty dict from the source is treated as a failed refresh
        # and we fall back to cached credentials.
        self.refresher.return_value = {}
        self.mock_time.return_value = datetime.now(tzlocal())
        self.assertTrue(self.creds.refresh_needed())
        self.assertEqual(self.creds.access_key, 'ORIGINAL-ACCESS')
        self.assertTrue(self.refresher.called)

    def test_refresh_returns_none(self):
        # None from the source is treated as a failed refresh and we fall
        # back to cached credentials.
        self.refresher.return_value = None
        self.mock_time.return_value = datetime.now(tzlocal())
        self.assertTrue(self.creds.refresh_needed())
        self.assertEqual(self.creds.access_key, 'ORIGINAL-ACCESS')
        self.assertTrue(self.refresher.called)

    def test_refresh_returns_partial_credentials(self):
        # Partial credentials from the source are treated as a failed
        # refresh and we fall back to cached credentials.
        self.refresher.return_value = {'access_key': 'akid'}
        self.mock_time.return_value = datetime.now(tzlocal())
        self.assertTrue(self.creds.refresh_needed())
        self.assertEqual(self.creds.access_key, 'ORIGINAL-ACCESS')
        self.assertTrue(self.refresher.called)


class TestRefreshLogic(unittest.TestCase):
    def test_mandatory_refresh_needed(self):
        creds = IntegerRefresher(
            # These values will immediately trigger
            # a mandatory refresh.
            creds_last_for=2,
            mandatory_refresh=3,
            advisory_refresh=3,
        )
        temp = creds.get_frozen_credentials()
        self.assertEqual(temp, credentials.ReadOnlyCredentials('1', '1', '1'))

    def test_advisory_refresh_needed(self):
        creds = IntegerRefresher(
            # These values will immediately trigger
            # an advisory refresh.
            creds_last_for=4,
            mandatory_refresh=2,
            advisory_refresh=5,
        )
        temp = creds.get_frozen_credentials()
        self.assertEqual(temp, credentials.ReadOnlyCredentials('1', '1', '1'))

    def test_refresh_fails_is_not_an_error_during_advisory_period(self):
        fail_refresh = mock.Mock(side_effect=Exception("refresh failed"))
        creds = IntegerRefresher(
            creds_last_for=5,
            advisory_refresh=7,
            mandatory_refresh=3,
            refresh_function=fail_refresh,
        )
        temp = creds.get_frozen_credentials()
        # We should have called the refresh function.
        self.assertTrue(fail_refresh.called)
        # The fail_refresh function will raise an exception.
        # Because we're in the advisory period we'll not propogate
        # the exception and return the current set of credentials
        # (generation '0').
        self.assertEqual(temp, credentials.ReadOnlyCredentials('0', '0', '0'))

    def test_exception_not_propogated_on_error_during_mandatory_period(self):
        # Refresh failures in the mandatory window fall back to cached
        # credentials instead of propagating.
        fail_refresh = mock.Mock(side_effect=Exception("refresh failed"))
        creds = IntegerRefresher(
            creds_last_for=5,
            advisory_refresh=10,
            # Note we're in the mandatory period now (5 < 7 < 10).
            mandatory_refresh=7,
            refresh_function=fail_refresh,
        )
        temp = creds.get_frozen_credentials()
        self.assertTrue(fail_refresh.called)
        self.assertEqual(temp, credentials.ReadOnlyCredentials('0', '0', '0'))

    def test_exception_not_propogated_on_expired_credentials(self):
        # Even with fully expired credentials, a refresh failure returns
        # the cached credentials.
        fail_refresh = mock.Mock(side_effect=Exception("refresh failed"))
        creds = IntegerRefresher(
            # Setting this to 0 means the credentials are immediately
            # expired.
            creds_last_for=0,
            advisory_refresh=10,
            mandatory_refresh=7,
            refresh_function=fail_refresh,
        )
        temp = creds.get_frozen_credentials()
        self.assertTrue(fail_refresh.called)
        self.assertEqual(temp, credentials.ReadOnlyCredentials('0', '0', '0'))

    def test_refresh_giving_expired_credentials_returns_cached(self):
        # This verifies an edge case where refreshed credentials
        # still give expired credentials:
        # 1. We see credentials are expired.
        # 2. We try to refresh the credentials.
        # 3. The "refreshed" credentials are still expired.
        #
        # In this case, we treat it as a failed refresh and fall back
        # to the cached credentials.
        creds = IntegerRefresher(
            # Negative number indicates that the credentials
            # have already been expired for 2 seconds, even
            # on refresh.
            creds_last_for=-2,
        )
        temp = creds.get_frozen_credentials()
        self.assertEqual(temp, credentials.ReadOnlyCredentials('0', '0', '0'))


# ---------------------------------------------------------------------------
# Mirrored provider suites: these reuse the existing Env and Process provider
# tests with the flag enabled. Because these providers are out of scope for
# static stability, their provider behavior should remain unchanged.
# ---------------------------------------------------------------------------
class TestEnvVarFlagOn(test_credentials.TestEnvVar):
    pass


class TestProcessProviderFlagOn(test_credentials.TestProcessProvider):
    pass


class TestInstanceMetadataProviderFlagOn(
    test_credentials.TestInstanceMetadataProvider
):
    # GA: keep all tests from test_credentials.TestInstanceMetadataProvider and
    # add the shared static-stability coverage below.
    def test_refresh_failure_returns_cached_credentials(self):
        # IMDS should pick up shared static stability from
        # RefreshableCredentials.
        fetcher = mock.Mock()
        fetcher.retrieve_iam_role_credentials.side_effect = [
            {
                'access_key': 'a',
                'secret_key': 'b',
                'token': 'c',
                'expiry_time': '2000-01-01T00:00:00Z',
                'role_name': 'myrole',
            },
            Exception("imds down"),
        ]
        provider = credentials.InstanceMetadataProvider(
            iam_role_fetcher=fetcher
        )

        creds = provider.load()

        self.assertEqual(creds.access_key, 'a')
        self.assertEqual(fetcher.retrieve_iam_role_credentials.call_count, 2)


class TestInstanceMetadataFetcherFlagOn(unittest.TestCase):
    # GA replacement for test_utils.TestInstanceMetadataFetcher.
    #
    # Relative to the legacy class, this version:
    # - keeps the general IMDS fetcher coverage that still applies
    # - removes:
    #   - test_expiry_time_extension
    #   - test_expired_expiry_extension
    #   - test_expiry_extension_with_config
    #   - test_expiry_extension_with_bad_datetime
    # - adds new-path coverage for IMDS returning the real expiry unchanged
    def setUp(self):
        urllib3_session_send = 'botocore.httpsession.URLLib3Session.send'
        self._urllib3_patch = mock.patch(urllib3_session_send)
        self._send = self._urllib3_patch.start()
        self._imds_responses = []
        self._send.side_effect = self.get_imds_response
        self._role_name = 'role-name'
        self._creds = {
            'AccessKeyId': 'spam',
            'SecretAccessKey': 'eggs',
            'Token': 'spam-token',
            'Expiration': 'something',
        }
        self._expected_creds = {
            'access_key': self._creds['AccessKeyId'],
            'secret_key': self._creds['SecretAccessKey'],
            'token': self._creds['Token'],
            'expiry_time': self._creds['Expiration'],
            'role_name': self._role_name,
        }

    def tearDown(self):
        self._urllib3_patch.stop()

    def add_imds_response(self, body, status_code=200):
        response = AWSResponse(
            url='http://169.254.169.254/',
            status_code=status_code,
            headers={},
            raw=RawResponse(body),
        )
        self._imds_responses.append(response)

    def add_get_role_name_imds_response(self, role_name=None):
        if role_name is None:
            role_name = self._role_name
        self.add_imds_response(body=role_name.encode('utf-8'))

    def add_get_credentials_imds_response(self, creds=None):
        if creds is None:
            creds = self._creds
        self.add_imds_response(
            status_code=200, body=json.dumps(creds).encode('utf-8')
        )

    def add_get_token_imds_response(self, token, status_code=200):
        self.add_imds_response(
            body=token.encode('utf-8'), status_code=status_code
        )

    def add_metadata_token_not_supported_response(self):
        self.add_imds_response(b'', status_code=404)

    def add_imds_connection_error(self, exception):
        self._imds_responses.append(exception)

    def add_default_imds_responses(self):
        self.add_get_token_imds_response(token='token')
        self.add_get_role_name_imds_response()
        self.add_get_credentials_imds_response()

    def get_imds_response(self, request):
        response = self._imds_responses.pop(0)
        if isinstance(response, Exception):
            raise response
        return response

    def _test_imds_base_url(self, config, expected_url):
        self.add_default_imds_responses()

        fetcher = utils.InstanceMetadataFetcher(config=config)
        result = fetcher.retrieve_iam_role_credentials()

        self.assertEqual(result, self._expected_creds)
        self.assertEqual(fetcher.get_base_url(), expected_url)

    def test_disabled_by_environment(self):
        env = {'AWS_EC2_METADATA_DISABLED': 'true'}
        fetcher = utils.InstanceMetadataFetcher(env=env)
        result = fetcher.retrieve_iam_role_credentials()
        self.assertEqual(result, {})
        self._send.assert_not_called()

    def test_disabled_by_environment_mixed_case(self):
        env = {'AWS_EC2_METADATA_DISABLED': 'tRuE'}
        fetcher = utils.InstanceMetadataFetcher(env=env)
        result = fetcher.retrieve_iam_role_credentials()
        self.assertEqual(result, {})
        self._send.assert_not_called()

    def test_disabling_env_var_not_true(self):
        url = 'https://example.com/'
        env = {'AWS_EC2_METADATA_DISABLED': 'false'}

        self.add_default_imds_responses()

        fetcher = utils.InstanceMetadataFetcher(base_url=url, env=env)
        result = fetcher.retrieve_iam_role_credentials()

        self.assertEqual(result, self._expected_creds)

    def test_ec2_metadata_endpoint_service_mode(self):
        configs = [
            (
                {'ec2_metadata_service_endpoint_mode': 'ipv6'},
                'http://[fd00:ec2::254]/',
            ),
            (
                {'ec2_metadata_service_endpoint_mode': 'ipv6'},
                'http://[fd00:ec2::254]/',
            ),
            (
                {'ec2_metadata_service_endpoint_mode': 'ipv4'},
                'http://169.254.169.254/',
            ),
            (
                {'ec2_metadata_service_endpoint_mode': 'foo'},
                'http://169.254.169.254/',
            ),
            (
                {
                    'ec2_metadata_service_endpoint_mode': 'ipv6',
                    'ec2_metadata_service_endpoint': 'http://[fd00:ec2::010]/',
                },
                'http://[fd00:ec2::010]/',
            ),
        ]

        for config, expected_url in configs:
            self._test_imds_base_url(config, expected_url)

    def test_metadata_endpoint(self):
        urls = [
            'http://fd00:ec2:0000:0000:0000:0000:0000:0000/',
            'http://[fd00:ec2::010]/',
            'http://192.168.1.1/',
        ]
        for url in urls:
            self.assertTrue(utils.is_valid_uri(url))

    def test_ipv6_endpoint_no_brackets_env_var_set(self):
        url = 'http://fd00:ec2::010/'
        self.assertFalse(utils.is_valid_ipv6_endpoint_url(url))

    def test_ipv6_invalid_endpoint(self):
        url = 'not.a:valid:dom@in'
        config = {'ec2_metadata_service_endpoint': url}
        with self.assertRaises(InvalidIMDSEndpointError):
            utils.InstanceMetadataFetcher(config=config)

    def test_ipv6_endpoint_env_var_set_and_args(self):
        url = 'http://[fd00:ec2::254]/'
        url_arg = 'http://fd00:ec2:0000:0000:0000:8a2e:0370:7334/'
        config = {'ec2_metadata_service_endpoint': url}

        self.add_default_imds_responses()

        fetcher = utils.InstanceMetadataFetcher(
            config=config, base_url=url_arg
        )
        result = fetcher.retrieve_iam_role_credentials()

        self.assertEqual(result, self._expected_creds)
        self.assertEqual(fetcher.get_base_url(), url_arg)

    def test_ipv6_imds_not_allocated(self):
        url = 'http://fd00:ec2:0000:0000:0000:0000:0000:0000/'
        config = {'ec2_metadata_service_endpoint': url}

        self.add_imds_response(status_code=400, body=b'{}')

        fetcher = utils.InstanceMetadataFetcher(config=config)
        result = fetcher.retrieve_iam_role_credentials()
        self.assertEqual(result, {})

    def test_ipv6_imds_empty_config(self):
        configs = [
            ({'ec2_metadata_service_endpoint': ''}, 'http://169.254.169.254/'),
            (
                {'ec2_metadata_service_endpoint_mode': ''},
                'http://169.254.169.254/',
            ),
            ({}, 'http://169.254.169.254/'),
            (None, 'http://169.254.169.254/'),
        ]

        for config, expected_url in configs:
            self._test_imds_base_url(config, expected_url)

    def test_includes_user_agent_header(self):
        user_agent = 'my-user-agent'
        self.add_default_imds_responses()

        utils.InstanceMetadataFetcher(
            user_agent=user_agent
        ).retrieve_iam_role_credentials()

        self.assertEqual(self._send.call_count, 3)
        for call in self._send.calls:
            self.assertTrue(call[0][0].headers['User-Agent'], user_agent)

    def test_non_200_response_for_role_name_is_retried(self):
        self.add_get_token_imds_response(token='token')
        self.add_imds_response(
            status_code=429, body=b'{"message": "Slow down"}'
        )
        self.add_get_role_name_imds_response()
        self.add_get_credentials_imds_response()
        result = utils.InstanceMetadataFetcher(
            num_attempts=2
        ).retrieve_iam_role_credentials()
        self.assertEqual(result, self._expected_creds)

    def test_http_connection_error_for_role_name_is_retried(self):
        self.add_get_token_imds_response(token='token')
        self.add_imds_connection_error(ConnectionClosedError(endpoint_url=''))
        self.add_get_role_name_imds_response()
        self.add_get_credentials_imds_response()
        result = utils.InstanceMetadataFetcher(
            num_attempts=2
        ).retrieve_iam_role_credentials()
        self.assertEqual(result, self._expected_creds)

    def test_empty_response_for_role_name_is_retried(self):
        self.add_get_token_imds_response(token='token')
        self.add_imds_response(body=b'')
        self.add_get_role_name_imds_response()
        self.add_get_credentials_imds_response()
        result = utils.InstanceMetadataFetcher(
            num_attempts=2
        ).retrieve_iam_role_credentials()
        self.assertEqual(result, self._expected_creds)

    def test_non_200_response_is_retried(self):
        self.add_get_token_imds_response(token='token')
        self.add_get_role_name_imds_response()
        self.add_imds_response(
            status_code=429, body=b'{"message": "Slow down"}'
        )
        self.add_get_credentials_imds_response()
        result = utils.InstanceMetadataFetcher(
            num_attempts=2
        ).retrieve_iam_role_credentials()
        self.assertEqual(result, self._expected_creds)

    def test_http_connection_errors_is_retried(self):
        self.add_get_token_imds_response(token='token')
        self.add_get_role_name_imds_response()
        self.add_imds_connection_error(ConnectionClosedError(endpoint_url=''))
        self.add_get_credentials_imds_response()
        result = utils.InstanceMetadataFetcher(
            num_attempts=2
        ).retrieve_iam_role_credentials()
        self.assertEqual(result, self._expected_creds)

    def test_empty_response_is_retried(self):
        self.add_get_token_imds_response(token='token')
        self.add_get_role_name_imds_response()
        self.add_imds_response(body=b'')
        self.add_get_credentials_imds_response()
        result = utils.InstanceMetadataFetcher(
            num_attempts=2
        ).retrieve_iam_role_credentials()
        self.assertEqual(result, self._expected_creds)

    def test_invalid_json_is_retried(self):
        self.add_get_token_imds_response(token='token')
        self.add_get_role_name_imds_response()
        self.add_imds_response(body=b'{"AccessKey":')
        self.add_get_credentials_imds_response()
        result = utils.InstanceMetadataFetcher(
            num_attempts=2
        ).retrieve_iam_role_credentials()
        self.assertEqual(result, self._expected_creds)

    def test_exhaust_retries_on_role_name_request(self):
        self.add_get_token_imds_response(token='token')
        self.add_imds_response(status_code=400, body=b'')
        result = utils.InstanceMetadataFetcher(
            num_attempts=1
        ).retrieve_iam_role_credentials()
        self.assertEqual(result, {})

    def test_exhaust_retries_on_credentials_request(self):
        self.add_get_token_imds_response(token='token')
        self.add_get_role_name_imds_response()
        self.add_imds_response(status_code=400, body=b'')
        result = utils.InstanceMetadataFetcher(
            num_attempts=1
        ).retrieve_iam_role_credentials()
        self.assertEqual(result, {})

    def test_missing_fields_in_credentials_response(self):
        self.add_get_token_imds_response(token='token')
        self.add_get_role_name_imds_response()
        self.add_imds_response(
            body=b'{"Code":"AssumeRoleUnauthorizedAccess","Message":"error"}'
        )
        result = (
            utils.InstanceMetadataFetcher().retrieve_iam_role_credentials()
        )
        self.assertEqual(result, {})

    def test_token_is_included(self):
        user_agent = 'my-user-agent'
        self.add_default_imds_responses()

        result = utils.InstanceMetadataFetcher(
            user_agent=user_agent
        ).retrieve_iam_role_credentials()

        self.assertEqual(self._send.call_count, 3)
        for call in self._send.call_args_list[1:]:
            self.assertEqual(
                call[0][0].headers['x-aws-ec2-metadata-token'], 'token'
            )
        self.assertEqual(result, self._expected_creds)

    def test_metadata_token_not_supported_404(self):
        user_agent = 'my-user-agent'
        self.add_imds_response(b'', status_code=404)
        self.add_get_role_name_imds_response()
        self.add_get_credentials_imds_response()

        result = utils.InstanceMetadataFetcher(
            user_agent=user_agent
        ).retrieve_iam_role_credentials()

        for call in self._send.call_args_list[1:]:
            self.assertNotIn('x-aws-ec2-metadata-token', call[0][0].headers)
        self.assertEqual(result, self._expected_creds)

    def test_metadata_token_not_supported_403(self):
        user_agent = 'my-user-agent'
        self.add_imds_response(b'', status_code=403)
        self.add_get_role_name_imds_response()
        self.add_get_credentials_imds_response()

        result = utils.InstanceMetadataFetcher(
            user_agent=user_agent
        ).retrieve_iam_role_credentials()

        for call in self._send.call_args_list[1:]:
            self.assertNotIn('x-aws-ec2-metadata-token', call[0][0].headers)
        self.assertEqual(result, self._expected_creds)

    def test_metadata_token_not_supported_405(self):
        user_agent = 'my-user-agent'
        self.add_imds_response(b'', status_code=405)
        self.add_get_role_name_imds_response()
        self.add_get_credentials_imds_response()

        result = utils.InstanceMetadataFetcher(
            user_agent=user_agent
        ).retrieve_iam_role_credentials()

        for call in self._send.call_args_list[1:]:
            self.assertNotIn('x-aws-ec2-metadata-token', call[0][0].headers)
        self.assertEqual(result, self._expected_creds)

    def test_metadata_token_not_supported_timeout(self):
        user_agent = 'my-user-agent'
        self.add_imds_connection_error(ReadTimeoutError(endpoint_url='url'))
        self.add_get_role_name_imds_response()
        self.add_get_credentials_imds_response()

        result = utils.InstanceMetadataFetcher(
            user_agent=user_agent
        ).retrieve_iam_role_credentials()

        for call in self._send.call_args_list[1:]:
            self.assertNotIn('x-aws-ec2-metadata-token', call[0][0].headers)
        self.assertEqual(result, self._expected_creds)

    def test_token_not_supported_exhaust_retries(self):
        user_agent = 'my-user-agent'
        self.add_imds_connection_error(ConnectTimeoutError(endpoint_url='url'))
        self.add_get_role_name_imds_response()
        self.add_get_credentials_imds_response()

        result = utils.InstanceMetadataFetcher(
            user_agent=user_agent
        ).retrieve_iam_role_credentials()

        for call in self._send.call_args_list[1:]:
            self.assertNotIn('x-aws-ec2-metadata-token', call[0][0].headers)
        self.assertEqual(result, self._expected_creds)

    def test_metadata_token_bad_request_yields_no_credentials(self):
        user_agent = 'my-user-agent'
        self.add_imds_response(b'', status_code=400)
        result = utils.InstanceMetadataFetcher(
            user_agent=user_agent
        ).retrieve_iam_role_credentials()
        self.assertEqual(result, {})

    def test_v1_disabled_by_config(self):
        config = {'ec2_metadata_v1_disabled': True}
        self.add_imds_response(b'', status_code=404)
        fetcher = utils.InstanceMetadataFetcher(num_attempts=1, config=config)
        with self.assertRaises(MetadataRetrievalError):
            fetcher.retrieve_iam_role_credentials()

    def _get_datetime(self, dt=None, offset=None, offset_func=operator.add):
        if dt is None:
            dt = DATE.replace(tzinfo=None)
        if offset is not None:
            dt = offset_func(dt, offset)

        return dt

    def _get_default_creds(self, overrides=None):
        if overrides is None:
            overrides = {}

        creds = {
            'AccessKeyId': 'access',
            'SecretAccessKey': 'secret',
            'Token': 'token',
            'Expiration': '1970-01-01T00:00:00',
        }
        creds.update(overrides)
        return creds

    def _convert_creds_to_imds_fetcher(self, creds):
        return {
            'access_key': creds['AccessKeyId'],
            'secret_key': creds['SecretAccessKey'],
            'token': creds['Token'],
            'expiry_time': creds['Expiration'],
            'role_name': self._role_name,
        }

    def mock_randint(self, int_val=600):
        randint_mock = mock.Mock()
        randint_mock.return_value = int_val
        return randint_mock

    def test_near_expiry_credentials_are_not_extended(self):
        current_time = self._get_datetime()
        expiration_time = self._get_datetime(
            dt=current_time, offset=timedelta(seconds=14 * 60)
        )

        creds = self._get_default_creds(
            {"Expiration": expiration_time.strftime(DT_FORMAT)}
        )
        expected_data = self._convert_creds_to_imds_fetcher(creds)

        self.add_get_token_imds_response(token='token')
        self.add_get_role_name_imds_response()
        self.add_imds_response(
            status_code=200, body=json.dumps(creds).encode('utf-8')
        )

        with mock.patch("random.randint", self.mock_randint()):
            fetcher = utils.InstanceMetadataFetcher()
            result = fetcher.retrieve_iam_role_credentials()
            assert result == expected_data

    def test_already_expired_credentials_are_not_extended(self):
        current_time = self._get_datetime()
        expiration_time = self._get_datetime(
            dt=current_time,
            offset=timedelta(seconds=14 * 60),
            offset_func=operator.sub,
        )

        creds = self._get_default_creds(
            {"Expiration": expiration_time.strftime(DT_FORMAT)}
        )
        expected_data = self._convert_creds_to_imds_fetcher(creds)

        self.add_get_token_imds_response(token='token')
        self.add_get_role_name_imds_response()
        self.add_imds_response(
            status_code=200, body=json.dumps(creds).encode('utf-8')
        )

        with mock.patch("random.randint", self.mock_randint()):
            fetcher = utils.InstanceMetadataFetcher()
            result = fetcher.retrieve_iam_role_credentials()
            assert result == expected_data


# ---------------------------------------------------------------------------
# Net-new tests: these cover backoff behavior that has no counterpart in the
# legacy code path. At GA they will be added to test_credentials.py.
# ---------------------------------------------------------------------------


@pytest.fixture
def refresher():
    return mock.Mock()


@pytest.fixture
def mock_time():
    return mock.Mock(return_value=DATE)


@pytest.fixture
def creds(refresher, mock_time):
    # The expiry time is in the past so that accessing the credentials
    # triggers a refresh.
    return credentials.RefreshableCredentials(
        'ORIGINAL-ACCESS',
        'ORIGINAL-SECRET',
        'ORIGINAL-TOKEN',
        mock_time() - timedelta(minutes=30),
        refresher,
        'iam-role',
        time_fetcher=mock_time,
    )


def _valid_metadata(mock_time, expires_in=timedelta(hours=24)):
    expiry_time = mock_time() + expires_in
    return {
        'access_key': 'NEW-ACCESS',
        'secret_key': 'NEW-SECRET',
        'token': 'NEW-TOKEN',
        'expiry_time': expiry_time.isoformat(),
    }


def _create_refreshable_credentials(
    mock_time,
    refresher=None,
    expires_in=timedelta(hours=24),
    method='iam-role',
    **kwargs,
):
    if refresher is None:
        refresher = mock.Mock()
    return credentials.RefreshableCredentials(
        'ORIGINAL-ACCESS',
        'ORIGINAL-SECRET',
        'ORIGINAL-TOKEN',
        mock_time() + expires_in,
        refresher,
        method,
        time_fetcher=mock_time,
        **kwargs,
    )


class _CacheableNonRecoverableError(Exception, RefreshNonRecoverableError):
    pass


# ---------------------------------------------------------------------------
# Refresh-window tests: these cover the advisory/mandatory defaults and their
# interactions with successful and failed refreshes.
# ---------------------------------------------------------------------------


def _assert_refresh_boundary(
    creds, mock_time, issued_at, expires_in, refresh_window
):
    expiry_time = issued_at + expires_in

    # 1 second outside the window: no refresh yet.
    mock_time.return_value = expiry_time - timedelta(
        seconds=refresh_window + 1
    )
    assert creds.refresh_needed() is False

    # 1 second inside the window: refresh needed.
    mock_time.return_value = expiry_time - timedelta(
        seconds=refresh_window - 1
    )
    assert creds.refresh_needed() is True


def test_15_minute_credentials_do_not_refresh_immediately(mock_time):
    creds = _create_refreshable_credentials(
        mock_time, expires_in=timedelta(minutes=15)
    )

    assert creds.refresh_needed() is False


@pytest.mark.parametrize(
    "expires_in, expected_timeout",
    [
        (timedelta(minutes=20), 5 * 60),
        (timedelta(minutes=20, seconds=1), 15 * 60),
        (timedelta(minutes=89, seconds=59), 15 * 60),
        (timedelta(minutes=90), 60 * 60),
    ],
)
def test_effective_advisory_window_tier_boundaries(
    mock_time, expires_in, expected_timeout
):
    issued_at = mock_time()
    creds = _create_refreshable_credentials(mock_time, expires_in=expires_in)

    _assert_refresh_boundary(
        creds, mock_time, issued_at, expires_in, expected_timeout
    )


def test_effective_advisory_window_uses_lifetime_at_set_time(mock_time):
    issued_at = mock_time()
    creds = _create_refreshable_credentials(
        mock_time,
        expires_in=timedelta(hours=2),
    )

    mock_time.return_value = issued_at + timedelta(minutes=70)

    assert creds.refresh_needed() is True


def test_effective_advisory_window_recomputed_after_successful_refresh(
    mock_time, refresher
):
    issued_at = mock_time()
    refresher.return_value = _valid_metadata(
        mock_time, expires_in=timedelta(hours=6)
    )
    creds = _create_refreshable_credentials(
        mock_time,
        refresher=refresher,
        expires_in=timedelta(seconds=30),
    )

    frozen = creds.get_frozen_credentials()

    assert frozen.access_key == 'NEW-ACCESS'
    _assert_refresh_boundary(
        creds, mock_time, issued_at, timedelta(hours=6), 60 * 60
    )


def test_effective_advisory_window_not_recomputed_on_failure(
    mock_time, refresher
):
    issued_at = mock_time()
    creds = _create_refreshable_credentials(
        mock_time,
        refresher=refresher,
        expires_in=timedelta(minutes=30),
    )

    refresher.side_effect = Exception("source down")
    mock_time.return_value = issued_at + timedelta(minutes=16)

    assert creds.refresh_needed() is True

    frozen = creds.get_frozen_credentials()

    assert frozen.access_key == 'ORIGINAL-ACCESS'
    assert creds.refresh_needed() is True


def test_mandatory_refresh_boundary_is_one_minute(mock_time):
    issued_at = mock_time()
    expires_in = timedelta(minutes=30)
    creds = _create_refreshable_credentials(
        mock_time,
        expires_in=expires_in,
    )
    expiry_time = issued_at + expires_in

    # RefreshableCredentials does not branch on is_mandatory directly, but
    # _refresh() still computes it and _StrictRefreshableCredentials depends
    # on the mandatory-window classification.
    mock_time.return_value = expiry_time - timedelta(seconds=61)
    with mock.patch.object(creds, '_protected_refresh') as protected_refresh:
        creds.get_frozen_credentials()
    protected_refresh.assert_called_once_with(is_mandatory=False)

    # Inside the 60-second mandatory window.
    mock_time.return_value = expiry_time - timedelta(seconds=59)
    with mock.patch.object(creds, '_protected_refresh') as protected_refresh:
        creds.get_frozen_credentials()
    protected_refresh.assert_called_once_with(is_mandatory=True)


def test_explicit_refresh_windows_are_preserved(mock_time):
    issued_at = mock_time()
    expires_in = timedelta(minutes=2)
    creds = _create_refreshable_credentials(
        mock_time,
        expires_in=expires_in,
        advisory_timeout=45,
        mandatory_timeout=10,
    )
    expiry_time = issued_at + expires_in

    _assert_refresh_boundary(creds, mock_time, issued_at, expires_in, 45)

    # Outside the explicit 10-second mandatory window.
    mock_time.return_value = expiry_time - timedelta(seconds=11)
    with mock.patch.object(creds, '_protected_refresh') as protected_refresh:
        creds.get_frozen_credentials()
    protected_refresh.assert_called_once_with(is_mandatory=False)

    # Inside the explicit 10-second mandatory window.
    mock_time.return_value = expiry_time - timedelta(seconds=9)
    with mock.patch.object(creds, '_protected_refresh') as protected_refresh:
        creds.get_frozen_credentials()
    protected_refresh.assert_called_once_with(is_mandatory=True)


def test_deferred_first_fetch_uses_recomputed_advisory_window(mock_time):
    issued_at = mock_time()
    refresher = mock.Mock(
        return_value=_valid_metadata(mock_time, expires_in=timedelta(hours=6))
    )
    creds = credentials.DeferredRefreshableCredentials(
        refresher,
        'iam-role',
        time_fetcher=mock_time,
    )

    frozen = creds.get_frozen_credentials()

    assert frozen.access_key == 'NEW-ACCESS'
    assert refresher.call_count == 1
    _assert_refresh_boundary(
        creds, mock_time, issued_at, timedelta(hours=6), 60 * 60
    )


# ---------------------------------------------------------------------------
# Backoff tests: these cover behavior that has no counterpart in the legacy
# code path.
# ---------------------------------------------------------------------------


def test_in_refresh_backoff_does_not_reread_blocked_until(mock_time):
    creds = _create_refreshable_credentials(
        mock_time, expires_in=timedelta(hours=1)
    )
    creds._refresh_blocked_until = DATE + timedelta(minutes=5)

    def clear_backoff_during_read():
        creds._refresh_blocked_until = None
        return DATE

    creds._time_fetcher = clear_backoff_during_read

    assert creds._in_refresh_backoff() is True
    assert creds._refresh_blocked_until is None


def test_failed_refresh_returns_cached_credentials(creds, refresher):
    # When the source fails, we keep serving the cached credentials instead
    # of raising.
    refresher.side_effect = Exception("source down")
    frozen = creds.get_frozen_credentials()
    assert frozen.access_key == 'ORIGINAL-ACCESS'
    assert frozen.secret_key == 'ORIGINAL-SECRET'
    assert frozen.token == 'ORIGINAL-TOKEN'


def test_failed_refresh_is_not_retried_immediately(creds, refresher):
    # After a failed refresh, accessing the credentials again keeps using the
    # cached credentials and does not call the source a second time.
    refresher.side_effect = Exception("source down")
    creds.get_frozen_credentials()
    assert refresher.call_count == 1
    frozen = creds.get_frozen_credentials()
    assert refresher.call_count == 1
    assert frozen.access_key == 'ORIGINAL-ACCESS'


def test_failed_refresh_is_retried_after_backoff(creds, refresher, mock_time):
    # The first refresh fails and the source is not contacted again right
    # away. Once enough time has passed, the next access retries the source
    # and picks up the new credentials.
    refresher.side_effect = [
        Exception("source down"),
        _valid_metadata(mock_time),
    ]
    creds.get_frozen_credentials()
    assert refresher.call_count == 1

    # Advance time past the maximum backoff window (10 minutes) so the next
    # access is allowed to retry.
    mock_time.return_value = DATE + timedelta(minutes=11)
    frozen = creds.get_frozen_credentials()
    assert refresher.call_count == 2
    assert frozen.access_key == 'NEW-ACCESS'


def test_failed_refresh_without_cached_credentials_raises(mock_time):
    # If we've never successfully fetched credentials, a refresh failure has
    # nothing to fall back to and must be surfaced.
    refresher = mock.Mock(side_effect=Exception("source down"))
    creds = credentials.DeferredRefreshableCredentials(
        refresher,
        'iam-role',
        time_fetcher=mock_time,
    )
    with pytest.raises(Exception, match='source down'):
        creds.get_frozen_credentials()


def test_incomplete_refresh_response_without_cached_credentials_raises(
    mock_time,
):
    refresher = mock.Mock(return_value={})
    creds = credentials.DeferredRefreshableCredentials(
        refresher,
        'iam-role',
        time_fetcher=mock_time,
    )
    with pytest.raises(
        CredentialRetrievalError, match='Response did not contain'
    ):
        creds.get_frozen_credentials()


def test_malformed_expiry_without_cached_credentials_raises(mock_time):
    refresher = mock.Mock(
        return_value={
            'access_key': 'NEW-ACCESS',
            'secret_key': 'NEW-SECRET',
            'token': 'NEW-TOKEN',
            'expiry_time': 'not-a-datetime',
        }
    )
    creds = credentials.DeferredRefreshableCredentials(
        refresher,
        'iam-role',
        time_fetcher=mock_time,
    )
    with pytest.raises(CredentialRetrievalError, match='invalid expiry_time'):
        creds.get_frozen_credentials()


def test_malformed_expiry_returns_cached_credentials(creds, refresher):
    refresher.return_value = {
        'access_key': 'NEW-ACCESS',
        'secret_key': 'NEW-SECRET',
        'token': 'NEW-TOKEN',
        'expiry_time': 'not-a-datetime',
    }

    frozen = creds.get_frozen_credentials()

    assert frozen.access_key == 'ORIGINAL-ACCESS'
    assert refresher.call_count == 1

    frozen = creds.get_frozen_credentials()

    assert frozen.access_key == 'ORIGINAL-ACCESS'
    assert refresher.call_count == 1


# ---------------------------------------------------------------------------
# Non-recoverable tests: these cover the flag-on-only behavior for providers
# surfacing non-recoverable errors and short-lived retry suppression.
# ---------------------------------------------------------------------------


class TestNonRecoverableRefresh:
    @pytest.fixture
    def patched_jitter(self):
        with mock.patch('botocore.credentials.random.uniform', return_value=5):
            yield

    def _assert_reauth_raised(self, creds):
        with pytest.raises(
            _CacheableNonRecoverableError, match='reauth required'
        ):
            creds.get_frozen_credentials()

    def test_advisory_nonrecoverable_error_is_not_retried_within_ttl(
        self, patched_jitter, mock_time
    ):
        refresher = mock.Mock(
            side_effect=_CacheableNonRecoverableError("reauth required")
        )
        creds = _create_refreshable_credentials(
            mock_time,
            refresher=refresher,
            expires_in=timedelta(seconds=90),
            advisory_timeout=120,
            mandatory_timeout=60,
        )

        self._assert_reauth_raised(creds)
        assert refresher.call_count == 1

        self._assert_reauth_raised(creds)
        assert refresher.call_count == 1

    def test_mandatory_nonrecoverable_error_is_not_retried_within_ttl(
        self, patched_jitter, creds, refresher
    ):
        refresher.side_effect = _CacheableNonRecoverableError(
            "reauth required"
        )

        self._assert_reauth_raised(creds)
        assert refresher.call_count == 1

        self._assert_reauth_raised(creds)
        assert refresher.call_count == 1

    def test_advisory_nonrecoverable_error_is_retried_after_ttl_expires(
        self, patched_jitter, mock_time
    ):
        refresher = mock.Mock(
            side_effect=[
                _CacheableNonRecoverableError("reauth required"),
                _valid_metadata(mock_time),
            ]
        )
        issued_at = mock_time()
        creds = _create_refreshable_credentials(
            mock_time,
            refresher=refresher,
            expires_in=timedelta(seconds=90),
            advisory_timeout=120,
            mandatory_timeout=60,
        )

        self._assert_reauth_raised(creds)

        mock_time.return_value = issued_at + timedelta(seconds=6)
        frozen = creds.get_frozen_credentials()

        assert refresher.call_count == 2
        assert frozen.access_key == 'NEW-ACCESS'

    def test_deferred_nonrecoverable_error_retries_after_ttl_expires(
        self, patched_jitter, mock_time
    ):
        refresher = mock.Mock(
            side_effect=[
                _CacheableNonRecoverableError("reauth required"),
                _valid_metadata(mock_time),
            ]
        )
        issued_at = mock_time()
        creds = credentials.DeferredRefreshableCredentials(
            refresher,
            'iam-role',
            time_fetcher=mock_time,
        )

        self._assert_reauth_raised(creds)

        self._assert_reauth_raised(creds)
        assert refresher.call_count == 1

        mock_time.return_value = issued_at + timedelta(seconds=6)
        frozen = creds.get_frozen_credentials()

        assert refresher.call_count == 2
        assert frozen.access_key == 'NEW-ACCESS'

    @pytest.mark.parametrize(
        'method',
        ['assume-role', 'assume-role-with-web-identity'],
    )
    def test_sts_nonrecoverable_error_is_not_retried_within_ttl(
        self, patched_jitter, mock_time, method
    ):
        refresher = mock.Mock()
        refresher.side_effect = ClientError(
            {
                'Error': {
                    'Code': 'InvalidIdentityToken',
                    'Message': 'bad token',
                }
            },
            'AssumeRole',
        )
        creds = _create_refreshable_credentials(
            mock_time,
            refresher=refresher,
            expires_in=timedelta(seconds=30),
            method=method,
        )

        with pytest.raises(ClientError, match='InvalidIdentityToken'):
            creds.get_frozen_credentials()

        with pytest.raises(ClientError, match='InvalidIdentityToken'):
            creds.get_frozen_credentials()

        assert refresher.call_count == 1

    def test_sts_nonrecoverable_codes_do_not_apply_to_non_sts_providers(
        self, mock_time
    ):
        # Even if a non-STS provider raises a ClientError with an STS-listed
        # non-recoverable code, we should not classify it as STS
        # non-recoverable unless the provider method is actually STS-backed.
        refresher = mock.Mock(
            side_effect=ClientError(
                {'Error': {'Code': 'AccessDenied', 'Message': 'denied'}},
                'GetRoleCredentials',
            )
        )
        creds = _create_refreshable_credentials(
            mock_time,
            refresher=refresher,
            expires_in=timedelta(seconds=30),
            method='sso',
        )

        frozen = creds.get_frozen_credentials()

        assert frozen.access_key == 'ORIGINAL-ACCESS'
        assert refresher.call_count == 1

        frozen = creds.get_frozen_credentials()

        assert frozen.access_key == 'ORIGINAL-ACCESS'
        assert refresher.call_count == 1


class TestNonRecoverableProviderErrors:
    def test_sso_unauthorized_service_error_raises_nonrecoverable_error(self):
        # Service-side unauthorized responses are non-recoverable.
        token_loader = mock.Mock(
            return_value={
                'accessToken': 'some.sso.token',
                'expiresAt': '2099-10-18T22:26:40Z',
            }
        )
        client = mock.Mock()
        client.exceptions.UnauthorizedException = ClientError
        client.get_role_credentials.side_effect = ClientError(
            {'Error': {'Code': 'UnauthorizedException'}},
            'GetRoleCredentials',
        )
        fetcher = credentials.SSOCredentialFetcher(
            start_url='https://d-92671207e4.awsapps.com/start',
            sso_region='us-east-1',
            role_name='test-role',
            account_id='1234567890',
            client_creator=mock.Mock(return_value=client),
            token_loader=token_loader,
            cache={},
            time_fetcher=mock.Mock(return_value=DATE),
        )

        with pytest.raises(UnauthorizedSSOTokenError):
            fetcher.fetch_credentials()

    def test_sso_expired_cached_token_raises_nonrecoverable_error(self):
        # Client-side expired cached tokens are non-recoverable and should
        # fail before calling SSO.
        token_loader = mock.Mock(
            return_value={
                'accessToken': 'some.sso.token',
                'expiresAt': '2018-10-18T22:26:40Z',
            }
        )
        client = mock.Mock()
        fetcher = credentials.SSOCredentialFetcher(
            start_url='https://d-92671207e4.awsapps.com/start',
            sso_region='us-east-1',
            role_name='test-role',
            account_id='1234567890',
            client_creator=mock.Mock(return_value=client),
            token_loader=token_loader,
            cache={},
            time_fetcher=mock.Mock(return_value=DATE),
        )

        with pytest.raises(UnauthorizedSSOTokenError):
            fetcher.fetch_credentials()
        client.get_role_credentials.assert_not_called()

    def test_sso_missing_cached_token_raises_nonrecoverable_error(self):
        # Client-side token cache load failures are also non-recoverable.
        loader = utils.SSOTokenLoader(cache={})

        with pytest.raises(SSOTokenLoadError):
            loader('https://d-92671207e4.awsapps.com/start')

    @pytest.mark.parametrize(
        'token,error_msg',
        [
            (
                None,
                'Unable to load a existing login session for session test-session.',
            ),
            (
                {'accessToken': {}, 'refreshToken': 'refresh'},
                'missing required fields',
            ),
        ],
    )
    def test_login_refresh_invalid_cached_token_raises_nonrecoverable_error(
        self, token, error_msg
    ):
        # Client-side invalid cached login tokens are non-recoverable.
        token_loader = mock.Mock()
        token_loader.load_token.return_value = token
        fetcher = credentials.LoginCredentialFetcher(
            session_name='test-session',
            token_loader=token_loader,
            client_creator=mock.Mock(),
        )

        with pytest.raises(
            LoginInvalidCachedTokenError,
            match=error_msg,
        ):
            fetcher.refresh_credentials()


class TestInvalidate:
    def test_matching_access_key_forces_refresh(self, mock_time, refresher):
        refresher.return_value = _valid_metadata(mock_time)
        creds = _create_refreshable_credentials(
            mock_time,
            refresher=refresher,
            expires_in=timedelta(hours=1),
        )

        creds._invalidate('ORIGINAL-ACCESS')
        frozen = creds.get_frozen_credentials()

        assert refresher.call_count == 1
        assert frozen.access_key == 'NEW-ACCESS'

    def test_mismatched_access_key_is_noop(self, mock_time, refresher):
        refresher.return_value = _valid_metadata(mock_time)
        creds = _create_refreshable_credentials(
            mock_time,
            refresher=refresher,
            expires_in=timedelta(hours=1),
        )

        creds._invalidate('DIFFERENT-ACCESS')
        frozen = creds.get_frozen_credentials()

        assert refresher.call_count == 0
        assert frozen.access_key == 'ORIGINAL-ACCESS'

    def test_provider_cache_invalidation_failure_still_refreshes(
        self, mock_time, refresher
    ):
        refresher.return_value = _valid_metadata(mock_time)
        invalidate_provider_cache = mock.Mock(
            side_effect=RuntimeError("error")
        )
        creds = _create_refreshable_credentials(
            mock_time,
            refresher=refresher,
            expires_in=timedelta(hours=1),
            invalidate_provider_cache=invalidate_provider_cache,
        )

        creds._invalidate('ORIGINAL-ACCESS')
        frozen = creds.get_frozen_credentials()

        invalidate_provider_cache.assert_called_once_with('ORIGINAL-ACCESS')
        assert refresher.call_count == 1
        assert frozen.access_key == 'NEW-ACCESS'

    def test_does_not_bypass_refresh_backoff(
        self, creds, refresher, mock_time
    ):
        refresher.side_effect = [
            Exception("source down"),
            _valid_metadata(mock_time),
        ]

        frozen = creds.get_frozen_credentials()
        assert frozen.access_key == 'ORIGINAL-ACCESS'
        assert refresher.call_count == 1

        creds._invalidate('ORIGINAL-ACCESS')
        frozen = creds.get_frozen_credentials()

        assert frozen.access_key == 'ORIGINAL-ACCESS'
        assert refresher.call_count == 1

        mock_time.return_value = DATE + timedelta(minutes=11)
        frozen = creds.get_frozen_credentials()

        assert frozen.access_key == 'NEW-ACCESS'
        assert refresher.call_count == 2

    def test_strict_credentials_invalidation_surfaces_refresh_failure(
        self, mock_time
    ):
        # Strict providers still invalidate, but they do not fall back to
        # stale credentials when the forced refresh fails.
        refresher = mock.Mock(
            side_effect=[
                Exception("source down"),
                _valid_metadata(mock_time),
            ]
        )
        creds = credentials._StrictRefreshableCredentials(
            'ORIGINAL-ACCESS',
            'ORIGINAL-SECRET',
            'ORIGINAL-TOKEN',
            mock_time() + timedelta(hours=1),
            refresher,
            'custom-process',
            time_fetcher=mock_time,
        )

        frozen = creds.get_frozen_credentials()
        assert frozen.access_key == 'ORIGINAL-ACCESS'
        assert refresher.call_count == 0

        creds._invalidate('ORIGINAL-ACCESS')

        with pytest.raises(Exception, match='source down'):
            creds.get_frozen_credentials()
        assert refresher.call_count == 1

        frozen = creds.get_frozen_credentials()
        assert frozen.access_key == 'NEW-ACCESS'
        assert refresher.call_count == 2

    def test_refresh_lock_held_skips_invalidation(self, mock_time, refresher):
        refresher.return_value = _valid_metadata(mock_time)
        invalidate_provider_cache = mock.Mock()
        creds = _create_refreshable_credentials(
            mock_time,
            refresher=refresher,
            expires_in=timedelta(hours=1),
            invalidate_provider_cache=invalidate_provider_cache,
        )

        assert creds._refresh_lock.acquire(False)
        try:
            creds._invalidate('ORIGINAL-ACCESS')
        finally:
            creds._refresh_lock.release()

        frozen = creds.get_frozen_credentials()

        assert frozen.access_key == 'ORIGINAL-ACCESS'
        assert refresher.call_count == 0
        invalidate_provider_cache.assert_not_called()


class TestProviderCacheInvalidation:
    @pytest.fixture
    def assume_role_load_config(self):
        return mock.Mock(
            return_value={
                'profiles': {
                    'development': {
                        'role_arn': 'arn:aws:iam::123456789012:role/test-role',
                        'source_profile': 'source',
                    },
                    'source': {
                        'aws_access_key_id': 'SOURCE-ACCESS',
                        'aws_secret_access_key': 'SOURCE-SECRET',
                        'aws_session_token': 'SOURCE-TOKEN',
                    },
                }
            }
        )

    @pytest.fixture
    def web_identity_load_config(self):
        return mock.Mock(
            return_value={
                'profiles': {
                    'development': {
                        'role_arn': 'arn:aws:iam::123456789012:role/test-role',
                        'web_identity_token_file': '/tmp/token',
                    }
                }
            }
        )

    @pytest.fixture
    def web_identity_token_loader_cls(self):
        token_loader = mock.Mock(return_value='OIDC-TOKEN')
        return mock.Mock(return_value=token_loader)

    @pytest.fixture
    def sso_start_url(self):
        return 'https://test.awsapps.com/start'

    @pytest.fixture
    def sso_load_config(self, sso_start_url):
        return mock.Mock(
            return_value={
                'profiles': {
                    'sso-profile': {
                        'sso_start_url': sso_start_url,
                        'sso_region': 'us-east-1',
                        'sso_role_name': 'Administrator',
                        'sso_account_id': '1234567890',
                    }
                }
            }
        )

    @pytest.fixture
    def future_expiration(self):
        return datetime(2099, 1, 1, tzinfo=timezone.utc)

    @pytest.fixture
    def sso_token_cache(self, sso_start_url, future_expiration):
        access_token_expiry = future_expiration
        token_cache = {}
        utils.SSOTokenLoader(cache=token_cache).save_token(
            sso_start_url,
            {
                'accessToken': 'ACCESS-TOKEN',
                'expiresAt': access_token_expiry.strftime(
                    '%Y-%m-%dT%H:%M:%SUTC'
                ),
            },
        )
        return token_cache

    def test_assume_role_refreshes_source_credentials(
        self, assume_role_load_config, future_expiration
    ):
        expiration = future_expiration
        client = mock.Mock()
        client.assume_role.side_effect = [
            {
                'Credentials': {
                    'AccessKeyId': 'OLD-ACCESS',
                    'SecretAccessKey': 'OLD-ACCESS-SECRET',
                    'SessionToken': 'OLD-ACCESS-TOKEN',
                    'Expiration': expiration,
                }
            },
            {
                'Credentials': {
                    'AccessKeyId': 'NEW-ACCESS',
                    'SecretAccessKey': 'NEW-ACCESS-SECRET',
                    'SessionToken': 'NEW-ACCESS-TOKEN',
                    'Expiration': expiration,
                }
            },
        ]
        client_creator = mock.Mock(return_value=client)
        provider = credentials.AssumeRoleProvider(
            assume_role_load_config,
            client_creator,
            cache={},
            profile_name='development',
        )

        creds = provider.load()
        first = creds.get_frozen_credentials()
        creds._invalidate('OLD-ACCESS')
        second = creds.get_frozen_credentials()

        assert first.access_key == 'OLD-ACCESS'
        assert second.access_key == 'NEW-ACCESS'
        assert client.assume_role.call_count == 2

    def test_web_identity_refreshes_source_credentials(
        self,
        web_identity_load_config,
        web_identity_token_loader_cls,
        future_expiration,
    ):
        expiration = future_expiration
        client = mock.Mock()
        client.assume_role_with_web_identity.side_effect = [
            {
                'Credentials': {
                    'AccessKeyId': 'OLD-ACCESS',
                    'SecretAccessKey': 'OLD-ACCESS-SECRET',
                    'SessionToken': 'OLD-ACCESS-TOKEN',
                    'Expiration': expiration,
                }
            },
            {
                'Credentials': {
                    'AccessKeyId': 'NEW-ACCESS',
                    'SecretAccessKey': 'NEW-ACCESS-SECRET',
                    'SessionToken': 'NEW-ACCESS-TOKEN',
                    'Expiration': expiration,
                }
            },
        ]
        client_creator = mock.Mock(return_value=client)
        provider = credentials.AssumeRoleWithWebIdentityProvider(
            load_config=web_identity_load_config,
            client_creator=client_creator,
            profile_name='development',
            cache={},
            token_loader_cls=web_identity_token_loader_cls,
        )

        creds = provider.load()
        first = creds.get_frozen_credentials()
        creds._invalidate('OLD-ACCESS')
        second = creds.get_frozen_credentials()

        assert first.access_key == 'OLD-ACCESS'
        assert second.access_key == 'NEW-ACCESS'
        assert client.assume_role_with_web_identity.call_count == 2
        web_identity_token_loader_cls.assert_called_once_with('/tmp/token')

    def test_sso_refreshes_source_credentials(
        self, sso_load_config, sso_token_cache, future_expiration
    ):
        expiration = future_expiration
        client = mock.Mock()
        client.get_role_credentials.side_effect = [
            {
                'roleCredentials': {
                    'accessKeyId': 'OLD-ACCESS',
                    'secretAccessKey': 'OLD-ACCESS-SECRET',
                    'sessionToken': 'OLD-ACCESS-TOKEN',
                    'expiration': int(expiration.timestamp() * 1000),
                }
            },
            {
                'roleCredentials': {
                    'accessKeyId': 'NEW-ACCESS',
                    'secretAccessKey': 'NEW-ACCESS-SECRET',
                    'sessionToken': 'NEW-ACCESS-TOKEN',
                    'expiration': int(expiration.timestamp() * 1000),
                }
            },
        ]
        client_creator = mock.Mock(return_value=client)
        provider = credentials.SSOProvider(
            load_config=sso_load_config,
            client_creator=client_creator,
            profile_name='sso-profile',
            cache={},
            token_cache=sso_token_cache,
        )

        creds = provider.load()
        first = creds.get_frozen_credentials()
        creds._invalidate('OLD-ACCESS')
        second = creds.get_frozen_credentials()

        assert first.access_key == 'OLD-ACCESS'
        assert second.access_key == 'NEW-ACCESS'
        assert client.get_role_credentials.call_count == 2


class CredentialRefreshClock:
    def __init__(self, now=DATE):
        self._now = now

    def __call__(self):
        return self._now

    def advance(self, seconds):
        self._now += timedelta(seconds=seconds)


class CredentialRefreshLifecycleHarness:
    def __init__(self, test_case):
        self._test_case = test_case
        self._clock = CredentialRefreshClock()
        self._next_refresh_response = None
        self._next_lifetime_seconds = 3600
        self._refresh_count = 0
        self._refresh_backoff_seconds = test_case['given'].get(
            'refreshBackoffSeconds', 420
        )
        self._creds = self._create_credentials()

    def uniform_random(self, low, high):
        """Pins jittered backoff values so modeled cases stay deterministic."""
        if (low, high) == (300, 600):
            return self._refresh_backoff_seconds
        if (low, high) == (1, 5):
            return 5
        raise AssertionError(
            f"Unexpected random.uniform call with bounds {(low, high)}"
        )

    def run_step(self, step):
        step_type = step['type']
        if step_type == 'advanceTime':
            self._clock.advance(step['seconds'])
            return None
        if step_type == 'invalidate':
            self._creds._invalidate(step['rejectedAccessKeyId'])
            return None
        if step_type != 'getCredentials':
            raise AssertionError(f"Unknown step type: {step_type}")

        # Fresh-credential steps can override the lifetime returned by the
        # next refresh.
        self._next_lifetime_seconds = step.get('lifetimeSeconds', 3600)
        response = step.get('response')
        if response is None:
            self._next_refresh_response = None
        else:
            self._next_refresh_response = self._build_refresh_response(step)

        rate_limited = self._creds._in_refresh_backoff()
        had_cached_credentials = self._creds._frozen_credentials is not None
        previous_access_key = self._current_access_key()
        refresh_count = self._refresh_count
        try:
            frozen = self._creds.get_frozen_credentials()
        except Exception as error:
            source_contacted = self._refresh_count != refresh_count
            if self._next_refresh_response is not None and source_contacted:
                self._next_refresh_response = None
            return {
                'result': self._result_from_error(
                    error, had_cached_credentials
                ),
                'sourceContacted': source_contacted,
                'rateLimited': rate_limited,
            }

        source_contacted = self._refresh_count != refresh_count
        if self._next_refresh_response is not None and source_contacted:
            self._next_refresh_response = None
        result = 'cachedCredentials'
        if previous_access_key != frozen.access_key:
            result = 'newCredentials'
        actual = {
            'result': result,
            'sourceContacted': source_contacted,
            'rateLimited': rate_limited,
        }
        if result == 'newCredentials':
            actual['advisoryWindowSeconds'] = (
                self._creds._resolve_advisory_refresh_timeout()
            )
        return actual

    def _create_credentials(self):
        given = self._test_case['given']
        state = given['cachedCredentials']
        if state == 'none':
            creds = credentials.DeferredRefreshableCredentials(
                self._refresh_using,
                'iam-role',
                time_fetcher=self._clock,
            )
            # Deferred credentials do not accept refresh-window kwargs, so keep
            # the configured override on the instance for the shared resolver.
            creds._explicit_advisory_refresh_timeout = given.get(
                'configuredAdvisoryWindowSeconds'
            )
            return creds

        advisory_timeout = given.get('configuredAdvisoryWindowSeconds')
        access_key = given.get('accessKeyId', 'ORIGINAL-ACCESS')
        return credentials.RefreshableCredentials(
            access_key,
            'ORIGINAL-SECRET',
            'ORIGINAL-TOKEN',
            self._seed_expiry_time(state),
            self._refresh_using,
            'iam-role',
            time_fetcher=self._clock,
            advisory_timeout=advisory_timeout,
        )

    def _seed_expiry_time(self, state):
        """Returns an expiry time that places credentials in the requested state."""
        if state == 'valid':
            return self._clock() + timedelta(minutes=20)
        if state == 'advisory':
            return self._clock() + timedelta(minutes=4)
        if state == 'mandatory':
            return self._clock() + timedelta(seconds=30)
        if state == 'expired':
            return self._clock() - timedelta(seconds=30)
        raise AssertionError(f"Unknown cached credential state: {state}")

    def _refresh_using(self):
        if self._next_refresh_response is None:
            raise AssertionError(
                "Credential source was contacted unexpectedly"
            )
        self._refresh_count += 1
        return self._next_refresh_response()

    def _build_refresh_response(self, step):
        response_type = step['response']
        if response_type == 'freshCredentials':
            return self._fresh_credentials_response
        if response_type == 'staleCredentials':
            return self._stale_credentials_response
        if response_type == 'error':
            return self._recoverable_error_response
        if response_type == 'nonRecoverableError':
            return self._nonrecoverable_error_response
        raise AssertionError(f"Unknown refresh response: {response_type}")

    def _fresh_credentials_response(self):
        access_key = f'NEW-ACCESS-{self._refresh_count + 1}'
        expiry_time = self._clock() + timedelta(
            seconds=self._next_lifetime_seconds
        )
        return {
            'access_key': access_key,
            'secret_key': 'NEW-SECRET',
            'token': 'NEW-TOKEN',
            'expiry_time': expiry_time.isoformat(),
        }

    def _stale_credentials_response(self):
        return {
            'access_key': f'STALE-ACCESS-{self._refresh_count}',
            'secret_key': 'STALE-SECRET',
            'token': 'STALE-TOKEN',
            'expiry_time': self._clock().isoformat(),
        }

    def _recoverable_error_response(self):
        raise Exception("source down")

    def _nonrecoverable_error_response(self):
        raise _CacheableNonRecoverableError("reauth required")

    def _current_access_key(self):
        if self._creds._frozen_credentials is None:
            return None
        return self._creds._frozen_credentials.access_key

    def _result_from_error(self, error, had_cached_credentials):
        if credentials._is_nonrecoverable_refresh_error(
            self._creds.method, error
        ):
            return 'nonRecoverableError'
        if not had_cached_credentials:
            return 'noCredentialsError'
        raise AssertionError(
            f"Unexpected exception for modeled lifecycle case: {error!r}"
        )


class PausingRefresher:
    """Pauses a refresh so concurrent callers can be observed."""

    def __init__(self, response):
        self._response = response
        self.started = threading.Event()
        self.resume = threading.Event()
        self.call_count = 0

    def __call__(self):
        self.call_count += 1
        self.started.set()
        if not self.resume.wait(timeout=1):
            raise AssertionError("Timed out waiting to resume refresh")
        return self._response


class CredentialFetchThread(threading.Thread):
    """Fetches frozen credentials on a background thread."""

    def __init__(self, creds):
        super().__init__()
        self._creds = creds
        self.frozen_credentials = None
        self.error = None

    def run(self):
        try:
            self.frozen_credentials = self._creds.get_frozen_credentials()
        except Exception as error:
            self.error = error


def _get_credential_refresh_test_id():
    if 'BOTOCORE_TEST_ID' not in os.environ:
        return None
    try:
        return int(os.environ['BOTOCORE_TEST_ID'])
    except ValueError:
        raise TypeError(
            "Invalid format for BOTOCORE_TEST_ID, should be a single integer."
        )


def _load_credential_refresh_lifecycle_cases():
    with open(CREDENTIAL_REFRESH_TEST_CASES_FILE, encoding='utf-8') as f:
        test_cases = json.load(f)

    requested_case_id = _get_credential_refresh_test_id()
    loaded_cases = []
    for case_id, test_case in enumerate(test_cases):
        if requested_case_id is not None and case_id != requested_case_id:
            continue
        loaded_cases.append(dict(test_case, case_id=case_id))
    return loaded_cases


def _credential_refresh_case_id(test_case):
    return f"{test_case['case_id']}: {test_case['documentation']}"


class TestCredentialRefreshLifecycle:
    @pytest.mark.parametrize(
        'test_case',
        _load_credential_refresh_lifecycle_cases(),
        ids=_credential_refresh_case_id,
    )
    def test_credential_refresh_lifecycle(self, test_case):
        harness = CredentialRefreshLifecycleHarness(test_case)
        with mock.patch(
            'botocore.credentials.random.uniform',
            side_effect=harness.uniform_random,
        ):
            for step in test_case['steps']:
                actual = harness.run_step(step)
                if actual is None:
                    continue
                for key, expected in step['expected'].items():
                    assert actual[key] == expected


class TestCredentialRefreshConcurrency:
    def test_advisory_refresh_concurrent_callers_reuse_cached_credentials(
        self,
    ):
        clock = CredentialRefreshClock()
        pausing_refresher = PausingRefresher(
            _valid_metadata(clock, expires_in=timedelta(hours=1))
        )
        refresher = mock.Mock(side_effect=pausing_refresher)
        creds = _create_refreshable_credentials(
            clock,
            refresher=refresher,
            expires_in=timedelta(seconds=90),
            advisory_timeout=120,
            mandatory_timeout=60,
        )

        refreshing_thread = CredentialFetchThread(creds)
        refreshing_thread.start()

        assert pausing_refresher.started.wait(timeout=1)

        cached = creds.get_frozen_credentials()

        assert cached.access_key == 'ORIGINAL-ACCESS'
        assert cached.secret_key == 'ORIGINAL-SECRET'
        assert cached.token == 'ORIGINAL-TOKEN'
        assert refreshing_thread.is_alive()

        pausing_refresher.resume.set()
        refreshing_thread.join(timeout=1)

        assert refreshing_thread.error is None
        assert refreshing_thread.frozen_credentials.access_key == 'NEW-ACCESS'
        assert refresher.call_count == 1

    @pytest.mark.parametrize(
        'expires_in',
        [timedelta(seconds=30), timedelta(seconds=-30)],
        ids=['mandatory', 'expired'],
    )
    def test_mandatory_refresh_concurrent_callers_wait_for_single_refresh(
        self, expires_in
    ):
        clock = CredentialRefreshClock()
        pausing_refresher = PausingRefresher(
            _valid_metadata(clock, expires_in=timedelta(hours=1))
        )
        refresher = mock.Mock(side_effect=pausing_refresher)
        creds = _create_refreshable_credentials(
            clock,
            refresher=refresher,
            expires_in=expires_in,
        )

        refresh_owner_thread = CredentialFetchThread(creds)
        waiting_thread = CredentialFetchThread(creds)
        refresh_owner_thread.start()

        assert pausing_refresher.started.wait(timeout=1)

        waiting_thread.start()
        waiting_thread.join(timeout=0.05)
        assert waiting_thread.is_alive()

        pausing_refresher.resume.set()
        refresh_owner_thread.join(timeout=1)
        waiting_thread.join(timeout=1)

        assert refresh_owner_thread.error is None
        assert waiting_thread.error is None
        assert (
            refresh_owner_thread.frozen_credentials.access_key == 'NEW-ACCESS'
        )
        assert waiting_thread.frozen_credentials.access_key == 'NEW-ACCESS'
        assert refresher.call_count == 1
