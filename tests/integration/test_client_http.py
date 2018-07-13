import time
import select
import socket
import random
import threading
from tests import unittest
from contextlib import contextmanager

import botocore.session
from botocore.config import Config
from botocore.exceptions import EndpointConnectionError, ConnectionClosedError
from botocore.vendored.six.moves import BaseHTTPServer, socketserver
from botocore.exceptions import ReadTimeoutError, EndpointConnectionError


class TestClientHTTPBehavior(unittest.TestCase):
    def setUp(self):
        self.port = random_port()
        self.localhost = 'http://localhost:%s/' % self.port
        self.session = botocore.session.get_session()

    def test_can_proxy_https_request_with_auth(self):
        proxy_url = 'http://user:pass@localhost:%s/' % self.port
        config = Config(proxies={'https': proxy_url})
        client = self.session.create_client('ec2', config=config)

        class AuthProxyHandler(ProxyHandler):
            def validate_auth(self):
                proxy_auth = self.headers.get('Proxy-Authorization')
                return proxy_auth == 'Basic dXNlcjpwYXNz'

        try:
            with background(run_server, args=(AuthProxyHandler, self.port)):
                client.describe_regions()
        except BackgroundTaskFailed:
            self.fail('Background task did not exit, proxy was not used.')

    def test_read_timeout_exception(self):
        config = Config(read_timeout=0.1, retries={'max_attempts': 0})
        client = self.session.create_client('ec2', endpoint_url=self.localhost,
                                            config=config)

        class FakeEC2(SimpleHandler):
            msg = b'<response/>'
            def get_length(self):
                return len(self.msg)

            def get_body(self):
                time.sleep(1)
                return self.msg

        try:
            with background(run_server, args=(FakeEC2, self.port)):
                client.describe_regions()
        except ReadTimeoutError:
            # Note: This was vendored requests ConnectionError & ReadTimeout
            pass
        except BackgroundTaskFailed:
            self.fail('Fake EC2 service was not called.')
        else:
            self.fail('Excepted exception was not thrown')

    def test_connect_timeout_exception(self):
        config = Config(connect_timeout=0.2, retries={'max_attempts': 0})
        client = self.session.create_client('ec2', endpoint_url=self.localhost,
                                            config=config)

        def no_accept_server():
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(('', self.port))
            time.sleep(4)
            sock.close()

        try:
            with background(no_accept_server):
                time.sleep(2)
                client.describe_regions()
        except EndpointConnectionError:
            pass
        except BackgroundTaskFailed:
            self.fail('Server failed to exit in a timely manner.')
        else:
            self.fail('Excepted exception was not thrown')

    def test_invalid_host_gaierror(self):
        config = Config(retries={'max_attempts': 0})
        endpoint = 'https://ec2.us-weast-1.amazonaws.com/'
        client = self.session.create_client('ec2', endpoint_url=endpoint,
                                            config=config)
        try:
            client.describe_regions()
        except EndpointConnectionError:
            pass

    def test_bad_status_line(self):
        config = Config(retries={'max_attempts': 0})
        client = self.session.create_client('ec2', endpoint_url=self.localhost,
                                            config=config)

        class BadStatusHandler(BaseHTTPServer.BaseHTTPRequestHandler):
            def do_POST(self):
                self.wfile.write(b'garbage')

        try:
            with background(run_server, args=(BadStatusHandler, self.port)):
                client.describe_regions()
        except ConnectionClosedError:
            pass
        except BackgroundTaskFailed:
            self.fail('Fake EC2 service was not called.')
        else:
            self.fail('Excepted exception was not thrown')


def random_port():
    return random.randint(8080, 9000)


class SimpleHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    status = 200

    def get_length(self):
        return 0

    def get_body(self):
        return b''

    def do_GET(self):
        length = str(self.get_length())
        self.send_response(self.status)
        self.send_header('Content-Length', length)
        self.end_headers()
        self.wfile.write(self.get_body())

    do_POST = do_PUT = do_GET


class ProxyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    tunnel_chunk_size = 1024
    def _tunnel(self, client, remote):
        client.setblocking(0)
        remote.setblocking(0)
        sockets = [client, remote]
        while True:
            readable, writeable, _ = select.select(sockets, sockets, [], 1)
            if client in readable and remote in writeable:
                client_bytes = client.recv(self.tunnel_chunk_size)
                if not client_bytes:
                    break
                remote.sendall(client_bytes)
            if remote in readable and client in writeable:
                remote_bytes = remote.recv(self.tunnel_chunk_size)
                if not remote_bytes:
                    break
                client.sendall(remote_bytes)

    def do_CONNECT(self):
        if not self.validate_auth():
            self.send_response(401)
            self.end_headers()
            return

        self.send_response(200)
        self.end_headers()

        remote_host, remote_port = self.path.split(':')
        remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        remote_socket.connect((remote_host, int(remote_port)))

        self._tunnel(self.request, remote_socket)
        remote_socket.close()

    def validate_auth(self):
        return True


class BackgroundTaskFailed(Exception):
    pass


@contextmanager
def background(target, args=(), timeout=10):
    thread = threading.Thread(target=target, args=args, daemon=True)
    thread.start()
    yield target
    thread.join(timeout=timeout)
    if thread.is_alive():
        msg = 'Background task did not exit in a timely manner.'
        raise BackgroundTaskFailed(msg)


def run_server(handler, port):
    address = ('', port)
    httpd = socketserver.TCPServer(address, handler, bind_and_activate=False)
    httpd.allow_reuse_address = True
    httpd.server_bind()
    httpd.server_activate()
    httpd.handle_request()
    httpd.server_close()
