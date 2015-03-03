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
import botocore.exceptions
from botocore.config import raw_config_parse, load_config


def path(filename):
    return os.path.join(os.path.dirname(__file__), 'cfg', filename)


class TestConfig(BaseEnvVar):

    def test_config_not_found(self):
        with self.assertRaises(botocore.exceptions.ConfigNotFound):
            loaded_config = raw_config_parse(path('aws_config_notfound'))

    def test_config_parse_error(self):
        filename = path('aws_config_bad')
        with self.assertRaises(botocore.exceptions.ConfigParseError):
            raw_config_parse(filename)

    def test_config(self):
        loaded_config = raw_config_parse(path('aws_config'))
        self.assertIn('default', loaded_config)
        self.assertIn('profile "personal"', loaded_config)

    def test_profile_map_conversion(self):
        loaded_config = load_config(path('aws_config'))
        self.assertIn('profiles', loaded_config)
        self.assertEqual(sorted(loaded_config['profiles'].keys()),
                         ['default', 'personal'])

    def test_bad_profiles_are_ignored(self):
        filename = path('aws_bad_profile')
        loaded_config = load_config(filename)
        self.assertEqual(len(loaded_config['profiles']), 3)
        profiles = loaded_config['profiles']
        self.assertIn('my profile', profiles)
        self.assertIn('personal1', profiles)
        self.assertIn('default', profiles)

    def test_nested_hierarchy_parsing(self):
        filename = path('aws_config_nested')
        loaded_config = load_config(filename)
        config = loaded_config['profiles']['default']
        self.assertEqual(config['aws_access_key_id'], 'foo')
        self.assertEqual(config['region'], 'us-west-2')
        self.assertEqual(config['s3']['signature_version'], 's3v4')
        self.assertEqual(config['cloudwatch']['signature_version'], 'v4')

    def test_nested_bad_config(self):
        filename = path('aws_config_nested_bad')
        with self.assertRaises(botocore.exceptions.ConfigParseError):
            loaded_config = load_config(filename)


if __name__ == "__main__":
    unittest.main()
