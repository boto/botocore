import shutil
import tempfile
import os
import nose
import sys
from tests import BaseSessionTest

class ZipTest(BaseSessionTest):
    def test_load_from_zip(self):
        fd, temp_path = tempfile.mkstemp(suffix='.zip')
        root, ext = os.path.splitext(temp_path)
        shutil.make_archive(root, 'zip', '../..')
        sys.path.insert(0, temp_path)
        super(ZipTest, self).setUp()
        self.region = 'us-west-2'
        self.client = self.session.create_client(
            's3', self.region)
        sys.path.remove(temp_path)
        os.close(fd)
        os.remove(temp_path)