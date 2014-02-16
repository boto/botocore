#!/usr/bin/env
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

from tests import unittest, BaseEnvVar
import os
import botocore.session
import botocore.exceptions


def path(filename):
    return os.path.join(os.path.dirname(__file__), 'cfg', filename)


class TestConfig(BaseEnvVar):

    def setUp(self):
        super(TestConfig, self).setUp()
        self.env_vars = {
            'config_file': (None, 'FOO_CONFIG_FILE', None),
            'profile': (None, 'FOO_DEFAULT_PROFILE', None),
        }

    def test_config_not_found(self):
        self.environ['FOO_CONFIG_FILE'] = path('aws_config_notfound')
        session = botocore.session.get_session(self.env_vars)
        self.assertEqual(session.get_config(), {})

    def test_config_parse_error(self):
        self.environ['FOO_CONFIG_FILE'] = path('aws_config_bad')
        session = botocore.session.get_session(self.env_vars)
        self.assertRaises(botocore.exceptions.ConfigParseError,
                          session.get_config)

    def test_config(self):
        self.environ['FOO_CONFIG_FILE'] = path('aws_config')
        session = botocore.session.get_session(self.env_vars)
        session.get_config()
        self.assertEqual(len(session.available_profiles), 2)
        self.assertIn('default', session.available_profiles)
        self.assertIn('personal', session.available_profiles)

    def test_default_values_are_used_in_configs(self):
        env_vars = {'config_file': (
            None, 'FOO_CONFIG_FILE', path('aws_config'))}
        session = botocore.session.get_session(env_vars)
        config = session.get_config()
        self.assertEqual(config['aws_access_key_id'], 'foo')
        self.assertEqual(config['aws_secret_access_key'], 'bar')

    def test_env_vars_trump_defaults(self):
        env_vars = {'config_file': (
            None, 'FOO_CONFIG_FILE', path('aws_config'))}
        self.environ['FOO_CONFIG_FILE'] = path('aws_config_other')
        # aws_config has access/secret keys of foo/bar, while
        # aws_config_other has access/secret key of other_foo/other_bar,
        # which is what should be used by the session since env vars
        # trump the default value.
        session = botocore.session.get_session(env_vars)
        config = session.get_config()
        self.assertEqual(config['aws_access_key_id'], 'other_foo')
        self.assertEqual(config['aws_secret_access_key'], 'other_bar')

    def test_bad_profile(self):
        self.environ['FOO_CONFIG_FILE'] = path('aws_bad_profile')
        self.environ['FOO_DEFAULT_PROFILE'] = 'personal1'
        session = botocore.session.get_session(self.env_vars)
        config = session.get_config()
        profiles = session.available_profiles
        self.assertEqual(len(profiles), 3)
        self.assertIn('my profile', profiles)
        self.assertIn('personal1', profiles)
        self.assertIn('default', profiles)
        self.assertEqual(config, {'aws_access_key_id': 'access_personal1',
                                  'aws_secret_access_key': 'key_personal1'})

    def test_profile_cached_returns_same_values(self):
        self.environ['FOO_CONFIG_FILE'] = path('aws_bad_profile')
        self.environ['FOO_DEFAULT_PROFILE'] = 'personal1'
        session = botocore.session.get_session(self.env_vars)
        # First time is built from scratch.
        config = session.get_config()
        # Second time is cached.
        cached_config = session.get_config()
        # Both versions should be identical.
        self.assertEqual(config, cached_config)

    def test_nested_hierarchy_parsing(self):
        self.environ['FOO_CONFIG_FILE'] = path('aws_config_nested')
        session = botocore.session.get_session(self.env_vars)
        config = session.get_config()
        self.assertEqual(config['aws_access_key_id'], 'foo')
        self.assertEqual(config['region'], 'us-west-2')
        self.assertEqual(config['s3']['signature_version'], 's3v4')
        self.assertEqual(config['cloudwatch']['signature_version'], 'v4')

    def test_nested_bad_config(self):
        self.environ['FOO_CONFIG_FILE'] = path('aws_config_nested_bad')
        session = botocore.session.get_session(self.env_vars)
        with self.assertRaises(botocore.exceptions.ConfigParseError):
            cfg = session.get_config()


if __name__ == "__main__":
    unittest.main()
