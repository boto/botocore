# Copyright 2015 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
from tests import unittest, mock, IntegerRefresher
import datetime
import threading
import math
import time

from dateutil.tz import tzlocal

from botocore import credentials
from botocore import utils


class TestCredentialRefreshRaces(unittest.TestCase):
    def assert_consistent_credentials_seen(self, creds, func):
        collected = []
        threads = []
        for _ in range(20):
            threads.append(threading.Thread(target=func, args=(collected,)))
        start = time.time()
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        for triple in collected:
            self.assertTrue(triple[0] == triple[1] == triple[2], triple)

    def test_has_no_race_conditions(self):
        creds = IntegerRefresher(
            creds_last_for=2,
            advisory_refresh=1,
            mandatory_refresh=0
        )
        def _run_in_thread(collected):
            for _ in range(4000):
                frozen = creds.get_frozen_credentials()
                collected.append((frozen.access_key,
                                  frozen.secret_key,
                                  frozen.token))
        start = time.time()
        self.assert_consistent_credentials_seen(creds, _run_in_thread)
        end = time.time()
        # creds_last_for = 2 seconds (from above)
        # So, for example, if execution time took 6.1 seconds, then
        # we should see a maximum number of refreshes being (6 / 2.0) + 1 = 4
        max_calls_allowed = math.ceil((end - start) / 2.0) + 1
        self.assertTrue(creds.refresh_counter <= max_calls_allowed,
                        "Too many cred refreshes, max: %s, actual: %s, "
                        "time_delta: %.4f" % (max_calls_allowed,
                                              creds.refresh_counter,
                                              (end - start)))

    def test_no_race_for_immediate_expiration(self):
        creds = IntegerRefresher(
            creds_last_for=1,
            advisory_refresh=1,
            mandatory_refresh=0
        )
        def _run_in_thread(collected):
            for _ in range(100):
                frozen = creds.get_frozen_credentials()
                collected.append((frozen.access_key,
                                  frozen.secret_key,
                                  frozen.token))
        self.assert_consistent_credentials_seen(creds, _run_in_thread)
