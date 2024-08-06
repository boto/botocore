# Copyright 2024 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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

from botocore.auth import (
    AUTH_TYPE_MAPS,
    AUTH_TYPE_TO_SIGNATURE_VERSION,
    BaseSigner,
    resolve_auth_type,
)
from botocore.exceptions import (
    UnknownSignatureVersionError,
)
from tests import mock, unittest

class TestAuthTraitResolution(unittest.TestCase):

    def test_auth_resolves_first_available(self):
        auth = ['aws.auth#foo', 'aws.auth#bar']
        bar_signer = mock.Mock(spec=BaseSigner)

        auth_types = AUTH_TYPE_MAPS.copy()
        auth_types['bar'] = bar_signer

        auth_type_conversions = AUTH_TYPE_TO_SIGNATURE_VERSION.copy()
        auth_type_conversions['aws.auth#foo'] = "foo"
        auth_type_conversions['aws.auth#bar'] = "bar"

        with mock.patch('botocore.auth.AUTH_TYPE_MAPS', auth_types):
            with mock.patch(
                'botocore.auth.AUTH_TYPE_TO_SIGNATURE_VERSION',
                auth_type_conversions,
            ):
                assert resolve_auth_type(auth) == 'bar'

    def test_invalid_auth_type_error(self):
        auth = ['aws.auth#invalidAuth']
        with self.assertRaises(UnknownSignatureVersionError):
            resolve_auth_type(auth)