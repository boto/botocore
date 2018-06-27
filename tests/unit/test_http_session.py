from mock import patch, Mock, ANY
from tests import unittest
from nose.tools import raises
from urllib3.exceptions import NewConnectionError, ProtocolError

from botocore.http_session import (
    construct_basic_auth,
    get_auth_from_url,
    get_proxy_headers,
    get_cert_path,
    fix_proxy_url,
)

from botocore.vendored import six
from botocore.awsrequest import AWSRequest
from botocore.http_session import Urllib3Session
from botocore.exceptions import ConnectionClosedError, EndpointConnectionError


class TestHttpSessionUtils(unittest.TestCase):

    def setUp(self):
        self.url = 'http://localhost/'
        self.auth_url = 'http://user:pass@localhost/'

    def test_construct_basic_auth(self):
        auth = construct_basic_auth('user', 'pass')
        self.assertEqual('Basic dXNlcjpwYXNz', auth)

    def test_get_auth_from_url(self):
        username, password = get_auth_from_url(self.auth_url)
        self.assertEqual('user', username)
        self.assertEqual('pass', password)

    def test_get_auth_from_url_no_auth(self):
        username, password = get_auth_from_url(self.url)
        self.assertIsNone(username)
        self.assertIsNone(password)

    def test_get_proxy_headers(self):
        headers = get_proxy_headers(self.auth_url)
        proxy_auth = headers.get('Proxy-Authorization')
        self.assertEqual('Basic dXNlcjpwYXNz', proxy_auth)

    def test_fix_proxy_url_no_slashes(self):
        url = 'localhost:8081/'
        fixed_url = fix_proxy_url(url)
        self.assertEqual('http://localhost:8081/', fixed_url)

    def test_fix_proxy_url_no_protocol(self):
        url = '//localhost:8081/'
        fixed_url = fix_proxy_url(url)
        self.assertEqual('http://localhost:8081/', fixed_url)

    def test_fix_proxy_url_has_protocol_http(self):
        url = 'http://localhost:8081/'
        fixed_url = fix_proxy_url(url)
        self.assertEqual(url, fixed_url)

    def test_fix_proxy_url_has_protocol_https(self):
        url = 'https://localhost:8081/'
        fixed_url = fix_proxy_url(url)
        self.assertEqual(url, fixed_url)

    def test_get_cert_path_path(self):
        path = '/some/path'
        cert_path = get_cert_path(path)
        self.assertEqual(path, cert_path)

    def test_get_cert_path_certifi_or_default(self):
        with patch('botocore.http_session.where') as where:
            path = '/bundle/path'
            where.return_value = path
            cert_path = get_cert_path(True)
            self.assertEqual(path, cert_path)


class TestUrllib3Session(unittest.TestCase):

    def setUp(self):
        self.request = AWSRequest(
            method='GET',
            url='http://example.com',
            headers={},
            data=b'',
        )

        self.response = Mock()
        self.response.headers = {}
        self.response.stream.return_value = b''

        self.pool_manager = Mock()
        self.connection = Mock()
        self.connection.urlopen.return_value = self.response
        self.pool_manager.connection_from_url.return_value = self.connection

        self.pool_patch = patch('botocore.http_session.PoolManager')
        self.proxy_patch = patch('botocore.http_session.proxy_from_url')
        self.pool_manager_cls = self.pool_patch.start()
        self.proxy_manager_fun = self.proxy_patch.start()
        self.pool_manager_cls.return_value = self.pool_manager
        self.proxy_manager_fun.return_value = self.pool_manager

    def tearDown(self):
        self.pool_patch.stop()

    def asert_request_sent(self, headers=None, body=None):
        if headers is None:
            headers = {}

        self.connection.urlopen.assert_called_once_with(
            method=self.request.method,
            url=self.request.url,
            body=body,
            headers=headers,
            retries=False,
            assert_same_host=False,
            preload_content=False,
            decode_content=False,
        )

    def test_forwards_max_pool_size(self):
        Urllib3Session(max_pool_connections=22)
        self.pool_manager_cls.assert_called_with(maxsize=22, timeout=ANY,
                                                 strict=True)

    def test_basic_request(self):
        session = Urllib3Session()
        session.send(self.request.prepare())
        self.asert_request_sent()
        self.response.stream.assert_called_once_with()

    def test_basic_streaming_request(self):
        session = Urllib3Session()
        self.request.stream_output = True
        session.send(self.request.prepare())
        self.asert_request_sent()
        self.response.stream.assert_not_called()

    def test_basic_https_request(self):
        session = Urllib3Session()
        self.request.url = 'https://example.com'
        session.send(self.request.prepare())
        self.asert_request_sent()

    def test_basic_proxy_request(self):
        proxies = {'https': 'http://proxy.com'}
        session = Urllib3Session(proxies=proxies)
        self.request.url = 'https://example.com'
        session.send(self.request.prepare())
        self.proxy_manager_fun.assert_any_call(
            proxies['https'],
            proxy_headers={},
            maxsize=ANY,
            timeout=ANY,
            strict=True,
        )
        self.asert_request_sent()

    def make_request_with_error(self, error):
        self.connection.urlopen.side_effect = error
        session = Urllib3Session()
        session.send(self.request.prepare())

    @raises(EndpointConnectionError)
    def test_catches_new_connection_error(self):
        error = NewConnectionError(None, None)
        self.make_request_with_error(error)

    @raises(ConnectionClosedError)
    def test_catches_bad_status_line(self):
        error = ProtocolError(None)
        self.make_request_with_error(error)
