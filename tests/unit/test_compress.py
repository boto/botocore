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


OP_WITH_COMPRESSION = _make_op(request_compression={'encodings': ['gzip']})
OP_UNKNOWN_COMPRESSION = _make_op(request_compression={'encodings': ['foo']})
OP_MULTIPLE_COMPRESSIONS = _make_op(
    request_compression={'encodings': ['gzip', 'foo']}
)
STREAMING_OP_WITH_COMPRESSION = _make_op(
    request_compression={'encodings': ['gzip']},
    has_streaming_input=True,
    streaming_metadata={},
)
STREAMING_OP_WITH_COMPRESSION_REQUIRES_LENGTH = _make_op(
    request_compression={'encodings': ['gzip']},
    has_streaming_input=True,
    streaming_metadata={'requiresLength': True},
)
REQUEST_BODY = (
    b'Action=PutMetricData&Version=2010-08-01&Namespace=Namespace'
    b'&MetricData.member.1.MetricName=metric&MetricData.member.1.Unit=Bytes'
    b'&MetricData.member.1.Value=128'
)

DEFAULT_COMPRESSION_CONFIG = Config(
    disable_request_compression=False,
    request_min_compression_size_bytes=10420,
)
COMPRESSION_CONFIG_128_BYTES = Config(
    disable_request_compression=False,
    request_min_compression_size_bytes=128,
)
COMPRESSION_CONFIG_0_BYTES = Config(
    disable_request_compression=False,
    request_min_compression_size_bytes=0,
)


def request_dict():
    return {
        'body': REQUEST_BODY,
        'headers': {'foo': 'bar'},
    }


def request_dict_with_content_encoding_header():
    return {
        'body': REQUEST_BODY,
        'headers': {'foo': 'bar', 'Content-Encoding': 'identity'},
    }


DECOMPRESSION_METHOD_MAP = {'gzip': gzip.decompress}


def _assert_compression(body, maybe_compressed_body, encoding):
    if hasattr(body, 'read'):
        body = body.read()
        maybe_compressed_body = maybe_compressed_body.read()
    if isinstance(body, str):
        body = body.encode('utf-8')
    if isinstance(body, dict) and encoding is not None:
        body = urlencode(body, doseq=True, encoding='utf-8').encode('utf-8')
    decompress_method = DECOMPRESSION_METHOD_MAP.get(
        encoding, lambda body: body
    )
    assert decompress_method(maybe_compressed_body) == body


def _bad_compression(body):
    raise ValueError('Reached unintended compression algorithm "foo"')


MOCK_COMPRESSION = {'foo': _bad_compression}
MOCK_COMPRESSION.update(COMPRESSION_MAPPING)


@pytest.mark.parametrize(
    'config, request_dict, operation_model, is_compressed, encoding',
    [
        (
            Config(
                disable_request_compression=True,
                request_min_compression_size_bytes=1000,
            ),
            {'body': b'foo', 'headers': {}},
            OP_WITH_COMPRESSION,
            False,
            None,
        ),
        (
            COMPRESSION_CONFIG_128_BYTES,
            request_dict(),
            OP_WITH_COMPRESSION,
            True,
            'gzip',
        ),
        (
            Config(
                disable_request_compression=False,
                request_min_compression_size_bytes=256,
            ),
            request_dict(),
            OP_WITH_COMPRESSION,
            False,
            None,
        ),
        (
            Config(request_min_compression_size_bytes=128),
            request_dict(),
            OP_WITH_COMPRESSION,
            True,
            'gzip',
        ),
        (
            COMPRESSION_CONFIG_128_BYTES,
            request_dict(),
            OP_MULTIPLE_COMPRESSIONS,
            True,
            'gzip',
        ),
        (
            DEFAULT_COMPRESSION_CONFIG,
            request_dict(),
            STREAMING_OP_WITH_COMPRESSION,
            True,
            'gzip',
        ),
        (
            DEFAULT_COMPRESSION_CONFIG,
            request_dict(),
            STREAMING_OP_WITH_COMPRESSION_REQUIRES_LENGTH,
            False,
            None,
        ),
        (
            DEFAULT_COMPRESSION_CONFIG,
            request_dict(),
            _make_op(),
            False,
            None,
        ),
        (
            COMPRESSION_CONFIG_128_BYTES,
            request_dict(),
            OP_UNKNOWN_COMPRESSION,
            False,
            None,
        ),
        (
            COMPRESSION_CONFIG_128_BYTES,
            {'body': REQUEST_BODY.decode(), 'headers': {}},
            OP_WITH_COMPRESSION,
            True,
            'gzip',
        ),
        (
            COMPRESSION_CONFIG_128_BYTES,
            {'body': bytearray(REQUEST_BODY), 'headers': {}},
            OP_WITH_COMPRESSION,
            True,
            'gzip',
        ),
        (
            COMPRESSION_CONFIG_128_BYTES,
            {'body': io.BytesIO(REQUEST_BODY), 'headers': {}},
            OP_WITH_COMPRESSION,
            True,
            'gzip',
        ),
        (
            COMPRESSION_CONFIG_128_BYTES,
            {'body': io.StringIO(REQUEST_BODY.decode()), 'headers': {}},
            OP_WITH_COMPRESSION,
            True,
            'gzip',
        ),
        (
            COMPRESSION_CONFIG_128_BYTES,
            request_dict_with_content_encoding_header(),
            OP_UNKNOWN_COMPRESSION,
            False,
            'foo',
        ),
        (
            COMPRESSION_CONFIG_128_BYTES,
            request_dict_with_content_encoding_header(),
            OP_WITH_COMPRESSION,
            True,
            'gzip',
        ),
        (
            COMPRESSION_CONFIG_0_BYTES,
            {'body': {'foo': 'bar'}, 'headers': {}},
            OP_WITH_COMPRESSION,
            True,
            'gzip',
        ),
        (
            COMPRESSION_CONFIG_128_BYTES,
            {'body': {'foo': 'bar'}, 'headers': {}},
            OP_WITH_COMPRESSION,
            False,
            None,
        ),
    ],
)
def test_compress(
    config,
    request_dict,
    operation_model,
    is_compressed,
    encoding,
):
    original_body = request_dict['body']
    maybe_compress_request(config, request_dict, operation_model)
    _assert_compression(original_body, request_dict['body'], encoding)
    assert (
        'headers' in request_dict
        and 'Content-Encoding' in request_dict['headers']
        and encoding in request_dict['headers']['Content-Encoding']
    ) == is_compressed


@pytest.mark.parametrize('body', [1, object(), None, True, 1.0])
def test_compress_bad_types(body):
    request_dict = {'body': body, 'headers': {}}
    maybe_compress_request(
        COMPRESSION_CONFIG_0_BYTES, request_dict, OP_WITH_COMPRESSION
    )
    assert request_dict['body'] == body


@pytest.mark.parametrize(
    'body',
    [io.StringIO('foo'), io.BytesIO(b'foo')],
)
def test_body_streams_position_reset(body):
    maybe_compress_request(
        COMPRESSION_CONFIG_0_BYTES,
        {'body': body, 'headers': {}},
        OP_WITH_COMPRESSION,
    )
    assert body.tell() == 0


def test_only_compress_once():
    with mock.patch('botocore.compress.COMPRESSION_MAPPING', MOCK_COMPRESSION):
        request_dict = {'body': REQUEST_BODY, 'headers': {}}
        maybe_compress_request(
            COMPRESSION_CONFIG_128_BYTES, request_dict, OP_WITH_COMPRESSION
        )
        _assert_compression(REQUEST_BODY, request_dict['body'], 'gzip')
