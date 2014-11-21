# Copyright 2014 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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
import datetime

import mock
from dateutil.tz import tzutc

from botocore import parsers
from botocore import model


# These tests contain botocore specific tests that either
# don't make sense in the protocol tests or haven't been added
# yet.

class TestResponseMetadataParsed(unittest.TestCase):
    def test_response_metadata_parsed_for_query_service(self):
        parser = parsers.QueryParser()
        response = (
            '<OperationNameResponse>'
              '<OperationNameResult><Str>myname</Str></OperationNameResult>'
              '<ResponseMetadata>'
                '<RequestId>request-id</RequestId>'
              '</ResponseMetadata>'
            '</OperationNameResponse>').encode('utf-8')
        output_shape = model.StructureShape(
            'OutputShape',
            {
                'type': 'structure',
                'resultWrapper': 'OperationNameResult',
                'members': {
                    'Str': {
                        'shape': 'StringType',
                    },
                    'Num': {
                        'shape': 'IntegerType',
                    }
                }
            },
            model.ShapeResolver({
                'StringType': {
                    'type': 'string',
                },
                'IntegerType': {
                    'type': 'integer',
                }
            })
        )
        parsed = parser.parse({'body': response, 'status_code': 200}, output_shape)
        self.assertEqual(
            parsed, {'Str': 'myname',
                     'ResponseMetadata': {'RequestId': 'request-id'}})


    def test_response_metadata_parsed_for_ec2(self):
        parser = parsers.EC2QueryParser()
        response = (
            '<OperationNameResponse>'
              '<Str>myname</Str>'
              '<requestId>request-id</requestId>'
            '</OperationNameResponse>').encode('utf-8')
        output_shape = model.StructureShape(
            'OutputShape',
            {
                'type': 'structure',
                'members': {
                    'Str': {
                        'shape': 'StringType',
                    }
                }
            },
            model.ShapeResolver({'StringType': {'type': 'string'}})
        )
        parsed = parser.parse({'body': response, 'status_code': 200}, output_shape)
        # Note that the response metadata is normalized to match the query
        # protocol, even though this is not how it appears in the output.
        self.assertEqual(
            parsed, {'Str': 'myname',
                     'ResponseMetadata': {'RequestId': 'request-id'}})

    def test_response_metadata_errors_for_json(self):
        parser = parsers.JSONParser()
        response = {
            "body": b"""
                {"__type":"amazon.foo.validate#ValidationException",
                 "message":"this is a message"}
                """,
            "status_code": 400,
            "headers": {
                "x-amzn-requestid": "request-id"
            }
        }
        parsed = parser.parse(response, None)
        # Even (especially) on an error condition, the
        # ResponseMetadata should be populated.
        self.assertIn('ResponseMetadata', parsed)
        self.assertEqual(parsed['ResponseMetadata']['RequestId'], 'request-id')

        self.assertIn('Error', parsed)
        self.assertEqual(parsed['Error']['Message'], 'this is a message')
        self.assertEqual(parsed['Error']['Code'], 'ValidationException')

    def test_response_metadata_errors_alternate_form(self):
        # Sometimes there is no '#' in the __type.  We need to be
        # able to parse this error message as well.
        parser = parsers.JSONParser()
        response = {
            "body": b"""
                {"__type":"ValidationException",
                 "message":"this is a message"}
                """,
            "status_code": 400,
            "headers": {
                "x-amzn-requestid": "request-id"
            }
        }
        parsed = parser.parse(response, None)
        self.assertIn('Error', parsed)
        self.assertEqual(parsed['Error']['Message'], 'this is a message')
        self.assertEqual(parsed['Error']['Code'], 'ValidationException')

    def test_response_metadata_on_normal_request(self):
        parser = parsers.JSONParser()
        response = b'{"Str": "mystring"}'
        headers = {'x-amzn-requestid': 'request-id'}
        output_shape = model.StructureShape(
            'OutputShape',
            {
                'type': 'structure',
                'members': {
                    'Str': {
                        'shape': 'StringType',
                    }
                }
            },
            model.ShapeResolver({'StringType': {'type': 'string'}})
        )
        parsed = parser.parse({'body': response, 'headers': headers,
                               'status_code': 200}, output_shape)
        # Note that the response metadata is normalized to match the query
        # protocol, even though this is not how it appears in the output.
        self.assertEqual(
            parsed, {'Str': 'mystring',
                     'ResponseMetadata': {'RequestId': 'request-id'}})

    def test_response_metadata_on_empty_rest_response(self):
        headers = {'x-amzn-requestid': 'request-id'}
        parser = parsers.RestJSONParser()
        parsed = parser.parse(
            {'body': b'', 'headers': headers, 'status_code': 200}, None)
        self.assertEqual(
            parsed,
            {'ResponseMetadata': {'RequestId': 'request-id'}})

    def test_response_metadata_on_rest_response(self):
        parser = parsers.RestJSONParser()
        response = b'{"Str": "mystring"}'
        headers = {'x-amzn-requestid': 'request-id'}
        output_shape = model.StructureShape(
            'OutputShape',
            {
                'type': 'structure',
                'members': {
                    'Str': {
                        'shape': 'StringType',
                    }
                }
            },
            model.ShapeResolver({'StringType': {'type': 'string'}})
        )
        parsed = parser.parse({'body': response, 'headers': headers,
                               'status_code': 200}, output_shape)
        # Note that the response metadata is normalized to match the query
        # protocol, even though this is not how it appears in the output.
        self.assertEqual(
            parsed, {'Str': 'mystring',
                     'ResponseMetadata': {'RequestId': 'request-id'}})

    def test_response_metadata_on_empty_rest_xml_response(self):
        # This is the format used by cloudfront, route53.
        headers = {'x-amzn-requestid': 'request-id'}
        parser = parsers.RestXMLParser()
        parsed = parser.parse(
            {'body': b'', 'headers': headers, 'status_code': 200}, None)
        self.assertEqual(
            parsed,
            {'ResponseMetadata': {'RequestId': 'request-id'}})

    def test_response_metadata_from_s3_response(self):
        # Even though s3 is a rest-xml service, it's response metadata
        # is slightly different.  It has two request ids, both come from
        # the response headers, are both are named differently from other
        # rest-xml responses.
        headers = {
            'x-amz-id-2': 'second-id',
            'x-amz-request-id': 'request-id'
        }
        parser = parsers.RestXMLParser()
        parsed = parser.parse(
            {'body': '', 'headers': headers, 'status_code': 200}, None)
        self.assertEqual(
            parsed,
            {'ResponseMetadata': {'RequestId': 'request-id',
                                  'HostId': 'second-id'}})

    def test_s3_error_response(self):
        body = (
            '<Error>'
              '<Code>NoSuchBucket</Code>'
              '<Message>error message</Message>'
              '<BucketName>asdf</BucketName>'
              '<RequestId>EF1EF43A74415102</RequestId>'
              '<HostId>hostid</HostId>'
            '</Error>'
        ).encode('utf-8')
        headers = {
            'x-amz-id-2': 'second-id',
            'x-amz-request-id': 'request-id'
        }
        parser = parsers.RestXMLParser()
        parsed = parser.parse(
            {'body': body, 'headers': headers, 'status_code': 400}, None)
        self.assertIn('Error', parsed)
        self.assertEqual(parsed['Error'], {
            'Code': 'NoSuchBucket',
            'Message': 'error message',
            'BucketName': 'asdf',
            # We don't want the RequestId/HostId because they're already
            # present in the ResponseMetadata key.
        })
        self.assertEqual(parsed['ResponseMetadata'], {
            'RequestId': 'request-id',
            'HostId': 'second-id',
        })

    def test_s3_error_response_with_no_body(self):
        # If you try to HeadObject a key that does not exist,
        # you will get an empty body.  When this happens
        # we expect that we will use Code/Message from the
        # HTTP status code.
        body = ''
        headers = {
            'x-amz-id-2': 'second-id',
            'x-amz-request-id': 'request-id'
        }
        parser = parsers.RestXMLParser()
        parsed = parser.parse(
            {'body': body, 'headers': headers, 'status_code': 404}, None)
        self.assertIn('Error', parsed)
        self.assertEqual(parsed['Error'], {
            'Code': '404',
            'Message': 'Not Found',
        })
        self.assertEqual(parsed['ResponseMetadata'], {
            'RequestId': 'request-id',
            'HostId': 'second-id',
        })


class TestResponseParsingDatetimes(unittest.TestCase):
    def test_can_parse_float_timestamps(self):
        # The type "timestamp" can come back as both an integer or as a float.
        # We need to make sure we handle the case where the timestamp comes
        # back as a float.  It might make sense to move this to protocol tests.
        output_shape = model.Shape(shape_name='datetime',
                                   shape_model={'type': 'timestamp'})
        parser = parsers.JSONParser()
        timestamp_as_float = b'1407538750.49'
        expected_parsed = datetime.datetime(
            2014, 8, 8, 22, 59, 10, 490000, tzinfo=tzutc())
        parsed = parser.parse(
            {'body': timestamp_as_float,
             'headers': [],
             'status_code': 200}, output_shape)
        self.assertEqual(parsed, expected_parsed)
