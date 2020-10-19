import unittest
import pytest
import botocore

class TestCreateClients(unittest.TestCase):
    def setUp(self):
        self.session = botocore.session.get_session()

    def test_client_can_clone_with_service_events(self):
        # We should also be able to create a client object.
        client = self.session.create_client('s3', region_name='us-west-2')
        # We really just want to ensure create_client doesn't raise
        # an exception, but we'll double check that the client looks right.
        assert hasattr(client, 'list_buckets')

    def test_client_raises_exception_invalid_region(self):
        with pytest.raises(ValueError, match=r'invalid region name'):
            self.session.create_client(
                'cloudformation', region_name='invalid region name')
