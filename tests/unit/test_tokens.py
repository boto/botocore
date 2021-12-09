# Copyright 2022 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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
import pytest
import dateutil.parser

from tests import mock

from botocore.exceptions import (
    InvalidConfigError,
    TokenRetrievalError,
    SSOTokenLoadError,
)
from botocore.session import Session
from botocore.tokens import SSOTokenProvider


def parametrize(cases):
    return pytest.mark.parametrize(
        "test_case", cases, ids=[c["documentation"] for c in cases],
    )


sso_provider_resolution_cases = [
    {
        "documentation": "Full valid profile",
        "profile": {
            "sso_region": "us-east-1",
            "sso_start_url": "https://d-abc123.awsapps.com/start",
        },
        "resolves": True,
    },
    {
        "documentation": "Non-SSO profiles are skipped",
        "profile": {"region": "us-west-2"},
        "resolves": False,
    },
    {
        "documentation": "Only start URL is invalid",
        "profile": {"sso_start_url": "https://d-abc123.awsapps.com/start"},
        "resolves": False,
        "expectedException": InvalidConfigError,
    },
    {
        "documentation": "SSO Region only is skipped",
        "profile": {"sso_region": "us-east-1"},
        "resolves": False,
    },
]


def _create_mock_session(config):
    mock_session = mock.Mock(spec=Session)
    mock_session.get_config_variable.return_value = "default"
    mock_session.full_config = {"profiles": {"default": config}}
    return mock_session


@parametrize(sso_provider_resolution_cases)
def test_sso_token_provider_resolution(test_case):
    config = test_case["profile"]
    mock_session = _create_mock_session(config)
    resolver = SSOTokenProvider(mock_session)

    expected_exception = test_case.get("expectedException")
    if expected_exception is not None:
        with pytest.raises(expected_exception):
            auth_token = resolver.load_token()
        return

    auth_token = resolver.load_token()
    if test_case["resolves"]:
        assert auth_token is not None
    else:
        assert auth_token is None


sso_provider_refresh_cases = [
    {
        "documentation": "Valid token with all fields",
        "currentTime": "2021-12-25T13:30:00Z",
        "cachedToken": {
            "startUrl": "https://d-123.awsapps.com/start",
            "region": "us-west-2",
            "accessToken": "cachedtoken",
            "expiresAt": "2021-12-25T21:30:00Z",
            "clientId": "clientid",
            "clientSecret": "YSBzZWNyZXQ=",
            "registrationExpiresAt": "2022-12-25T13:30:00Z",
            "refreshToken": "cachedrefreshtoken",
        },
        "expectedToken": {
            "token": "cachedtoken",
            "expiration": "2021-12-25T21:30:00Z",
        },
    },
    {
        "documentation": "Minimal valid cached token",
        "currentTime": "2021-12-25T13:30:00Z",
        "cachedToken": {
            "accessToken": "cachedtoken",
            "expiresAt": "2021-12-25T21:30:00Z",
        },
        "expectedToken": {
            "token": "cachedtoken",
            "expiration": "2021-12-25T21:30:00Z",
        },
    },
    {
        "documentation": "Minimal expired cached token",
        "currentTime": "2021-12-25T13:30:00Z",
        "cachedToken": {
            "accessToken": "cachedtoken",
            "expiresAt": "2021-12-25T13:00:00Z",
        },
        "expectedException": TokenRetrievalError,
    },
    {
        "documentation": "Token missing the expiresAt field",
        "currentTime": "2021-12-25T13:30:00Z",
        "cachedToken": {"accessToken": "cachedtoken"},
        "expectedException": SSOTokenLoadError,
    },
    {
        "documentation": "Token missing the accessToken field",
        "currentTime": "2021-12-25T13:30:00Z",
        "cachedToken": {"expiresAt": "2021-12-25T13:00:00Z"},
        "expectedException": SSOTokenLoadError,
    },
    {
        "documentation": "Expired token refresh with refresh token",
        "currentTime": "2021-12-25T13:30:00Z",
        "cachedToken": {
            "startUrl": "https://d-123.awsapps.com/start",
            "region": "us-west-2",
            "accessToken": "cachedtoken",
            "expiresAt": "2021-12-25T13:00:00Z",
            "clientId": "clientid",
            "clientSecret": "YSBzZWNyZXQ=",
            "registrationExpiresAt": "2022-12-25T13:30:00Z",
            "refreshToken": "cachedrefreshtoken",
        },
        "refreshResponse": {
            "tokenType": "Bearer",
            "accessToken": "newtoken",
            "expiresIn": 28800,
            "refreshToken": "newrefreshtoken",
        },
        "expectedTokenWriteback": {
            "startUrl": "https://d-123.awsapps.com/start",
            "region": "us-west-2",
            "accessToken": "newtoken",
            "expiresAt": "2021-12-25T21:30:00Z",
            "clientId": "clientid",
            "clientSecret": "YSBzZWNyZXQ=",
            "registrationExpiresAt": "2022-12-25T13:30:00Z",
            "refreshToken": "newrefreshtoken",
        },
        "expectedToken": {
            "token": "newtoken",
            "expiration": "2021-12-25T21:30:00Z",
        },
    },
    {
        "documentation": "Expired token refresh without new refresh token",
        "currentTime": "2021-12-25T13:30:00Z",
        "cachedToken": {
            "startUrl": "https://d-123.awsapps.com/start",
            "region": "us-west-2",
            "accessToken": "cachedtoken",
            "expiresAt": "2021-12-25T13:00:00Z",
            "clientId": "clientid",
            "clientSecret": "YSBzZWNyZXQ=",
            "registrationExpiresAt": "2022-12-25T13:30:00Z",
            "refreshToken": "cachedrefreshtoken",
        },
        "refreshResponse": {
            "tokenType": "Bearer",
            "accessToken": "newtoken",
            "expiresIn": 28800,
        },
        "expectedTokenWriteback": {
            "startUrl": "https://d-123.awsapps.com/start",
            "region": "us-west-2",
            "accessToken": "newtoken",
            "expiresAt": "2021-12-25T21:30:00Z",
            "clientId": "clientid",
            "clientSecret": "YSBzZWNyZXQ=",
            "registrationExpiresAt": "2022-12-25T13:30:00Z",
            # TODO: Verify if we should preserve old refresh token
            "refreshToken": "cachedrefreshtoken",
        },
        "expectedToken": {
            "token": "newtoken",
            "expiration": "2021-12-25T21:30:00Z",
        },
    },
    {
        "documentation": "Expired token and expired client registration",
        "currentTime": "2021-12-25T13:30:00Z",
        "cachedToken": {
            "startUrl": "https://d-123.awsapps.com/start",
            "region": "us-west-2",
            "accessToken": "cachedtoken",
            "expiresAt": "2021-10-25T13:00:00Z",
            "clientId": "clientid",
            "clientSecret": "YSBzZWNyZXQ=",
            "registrationExpiresAt": "2021-11-25T13:30:00Z",
            "refreshToken": "cachedrefreshtoken",
        },
        "expectedException": TokenRetrievalError,
    },
]


@parametrize(sso_provider_refresh_cases)
def test_sso_token_provider_refresh(test_case):
    config = {
        "sso_region": "us-west-2",
        "sso_start_url": "https://d-123.awsapps.com/start",
    }
    cache_key = "2b829a45f04c9828cb45b7d092d8e4aa30818393"
    token_cache = {}

    # Prepopulate the token cache
    cached_token = test_case.pop("cachedToken", None)
    if cached_token:
        token_cache[cache_key] = cached_token

    mock_session = _create_mock_session(config)
    mock_sso_oidc = mock.Mock()
    mock_session.create_client.return_value = mock_sso_oidc

    refresh_response = test_case.pop("refreshResponse", None)
    mock_sso_oidc.create_token.return_value = refresh_response

    current_time = dateutil.parser.parse(test_case.pop("currentTime"))

    def _time_fetcher():
        return current_time

    resolver = SSOTokenProvider(
        mock_session, token_cache, time_fetcher=_time_fetcher,
    )

    auth_token = resolver.load_token()

    actual_exception = None
    try:
        actual_token = auth_token.get_frozen_token()
    except Exception as e:
        actual_exception = e

    expected_exception = test_case.pop("expectedException", None)
    if expected_exception is not None:
        assert isinstance(actual_exception, expected_exception)
    elif actual_exception is not None:
        raise actual_exception

    expected_token = test_case.pop("expectedToken", {})
    raw_token = expected_token.get("token")
    if raw_token is not None:
        assert actual_token.token == raw_token

    raw_expiration = expected_token.get("expiration")
    if raw_expiration is not None:
        expected_expiration = dateutil.parser.parse(raw_expiration)
        assert actual_token.expiration == expected_expiration

    expected_token_write_back = test_case.pop("expectedTokenWriteback", None)
    if expected_token_write_back:
        mock_sso_oidc.create_token.assert_called_with(
            grantType="refresh_token",
            clientId=cached_token["clientId"],
            clientSecret=cached_token["clientSecret"],
            refreshToken=cached_token["refreshToken"],
        )
        raw_expiration = expected_token_write_back["expiresAt"]
        # The in-memory cache doesn't serialize to JSON so expect a datetime
        expected_expiration = dateutil.parser.parse(raw_expiration)
        expected_token_write_back["expiresAt"] = expected_expiration
        assert expected_token_write_back == token_cache[cache_key]

    # Pop the documentation to ensure all test fields are handled
    test_case.pop("documentation")
    assert not test_case.keys(), "All fields of test case should be handled"
