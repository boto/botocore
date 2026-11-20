"""End-to-end test for NO_PROXY re-evaluation across redirect-style flows.

This test exercises the real socket path through ``URLLib3Session``: two
sequential requests through the same session, where one host matches
``NO_PROXY`` and the other does not. With the per-request bypass check in
place, the first request must go direct and the second must go through the
proxy. Without it (the legacy behaviour), the bypass decision is frozen at
session-construction time, so the second request also bypasses the proxy.
"""

import contextlib
import socket
import socketserver
import threading
from http.server import BaseHTTPRequestHandler

from botocore.awsrequest import AWSRequest
from botocore.httpsession import URLLib3Session
from tests import mock, unittest


def _unused_port():
    with contextlib.closing(socket.socket()) as sock:
        sock.bind(('127.0.0.1', 0))
        return sock.getsockname()[1]


class _RecordingHandler(BaseHTTPRequestHandler):
    """HTTP handler that records every request path and host header."""

    received = []
    ready = None  # set in setUp

    def do_GET(self):
        type(self).received.append(
            {
                'path': self.path,
                'host': self.headers.get('Host', ''),
            }
        )
        self.send_response(200)
        self.send_header('Content-Length', '2')
        self.end_headers()
        self.wfile.write(b'ok')

    def log_message(self, format, *args):
        pass


def _serve(handler_cls, port, request_count):
    address = ('127.0.0.1', port)
    server = socketserver.TCPServer(
        address, handler_cls, bind_and_activate=False
    )
    server.allow_reuse_address = True
    server.server_bind()
    server.server_activate()
    handler_cls.ready.set()
    try:
        for _ in range(request_count):
            server.handle_request()
    finally:
        server.server_close()


class TestNoProxyAcrossRedirect(unittest.TestCase):
    def setUp(self):
        self.backend_port = _unused_port()
        self.proxy_port = _unused_port()

        class BackendHandler(_RecordingHandler):
            received = []
            ready = threading.Event()

        class ProxyHandler(_RecordingHandler):
            received = []
            ready = threading.Event()

        self.BackendHandler = BackendHandler
        self.ProxyHandler = ProxyHandler

        self.backend_thread = threading.Thread(
            target=_serve,
            args=(BackendHandler, self.backend_port, 1),
            daemon=True,
        )
        self.proxy_thread = threading.Thread(
            target=_serve,
            args=(ProxyHandler, self.proxy_port, 1),
            daemon=True,
        )
        self.backend_thread.start()
        self.proxy_thread.start()
        self.assertTrue(BackendHandler.ready.wait(timeout=5))
        self.assertTrue(ProxyHandler.ready.wait(timeout=5))

    def tearDown(self):
        self.backend_thread.join(timeout=5)
        self.proxy_thread.join(timeout=5)

    def test_no_proxy_re_evaluated_across_sequential_requests(self):
        proxy_url = f'http://127.0.0.1:{self.proxy_port}'
        initial_url = f'http://127.0.0.1:{self.backend_port}/initial'
        redirect_url = f'http://localhost:{self.backend_port}/redirect'

        env = {
            'HTTP_PROXY': proxy_url,
            'NO_PROXY': '127.0.0.1',
        }
        with mock.patch.dict('os.environ', env, clear=True):
            session = URLLib3Session(proxies={'http': proxy_url})

            req1 = AWSRequest(
                method='GET', url=initial_url, headers={}, data=b''
            )
            resp1 = session.send(req1.prepare())
            self.assertEqual(resp1.status_code, 200)

            req2 = AWSRequest(
                method='GET', url=redirect_url, headers={}, data=b''
            )
            resp2 = session.send(req2.prepare())
            self.assertEqual(resp2.status_code, 200)

            session.close()

        self.assertEqual(
            len(self.BackendHandler.received),
            1,
            'NO_PROXY host should have been contacted directly once',
        )
        self.assertEqual(self.BackendHandler.received[0]['path'], '/initial')

        self.assertEqual(
            len(self.ProxyHandler.received),
            1,
            'Redirect target (not in NO_PROXY) should go via the proxy',
        )
        proxy_req = self.ProxyHandler.received[0]
        self.assertEqual(proxy_req['path'], redirect_url)
        self.assertIn('localhost', proxy_req['host'])
