# Copyright 2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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
from nose.tools import assert_equal

from tests import unittest
from botocore.stub import Stubber, StubAssertionError
from botocore.paginate import TokenDecoder, TokenEncoder
from botocore.compat import six
import botocore.session


class TestRDSPagination(unittest.TestCase):
    def setUp(self):
        self.region = 'us-west-2'
        self.session = botocore.session.get_session()
        self.client = self.session.create_client(
            'rds', self.region)
        self.stubber = Stubber(self.client)

    def test_can_specify_zero_marker(self):
        service_response = {
            'LogFileData': 'foo',
            'Marker': '2',
            'AdditionalDataPending': True
        }
        expected_params = {
            'DBInstanceIdentifier': 'foo',
            'LogFileName': 'bar',
            'NumberOfLines': 2,
            'Marker': '0'
        }
        function_name = 'download_db_log_file_portion'

        # The stubber will assert that the function is called with the expected
        # parameters.
        self.stubber.add_response(
            function_name, service_response, expected_params)
        self.stubber.activate()

        try:
            paginator = self.client.get_paginator(function_name)
            result = paginator.paginate(
                DBInstanceIdentifier='foo',
                LogFileName='bar',
                NumberOfLines=2,
                PaginationConfig={
                    'StartingToken': '0',
                    'MaxItems': 3
                }).build_full_result()
            self.assertEqual(result['LogFileData'], 'foo')
            self.assertIn('NextToken', result)
        except StubAssertionError as e:
            self.fail(str(e))


def test_token_encoding():
    cases = [
        {'foo': 'bar'},
        {'foo': b'bar'},
        {'foo': {'bar': b'baz'}},
        {'foo': ['bar', b'baz']},
        {'foo': b'\xff'},
        {'foo': {'bar': b'baz', 'bin': [b'bam']}},
    ]

    for token_dict in cases:
        yield assert_token_encodes_and_decodes, token_dict


def assert_token_encodes_and_decodes(token_dict):
    encoded = TokenEncoder().encode(token_dict)
    assert isinstance(encoded, six.string_types)
    decoded = TokenDecoder().decode(encoded)
    assert_equal(decoded, token_dict)
