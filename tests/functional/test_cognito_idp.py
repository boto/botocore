# Copyright 2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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
import mock

from nose.tools import assert_false

from tests import create_session, ClientHTTPStubber


def test_unsigned_operations():
    operation_params = {
        'change_password': {
            'PreviousPassword': 'myoldbadpassword',
            'ProposedPassword': 'mynewgoodpassword',
            'AccessToken': 'foobar'
        },
        'confirm_forgot_password': {
            'ClientId': 'foo',
            'Username': 'myusername',
            'ConfirmationCode': 'thisismeforreal',
            'Password': 'whydowesendpasswordsviaemail'
        },
        'confirm_sign_up': {
            'ClientId': 'foo',
            'Username': 'myusername',
            'ConfirmationCode': 'ireallydowanttosignup'
        },
        'delete_user': {
            'AccessToken': 'foobar'
        },
        'delete_user_attributes': {
            'UserAttributeNames': ['myattribute'],
            'AccessToken': 'foobar'
        },
        'forgot_password': {
            'ClientId': 'foo',
            'Username': 'myusername'
        },
        'get_user': {
            'AccessToken': 'foobar'
        },
        'get_user_attribute_verification_code': {
            'AttributeName': 'myattribute',
            'AccessToken': 'foobar'
        },
        'resend_confirmation_code': {
            'ClientId': 'foo',
            'Username': 'myusername'
        },
        'set_user_settings': {
            'AccessToken': 'randomtoken',
            'MFAOptions': [{
                'DeliveryMedium': 'SMS',
                'AttributeName': 'someattributename'
            }]
        },
        'sign_up': {
            'ClientId': 'foo',
            'Username': 'bar',
            'Password': 'mysupersecurepassword',
        },
        'update_user_attributes': {
            'UserAttributes': [{
                'Name': 'someattributename',
                'Value': 'newvalue'
            }],
            'AccessToken': 'foobar'
        },
        'verify_user_attribute': {
            'AttributeName': 'someattributename',
            'Code': 'someverificationcode',
            'AccessToken': 'foobar'
        },
    }

    environ = {
        'AWS_ACCESS_KEY_ID': 'access_key',
        'AWS_SECRET_ACCESS_KEY': 'secret_key',
        'AWS_CONFIG_FILE': 'no-exist-foo',
    }

    with mock.patch('os.environ', environ):
        session = create_session()
        session.config_filename = 'no-exist-foo'
        client = session.create_client('cognito-idp', 'us-west-2')

        for operation, params in operation_params.items():
            test_case = UnsignedOperationTestCase(client, operation, params)
            yield test_case.run


class UnsignedOperationTestCase(object):
    def __init__(self, client, operation_name, parameters):
        self._client = client
        self._operation_name = operation_name
        self._parameters = parameters
        self._http_stubber = ClientHTTPStubber(self._client)

    def run(self):
        operation = getattr(self._client, self._operation_name)

        self._http_stubber.add_response(body=b'{}')
        with self._http_stubber:
            operation(**self._parameters)
            request = self._http_stubber.requests[0]

        assert_false(
            'authorization' in request.headers,
            'authorization header found in unsigned operation'
        )
