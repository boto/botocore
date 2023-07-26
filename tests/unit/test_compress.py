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
import gzip
import io
from copy import deepcopy

import pytest

from botocore.compat import urlencode
from botocore.compress import COMPRESSION_MAPPING, maybe_compress_request
from botocore.config import Config
from tests import mock


def _make_op(
    request_compression=None,
    has_streaming_input=False,
    streaming_metadata=None,
):
    op = mock.Mock()
    op.request_compression = request_compression
    op.has_streaming_input = has_streaming_input
    if streaming_metadata is not None:
        streaming_shape = mock.Mock()
        streaming_shape.metadata = streaming_metadata
        op.get_streaming_input.return_value = streaming_shape
    return op


OP_NO_COMPRESSION = _make_op()
OP_WITH_COMPRESSION = _make_op({'encodings': ['gzip']})
OP_UNKNOWN_COMPRESSION = _make_op({'encodings': ['foo']})
OP_MULTIPLE_COMPRESSIONS = _make_op({'encodings': ['gzip', 'foo']})
STREAMING_OP_WITH_COMPRESSION = _make_op(
    {'encodings': ['gzip']},
    True,
    {},
)
STREAMING_OP_WITH_COMPRESSION_REQUIRES_LENGTH = _make_op(
    {'encodings': ['gzip']},
    True,
    {'requiresLength': True},
)
REQUEST_BODY = (
    b'Action=PutMetricData&Version=2010-08-01&Namespace=Namespace'
    b'&MetricData.member.1.MetricName=metric&MetricData.member.1.Unit=Bytes'
    b'&MetricData.member.1.Value=128'
)

REQUEST_BODY_STRING = REQUEST_BODY.decode('utf-8')

DEFAULT_COMPRESSION_CONFIG = Config(
    disable_request_compression=False,
    request_min_compression_size_bytes=10420,
)
COMPRESSION_CONFIG_128_BYTES = Config(
    disable_request_compression=False,
    request_min_compression_size_bytes=128,
)
COMPRESSION_CONFIG_1_BYTE = Config(
    disable_request_compression=False,
    request_min_compression_size_bytes=1,
)


class NonSeekableStream:
    def __init__(self, buffer):
        self._buffer = buffer

    def read(self, size=None):
        return self._buffer.read(size)


def _request_dict(body=None, headers=None):
    if body is None:
        body = b''
    if headers is None:
        headers = {}

    return {
        'body': body,
        'headers': headers,
    }


def default_request_dict():
    return _request_dict(REQUEST_BODY)


def request_dict_string():
    return _request_dict(REQUEST_BODY_STRING)


def request_dict_bytearray():
    return _request_dict(bytearray(REQUEST_BODY))


def request_dict_with_content_encoding_header():
    return _request_dict(
        REQUEST_BODY, {'foo': b'bar', 'Content-Encoding': 'identity'}
    )


def request_dict_string_io():
    return _request_dict(io.StringIO(REQUEST_BODY_STRING))


def request_dict_bytes_io():
    return _request_dict(io.BytesIO(REQUEST_BODY))


def request_dict_non_seekable_text_stream():
    return _request_dict(NonSeekableStream(io.StringIO(REQUEST_BODY_STRING)))


def request_dict_non_seekable_bytes_stream():
    return _request_dict(NonSeekableStream(io.BytesIO(REQUEST_BODY)))


def request_dict_dict():
    return _request_dict({'foo': 'bar'})


DECOMPRESSION_METHOD_MAP = {'gzip': gzip.decompress}


def _bad_compression(body):
    raise ValueError('Reached unintended compression algorithm "foo"')


MOCK_COMPRESSION = {'foo': _bad_compression}
MOCK_COMPRESSION.update(COMPRESSION_MAPPING)


def _assert_compression_body(original_body, compressed_body, encoding):
    if hasattr(original_body, 'read'):
        original_body = original_body.read()
        compressed_body = compressed_body.read()
    if isinstance(original_body, dict):
        original_body = urlencode(original_body, doseq=True, encoding='utf-8')
    if isinstance(original_body, str):
        original_body = original_body.encode('utf-8')
    decompress = DECOMPRESSION_METHOD_MAP[encoding]
    assert original_body == decompress(compressed_body)


def _assert_compression_header(headers, encoding):
    assert (
        'Content-Encoding' in headers
        and encoding in headers['Content-Encoding']
    )


def assert_compression(original_body, request_dict, encoding):
    compressed_body = request_dict['body']
    headers = request_dict['headers']
    _assert_compression_body(original_body, compressed_body, encoding)
    _assert_compression_header(headers, encoding)


@pytest.mark.parametrize(
    'config, request_dict, operation_model, encoding',
    [
        (
            COMPRESSION_CONFIG_128_BYTES,
            default_request_dict(),
            OP_WITH_COMPRESSION,
            'gzip',
        ),
        (
            COMPRESSION_CONFIG_128_BYTES,
            default_request_dict(),
            OP_MULTIPLE_COMPRESSIONS,
            'gzip',
        ),
        (
            DEFAULT_COMPRESSION_CONFIG,
            default_request_dict(),
            STREAMING_OP_WITH_COMPRESSION,
            'gzip',
        ),
        (
            COMPRESSION_CONFIG_128_BYTES,
            request_dict_bytearray(),
            OP_WITH_COMPRESSION,
            'gzip',
        ),
        (
            COMPRESSION_CONFIG_128_BYTES,
            request_dict_with_content_encoding_header(),
            OP_WITH_COMPRESSION,
            'gzip',
        ),
        (
            COMPRESSION_CONFIG_128_BYTES,
            request_dict_string(),
            OP_WITH_COMPRESSION,
            'gzip',
        ),
        (
            COMPRESSION_CONFIG_128_BYTES,
            request_dict_bytes_io(),
            OP_WITH_COMPRESSION,
            'gzip',
        ),
        (
            COMPRESSION_CONFIG_128_BYTES,
            request_dict_string_io(),
            OP_WITH_COMPRESSION,
            'gzip',
        ),
        (
            COMPRESSION_CONFIG_1_BYTE,
            request_dict_dict(),
            OP_WITH_COMPRESSION,
            'gzip',
        ),
    ],
)
def test_compression(config, request_dict, operation_model, encoding):
    original_body = request_dict['body']
    maybe_compress_request(config, request_dict, operation_model)
    assert_compression(original_body, request_dict, encoding)


@pytest.mark.parametrize(
    'config, request_dict, operation_model, encoding',
    [
        (
            DEFAULT_COMPRESSION_CONFIG,
            request_dict_non_seekable_bytes_stream(),
            STREAMING_OP_WITH_COMPRESSION,
            'gzip',
        ),
        (
            DEFAULT_COMPRESSION_CONFIG,
            request_dict_non_seekable_text_stream(),
            STREAMING_OP_WITH_COMPRESSION,
            'gzip',
        ),
    ],
)
def test_compression_non_seekable_streams(
    config, request_dict, operation_model, encoding
):
    # since the body can't be reset, we must make a copy
    # of the original body to test against
    original_body = deepcopy(request_dict['body'])
    maybe_compress_request(config, request_dict, operation_model)
    assert_compression(original_body, request_dict, encoding)


@pytest.mark.parametrize(
    'config, request_dict, operation_model',
    [
        (
            Config(
                disable_request_compression=True,
                request_min_compression_size_bytes=1000,
            ),
            default_request_dict(),
            OP_WITH_COMPRESSION,
        ),
        (
            Config(
                disable_request_compression=False,
                request_min_compression_size_bytes=256,
            ),
            default_request_dict(),
            OP_WITH_COMPRESSION,
        ),
        (
            DEFAULT_COMPRESSION_CONFIG,
            default_request_dict(),
            STREAMING_OP_WITH_COMPRESSION_REQUIRES_LENGTH,
        ),
        (
            DEFAULT_COMPRESSION_CONFIG,
            default_request_dict(),
            OP_NO_COMPRESSION,
        ),
        (
            COMPRESSION_CONFIG_128_BYTES,
            default_request_dict(),
            OP_UNKNOWN_COMPRESSION,
        ),
        (
            DEFAULT_COMPRESSION_CONFIG,
            request_dict_string(),
            OP_WITH_COMPRESSION,
        ),
        (
            DEFAULT_COMPRESSION_CONFIG,
            request_dict_bytearray(),
            OP_WITH_COMPRESSION,
        ),
        (
            DEFAULT_COMPRESSION_CONFIG,
            request_dict_bytes_io(),
            OP_WITH_COMPRESSION,
        ),
        (
            DEFAULT_COMPRESSION_CONFIG,
            request_dict_string_io(),
            OP_WITH_COMPRESSION,
        ),
        (
            COMPRESSION_CONFIG_128_BYTES,
            request_dict_with_content_encoding_header(),
            OP_UNKNOWN_COMPRESSION,
        ),
        (
            COMPRESSION_CONFIG_1_BYTE,
            request_dict_non_seekable_bytes_stream(),
            OP_WITH_COMPRESSION,
        ),
        (
            COMPRESSION_CONFIG_1_BYTE,
            request_dict_non_seekable_text_stream(),
            OP_WITH_COMPRESSION,
        ),
    ],
)
def test_no_compression(config, request_dict, operation_model):
    ce_header = request_dict['headers'].get('Content-Encoding')
    original_body = request_dict['body']
    maybe_compress_request(config, request_dict, operation_model)
    assert request_dict['body'] is original_body
    assert ce_header is request_dict['headers'].get('Content-Encoding')


def test_dict_no_compression():
    request_dict = request_dict_dict()
    original_body = request_dict['body']
    maybe_compress_request(
        COMPRESSION_CONFIG_128_BYTES, request_dict, OP_WITH_COMPRESSION
    )
    body = request_dict['body']
    encoded_body = urlencode(original_body, doseq=True, encoding='utf-8')
    assert body == encoded_body.encode('utf-8')


@pytest.mark.parametrize('body', [1, object(), True, 1.0])
def test_maybe_compress_bad_types(body):
    request_dict = _request_dict(body)
    maybe_compress_request(
        COMPRESSION_CONFIG_1_BYTE, request_dict, OP_WITH_COMPRESSION
    )
    assert request_dict['body'] is body


@pytest.mark.parametrize(
    'request_dict',
    [request_dict_string_io(), request_dict_bytes_io()],
)
def test_body_streams_position_reset(request_dict):
    maybe_compress_request(
        COMPRESSION_CONFIG_128_BYTES,
        request_dict,
        OP_WITH_COMPRESSION,
    )
    assert request_dict['body'].tell() == 0


def test_only_compress_once():
    with mock.patch('botocore.compress.COMPRESSION_MAPPING', MOCK_COMPRESSION):
        request_dict = default_request_dict()
        body = request_dict['body']
        maybe_compress_request(
            COMPRESSION_CONFIG_128_BYTES, request_dict, OP_WITH_COMPRESSION
        )
        assert_compression(body, request_dict, 'gzip')
