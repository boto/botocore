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

import os
import datetime
import logging

from six.moves import configparser

from botocore.vendored import requests
from botocore.compat import json
from botocore.exceptions import TemporaryCredentialsError


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

    :ivar access_key: The access key part of the credentials.
    :ivar secret_key: The secret key part of the credentials.
    :ivar token: The security token, valid only for session credentials.
    :ivar method: A string which identifies where the credentials
        were found.  Valid values are: iam_role|env|config|boto.
    """

    def __init__(self, access_key=None, secret_key=None, token=None):
        self.access_key = access_key
        self.secret_key = secret_key
        self.token = token
        self.method = None
        self.profiles = []


def get_temporary_credential_path(session):
    cred_path = None
    config_path = session.get_variable('config_file')
    if config_path:
        cred_path = os.path.dirname(session.get_variable('config_file'))
        cred_path = os.path.expanduser(cred_path)
        cred_path = os.path.expandvars(cred_path)
        cred_path = os.path.join(cred_path, '.session')
    return cred_path


def create_temporary_credentials(session, credential_service=None,
                                 credential_fn=None, **kwargs):
    return TemporaryCredentials(session, cred_service=credential_service,
                                cred_op=credential_fn, **kwargs)


def delete_temporary_credentials(session):
    path = get_temporary_credential_path(session)
    if os.path.isfile(path):
        os.unlink(path)


class TemporaryCredentials(Credentials):

    def __init__(self, session, path=None, cred_service=None,
                 cred_op=None, **cred_params):
        self._session = session
        self._cred_data = None
        if not path:
            self._path = get_temporary_credential_path(self._session)
        else:
            self._path = path
        if cred_service and cred_op:
            self._fetch(cred_service, cred_op, cred_params)
        else:
            self._load()
        self.method = 'session-cache'

    @property
    def access_key(self):
        self._check()
        return self._cred_data['AccessKeyId']

    @property
    def secret_key(self):
        self._check()
        return self._cred_data['SecretAccessKey']

    @property
    def token(self):
        self._check()
        return self._cred_data['SessionToken']

    def _load(self):
        with open(self._path) as fp:
            self._cred_data = json.load(fp)

    def _check(self):
        # Now we need to check to see if the cached credentials
        # are still valid or if they have expired.
        expiry_time = datetime.datetime.strptime(
            self._cred_data['Expiration'], "%Y-%m-%dT%H:%M:%SZ")
        now = datetime.datetime.utcnow()
        # The credentials should be refreshed if they're going to expire
        # in less than 15 minutes.
        delta = expiry_time - now
        # python2.6 does not have timedelta.total_seconds() so we have
        # to calculate this ourselves.  This is straight from the
        # datetime docs.
        seconds_left = (
            (delta.microseconds + (delta.seconds + delta.days * 24 * 3600)
             * 10**6) / 10**6)
        if seconds_left < (15 * 60):
            os.unlink(self._path)
            cred_service = self._cred_data['CredentialService']
            cred_op = self._cred_data['CredentialOp']
            cred_params = self._cred_data['CredentialParams']
            self._fetch(cred_service, cred_op, cred_params)

    def _fetch(self, cred_service, cred_op, cred_params):
        logger.debug('Calling %s.%s to refresh credentials',
                     cred_service, cred_op)
        self._session._credentials = None
        svc = self._session.get_service(cred_service)
        endpoint = svc.get_endpoint()
        operation = svc.get_operation(cred_op)
        http_response, data = operation.call(endpoint, **cred_params)
        if http_response.status_code != 200:
            logger.debug(data)
            msg = 'Received code: %d' % http_response.status_code
            if 'Errors' in data:
                if 'Message' in data['Errors'][0]:
                    msg = data['Errors'][0]['Message']
            raise TemporaryCredentialsError(msg=msg)
        with open(self._path, 'w') as fp:
            self._cred_data = data['Credentials']
            self._cred_data['CredentialService'] = cred_service
            self._cred_data['CredentialOp'] = cred_op
            self._cred_data['CredentialParams'] = cred_params
            json.dump(self._cred_data, fp, indent=4)
        self._session._credentials = None


def retrieve_iam_role_credentials(url=METADATA_SECURITY_CREDENTIALS_URL,
                                  timeout=None, num_attempts=1):
    if timeout is None:
        timeout = DEFAULT_METADATA_SERVICE_TIMEOUT
    d = {}
    try:
        r = _get_request(url, timeout, num_attempts)
        if r.content:
            fields = r.content.decode('utf-8').split('\n')
            for field in fields:
                if field.endswith('/'):
                    d[field[0:-1]] = retrieve_iam_role_credentials(
                        url + field, timeout, num_attempts)
                else:
                    val = _get_request(
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


def _get_request(url, timeout, num_attempts):
    for i in range(num_attempts):
        try:
            response = requests.get(url, timeout=timeout)
        except (requests.Timeout, requests.ConnectionError) as e:
            logger.debug("Caught exception wil trying to retrieve credentials "
                         "from metadata service: %s", e, exc_info=True)
        else:
            if response.status_code == 200:
                return response
    raise _RetriesExceededError()


def search_iam_role(session, **kwargs):
    credentials = None
    timeout = session.get_config_variable('metadata_service_timeout')
    num_attempts = session.get_config_variable('metadata_service_num_attempts')
    retrieve_kwargs = {}
    if timeout is not None:
        retrieve_kwargs['timeout'] = float(timeout)
    if num_attempts is not None:
        retrieve_kwargs['num_attempts'] = int(num_attempts)
    metadata = retrieve_iam_role_credentials(**retrieve_kwargs)
    if metadata:
        for role_name in metadata:
            credentials = Credentials(metadata[role_name]['AccessKeyId'],
                                      metadata[role_name]['SecretAccessKey'],
                                      metadata[role_name]['Token'])
            credentials.method = 'iam-role'
            logger.info('Found IAM Role: %s', role_name)
    return credentials


def search_environment(**kwargs):
    """
    Search for credentials in explicit environment variables.
    """
    session = kwargs.get('session')
    credentials = None
    access_key = session.get_config_variable('access_key', ('env',))
    secret_key = session.get_config_variable('secret_key', ('env',))
    token = session.get_config_variable('token', ('env',))
    if access_key and secret_key:
        credentials = Credentials(access_key, secret_key, token)
        credentials.method = 'env'
        logger.info('Found credentials in Environment variables.')
    return credentials


def search_credentials_file(**kwargs):
    """
    Search for a credential file used by original EC2 CLI tools.
    """
    credentials = None
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
                credentials = Credentials(access_key, secret_key)
                credentials.method = 'credentials-file'
                logger.info('Found credentials in AWS_CREDENTIAL_FILE.')
    return credentials


def search_file(**kwargs):
    """
    If there is are credentials in the configuration associated with
    the session, use those.
    """
    credentials = None
    session = kwargs.get('session')
    access_key = session.get_config_variable('access_key', methods=('config',))
    secret_key = session.get_config_variable('secret_key', methods=('config',))
    token = session.get_config_variable('token', ('config',))
    if access_key and secret_key:
        credentials = Credentials(access_key, secret_key, token)
        credentials.method = 'config'
        logger.info('Found credentials in config file.')
    return credentials


def search_boto_config(**kwargs):
    """
    Look for credentials in boto config file.
    """
    credentials = access_key = secret_key = None
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
        credentials = Credentials(access_key, secret_key)
        credentials.method = 'boto'
        logger.info('Found credentials in boto config file.')
    return credentials

def search_temporary_credentials(**kwargs):
    """
    If there are temporary credentials stored on the filesystem
    use those.
    """
    credentials = None
    session = kwargs.get('session')
    cache_path = get_temporary_credential_path(session)
    if cache_path is not None and os.path.isfile(cache_path):
        credentials = TemporaryCredentials(session, cache_path)
        credentials.method = 'session-cache'
        logger.info('Found credentials in temporary credential cache.')
    return credentials


AllCredentialFunctions = [search_temporary_credentials,
                          search_environment,
                          search_credentials_file,
                          search_file,
                          search_boto_config,
                          search_iam_role]

_credential_methods = (('session-cache', search_temporary_credentials),
                       ('env', search_environment),
                       ('config', search_file),
                       ('credentials-file', search_credentials_file),
                       ('boto', search_boto_config),
                       ('iam-role', search_iam_role))


def get_credentials(session):
    credentials = None
    for cred_method, cred_fn in _credential_methods:
        credentials = cred_fn(session=session)
        if credentials:
            break
    return credentials

