# Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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
from tests import unittest
import mock
from nose.tools import assert_equal

import botocore
import botocore.session as session
from botocore.configprovider import ConfigProviderComponent
from botocore.configprovider import BaseConfigValueProvider
from botocore.configprovider import DictConfigValueProvider
from botocore.configprovider import ScopedConfigValueProvider
from botocore.configprovider import ConstantValueProvider
from botocore.configprovider import ChainProvider
from botocore.configprovider import DefaultConfigChainBuilder


class TestDefaultConfigChainBuilder(unittest.TestCase):
    def assert_chain_does_provide(self, instance_map, environ_map, config_map,
                                  build_config_chain_args,
                                  expected_value):
        fake_session = mock.Mock(spec=session.Session)
        fake_session.get_scoped_config.return_value = config_map
        fake_session.instance_variables.return_value = instance_map
        builder = DefaultConfigChainBuilder(fake_session, environ=environ_map)
        chain = builder.build_config_chain(**build_config_chain_args)
        value = chain.provide()
        self.assertEqual(value, expected_value)

    def test_chain_builder_can_provide_instance(self):
        self.assert_chain_does_provide(
            instance_map={'foo': 'bar'},
            environ_map={},
            config_map={},
            build_config_chain_args={
                'instance_var': 'foo',
            },
            expected_value='bar',
        )

    def test_chain_builder_can_provide_env_var(self):
        self.assert_chain_does_provide(
            instance_map={},
            environ_map={'FOO': 'bar'},
            config_map={},
            build_config_chain_args={
                'env_vars': 'FOO',
            },
            expected_value='bar',
        )

    def test_chain_builder_can_provide_config_var(self):
        self.assert_chain_does_provide(
            instance_map={},
            environ_map={},
            config_map={'foo': 'bar'},
            build_config_chain_args={
                'config_property': 'foo',
            },
            expected_value='bar',
        )

    def test_chain_builder_can_provide_default(self):
        self.assert_chain_does_provide(
            instance_map={},
            environ_map={},
            config_map={},
            build_config_chain_args={
                'default': 'bar'
            },
            expected_value='bar',
        )

    def test_chain_provider_does_follow_priority_instance_var(self):
        self.assert_chain_does_provide(
            instance_map={'instance_var': 'qux'},
            environ_map={'ENV_VAR': 'foo'},
            config_map={'config_key': 'bar'},
            build_config_chain_args={
                'instance_var': 'instance_var',
                'env_vars': 'ENV_VAR',
                'config_property': 'config_key',
                'default': 'baz',
            },
            expected_value='qux',
        )

    def test_chain_provider_does_follow_priority_env_var(self):
        self.assert_chain_does_provide(
            instance_map={'wrong_instance_var': 'qux'},
            environ_map={'ENV_VAR': 'foo'},
            config_map={'config_key': 'bar'},
            build_config_chain_args={
                'instance_var': 'instance_var',
                'env_vars': 'ENV_VAR',
                'config_property': 'config_key',
                'default': 'baz',
            },
            expected_value='foo',
        )

    def test_chain_provider_does_follow_priority_config(self):
        self.assert_chain_does_provide(
            instance_map={'wrong_instance_var': 'qux'},
            environ_map={'WRONG_ENV_VAR': 'foo'},
            config_map={'config_key': 'bar'},
            build_config_chain_args={
                'instance_var': 'instance_var',
                'env_vars': 'ENV_VAR',
                'config_property': 'config_key',
                'default': 'baz',
            },
            expected_value='bar',
        )

    def test_chain_provider_does_follow_priority_default(self):
        self.assert_chain_does_provide(
            instance_map={'wrong_instance_var': 'qux'},
            environ_map={'WRONG_ENV_VAR': 'foo'},
            config_map={'wrong_config_key': 'baz'},
            build_config_chain_args={
                'instance_var': 'instance_var',
                'env_vars': 'ENV_VAR',
                'config_property': 'config_key',
                'default': 'baz',
            },
            expected_value='baz',
        )


class TestConfigProviderComponent(unittest.TestCase):
    def test_does_provide_none_if_no_variable_exists(self):
        provider = ConfigProviderComponent()
        value = provider.get_config_variable('fake_variable')
        self.assertIsNone(value)

    def test_does_provide_value_if_variable_exists(self):
        mock_value_provider = mock.Mock(spec=BaseConfigValueProvider)
        mock_value_provider.provide.return_value = 'foo'
        provider = ConfigProviderComponent(mapping={
            'fake_variable': mock_value_provider,
        })
        value = provider.get_config_variable('fake_variable')
        self.assertEqual(value, 'foo')

    def test_provided_value_is_cached(self):
        mock_value_provider = mock.Mock(spec=BaseConfigValueProvider)
        mock_value_provider.provide.return_value = 'foo'
        provider = ConfigProviderComponent(mapping={
            'fake_variable': mock_value_provider,
        })
        value = provider.get_config_variable('fake_variable')
        self.assertEqual(value, 'foo')

        # Change the returned value to bar instead of foo. The value returned
        # from the ConfigProviderComponent should still be the cached foo from
        # before.
        mock_value_provider.provide.return_value = 'bar'
        self.assertEqual(value, 'foo')

    def test_can_set_variable(self):
        provider = ConfigProviderComponent()
        provider.set_config_variable('fake_variable', 'foo')
        value = provider.get_config_variable('fake_variable')
        self.assertEquals(value, 'foo')

    def test_set_variable_does_override_cache(self):
        mock_value_provider = mock.Mock(spec=BaseConfigValueProvider)
        mock_value_provider.provide.return_value = 'foo'
        provider = ConfigProviderComponent(mapping={
            'fake_variable': mock_value_provider,
        })
        value = provider.get_config_variable('fake_variable')
        self.assertEqual(value, 'foo')

        provider.set_config_variable('fake_variable', 'bar')
        value = provider.get_config_variable('fake_variable')
        self.assertEqual(value, 'bar')


class TestDictConfigValueProvider(unittest.TestCase):
    def assert_does_provide(self, names, source, expected_value):
        provider = DictConfigValueProvider(
            names=names,
            source=source,
        )
        value = provider.provide()
        self.assertEquals(value, expected_value)

    def test_does_provide_none_if_no_variable_exists(self):
        self.assert_does_provide(
            names='FOO',
            source={},
            expected_value=None,
        )

    def test_does_provide_value_if_variable_exists(self):
        self.assert_does_provide(
            names='FOO',
            source={
                'FOO': 'bar',
            },
            expected_value='bar',
        )

    def test_does_provide_none_if_no_variable_exists_in_list(self):
        self.assert_does_provide(
            names=['FOO'],
            source={},
            expected_value=None,
        )

    def test_does_provide_value_if_variable_exists_in_list(self):
        self.assert_does_provide(
            names=['FOO'],
            source={
                'FOO': 'bar',
            },
            expected_value='bar',
        )

    def test_does_provide_first_non_none_value_first(self):
        self.assert_does_provide(
            names=['FOO', 'BAR'],
            source={
                'FOO': 'baz',
            },
            expected_value='baz',
        )

    def test_does_provide_first_non_none_value_second(self):
        self.assert_does_provide(
            names=['FOO', 'BAR'],
            source={
                'BAR': 'baz',
            },
            expected_value='baz',
        )

    def test_does_provide_none_if_all_list_variables_are_none(self):
        self.assert_does_provide(
            names=['FOO', 'BAR'],
            source={},
            expected_value=None,
        )

    def test_does_provide_first_value_when_both_exist(self):
        self.assert_does_provide(
            names=['FOO', 'BAR'],
            source={
                'FOO': 'baz',
                'BAR': 'buz',
            },
            expected_value='baz',
        )


class TestScopedConfigValueProvider(unittest.TestCase):
    def assert_provides_value(self, source, name, expected_value):
        dict_loader = mock.Mock(autospec=True)
        dict_loader.return_value = source
        provider = ScopedConfigValueProvider(
            name=name,
            scoped_config_method=dict_loader
        )
        value = provider.provide()
        self.assertEqual(value, expected_value)

    def test_can_provide_value(self):
        self.assert_provides_value(
            source={'foo': 'bar'},
            name='foo',
            expected_value='bar',
        )

    def test_does_provide_none_if_value_not_in_dict(self):
        self.assert_provides_value(
            source={},
            name='foo',
            expected_value=None,
        )


def _make_provider_that_returns(return_value):
    provider = mock.Mock(spec=BaseConfigValueProvider)
    provider.provide.return_value = return_value
    return provider


def _make_providers_that_return(return_values):
    mocks = []
    for return_value in return_values:
        provider = _make_provider_that_returns(return_value)
        mocks.append(provider)
    return mocks


def assert_chain_does_provide(providers, expected_value):
    provider = ChainProvider(
        providers=providers,
    )
    value = provider.provide()
    assert_equal(value, expected_value)


def test_chain_provider():
    # Each case is a tuple with the first element being the return values
    # from the providers in the ChainProvider in order. The second value is the
    # expected return value from the ChainProvider.
    cases = [
        (None, []),
        (None, [None]),
        ('foo', ['foo']),
        ('foo', ['foo', 'bar']),
        ('bar', [None, 'bar']),
        ('foo', ['foo', None]),
        ('baz', [None, None, 'baz']),
        ('bar', [None, 'bar', None]),
        ('foo', ['foo', 'bar', None]),
        ('foo', ['foo', 'bar', 'baz']),
    ]
    for case in cases:
        yield assert_chain_does_provide, \
            _make_providers_that_return(case[1]), \
            case[0]


class TestChainProvider(unittest.TestCase):
    def test_can_cast_provided_value(self):
        chain_provider = ChainProvider(
            providers=_make_providers_that_return(['1']),
            cast=int,
        )
        value = chain_provider.provide()
        self.assertIsInstance(value, int)
        self.assertEqual(value, 1)


class TestConstantValueProvider(unittest.TestCase):
    def test_can_provide_value(self):
        provider = ConstantValueProvider(value='foo')
        value = provider.provide()
        self.assertEqual(value, 'foo')
