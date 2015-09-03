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
import binascii
import platform
import select
from subprocess import Popen, PIPE


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


def skip_unless_has_memory_collection(cls):
    """Class decorator to skip tests that require memory collection.

    Any test that uses memory collection (such as the resource leak tests)
    can decorate their class with skip_unless_has_memory_collection to
    indicate that if the platform does not support memory collection
    the tests should be skipped.
    """
    if platform.system() not in ['Darwin', 'Linux']:
        return unittest.skip('Memory tests only supported on mac/linux.')(cls)
    return cls


def random_chars(num_chars):
    """Returns random hex characters.

    Useful for creating resources with random names.

    """
    return binascii.hexlify(os.urandom(int(num_chars / 2))).decode('ascii')


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


@skip_unless_has_memory_collection
class BaseClientDriverTest(unittest.TestCase):
    def setUp(self):
        self.driver = ClientDriver()
        self.driver.start()

    def cmd(self, *args):
        self.driver.cmd(*args)

    def send_cmd(self, *args):
        self.driver.send_cmd(*args)

    def record_memory(self):
        self.driver.record_memory()

    @property
    def memory_samples(self):
        return self.driver.memory_samples

    def tearDown(self):
        self.driver.stop()


class ClientDriver(object):
    CLIENT_SERVER = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'cmd-runner'
    )

    def __init__(self):
        self._popen = None
        self.memory_samples = []

    def _get_memory_with_ps(self, pid):
        # It would be better to eventually switch to psutil,
        # which should allow us to test on windows, but for now
        # we'll just use ps and run on POSIX platforms.
        command_list = ['ps', '-p', str(pid), '-o', 'rss']
        p = Popen(command_list, stdout=PIPE)
        stdout = p.communicate()[0]
        if not p.returncode == 0:
            raise RuntimeError("Could not retrieve memory")
        else:
            # Get the RSS from output that looks like this:
            # RSS
            # 4496
            return int(stdout.splitlines()[1].split()[0]) * 1024

    def record_memory(self):
        mem = self._get_memory_with_ps(self._popen.pid)
        self.memory_samples.append(mem)

    def start(self):
        """Start up the command runner process."""
        self._popen = Popen([sys.executable, self.CLIENT_SERVER],
                            stdout=PIPE, stdin=PIPE)

    def stop(self):
        """Shutdown the command runner process."""
        self.cmd('exit')
        self._popen.wait()

    def send_cmd(self, *cmd):
        """Send a command and return immediately.

        This is a lower level method than cmd().
        This method will instruct the cmd-runner process
        to execute a command, but this method will
        immediately return.  You will need to use
        ``is_cmd_finished()`` to check that the command
        is finished.

        This method is useful if you want to record attributes
        about the process while an operation is occurring.  For
        example, if you want to instruct the cmd-runner process
        to upload a 1GB file to S3 and you'd like to record
        the memory during the upload process, you can use
        send_cmd() instead of cmd().

        """
        cmd_str = ' '.join(cmd) + '\n'
        cmd_bytes = cmd_str.encode('utf-8')
        self._popen.stdin.write(cmd_bytes)
        self._popen.stdin.flush()

    def is_cmd_finished(self):
        rlist = [self._popen.stdout.fileno()]
        result = select.select(rlist, [], [], 0.01)
        if result[0]:
            return True
        return False

    def cmd(self, *cmd):
        """Send a command and block until it finishes.

        This method will send a command to the cmd-runner process
        to run.  It will block until the cmd-runner process is
        finished executing the command and sends back a status
        response.

        """
        self.send_cmd(*cmd)
        result = self._popen.stdout.readline().strip()
        if result != b'OK':
            raise RuntimeError(
                "Error from command '%s': %s" % (cmd, result))
