import sys

import pytest

from botocore import utils
from botocore.session import get_session
from tests import mock


class TestPluginModule:
    """A mock plugin module for testing client plugin loading."""

    def __init__(self):
        self.events_seen = []

    def initialize_client_plugin(self, client):
        client.meta.events.register('before-call', self.increment_calls)

    def increment_calls(self, **kwargs):
        self.events_seen.append(kwargs)


class RecursivePluginModule:
    def initialize_client_plugin(self, client):
        client.meta.events.register('before-call.s3.*', self.create_client)

    def create_client(self, **kwargs):
        session = get_session()
        client = utils.create_nested_client(
            session, "s3", region_name="us-west-2"
        )
        client.list_buckets()


@pytest.fixture
def test_plugin():
    """Fixture to create and register test plugin module in sys.modules."""
    module = TestPluginModule()
    sys.modules['test_plugin'] = module
    yield module
    sys.modules.pop('test_plugin', None)


@pytest.fixture
def recursive_plugin():
    """Fixture to create and register recursive plugin module in sys.modules."""
    module = RecursivePluginModule()
    sys.modules['recursive_plugin'] = module
    yield module
    sys.modules.pop('recursive_plugin', None)


@pytest.fixture(autouse=True)
def restore_sys_modules(request):
    """
    Restore sys.modules after each test for isolation.

    This fixture is autouse for this file, so any test that modifies sys.modules
    will not leak changes to other tests.
    """
    old_modules = sys.modules.copy()
    yield
    sys.modules.clear()
    sys.modules.update(old_modules)


class TestPluginConfig:
    def test_environment_variable(self, test_plugin):
        """Tests that plugin is loaded and event registered via env variable."""
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
            assert len(test_plugin.events_seen) == 1
            assert isinstance(test_plugin.events_seen[0], dict)

    def test_plugin_not_loaded_without_env(self, test_plugin):
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
            assert test_plugin.events_seen == []

    def test_multiple_plugins_and_malformed(self):
        """Tests that multiple plugins are loaded and a malformed one is skipped."""
        plugin1 = TestPluginModule()
        plugin2 = TestPluginModule()
        sys.modules['test_plugin1'] = plugin1
        sys.modules['test_module.test_plugin2'] = plugin2
        try:
            with (
                mock.patch(
                    'os.environ',
                    {
                        'AWS_ACCESS_KEY_ID': 'access_key',
                        "AWS_SECRET_ACCESS_KEY": "secret_key",
                        "BOTOCORE_EXPERIMENTAL__PLUGINS": (
                            "plugin1=test_plugin1,plugin2=test_module.test_plugin2,malformedplugin"
                        ),
                    },
                ),
                mock.patch(
                    'botocore.httpsession.URLLib3Session.send'
                ) as mock_send,
            ):
                session = get_session()
                client = session.create_client(
                    'dynamodb', region_name='us-east-1'
                )
                mock_send.return_value = mock.Mock(
                    status_code=200, headers={}, content=b''
                )
                client.list_tables()
                assert len(plugin1.events_seen) == 1
                assert len(plugin2.events_seen) == 1
        finally:
            sys.modules.pop('test_plugin1', None)
            sys.modules.pop('test_module.test_plugin2', None)

    def test_recursive_plugin_module(self, recursive_plugin):
        """Tests that a recursive plugin does not leak sys.modules."""
        with (
            mock.patch(
                'os.environ',
                {
                    'AWS_ACCESS_KEY_ID': 'access_key',
                    "AWS_SECRET_ACCESS_KEY": "secret_key",
                    "BOTOCORE_EXPERIMENTAL__PLUGINS": (
                        "recursive=recursive_plugin"
                    ),
                },
            ),
            mock.patch(
                'botocore.httpsession.URLLib3Session.send'
            ) as mock_send,
        ):
            session = get_session()
            client = session.create_client('s3', region_name='us-east-1')
            mock_send.return_value = mock.Mock(
                status_code=200, headers={}, content=b''
            )
            client.list_buckets()
