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

import os

import mock

from botocore.exceptions import ApiVersionNotFoundError
from botocore.exceptions import DataNotFoundError
from botocore.loaders import cachable
from botocore.loaders import JSONFileLoader
from botocore.loaders import Loader
import botocore.session

from tests import unittest, BaseEnvVar


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
        self.loader = Loader(data_path=self.environ['BOTO_DATA_PATH'])

        # Make sure the cache is clear.
        self.loader._cache.clear()

    def test_data_path_not_required(self):
        loader = Loader()
        self.assertEqual(loader.data_path, '')
        loader.data_path = 'foo:bar'
        self.assertEqual(loader.data_path, 'foo:bar')

    def test_get_search_paths(self):
        paths = self.loader.get_search_paths()
        self.assertTrue(self.data_path in paths)

    def test_determine_latest_no_version(self):
        path = self.loader.determine_latest('someservice')
        self.assertEqual(path, os.path.join('someservice',
                                            '2013-08-21.normal'))

    def test_determine_latest_with_version(self):
        path = self.loader.determine_latest(
            'someservice',
            api_version='2012-10-01'
        )
        self.assertEqual(path, os.path.join('someservice',
                                            '2012-10-01.normal'))

    def test_determine_latest_with_version_the_wrong_way(self):
        with self.assertRaises(ApiVersionNotFoundError):
            self.loader.determine_latest('someservice/2012-10-01')

    def test_determine_latest_with_version_not_found(self):
        with self.assertRaises(ApiVersionNotFoundError):
            path = self.loader.determine_latest(
                'someservice',
                api_version='2010-02-02'
            )

    def test_load_data_plain_file(self):
        data = self.loader.load_data('foo')
        self.assertEqual(data['test_key_1'], 'test_value_1')

    def test_load_data_plain_file_nonexistant(self):
        with self.assertRaises(DataNotFoundError):
            data = self.loader.load_data('i_totally_dont_exist')

    def test_load_service_model_latest_without_version(self):
        data = self.loader.load_service_model('someservice')
        self.assertEqual(data['api_version'], '2013-08-21')

    def test_load_service_model_with_version(self):
        data = self.loader.load_service_model(
            'someservice',
            api_version='2012-10-01'
        )
        self.assertEqual(data['api_version'], '2012-10-01')

    def test_load_service_model_version_not_found(self):
        with self.assertRaises(ApiVersionNotFoundError):
            data = self.loader.load_service_model(
                'someservice',
                api_version='2010-02-02'
            )

    def test_load_service_model_data_path_order(self):
        # There's an s3/ directory both in our custom BOTO_DATA_PATH
        # directory as well as in the botocore/data/ directory.
        # Our path should win since the default built in path is always
        # last.
        data = self.loader.load_service_model('aws/s3')
        self.assertTrue(data.get('WAS_OVERRIDEN_VIA_DATA_PATH'),
                        "S3 model was loaded from botocore's default "
                        "data path instead of from the BOTO_DATA_PATH"
                        " directory.")

    def test_list_available_services(self):
        avail = self.loader.list_available_services('')
        self.assertEqual(sorted(avail), [
            'aws',
            'aws',
            'someservice',
            'sub',
        ])

        aws_avail = self.loader.list_available_services('aws')
        self.assertTrue(len(aws_avail) > 10)
        self.assertTrue('ec2' in aws_avail)

    def test_load_data_overridden(self):
        self.overrides_path = os.path.join(
            os.path.dirname(__file__),
            'data_overrides'
        )
        self.environ['BOTO_DATA_PATH'] = "{0}{1}{2}".format(
            self.overrides_path,
            os.pathsep,
            self.data_path
        )
        loader = Loader(data_path=self.environ['BOTO_DATA_PATH'])
        # This should load the data the first data it finds.
        data = loader.load_service_model(
            'someservice',
            api_version='2012-10-01'
        )
        # An overridden key.
        self.assertEqual(data['api_version'], '2012-10-01')
        # A key unique to the base.
        self.assertEqual(data['something-else'], 'another')
        # Ensure a key present in other variants is not there.
        self.assertTrue('Purpose' not in data)

    @mock.patch('os.pathsep', ';')
    def test_search_path_on_windows(self):
        # On windows, the search path is separated by ';' chars.
        self.environ['BOTO_DATA_PATH'] = 'c:\\path1;c:\\path2'
        # The builtin botocore data path is added as the last element
        # so we're only interested in checking the two that we've added.
        loader = Loader(data_path=self.environ['BOTO_DATA_PATH'])
        paths = loader.get_search_paths()[:-1]
        self.assertEqual(paths, ['c:\\path1', 'c:\\path2'])


if __name__ == "__main__":
    unittest.main()
