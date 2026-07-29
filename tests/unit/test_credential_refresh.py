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
"""

from datetime import datetime, timedelta

import pytest
from dateutil.tz import tzlocal

from botocore import credentials
from botocore.exceptions import CredentialRetrievalError
from tests import BaseEnvVar, IntegerRefresher, mock, unittest
from tests.unit.test_credentials import (
    TestEnvVar as _TestEnvVar,
)
from tests.unit.test_credentials import (
    TestProcessProvider as _TestProcessProvider,
)


@pytest.fixture(autouse=True)
def _enable_new_credential_refresh(monkeypatch):
    monkeypatch.setattr(credentials, 'DEFAULT_NEW_CREDENTIAL_REFRESH', True)


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
class TestEnvVarFlagOn(_TestEnvVar):
    pass


class TestProcessProviderFlagOn(_TestProcessProvider):
    pass


# ---------------------------------------------------------------------------
# Net-new tests: these cover backoff behavior that has no counterpart in the
# legacy code path. At GA they will be added to test_credentials.py.
# ---------------------------------------------------------------------------


@pytest.fixture
def refresher():
    return mock.Mock()


@pytest.fixture
def mock_time():
    return mock.Mock(return_value=datetime.now(tzlocal()))


@pytest.fixture
def creds(refresher, mock_time):
    # The expiry time is in the past so that accessing the credentials
    # triggers a refresh.
    return credentials.RefreshableCredentials(
        'ORIGINAL-ACCESS',
        'ORIGINAL-SECRET',
        'ORIGINAL-TOKEN',
        datetime.now(tzlocal()) - timedelta(minutes=30),
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
        'iam-role',
        time_fetcher=mock_time,
        **kwargs,
    )


# ---------------------------------------------------------------------------
# Refresh-window tests: these cover the advisory/mandatory defaults and their
# interactions with successful and failed refreshes.
# ---------------------------------------------------------------------------


def _assert_refresh_boundary(
    creds, mock_time, issued_at, expires_in, refresh_window
):
    expiry_time = issued_at + expires_in

    # Just outside the window: no refresh yet.
    mock_time.return_value = expiry_time - timedelta(
        seconds=refresh_window + 1
    )
    assert creds.refresh_needed() is False

    # Just inside the window: refresh needed.
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


def test_new_path_uses_one_minute_mandatory_window_by_default(mock_time):
    creds = _create_refreshable_credentials(mock_time)

    assert creds._resolve_mandatory_refresh_timeout() == 60


def test_explicit_refresh_windows_are_preserved_on_new_path(mock_time):
    issued_at = mock_time()
    expires_in = timedelta(minutes=2)
    creds = _create_refreshable_credentials(
        mock_time,
        expires_in=expires_in,
        advisory_timeout=45,
        mandatory_timeout=10,
    )

    _assert_refresh_boundary(creds, mock_time, issued_at, expires_in, 45)
    assert creds._resolve_mandatory_refresh_timeout() == 10


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


def test_refresh_failure_returns_cached(creds, refresher):
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


def test_refresh_is_retried_after_backoff(creds, refresher, mock_time):
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
    mock_time.return_value = datetime.now(tzlocal()) + timedelta(minutes=11)
    frozen = creds.get_frozen_credentials()
    assert refresher.call_count == 2
    assert frozen.access_key == 'NEW-ACCESS'


def test_refresh_failure_without_cached_creds_raises(mock_time):
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


def test_invalid_refresh_data_without_cached_creds_raises(mock_time):
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
