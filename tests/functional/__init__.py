# Copyright 2015 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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
import uuid

_ORIGINAL = os.environ.copy()
# These are environment variables that allow users to control
# the location of config files used by botocore.
_CONFIG_FILE_ENV_VARS = [
    'AWS_CONFIG_FILE',
    'AWS_SHARED_CREDENTIALS_FILE',
    'BOTO_CONFIG',
]
_CREDENTIAL_ENV_VARS = [
    'AWS_ACCESS_KEY_ID',
    'AWS_SECRET_ACCESS_KEY',
    'AWS_SESSION_TOKEN',
]


def setup_package():
    random_file = str(uuid.uuid4())
    for varname in _CONFIG_FILE_ENV_VARS:
        os.environ[varname] = random_file
    for credvar in _CREDENTIAL_ENV_VARS:
        os.environ.pop(credvar, None)


def teardown_package():
    os.environ = _ORIGINAL
