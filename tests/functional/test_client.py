import unittest

import botocore
from botocore.exceptions import DataNotFoundError
from tests import mock

FAKE_SERVICE_MODEL = {
    'metadata': {
        'serviceFullName': 'Custom Service',
        'apiVersion': '2020-01-01',
        'endpointPrefix': 'customservice',
        'signatureVersion': 'v4',
        'protocol': 'json',
        'serviceId': 'CustomService',
    },
    'operations': {},
    'shapes': {},
}


def _fake_load_service_model(service_name, type_name, api_version=None):
    if type_name == 'service-2':
        return FAKE_SERVICE_MODEL
    raise DataNotFoundError(data_path='endpoint-rule-set-1')


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

    def test_client_creates_with_missing_endpoint_ruleset(self):
        # Without explicit api_version, load_service_model converts the
        # DataNotFoundError into UnknownServiceError via
        # determine_latest_version. Verify the fallback works.
        loader = self.session.get_component('data_loader')
        with mock.patch.object(
            loader, 'load_service_model', _fake_load_service_model
        ):
            client = self.session.create_client(
                'customservice', region_name='us-east-1'
            )
        self.assertIsNotNone(client)

    def test_client_creates_with_missing_endpoint_ruleset_explicit_version(
        self,
    ):
        # With explicit api_version, load_service_model skips
        # determine_latest_version and load_data raises DataNotFoundError
        # directly. Verify the fallback catches this too.
        loader = self.session.get_component('data_loader')
        with mock.patch.object(
            loader, 'load_service_model', _fake_load_service_model
        ):
            client = self.session.create_client(
                'customservice',
                region_name='us-east-1',
                api_version='2020-01-01',
            )
        self.assertIsNotNone(client)
