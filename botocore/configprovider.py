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
"""This module contains the inteface for controlling how configuration
is loaded.
"""
import os
import copy


def create_botocore_default_config_mapping(chain_builder):
    return {
        'profile': chain_builder.build_config_chain(
            instance_var='profile',
            env_vars=['AWS_DEFAULT_PROFILE', 'AWS_PROFILE'],
        ),
        'region': chain_builder.build_config_chain(
            instance_var='region',
            env_vars='AWS_DEFAULT_REGION',
            config_property='region',
            default=None,
        ),
        'data_path': chain_builder.build_config_chain(
            instance_var='data_path',
            env_vars='AWS_DATA_PATH',
            config_property='data_path',
            default=None
        ),
        'config_file': chain_builder.build_config_chain(
            instance_var='config_file',
            env_vars='AWS_CONFIG_FILE',
            default='~/.aws/config',
        ),
        'ca_bundle': chain_builder.build_config_chain(
            instance_var='ca_bundle',
            env_vars='AWS_CA_BUNDLE',
            config_property='ca_bundle',
        ),
        'api_versions': chain_builder.build_config_chain(
            instance_var='api_versions',
            config_property='api_versions',
            default={},
        ),
        'credentials_file': chain_builder.build_config_chain(
            instance_var='credentials_file',
            env_vars='AWS_SHARED_CREDENTIALS_FILE',
            default='~/.aws/credentials',
        ),
        'metadata_service_timeout': chain_builder.build_config_chain(
            instance_var='metadata_service_timeout',
            env_vars='AWS_METADATA_SERVICE_TIMEOUT',
            config_property='metadata_service_timeout',
            default=1,
            cast=int,
        ),
        'metadata_service_num_attempts': chain_builder.build_config_chain(
            instance_var='metadata_service_num_attempts',
            env_vars='AWS_METADATA_SERVICE_NUM_ATTEMPTS',
            config_property='metadata_service_num_attempts',
            default=1,
            cast=int,
        ),
        'parameter_validation': chain_builder.build_config_chain(
            instance_var='parameter_validation',
            config_property='parameter_validation',
            default=True,
            cast=bool,
        ),
    }


class DefaultConfigChainBuilder(object):
    """Common config builder.

    This is a convenience class to construct configuration chains that follow
    our most common pattern. This is to prevent ordering them incorrectly,
    and to make the config chain construction more readable.
    """
    def __init__(self, session, environ=None):
        """Initialzie a DefaultConfigChainBuilder.

        :type session: :class:`botocore.session.Session`
        :param session: This is the session that should be used to look up
            values from the config file.

        :type environ: dict
        :param environ: A mapping to use for environment variables. If this
            is not provided it will default to use os.environ.
        """
        self._session = session
        if environ is None:
            environ = copy.copy(os.environ)
        self._environ = environ

    def build_config_chain(self, instance_var=None, env_vars=None,
                           config_property=None, default=None, cast=None):
        """Build a config chain following the standard botocore pattern.

        In botocore most of our config chains follow the the precendence:
        environment, config_file, default_value.

        This is a convenience function for creating a chain that follows
        that precendence.

        :type instance_var: str
        :param instance_var: The insance variable to associate with this key.
            Instance variables are looked up in the session instance variable
            mapping.

        :type env_vars: str or list of str or None
        :param env_vars: One or more environment variable names to search for
            this value. They are searched in order. If it is None it will
            not be added to the chain.

        :type config_property: str or None
        :param config_property: The string name of the key in the config file
            for this config option. If it is None it will not be added to the
            chain.

        :type default: Any
        :param default: Any constant value to be returned. If this is a
            callable it will be treated as a lazy value, and the callable will
            be called when the value is needed.

        :type cast: None or callable
        :param cast: If this value is None then it has no affect on the return
            type. Otherwise, it is treated as a function that will cast our
            provided type.

        :rvalue: ConfigChain
        :returns: A ConfigChain that resolves in the order env_vars ->
            config_property -> default. Any values that were none are
            omitted form the chain.
        """
        providers = []
        if instance_var is not None:
            providers.append(
                ScopedConfigValueProvider(
                    name=instance_var,
                    scoped_config_method=self._session.instance_variables,
                )
            )
        if env_vars is not None:
            providers.append(
                DictConfigValueProvider(
                    names=env_vars,
                    source=self._environ
                )
            )
        if config_property is not None:
            providers.append(
                ScopedConfigValueProvider(
                    name=config_property,
                    scoped_config_method=self._session.get_scoped_config,
                )
            )
        if callable(default):
            default = LazyConstantValueProvider(source=default)
        elif default is not None:
            default = ConstantValueProvider(value=default)
        if default is not None:
            providers.append(default)

        return ChainProvider(providers=providers, cast=cast)


class ConfigProviderComponent(object):
    """The ConfigProviderComponent object loads configuration values lazily."""
    def __init__(self, mapping=None):
        """Initialize a ConfigProviderComponent.

        :type mapping: dict
        :param mapping: The mapping parameter is a map of string to a subclass
            of ConfigValueProvider. When a config variable is asked for via the
            get_config_variable method, the corresponding provider will be
            invoked to load the value.
        """
        if mapping is None:
            mapping = {}
        self._mapping = mapping
        self._cache = {}

    def get_config_variable(self, logical_name):
        """
        Retrieve the value associeated with the specified logical_name
        from the corresponding provider. If no value is found None will
        be returned.

        :type logical_name: str
        :param logical_name: The logical name of the session variable
            you want to retrieve.  This name will be mapped to the
            appropriate environment variable name for this session as
            well as the appropriate config file entry.

        :returns: value of variable or None if not defined.
        """
        if logical_name in self._cache:
            return self._cache[logical_name]
        if logical_name not in self._mapping:
            return None
        provider = self._mapping[logical_name]
        return provider.provide()

    def set_config_variable(self, logical_name, value):
        """Set a configuration variable to a specific value.

        By using this method, you can override the normal lookup
        process used in ``get_config_variable`` by explicitly setting
        a value.  Subsequent calls to ``get_config_variable`` will
        use the ``value``.  This gives you per-session specific
        configuration values.

        ::
            >>> # Assume logical name 'foo' maps to env var 'FOO'
            >>> os.environ['FOO'] = 'myvalue'
            >>> s.get_config_variable('foo')
            'myvalue'
            >>> s.set_config_variable('foo', 'othervalue')
            >>> s.get_config_variable('foo')
            'othervalue'

        :type logical_name: str
        :param logical_name: The logical name of the session variable
            you want to set.  These are the keys in ``SESSION_VARIABLES``.

        :param value: The value to associate with the config variable.
        """
        if value is None:
            self._cache.pop(logical_name, None)
        else:
            self._cache[logical_name] = value

    def update_mapping(self, new_mapping):
        """Update the config mapping.

        :type new_mapping: dict
        :param new_mapping: The new mapping of logical names to config
            providers. Each name in this map will be added to or override an
            existing mapping.
        """
        self._mapping.update(new_mapping)


class BaseConfigValueProvider(object):
    """Base class for configuration value providers.

    A configuration provider has some method of providing a configuration
    value.
    """
    def provide(self):
        raise NotImplementedError('provide')


class ConstantValueProvider(object):
    """This provider provides a constant value."""
    def __init__(self, value):
        self._value = value

    def provide(self):
        """Provide the constant value given during initialization."""
        return self._value


class DictConfigValueProvider(BaseConfigValueProvider):
    """This class loads config values from an environment variable."""
    def __init__(self, names, source):
        """Initialize with the environment variable names to check.

        :type environment_vars: str or list
        :param environment_vars: If this is a str, the environment variable
            with that name will be loaded and returned. If this variable is
            a list, then it must be a list of str. The same process will be
            repeated for each string in the list, the first that returns non
            None will be returned.

        :type source: dict
        :param source: A source dictionary to fetch vairables from.
        """
        self._names = names
        self._source = source

    def provide(self):
        """Provide a config value from a source."""
        names = self._names
        if not isinstance(names, list):
            names = [names]
        for name in names:
            if name in self._source:
                return self._source[name]
        return None


class ChainProvider(BaseConfigValueProvider):
    """This provider wraps one or more other providers.

    Each provider in the chain is called, the first one returning a non-None
    value is then returned.
    """
    def __init__(self, providers=None, cast=None):
        """Initalize a ChainProvider.

        :type providers: list
        :param providers: The initial list of providers to check for values
            when invoked.

        :type cast: None or callable
        :param cast: If this value is None then it has no affect on the return
            type. Otherwise, it is treated as a function that will cast our
            provided type.
        """
        if providers is None:
            providers = []
        self._providers = providers
        self._cast = cast

    def provide(self):
        """Provide the value from the first provider to return non-None.

        Each provider in the chain has its provide method called. The first
        one in the chain to return a non-None value is the returned from the
        ChainProvider. When no non-None value is found, None is returned.
        """
        for provider in self._providers:
            value = provider.provide()
            if value is not None:
                return self._convert_type(value)
        return None

    def _convert_type(self, value):
        if self._cast is not None:
            return self._cast(value)
        return value


class ScopedConfigValueProvider(BaseConfigValueProvider):
    def __init__(self, name, scoped_config_method):
        """Initialize ScopedConfigValueProvider

        :type name: str
        :param name: The name of the config value to load from the scoped
            config.

        :type scoped_config_method: callable
        :param scoped_config_method: A function that when called will return a
            scoped config.
        """
        self._name = name
        self._scoped_config_method = scoped_config_method

    def provide(self):
        """Provide a value from a scoped config.

        This method first calls the scoped_config_method given to load the
        scoped config. Once loaded it looks up the value in the config and
        reutrns it.
        """
        scoped_config = self._scoped_config_method()
        value = scoped_config.get(self._name)
        return value


class LazyConstantValueProvider(BaseConfigValueProvider):
    def __init__(self, source):
        self._source = source

    def provide(self):
        value = self._source()
        return value
