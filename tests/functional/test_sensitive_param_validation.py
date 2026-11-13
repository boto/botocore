# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
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
"""Parameter validation errors must not echo values the models mark sensitive.

These use the real service models, so they cover the calls where this was
found: a secret passed as bytes (as ``fileb://`` does in the CLI) and a
database password passed as a number.
"""

import pytest

import botocore.session
from botocore.exceptions import ParamValidationError
from botocore.validate import SENSITIVE_VALUE_PLACEHOLDER

FAKE_SECRET = 'not-a-real-secret-123'


@pytest.fixture
def session():
    return botocore.session.get_session()


def _client(session, service_name):
    return session.create_client(
        service_name,
        region_name='us-east-1',
        aws_access_key_id='foo',
        aws_secret_access_key='bar',
    )


def test_secret_string_as_bytes_is_redacted(session):
    client = _client(session, 'secretsmanager')
    with pytest.raises(ParamValidationError) as error:
        client.put_secret_value(
            SecretId='example', SecretString=FAKE_SECRET.encode()
        )
    message = str(error.value)
    assert FAKE_SECRET not in message
    assert 'Invalid type for parameter SecretString' in message
    assert SENSITIVE_VALUE_PLACEHOLDER in message


def test_numeric_master_password_is_redacted(session):
    client = _client(session, 'rds')
    with pytest.raises(ParamValidationError) as error:
        client.create_db_instance(
            DBInstanceIdentifier='example',
            DBInstanceClass='db.t4g.micro',
            Engine='postgres',
            MasterUsername='admin',
            MasterUserPassword=48213377,
        )
    message = str(error.value)
    assert '48213377' not in message
    assert 'Invalid type for parameter MasterUserPassword' in message


def test_lambda_environment_variable_value_is_redacted(session):
    # Environment values must be strings, so a numeric password from YAML or a
    # config file is a common way to reach this error.
    # EnvironmentVariables has a sensitive key shape as well as a sensitive
    # value shape, so both halves of the message matter here.
    client = _client(session, 'lambda')
    with pytest.raises(ParamValidationError) as error:
        client.update_function_configuration(
            FunctionName='example',
            Environment={'Variables': {'DB_PASSWORD': 48213377}},
        )
    message = str(error.value)
    assert '48213377' not in message
    assert 'Invalid type for parameter Environment.Variables.' in message


def test_non_sensitive_value_is_still_shown(session):
    client = _client(session, 'secretsmanager')
    with pytest.raises(ParamValidationError) as error:
        client.put_secret_value(SecretId=12345, SecretString='fine')
    assert 'value: 12345' in str(error.value)
