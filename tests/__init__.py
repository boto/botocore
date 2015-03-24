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

import os
import sys
import mock
import time
import random
import shutil
import contextlib
import tempfile


# The unittest module got a significant overhaul
# in 2.7, so if we're in 2.6 we can use the backported
# version unittest2.
if sys.version_info[:2] == (2, 6):
    import unittest2 as unittest
else:
    import unittest


import botocore.loaders
import botocore.session
_LOADER = botocore.loaders.Loader()


def create_session(**kwargs):
    # Create a Session object.  By default,
    # the _LOADER object is used as the loader
    # so that we reused the same models across tests.
    session = botocore.session.Session(**kwargs)
    data_path = session.get_config_variable('data_path')
    _LOADER.data_path = data_path or ''
    session.register_component('data_loader', _LOADER)
    session.set_config_variable('credentials_file', 'noexist/foo/botocore')
    return session


@contextlib.contextmanager
def temporary_file(mode):
    """This is a cross platform temporary file creation.

    tempfile.NamedTemporary file on windows creates a secure temp file
    that can't be read by other processes and can't be opened a second time.

    For tests, we generally *want* them to be read multiple times.
    The test fixture writes the temp file contents, the test reads the
    temp file.

    """
    temporary_directory = tempfile.mkdtemp()
    basename = 'tmpfile-%s-%s' % (int(time.time()), random.randint(1, 1000))
    full_filename = os.path.join(temporary_directory, basename)
    open(full_filename, 'w').close()
    try:
        with open(full_filename, mode) as f:
            yield f
    finally:
        shutil.rmtree(temporary_directory)


class BaseEnvVar(unittest.TestCase):
    def setUp(self):
        # Automatically patches out os.environ for you
        # and gives you a self.environ attribute that simulates
        # the environment.  Also will automatically restore state
        # for you in tearDown()
        self.environ = {}
        self.environ_patch = mock.patch('os.environ', self.environ)
        self.environ_patch.start()

    def tearDown(self):
        self.environ_patch.stop()


class BaseSessionTest(BaseEnvVar):
    """Base class used to provide credentials.

    This class can be used as a base class that want to use a real
    session class but want to be completely isolated from the
    external environment (including environment variables).

    This class will also set credential vars so you can make fake
    requests to services.

    """

    def setUp(self, **environ):
        super(BaseSessionTest, self).setUp()
        self.environ['AWS_ACCESS_KEY_ID'] = 'access_key'
        self.environ['AWS_SECRET_ACCESS_KEY'] = 'secret_key'
        self.environ['AWS_CONFIG_FILE'] = 'no-exist-foo'
        self.environ.update(environ)
        self.session = create_session()
        self.session.config_filename = 'no-exist-foo'
