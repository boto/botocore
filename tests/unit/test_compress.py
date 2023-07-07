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
import io

import pytest

from botocore.compress import RequestCompressor
from botocore.config import Config
from tests import mock


def _op_with_compression():
    op = mock.Mock()
    op.request_compression = {'encodings': ['gzip']}
    op.has_streaming_input = False
    return op


def _op_unknown_compression():
    op = mock.Mock()
    op.request_compression = {'encodings': ['foo']}
    op.has_streaming_input = None
    return op


def _op_without_compression():
    op = mock.Mock()
    op.request_compression = None
    op.has_streaming_input = False
    return op


def _streaming_op_with_compression():
    op = _op_with_compression()
    op.has_streaming_input = True
    streaming_shape = mock.Mock()
    streaming_shape.metadata = {}
    op.get_streaming_input.return_value = streaming_shape
    return op


def _streaming_op_with_compression_requires_length():
    op = _streaming_op_with_compression()
    streaming_shape = mock.Mock()
    streaming_shape.metadata = {'requiresLength': True}
    op.get_streaming_input.return_value = streaming_shape
    return op


OP_WITH_COMPRESSION = _op_with_compression()
OP_UNKNOWN_COMPRESSION = _op_unknown_compression()
STREAMING_OP_WITH_COMPRESSION = _streaming_op_with_compression()
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


COMPRESSION_HEADERS = {'gzip': b'\x1f\x8b'}


def _assert_compression(is_compressed, body, encoding):
    if hasattr(body, 'read'):
        header = body.read(2)
    else:
        header = body[:2]
    assert is_compressed == (header == COMPRESSION_HEADERS.get(encoding))


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
            DEFAULT_COMPRESSION_CONFIG,
            request_dict(),
            STREAMING_OP_WITH_COMPRESSION,
            True,
            'gzip',
        ),
        (
            DEFAULT_COMPRESSION_CONFIG,
            request_dict(),
            _streaming_op_with_compression_requires_length(),
            False,
            None,
        ),
        (
            DEFAULT_COMPRESSION_CONFIG,
            request_dict(),
            _op_without_compression(),
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
    ],
)
def test_compress(
    config,
    request_dict,
    operation_model,
    is_compressed,
    encoding,
):
    RequestCompressor.compress(config, request_dict, operation_model)
    _assert_compression(is_compressed, request_dict['body'], encoding)
    assert (
        'headers' in request_dict
        and 'Content-Encoding' in request_dict['headers']
        and encoding in request_dict['headers']['Content-Encoding']
    ) == is_compressed


@pytest.mark.parametrize('body', [1, object(), None, True, 1.0])
def test_compress_bad_types(body):
    request_dict = {'body': body, 'headers': {}}
    RequestCompressor.compress(
        COMPRESSION_CONFIG_0_BYTES, request_dict, OP_WITH_COMPRESSION
    )
    assert request_dict['body'] == body


@pytest.mark.parametrize(
    'body',
    [io.StringIO('foo'), io.BytesIO(b'foo')],
)
def test_body_streams_position_reset(body):
    RequestCompressor.compress(
        COMPRESSION_CONFIG_0_BYTES,
        {'body': body, 'headers': {}},
        OP_WITH_COMPRESSION,
    )
    assert body.tell() == 0
