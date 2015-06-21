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

from botocore.compat import six
from six.moves import configparser
from dateutil.parser import parse
from dateutil.tz import tzlocal

import botocore.config
from botocore.compat import total_seconds
from botocore.exceptions import UnknownCredentialError
from botocore.exceptions import PartialCredentialsError
from botocore.exceptions import ConfigNotFound
from botocore.utils import InstanceMetadataFetcher, parse_key_val_file


logger = logging.getLogger(__name__)


def create_credential_resolver(session):
    """Create a default credential resolver.

    This creates a pre-configured credential resolver
    that includes the default lookup chain for
    credentials.

    """
    profile_name = session.get_config_variable('profile') or 'default'
    credential_file = session.get_config_variable('credentials_file')
    config_file = session.get_config_variable('config_file')
    metadata_timeout = session.get_config_variable('metadata_service_timeout')
    num_attempts = session.get_config_variable('metadata_service_num_attempts')

    providers = [
        SharedCredentialProvider(
            creds_filename=credential_file,
            profile_name=profile_name
        ),
        # The new config file has precedence over the legacy
        # config file.
        ConfigProvider(config_filename=config_file, profile_name=profile_name),
        OriginalEC2Provider(),
        BotoProvider(),
        InstanceMetadataProvider(
            iam_role_fetcher=InstanceMetadataFetcher(
                timeout=metadata_timeout,
                num_attempts=num_attempts)
        )
    ]

    # We use ``session.profile`` for EnvProvider rather than
    # ``profile_name`` because it is ``None`` when unset.
    # TODO: Remove use of internal var.  We'll need to rethink this.
    if session._profile is None:
        # No profile has been explicitly set, so we prepend the environment
        # variable provider. That provider, in turn, may set a profile
        # or credentials.
        providers.insert(0, EnvProvider())
    else:
        logger.debug('Skipping environment variable credential check'
                     ' because profile name was explicitly set.')

    resolver = CredentialResolver(providers=providers)
    return resolver


def get_credentials(session):
    resolver = create_credential_resolver(session)
    return resolver.load_credentials()


def _local_now():
    return datetime.datetime.now(tzlocal())


class Credentials(object):
    """
    Holds the credentials needed to authenticate requests.

    :ivar access_key: The access key part of the credentials.
    :ivar secret_key: The secret key part of the credentials.
    :ivar token: The security token, valid only for session credentials.
    :ivar method: A string which identifies where the credentials
        were found.
    """

    def __init__(self, access_key, secret_key, token=None,
                 method=None):
        self.access_key = access_key
        self.secret_key = secret_key
        self.token = token

        if method is None:
            method = 'explicit'
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
    refresh_timeout = 15 * 60

    def __init__(self, access_key, secret_key, token,
                 expiry_time, refresh_using, method,
                 time_fetcher=_local_now):
        self._refresh_using = refresh_using
        self._access_key = access_key
        self._secret_key = secret_key
        self._token = token
        self._expiry_time = expiry_time
        self._time_fetcher = time_fetcher
        self.method = method

    @classmethod
    def create_from_metadata(cls, metadata, refresh_using, method):
        instance = cls(
            access_key=metadata['access_key'],
            secret_key=metadata['secret_key'],
            token=metadata['token'],
            expiry_time=cls._expiry_datetime(metadata['expiry_time']),
            method=method,
            refresh_using=refresh_using
        )
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
        delta = self._expiry_time - self._time_fetcher()
        return total_seconds(delta)

    def refresh_needed(self):
        if self._expiry_time is None:
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

        metadata = self._refresh_using()
        self._set_from_data(metadata)

    @staticmethod
    def _expiry_datetime(time_str):
        return parse(time_str)

    def _set_from_data(self, data):
        self.access_key = data['access_key']
        self.secret_key = data['secret_key']
        self.token = data['token']
        self._expiry_time = parse(data['expiry_time'])
        logger.debug("Retrieved credentials will expire at: %s", self._expiry_time)


class CredentialProvider(object):

    # Implementations must provide a method.
    METHOD = None

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

    def _extract_creds_from_mapping(self, mapping, *key_names):
        found = []
        for key_name in key_names:
            try:
                found.append(mapping[key_name])
            except KeyError:
                raise PartialCredentialsError(provider=self.METHOD,
                                              cred_var=key_name)
        return found


class InstanceMetadataProvider(CredentialProvider):
    METHOD = 'iam-role'

    def __init__(self, iam_role_fetcher):
        self._role_fetcher = iam_role_fetcher

    def load(self):
        fetcher = self._role_fetcher
        # We do the first request, to see if we get useful data back.
        # If not, we'll pass & move on to whatever's next in the credential
        # chain.
        metadata = fetcher.retrieve_iam_role_credentials()
        if not metadata:
            return None
        logger.info('Found credentials from IAM Role: %s', metadata['role_name'])
        # We manually set the data here, since we already made the request &
        # have it. When the expiry is hit, the credentials will auto-refresh
        # themselves.
        creds = RefreshableCredentials.create_from_metadata(
            metadata,
            method=self.METHOD,
            refresh_using=fetcher.retrieve_iam_role_credentials,
        )
        return creds


class EnvProvider(CredentialProvider):
    METHOD = 'env'
    ACCESS_KEY = 'AWS_ACCESS_KEY_ID'
    SECRET_KEY = 'AWS_SECRET_ACCESS_KEY'
    # The token can come from either of these env var.
    # AWS_SESSION_TOKEN is what other AWS SDKs have standardized on.
    TOKENS = ['AWS_SECURITY_TOKEN', 'AWS_SESSION_TOKEN']

    def __init__(self, environ=None, mapping=None):
        """

        :param environ: The environment variables (defaults to
            ``os.environ`` if no value is provided).
        :param mapping: An optional mapping of variable names to
            environment variable names.  Use this if you want to
            change the mapping of access_key->AWS_ACCESS_KEY_ID, etc.
            The dict can have up to 3 keys: ``access_key``, ``secret_key``,
            ``session_token``.
        """
        if environ is None:
            environ = os.environ
        self.environ = environ
        self._mapping = self._build_mapping(mapping)

    def _build_mapping(self, mapping):
        # Mapping of variable name to env var name.
        var_mapping = {}
        if mapping is None:
            # Use the class var default.
            var_mapping['access_key'] = self.ACCESS_KEY
            var_mapping['secret_key'] = self.SECRET_KEY
            var_mapping['token'] = self.TOKENS
        else:
            var_mapping['access_key'] = mapping.get(
                'access_key', self.ACCESS_KEY)
            var_mapping['secret_key'] = mapping.get(
                'secret_key', self.SECRET_KEY)
            var_mapping['token'] = mapping.get(
                'token', self.TOKENS)
            if not isinstance(var_mapping['token'], list):
                var_mapping['token'] = [var_mapping['token']]
        return var_mapping

    def load(self):
        """
        Search for credentials in explicit environment variables.
        """
        if self._mapping['access_key'] in self.environ:
            logger.info('Found credentials in environment variables.')
            access_key, secret_key = self._extract_creds_from_mapping(
                self.environ, self._mapping['access_key'],
                self._mapping['secret_key'])
            token = self._get_session_token()
            return Credentials(access_key, secret_key, token,
                               method=self.METHOD)
        else:
            return None

    def _get_session_token(self):
        for token_envvar in self._mapping['token']:
            if token_envvar in self.environ:
                return self.environ[token_envvar]


class OriginalEC2Provider(CredentialProvider):
    METHOD = 'ec2-credentials-file'

    CRED_FILE_ENV = 'AWS_CREDENTIAL_FILE'
    ACCESS_KEY = 'AWSAccessKeyId'
    SECRET_KEY = 'AWSSecretKey'

    def __init__(self, environ=None, parser=None):
        if environ is None:
            environ = os.environ
        if parser is None:
            parser = parse_key_val_file
        self._environ = environ
        self._parser = parser

    def load(self):
        """
        Search for a credential file used by original EC2 CLI tools.
        """
        if 'AWS_CREDENTIAL_FILE' in self._environ:
            full_path = os.path.expanduser(self._environ['AWS_CREDENTIAL_FILE'])
            creds = self._parser(full_path)
            if self.ACCESS_KEY in creds:
                logger.info('Found credentials in AWS_CREDENTIAL_FILE.')
                access_key = creds[self.ACCESS_KEY]
                secret_key = creds[self.SECRET_KEY]
                # EC2 creds file doesn't support session tokens.
                return Credentials(access_key, secret_key, method=self.METHOD)
        else:
            return None


class SharedCredentialProvider(CredentialProvider):
    METHOD = 'shared-credentials-file'

    ACCESS_KEY = 'aws_access_key_id'
    SECRET_KEY = 'aws_secret_access_key'
    # Same deal as the EnvProvider above.  Botocore originally supported
    # aws_security_token, but the SDKs are standardizing on aws_session_token
    # so we support both.
    TOKENS = ['aws_security_token', 'aws_session_token']

    def __init__(self, creds_filename, profile_name=None, ini_parser=None):
        self._creds_filename = creds_filename
        if profile_name is None:
            profile_name = 'default'
        self._profile_name = profile_name
        if ini_parser is None:
            ini_parser = botocore.config.raw_config_parse
        self._ini_parser = ini_parser

    def load(self):
        try:
            available_creds = self._ini_parser(self._creds_filename)
        except ConfigNotFound:
            return None
        if self._profile_name in available_creds:
            config = available_creds[self._profile_name]
            if self.ACCESS_KEY in config:
                logger.info("Found credentials in shared credentials file: %s",
                            self._creds_filename)
                access_key, secret_key = self._extract_creds_from_mapping(
                    config, self.ACCESS_KEY, self.SECRET_KEY)
                token =  self._get_session_token(config)
                return Credentials(access_key, secret_key, token,
                                   method=self.METHOD)

    def _get_session_token(self, config):
        for token_envvar in self.TOKENS:
            if token_envvar in config:
                return config[token_envvar]


class ConfigProvider(CredentialProvider):
    """INI based config provider with profile sections."""
    METHOD = 'config-file'

    ACCESS_KEY = 'aws_access_key_id'
    SECRET_KEY = 'aws_secret_access_key'
    # Same deal as the EnvProvider above.  Botocore originally supported
    # aws_security_token, but the SDKs are standardizing on aws_session_token
    # so we support both.
    TOKENS = ['aws_security_token', 'aws_session_token']

    def __init__(self, config_filename, profile_name, config_parser=None):
        """

        :param config_filename: The session configuration scoped to the current
            profile.  This is available via ``session.config``.
        :param profile_name: The name of the current profile.
        :param config_parser: A config parser callable.

        """
        self._config_filename = config_filename
        self._profile_name = profile_name
        if config_parser is None:
            config_parser = botocore.config.load_config
        self._config_parser = config_parser

    def load(self):
        """
        If there is are credentials in the configuration associated with
        the session, use those.
        """
        try:
            full_config = self._config_parser(self._config_filename)
        except ConfigNotFound:
            return None
        if self._profile_name in full_config['profiles']:
            profile_config = full_config['profiles'][self._profile_name]
            if self.ACCESS_KEY in profile_config:
                logger.info("Credentials found in config file: %s",
                            self._config_filename)
                access_key, secret_key = self._extract_creds_from_mapping(
                    profile_config, self.ACCESS_KEY, self.SECRET_KEY)
                token = self._get_session_token(profile_config)
                return Credentials(access_key, secret_key, token,
                                method=self.METHOD)
        else:
            return None

    def _get_session_token(self, profile_config):
        for token_name in self.TOKENS:
            if token_name in profile_config:
                return profile_config[token_name]


class BotoProvider(CredentialProvider):
    METHOD = 'boto-config'

    BOTO_CONFIG_ENV = 'BOTO_CONFIG'
    DEFAULT_CONFIG_FILENAMES = ['/etc/boto.cfg', '~/.boto']
    ACCESS_KEY = 'aws_access_key_id'
    SECRET_KEY = 'aws_secret_access_key'

    def __init__(self, environ=None, ini_parser=None):
        if environ is None:
            environ = os.environ
        if ini_parser is None:
            ini_parser = botocore.config.raw_config_parse
        self._environ = environ
        self._ini_parser = ini_parser

    def load(self):
        """
        Look for credentials in boto config file.
        """
        if self.BOTO_CONFIG_ENV in self._environ:
            potential_locations = [self._environ[self.BOTO_CONFIG_ENV]]
        else:
            potential_locations = self.DEFAULT_CONFIG_FILENAMES
        for filename in potential_locations:
            try:
                config = self._ini_parser(filename)
            except ConfigNotFound:
                # Move on to the next potential config file name.
                continue
            if 'Credentials' in config:
                credentials = config['Credentials']
                if self.ACCESS_KEY in credentials:
                    logger.info("Found credentials in boto config file: %s",
                                filename)
                    access_key, secret_key = self._extract_creds_from_mapping(
                        credentials, self.ACCESS_KEY, self.SECRET_KEY)
                    return Credentials(access_key, secret_key,
                                       method=self.METHOD)


class CredentialResolver(object):

    def __init__(self, providers):
        """

        :param providers: A list of ``CredentialProvider`` instances.

        """
        self.providers = providers

    def insert_before(self, name, credential_provider):
        """
        Inserts a new instance of ``CredentialProvider`` into the chain that will
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
            offset = [p.METHOD for p in self.providers].index(name)
        except ValueError:
            raise UnknownCredentialError(name=name)
        self.providers.insert(offset, credential_provider)

    def insert_after(self, name, credential_provider):
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
            offset = [p.METHOD for p in self.providers].index(name)
        except ValueError:
            raise UnknownCredentialError(name=name)

        self.providers.insert(offset + 1, credential_provider)

    def remove(self, name):
        """
        Removes a given ``Credentials`` instance from the chain.

        :param name: The short name of the credentials instance to remove.
        :type name: string
        """
        available_methods = [p.METHOD for p in self.providers]
        if not name in available_methods:
            # It's not present. Fail silently.
            return

        offset = available_methods.index(name)
        self.providers.pop(offset)

    def load_credentials(self):
        """
        Goes through the credentials chain, returning the first ``Credentials``
        that could be loaded.
        """
        # First provider to return a non-None response wins.
        for provider in self.providers:
            logger.debug("Looking for credentials via: %s", provider.METHOD)
            creds = provider.load()
            if creds is not None:
                return creds

        # If we got here, no credentials could be found.
        # This feels like it should be an exception, but historically, ``None``
        # is returned.
        #
        # +1
        # -js
        return None
