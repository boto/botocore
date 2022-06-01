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

import unittest
import zipfile
import zipimport

import botocore
from botocore.loaders import Loader


class ZippedBotocoreTestCase(unittest.TestCase):
    def setUp(self):
        self.session = botocore.session.get_session()

    def test_import(self):
        self.assertIsInstance(botocore.__loader__, zipimport.zipimporter)
        self.assertIn('botocore.zip/botocore/__init__.py', botocore.__file__)

    def test_BOTOCORE_ROOT(self):
        self.assertIsInstance(botocore.BOTOCORE_ROOT, zipfile.Path)

    def test_loader(self):
        loader = Loader()
        self.assertIsInstance(loader.BUILTIN_DATA_PATH, zipfile.Path)
        try:
            loader.load_data('endpoints')
        except Exception:
            self.fail()
        try:
            loader.load_service_model('s3', 'service-2')
        except Exception:
            self.fail()

    def test_client(self):
        try:
            client = self.session.create_client('s3', region_name='us-west-2')
        except Exception:
            self.fail()
        self.assertTrue(hasattr(client, 'list_buckets'))
