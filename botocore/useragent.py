# Copyright 2023 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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
from string import ascii_letters, digits

_USERAGENT_ALLOWED_CHARACTERS = ascii_letters + digits + "!$%&'*+-.^_`|~"


def sanitize_user_agent_string_component(raw_str, allow_hash):
    """Replaces all not allowed characters in the string with a dash ("-").

    Allowed characters are ASCII alphanumerics and ``!$%&'*+-.^_`|~``. If
    ``allow_hash`` is ``True``, "#"``" is also allowed.

    :type allow_hash: bool
    :param allow_hash: Whether "#" is considered an allowed character.
    """
    return ''.join(
        c
        if c in _USERAGENT_ALLOWED_CHARACTERS or (allow_hash and c == '#')
        else '-'
        for c in raw_str
    )
