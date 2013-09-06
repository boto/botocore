# Copyright (c) 2013 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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
import os

from botocore.exceptions import ApiVersionNotFound
from botocore.exceptions import DataNotFoundError
from botocore.loaders import Cache
from botocore.loaders import cachable
from botocore.loaders import JSONFileLoader
from botocore.loaders import Loader
import botocore.session

from tests import unittest, BaseEnvVar


class CacheTestCase(BaseEnvVar):
    def setUp(self):
        super(CacheTestCase, self).setUp()
        self.cache = Cache()

    def test_len(self):
        self.assertEqual(len(self.cache), 0)

        self.cache['whatever'] = 'something'
        self.assertEqual(len(self.cache), 1)

        self.cache['whatever'] = 'something'
        self.assertEqual(len(self.cache), 1)

        self.cache['another'] = 'thing'
        self.assertEqual(len(self.cache), 2)

    def test_contains(self):
        self.cache['whatever'] = 'something'
        self.assertTrue('whatever' in self.cache)
        self.assertFalse('another' in self.cache)

    def test_get(self):
        self.cache['abc'] = 123
        self.assertEqual(self.cache['abc'], 123)

        with self.assertRaises(KeyError):
            self.cache['def']

    def test_set(self):
        with self.assertRaises(KeyError):
            self.cache['a_thing']

        self.cache['a_thing'] = 'that_lives'
        self.assertEqual(self.cache['a_thing'], 'that_lives')

    def test_del(self):
        self.cache['a_thing'] = 'that_lives'
        self.cache['whatever'] = 'something'
        self.assertEqual(len(self.cache), 2)

        del self.cache['a_thing']
        self.assertEqual(len(self.cache), 1)

        # Make sure no exceptions are thrown.
        del self.cache['a_thing']
        self.assertEqual(len(self.cache), 1)

    def test_clear(self):
        self.cache['a_thing'] = 'that_lives'
        self.cache['whatever'] = 'something'
        self.assertEqual(len(self.cache), 2)

        self.cache.clear()
        self.assertEqual(len(self.cache), 0)


class JSONFileLoaderTestCase(BaseEnvVar):
    def setUp(self):
        super(JSONFileLoaderTestCase, self).setUp()
        self.data_path = os.path.join(os.path.dirname(__file__), 'data')
        self.file_loader = JSONFileLoader()

    def test_load_file(self):
        data = self.file_loader.load_file(
            os.path.join(self.data_path, 'foo.json')
        )
        self.assertEqual(len(data), 3)
        self.assertTrue('test_key_1' in data)


class LoaderTestCase(BaseEnvVar):
    def setUp(self):
        super(LoaderTestCase, self).setUp()
        self.data_path = os.path.join(os.path.dirname(__file__), 'data')
        self.environ['BOTO_DATA_PATH'] = self.data_path
        self.session = botocore.session.get_session()
        self.loader = Loader(session=self.session)

    def test_get_search_paths(self):
        paths = self.loader.get_search_paths()
        self.assertTrue(self.data_path in paths)

    def test_determine_latest_no_version(self):
        path = self.loader.determine_latest('someservice')
        self.assertEqual(path, 'someservice/2013-08-21')

    def test_determine_latest_with_version(self):
        path = self.loader.determine_latest(
            'someservice',
            api_version='2012-10-01'
        )
        self.assertEqual(path, 'someservice/2012-10-01')

    def test_determine_latest_with_version_the_wrong_way(self):
        with self.assertRaises(ApiVersionNotFound):
            self.loader.determine_latest('someservice/2012-10-01')

    def test_determine_latest_with_version_not_found(self):
        with self.assertRaises(ApiVersionNotFound):
            path = self.loader.determine_latest(
                'someservice',
                api_version='2010-02-02'
            )

    def test_get_data_plain_file(self):
        data = self.loader.get_data('foo')
        self.assertEqual(data['test_key_1'], 'test_value_1')

    def test_get_data_plain_file_nonexistant(self):
        with self.assertRaises(DataNotFoundError):
            data = self.loader.get_data('i_totally_dont_exist')

    def test_get_service_model_latest_without_version(self):
        data = self.loader.get_service_model('someservice')
        self.assertEqual(data['api_version'], '2013-08-21')

    def test_get_service_model_with_version(self):
        data = self.loader.get_service_model(
            'someservice',
            api_version='2012-10-01'
        )
        self.assertEqual(data['api_version'], '2012-10-01')

    def test_get_service_model_version_not_found(self):
        with self.assertRaises(ApiVersionNotFound):
            data = self.loader.get_service_model(
                'someservice',
                api_version='2010-02-02'
            )

    def test_list_available_services(self):
        avail = self.loader.list_available_services('')
        self.assertEqual(sorted(avail), [
            'aws',
            'someservice',
            'sub',
        ])

        aws_avail = self.loader.list_available_services('aws')
        self.assertTrue(len(aws_avail) > 10)
        self.assertTrue('ec2' in aws_avail)


if __name__ == "__main__":
    unittest.main()
