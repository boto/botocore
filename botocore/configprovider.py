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

class ConfigProvider(object):
    """The ConfigProvider object loads configuration values lazily."""
    def __init__(self, mapping=None):
        """Initialize a ConfigProvider.

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
        self._cache[logical_name] = value


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

    def append_provider(self, provider):
        """Append a new provider to the end of the chain.

        :type provider: Subclass of BaseConfigValueProvider
        :param provider: The new ConfigValueProvider to add to the end of the
            lookup chain.
        """
        self._providers.append(provider)

    def prepend_provider(self, provider):
        """Prepend a new provider to the beginning of the chain.

        :type provider: Subclass of BaseConfigValueProvider
        :param provider: The new ConfigValueProvider to prepend to the
            beginning of the lookup chain.
        """
        self._providers.insert(0, provider)

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
