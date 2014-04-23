# Copyright (c) 2012-2013 Mitch Garnaat http://garnaat.org/
# Copyright 2012-2014 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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
import os
import shlex
import copy

from six.moves import configparser

import botocore.exceptions


def get_config(config_filename):
    """Returns the parsed INI config contents.

    Each section name is a top level key, and a _path key is inserted whose
    value is the ``config_filename``.

    :returns: A dict with keys for each profile found in the config
        file and the value of each key being a dict containing name
        value pairs found in that profile.

    :raises: ConfigNotFound, ConfigParseError
    """
    config = {}
    path = config_filename
    if path is not None:
        path = os.path.expandvars(path)
        path = os.path.expanduser(path)
        if not os.path.isfile(path):
            raise botocore.exceptions.ConfigNotFound(path=path)
        cp = configparser.RawConfigParser()
        try:
            cp.read(path)
        except configparser.Error:
            raise botocore.exceptions.ConfigParseError(path=path)
        else:
            config['_path'] = path
            for section in cp.sections():
                config[section] = {}
                for option in cp.options(section):
                    config_value = cp.get(section, option)
                    if config_value.startswith('\n'):
                        # Then we need to parse the inner contents as
                        # hierarchical.  We support a single level
                        # of nesting for now.
                        try:
                            config_value = _parse_nested(config_value)
                        except ValueError:
                            raise botocore.exceptions.ConfigParseError(
                                path=path)
                    config[section][option] = config_value
    return config


def _parse_nested(config_value):
    # Given a value like this:
    # \n
    # foo = bar
    # bar = baz
    # We need to parse this into
    # {'foo': 'bar', 'bar': 'baz}
    parsed = {}
    for line in config_value.splitlines():
        line = line.strip()
        if not line:
            continue
        # The caller will catch ValueError
        # and raise an appropriate error
        # if this fails.
        key, value = line.split('=', 1)
        parsed[key.strip()] = value.strip()
    return parsed


def build_profile_map(parsed_ini_config):
    """Convert the parsed INI config into a profile map.

    The config file format requires that every profile except the
    default to be prepended with "profile", e.g.::

        [profile test]
        aws_... = foo
        aws_... = bar

        [profile bar]
        aws_... = foo
        aws_... = bar

        # This is *not* a profile
        [preview]
        otherstuff = 1

        # Neither is this
        [foobar]
        morestuff = 2

    The build_profile_map will take a parsed INI config file where each top
    level key represents a section name, and convert into a format where all
    the profiles are under a single top level "profiles" key, and each key in
    the sub dictionary is a profile name.  For example, the above config file
    would be converted from::

        {"profile test": {"aws_...": "foo", "aws...": "bar"},
         "profile bar": {"aws...": "foo", "aws...": "bar"},
         "preview": {"otherstuff": ...},
         "foobar": {"morestuff": ...},
         }

    into::

        {"profiles": {"test": {"aws_...": "foo", "aws...": "bar"},
                      "bar": {"aws...": "foo", "aws...": "bar"},
         "preview": {"otherstuff": ...},
         "foobar": {"morestuff": ...},
        }

    If there are no profiles in the provided parsed INI contents, then
    an empty dict will be the value associated with the ``profiles`` key.

    .. note::

        This will not mutate the passed in parsed_ini_config.  Instead it will
        make a deepcopy and return that value.

    """
    parsed_config = copy.deepcopy(parsed_ini_config)
    profiles = {}
    final_config = {}
    for key, values in parsed_config.items():
        if key.startswith("profile"):
            try:
                parts = shlex.split(key)
            except ValueError:
                continue
            if len(parts) == 2:
                profiles[parts[1]] = values
        elif key == 'default':
            # default section is special and is considered a profile
            # name but we don't require you use 'profile "default"'
            # as a section.
            profiles[key] = values
        else:
            final_config[key] = values
    final_config['profiles'] = profiles
    return final_config
