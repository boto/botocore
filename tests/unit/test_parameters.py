#!/usr/bin/env
# Copyright (c) 2012-2013 Mitch Garnaat http://garnaat.org/
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
import time

import mock
import dateutil.parser

import botocore.parameters
import botocore.exceptions



class FakeService(object):

    def __init__(self, timestamp_format):
        self.timestamp_format = timestamp_format


class FakeOperation(object):

    def __init__(self, timestamp_format):
        self.service = FakeService(timestamp_format)


class TestParameters(unittest.TestCase):

    def test_iso_timestamp_from_iso(self):
        op = FakeOperation('iso8601')
        p = botocore.parameters.TimestampParameter(op, name='paramname',
                                                   type='timestamp')
        d = {}
        ts = '2012-10-12T00:00'
        dt = dateutil.parser.parse(ts)
        p.build_parameter_query(ts, d)
        self.assertEqual(d['paramname'], dt.isoformat())
        with self.assertRaisesRegexp(botocore.exceptions.ValidationError,
                                     'timestamp:paramname'):
            p.build_parameter_query(value='not a date string',
                                    built_params=d)

    def test_iso_timestamp_from_epoch(self):
        op = FakeOperation('iso8601')
        p = botocore.parameters.TimestampParameter(op, name='foo')
        d = {}
        iso = '2013-04-11T23:23:15'
        epoch = 1365722595
        p.build_parameter_query(epoch, d)
        self.assertEqual(d['foo'], iso)
        with self.assertRaises(botocore.exceptions.ValidationError):
            p.build_parameter_query(value='not a date string',
                                    built_params=d)

    def test_epoch_timestamp_from_iso(self):
        op = FakeOperation('unixTimestamp')
        p = botocore.parameters.TimestampParameter(op, name='foo')
        d = {}
        iso = '2013-04-11T23:23:15'
        epoch = 1365722595
        p.build_parameter_query(iso, d)
        self.assertEqual(d['foo'], str(epoch))
        with self.assertRaises(botocore.exceptions.ValidationError):
            p.build_parameter_query(value='not a date string',
                                    built_params=d)

    def test_epoch_timestamp_from_epoch(self):
        op = FakeOperation('unixTimestamp')
        p = botocore.parameters.TimestampParameter(op, name='foo')
        d = {}
        epoch = 1365722595
        p.build_parameter_query(epoch, d)
        self.assertEqual(d['foo'], str(epoch))
        with self.assertRaises(botocore.exceptions.ValidationError):
            p.build_parameter_query(value='not a date string',
                                    built_params=d)

    def test_string(self):
        p = botocore.parameters.StringParameter(None, name='foo')
        d = {}
        value = 'This is a test'
        p.build_parameter_query(value, d)
        self.assertEqual(d['foo'], value)
        with self.assertRaises(botocore.exceptions.ValidationError):
            p.build_parameter_query(value=1,
                                    built_params=d)

    def test_utf8_string(self):
        p = botocore.parameters.StringParameter(None, name='foo')
        d = {}
        value = u'\u65e5\u672c\u8a9e'
        p.build_parameter_query(value, d)
        self.assertEqual(d['foo'], value)
        with self.assertRaises(botocore.exceptions.ValidationError):
            p.build_parameter_query(value=1,
                                    built_params=d)

    def test_integer(self):
        p = botocore.parameters.IntegerParameter(None, name='foo')
        d = {}
        p.build_parameter_query(123, d)
        self.assertEqual(d['foo'], '123')
        p.build_parameter_json(123, d)
        self.assertEqual(d['foo'], 123)
        with self.assertRaises(botocore.exceptions.ValidationError):
            p.build_parameter_query(value=123.4,
                                    built_params=d)

    def test_integer_range(self):
        p = botocore.parameters.IntegerParameter(None, name='foo',
                                                 min=0, max=10)
        d = {}
        p.build_parameter_query(9, d)
        self.assertEqual(d['foo'], '9')
        with self.assertRaises(botocore.exceptions.ValidationError):
            p.build_parameter_query(value=8.4,
                                    built_params=d)
        with self.assertRaisesRegexp(botocore.exceptions.RangeError,
                                     'foo'):
            p.build_parameter_query(value=100,
                                    built_params=d)

    def test_float(self):
        p = botocore.parameters.FloatParameter(None, name='foo')
        d = {}
        p.build_parameter_query(123.4, d)
        self.assertEqual(d['foo'], '123.4')
        p.build_parameter_json(123.4, d)
        self.assertEqual(d['foo'], 123.4)
        with self.assertRaises(botocore.exceptions.ValidationError):
            p.build_parameter_query(value=True,
                                    built_params=d)

    def test_float_range(self):
        p = botocore.parameters.FloatParameter(None, name='foo',
                                               min=0, max=10)
        d = {}
        p.build_parameter_query(9.0, d)
        self.assertEqual(d['foo'], '9.0')
        p.build_parameter_json(9.0, d)
        self.assertEqual(d['foo'], 9.0)
        with self.assertRaises(botocore.exceptions.RangeError):
            p.build_parameter_query(value=100.0,
                                    built_params=d)


    def test_boolean(self):
        p = botocore.parameters.BooleanParameter(None, name='foo')
        d = {}
        p.build_parameter_query('true', d)
        self.assertEqual(d['foo'], 'true')
        p.build_parameter_query('True', d)
        self.assertEqual(d['foo'], 'true')
        p.build_parameter_query('TRUE', d)
        self.assertEqual(d['foo'], 'true')
        p.build_parameter_query('false', d)
        self.assertEqual(d['foo'], 'false')
        p.build_parameter_query('False', d)
        self.assertEqual(d['foo'], 'false')
        p.build_parameter_query('FALSE', d)
        self.assertEqual(d['foo'], 'false')
        p.build_parameter_query(True, d)
        self.assertEqual(d['foo'], 'true')
        p.build_parameter_json(True, d)
        self.assertEqual(d['foo'], True)
        with self.assertRaises(botocore.exceptions.ValidationError):
            p.build_parameter_query(value='100',
                                    built_params=d)

    def test_list_fails_member_validation(self):
        p = botocore.parameters.ListParameter(operation=None, name='foo',
                                              members={'type': 'string'})
        d = {}
        # None is not of type string.
        value = ['This', 'is', None, 'test']
        with self.assertRaises(botocore.exceptions.ValidationError):
            p.build_parameter('query', value, d)

    def test_list_type_validation(self):
        p = botocore.parameters.ListParameter(operation=None, name='foo',
                                              members={'type': 'string'})
        d = {}
        # None is not of type string.
        value = 'not a list'
        with self.assertRaises(botocore.exceptions.ValidationError):
            p.build_parameter('query', value, d)

    def test_list_struct_fails_validation(self):
        members = {
            "shape_name": "Foo",
            "type": "structure",
            "members": {
                "foo": {
                    "shape_name": "String",
                    "type": "string",
                    "required": True,
                },
            },
        }
        p = botocore.parameters.ListParameter(operation=None, name='foo',
                                              members=members)
        d = {}
        # 'notfoo' is an unknown key so this will raise an exception
        # when we try to validate this value.
        value = [{'foo': 'bar'}, {'foo': 'baz'}, {'notfoo': 'bad'}]
        with self.assertRaisesRegexp(botocore.exceptions.ValidationError,
                                     'element of None:foo'):
            p.build_parameter('query', value, d)

    def test_plain_list(self):
        # Test a plain vanilla list.
        p = botocore.parameters.ListParameter(operation=None, name='foo',
                                              members={'type': 'string'})
        d = {}
        value = ['This', 'is', 'a', 'test']
        p.build_parameter_query(value, d)
        self.assertEquals(d, {'foo.member.4': 'test',
                              'foo.member.2': 'is',
                              'foo.member.3': 'a',
                              'foo.member.1': 'This'})

    def test_list_with_xmlname(self):
        # Test a list where the member specifies an xmlname.
        # This should be ignored.
        p = botocore.parameters.ListParameter(
            operation=None, name='foo',
            members={'type': 'string', 'xmlname': 'bar'})
        d = {}
        value = ['This', 'is', 'a', 'test']
        p.build_parameter_query(value, d)
        self.assertEquals(d, {'foo.member.4': 'test',
                              'foo.member.2': 'is',
                              'foo.member.3': 'a',
                              'foo.member.1': 'This'})
        d = {}
        p.build_parameter_json(value, d)
        self.assertEquals(d, {'foo': ['This', 'is', 'a', 'test']})

    def test_flattened_list(self):
        # Test a flattened list.  Member should always define
        # and xmlname attribute.
        p = botocore.parameters.ListParameter(
            operation=None, name='foo', flattened=True,
            members={'type': 'string', 'xmlname': 'bar'})
        d = {}
        value = ['This', 'is', 'a', 'test']
        p.build_parameter_query(value, d)
        self.assertEquals(d, {'bar.4': 'test',
                              'bar.1': 'This',
                              'bar.2': 'is',
                              'bar.3': 'a'})

    def test_type_blob_validation(self):
        p = botocore.parameters.BlobParameter(
            operation=None, name='Foo', payload=True)
        bytearray_type = bytearray(b'foo')
        byte_type = bytes(b'foo')
        str_type = str('foo')
        self.assertEqual(p.validate(str_type), str_type)
        self.assertEqual(p.validate(byte_type), byte_type)
        self.assertEqual(p.validate(bytearray_type), bytearray_type)

    def test_blob_conversion_to_base64(self):
        # Blobs that are not in the payload should be base64-encoded
        p = botocore.parameters.BlobParameter(
            operation=None, name='Foo', payload=False)
        self.assertEqual(p.validate('foo'), 'Zm9v')


class TestStructureParamaters(unittest.TestCase):

    def setUp(self):
        self.members = {
            "AvailabilityZone": {
              "shape_name": "String",
              "type": "string",
              "documentation": "",
            },
            "GroupName": {
              "shape_name": "String",
              "type": "string",
              "documentation": "",
            },
            "Tenancy": {
              "shape_name": "String",
              "type": "string",
              "documentation": "",
            }
        }
        self.p = botocore.parameters.StructParameter(
            operation=None, name='Foo',
            members=self.members)

    def test_struct_parameter_query_build(self):
        d = {}
        self.p.build_parameter_query({'AvailabilityZone': 'foo',
                                      'GroupName': 'bar',
                                      'Tenancy': 'baz'}, d)
        self.assertEqual(d, {
            'Foo.AvailabilityZone': 'foo',
            'Foo.GroupName': 'bar',
            'Foo.Tenancy': 'baz',
        })

    def test_struct_type_validation(self):
        self.p.validate({'AvailabilityZone': 'foo',
                         'GroupName': 'bar',
                         'Tenancy': 'baz'})
        with self.assertRaisesRegexp(
                botocore.exceptions.ValidationError,
                ("Invalid value \('not a dict'\) for param "
                 "None:Foo of type structure")):
            self.p.validate('not a dict')

    def test_struct_unknown_keys_validation(self):
        # Unknown key 'group_name' key
        with self.assertRaises(botocore.exceptions.UnknownKeyError):
            # Missing the 'GroupName' key
            self.p.validate({'AvailabilityZone': 'foo',
                             'group_name': 'unknown',
                             'Tenancy': 'baz'})

    def test_snake_case_parameters(self):
        """
        Test support for snake case parameters
        """
        session = botocore.session.get_session()
        service = session.get_service('dynamodb')
        op = service.get_operation('UpdateTable')

        # All CamelCase
        params = {
            'ProvisionedThroughput': {
                'WriteCapacityUnits': 2,
                'ReadCapacityUnits': 2
            },
            'TableName': 'test-table'
        }
        built_params = op.build_parameters(**params)
        self.assertEqual(
            built_params,
            {
                'ProvisionedThroughput': {
                    'WriteCapacityUnits': 2,
                    'ReadCapacityUnits': 2
                },
                'TableName': 'test-table'
            }
        )

        # Mixed case
        params = {
            'provisioned_throughput': {
                'WriteCapacityUnits': 2,
                'ReadCapacityUnits': 2
            },
            'table_name': 'test-table'
        }
        built_params = op.build_parameters(**params)
        self.assertEqual(
            built_params,
            {
                'ProvisionedThroughput': {
                    'WriteCapacityUnits': 2,
                    'ReadCapacityUnits': 2
                },
                'TableName': 'test-table'
            }
        )


if __name__ == "__main__":
    unittest.main()
