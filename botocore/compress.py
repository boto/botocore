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
"""
NOTE: All functions in this module are considered private and are
subject to abrupt breaking changes. Please do not use them directly.

"""

import io
import logging
from gzip import GzipFile
from gzip import compress as gzip_compress

from botocore.compat import urlencode
from botocore.exceptions import InvalidConfigError
from botocore.useragent import register_feature_id
from botocore.utils import determine_content_length

logger = logging.getLogger(__name__)


def maybe_compress_request(config, request_dict, operation_model):
    """Attempt to compress the request body using the modeled encodings."""
    if _should_compress_request(config, request_dict, operation_model):
        encodings = operation_model.request_compression['encodings']
        if config.request_compression_encoding is not None:
            encodings = [config.request_compression_encoding]
        for encoding in encodings:
            encoder = COMPRESSION_MAPPING.get(encoding)
            if encoder is not None:
                logger.debug('Compressing request with %s encoding.', encoding)
                request_dict['body'] = encoder(request_dict['body'])
                # The request preparer recalculates length for the new body,
                # or preserves an existing transfer encoding when present.
                for name in list(request_dict['headers']):
                    if name.lower() == 'content-length':
                        del request_dict['headers'][name]
                _set_compression_header(request_dict['headers'], encoding)
                return
            else:
                logger.debug('Unsupported compression encoding: %s', encoding)


def _should_compress_request(config, request_dict, operation_model):
    encoding = config.request_compression_encoding
    if encoding is not None:
        if (
            encoding not in COMPRESSION_MAPPING
            or config.disable_request_compression is True
            or config.signature_version == 'v2'
            or operation_model.request_compression is None
            or encoding
            not in (
                advertised.lower()
                for advertised in operation_model.request_compression[
                    'encodings'
                ]
            )
        ):
            raise InvalidConfigError(
                error_msg=(
                    f'Request compression encoding "{encoding}" is not '
                    'supported for this operation or configuration.'
                )
            )
    if (
        config.disable_request_compression is not True
        and config.signature_version != 'v2'
        and operation_model.request_compression is not None
    ):
        if not _is_compressible_type(request_dict):
            if encoding is not None:
                raise InvalidConfigError(
                    error_msg=f'Cannot apply {encoding} to this request body.'
                )
            body_type = type(request_dict['body'])
            log_msg = 'Body type %s does not support compression.'
            logger.debug(log_msg, body_type)
            return False

        if operation_model.has_streaming_input:
            streaming_input = operation_model.get_streaming_input()
            streaming_metadata = streaming_input.metadata
            if encoding is not None and 'requiresLength' in streaming_metadata:
                raise InvalidConfigError(
                    error_msg=(
                        f'Cannot apply {encoding} to a streaming input '
                        'that requires length.'
                    )
                )
            return 'requiresLength' not in streaming_metadata

        if encoding is not None:
            return True
        body_size = _get_body_size(request_dict['body'])
        min_size = config.request_min_compression_size_bytes
        return min_size <= body_size

    return False


def _is_compressible_type(request_dict):
    body = request_dict['body']
    # Coerce dict to a format compatible with compression.
    if isinstance(body, dict):
        body = urlencode(body, doseq=True, encoding='utf-8').encode('utf-8')
        request_dict['body'] = body
    is_supported_type = isinstance(body, (str, bytes, bytearray))
    return is_supported_type or hasattr(body, 'read')


def _get_body_size(body):
    size = determine_content_length(body)
    if size is None:
        logger.debug(
            'Unable to get length of the request body: %s. '
            'Skipping compression.',
            body,
        )
        size = 0
    return size


def _gzip_compress_body(body):
    register_feature_id('GZIP_REQUEST_COMPRESSION')
    if isinstance(body, str):
        return gzip_compress(body.encode('utf-8'))
    elif isinstance(body, (bytes, bytearray)):
        return gzip_compress(body)
    elif hasattr(body, 'read'):
        if hasattr(body, 'seek') and hasattr(body, 'tell'):
            current_position = body.tell()
            compressed_obj = _gzip_compress_fileobj(body)
            body.seek(current_position)
            return compressed_obj
        return _gzip_compress_fileobj(body)


def _gzip_compress_fileobj(body):
    compressed_obj = io.BytesIO()
    with GzipFile(fileobj=compressed_obj, mode='wb') as gz:
        while True:
            chunk = body.read(8192)
            if not chunk:
                break
            if isinstance(chunk, str):
                chunk = chunk.encode('utf-8')
            gz.write(chunk)
    compressed_obj.seek(0)
    return compressed_obj


def _set_compression_header(headers, encoding):
    encodings = []
    for name in list(headers):
        if name.lower() == 'content-encoding':
            value = headers.pop(name)
            if value is not None:
                encodings.append(value)
    encodings.append(encoding)
    headers['Content-Encoding'] = ','.join(encodings)


COMPRESSION_MAPPING = {'gzip': _gzip_compress_body}
