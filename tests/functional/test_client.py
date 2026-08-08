import unittest

import botocore
from tests import BaseSessionTest, ClientHTTPStubber


class TestCreateClients(unittest.TestCase):
    def setUp(self):
        self.session = botocore.session.get_session()

    def test_client_can_clone_with_service_events(self):
        # We should also be able to create a client object.
        client = self.session.create_client('s3', region_name='us-west-2')
        # We really just want to ensure create_client doesn't raise
        # an exception, but we'll double check that the client looks right.
        self.assertTrue(hasattr(client, 'list_buckets'))

    def test_client_raises_exception_invalid_region(self):
        with self.assertRaisesRegex(ValueError, ('invalid region name')):
            self.session.create_client(
                'cloudformation', region_name='invalid region name'
            )


class TestRequestContextReadTimeout(BaseSessionTest):
    def test_read_timeout_override_reaches_prepared_request(self):
        # A handler can set a per-invocation read timeout in the request
        # context, which is carried through to the prepared request that
        # is passed to the http session's send() method.
        client = self.session.create_client('s3', region_name='us-west-2')

        def set_read_timeout(context, **kwargs):
            context['read_timeout'] = 300

        client.meta.events.register(
            'before-parameter-build.s3.ListBuckets', set_read_timeout
        )
        with ClientHTTPStubber(client) as http_stubber:
            http_stubber.add_response(
                body=b'<?xml version="1.0" encoding="UTF-8"?>'
                b'<ListAllMyBucketsResult><Buckets></Buckets>'
                b'</ListAllMyBucketsResult>'
            )
            client.list_buckets()
        prepared_request = http_stubber.requests[0]
        self.assertEqual(prepared_request.context['read_timeout'], 300)
