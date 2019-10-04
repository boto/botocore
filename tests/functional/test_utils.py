# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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
import os
import tempfile
import shutil
from tests import unittest

from botocore.utils import FileWebIdentityTokenLoader


class TestFileWebIdentityTokenLoader(unittest.TestCase):
    def setUp(self):
        super(TestFileWebIdentityTokenLoader, self).setUp()
        self.tempdir = tempfile.mkdtemp()
        self.token = 'totally.a.token'
        self.token_file = os.path.join(self.tempdir, 'token.jwt')
        self.write_token(self.token)

    def tearDown(self):
        shutil.rmtree(self.tempdir)
        super(TestFileWebIdentityTokenLoader, self).tearDown()

    def write_token(self, token, path=None):
        if path is None:
            path = self.token_file
        with open(path, 'w') as f:
            f.write(token)

    def test_can_load_token(self):
        loader = FileWebIdentityTokenLoader(self.token_file)
        token = loader()
        self.assertEqual(self.token, token)
