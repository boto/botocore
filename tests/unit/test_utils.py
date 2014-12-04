# Copyright 2012-2014 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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

from tests import unittest
from dateutil.tz import tzutc, tzoffset
import datetime

import mock

from botocore import xform_name
from botocore.exceptions import InvalidExpressionError, ConfigNotFound
from botocore.utils import remove_dot_segments
from botocore.utils import normalize_url_path
from botocore.utils import validate_jmespath_for_set
from botocore.utils import set_value_from_jmespath
from botocore.utils import parse_key_val_file_contents
from botocore.utils import parse_key_val_file
from botocore.utils import parse_timestamp
from botocore.utils import parse_to_aware_datetime
from botocore.utils import CachedProperty
from botocore.utils import ArgumentGenerator
from botocore.model import DenormalizedStructureBuilder
from botocore.model import ShapeResolver


class TestURINormalization(unittest.TestCase):
    def test_remove_dot_segments(self):
        self.assertEqual(remove_dot_segments('../foo'), 'foo')
        self.assertEqual(remove_dot_segments('../../foo'), 'foo')
        self.assertEqual(remove_dot_segments('./foo'), 'foo')
        self.assertEqual(remove_dot_segments('/./'), '/')
        self.assertEqual(remove_dot_segments('/../'), '/')
        self.assertEqual(remove_dot_segments('/foo/bar/baz/../qux'),
                         '/foo/bar/qux')
        self.assertEqual(remove_dot_segments('/foo/..'), '/')
        self.assertEqual(remove_dot_segments('foo/bar/baz'), 'foo/bar/baz')
        self.assertEqual(remove_dot_segments('..'), '')
        self.assertEqual(remove_dot_segments('.'), '')
        self.assertEqual(remove_dot_segments('/.'), '/')
        # I don't think this is RFC compliant...
        self.assertEqual(remove_dot_segments('//foo//'), '/foo/')

    def test_empty_url_normalization(self):
        self.assertEqual(normalize_url_path(''), '/')


class TestTransformName(unittest.TestCase):
    def test_upper_camel_case(self):
        self.assertEqual(xform_name('UpperCamelCase'), 'upper_camel_case')
        self.assertEqual(xform_name('UpperCamelCase', '-'), 'upper-camel-case')

    def test_lower_camel_case(self):
        self.assertEqual(xform_name('lowerCamelCase'), 'lower_camel_case')
        self.assertEqual(xform_name('lowerCamelCase', '-'), 'lower-camel-case')

    def test_consecutive_upper_case(self):
        self.assertEqual(xform_name('HTTPHeaders'), 'http_headers')
        self.assertEqual(xform_name('HTTPHeaders', '-'), 'http-headers')

    def test_consecutive_upper_case_middle_string(self):
        self.assertEqual(xform_name('MainHTTPHeaders'), 'main_http_headers')
        self.assertEqual(xform_name('MainHTTPHeaders', '-'), 'main-http-headers')

    def test_s3_prefix(self):
        self.assertEqual(xform_name('S3BucketName'), 's3_bucket_name')

    def test_already_snake_cased(self):
        self.assertEqual(xform_name('leave_alone'), 'leave_alone')
        self.assertEqual(xform_name('s3_bucket_name'), 's3_bucket_name')
        self.assertEqual(xform_name('bucket_s3_name'), 'bucket_s3_name')

    def test_special_cases(self):
        # Some patterns don't actually match the rules we expect.
        self.assertEqual(xform_name('SwapEnvironmentCNAMEs'), 'swap_environment_cnames')
        self.assertEqual(xform_name('SwapEnvironmentCNAMEs', '-'), 'swap-environment-cnames')
        self.assertEqual(xform_name('CreateCachediSCSIVolume', '-'), 'create-cached-iscsi-volume')
        self.assertEqual(xform_name('DescribeCachediSCSIVolumes', '-'), 'describe-cached-iscsi-volumes')
        self.assertEqual(xform_name('DescribeStorediSCSIVolumes', '-'), 'describe-stored-iscsi-volumes')
        self.assertEqual(xform_name('CreateStorediSCSIVolume', '-'), 'create-stored-iscsi-volume')


class TestValidateJMESPathForSet(unittest.TestCase):
    def setUp(self):
        super(TestValidateJMESPathForSet, self).setUp()
        self.data = {
            'Response': {
                'Thing': {
                    'Id': 1,
                    'Name': 'Thing #1',
                }
            },
            'Marker': 'some-token'
        }

    def test_invalid_exp(self):
        with self.assertRaises(InvalidExpressionError):
            validate_jmespath_for_set('Response.*.Name')

        with self.assertRaises(InvalidExpressionError):
            validate_jmespath_for_set('Response.Things[0]')

        with self.assertRaises(InvalidExpressionError):
            validate_jmespath_for_set('')

        with self.assertRaises(InvalidExpressionError):
            validate_jmespath_for_set('.')


class TestSetValueFromJMESPath(unittest.TestCase):
    def setUp(self):
        super(TestSetValueFromJMESPath, self).setUp()
        self.data = {
            'Response': {
                'Thing': {
                    'Id': 1,
                    'Name': 'Thing #1',
                }
            },
            'Marker': 'some-token'
        }

    def test_single_depth_existing(self):
        set_value_from_jmespath(self.data, 'Marker', 'new-token')
        self.assertEqual(self.data['Marker'], 'new-token')

    def test_single_depth_new(self):
        self.assertFalse('Limit' in self.data)
        set_value_from_jmespath(self.data, 'Limit', 100)
        self.assertEqual(self.data['Limit'], 100)

    def test_multiple_depth_existing(self):
        set_value_from_jmespath(self.data, 'Response.Thing.Name', 'New Name')
        self.assertEqual(self.data['Response']['Thing']['Name'], 'New Name')

    def test_multiple_depth_new(self):
        self.assertFalse('Brand' in self.data)
        set_value_from_jmespath(self.data, 'Brand.New', {'abc': 123})
        self.assertEqual(self.data['Brand']['New']['abc'], 123)


class TestParseEC2CredentialsFile(unittest.TestCase):
    def test_parse_ec2_content(self):
        contents = "AWSAccessKeyId=a\nAWSSecretKey=b\n"
        self.assertEqual(parse_key_val_file_contents(contents),
                         {'AWSAccessKeyId': 'a',
                          'AWSSecretKey': 'b'})

    def test_parse_ec2_content_empty(self):
        contents = ""
        self.assertEqual(parse_key_val_file_contents(contents), {})

    def test_key_val_pair_with_blank_lines(self):
        # The \n\n has an extra blank between the access/secret keys.
        contents = "AWSAccessKeyId=a\n\nAWSSecretKey=b\n"
        self.assertEqual(parse_key_val_file_contents(contents),
                         {'AWSAccessKeyId': 'a',
                          'AWSSecretKey': 'b'})

    def test_key_val_parser_lenient(self):
        # Ignore any line that does not have a '=' char in it.
        contents = "AWSAccessKeyId=a\nNOTKEYVALLINE\nAWSSecretKey=b\n"
        self.assertEqual(parse_key_val_file_contents(contents),
                         {'AWSAccessKeyId': 'a',
                          'AWSSecretKey': 'b'})

    def test_multiple_equals_on_line(self):
        contents = "AWSAccessKeyId=a\nAWSSecretKey=secret_key_with_equals=b\n"
        self.assertEqual(parse_key_val_file_contents(contents),
                         {'AWSAccessKeyId': 'a',
                          'AWSSecretKey': 'secret_key_with_equals=b'})

    def test_os_error_raises_config_not_found(self):
        mock_open = mock.Mock()
        mock_open.side_effect = OSError()
        with self.assertRaises(ConfigNotFound):
            parse_key_val_file('badfile', _open=mock_open)


class TestParseTimestamps(unittest.TestCase):
    def test_parse_iso8601(self):
        self.assertEqual(
            parse_timestamp('1970-01-01T00:10:00.000Z'),
            datetime.datetime(1970, 1, 1, 0, 10, tzinfo=tzutc()))

    def test_parse_epoch(self):
        self.assertEqual(
            parse_timestamp(1222172800),
            datetime.datetime(2008, 9, 23, 12, 26, 40, tzinfo=tzutc()))

    def test_parse_epoch_zero_time(self):
        self.assertEqual(
            parse_timestamp(0),
            datetime.datetime(1970, 1, 1, 0, 0, 0, tzinfo=tzutc()))

    def test_parse_epoch_as_string(self):
        self.assertEqual(
            parse_timestamp('1222172800'),
            datetime.datetime(2008, 9, 23, 12, 26, 40, tzinfo=tzutc()))

    def test_parse_rfc822(self):
        self.assertEqual(
            parse_timestamp('Wed, 02 Oct 2002 13:00:00 GMT'),
            datetime.datetime(2002, 10, 2, 13, 0, tzinfo=tzutc()))

    def test_parse_invalid_timestamp(self):
        with self.assertRaises(ValueError):
            parse_timestamp('invalid date')


class TestParseToUTCDatetime(unittest.TestCase):
    def test_handles_utc_time(self):
        original = datetime.datetime(1970, 1, 1, 0, 0, 0, tzinfo=tzutc())
        self.assertEqual(parse_to_aware_datetime(original), original)

    def test_handles_other_timezone(self):
        tzinfo = tzoffset("BRST", -10800)
        original = datetime.datetime(2014, 1, 1, 0, 0, 0, tzinfo=tzinfo)
        self.assertEqual(parse_to_aware_datetime(original), original)

    def test_handles_naive_datetime(self):
        original = datetime.datetime(1970, 1, 1, 0, 0, 0)
        expected = datetime.datetime(1970, 1, 1, 0, 0, 0, tzinfo=tzutc())
        self.assertEqual(parse_to_aware_datetime(original), expected)

    def test_handles_string_epoch(self):
        expected = datetime.datetime(1970, 1, 1, 0, 0, 0, tzinfo=tzutc())
        self.assertEqual(parse_to_aware_datetime('0'), expected)

    def test_handles_int_epoch(self):
        expected = datetime.datetime(1970, 1, 1, 0, 0, 0, tzinfo=tzutc())
        self.assertEqual(parse_to_aware_datetime(0), expected)

    def test_handles_full_iso_8601(self):
        expected = datetime.datetime(1970, 1, 1, 0, 0, 0, tzinfo=tzutc())
        self.assertEqual(
            parse_to_aware_datetime('1970-01-01T00:00:00Z'),
            expected)

    def test_year_only_iso_8601(self):
        expected = datetime.datetime(1970, 1, 1, 0, 0, 0, tzinfo=tzutc())
        self.assertEqual(parse_to_aware_datetime('1970-01-01'), expected)


class TestCachedProperty(unittest.TestCase):
    def test_cached_property_same_value(self):
        class CacheMe(object):
            @CachedProperty
            def foo(self):
                return 'foo'

        c = CacheMe()
        self.assertEqual(c.foo, 'foo')
        self.assertEqual(c.foo, 'foo')

    def test_cached_property_only_called_once(self):
        # Note: you would normally never want to cache
        # a property that returns a new value each time,
        # but this is done to demonstrate the caching behavior.

        class NoIncrement(object):
            def __init__(self):
                self.counter = 0

            @CachedProperty
            def current_value(self):
                self.counter += 1
                return self.counter

        c = NoIncrement()
        self.assertEqual(c.current_value, 1)
        # If the property wasn't cached, the next value should be
        # be 2, but because it's cached, we know the value will be 1.
        self.assertEqual(c.current_value, 1)


class TestArgumentGenerator(unittest.TestCase):
    def setUp(self):
        self.arg_generator = ArgumentGenerator()

    def assert_skeleton_from_model_is(self, model, generated_skeleton):
        shape = DenormalizedStructureBuilder().with_members(
            model).build_model()
        actual = self.arg_generator.generate_skeleton(shape)
        self.assertEqual(actual, generated_skeleton)

    def test_generate_string(self):
        self.assert_skeleton_from_model_is(
            model={
                'A': {'type': 'string'}
            },
            generated_skeleton={
                'A': ''
            }
        )

    def test_generate_scalars(self):
        self.assert_skeleton_from_model_is(
            model={
                'A': {'type': 'string'},
                'B': {'type': 'integer'},
                'C': {'type': 'float'},
                'D': {'type': 'boolean'},
            },
            generated_skeleton={
                'A': '',
                'B': 0,
                'C': 0.0,
                'D': True,
            }
        )

    def test_generate_nested_structure(self):
        self.assert_skeleton_from_model_is(
            model={
                'A': {
                    'type': 'structure',
                    'members': {
                        'B': {'type': 'string'},
                    }
                }
            },
            generated_skeleton={
                'A': {'B': ''}
            }
        )

    def test_generate_scalar_list(self):
        self.assert_skeleton_from_model_is(
            model={
                'A': {
                    'type': 'list',
                    'member': {
                        'type': 'string'
                    }
                },
            },
            generated_skeleton={
                'A': [''],
            }
        )

    def test_generate_scalar_map(self):
        self.assert_skeleton_from_model_is(
            model={
                'A': {
                    'type': 'map',
                    'key': {'type': 'string'},
                    'value':  {'type': 'string'},
                }
            },
            generated_skeleton={
                'A': {
                    'KeyName': '',
                }
            }
        )

    def test_handles_recursive_shapes(self):
        # We're not using assert_skeleton_from_model_is
        # because we can't use a DenormalizedStructureBuilder,
        # we need a normalized model to represent recursive
        # shapes.
        shape_map = ShapeResolver({
            'InputShape': {
                'type': 'structure',
                'members': {
                    'A': {'shape': 'RecursiveStruct'},
                    'B': {'shape': 'StringType'},
                }
            },
            'RecursiveStruct': {
                'type': 'structure',
                'members': {
                    'C': {'shape': 'RecursiveStruct'},
                    'D': {'shape': 'StringType'},
                }
            },
            'StringType': {
                'type': 'string',
            }
        })
        shape = shape_map.get_shape_by_name('InputShape')
        actual = self.arg_generator.generate_skeleton(shape)
        expected = {
            'A': {
                'C': {
                    # For recurisve shapes, we'll just show
                    # an empty dict.
                },
                'D': ''
            },
            'B': ''
        }
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
