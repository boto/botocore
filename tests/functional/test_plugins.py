import sys

import pytest

from botocore.session import get_session
from tests import mock


class DummyPluginModule:
    """A mock plugin module for testing client plugin loading."""

    def __init__(self):
        self.events_seen = []

    def initialize_client_plugin(self, client):
        client.meta.events.register('before-call', self.increment_calls)

    def increment_calls(self, **kwargs):
        self.events_seen.append(kwargs)


@pytest.fixture
def dummy_plugin():
    """Fixture to create and register dummy plugin module in sys.modules."""
    module = DummyPluginModule()
    sys.modules['dummy_plugin'] = module
    yield module


class TestPluginConfig:
    @pytest.fixture(autouse=True)
    def restore_sys_modules(self):
        """Restore sys.modules after each test for isolation."""
        old_modules = sys.modules.copy()
        yield
        sys.modules.clear()
        sys.modules.update(old_modules)

    def test_environment_variable(self, dummy_plugin):
        """Tests that plugin is loaded and event registered via env variable."""
        with (
            mock.patch(
                'os.environ',
                {
                    'AWS_ACCESS_KEY_ID': 'access_key',
                    "AWS_SECRET_ACCESS_KEY": "secret_key",
                    "BOTOCORE_EXPERIMENTAL__PLUGINS": "plugin_name=dummy_plugin",
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
            assert len(dummy_plugin.events_seen) == 1
            assert isinstance(dummy_plugin.events_seen[0], dict)

    def test_plugin_not_loaded_without_env(self, dummy_plugin):
        """Tests that plugin is not loaded if env var is not set."""
        with (
            mock.patch(
                'os.environ',
                {
                    'AWS_ACCESS_KEY_ID': 'access_key',
                    "AWS_SECRET_ACCESS_KEY": "secret_key",
                    # No BOTOCORE_EXPERIMENTAL__PLUGINS
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
            assert dummy_plugin.events_seen == []

    def test_multiple_plugins_and_malformed(self):
        """Tests that multiple plugins are loaded and a malformed one is skipped."""
        plugin1 = DummyPluginModule()
        plugin2 = DummyPluginModule()
        sys.modules['dummy_plugin1'] = plugin1
        sys.modules['dummy_module.dummy_plugin2'] = plugin2
        with (
            mock.patch(
                'os.environ',
                {
                    'AWS_ACCESS_KEY_ID': 'access_key',
                    "AWS_SECRET_ACCESS_KEY": "secret_key",
                    "BOTOCORE_EXPERIMENTAL__PLUGINS": (
                        "plugin1=dummy_plugin1,plugin2=dummy_module.dummy_plugin2,malformedplugin"
                    ),
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
            assert len(plugin1.events_seen) == 1
            assert len(plugin2.events_seen) == 1
