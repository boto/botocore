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

import base64
import copy
import gzip
import struct
import zlib

import pytest

from botocore.compress import COMPRESSION_MAPPING
from botocore.config import Config
from botocore.exceptions import InvalidConfigError
from tests import ALL_SERVICES, ClientHTTPStubber, patch_load_service_model
from tests.functional.test_useragent import (
    get_captured_ua_strings,
    parse_registered_feature_ids,
)

FAKE_MODEL = {
    "version": "2.0",
    "documentation": "",
    "metadata": {
        "apiVersion": "2020-02-02",
        "endpointPrefix": "otherservice",
        "protocol": "query",
        "serviceFullName": "Other Service",
        "serviceId": "Other Service",
        "signatureVersion": "v4",
        "signingName": "otherservice",
        "uid": "otherservice-2020-02-02",
    },
    "operations": {
        "MockOperation": {
            "name": "MockOperation",
            "http": {"method": "POST", "requestUri": "/"},
            "input": {"shape": "MockOperationRequest"},
            "documentation": "",
            "requestcompression": {
                "encodings": ["gzip"],
            },
        },
    },
    "shapes": {
        "MockOpParamList": {
            "type": "list",
            "member": {"shape": "MockOpParam"},
        },
        "MockOpParam": {
            "type": "structure",
            "members": {"MockOpParam": {"shape": "MockOpParamValue"}},
        },
        "MockOpParamValue": {
            "type": "string",
        },
        "MockOperationRequest": {
            "type": "structure",
            "required": ["MockOpParamList"],
            "members": {
                "MockOpParamList": {
                    "shape": "MockOpParamList",
                    "documentation": "",
                },
            },
        },
    },
}

FAKE_RULESET = {
    "version": "1.0",
    "parameters": {},
    "rules": [
        {
            "conditions": [],
            "type": "endpoint",
            "endpoint": {
                "url": "https://foo.bar",
                "properties": {},
                "headers": {},
            },
        }
    ],
}


def _all_compression_operations():
    for service_model in ALL_SERVICES:
        for operation_name in service_model.operation_names:
            operation_model = service_model.operation_model(operation_name)
            if operation_model.request_compression is not None:
                yield operation_model


@pytest.mark.parametrize("operation_model", _all_compression_operations())
def test_no_unknown_compression_encodings(operation_model):
    for encoding in operation_model.request_compression["encodings"]:
        assert encoding in COMPRESSION_MAPPING.keys(), (
            f"Found unknown compression encoding '{encoding}' "
            f"in operation {operation_model.name}."
        )


def test_compression(patched_session, monkeypatch):
    patch_load_service_model(
        patched_session, monkeypatch, FAKE_MODEL, FAKE_RULESET
    )
    client = patched_session.create_client(
        "otherservice",
        region_name="us-west-2",
        config=Config(request_min_compression_size_bytes=100),
    )
    with ClientHTTPStubber(client, strict=True) as http_stubber:
        http_stubber.add_response(status=200, body=b"<response/>")
        params_list = [
            {"MockOpParam": f"MockOpParamValue{i}"} for i in range(1, 21)
        ]
        client.mock_operation(MockOpParamList=params_list)
        param_template = (
            "MockOpParamList.member.{i}.MockOpParam=MockOpParamValue{i}"
        )
        serialized_params = "&".join(
            param_template.format(i=i) for i in range(1, 21)
        )
        additional_params = "Action=MockOperation&Version=2020-02-02"
        serialized_body = f"{additional_params}&{serialized_params}"
        actual_body = gzip.decompress(http_stubber.requests[0].body)
        assert serialized_body.encode('utf-8') == actual_body


def test_user_agent_has_gzip_feature_id(patched_session, monkeypatch):
    patch_load_service_model(
        patched_session, monkeypatch, FAKE_MODEL, FAKE_RULESET
    )
    client = patched_session.create_client(
        "otherservice",
        region_name="us-west-2",
        config=Config(request_min_compression_size_bytes=100),
    )
    with ClientHTTPStubber(client, strict=True) as http_stubber:
        http_stubber.add_response(status=200, body=b"<response/>")
        params_list = [
            {"MockOpParam": f"MockOpParamValue{i}"} for i in range(1, 21)
        ]
        # The mock operation registers `'GZIP_REQUEST_COMPRESSION': 'L'`
        client.mock_operation(MockOpParamList=params_list)
    ua_string = get_captured_ua_strings(http_stubber)[0]
    feature_list = parse_registered_feature_ids(ua_string)
    assert 'L' in feature_list


def test_explicit_gzip_signs_and_retries_compressed_request(
    patched_session, monkeypatch
):
    model = copy.deepcopy(FAKE_MODEL)
    model['operations']['MockOperation']['httpChecksumRequired'] = True
    patch_load_service_model(patched_session, monkeypatch, model, FAKE_RULESET)
    client = patched_session.create_client(
        'otherservice',
        region_name='us-west-2',
        config=Config(
            request_compression_encoding='gzip',
            request_min_compression_size_bytes=1048576,
            retries={'mode': 'standard', 'max_attempts': 1},
        ),
    )
    signing_bodies = []

    def capture_signing_body(request, **kwargs):
        signing_bodies.append(request.body)
        expected_crc32 = base64.b64encode(
            struct.pack('!I', zlib.crc32(request.body) & 0xFFFFFFFF)
        ).decode('ascii')
        assert request.headers['x-amz-checksum-crc32'] == expected_crc32
        assert request.headers['Content-Encoding'] == 'gzip'

    client.meta.events.register('before-sign', capture_signing_body)
    monkeypatch.setattr('botocore.endpoint.time.sleep', lambda duration: None)
    with ClientHTTPStubber(client, strict=True) as http_stubber:
        http_stubber.add_response(
            status=500, body=b'<Error><Code>InternalFailure</Code></Error>'
        )
        http_stubber.add_response(status=200, body=b'<response/>')
        client.mock_operation(MockOpParamList=[{'MockOpParam': 'small'}])
    assert len(http_stubber.requests) == 2
    assert len(signing_bodies) == 2
    body = http_stubber.requests[0].body
    assert gzip.decompress(body) == (
        b'Action=MockOperation&Version=2020-02-02&'
        b'MockOpParamList.member.1.MockOpParam=small'
    )
    assert signing_bodies == [body, body]
    for request in http_stubber.requests:
        assert request.body == body
        assert int(request.headers['Content-Length']) == len(body)
        assert request.headers['Content-Encoding'] == b'gzip'
        assert b'content-encoding' in request.headers['Authorization']


def test_explicit_gzip_rejects_unmodeled_bedrock_before_send(patched_session):
    client = patched_session.create_client(
        'bedrock-runtime',
        region_name='us-west-2',
        config=Config(request_compression_encoding='gzip'),
    )
    with ClientHTTPStubber(client, strict=True) as http_stubber:
        with pytest.raises(InvalidConfigError, match='gzip'):
            client.converse(
                modelId='test-model',
                messages=[{'role': 'user', 'content': [{'text': 'hello'}]}],
            )
    assert http_stubber.requests == []


@pytest.mark.parametrize('header_case', ['lower', 'title'])
@pytest.mark.parametrize('chunked', [False, True])
def test_explicit_gzip_preserves_injected_headers_on_wire(
    patched_session, monkeypatch, header_case, chunked
):
    patch_load_service_model(
        patched_session, monkeypatch, FAKE_MODEL, FAKE_RULESET
    )
    client = patched_session.create_client(
        'otherservice',
        region_name='us-west-2',
        config=Config(request_compression_encoding='gzip'),
    )
    uncompressed = (
        b'Action=MockOperation&Version=2020-02-02&'
        b'MockOpParamList.member.1.MockOpParam=small'
    )

    def inject_headers(params, **kwargs):
        length_name = (
            'content-length' if header_case == 'lower' else 'Content-Length'
        )
        encoding_name = (
            'content-encoding'
            if header_case == 'lower'
            else 'Content-Encoding'
        )
        params['headers'][length_name] = str(len(uncompressed))
        params['headers'][encoding_name] = 'identity'
        if chunked:
            params['headers']['Transfer-Encoding'] = 'chunked'

    client.meta.events.register('before-call', inject_headers)
    with ClientHTTPStubber(client, strict=True) as http_stubber:
        http_stubber.add_response(status=200, body=b'<response/>')
        client.mock_operation(MockOpParamList=[{'MockOpParam': 'small'}])
    request = http_stubber.requests[0]
    assert gzip.decompress(request.body) == uncompressed
    if chunked:
        assert request.headers['Transfer-Encoding'] == b'chunked'
        assert 'Content-Length' not in request.headers
    else:
        assert int(request.headers['Content-Length']) == len(request.body)
    encoding_values = [
        value
        for name, value in request.headers.items()
        if name.lower() == 'content-encoding'
    ]
    assert len(encoding_values) == 1
    assert [
        value.strip()
        for value in encoding_values[0].decode('ascii').split(',')
    ] == ['identity', 'gzip']
    assert b'content-encoding' in request.headers['Authorization']
