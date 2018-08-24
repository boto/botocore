from mock import patch, Mock, ANY
from tests import unittest
from nose.tools import raises
from urllib3.exceptions import NewConnectionError, ProtocolError

from botocore.vendored import six
from botocore.awsrequest import AWSRequest
from botocore.awsrequest import AWSHTTPConnectionPool, AWSHTTPSConnectionPool
from botocore.httpsession import get_cert_path
from botocore.httpsession import URLLib3Session, ProxyConfiguration
from botocore.exceptions import ConnectionClosedError, EndpointConnectionError


class TestProxyConfiguration(unittest.TestCase):
    def setUp(self):
        self.url = 'http://localhost/'
        self.auth_url = 'http://user:pass@localhost/'
        self.proxy_config = ProxyConfiguration(
            proxies={'http': 'http://localhost:8081/'}
        )

    def update_http_proxy(self, url):
        self.proxy_config = ProxyConfiguration(
            proxies={'http': url}
        )

    def test_construct_proxy_headers_with_auth(self):
        headers = self.proxy_config.proxy_headers_for(self.auth_url)
        proxy_auth = headers.get('Proxy-Authorization')
        self.assertEqual('Basic dXNlcjpwYXNz', proxy_auth)

    def test_construct_proxy_headers_without_auth(self):
        headers = self.proxy_config.proxy_headers_for(self.url)
        self.assertEqual({}, headers)

    def test_proxy_for_url_no_slashes(self):
        self.update_http_proxy('localhost:8081/')
        proxy_url = self.proxy_config.proxy_url_for(self.url)
        self.assertEqual('http://localhost:8081/', proxy_url)

    def test_proxy_for_url_no_protocol(self):
        self.update_http_proxy('//localhost:8081/')
        proxy_url = self.proxy_config.proxy_url_for(self.url)
        self.assertEqual('http://localhost:8081/', proxy_url)

    def test_fix_proxy_url_has_protocol_http(self):
        proxy_url = self.proxy_config.proxy_url_for(self.url)
        self.assertEqual('http://localhost:8081/', proxy_url)


class TestHttpSessionUtils(unittest.TestCase):
    def test_get_cert_path_path(self):
        path = '/some/path'
        cert_path = get_cert_path(path)
        self.assertEqual(path, cert_path)

    def test_get_cert_path_certifi_or_default(self):
        with patch('botocore.httpsession.where') as where:
            path = '/bundle/path'
            where.return_value = path
            cert_path = get_cert_path(True)
            self.assertEqual(path, cert_path)


class TestURLLib3Session(unittest.TestCase):
    def setUp(self):
        self.request = AWSRequest(
            method='GET',
            url='http://example.com/',
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

        self.pool_patch = patch('botocore.httpsession.PoolManager')
        self.proxy_patch = patch('botocore.httpsession.proxy_from_url')
        self.pool_manager_cls = self.pool_patch.start()
        self.proxy_manager_fun = self.proxy_patch.start()
        self.pool_manager_cls.return_value = self.pool_manager
        self.proxy_manager_fun.return_value = self.pool_manager

    def tearDown(self):
        self.pool_patch.stop()

    def assert_request_sent(self, headers=None, body=None, url='/'):
        if headers is None:
            headers = {}

        self.connection.urlopen.assert_called_once_with(
            method=self.request.method,
            url=url,
            body=body,
            headers=headers,
            retries=False,
            assert_same_host=False,
            preload_content=False,
            decode_content=False,
        )

    def test_forwards_max_pool_size(self):
        URLLib3Session(max_pool_connections=22)
        self.pool_manager_cls.assert_called_with(
            maxsize=22,
            timeout=ANY,
            strict=True,
            ssl_context=ANY,
        )

    def test_basic_request(self):
        session = URLLib3Session()
        session.send(self.request.prepare())
        self.assert_request_sent()
        self.response.stream.assert_called_once_with()

    def test_basic_streaming_request(self):
        session = URLLib3Session()
        self.request.stream_output = True
        session.send(self.request.prepare())
        self.assert_request_sent()
        self.response.stream.assert_not_called()

    def test_basic_https_request(self):
        session = URLLib3Session()
        self.request.url = 'https://example.com/'
        session.send(self.request.prepare())
        self.assert_request_sent()

    def test_basic_https_proxy_request(self):
        proxies = {'https': 'http://proxy.com'}
        session = URLLib3Session(proxies=proxies)
        self.request.url = 'https://example.com/'
        session.send(self.request.prepare())
        self.proxy_manager_fun.assert_any_call(
            proxies['https'],
            proxy_headers={},
            maxsize=ANY,
            timeout=ANY,
            strict=True,
            ssl_context=ANY,
        )
        self.assert_request_sent()

    def test_basic_proxy_request_caches_manager(self):
        proxies = {'https': 'http://proxy.com'}
        session = URLLib3Session(proxies=proxies)
        self.request.url = 'https://example.com/'
        session.send(self.request.prepare())
        # assert we created the proxy manager
        self.proxy_manager_fun.assert_any_call(
            proxies['https'],
            proxy_headers={},
            maxsize=ANY,
            timeout=ANY,
            strict=True,
            ssl_context=ANY,
        )
        session.send(self.request.prepare())
        # assert that we did not create another proxy manager
        self.assertEqual(self.proxy_manager_fun.call_count, 1)

    def test_basic_http_proxy_request(self):
        proxies = {'http': 'http://proxy.com'}
        session = URLLib3Session(proxies=proxies)
        session.send(self.request.prepare())
        self.proxy_manager_fun.assert_any_call(
            proxies['http'],
            proxy_headers={},
            maxsize=ANY,
            timeout=ANY,
            strict=True,
            ssl_context=ANY,
        )
        self.assert_request_sent(url=self.request.url)

    def test_ssl_context_is_explicit(self):
        session = URLLib3Session()
        session.send(self.request.prepare())
        _, manager_kwargs = self.pool_manager_cls.call_args
        self.assertIsNotNone(manager_kwargs.get('ssl_context'))

    def test_proxy_request_ssl_context_is_explicit(self):
        proxies = {'http': 'http://proxy.com'}
        session = URLLib3Session(proxies=proxies)
        session.send(self.request.prepare())
        _, proxy_kwargs = self.proxy_manager_fun.call_args
        self.assertIsNotNone(proxy_kwargs.get('ssl_context'))

    def make_request_with_error(self, error):
        self.connection.urlopen.side_effect = error
        session = URLLib3Session()
        session.send(self.request.prepare())

    @raises(EndpointConnectionError)
    def test_catches_new_connection_error(self):
        error = NewConnectionError(None, None)
        self.make_request_with_error(error)

    @raises(ConnectionClosedError)
    def test_catches_bad_status_line(self):
        error = ProtocolError(None)
        self.make_request_with_error(error)

    def test_aws_connection_classes_are_used(self):
        session = URLLib3Session()
        # ensure the pool manager is using the correct classes
        http_class = self.pool_manager.pool_classes_by_scheme.get('http')
        self.assertIs(http_class, AWSHTTPConnectionPool)
        https_class = self.pool_manager.pool_classes_by_scheme.get('https')
        self.assertIs(https_class, AWSHTTPSConnectionPool)
