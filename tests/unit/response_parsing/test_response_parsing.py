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

import os
import glob
import json
import pprint
import logging
import difflib
from tests import create_session

import botocore.session
from botocore import xform_name
from botocore import parsers

log = logging.getLogger(__name__)


SPECIAL_CASES = [
    'iam-get-user-policy.xml', # Needs the JSON decode from handlers.py
    'iam-list-roles.xml',  # Needs the JSON decode from handlers.py for the policy
    's3-get-bucket-location.xml', # Confirmed, this will need a special handler
    #'s3-list-multipart-uploads.xml',  # Bug in model, missing delimeter
    'cloudformation-get-template.xml', # Need to JSON decode the template body.
]


def _test_parsed_response(xmlfile, response_body, operation_model, expected):
    response = {
        'body': response_body,
        'status_code': 200,
        'headers': {}
    }
    for case in SPECIAL_CASES:
        if case in xmlfile:
            print("SKIP: %s" % xmlfile)
            return
    if 'errors' in xmlfile:
        response['status_code'] = 400
    # Handle the special cased __headers__ key if it exists.
    if b'__headers__' in response_body:
        loaded = json.loads(response_body.decode('utf-8'))
        response['headers'] = loaded.pop('__headers__')
        response['body'] = json.dumps(loaded).encode('utf-8')

    protocol = operation_model.service_model.protocol
    parser_cls = parsers.PROTOCOL_PARSERS[protocol]
    parser = parser_cls(timestamp_parser=lambda x: x)
    parsed = parser.parse(response, operation_model.output_shape)
    parsed = _convert_bytes_to_str(parsed)
    expected['ResponseMetadata']['HTTPStatusCode'] = response['status_code']
    expected['ResponseMetadata']['HTTPHeaders'] = response['headers']

    d2 = parsed
    d1 = expected

    if d1 != d2:
        log.debug('-' * 40)
        log.debug("XML FILE:\n" + xmlfile)
        log.debug('-' * 40)
        log.debug("ACTUAL:\n" + pprint.pformat(parsed))
        log.debug('-' * 40)
        log.debug("EXPECTED:\n" + pprint.pformat(expected))
    if not d1 == d2:
        # Borrowed from assertDictEqual, though this doesn't
        # handle the case when unicode literals are used in one
        # dict but not in the other (and we want to consider them
        # as being equal).
        print(d1)
        print()
        print(d2)
        pretty_d1 = pprint.pformat(d1, width=1).splitlines()
        pretty_d2 = pprint.pformat(d2, width=1).splitlines()
        diff = ('\n' + '\n'.join(difflib.ndiff(pretty_d1, pretty_d2)))
        raise AssertionError("Dicts are not equal:\n%s" % diff)


def _convert_bytes_to_str(parsed):
    if isinstance(parsed, dict):
        new_dict = {}
        for key, value in parsed.items():
            new_dict[key] = _convert_bytes_to_str(value)
        return new_dict
    elif isinstance(parsed, bytes):
        return parsed.decode('utf-8')
    elif isinstance(parsed, list):
        new_list = []
        for item in parsed:
            new_list.append(_convert_bytes_to_str(item))
        return new_list
    else:
        return parsed


def test_xml_parsing():
    for dp in ['responses', 'errors']:
        data_path = os.path.join(os.path.dirname(__file__), 'xml')
        data_path = os.path.join(data_path, dp)
        session = create_session()
        xml_files = glob.glob('%s/*.xml' % data_path)
        service_names = set()
        for fn in xml_files:
            service_names.add(os.path.split(fn)[1].split('-')[0])
        for service_name in service_names:
            service_model = session.get_service_model(service_name)
            service_xml_files = glob.glob('%s/%s-*.xml' % (data_path,
                                                           service_name))
            for xmlfile in service_xml_files:
                expected = _get_expected_parsed_result(xmlfile)
                operation_model = _get_operation_model(service_model, xmlfile)
                raw_response_body = _get_raw_response_body(xmlfile)
                yield _test_parsed_response, xmlfile, raw_response_body, \
                    operation_model, expected


def _get_raw_response_body(xmlfile):
    with open(xmlfile, 'rb') as f:
        return f.read()


def _get_operation_model(service_model, filename):
    dirname, filename = os.path.split(filename)
    basename = os.path.splitext(filename)[0]
    sn, opname = basename.split('-', 1)
    # In order to have multiple tests for the same
    # operation a '#' char is used to separate
    # operation names from some other suffix so that
    # the tests have a different filename, e.g
    # my-operation#1.xml, my-operation#2.xml.
    opname = opname.split('#')[0]
    operation_names = service_model.operation_names
    for operation_name in operation_names:
        if xform_name(operation_name) == opname.replace('-', '_'):
            return service_model.operation_model(operation_name)
    return operation


def _get_expected_parsed_result(filename):
    dirname, filename = os.path.split(filename)
    basename = os.path.splitext(filename)[0]
    jsonfile = os.path.join(dirname, basename + '.json')
    with open(jsonfile) as f:
        return json.load(f)


def test_json_errors_parsing():
    # The outputs/ directory has sample output responses
    # For each file in outputs/ there's a corresponding file
    # in expected/ that has the expected parsed response.
    base_dir = os.path.join(os.path.dirname(__file__), 'json')
    json_responses_dir = os.path.join(base_dir, 'errors')
    expected_parsed_dir = os.path.join(base_dir, 'expected')
    session = botocore.session.get_session()
    for json_response_file in os.listdir(json_responses_dir):
        # Files look like: 'datapipeline-create-pipeline.json'
        service_name, operation_name = os.path.splitext(
            json_response_file)[0].split('-', 1)
        expected_parsed_response = os.path.join(expected_parsed_dir,
                                                json_response_file)
        raw_response_file = os.path.join(json_responses_dir,
                                         json_response_file)
        with open(expected_parsed_response) as f:
            expected = json.load(f)
        service_model = session.get_service_model(service_name)
        operation_names = service_model.operation_names
        operation_model = None
        for op_name in operation_names:
            if xform_name(op_name) == operation_name.replace('-', '_'):
                operation_model = service_model.operation_model(op_name)
        with open(raw_response_file, 'rb') as f:
            raw_response_body = f.read()
        yield _test_parsed_response, raw_response_file, \
            raw_response_body, operation_model, expected


def _uhg_test_json_parsing():
    input_path = os.path.join(os.path.dirname(__file__), 'json')
    input_path = os.path.join(input_path, 'inputs')
    output_path = os.path.join(os.path.dirname(__file__), 'json')
    output_path = os.path.join(output_path, 'outputs')
    session = botocore.session.get_session()
    jsonfiles = glob.glob('%s/*.json' % input_path)
    service_names = set()
    for fn in jsonfiles:
        service_names.add(os.path.split(fn)[1].split('-')[0])
    for service_name in service_names:
        service_model = session.get_service_model(service_name)
        service_json_files = glob.glob('%s/%s-*.json' % (input_path,
                                                         service_name))
        for jsonfile in service_json_files:
            expected = _get_expected_parsed_result(jsonfile)
            operation_model = _get_operation_model(service_model, jsonfile)
            with open(jsonfile, 'rb') as f:
                raw_response_body = f.read()
            yield _test_parsed_response, jsonfile, \
                raw_response_body, operation_model, expected
            # TODO: handle the __headers crap.


#class TestHeaderParsing(unittest.TestCase):
#
#    maxDiff = None
#
#    def setUp(self):
#        self.session = botocore.session.get_session()
#        self.s3 = self.session.get_service('s3')
#
#    def test_put_object(self):
#        http_response = Mock()
#        http_response.encoding = 'utf-8'
#        http_response.headers = CaseInsensitiveDict(
#            {'Date': 'Thu, 22 Aug 2013 02:11:57 GMT',
#             'Content-Length': '0',
#             'x-amz-request-id': '2B74ECB010FF029E',
#             'ETag': '"b081e66e7e0c314285c655cafb4d1e71"',
#             'x-amz-id-2': 'bKECRRBFttBRVbJPIVBLQwwipI0i+s9HMvNFdttR17ouR0pvQSKEJUR+1c6cW1nQ',
#             'Server': 'AmazonS3',
#             'content-type': 'text/xml'})
#        http_response.content = ''
#        put_object = self.s3.get_operation('PutObject')
#        expected = {"ETag": '"b081e66e7e0c314285c655cafb4d1e71"'}
#        response_data = get_response(self.session, put_object, http_response)[1]
#        self.assertEqual(response_data, expected)
#
#    def test_head_object(self):
#        http_response = Mock()
#        http_response.encoding = 'utf-8'
#        http_response.headers = CaseInsensitiveDict(
#            {'Date': 'Thu, 22 Aug 2013 02:11:57 GMT',
#             'Content-Length': '265',
#             'x-amz-request-id': '2B74ECB010FF029E',
#             'ETag': '"40d06eb6194712ac1c915783004ef730"',
#             'Server': 'AmazonS3',
#             'content-type': 'binary/octet-stream',
#             'Content-Type': 'binary/octet-stream',
#             'accept-ranges': 'bytes',
#             'Last-Modified': 'Tue, 20 Aug 2013 18:33:25 GMT',
#             'x-amz-server-side-encryption': 'AES256',
#             'x-amz-meta-mykey1': 'value1',
#             'x-amz-meta-mykey2': 'value2',
#             })
#        http_response.content = ''
#        http_response.request.method = 'HEAD'
#        put_object = self.s3.get_operation('HeadObject')
#        expected = {"AcceptRanges": "bytes",
#                    "ContentType": "binary/octet-stream",
#                    "LastModified": "Tue, 20 Aug 2013 18:33:25 GMT",
#                    "ContentLength": "265",
#                    "ETag": '"40d06eb6194712ac1c915783004ef730"',
#                    "ServerSideEncryption": "AES256",
#                    "Metadata": {
#                        'mykey1': 'value1',
#                        'mykey2': 'value2',
#                    }}
#        response_data = get_response(self.session, put_object,
#                                     http_response)[1]
#        self.assertEqual(response_data, expected)
#
#    def test_list_objects_with_invalid_content_length(self):
#        http_response = Mock()
#        http_response.encoding = 'utf-8'
#        http_response.headers = CaseInsensitiveDict(
#            {'Date': 'Thu, 22 Aug 2013 02:11:57 GMT',
#             # We say we have 265 bytes but we're returning 0,
#             # this should raise an exception because this is not
#             # a HEAD request.
#             'Content-Length': '265',
#             'x-amz-request-id': '2B74ECB010FF029E',
#             'ETag': '"40d06eb6194712ac1c915783004ef730"',
#             'Server': 'AmazonS3',
#             'content-type': 'binary/octet-stream',
#             'Content-Type': 'binary/octet-stream',
#             'accept-ranges': 'bytes',
#             'Last-Modified': 'Tue, 20 Aug 2013 18:33:25 GMT',
#             'x-amz-server-side-encryption': 'AES256'
#             })
#        http_response.content = ''
#        http_response.request.method = 'GET'
#        list_objects = self.s3.get_operation('ListObjects')
#        expected = {"AcceptRanges": "bytes",
#                    "ContentType": "binary/octet-stream",
#                    "LastModified": "Tue, 20 Aug 2013 18:33:25 GMT",
#                    "ContentLength": "265",
#                    "ETag": '"40d06eb6194712ac1c915783004ef730"',
#                    "ServerSideEncryption": "AES256"
#                    }
#        with self.assertRaises(IncompleteReadError):
#            response_data = get_response(self.session, list_objects,
#                                         http_response)[1]
#
#    def test_head_object_with_json(self):
#        http_response = Mock()
#        http_response.encoding = 'utf-8'
#        http_response.headers = CaseInsensitiveDict(
#            {'Date': 'Thu, 22 Aug 2013 02:11:57 GMT',
#             'Content-Length': '0',
#             'x-amz-request-id': '2B74ECB010FF029E',
#             'ETag': '"40d06eb6194712ac1c915783004ef730"',
#             'Server': 'AmazonS3',
#             'content-type': 'application/json',
#             'Content-Type': 'application/json',
#             'accept-ranges': 'bytes',
#             'Last-Modified': 'Tue, 20 Aug 2013 18:33:25 GMT',
#             'x-amz-server-side-encryption': 'AES256'})
#        http_response.content = ''
#        put_object = self.s3.get_operation('HeadObject')
#        expected = {"AcceptRanges": "bytes",
#                    "ContentType": "application/json",
#                    "LastModified": "Tue, 20 Aug 2013 18:33:25 GMT",
#                    "ContentLength": "0",
#                    "ETag": '"40d06eb6194712ac1c915783004ef730"',
#                    "ServerSideEncryption": "AES256"
#                    }
#        response_data = get_response(self.session, put_object,
#                                     http_response)[1]
#        self.assertEqual(response_data, expected)
