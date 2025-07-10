# Copyright 2025 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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

import sys

import pytest

from botocore.session import get_session
from tests import mock


class TestModule:
    def __init__(self):
        self.events_seen = []

    def initialize_client_plugin(self, client):
        client.meta.events.register('before-call', self.increment_calls)

    def increment_calls(self, **kwargs):
        self.events_seen.append(kwargs)


class TestPluginConfig:
    @pytest.fixture(autouse=True)
    def mock_sys_modules(self):
        self.test_module = TestModule()
        with mock.patch.dict(sys.modules):
            sys.modules['test_plugin'] = self.test_module
            yield

    def test_environment_variable(self):
        with (
            mock.patch(
                'os.environ',
                {
                    'AWS_ACCESS_KEY_ID': 'access_key',
                    "AWS_SECRET_ACCESS_KEY": "secret_key",
                    "BOTOCORE_EXPERIMENTAL__PLUGINS": "plugin_name=test_plugin",
                },
            ),
            mock.patch(
                'botocore.httpsession.URLLib3Session.send'
            ) as mock_send,
        ):
            session = get_session()
            client = session.create_client('dynamodb', region_name='us-east-1')
            mock_send.return_value = mock.Mock(
                status_code=200, headers={}, content=b''
            )
            client.list_tables()
            assert len(self.test_module.events_seen) == 1
