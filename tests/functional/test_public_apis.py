# Copyright 2012-2015 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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
from collections import defaultdict

import mock

from botocore.session import Session
from botocore.exceptions import NoCredentialsError
from botocore import xform_name


REGIONS = defaultdict(lambda: 'us-east-1')
PUBLIC_API_TESTS = {
    "cognito-identity": {
        "GetId": {"IdentityPoolId": "region:1234"},
        "GetOpenIdToken": {"IdentityId": "region:1234"},
        "UnlinkIdentity": {
            "IdentityId": "region:1234", "Logins": {}, "LoginsToRemove": []},
        "GetCredentialsForIdentity": {"IdentityId": "region:1234"},
    },
    "sts": {
        "AssumeRoleWithSaml": {
            "PrincipalArn": "a"*20, "RoleArn": "a"*20, "SAMLAssertion": "abcd",
        },
        "AssumeRoleWithWebIdentity": {
            "RoleArn": "a"*20,
            "RoleSessionName": "foo",
            "WebIdentityToken": "abcd",
        },
    },
}


class EarlyExit(BaseException):
    pass


def _test_public_apis_will_not_be_signed(func, kwargs):
    # TODO: fix with stubber / before send event
    with mock.patch('botocore.endpoint.Endpoint._send') as _send:
        _send.side_effect = EarlyExit("we don't care about response here")
        try:
            func(**kwargs)
        except EarlyExit:
            pass
        except NoCredentialsError:
            assert False, "NoCredentialsError should not be triggered"
        request = _send.call_args[0][0]
        sig_v2_disabled = 'SignatureVersion=2' not in request.url
        assert sig_v2_disabled, "SigV2 is incorrectly enabled"
        sig_v3_disabled = 'X-Amzn-Authorization' not in request.headers
        assert sig_v3_disabled, "SigV3 is incorrectly enabled"
        sig_v4_disabled = 'Authorization' not in request.headers
        assert sig_v4_disabled, "SigV4 is incorrectly enabled"


def test_public_apis_will_not_be_signed():
    session = Session()

    # Mimic the scenario that user does not have aws credentials setup
    session.get_credentials = mock.Mock(return_value=None)

    for service_name in PUBLIC_API_TESTS:
        client = session.create_client(service_name, REGIONS[service_name])
        for operation_name in PUBLIC_API_TESTS[service_name]:
            kwargs = PUBLIC_API_TESTS[service_name][operation_name]
            method = getattr(client, xform_name(operation_name))
            yield (_test_public_apis_will_not_be_signed, method, kwargs)
