from botocore.stub import Stubber
from tests import BaseSessionTest


class TestSagemaker(BaseSessionTest):
    def setUp(self):
        super().setUp()
        self.region = 'us-west-2'
        self.client = self.session.create_client('sagemaker', self.region)
        self.stubber = Stubber(self.client)
        self.stubber.activate()
        self.hook_calls = []

    def _hook(self, **kwargs):
        self.hook_calls.append(kwargs['event_name'])

    def tearDown(self):
        super().tearDown()
        self.stubber.deactivate()

    def test_event_with_old_prefix(self):
        self.client.meta.events.register(
            'provide-client-params.sagemaker.ListEndpoints', self._hook
        )
        self.stubber.add_response('list_endpoints', {'Endpoints': []})
        self.client.list_endpoints()
        self.assertEqual(
            self.hook_calls, ['provide-client-params.sagemaker.ListEndpoints']
        )

    def test_event_with_new_prefix(self):
        self.client.meta.events.register(
            'provide-client-params.api.sagemaker.ListEndpoints', self._hook
        )
        self.stubber.add_response('list_endpoints', {'Endpoints': []})
        self.client.list_endpoints()
        self.assertEqual(
            self.hook_calls, ['provide-client-params.sagemaker.ListEndpoints']
        )


class TestSagemakerWaiters(BaseSessionTest):
    """Regression tests for GH #3782.

    DescribeImage/DescribeImageVersion return a ``ResourceNotFound``
    error (per the service model's declared error shape for these
    operations) once the resource has actually been deleted, not
    ``ResourceNotFoundException``. The image_deleted/image_version_deleted
    waiters previously matched on the wrong (nonexistent) shape name, so
    a successful deletion was incorrectly reported as a waiter failure.
    """

    def setUp(self):
        super().setUp()
        self.region = 'us-west-2'
        self.client = self.session.create_client('sagemaker', self.region)
        self.stubber = Stubber(self.client)
        self.stubber.activate()

    def tearDown(self):
        super().tearDown()
        self.stubber.deactivate()

    def test_image_deleted_waiter_succeeds_on_resource_not_found(self):
        self.stubber.add_client_error(
            'describe_image',
            service_error_code='ResourceNotFound',
            http_status_code=404,
        )
        waiter = self.client.get_waiter('image_deleted')
        # Should not raise: a ResourceNotFound error is the documented
        # success condition for this waiter (the image is gone). Override
        # the config so a mismatch fails fast instead of sleeping through
        # 60s waits before timing out.
        waiter.wait(
            ImageName='some-image',
            WaiterConfig={'Delay': 1, 'MaxAttempts': 1},
        )

    def test_image_version_deleted_waiter_succeeds_on_resource_not_found(self):
        self.stubber.add_client_error(
            'describe_image_version',
            service_error_code='ResourceNotFound',
            http_status_code=404,
        )
        waiter = self.client.get_waiter('image_version_deleted')
        waiter.wait(
            ImageName='some-image',
            Version=1,
            WaiterConfig={'Delay': 1, 'MaxAttempts': 1},
        )
