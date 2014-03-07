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
import functools
import logging
import os

from six.moves import configparser

from botocore.compat import total_seconds
from botocore.exceptions import UnknownCredentialError
from botocore.utils import InstanceMetadataFetcher


logger = logging.getLogger(__name__)


class Credentials(object):
    """
    Holds the credentials needed to authenticate requests.

    :ivar access_key: The access key part of the credentials.
    :ivar secret_key: The secret key part of the credentials.
    :ivar token: The security token, valid only for session credentials.
    :ivar method: A string which identifies where the credentials
        were found.
    """
    method = 'explicit'

    def __init__(self, access_key=None, secret_key=None, token=None,
                 session=None, method=None):
        self.session = session
        self.access_key = access_key
        self.secret_key = secret_key
        self.token = token

        if method:
            self.method = method


class RefreshableCredentials(Credentials):
    """
    Holds the credentials needed to authenticate requests. In addition, it
    knows how to refresh itself.

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
    method = 'temporary'

    def __init__(self, access_key=None, secret_key=None, token=None,
                 session=None, method=None, expiry_time=None,
                 refresh_using=None):
        self.session = session
        self.refresh_using = refresh_using
        self._access_key = access_key
        self._secret_key = secret_key
        self._token = token
        self.expiry_time = expiry_time

        if self.expiry_time is None:
            # Set an old, expired time by default.
            self.expiry_time = datetime.datetime(2000, 1, 1)

        if method:
            self.method = method

    @classmethod
    def create_from_metadata(cls, metadata, session=None, method=None,
                             refresh_using=None):
        instance = cls(
            session=session,
            method=method,
            refresh_using=refresh_using
        )
        instance._set_from_data(metadata)
        return instance

    @property
    def access_key(self):
        self._refresh()
        return self._access_key

    @access_key.setter
    def access_key(self, value):
        self._access_key = value

    @property
    def secret_key(self):
        self._refresh()
        return self._secret_key

    @secret_key.setter
    def secret_key(self, value):
        self._secret_key = value

    @property
    def token(self):
        self._refresh()
        return self._token

    @token.setter
    def token(self, value):
        self._token = value

    def _seconds_remaining(self):
        delta = self.expiry_time - datetime.datetime.utcnow()
        return total_seconds(delta)

    def refresh_needed(self):
        if self.expiry_time is None:
            # No expiration, so assume we don't need to refresh.
            return False

        # The credentials should be refreshed if they're going to expire
        # in less than 5 minutes.
        if self._seconds_remaining() >= self.refresh_timeout:
            # There's enough time left. Don't refresh.
            return False

        # Assume the worst & refresh.
        logger.debug("Credentials need to be refreshed.")
        return True

    def _refresh(self):
        if not self.refresh_needed():
            return

        data = self.refresh_using()
        self._set_from_data(data)

    def _set_from_data(self, data):
        self.access_key = data['access_key']
        self.secret_key = data['secret_key']
        self.token = data.get('token', None)

        if data['expiry_time']:
            self.expiry_time = datetime.datetime.strptime(
                data['expiry_time'],
                "%Y-%m-%dT%H:%M:%SZ"
            )
            logger.debug(
                "Retrieved credentials will expire at: %s",
                self.expiry_time
            )


class CredentialProvider(object):
    def __init__(self, session=None):
        self.session = session

    def load(self):
        """
        Loads the credentials from their source & sets them on the object.

        Subclasses should implement this method (by reading from disk, the
        environment, the network or wherever), returning ``True`` if they were
        found & loaded.

        If not found, this method should return ``False``, indictating that the
        ``CredentialResolver`` should fall back to the next available method.

        The default implementation does nothing, assuming the user has set the
        ``access_key/secret_key/token`` themselves.

        :returns: Whether credentials were found & set
        :rtype: boolean
        """
        return True


class InstanceMetadataProvider(CredentialProvider):
    method = 'iam-role'

    def load(self):
        timeout = self.session.get_config_variable('metadata_service_timeout')
        num_attempts = self.session.get_config_variable(
            'metadata_service_num_attempts'
        )
        retrieve_kwargs = {}
        if timeout is not None:
            retrieve_kwargs['timeout'] = float(timeout)
        if num_attempts is not None:
            retrieve_kwargs['num_attempts'] = int(num_attempts)
        fetcher = InstanceMetadataFetcher()
        # Partially apply the arguments for future calls.
        refresh_using = functools.partial(
            fetcher.retrieve_iam_role_credentials,
            **retrieve_kwargs
        )
        # We do the first request, to see if we get useful data back.
        # If not, we'll pass & move on to whatever's next in the credential
        # chain.
        metadata = refresh_using()
        if not metadata:
            return None
        logger.info('Found IAM Role: %s', metadata['role_name'])
        # We manually set the data here, since we already made the request &
        # have it. When the expiry is hit, the credentials will auto-refresh
        # themselves.
        creds = RefreshableCredentials.create_from_metadata(
            metadata,
            method=self.method,
            refresh_using=refresh_using
        )
        return creds


class EnvProvider(CredentialProvider):
    method = 'env'

    def load(self):
        """
        Search for credentials in explicit environment variables.
        """
        access_key = self.session.get_config_variable('access_key', ('env',))
        secret_key = self.session.get_config_variable('secret_key', ('env',))
        token = self.session.get_config_variable('token', ('env',))
        if access_key and secret_key:
            logger.info('Found credentials in Environment variables.')
            return Credentials(access_key, secret_key, token,
                               method=self.method)
        return None


class OriginalEC2Provider(CredentialProvider):
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
                    logger.info('Found credentials in AWS_CREDENTIAL_FILE.')
                    return Credentials(access_key, secret_key,
                                       method=self.method)
        return None


class ConfigProvider(CredentialProvider):
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
            logger.info('Found credentials in config file.')
            return Credentials(access_key, secret_key, token,
                               method=self.method)
        return None


class BotoProvider(CredentialProvider):
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
            logger.info('Found credentials in boto config file.')
            return Credentials(access_key, secret_key, method=self.method)
        return None


class CredentialResolver(object):
    default_methods = [
        EnvProvider,
        ConfigProvider,
        OriginalEC2Provider,
        BotoProvider,
        InstanceMetadataProvider,
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
            creds = cred.load()

            if creds is not None:
                return creds

        # If we got here, no credentials could be found.
        # This feels like it should be an exception, but historically, ``None``
        # is returned.
        return None


def get_credentials(session):
    resolver = CredentialResolver(session=session)
    return resolver.get_credentials()
