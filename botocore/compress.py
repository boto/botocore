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
import logging

from botocore.utils import determine_content_length

logger = logging.getLogger(__name__)


class RequestCompressor:
    """A class that can compress a request body."""

    @classmethod
    def compress(cls, config, request_dict, operation_model):
        """Attempt to compress the request body using the modeled encodings."""
        body = request_dict['body']
        if cls._should_compress_request(config, body, operation_model):
            for encoding in operation_model.request_compression['encodings']:
                encoder = getattr(cls, f'_{encoding}_compress_body', None)
                if encoder is not None:
                    logger.debug(
                        'Compressing request with %s encoding.', encoding
                    )
                    request_dict['body'] = encoder(body)
                    cls._set_compression_header(
                        request_dict['headers'], encoding
                    )
                    return
                else:
                    logger.debug(
                        'Unsupported compression encoding: %s', encoding
                    )

    @classmethod
    def _should_compress_request(cls, config, body, operation_model):
        if (
            config.disable_request_compression is not True
            and config.signature_version != 'v2'
            and operation_model.request_compression is not None
        ):
            # Request is compressed no matter the content length if it has a streaming input.
            # However, if the stream has the `requiresLength` trait it is NOT compressed.
            if operation_model.has_streaming_input:
                return (
                    'requiresLength'
                    not in operation_model.get_streaming_input().metadata
                )
            return (
                config.request_min_compression_size_bytes
                <= cls._get_body_size(body)
            )
        return False

    @classmethod
    def _gzip_compress_body(cls, body):
        if isinstance(body, str):
            return gzip.compress(body.encode('utf-8'))
        elif isinstance(body, (bytes, bytearray)):
            return gzip.compress(body)
        elif hasattr(body, 'read'):
            if hasattr(body, 'seek') and hasattr(body, 'tell'):
                current_position = body.tell()
                compressed_obj = cls._gzip_compress_fileobj(body)
                body.seek(current_position)
                return compressed_obj
            return cls._gzip_compress_fileobj(body)

    @staticmethod
    def _gzip_compress_fileobj(body):
        compressed_obj = io.BytesIO()
        with gzip.GzipFile(fileobj=compressed_obj, mode='wb') as gz:
            while True:
                chunk = body.read(8192)
                if not chunk:
                    break
                if isinstance(chunk, str):
                    chunk = chunk.encode('utf-8')
                gz.write(chunk)
        compressed_obj.seek(0)
        return compressed_obj

    @staticmethod
    def _get_body_size(body):
        size = determine_content_length(body)
        if size is None:
            logger.debug(
                'Unable to get length of the request body: %s. '
                'Skipping compression.',
                body,
            )
            size = -1
        return size

    @staticmethod
    def _set_compression_header(headers, encoding):
        ce_header = headers.get('Content-Encoding')
        if ce_header is None:
            headers['Content-Encoding'] = encoding
        elif encoding not in ce_header.split(','):
            headers['Content-Encoding'] = f'{ce_header},{encoding}'
