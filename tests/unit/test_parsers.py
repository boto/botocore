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
            '  <OperationNameResult><Str>myname</Str></OperationNameResult>'
            '  <ResponseMetadata>'
            '    <RequestId>request-id</RequestId>'
            '  </ResponseMetadata>'
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
        parsed = parser.parse(
            {'body': response,
             'headers': {},
             'status_code': 200}, output_shape)
        self.assertEqual(
            parsed, {'Str': 'myname',
                     'ResponseMetadata': {'RequestId': 'request-id',
                                          'HTTPStatusCode': 200}})

    def test_response_metadata_parsed_for_ec2(self):
        parser = parsers.EC2QueryParser()
        response = (
            '<OperationNameResponse>'
            '  <Str>myname</Str>'
            '  <requestId>request-id</requestId>'
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
        parsed = parser.parse({'headers': {},
                               'body': response,
                               'status_code': 200}, output_shape)
        # Note that the response metadata is normalized to match the query
        # protocol, even though this is not how it appears in the output.
        self.assertEqual(
            parsed, {'Str': 'myname',
                     'ResponseMetadata': {'RequestId': 'request-id',
                                          'HTTPStatusCode': 200}})

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
                     'ResponseMetadata': {'RequestId': 'request-id',
                                          'HTTPStatusCode': 200}})

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
                     'ResponseMetadata': {'RequestId': 'request-id',
                                          'HTTPStatusCode': 200}})

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
                                  'HostId': 'second-id',
                                  'HTTPStatusCode': 200}})

    def test_s3_error_response(self):
        body = (
            '<Error>'
            '  <Code>NoSuchBucket</Code>'
            '  <Message>error message</Message>'
            '  <BucketName>asdf</BucketName>'
            '  <RequestId>EF1EF43A74415102</RequestId>'
            '  <HostId>hostid</HostId>'
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
            'HTTPStatusCode': 400,
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
            'HTTPStatusCode': 404,
        })

    def test_can_parse_sdb_error_response(self):
        body = (
            '<OperationNameResponse>'
            '    <Errors>'
            '        <Error>'
            '            <Code>1</Code>'
            '            <Message>msg</Message>'
            '        </Error>'
            '    </Errors>'
            '    <RequestId>abc-123</RequestId>'
            '</OperationNameResponse>'
        ).encode('utf-8')
        parser = parsers.QueryParser()
        parsed = parser.parse({
            'body': body, 'headers': {}, 'status_code': 500}, None)
        self.assertIn('Error', parsed)
        self.assertEqual(parsed['Error'], {
            'Code': '1',
            'Message': 'msg'
        })
        self.assertEqual(parsed['ResponseMetadata'], {
            'RequestId': 'abc-123',
            'HTTPStatusCode': 500
        })

    def test_can_parse_glacier_error_response(self):
        body = (b'{"code":"AccessDeniedException","type":"Client","message":'
                b'"Access denied"}')
        headers = {
             'x-amzn-requestid': 'request-id'
        }
        parser = parsers.RestJSONParser()
        parsed = parser.parse(
            {'body': body, 'headers': headers, 'status_code': 400}, None)
        self.assertEqual(parsed['Error'], {'Message': 'Access denied',
                                           'Code': 'AccessDeniedException'})

    def test_can_parse_restjson_error_code(self):
        body = b'''{
            "status": "error",
            "errors": [{"message": "[*Deprecated*: blah"}],
            "adds": 0,
            "__type": "#WasUnableToParseThis",
            "message": "blah",
            "deletes": 0}'''
        headers = {
             'x-amzn-requestid': 'request-id'
        }
        parser = parsers.RestJSONParser()
        parsed = parser.parse(
            {'body': body, 'headers': headers, 'status_code': 400}, None)
        self.assertEqual(parsed['Error'], {'Message': 'blah',
                                           'Code': 'WasUnableToParseThis'})

    def test_can_parse_with_case_insensitive_keys(self):
        body = (b'{"Code":"AccessDeniedException","type":"Client","Message":'
                b'"Access denied"}')
        headers = {
             'x-amzn-requestid': 'request-id'
        }
        parser = parsers.RestJSONParser()
        parsed = parser.parse(
            {'body': body, 'headers': headers, 'status_code': 400}, None)
        self.assertEqual(parsed['Error'], {'Message': 'Access denied',
                                           'Code': 'AccessDeniedException'})

    def test_can_parse_route53_with_missing_message(self):
        # The message isn't always in the XML response (or even the headers).
        # We should be able to handle this gracefully and still at least
        # populate a "Message" key so that consumers don't have to
        # conditionally check for this.
        body =  (
            '<ErrorResponse>'
            '  <Error>'
            '    <Type>Sender</Type>'
            '    <Code>InvalidInput</Code>'
            '  </Error>'
            '  <RequestId>id</RequestId>'
            '</ErrorResponse>'
        ).encode('utf-8')
        parser = parsers.RestXMLParser()
        parsed = parser.parse({
            'body': body, 'headers': {}, 'status_code': 400}, None)
        error = parsed['Error']
        self.assertEqual(error['Code'], 'InvalidInput')
        # Even though there's no <Message /> we should
        # still populate an empty string.
        self.assertEqual(error['Message'], '')


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


class TestCanDecorateResponseParsing(unittest.TestCase):
    def setUp(self):
        self.factory = parsers.ResponseParserFactory()

    def create_request_dict(self, with_body):
        return {
            'body': with_body, 'headers': [], 'status_code': 200
        }

    def test_normal_blob_parsing(self):
        output_shape = model.Shape(shape_name='BlobType',
                                   shape_model={'type': 'blob'})
        parser = self.factory.create_parser('json')

        hello_world_b64 = b'"aGVsbG8gd29ybGQ="'
        expected_parsed = b'hello world'
        parsed = parser.parse(
            self.create_request_dict(with_body=hello_world_b64),
            output_shape)
        self.assertEqual(parsed, expected_parsed)

    def test_can_decorate_scalar_parsing(self):
        output_shape = model.Shape(shape_name='BlobType',
                                   shape_model={'type': 'blob'})
        # Here we're overriding the blob parser so that
        # we can change it to a noop parser.
        self.factory.set_parser_defaults(
            blob_parser=lambda x: x)
        parser = self.factory.create_parser('json')

        hello_world_b64 = b'"aGVsbG8gd29ybGQ="'
        expected_parsed = "aGVsbG8gd29ybGQ="
        parsed = parser.parse(
            self.create_request_dict(with_body=hello_world_b64),
            output_shape)
        self.assertEqual(parsed, expected_parsed)

    def test_can_decorate_timestamp_parser(self):
        output_shape = model.Shape(shape_name='datetime',
                                   shape_model={'type': 'timestamp'})
        # Here we're overriding the timestamp parser so that
        # we can change it to just convert a string to an integer
        # instead of converting to a datetime.
        self.factory.set_parser_defaults(
            timestamp_parser=lambda x: int(x))
        parser = self.factory.create_parser('json')

        timestamp_as_int = b'1407538750'
        expected_parsed = int(timestamp_as_int)
        parsed = parser.parse(
            self.create_request_dict(with_body=timestamp_as_int),
            output_shape)
        self.assertEqual(parsed, expected_parsed)


class TestHandlesNoOutputShape(unittest.TestCase):
    """Verify that each protocol handles no output shape properly."""

    def test_empty_rest_json_response(self):
        headers = {'x-amzn-requestid': 'request-id'}
        parser = parsers.RestJSONParser()
        output_shape = None
        parsed = parser.parse(
            {'body': b'', 'headers': headers, 'status_code': 200},
            output_shape)
        self.assertEqual(
            parsed,
            {'ResponseMetadata': {'RequestId': 'request-id',
                                  'HTTPStatusCode': 200}})

    def test_empty_rest_xml_response(self):
        # This is the format used by cloudfront, route53.
        headers = {'x-amzn-requestid': 'request-id'}
        parser = parsers.RestXMLParser()
        output_shape = None
        parsed = parser.parse(
            {'body': b'', 'headers': headers, 'status_code': 200},
            output_shape)
        self.assertEqual(
            parsed,
            {'ResponseMetadata': {'RequestId': 'request-id',
                                  'HTTPStatusCode': 200}})

    def test_empty_query_response(self):
        body = (
            b'<DeleteTagsResponse xmlns="http://autoscaling.amazonaws.com/">'
            b'  <ResponseMetadata>'
            b'    <RequestId>request-id</RequestId>'
            b'  </ResponseMetadata>'
            b'</DeleteTagsResponse>'
        )
        parser = parsers.QueryParser()
        output_shape = None
        parsed = parser.parse(
            {'body': body, 'headers': {}, 'status_code': 200},
            output_shape)
        self.assertEqual(
            parsed,
            {'ResponseMetadata': {'RequestId': 'request-id',
                                  'HTTPStatusCode': 200}})

    def test_empty_json_response(self):
        headers = {'x-amzn-requestid': 'request-id'}
        # Output shape of None represents no output shape in the model.
        output_shape = None
        parser = parsers.JSONParser()
        parsed = parser.parse(
            {'body': b'', 'headers': headers, 'status_code': 200},
            output_shape)
        self.assertEqual(
            parsed,
            {'ResponseMetadata': {'RequestId': 'request-id',
                                  'HTTPStatusCode': 200}})


class TestHandlesInvalidXMLResponses(unittest.TestCase):
    def test_invalid_xml_shown_in_error_message(self):
        # Missing the closing XML tags.
        invalid_xml = (
            b'<DeleteTagsResponse xmlns="http://autoscaling.amazonaws.com/">'
            b'  <ResponseMetadata>'
        )
        parser = parsers.QueryParser()
        output_shape = None
        # The XML body should be in the error message.
        with self.assertRaisesRegexp(parsers.ResponseParserError,
                                     '<DeleteTagsResponse'):
            parser.parse(
                {'body': invalid_xml, 'headers': {}, 'status_code': 200},
                output_shape)


class TestRESTXMLResponses(unittest.TestCase):
    def test_multiple_structures_list_returns_struture(self):
        # This is to handle the scenario when something is modeled
        # as a structure and instead a list of structures is returned.
        # For this case, a single element from the list should be parsed
        # For botocore, this will be the first element.
        # Currently, this logic may happen in s3's GetBucketLifecycle
        # operation.
        headers = {}
        parser = parsers.RestXMLParser()
        body = (
            '<?xml version="1.0" ?>'
            '<OperationName xmlns="http://s3.amazonaws.com/doc/2006-03-01/">'
            '	<Foo><Bar>first_value</Bar></Foo>'
            '	<Foo><Bar>middle_value</Bar></Foo>'
            '	<Foo><Bar>last_value</Bar></Foo>'
            '</OperationName>'
        )
        builder = model.DenormalizedStructureBuilder()
        output_shape = builder.with_members({
            'Foo': {
                'type': 'structure',
                'members': {
                    'Bar': {
                        'type': 'string',
                    }
                }
            }
        }).build_model()
        parsed = parser.parse(
            {'body': body, 'headers': headers, 'status_code': 200},
            output_shape)
        # Ensure the first element is used out of the list.
        self.assertEqual(parsed['Foo'], {'Bar': 'first_value'})
