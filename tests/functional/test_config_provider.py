# Copyright 2022 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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
import pytest

from botocore.config import Config
from botocore.session import get_session

_SDK_DEFAULT_CONFIGURATION_VALUES_ALLOWLIST = (
    'retryMode',
    'stsRegionalEndpoints',
    's3UsEast1RegionalEndpoints',
    'connectTimeoutInMillis',
    'tlsNegotiationTimeoutInMillis',
)

session = get_session()
loader = session.get_component('data_loader')
sdk_default_configuration = loader.load_data('sdk-default-configuration')


@pytest.mark.parametrize("mode", sdk_default_configuration['base'])
def test_no_new_sdk_default_configuration_values(mode):
    err_msg = (
        f'New default configuration value {mode} introduced to '
        f'sdk-default-configuration.json. Support for setting {mode} must be '
        'considered and added to the DefaulConfigResolver. In addition, '
        'must add value to _SDK_DEFAULT_CONFIGURATION_VALUES_ALLOWLIST.'
    )
    assert mode in _SDK_DEFAULT_CONFIGURATION_VALUES_ALLOWLIST, err_msg


def test_default_configurations_resolve_correctly():
    session = get_session()
    config = Config(defaults_mode='standard')
    client = session.create_client(
        'sts', config=config, region_name='us-west-2'
    )
    assert client.meta.config.s3['us_east_1_regional_endpoint'] == 'regional'
    assert client.meta.config.connect_timeout == 3.1
    assert client.meta.endpoint_url == 'https://sts.us-west-2.amazonaws.com'
    assert client.meta.config.retries['mode'] == 'standard'
