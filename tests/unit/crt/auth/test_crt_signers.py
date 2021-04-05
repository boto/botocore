import botocore

from tests import requires_crt
from tests.unit.auth.test_signers import (
    TestS3SigV4Auth, TestSigV4Presign, TestSigV4Resign
)


@requires_crt
class TestCrtS3SigV4Auth(TestS3SigV4Auth):
    # Repeat TestS3SigV4Auth tests, but using CRT signer

    def setUp(self):
        AuthClass = botocore.crt.auth.CrtS3SigV4Auth
        super().setUp()

@requires_crt
class TestCrtSigV4Resign(TestSigV4Resign):
    # Run same tests against CRT auth

    def setUp(self):
        AuthClass = botocore.crt.auth.CrtSigV4Auth
        super().setUp()

@requires_crt
class TestCrtSigV4Presign(TestSigV4Presign):
    # Run same tests against CRT auth

    def setUp(self):
        # Use CRT logging to see interim steps (canonical request, etc)
        # import awscrt.io
        # awscrt.io.init_logging(awscrt.io.LogLevel.Trace, 'stderr')
        AuthClass = botocore.crt.auth.CrtSigV4QueryAuth
        super().setUp()
