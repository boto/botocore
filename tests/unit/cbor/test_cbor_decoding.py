import io
import json
import struct

import pytest

from botocore.parsers import ResponseParserError, RpcV2CBORParser

IGNORE_CASES = [
    # We ignore all the tag tests since none of them are supported tags in AWS.
    # The majority of these aren't even defined tags in CBOR and just test that we
    # can properly parse the number
    'tag - 0/min',
    'tag - 1/min',
    'tag - 2/min',
    'tag - 4/min',
    'tag - 8/min',
    'tag - 0/max',
    'tag - 1/max',
    'tag - 2/max',
    'tag - 4/max',
    'tag - 8/max',
    # We are expected to drop keys with null values, which is the opposite of the
    # assertion in these two map tests
    'map - {_ null}',
    'map - {null}',
]


@pytest.fixture(scope="module")
def parser():
    return RpcV2CBORParser()


def _get_cbor_decoding_success_tests():
    success_test_data = json.load(open('decode-success-tests.json'))
    for case in success_test_data:
        yield case['description'], case['input'], case['expect']


def _get_cbor_decoding_error_tests():
    success_test_data = json.load(open('decode-error-tests.json'))
    for case in success_test_data:
        yield case['description'], case['input'], case['error']


@pytest.mark.parametrize(
    "json_description, input, expect", _get_cbor_decoding_success_tests()
)
def test_cbor_decoding_success(json_description, input, expect, parser):
    if json_description in IGNORE_CASES:
        pytest.skip("Intentionally skipped CBOR case")
    stream = io.BytesIO(bytearray.fromhex(input))
    parsed = parser.parse_data_item(stream)
    _assert_expected_value(parsed, expect)


@pytest.mark.parametrize(
    "json_description, input, error", _get_cbor_decoding_error_tests()
)
def test_cbor_decoding_error(json_description, input, error, parser):
    stream = io.BytesIO(bytearray.fromhex(input))
    with pytest.raises(ResponseParserError):
        parser.parse_data_item(stream)


def _assert_expected_value(actual, expected):
    for expected_key, value in expected.items():
        if expected_key in ['null', 'undefined']:
            assert actual is None
        elif expected_key == 'bytestring':
            assert actual == bytes(value)
        elif expected_key == 'list':
            assert isinstance(actual, list)
            for act_val, exp_val in zip(actual, value):
                _assert_expected_value(act_val, exp_val)
        elif expected_key == 'map':
            assert isinstance(actual, dict)
            for key, val in value.items():
                assert key in actual
                _assert_expected_value(actual[key], val)
        elif expected_key == 'tag':
            assert actual.tag == value['id']
            assert actual.value == value['value']['uint']
        elif expected_key in ['float32', 'float64']:
            struct_format = '<f' if expected_key == 'float32' else '<d'
            packed_value = struct.pack(
                '<I' if expected_key == 'float32' else '<Q', value
            )
            unpacked_value = struct.unpack(struct_format, packed_value)[0]
            assert actual == unpacked_value
        else:
            assert actual == value
