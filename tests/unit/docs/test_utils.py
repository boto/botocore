# Copyright 2015 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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
from tests import unittest
from tests.unit.docs import BaseDocsTest
from botocore.docs.utils import py_type_name
from botocore.docs.utils import py_default
from botocore.docs.utils import get_official_service_name


class TestPythonTypeName(unittest.TestCase):
    def test_structure(self):
        self.assertEqual('dict', py_type_name('structure'))

    def test_list(self):
        self.assertEqual('list', py_type_name('list'))

    def test_map(self):
        self.assertEqual('dict', py_type_name('map'))

    def test_string(self):
        self.assertEqual('string', py_type_name('string'))

    def test_character(self):
        self.assertEqual('string', py_type_name('character'))

    def test_blob(self):
        self.assertEqual('bytes', py_type_name('blob'))

    def test_timestamp(self):
        self.assertEqual('datetime', py_type_name('timestamp'))

    def test_integer(self):
        self.assertEqual('integer', py_type_name('integer'))

    def test_long(self):
        self.assertEqual('integer', py_type_name('long'))

    def test_float(self):
        self.assertEqual('float', py_type_name('float'))

    def test_double(self):
        self.assertEqual('float', py_type_name('double'))


class TestPythonDefault(unittest.TestCase):
    def test_structure(self):
        self.assertEqual('{...}', py_default('structure'))

    def test_list(self):
        self.assertEqual('[...]', py_default('list'))

    def test_map(self):
        self.assertEqual('{...}', py_default('map'))

    def test_string(self):
        self.assertEqual('\'string\'', py_default('string'))

    def test_blob(self):
        self.assertEqual('b\'bytes\'', py_default('blob'))

    def test_timestamp(self):
        self.assertEqual('datetime(2015, 1, 1)', py_default('timestamp'))

    def test_integer(self):
        self.assertEqual('123', py_default('integer'))

    def test_long(self):
        self.assertEqual('123', py_default('long'))

    def test_double(self):
        self.assertEqual('123.0', py_default('double'))


class TestGetOfficialServiceName(BaseDocsTest):
    def setUp(self):
        super(TestGetOfficialServiceName, self).setUp()
        self.service_model.metadata = {
            'serviceFullName': 'Official Name'
        }

    def test_no_short_name(self):
        self.assertEqual('Official Name',
                         get_official_service_name(self.service_model))

    def test_aws_short_name(self):
        self.service_model.metadata['serviceAbbreviation'] = 'AWS Foo'
        self.assertEqual('Official Name (Foo)',
                         get_official_service_name(self.service_model))

    def test_amazon_short_name(self):
        self.service_model.metadata['serviceAbbreviation'] = 'Amazon Foo'
        self.assertEqual('Official Name (Foo)',
                         get_official_service_name(self.service_model))

    def test_short_name_in_official_name(self):
        self.service_model.metadata['serviceFullName'] = 'The Foo Service'
        self.service_model.metadata['serviceAbbreviation'] = 'Amazon Foo'
        self.assertEqual('The Foo Service',
                         get_official_service_name(self.service_model))
