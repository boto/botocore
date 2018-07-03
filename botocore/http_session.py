import os.path
import logging
import socket
from base64 import b64encode

from urllib3 import PoolManager, proxy_from_url, Timeout
from urllib3.exceptions import NewConnectionError, ProtocolError

from botocore.vendored import six
from botocore.vendored.six.moves.urllib_parse import unquote
from botocore.awsrequest import AWSResponse
from botocore.compat import filter_ssl_warnings, urlparse
from botocore.exceptions import ConnectionClosedError, EndpointConnectionError

try:
    from urllib3.contrib import pyopenssl
    pyopenssl.extract_from_urllib3()
except ImportError:
    pass

filter_ssl_warnings()
logger = logging.getLogger(__name__)
DEFAULT_TIMEOUT = 60
MAX_POOL_CONNECTIONS = 10
# TODO: move the vendored cacert when we drop requests
DEFAULT_CA_BUNDLE = os.path.join(
    os.path.dirname(__file__), 'vendored', 'requests', 'cacert.pem'
)

try:
    from certifi import where
except ImportError:
    def where():
        return DEFAULT_CA_BUNDLE


def construct_basic_auth(username, password):
    auth_str = '{0}:{1}'.format(username, password)
    encoded_str = b64encode(auth_str.encode('ascii')).strip().decode()
    return 'Basic {0}'.format(encoded_str)


def get_auth_from_url(url):
    parsed_url = urlparse(url)
    try:
        return unquote(parsed_url.username), unquote(parsed_url.password)
    except (AttributeError, TypeError):
        return None, None


def get_proxy_headers(proxy_url):
    headers = {}
    username, password = get_auth_from_url(proxy_url)
    if username and password:
        basic_auth = construct_basic_auth(username, password)
        headers['Proxy-Authorization'] = basic_auth
    return headers


def fix_proxy_url(proxy_url):
    if proxy_url.startswith('http:') or proxy_url.startswith('https:'):
        return proxy_url
    elif proxy_url.startswith('//'):
        return 'http:' + proxy_url
    else:
        return 'http://' + proxy_url


def get_cert_path(verify):
    if verify is not True:
        return verify

    return where()


class Urllib3Session(object):
    def __init__(self,
                 verify=True,
                 proxies=None,
                 timeout=None,
                 max_pool_connections=MAX_POOL_CONNECTIONS,
    ):
        self._verify = verify
        self._proxies = proxies or {}
        if timeout is None:
            timeout=DEFAULT_TIMEOUT
        if not isinstance(timeout, (int, float)):
            timeout = Timeout(connect=timeout[0], read=timeout[1])
        self._timeout = timeout
        self._max_pool_connections = max_pool_connections
        self._proxy_managers = {}
        self._http_pool = PoolManager(
            strict=True,
            timeout=self._timeout,
            maxsize=self._max_pool_connections,
        )

    def _get_proxy_manager(self, proxy_url):
        proxy_url = fix_proxy_url(proxy_url)
        if proxy_url not in self._proxy_managers:
            proxy_headers = get_proxy_headers(proxy_url)
            self._proxy_managers[proxy_url] = proxy_from_url(
                proxy_url,
                strict=True,
                timeout=self._timeout,
                proxy_headers=proxy_headers,
                maxsize=self._max_pool_connections
            )

        return self._proxy_managers[proxy_url]

    def _path_url(self, parsed_url):
        path = parsed_url.path
        if not path:
            path = '/'
        if parsed_url.query:
            path = path + '?' + parsed_url.query
        return path

    def _verify_cert(self, conn, url, verify):
        if url.lower().startswith('https') and verify:
            conn.cert_reqs = 'CERT_REQUIRED'
            conn.ca_certs = get_cert_path(verify)
        else:
            conn.cert_reqs = 'CERT_NONE'
            conn.ca_certs = None

    def send(self, request):
        try:
            parsed_url = urlparse(request.url)
            proxy = self._proxies.get(parsed_url.scheme)
            url = self._path_url(parsed_url)

            if proxy:
                if parsed_url.scheme == 'http':
                    url = request.url
                connection_manager = self._get_proxy_manager(proxy)
            else:
                connection_manager = self._http_pool

            conn = connection_manager.connection_from_url(request.url)
            self._verify_cert(conn, request.url, self._verify)
            urllib_response = conn.urlopen(
                method=request.method,
                url=url,
                body=request.body,
                headers=request.headers,
                retries=False,
                assert_same_host=False,
                preload_content=False,
                decode_content=False,
            )

            http_response = AWSResponse(
                url=request.url,
                raw=urllib_response,
                status_code=urllib_response.status,
                headers=dict(urllib_response.headers.items()),
            )

            if not request.stream_output:
                # Cause the raw stream to be exhausted immediatly
                http_response.content

            return http_response
        except (NewConnectionError, socket.gaierror) as e:
            raise EndpointConnectionError(endpoint_url=request.url, error=e)
        except ProtocolError as e:
            raise ConnectionClosedError(
                request=request,
                endpoint_url=request.url
            )
