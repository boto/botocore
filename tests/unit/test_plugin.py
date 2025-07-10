# Copyright 2025 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
import logging
import sys

import pytest

from botocore.config import Config
from botocore.plugin import load_client_plugins
from tests import create_session, mock


class TestModule:
    def __init__(self):
        self.events_seen = []

    def initialize_client_plugin(self, client):
        client.meta.events.register(
            'before_operation',
            (lambda **kwargs: self.events_seen.append(kwargs)),
        )


class TestRegisteredPlugins:
    @pytest.fixture(autouse=True)
    def session(self):
        self.session = create_session()

    @pytest.fixture()
    def mock_sys_modules(self):
        self.test_module_in_package = TestModule()
        self.test_standalone_module = TestModule()
        with mock.patch.dict(sys.modules):
            sys.modules['test_plugin'] = self.test_standalone_module
            sys.modules['testpackage.test_plugin'] = (
                self.test_module_in_package
            )
            yield

    def test_register_standalone_plugin_module(self, mock_sys_modules):
        config = Config(botocore_client_plugins={'plugins': 'test_plugin'})
        client = self.session.create_client('s3', config=config)
        client.meta.events.emit('before_operation')
        assert len(self.test_standalone_module.events_seen) == 1

    def test_register_package_plugin_module(self, mock_sys_modules):
        config = Config(
            botocore_client_plugins={'plugin': 'testpackage.test_plugin'}
        )
        client = self.session.create_client('s3', config=config)
        client.meta.events.emit('before_operation')
        assert len(self.test_module_in_package.events_seen) == 1

    def test_register_multiple_plugins(self, mock_sys_modules):
        plugins = {
            'plugin': 'test_plugin',
            'plugin_2': 'testpackage.test_plugin',
        }
        config = Config(botocore_client_plugins={})
        client = self.session.create_client('s3', config=config)
        load_client_plugins(client, plugins)
        client.meta.events.emit('before_operation')
        assert len(self.test_standalone_module.events_seen) == 1
        assert len(self.test_module_in_package.events_seen) == 1

    def test_warning_emitted_on_failed_plugin_loading(self, caplog):
        caplog.set_level(logging.DEBUG)
        plugins = {'foo': 'plugin_that_does_not_exist'}
        warning_message = 'Failed to locate the following plugin module'
        config = Config(botocore_client_plugins={})
        client = self.session.create_client('s3', config=config)
        load_client_plugins(client, plugins)
        assert warning_message in caplog.text
