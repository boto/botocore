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
import logging

from six import string_types, text_type

from botocore.exceptions import InvalidExpressionError, ConfigNotFound
from botocore.compat import json, quote
from botocore.vendored import requests


logger = logging.getLogger(__name__)
DEFAULT_METADATA_SERVICE_TIMEOUT = 1
METADATA_SECURITY_CREDENTIALS_URL = (
    'http://169.254.169.254/latest/meta-data/iam/security-credentials/'
)
# These are chars that do not need to be urlencoded.
# Based on rfc2986, section 2.3
SAFE_CHARS = '-._~'


class _RetriesExceededError(Exception):
    """Internal exception used when the number of retries are exceeded."""
    pass


def normalize_url_path(path):
    if not path:
        return '/'
    return remove_dot_segments(path)


def remove_dot_segments(url):
    # RFC 2986, section 5.2.4 "Remove Dot Segments"
    output = []
    while url:
        if url.startswith('../'):
            url = url[3:]
        elif url.startswith('./'):
            url = url[2:]
        elif url.startswith('/./'):
            url = '/' + url[3:]
        elif url.startswith('/../'):
            url = '/' + url[4:]
            if output:
                output.pop()
        elif url.startswith('/..'):
            url = '/' + url[3:]
            if output:
                output.pop()
        elif url.startswith('/.'):
            url = '/' + url[2:]
        elif url == '.' or url == '..':
            url = ''
        elif url.startswith('//'):
            # As far as I can tell, this is not in the RFC,
            # but AWS auth services require consecutive
            # slashes are removed.
            url = url[1:]
        else:
            if url[0] == '/':
                next_slash = url.find('/', 1)
            else:
                next_slash = url.find('/', 0)
            if next_slash == -1:
                output.append(url)
                url = ''
            else:
                output.append(url[:next_slash])
                url = url[next_slash:]
    return ''.join(output)


def validate_jmespath_for_set(expression):
    # Validates a limited jmespath expression to determine if we can set a value
    # based on it. Only works with dotted paths.
    if not expression or expression == '.':
        raise InvalidExpressionError(expression=expression)

    for invalid in ['[', ']', '*']:
        if invalid in expression:
            raise InvalidExpressionError(expression=expression)


def set_value_from_jmespath(source, expression, value, is_first=True):
    # This takes a (limited) jmespath-like expression & can set a value based
    # on it.
    # Limitations:
    # * Only handles dotted lookups
    # * No offsets/wildcards/slices/etc.
    if is_first:
        validate_jmespath_for_set(expression)

    bits = expression.split('.', 1)
    current_key, remainder = bits[0], bits[1] if len(bits) > 1 else ''

    if not current_key:
        raise InvalidExpressionError(expression=expression)

    if remainder:
        if not current_key in source:
            # We've got something in the expression that's not present in the
            # source (new key). If there's any more bits, we'll set the key with
            # an empty dictionary.
            source[current_key] = {}

        return set_value_from_jmespath(
            source[current_key],
            remainder,
            value,
            is_first=False
        )

    # If we're down to a single key, set it.
    source[current_key] = value


class InstanceMetadataFetcher(object):
    def __init__(self, timeout=DEFAULT_METADATA_SERVICE_TIMEOUT,
                 num_attempts=1, url=METADATA_SECURITY_CREDENTIALS_URL):
        self._timeout = timeout
        self._num_attempts = num_attempts
        self._url = url

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

    def retrieve_iam_role_credentials(self):
        data = {}
        url = self._url
        timeout = self._timeout
        num_attempts = self._num_attempts
        try:
            r = self._get_request(url, timeout, num_attempts)
            if r.content:
                fields = r.content.decode('utf-8').split('\n')
                for field in fields:
                    if field.endswith('/'):
                        data[field[0:-1]] = self.retrieve_iam_role_credentials(
                            url + field, timeout, num_attempts)
                    else:
                        val = self._get_request(
                            url + field,
                            timeout=timeout,
                            num_attempts=num_attempts).content.decode('utf-8')
                        if val[0] == '{':
                            val = json.loads(val)
                        data[field] = val
            else:
                logger.debug("Metadata service returned non 200 status code "
                             "of %s for url: %s, content body: %s",
                             r.status_code, url, r.content)
        except _RetriesExceededError:
            logger.debug("Max number of attempts exceeded (%s) when "
                         "attempting to retrieve data from metadata service.",
                         num_attempts)
        # We sort for stable ordering. In practice, this should only consist
        # of one role, but may need revisiting if this expands in the future.
        final_data = {}
        for role_name in sorted(data):
            final_data = {
                'role_name': role_name,
                'access_key': data[role_name]['AccessKeyId'],
                'secret_key': data[role_name]['SecretAccessKey'],
                'token': data[role_name]['Token'],
                'expiry_time': data[role_name]['Expiration'],
            }
        return final_data


def merge_dicts(dict1, dict2):
    """Given two dict, merge the second dict into the first.

    The dicts can have arbitrary nesting.

    """
    for key in dict2:
        if isinstance(dict2[key], dict):
            if key in dict1 and key in dict2:
                merge_dicts(dict1[key], dict2[key])
            else:
                dict1[key] = dict2[key]
        else:
            # At scalar types, we iterate and merge the
            # current dict that we're on.
            dict1[key] = dict2[key]


def parse_key_val_file(filename, _open=open):
    try:
        with _open(filename) as f:
            contents = f.read()
            return parse_key_val_file_contents(contents)
    except OSError as e:
        raise ConfigNotFound(path=filename)


def parse_key_val_file_contents(contents):
    # This was originally extracted from the EC2 credential provider, which was
    # fairly lenient in its parsing.  We only try to parse key/val pairs if
    # there's a '=' in the line.
    final = {}
    for line in contents.splitlines():
        if '=' not in line:
            continue
        key, val = line.split('=', 1)
        key = key.strip()
        val = val.strip()
        final[key] = val
    return final


def percent_encode_sequence(mapping, safe=SAFE_CHARS):
    """Urlencode a dict or list into a string.

    This is similar to urllib.urlencode except that:

    * It uses quote, and not quote_plus
    * It has a default list of safe chars that don't need
      to be encoded, which matches what AWS services expect.

    This function should be preferred over the stdlib
    ``urlencode()`` function.

    :param mapping: Either a dict to urlencode or a list of
        ``(key, value)`` pairs.

    """
    encoded_pairs = []
    if hasattr(mapping, 'items'):
        pairs = mapping.items()
    else:
        pairs = mapping
    for key, value in pairs:
        encoded_pairs.append('%s=%s' % (percent_encode(key),
                                        percent_encode(value)))
    return '&'.join(encoded_pairs)


def percent_encode(input_str, safe=SAFE_CHARS):
    """Urlencodes a string.

    Whereas percent_encode_sequence handles taking a dict/sequence and
    producing a percent encoded string, this function deals only with
    taking a string (not a dict/sequence) and percent encoding it.

    """
    if not isinstance(input_str, string_types):
        input_str = text_type(input_str)
    return quote(text_type(input_str), safe=safe)
