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
import datetime
from io import BytesIO
from subprocess import Popen, PIPE

from dateutil.tz import tzlocal
# The unittest module got a significant overhaul
# in 2.7, so if we're in 2.6 we can use the backported
# version unittest2.
if sys.version_info[:2] == (2, 6):
    import unittest2 as unittest
else:
    import unittest

from nose.tools import assert_equal

import botocore.loaders
import botocore.session
from botocore.awsrequest import AWSResponse
from botocore.compat import six
from botocore.compat import urlparse
from botocore.compat import parse_qs
from botocore import utils
from botocore import credentials


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


def skip_if_windows(reason):
    """Decorator to skip tests that should not be run on windows.
    Example usage:
        @skip_if_windows("Not valid")
        def test_some_non_windows_stuff(self):
            self.assertEqual(...)
    """
    def decorator(func):
        return unittest.skipIf(
            platform.system() not in ['Darwin', 'Linux'], reason)(func)
    return decorator


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
    INJECT_DUMMY_CREDS = False

    def setUp(self):
        self.driver = ClientDriver()
        env = None
        if self.INJECT_DUMMY_CREDS:
            env = {'AWS_ACCESS_KEY_ID': 'foo',
                   'AWS_SECRET_ACCESS_KEY': 'bar'}
        self.driver.start(env=env)

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

    def start(self, env=None):
        """Start up the command runner process."""
        self._popen = Popen([sys.executable, self.CLIENT_SERVER],
                            stdout=PIPE, stdin=PIPE, env=env)

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


# This is added to this file because it's used in both
# the functional and unit tests for cred refresh.
class IntegerRefresher(credentials.RefreshableCredentials):
    """Refreshable credentials to help with testing.

    This class makes testing refreshable credentials easier.
    It has the following functionality:

        * A counter, self.refresh_counter, to indicate how many
          times refresh was called.
        * A way to specify how many seconds to make credentials
          valid.
        * Configurable advisory/mandatory refresh.
        * An easy way to check consistency.  Each time creds are
          refreshed, all the cred values are set to the next
          incrementing integer.  Frozen credentials should always
          have this value.
    """

    _advisory_refresh_timeout = 2
    _mandatory_refresh_timeout = 1
    _credentials_expire = 3

    def __init__(self, creds_last_for=_credentials_expire,
                 advisory_refresh=_advisory_refresh_timeout,
                 mandatory_refresh=_mandatory_refresh_timeout,
                 refresh_function=None):
        expires_in = (
            self._current_datetime() +
            datetime.timedelta(seconds=creds_last_for))
        if refresh_function is None:
            refresh_function = self._do_refresh
        super(IntegerRefresher, self).__init__(
            '0', '0', '0', expires_in,
            refresh_function, 'INTREFRESH')
        self.creds_last_for = creds_last_for
        self.refresh_counter = 0
        self._advisory_refresh_timeout = advisory_refresh
        self._mandatory_refresh_timeout = mandatory_refresh

    def _do_refresh(self):
        self.refresh_counter += 1
        current = int(self._access_key)
        next_id = str(current + 1)

        return {
            'access_key': next_id,
            'secret_key': next_id,
            'token': next_id,
            'expiry_time': self._seconds_later(self.creds_last_for),
        }

    def _seconds_later(self, num_seconds):
        # We need to guarantee at *least* num_seconds.
        # Because this doesn't handle subsecond precision
        # we'll round up to the next second.
        num_seconds += 1
        t = self._current_datetime() + datetime.timedelta(seconds=num_seconds)
        return self._to_timestamp(t)

    def _to_timestamp(self, datetime_obj):
        obj = utils.parse_to_aware_datetime(datetime_obj)
        return obj.strftime('%Y-%m-%dT%H:%M:%SZ')

    def _current_timestamp(self):
        return self._to_timestamp(self._current_datetime())

    def _current_datetime(self):
        return datetime.datetime.now(tzlocal())


def _urlparse(url):
    if isinstance(url, six.binary_type):
        # Not really necessary, but it helps to reduce noise on Python 2.x
        url = url.decode('utf8')
    return urlparse(url)

def assert_url_equal(url1, url2):
    parts1 = _urlparse(url1)
    parts2 = _urlparse(url2)

    # Because the query string ordering isn't relevant, we have to parse
    # every single part manually and then handle the query string.
    assert_equal(parts1.scheme, parts2.scheme)
    assert_equal(parts1.netloc, parts2.netloc)
    assert_equal(parts1.path, parts2.path)
    assert_equal(parts1.params, parts2.params)
    assert_equal(parts1.fragment, parts2.fragment)
    assert_equal(parts1.username, parts2.username)
    assert_equal(parts1.password, parts2.password)
    assert_equal(parts1.hostname, parts2.hostname)
    assert_equal(parts1.port, parts2.port)
    assert_equal(parse_qs(parts1.query), parse_qs(parts2.query))


class HTTPStubberException(Exception):
    pass


class RawResponse(BytesIO):
    # TODO: There's a few objects similar to this in various tests, let's
    # try and consolidate to this one in a future commit.
    def stream(self, **kwargs):
        contents = self.read()
        while contents:
            yield contents
            contents = self.read()


class ClientHTTPStubber(object):
    def __init__(self, client, strict=True):
        self.reset()
        self._strict = strict
        self._client = client

    def reset(self):
        self.requests = []
        self.responses = []

    def add_response(self, url='https://example.com', status=200, headers=None,
                     body=b''):
        if headers is None:
            headers = {}

        raw = RawResponse(body)
        response = AWSResponse(url, status, headers, raw)
        self.responses.append(response)

    def start(self):
        self._client.meta.events.register('before-send', self)

    def stop(self):
        self._client.meta.events.unregister('before-send', self)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()

    def __call__(self, request, **kwargs):
        self.requests.append(request)
        if self.responses:
            response = self.responses.pop(0)
            if isinstance(response, Exception):
                raise response
            else:
                return response
        elif self._strict:
            raise HTTPStubberException('Insufficient responses')
        else:
            return None
