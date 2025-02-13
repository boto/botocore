import io
import json
import struct

import pytest

from botocore.parsers import ResponseParserError, RpcV2CBORParser


@pytest.fixture(scope="module")
def parser():
    return RpcV2CBORParser()


def _get_cbor_decoding_success_tests():
    success_test_data = json.load(open('decode-success-tests.json'))
    for case in success_test_data:
        yield case['description'], case['input'], case['expect']


@pytest.mark.parametrize(
    "json_description, input, expect", _get_cbor_decoding_success_tests()
)
def test_cbor_decoding_success(json_description, input, expect, parser):
    stream = io.BytesIO(bytearray.fromhex(input))
    parsed = parser.parse_data_item(stream)
    _assert_expected_value(parsed, expect)


def _get_cbor_decoding_error_tests():
    success_test_data = json.load(open('decode-error-tests.json'))
    for case in success_test_data:
        yield case['description'], case['input'], case['error']


@pytest.mark.parametrize(
    "json_description, input, error", _get_cbor_decoding_error_tests()
)
def test_cbor_decoding_error(json_description, input, error, parser):
    stream = io.BytesIO(bytearray.fromhex(input))
    with pytest.raises(ResponseParserError):
        parser.parse_data_item(stream)


def _assert_expected_value(actual_value, expected_value):
    for expected_key, value in expected_value.items():
        if expected_key in ['null', 'undefined']:
            assert actual_value is None
        elif expected_key == 'bytestring':
            assert actual_value == bytes(value)
        elif expected_key == 'list':
            values_list = [v for d in value for v in d.values()]
            return values_list
        elif expected_key == 'map':
            for key, val in value.items():
                assert key in actual_value
                _assert_expected_value(actual_value[key], val)
        elif expected_key == 'tag':
            assert int(actual_value.timestamp()) == value['value']['uint']
        elif expected_key in ['float32', 'float64']:
            struct_format = '<f' if expected_key == 'float32' else '<d'
            packed_value = struct.pack(
                '<I' if expected_key == 'float32' else '<Q', value
            )
            unpacked_value = struct.unpack(struct_format, packed_value)[0]
            assert actual_value == unpacked_value
        else:
            assert actual_value == value
