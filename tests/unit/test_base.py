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

import mock

import botocore.session
import botocore.exceptions
import botocore.base


class TestConfig(BaseEnvVar):

    def setUp(self):
        super(TestConfig, self).setUp()
        data_path = os.path.join(os.path.dirname(__file__), 'data')
        self.environ['BOTO_DATA_PATH'] = data_path
        self.session = botocore.session.get_session()

    def test_data_not_found(self):
        self.assertRaises(botocore.exceptions.DataNotFoundError,
                          self.session.get_data, 'bar')

    def test_data_bad(self):
        self.assertRaises(botocore.exceptions.DataNotFoundError,
                          self.session.get_data, 'baz')

    def test_all_data(self):
        data = self.session.get_data('foo')
        self.assertTrue('test_key_1' in data)
        self.assertTrue('test_key_2' in data)

    def test_not_there(self):
        self.assertRaises(botocore.exceptions.DataNotFoundError,
                          self.session.get_data,
                          'foo/test_key_4')

    def test_sub_data(self):
        data = self.session.get_data('foo/test_key_2')
        self.assertEqual(len(data), 2)
        self.assertTrue('test_value_2_1' in data)
        self.assertTrue('test_value_2_2' in data)

    def test_sublist_data(self):
        data = self.session.get_data('foo/test_key_3/test_list_2')
        self.assertTrue('name' in data)
        self.assertEqual(data['name'], 'test_list_2')
        self.assertTrue('value' in data)
        self.assertEqual(data['value'], 'test_list_value_2')

    def test_subdir(self):
        data = self.session.get_data('sub/fie')
        self.assertEqual(data['test_key_1'], 'test_value_1')

    def test_subdir_not_found(self):
        self.assertRaises(botocore.exceptions.DataNotFoundError,
                          self.session.get_data, 'sub/foo')


class TestWindowsSearchPath(BaseEnvVar):
    def setUp(self):
        self.session = botocore.session.get_session()
        super(TestWindowsSearchPath, self).setUp()

    @mock.patch('os.pathsep', ';')
    def test_search_path_on_windows(self):
        # On windows, the search path is separated by ';' chars.
        self.environ['BOTO_DATA_PATH'] = 'c:\\path1;c:\\path2'
        # The bulitin botocore data path is added as the 0th element
        # so we're only interested inchecking the two that we've added.
        paths = botocore.base.get_search_path(self.session)[1:]
        self.assertEqual(paths, ['c:\\path1', 'c:\\path2'])


if __name__ == "__main__":
    unittest.main()
