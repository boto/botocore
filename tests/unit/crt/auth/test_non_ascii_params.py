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

"""Test for non-ASCII query parameter encoding in CRT signers.

This test ensures that query parameters containing non-ASCII UTF-8 characters
(e.g., Swedish å, ä, ö) are properly percent-encoded before being passed to
the AWS CRT library for signing. Without proper encoding, these characters
cause signature mismatches when AWS validates the request.
"""

from botocore.awsrequest import AWSRequest
from botocore.credentials import Credentials
from tests import requires_crt


def _create_request_with_params(params):
    """Helper to create an AWSRequest with query parameters."""
    request = AWSRequest(
        method='GET', url='https://example.com', params=params, headers={}
    )
    request.context['payload_signing_enabled'] = False
    return request


def _get_crt_path_from_request(request, signer_class):
    """Helper to get the CRT path that would be signed."""
    credentials = Credentials('access_key', 'secret_key')
    region = 'us-east-1'
    service = 'vpc-lattice-svcs'

    signer = signer_class(credentials, service, region)
    crt_request = signer._crt_request_from_aws_request(request)
    return crt_request.path


@requires_crt()
class TestNonASCIIQueryParams:
    """Test that non-ASCII query parameters are properly URL-encoded."""

    def test_crt_sigv4_encodes_non_ascii_params(self):
        """Test CrtSigV4Auth properly encodes non-ASCII query parameters."""
        from botocore.crt.auth import CrtSigV4Auth

        # Test with Swedish characters
        request = _create_request_with_params({'q': 'åäö'})
        crt_path = _get_crt_path_from_request(request, CrtSigV4Auth)

        # Should be percent-encoded, not raw UTF-8
        assert crt_path == '/?q=%C3%A5%C3%A4%C3%B6'

        # Verify it's ASCII-safe
        crt_path.encode('ascii')  # Should not raise UnicodeEncodeError

    def test_crt_sigv4asym_encodes_non_ascii_params(self):
        """Test CrtSigV4AsymAuth properly encodes non-ASCII query parameters."""
        from botocore.crt.auth import CrtSigV4AsymAuth

        # Test with Swedish characters
        request = _create_request_with_params({'q': 'åäö'})
        crt_path = _get_crt_path_from_request(request, CrtSigV4AsymAuth)

        # Should be percent-encoded, not raw UTF-8
        assert crt_path == '/?q=%C3%A5%C3%A4%C3%B6'

        # Verify it's ASCII-safe
        crt_path.encode('ascii')  # Should not raise UnicodeEncodeError

    def test_encodes_mixed_ascii_and_non_ascii(self):
        """Test encoding of parameters with mixed ASCII and non-ASCII content."""
        from botocore.crt.auth import CrtSigV4Auth

        request = _create_request_with_params({'q': 'adapter för MIDI'})
        crt_path = _get_crt_path_from_request(request, CrtSigV4Auth)

        # Should encode non-ASCII 'ö' and space
        assert crt_path == '/?q=adapter%20f%C3%B6r%20MIDI'

        # Verify it's ASCII-safe
        crt_path.encode('ascii')

    def test_preserves_safe_characters(self):
        """Test that safe characters (hyphens, underscores, etc.) are preserved."""
        from botocore.crt.auth import CrtSigV4Auth

        request = _create_request_with_params(
            {'q': 'test-query_value.txt~file'}
        )
        crt_path = _get_crt_path_from_request(request, CrtSigV4Auth)

        # Safe characters should not be encoded
        assert crt_path == '/?q=test-query_value.txt~file'

    def test_encodes_spaces(self):
        """Test that spaces are properly encoded."""
        from botocore.crt.auth import CrtSigV4Auth

        request = _create_request_with_params({'q': 'test value'})
        crt_path = _get_crt_path_from_request(request, CrtSigV4Auth)

        # Spaces should be encoded as %20
        assert crt_path == '/?q=test%20value'

    def test_encodes_multiple_params_with_non_ascii(self):
        """Test encoding of multiple parameters including non-ASCII."""
        from botocore.crt.auth import CrtSigV4Auth

        request = _create_request_with_params(
            {'query': 'åäö', 'name': 'test', 'city': 'Göteborg'}
        )
        crt_path = _get_crt_path_from_request(request, CrtSigV4Auth)

        # All non-ASCII characters should be encoded
        # Note: dict order may vary, so we check for presence
        assert 'query=%C3%A5%C3%A4%C3%B6' in crt_path
        assert 'name=test' in crt_path
        assert 'city=G%C3%B6teborg' in crt_path

        # Verify entire path is ASCII-safe
        crt_path.encode('ascii')

    def test_param_keys_are_also_encoded(self):
        """Test that non-ASCII parameter keys are also encoded."""
        from botocore.crt.auth import CrtSigV4Auth

        # Using a non-ASCII key (contrived example, but possible)
        request = _create_request_with_params({'sök': 'value'})
        crt_path = _get_crt_path_from_request(request, CrtSigV4Auth)

        # Key should be encoded
        assert 's%C3%B6k=value' in crt_path

        # Verify it's ASCII-safe
        crt_path.encode('ascii')
