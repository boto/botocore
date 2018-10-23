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


def create_botocore_default_config_mapping(chain_builder):
    return {
        'profile': chain_builder.build_config_chain(
            env_vars=['AWS_DEFAULT_PROFILE', 'AWS_PROFILE'],
        ),
        'region': chain_builder.build_config_chain(
            env_vars='AWS_DEFAULT_REGION',
            config_property='region',
            default=None,
        ),
        'data_path': chain_builder.build_config_chain(
            env_vars='AWS_DATA_PATH',
            config_property='data_path',
            default=None,
        ),
        'config_file': chain_builder.build_config_chain(
            env_vars='AWS_CONFIG_FILE',
            default='~/.aws/config',
        ),
        'ca_bundle': chain_builder.build_config_chain(
            env_vars='AWS_CA_BUNDLE',
            config_property='ca_bundle',
        ),
        'api_versions': chain_builder.build_config_chain(
            config_property='api_versions',
            default={},
        ),
        'credentials_file': chain_builder.build_config_chain(
            env_vars='AWS_SHARED_CREDENTIALS_FILE',
            default='~/.aws/credentials',
        ),
        'metadata_service_timeout': chain_builder.build_config_chain(
            env_vars='AWS_METADATA_SERVICE_TIMEOUT',
            config_property='metadata_service_timeout',
            default=1,
            cast=int,
        ),
        'metadata_service_num_attempts': chain_builder.build_config_chain(
            env_vars='AWS_METADATA_SERVICE_NUM_ATTEMPTS',
            config_property='metadata_service_num_attempts',
            default=1,
            cast=int,
        ),
        'parameter_validation': chain_builder.build_config_chain(
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
    def __init__(self, session, environ=None, methods=None):
        """Initialzie a DefaultConfigChainBuilder.

        :type session: :class:`botocore.session.Session`
        :param session: This is the session that should be used to look up
            values from the config file.

        :type environ: dict
        :param environ: A mapping to use for environment variables. If this
            is not provided it will default to use os.environ.

        :type methods: tuple
        :param methods: A tuple of methods to allow in the chain. This is for
            backwards compatibility, the tuple is of strs with the values
            instance, env, config. Omitting any of those values will skip
            adding the corresponding config loading method to the chain.
        """
        self._session = session
        if environ is None:
            environ = os.environ
        self._environ = environ
        self._methods = methods

    def build_config_chain(self, instance=True, env_vars=None,
                           config_property=None, default=None, cast=None):
        """Build a config chain following the standard botocore pattern.

        In botocore most of our config chains follow the the precendence:
        session_instance_variables, environment, config_file, default_value.

        This is a convenience function for creating a chain that follow
        that precendence.

        :type instance: bool
        :param instance: This indicates whether or not session instance
            variable lookup should be included in the config chain. By default
            it is True.

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
        if instance:
            providers.append(
                LazyProvider(
                    provider_function=lambda: OpenDictProvider(
                        source=self._session.instance_variables(),
                    ),
                )
            )
        if env_vars is not None:
            providers.append(
                ClosedDictProvider(
                    keys=env_vars,
                    source=self._environ,
                )
            )
        if config_property is not None:
            providers.append(
                LazyProvider(
                    provider_function=lambda: ClosedDictProvider(
                        keys=config_property,
                        source=self._session.get_scoped_config(),
                    ),
                )
            )
        if callable(default):
            default = LazyProvider(
                provider_function=lambda: ConstantProvider(value=default()),
            )
        elif default is not None:
            default = ConstantProvider(value=default)
        if default is not None:
            providers.append(default)

        return ChainProvider(providers=providers, cast=cast)

    def _should_include_method(self, name):
        if self._methods is None:
            return True
        return name in self._methods


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
        return provider.provide(logical_name)

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


class BaseProvider(object):
    """Base class for configuration value providers.

    A configuration provider has some method of providing a configuration
    value.
    """
    def provide(self, logical_name=None):
        """Provide a config value."""
        raise NotImplementedError('provide')


class ChainProvider(BaseProvider):
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

    def provide(self, logical_name=None):
        """Provide the value from the first provider to return non-None.

        Each provider in the chain has its provide method called. The first
        one in the chain to return a non-None value is the returned from the
        ChainProvider. When no non-None value is found, None is returned.

        :type logical_name: str
        :param logical_name: The logical name of the config value to retrieve.
        """
        for provider in self._providers:
            value = provider.provide(logical_name)
            if value is not None:
                return self._convert_type(value)
        return None

    def _convert_type(self, value):
        if self._cast is not None:
            return self._cast(value)
        return value

    def __repr__(self):
        return '[%s]' % ', '.join([str(p) for p in self._providers])


class ClosedDictProvider(BaseProvider):
    """This class loads config values from a dictionary source.

    Closed here refers to the behavior where the logical name that is passed to
    the provide method is ignored. This provider can only be used to look up
    the given names in the initializer.
    """
    def __init__(self, keys, source):
        """Initialize with the keys in the dictionary to check.

        :type keys: str or list
        :param keys: If this is a str, the key with that name will
            be loaded and returned. If this variable is
            a list, then it must be a list of str. The same process will be
            repeated for each string in the list, the first that returns non
            None will be returned.

        :type source: dict
        :param source: A source dictionary to fetch variables from.
        """
        self._keys = keys
        self._source = source

    def provide(self, logical_name=None):
        """Provide a config value from a source dictionary."""
        names = self._keys
        if not isinstance(names, list):
            names = [names]
        for name in names:
            if name in self._source:
                return self._source[name]
        return None

    def __repr__(self):
        return 'ClosedDictProvider(keys=%s, source=%s)' % (self._keys,
                                                           self._source)


class OpenDictProvider(BaseProvider):
    """This class loads config values from a dictionary source.

    Open here refers to the behavior where this provider can look up any key
    in the dictonary it is initialized with. It is not tied to a particular
    key like ClosedDictProvider.
    """
    def __init__(self, source):
        """Initialize with the keys in the dictionary to check.

        :type source: dict
        :param source: A source dictionary to fetch variables from.
        """
        self._source = source

    def provide(self, logical_name=None):
        """Provide a config value from a source.

        :type logical_name: str
        :param logical_name: The name of the key to look up in the dictionary.
            Since this is an OpenDictProvider it can be used to look
            up any key in its source dict.
        """
        value = self._source.get(logical_name)
        return value

    def __repr__(self):
        return 'OpenDictProvider(source=%s)' % self._source


class ConstantProvider(object):
    """This provider provides a constant value."""
    def __init__(self, value):
        self._value = value

    def provide(self, logical_name=None):
        """Provide the constant value given during initialization."""
        return self._value

    def __repr__(self):
        return 'ConstantProvider(value=%s)' % self._value


class LazyProvider(BaseProvider):
    """LazyProvider wraps another provider to lazily load it."""
    def __init__(self, provider_function):
        """Initialize LazyProvider.

        :type provider_function: callable
        :param provider_function: A callable that returns a provider. This will
            be called when the provide method is called on the LazyProvider.
            Then the returned provider will have it's provide method called,
            producing the final result that the LazyProvider returns.
        """
        self._provider_function = provider_function

    def provide(self, logical_name=None):
        """Provide a value loaded lazyily at provide time."""
        provider = self._provider_function()
        value = provider.provide(logical_name)
        return value

    def __repr__(self):
        return 'LazyProvider(provider_function=%s)' % self._provider_function
