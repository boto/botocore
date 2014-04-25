# Copyright 2014 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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
"""Module for resolving variables.

There are three main criteria for the design of resolving variables:

1. Users should be able to add new variables to the resolver (i.e don't have a
fixed set of variables that can be resolved).

2. Users should be able to extend the variable resolution process.  While there
are built in variable resolvers (environment variables, config files, etc.), it
should be possible to add support for a new resolution process.

3. Users should be able to entirely replace this process with their own
resolver (have a documented interface that allows for alternate
implementations).

"""
import os
import botocore.config
import botocore.exceptions


def create_resolver(session_var_map, profile_name,
                    config_filenames):
    """

    :param session_var_map: The SessionVariables from the
        session object.  This is a dict of
        name: (config, env, default) pairs.

    """
    env_var_map = {}
    default_values = {}
    # Assume that the config names are the same as the logical name.
    for key, value in session_var_map.items():
        _, env_var, default = value
        env_var_map[key] = env_var
        default_values[key] = default

    environ_resolver = DictMapping(os.environ, env_var_map)
    config_resolver = ConfigVars(config_filenames=config_filenames,
                                 profile_name=profile_name)
    resolver = VariableResolver(
        ('environment', environ_resolver),
        ('configfile', config_resolver),
    )
    for key, value in default_values.items():
        resolver.declare_variable(key, default=value)
    return resolver


class VariableResolver(object):
    def __init__(self, *named_resolvers):
        self._name_to_resolver, self._resolvers = self._extract_resolvers(
            named_resolvers)
        self._known_variables = {}

    def _extract_resolvers(self, name_resolvers):
        # name_resolvers is a list of (name, resolver) pairs.
        mapping = {}
        resolvers = []
        for name, resolver in name_resolvers:
            mapping[name] = resolver
            resolvers.append((name, resolver))
        return mapping, resolvers

    def resolve_variable(self, name):
        for _, resolver in self._resolvers:
            value = resolver.resolve(name)
            if value is not None:
                return value
        # If none of the resolvers could resolve the variable
        # we can return a default value if one has been declared.
        return self._known_variables.get(name)

    def get_resolver(self, name):
        return self._name_to_resolver[name]

    def declare_variable(self, name, default=None):
        self._known_variables[name] = default

    def insert_after(self, name, name_resolver):
        # self._resolver is a list of (name, resolver) pairs.
        try:
            index = [n for n, _ in self._resolvers].index(name)
        except ValueError:
            raise ValueError("Unknown variable resolver: %s" % name)
        self._resolvers.insert(index + 1, name_resolver)
        self._name_to_resolver[name_resolver[0]] = name_resolver[1]


class DictMapping(object):
    def __init__(self, source_dict, mapping):
        self._source_dict = source_dict
        self._mapping = mapping

    def add_mapping(self, key, value):
        self._mapping[key] = value

    def resolve(self, name):
        if name in self._mapping:
            return self._source_dict.get(self._mapping[name])


class ConfigVars(object):
    """Load variables from configuration files scoped to a profile.
    """
    _NO_CONFIG_AVAILABLE = object()

    def __init__(self, config_filenames, profile_name, parser=None):
        self._config_filenames = config_filenames
        self._profile_name = profile_name
        if parser is None:
            parser=  botocore.config.multi_file_load_config
        self._parser = parser
        # The part of the config file scoped to the specified profile.
        self._loaded = None
        # The entire contents of the parsed config file.
        self._full_config = None

    def add_config_file(self, filename):
        self._config_filenames.append(filename)
        # Force a config reload.
        self._loaded = None
        self._full_config

    def resolve(self, name):
        if self._loaded is None:
            self._load_config()
        if self._loaded is self._NO_CONFIG_AVAILABLE:
            return None
        else:
            return self._loaded.get(name)

    def _load_config(self):
        try:
            full_config = self._parser(*self._config_filenames)
        except botocore.exceptions.ConfigNotFound:
            self._loaded = self._NO_CONFIG_AVAILABLE
            return
        self._full_config = full_config
        # If they explicitly specified a profile, it *has* to exist, otherwise
        # we raise an exception.
        if self._profile_name is not None and \
                self._profile_name not in full_config['profiles']:
            raise botocore.exceptions.ProfileNotFound(
                profile=self._profile_name)
        elif self._profile_name is None:
            self._loaded = full_config['profiles'].get('default', {})
        else:
            self._loaded = full_config['profiles'].get(self._profile_name, {})

    def get_scoped_config(self):
        # All of the config dict scoped to the current profile.
        if self._loaded is None:
            self._load_config()
        return self._loaded

    def get_full_config(self):
        # All of the config dict (not scoped to a profile).
        if self._loaded is None:
            self._load_config()
        return self._full_config


class InMemoryVars(object):
    def __init__(self, variables):
        self._vars = variables

    def resolve(self, name):
        return self._vars.get(name)

    def add_variable(self, name, value):
        self._vars[name] = value
