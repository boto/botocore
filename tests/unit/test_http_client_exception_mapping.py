from nose.tools import assert_raises

from botocore import exceptions as botocore_exceptions
from botocore.vendored.requests import exceptions as requests_exceptions
from botocore.vendored.requests.packages.urllib3 import exceptions as urllib3_exceptions

EXCEPTION_MAPPING = [
    (botocore_exceptions.ReadTimeoutError, requests_exceptions.ReadTimeout),
    (botocore_exceptions.ReadTimeoutError, urllib3_exceptions.ReadTimeoutError),
    (botocore_exceptions.ConnectTimeoutError, requests_exceptions.ConnectTimeout),
    (botocore_exceptions.ProxyConnectionError, requests_exceptions.ProxyError),
    (botocore_exceptions.SSLError, requests_exceptions.SSLError),
]


def _raise_exception(exception):
    raise exception(endpoint_url=None, proxy_url=None, error=None)


def _test_exception_mapping(new_exception, old_exception):
    # assert that the new exception can still be caught by the old vendored one
    assert_raises(old_exception, _raise_exception, new_exception)


def test_http_client_exception_mapping():
    for new_exception, old_exception in EXCEPTION_MAPPING:
        yield _test_exception_mapping, new_exception, old_exception
