import unittest

import botocore
from botocore.compat import HAS_CRT

from tests import requires_crt
from tests.unit.auth.test_signers import (
    TestS3SigV4Auth, TestSigV4Presign, TestSigV4Resign
)

@requires_crt()
class TestCrtS3SigV4Auth(TestS3SigV4Auth):
    # Repeat TestS3SigV4Auth tests, but using CRT signer
    if HAS_CRT:
        AuthClass = botocore.crt.auth.CrtS3SigV4Auth

@requires_crt()
class TestCrtSigV4Resign(TestSigV4Resign):
    # Run same tests against CRT auth
    if HAS_CRT:
        AuthClass = botocore.crt.auth.CrtSigV4Auth

@requires_crt()
class TestCrtSigV4Presign(TestSigV4Presign):
    # Run same tests against CRT auth
    if HAS_CRT:
        AuthClass = botocore.crt.auth.CrtSigV4QueryAuth
