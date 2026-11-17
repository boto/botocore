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
import logging
import platform
import threading

import pytest

import botocore.useragent
from botocore import __version__ as botocore_version
from botocore.config import Config
from botocore.context import (
    ClientContext,
    get_context,
    start_as_current_context,
)
from botocore.useragent import (
    RawStringUserAgentComponent,
    UserAgentComponent,
    UserAgentComponentSizeConfig,
    UserAgentString,
    register_feature_id,
    sanitize_user_agent_string_component,
)
from tests import mock

from .. import requires_crt

# Returns a list of unmodified User-Agent components.
unmodified_components = botocore.useragent._default_modify_components


@pytest.mark.parametrize(
    'raw_str, allow_hash, expected_str',
    [
        ('foo', False, 'foo'),
        ('foo', True, 'foo'),
        ('ExampleFramework (1.2.3)', False, 'ExampleFramework--1.2.3-'),
        ('foo#1.2.3', False, 'foo-1.2.3'),
        ('foo#1.2.3', True, 'foo#1.2.3'),
        ('', False, ''),
        ('', True, ''),
        ('', False, ''),
        ('#', False, '-'),
        ('#', True, '#'),
        (' ', False, '-'),
        ('  ', False, '--'),
        ('@=[]{ }/\\øß©', True, '------------'),
        (
            'Java_HotSpot_(TM)_64-Bit_Server_VM/25.151-b12',
            True,
            'Java_HotSpot_-TM-_64-Bit_Server_VM-25.151-b12',
        ),
    ],
)
def test_sanitize_ua_string_component(raw_str, allow_hash, expected_str):
    actual_str = sanitize_user_agent_string_component(raw_str, allow_hash)
    assert actual_str == expected_str


@mock.patch.object(
    botocore.useragent, 'modify_components', unmodified_components
)
def test_basic_user_agent_string():
    ua = UserAgentString(
        platform_name='linux',
        platform_version='1.2.3-foo',
        platform_machine='x86_64',
        python_version='3.8.20',
        python_implementation='Dpython',
        execution_env='AWS_Lambda_python3.8',
        crt_version='Unknown',
    ).with_client_config(
        Config(retries={'mode': 'legacy'}, user_agent_appid='fooapp')
    )

    actual = ua.to_string()
    expected = (
        f'Botocore/{botocore_version} '
        'md/awscrt#Unknown '
        'ua/2.1 '
        'os/linux#1.2.3-foo '
        'md/arch#x86_64 '
        'lang/python#3.8.20 '
        'md/pyimpl#Dpython '
        'exec-env/AWS_Lambda_python3.8 '
        'cfg/retry-mode#legacy '
        'app/fooapp'
    )
    assert actual == expected


def test_shared_test_case():
    # This test case is shared across AWS SDKs.

    uas = UserAgentString(
        platform_name="Linux",
        platform_version="5.4.228-131.415.AMZN2.X86_64",
        platform_machine="",
        python_version="4.3.2",
        python_implementation=None,
        execution_env='lambda',
    ).with_client_config(
        Config(user_agent_appid='123456', retries={'mode': 'standard'})
    )
    actual = uas.to_string().split(' ')
    expected_in_exact_order = [
        f"Botocore/{botocore_version}",
        "ua/2.1",
        "os/linux#5.4.228-131.415.AMZN2.X86_64",
        "lang/python#4.3.2",
        "exec-env/lambda",
    ]
    expected_in_any_order = [
        "cfg/retry-mode#standard",
        "app/123456",
    ]
    for el in [*expected_in_exact_order, *expected_in_any_order]:
        assert el in actual

    indices = [actual.index(el) for el in expected_in_exact_order]
    assert indices == list(sorted(indices)), 'Elements were found out of order'


@mock.patch.object(
    botocore.useragent, 'modify_components', unmodified_components
)
def test_user_agent_string_with_missing_information():
    # Even when collecting information from the environment fails completely,
    # some minimal string should be generated.
    uas = UserAgentString(
        platform_name=None,
        platform_version=None,
        platform_machine=None,
        python_version=None,
        python_implementation=None,
        execution_env=None,
        crt_version=None,
    ).with_client_config(Config())
    actual = uas.to_string()
    assert actual == f'Botocore/{botocore_version} ua/2.1 os/other lang/python'


def test_from_environment(monkeypatch):
    monkeypatch.setenv('AWS_EXECUTION_ENV', 'lambda')
    monkeypatch.setattr(platform, 'system', lambda: 'Linux')
    monkeypatch.setattr(
        platform, 'release', lambda: '5.4.228-131.415.AMZN2.X86_64'
    )
    monkeypatch.setattr(platform, 'python_version', lambda: '4.3.2')
    monkeypatch.setattr(platform, 'python_implementation', lambda: 'CPython')

    uas = UserAgentString.from_environment()

    assert uas._execution_env == 'lambda'
    assert uas._platform_name == 'Linux'
    assert uas._platform_version == '5.4.228-131.415.AMZN2.X86_64'
    assert uas._python_version == '4.3.2'
    assert uas._python_implementation == 'CPython'


@requires_crt()
def test_from_environment_can_read_crt_version(monkeypatch):
    import awscrt

    monkeypatch.setattr(awscrt, '__version__', 'a.b.c')
    uas = UserAgentString.from_environment()
    assert uas._crt_version == 'a.b.c'


def test_from_environment_with_most_values_not_available(monkeypatch):
    # Asserts that ``None`` values are properly passed through to the
    # UserAgentString class. There are separate tests to assert that
    # ``UserAgentString.to_string()`` can handle ``None`` values.
    monkeypatch.delenv('AWS_EXECUTION_ENV', raising=False)
    monkeypatch.setattr(platform, 'system', lambda: None)
    monkeypatch.setattr(platform, 'release', lambda: None)
    monkeypatch.setattr(platform, 'python_version', lambda: None)
    monkeypatch.setattr(platform, 'python_implementation', lambda: None)

    uas = UserAgentString.from_environment()

    assert uas._execution_env is None
    assert uas._platform_name is None
    assert uas._platform_version is None
    assert uas._python_version is None
    assert uas._python_implementation is None


def test_from_environment_unknown_platform(monkeypatch):
    monkeypatch.setattr(platform, 'system', lambda: 'FooOS')
    monkeypatch.setattr(platform, 'release', lambda: '0.0.1')
    uas = UserAgentString.from_environment()
    assert ' os/other md/FooOS#0.0.1 ' in uas.to_string()


def test_user_agent_string_with_registered_features(client_context):
    uas = UserAgentString.from_environment()
    uas.set_client_features({'A'})
    register_feature_id('WAITER')

    uafields = uas.to_string().split(' ')
    feature_field = [field for field in uafields if field.startswith('m/')][0]
    feature_list = feature_field[2:].split(',')
    assert sorted(feature_list) == ['A', 'B']


def test_register_feature_id(client_context):
    register_feature_id('WAITER')
    ctx = get_context()
    assert ctx.features == {'B'}


def test_register_unknown_feature_id_skips(client_context):
    register_feature_id('MY_FEATURE')
    ctx = get_context()
    assert ctx.features == set()


def test_user_agent_truncated_string():
    size_config = UserAgentComponentSizeConfig(4, ',')
    component = UserAgentComponent(
        'm',
        'A,BCD',
        size_config=size_config,
    )
    assert component.to_string() == 'm/A'


def test_user_agent_empty_truncated_string_logs(caplog):
    caplog.set_level(logging.DEBUG)
    size_config = UserAgentComponentSizeConfig(1, ',')
    component = UserAgentComponent(
        'm',
        'A,B,C',
        size_config=size_config,
    )
    assert component.to_string() == ''
    assert 'could not be truncated' in caplog.text


def test_non_positive_user_agent_component_size_config_raises():
    with pytest.raises(ValueError) as excinfo:
        UserAgentComponentSizeConfig(0, ',')
    assert 'Invalid `max_size_in_bytes`' in str(excinfo.value)
    with pytest.raises(ValueError) as excinfo:
        UserAgentComponentSizeConfig(-1, ',')
    assert 'Invalid `max_size_in_bytes`' in str(excinfo.value)


def test_hash_in_user_agent_appid():
    ua = UserAgentString(
        platform_name='linux',
        platform_version='1.2.3-foo',
        platform_machine='x86_64',
        python_version='3.8.20',
        python_implementation='Dpython',
        execution_env='AWS_Lambda_python3.8',
    ).with_client_config(Config(user_agent_appid='fooapp#1.0.0'))

    actual = ua.to_string()
    expected = (
        f'Botocore/{botocore_version} '
        'ua/2.1 '
        'os/linux#1.2.3-foo '
        'md/arch#x86_64 '
        'lang/python#3.8.20 '
        'md/pyimpl#Dpython '
        'exec-env/AWS_Lambda_python3.8 '
        'app/fooapp#1.0.0'
    )
    assert actual == expected


def _create_user_agent_string():
    return UserAgentString(
        platform_name='linux',
        platform_version='1.2.3-foo',
        platform_machine='x86_64',
        python_version='3.8.20',
        python_implementation='Dpython',
        execution_env='AWS_Lambda_python3.8',
    )


def _split_feature_field(ua_string):
    """Return the ``m/`` members as a set and the other fields as a list."""
    features = set()
    other_fields = []
    for field in ua_string.split(' '):
        if field.startswith('m/'):
            features = set(field[2:].split(','))
        else:
            other_fields.append(field)
    return features, other_fields


@mock.patch.object(
    botocore.useragent, 'modify_components', unmodified_components
)
def test_cached_user_agent_reads_request_features_on_each_call(
    client_context,
):
    uas = _create_user_agent_string().with_client_config(
        Config(retries={'mode': 'standard'})
    )
    uas.set_client_features({'A'})
    first = uas.to_string()
    static_parts = uas._static_parts
    assert static_parts is not None
    assert first == uas._build_uncached_ua_string()

    register_feature_id('WAITER')
    second = uas.to_string()
    assert uas._static_parts is static_parts
    assert second == uas._build_uncached_ua_string()

    register_feature_id('PAGINATOR')
    third = uas.to_string()
    assert uas._static_parts is static_parts
    assert third == uas._build_uncached_ua_string()

    first_features, first_fields = _split_feature_field(first)
    second_features, second_fields = _split_feature_field(second)
    third_features, third_fields = _split_feature_field(third)
    assert first_features == {'A'}
    assert second_features == {'A', 'B'}
    assert third_features == {'A', 'B', 'C'}
    assert first_fields == second_fields == third_fields


def test_supplied_user_agent_set_after_with_client_config():
    # Client creation sets ``_supplied_user_agent`` after
    # ``with_client_config()``.
    config = Config(user_agent='preliminary/1.0', user_agent_extra='cfg/extra')
    uas = _create_user_agent_string().with_client_config(config)
    assert uas.to_string() == 'preliminary/1.0 cfg/extra'

    config._supplied_user_agent = None
    ua_string = uas.to_string()
    assert ua_string.startswith(f'Botocore/{botocore_version} ')
    assert ua_string.endswith(' cfg/extra')
    assert ua_string == uas._build_uncached_ua_string()

    config._supplied_user_agent = 'custom/2.0'
    assert uas.to_string() == 'custom/2.0 cfg/extra'


def test_with_client_config_copy_builds_its_own_cache():
    parent = _create_user_agent_string().with_client_config(
        Config(user_agent_appid='parentapp')
    )
    parent_string = parent.to_string()
    assert 'app/parentapp' in parent_string.split(' ')

    child = parent.with_client_config(Config(user_agent_appid='childapp'))
    assert child._static_parts is None
    child_fields = child.to_string().split(' ')
    assert 'app/childapp' in child_fields
    assert 'app/parentapp' not in child_fields
    assert parent.to_string() == parent_string


@pytest.mark.parametrize(
    'change, expected_field',
    [
        pytest.param(
            lambda uas, config: setattr(config, 'user_agent_extra', 'extra/1'),
            'extra/1',
            id='user_agent_extra',
        ),
        pytest.param(
            lambda uas, config: setattr(config, 'user_agent_appid', 'newapp'),
            'app/newapp',
            id='user_agent_appid',
        ),
        pytest.param(
            lambda uas, config: config.retries.update(mode='adaptive'),
            'cfg/retry-mode#adaptive',
            id='retries_mode_in_place',
        ),
        pytest.param(
            lambda uas, config: setattr(config, 'retries', {'mode': 'legacy'}),
            'cfg/retry-mode#legacy',
            id='retries',
        ),
        pytest.param(
            lambda uas, config: setattr(
                config, 'endpoint_discovery_enabled', True
            ),
            'cfg/endpoint-discovery',
            id='endpoint_discovery_enabled',
        ),
        pytest.param(
            lambda uas, config: uas.set_session_config('MyTool', '1.0', None),
            'MyTool/1.0',
            id='session_name_and_version',
        ),
        pytest.param(
            lambda uas, config: uas.set_session_config(None, None, 'sess/1'),
            'sess/1',
            id='session_extra',
        ),
    ],
)
def test_change_after_first_render_updates_user_agent(change, expected_field):
    config = Config(retries={'mode': 'standard'})
    uas = _create_user_agent_string().with_client_config(config)
    assert expected_field not in uas.to_string().split(' ')

    change(uas, config)
    ua_string = uas.to_string()
    assert expected_field in ua_string.split(' ')
    assert ua_string == uas._build_uncached_ua_string()


@mock.patch.object(
    botocore.useragent, 'modify_components', unmodified_components
)
def test_custom_modify_components_bypasses_cache(client_context):
    received = []

    def modify_components(components):
        received.append([comp.to_string() for comp in components])
        return [*components, RawStringUserAgentComponent('custom/1')]

    uas = _create_user_agent_string().with_client_config(Config())
    with mock.patch.object(
        botocore.useragent, 'modify_components', modify_components
    ):
        register_feature_id('WAITER')
        first = uas.to_string()
        register_feature_id('PAGINATOR')
        second = uas.to_string()
        assert uas._static_parts is None

    assert len(received) == 2
    assert 'm/B' in received[0]
    second_features = [c for c in received[1] if c.startswith('m/')]
    assert len(second_features) == 1
    assert set(second_features[0][2:].split(',')) == {'B', 'C'}
    assert first.endswith(' custom/1')
    assert second.endswith(' custom/1')

    assert 'custom/1' not in uas.to_string()
    assert uas._static_parts is not None


def test_custom_modify_components_without_client_config():
    def modify_components(components):
        return components

    uas = _create_user_agent_string()
    with mock.patch.object(
        botocore.useragent, 'modify_components', modify_components
    ):
        assert uas.to_string().startswith(f'Botocore/{botocore_version} ')


def test_concurrent_renders_use_their_own_request_features():
    feature_ids = [
        'WAITER',
        'PAGINATOR',
        'RETRY_MODE_LEGACY',
        'RETRY_MODE_STANDARD',
        'RETRY_MODE_ADAPTIVE',
        'S3_TRANSFER',
        'GZIP_REQUEST_COMPRESSION',
        'PROTOCOL_RPC_V2_CBOR',
    ]
    # The threads share one object with an empty cache.
    uas = _create_user_agent_string().with_client_config(
        Config(retries={'mode': 'standard'})
    )
    uas.set_client_features({'A'})
    barrier = threading.Barrier(len(feature_ids), timeout=30)
    results = {}

    def render(feature_id):
        with start_as_current_context(ClientContext()):
            register_feature_id(feature_id)
            barrier.wait()
            results[feature_id] = [uas.to_string() for _ in range(200)]

    threads = [
        threading.Thread(target=render, args=(feature_id,))
        for feature_id in feature_ids
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    _, expected_fields = _split_feature_field(uas.to_string())
    for feature_id in feature_ids:
        code = botocore.useragent._USERAGENT_FEATURE_MAPPINGS[feature_id]
        assert len(results[feature_id]) == 200
        for ua_string in results[feature_id]:
            features, other_fields = _split_feature_field(ua_string)
            assert features == {'A', code}
            assert other_fields == expected_fields
