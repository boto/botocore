# Copyright 2023 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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
import logging
from contextlib import contextmanager
from datetime import datetime

import pytest

from botocore.config import Config
from botocore.stub import Stubber


@pytest.fixture
def useragent_cap_client(patched_session):
    @contextmanager
    def wrapper(*args, **kwargs):
        client = patched_session.create_client(*args, **kwargs)
        client.captured_user_agent_string = None

        def event_handler(params, **kwargs):
            client.captured_user_agent_string = params['headers']['User-Agent']

        client.meta.events.register_first(
            'before-call.*.*',
            event_handler,
            unique_id='useragent_cap_client',
        )

        yield client

        client.meta.events.unregister(
            'before-call.*.*',
            event_handler,
            unique_id='useragent_cap_client',
        )

    return wrapper


@pytest.fixture
def stubbed_list_buckets():
    """botocore.stubb.Stubber instance with a stubbed ``list_buckets`` method.

    Use with an S3 client, for example:

        client_s3 = session.create_client('s3')
        with stubbed_list_buckets(client_s3) as stubber:
            client_s3.list_buckets()
        assert stubber.assert_no_pending_responses()

    """
    response = {
        'Owner': {'ID': 'foo', 'DisplayName': 'bar'},
        'Buckets': [
            {'CreationDate': datetime(2099, 12, 31, 23, 59), 'Name': 'buck'}
        ],
    }

    @contextmanager
    def wrapper(client):
        with Stubber(client) as stubber:
            stubber.add_response('list_buckets', response, {})
            yield stubber

    return wrapper


def test_user_agent_from_config(useragent_cap_client, stubbed_list_buckets):
    client_cfg = Config(user_agent='my user agent str')
    with useragent_cap_client('s3', config=client_cfg) as client_s3:
        with stubbed_list_buckets(client_s3):
            client_s3.list_buckets()

    assert client_s3.captured_user_agent_string.startswith('my user agent str')


def test_user_agent_includes_extra(useragent_cap_client, stubbed_list_buckets):
    client_cfg = Config(user_agent_extra='extrastuff')
    with useragent_cap_client('s3', config=client_cfg) as client_s3:
        with stubbed_list_buckets(client_s3):
            client_s3.list_buckets()

    assert client_s3.captured_user_agent_string.endswith(' extrastuff')


def test_user_agent_includes_appid(useragent_cap_client, stubbed_list_buckets):
    client_cfg = Config(user_agent_appid='myappisbuiltwithbotocore')
    with useragent_cap_client('s3', config=client_cfg) as client_s3:
        with stubbed_list_buckets(client_s3):
            client_s3.list_buckets()

    uafields = client_s3.captured_user_agent_string.split(' ')
    assert 'app/myappisbuiltwithbotocore' in uafields


def test_user_agent_includes_all_config_values(
    useragent_cap_client, stubbed_list_buckets
):
    client_cfg = Config(
        user_agent='my user agent str',
        user_agent_extra='extrastuff',
        user_agent_appid='myappisbuiltwithbotocore',
    )
    with useragent_cap_client('s3', config=client_cfg) as client_s3:
        with stubbed_list_buckets(client_s3):
            client_s3.list_buckets()

    uafields = client_s3.captured_user_agent_string.split(' ')
    assert client_s3.captured_user_agent_string.startswith('my user agent str')
    assert 'app/myappisbuiltwithbotocore' in uafields
    assert client_s3.captured_user_agent_string.endswith(' extrastuff')


def test_user_agent_long_appid_gets_truncated(
    useragent_cap_client, stubbed_list_buckets, caplog
):
    # The maximum length for the user_agent_appid config is 50 characters
    sixtychars = '000000000011111111112222222222333333333344444444445555555555'
    client_cfg = Config(user_agent_appid=sixtychars)
    with useragent_cap_client('s3', config=client_cfg) as client_s3:
        with stubbed_list_buckets(client_s3):
            with caplog.at_level(logging.INFO):
                client_s3.list_buckets()

    # given string should be truncated to 50 characters
    uafields = client_s3.captured_user_agent_string.split(' ')
    assert 'app/00000000001111111111222222222233333333334444444444' in uafields
    # a warning-level log message should be raised
    assert (
        'The configured value for user_agent_appid exceeds the maximum length'
        in caplog.text
    )
    assert sixtychars in caplog.text


def test_user_agent_appid_gets_sanitized(
    useragent_cap_client, stubbed_list_buckets, caplog
):
    # Parentheses and the copyright symbol are not valid characters in the user
    # agent string
    badchars = 'Acme Inc(@2099)'
    client_cfg = Config(user_agent_appid=badchars)
    with useragent_cap_client('s3', config=client_cfg) as client_s3:
        with stubbed_list_buckets(client_s3):
            with caplog.at_level(logging.INFO):
                client_s3.list_buckets()

    # given string should be truncated to 50 characters
    uafields = client_s3.captured_user_agent_string.split(' ')
    assert 'app/Acme-Inc--2099-' in uafields
