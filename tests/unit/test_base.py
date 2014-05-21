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

from tests import unittest, BaseSessionTest
import os

import mock

import botocore.session
import botocore.exceptions


class TestConfig(BaseSessionTest):

    def setUp(self):
        super(TestConfig, self).setUp()
        data_path = os.path.join(os.path.dirname(__file__), 'data')
        self.environ['BOTO_DATA_PATH'] = data_path

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
        data = self.session.get_data('foo')
        self.assertFalse('foo/test_key_4' in data)

    def test_sub_data(self):
        data = self.session.get_data('foo')
        self.assertEqual(len(data['test_key_2']), 2)
        self.assertTrue('test_value_2_1' in data['test_key_2'])
        self.assertTrue('test_value_2_2' in data['test_key_2'])

    def test_sublist_data(self):
        data = self.session.get_data('foo')
        sublist = data['test_key_3'][1]
        self.assertTrue('name' in sublist)
        self.assertEqual(sublist['name'], 'test_list_2')
        self.assertTrue('value' in sublist)
        self.assertEqual(sublist['value'], 'test_list_value_2')

    def test_subdir(self):
        data = self.session.get_data('sub/fie')
        self.assertEqual(data['test_key_1'], 'test_value_1')

    def test_subdir_not_found(self):
        self.assertRaises(botocore.exceptions.DataNotFoundError,
                          self.session.get_data, 'sub/foo')


if __name__ == "__main__":
    unittest.main()
