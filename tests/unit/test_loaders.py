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

import mock

from botocore.exceptions import DataNotFoundError
from botocore.loaders import JSONLoader
import botocore.session

from tests import unittest, BaseEnvVar


class JSONLoaderTestCase(BaseEnvVar):
    def setUp(self):
        super(JSONLoaderTestCase, self).setUp()
        data_path = os.path.join(os.path.dirname(__file__), 'data')
        self.environ['BOTO_DATA_PATH'] = data_path
        self.session = botocore.session.get_session()
        self.loader = JSONLoader(session=self.session)

    def test_determine_latest_plain_file(self):
        path = self.loader.determine_latest('foo')
        self.assertEqual(path, 'foo')

    def test_determine_latest_directory(self):
        path = self.loader.determine_latest('sub')
        self.assertEqual(path, 'sub')

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
        path = self.loader.determine_latest('someservice/2012-10-01')
        # We've tried to traverse to find it & didn't, so it just gets returned
        # for ``botocore.base`` to have a whack at it.
        self.assertEqual(path, 'someservice/2012-10-01')

    def test_determine_latest_with_version_not_found(self):
        path = self.loader.determine_latest(
            'someservice',
            api_version='2010-02-02'
        )
        # We just return it, even if it's wrong, to let ``botocore.base`` try
        # to find it (maybe it's a key or something).
        self.assertEqual(path, 'someservice/2010-02-02')

    def test_get_data_plain_file_no_version(self):
        data = self.loader.get_data('foo')
        self.assertEqual(data['test_key_1'], 'test_value_1')

    def test_get_data_plain_directory(self):
        data = self.loader.get_data('sub')
        self.assertEqual(data[0], 'fie')

    def test_get_data_latest_without_version(self):
        data = self.loader.get_data('someservice')
        self.assertEqual(data['api_version'], '2013-08-21')

    def test_get_data_with_version(self):
        data = self.loader.get_data('someservice', api_version='2012-10-01')
        self.assertEqual(data['api_version'], '2012-10-01')

    def test_get_data_with_version_not_found(self):
        with self.assertRaises(DataNotFoundError):
            data = self.loader.get_data('someservice', api_version='2010-02-02')


if __name__ == "__main__":
    unittest.main()
