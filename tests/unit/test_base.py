#!/usr/bin/env
# Copyright (c) 2012-2013 Mitch Garnaat http://garnaat.org/
# Copyright 2012-2013 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, dis-
# tribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the fol-
# lowing conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#
from tests import unittest, BaseEnvVar
import os

import mock

import botocore.session
import botocore.exceptions


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
