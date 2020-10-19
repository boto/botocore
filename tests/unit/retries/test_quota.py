from tests import unittest


from botocore.retries import quota


class TestRetryQuota(unittest.TestCase):
    def setUp(self):
        self.retry_quota = quota.RetryQuota(50)

    def test_can_acquire_amount(self):
        assert self.retry_quota.acquire(5)
        assert self.retry_quota.available_capacity == 45

    def test_can_release_amount(self):
        assert self.retry_quota.acquire(5)
        assert self.retry_quota.available_capacity == 45
        self.retry_quota.release(5)
        assert self.retry_quota.available_capacity == 50

    def test_cant_exceed_max_capacity(self):
        assert self.retry_quota.acquire(5)
        assert self.retry_quota.available_capacity == 45
        self.retry_quota.release(10)
        assert self.retry_quota.available_capacity == 50

    def test_noop_if_at_max_capacity(self):
        self.retry_quota.release(10)
        assert self.retry_quota.available_capacity == 50

    def test_cant_go_below_zero(self):
        assert self.retry_quota.acquire(49)
        assert self.retry_quota.available_capacity == 1
        assert not self.retry_quota.acquire(10)
        assert self.retry_quota.available_capacity == 1
