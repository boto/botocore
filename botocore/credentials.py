# Copyright (c) 2012-2013 Mitch Garnaat http://garnaat.org/
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

import datetime
import logging
import os

from six.moves import configparser

from botocore.compat import json
from botocore.exceptions import UnknownCredentialError
from botocore.vendored import requests


logger = logging.getLogger(__name__)
DEFAULT_METADATA_SERVICE_TIMEOUT = 1
METADATA_SECURITY_CREDENTIALS_URL = (
    'http://169.254.169.254/latest/meta-data/iam/security-credentials/'
)


class _RetriesExceededError(Exception):
    """Internal exception used when the number of retries are exceeded."""
    pass


class Credentials(object):
    """
    Holds the credentials needed to authenticate requests.  In addition
    the Credential object knows how to search for credentials and how
    to choose the right credentials when multiple credentials are found.

    :ivar refresh_timeout: How long a given set of credentials are valid for.
        Useful for credentials fetched over the network.
    :ivar access_key: The access key part of the credentials.
    :ivar secret_key: The secret key part of the credentials.
    :ivar token: The security token, valid only for session credentials.
    :ivar method: A string which identifies where the credentials
        were found.
    :ivar session: The ``Session`` the credentials were created for. Useful for
        subclasses.
    """
    refresh_timeout = 5 * 60
    method = 'plain'

    def __init__(self, access_key=None, secret_key=None, token=None,
                 session=None):
        self.session = session
        self._access_key = access_key
        self._secret_key = secret_key
        self._token = token
        self._expiry_time = None

    @property
    def access_key(self):
        if self._refresh_needed():
            self.load()

        return self._access_key

    @access_key.setter
    def access_key(self, value):
        self._access_key = value

    @property
    def secret_key(self):
        if self._refresh_needed():
            self.load()

        return self._secret_key

    @secret_key.setter
    def secret_key(self, value):
        self._secret_key = value

    @property
    def token(self):
        if self._refresh_needed():
            self.load()

        return self._token

    @token.setter
    def token(self, value):
        self._token = value

    @property
    def is_populated(self):
        if self.access_key and self.secret_key:
            return True

        if self.token:
            return True

        return False

    def _get_request(self, url, timeout, num_attempts=1):
        for i in range(num_attempts):
            try:
                response = requests.get(url, timeout=timeout)
            except (requests.Timeout, requests.ConnectionError) as e:
                logger.debug("Caught exception while trying to retrieve "
                             "credentials: %s", e, exc_info=True)
            else:
                if response.status_code == 200:
                    return response
        raise _RetriesExceededError()

    def _seconds_remaining(self):
        # The credentials should be refreshed if they're going to expire
        # in less than 5 minutes.
        delta = self._expiry_time - datetime.datetime.utcnow()
        # python2.6 does not have timedelta.total_seconds() so we have
        # to calculate this ourselves.  This is straight from the
        # datetime docs.
        day_in_seconds = delta.days * 24 * 3600
        micro_in_seconds = delta.microseconds * 10**6
        return day_in_seconds + delta.seconds + micro_in_seconds

    def _refresh_needed(self):
        if self._expiry_time is None:
            # No expiration, so assume we don't need to refresh.
            return False

        if self._seconds_remaining() >= self.refresh_timeout:
            # There's enough time left. Don't refresh.
            return False

        # Assume the worst & refresh.
        logger.debug("Credentials need to be refreshed.")
        return True

    def load(self):
        """
        Loads the credentials from their source & sets them on the object.

        Subclasses should implement this method (by reading from disk, the
        environment, the network or wherever), returning ``True`` is they were
        found & loaded.

        If not found, this method should return ``False``, indictating that the
        ``CredentialResolver`` should fall back to the next available method.

        The default implementation does nothing, assuming the user has set the
        ``access_key/secret_key/token`` themselves.

        :returns: Whether credentials were found & set
        :rtype: boolean
        """
        return True


class IAMCredentials(Credentials):
    method = 'iam-role'

    def __init__(self, *args, **kwargs):
        # We need to set an initial expiration, well in the past.
        super(IAMCredentials, self).__init__(*args, **kwargs)
        self._expiry_time = datetime.datetime(2000, 1, 1)

    def load(self):
        timeout = self.session.get_config_variable('metadata_service_timeout')
        num_attempts = self.session.get_config_variable('metadata_service_num_attempts')
        retrieve_kwargs = {}
        if timeout is not None:
            retrieve_kwargs['timeout'] = float(timeout)
        if num_attempts is not None:
            retrieve_kwargs['num_attempts'] = int(num_attempts)
        metadata = self.retrieve_iam_role_credentials(**retrieve_kwargs)
        if not metadata:
            return False

        for role_name in metadata:
            # FIXME: This looks like it keeps overwriting, returning
            #        only the last role/credentials loaded? This is
            #        consistent with the pre-existing behavior, but seems
            #        potentially wrong.
            self.access_key = metadata[role_name]['AccessKeyId']
            self.secret_key = metadata[role_name]['SecretAccessKey']
            self.token = metadata[role_name]['Token']
            logger.info('Found IAM Role: %s', role_name)

        return True

    def retrieve_iam_role_credentials(self,
                                      url=METADATA_SECURITY_CREDENTIALS_URL,
                                      timeout=None, num_attempts=1):
        if timeout is None:
            timeout = DEFAULT_METADATA_SERVICE_TIMEOUT
        d = {}
        try:
            r = self._get_request(url, timeout, num_attempts)
            if r.content:
                fields = r.content.decode('utf-8').split('\n')
                for field in fields:
                    if field.endswith('/'):
                        d[field[0:-1]] = self.retrieve_iam_role_credentials(
                            url + field, timeout, num_attempts)
                    else:
                        val = self._get_request(
                            url + field,
                            timeout=timeout,
                            num_attempts=num_attempts).content.decode('utf-8')
                        if val[0] == '{':
                            val = json.loads(val)
                        d[field] = val
            else:
                logger.debug("Metadata service returned non 200 status code "
                             "of %s for url: %s, content body: %s",
                             r.status_code, url, r.content)
        except _RetriesExceededError:
            logger.debug("Max number of attempts exceeded (%s) when "
                         "attempting to retrieve data from metadata service.",
                         num_attempts)
        return d


class EnvCredentials(Credentials):
    method = 'env'

    def load(self):
        """
        Search for credentials in explicit environment variables.
        """
        access_key = self.session.get_config_variable('access_key', ('env',))
        secret_key = self.session.get_config_variable('secret_key', ('env',))
        token = self.session.get_config_variable('token', ('env',))
        if access_key and secret_key:
            self.access_key = access_key
            self.secret_key = secret_key
            self.token = token
            logger.info('Found credentials in Environment variables.')
            return True
        return False


class OriginalEC2Credentials(Credentials):
    method = 'credentials-file'

    def load(self):
        """
        Search for a credential file used by original EC2 CLI tools.
        """
        if 'AWS_CREDENTIAL_FILE' in os.environ:
            full_path = os.path.expanduser(os.environ['AWS_CREDENTIAL_FILE'])
            try:
                lines = map(str.strip, open(full_path).readlines())
            except IOError:
                logger.warn('Unable to load AWS_CREDENTIAL_FILE (%s).', full_path)
            else:
                config = dict(line.split('=', 1) for line in lines if '=' in line)
                access_key = config.get('AWSAccessKeyId')
                secret_key = config.get('AWSSecretKey')
                if access_key and secret_key:
                    self.access_key = access_key
                    self.secret_key = secret_key
                    logger.info('Found credentials in AWS_CREDENTIAL_FILE.')
                    return True
        return False


class ConfigCredentials(Credentials):
    method = 'config'

    def load(self):
        """
        If there is are credentials in the configuration associated with
        the session, use those.
        """
        access_key = self.session.get_config_variable('access_key', methods=('config',))
        secret_key = self.session.get_config_variable('secret_key', methods=('config',))
        token = self.session.get_config_variable('token', ('config',))
        if access_key and secret_key:
            self.access_key = access_key
            self.secret_key = secret_key
            self.token = token
            logger.info('Found credentials in config file.')
            return True
        return False


class BotoCredentials(Credentials):
    method = 'boto'

    def load(self):
        """
        Look for credentials in boto config file.
        """
        access_key = secret_key = None
        if 'BOTO_CONFIG' in os.environ:
            paths = [os.environ['BOTO_CONFIG']]
        else:
            paths = ['/etc/boto.cfg', '~/.boto']
        paths = [os.path.expandvars(p) for p in paths]
        paths = [os.path.expanduser(p) for p in paths]
        cp = configparser.RawConfigParser()
        cp.read(paths)
        if cp.has_section('Credentials'):
            if cp.has_option('Credentials', 'aws_access_key_id'):
                access_key = cp.get('Credentials', 'aws_access_key_id')
            if cp.has_option('Credentials', 'aws_secret_access_key'):
                secret_key = cp.get('Credentials', 'aws_secret_access_key')
        if access_key and secret_key:
            self.access_key = access_key
            self.secret_key = secret_key
            logger.info('Found credentials in boto config file.')
            return True
        return False


class CredentialResolver(object):
    default_methods = [
        EnvCredentials,
        ConfigCredentials,
        OriginalEC2Credentials,
        BotoCredentials,
        IAMCredentials,
    ]

    def __init__(self, session=None, methods=None):
        self.session = session
        self.methods = methods
        self.available_methods = []

        if self.methods is None:
            self.methods = []

            for method in self.default_methods:
                self.methods.append(method(session=self.session))

            self._rebuild_available_methods()

    def _rebuild_available_methods(self):
        # We basically maintain a cache of names, so that we don't have to
        # iterate over the all the ``self.methods`` all the time.
        self.available_methods = [cred.method for cred in self.methods]

    def insert_before(self, name, cred_instance):
        """
        Inserts a new type of ``Credentials`` instance into the chain that will
        be tried before an existing one.

        :param name: The short name of the credentials you'd like to insert the
            new credentials before. (ex. ``env`` or ``config``). Existing names
            & ordering can be discovered via ``self.available_methods``.
        :type name: string

        :param cred_instance: An instance of the new ``Credentials`` object
            you'd like to add to the chain.
        :type cred_instance: A subclass of ``Credentials``
        """
        try:
            offset = self.available_methods.index(name)
        except ValueError:
            raise UnknownCredentialError(name=name)

        self.methods.insert(offset, cred_instance)
        self._rebuild_available_methods()

    def insert_after(self, name, cred_instance):
        """
        Inserts a new type of ``Credentials`` instance into the chain that will
        be tried after an existing one.

        :param name: The short name of the credentials you'd like to insert the
            new credentials after. (ex. ``env`` or ``config``). Existing names
            & ordering can be discovered via ``self.available_methods``.
        :type name: string

        :param cred_instance: An instance of the new ``Credentials`` object
            you'd like to add to the chain.
        :type cred_instance: A subclass of ``Credentials``
        """
        try:
            offset = self.available_methods.index(name)
        except ValueError:
            raise UnknownCredentialError(name=name)

        self.methods.insert(offset + 1, cred_instance)
        self._rebuild_available_methods()

    def remove(self, name):
        """
        Removes a given ``Credentials`` instance from the chain.

        :param name: The short name of the credentials instance to remove.
        :type name: string
        """
        if not name in self.available_methods:
            # It's not present. Fail silently.
            return

        offset = self.available_methods.index(name)
        self.methods.pop(offset)
        self.available_methods.pop(offset)

    def get_credentials(self):
        """
        Goes through the credentials chain, returning the first ``Credentials``
        that could be loaded.
        """
        for cred in self.methods:
            if cred.is_populated or cred.load():
                return cred

        # If we got here, no credentials could be found.
        # This feels like it should be an exception, but historically, ``None``
        # is returned.
        return None


def get_credentials(session):
    resolver = CredentialResolver(session=session)
    return resolver.get_credentials()
