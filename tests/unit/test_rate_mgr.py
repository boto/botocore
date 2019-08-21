import statistics
import time
import unittest
from multiprocessing import Lock
from threading import Thread
from time import sleep
from botocore.api_rate_manager import ApiRateManager


class TestRateManager(unittest.TestCase):

    test_metrics = []
    thread_end_times = []
    mutex = Lock()
    brm = None

    def setUp(self):
        self.start = now_millis()
        self.run_times = []
        self.step = 0
        self.thread_end_times = []
        self.brm = None

    def join_queue(self, thread_id):
        waiter = self.brm.enqueue()
        while waiter.waiting is True:
            now = waiter.now()
            if now >= waiter.timeout:
                print('ERROR: ThreadID ' + str(thread_id) + ' timed-out now = ' + str(now) + ' timeout = ' + str(waiter.timeout))
            pass

        with self.mutex:
            self.thread_end_times.append(waiter.now())

    def test_10_waiters_takes_less_than_ten_seconds(self):
        # Half second latency
        self.step = 500
        self.brm = ApiRateManager(self.step)
        self.brm.debug = True
        self.brm.start()
        threads = []

        # Ten threads
        for i in range(10):
            threads.append(Thread(target=self.join_queue, args=[i]))

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        self.brm.stop(True)

        # self.record_test_metrics(self)
        self.assertTrue((now_millis() - self.start) < 10000)

    def test_100_waiters_with_no_contention(self):
        self.step = 100
        self.brm = ApiRateManager(self.step)
        self.brm.debug = True
        self.brm.start()
        threads = []

        for i in range(100):
            threads.append(Thread(target=self.join_queue, args=[i]))

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        self.brm.stop(True)
        # self.record_test_metrics(self)

        self.assertTrue(self.brm.queue.empty())

    def test_reset_of_rate_reduces_run_time(self):
        self.step = 500
        self.brm = ApiRateManager(self.step)
        self.brm.debug = True
        self.brm.start()
        threads = []

        # 50 threads at .5 secs each is 30 secs ish run time
        for i in range(50):
            threads.append(Thread(target=self.join_queue, args=[i]))

        for t in threads:
            t.start()

        sleep(1)

        # Reset rate to 20 from 500 drops runtime from 30ish to 17ish secs
        self.brm.reset_rate(20)

        for t in threads:
            t.join()

        self.brm.stop(True)

        # self.record_test_metrics(self)
        self.assertTrue(self.brm.queue.empty())

    # def test_print_metric(self):
    #     self.print_test_metrics(self)

#     def record_test_metrics(self):
#         total = 0
#         for t in self.thread_end_times:
#             total += t
#
#         avg = float(get_step_average(self.thread_end_times)) / 1000
#         avg_step_str = '{0: <25}'.format('Average thread time') + "= {0:.2f}".format(avg)
#         act_step = '{0: <25}'.format('Set step interval') + "= {0:.2f}".format(float(self.step) / 1000)
#
#         dev = statistics.stdev(get_intervals(self.brm.steps, 1001))
#         std_dev = 'Step Standard Deviation = ' + str("{0:.2f}".format(dev))
#
#         self.test_metrics.append(
#             self.TestMetric(
#                 test_name=self._testMethodName,
#                 std_dev=std_dev,
#                 act_step=act_step,
#                 avg_steps=avg_step_str
#             )
#                                  )
#
#     def print_test_metrics(self):
#         for metrics in self.test_metrics:
#             print('\n' + metrics.test_name)
#             print('\t' + metrics.std_dev)
#             print('\t' + metrics.act_step)
#             print('\t' + metrics.avg_steps)
#
#     class TestMetric:
#         """
#         Record the metrics for a run
#         """
#         def __init__(self, **kwargs):
#             self.test_name = kwargs['test_name']
#             self.std_dev = kwargs['std_dev']
#             self.act_step = kwargs['act_step']
#             self.avg_steps = kwargs['avg_steps']
#
#
# def get_step_average(steps):
#     total = 0
#     intervals = get_intervals(steps, 1)
#     for interval in intervals:
#         total = total + interval
#
#     size = intervals.__len__() or 1
#     return total / size
#
#
# def get_intervals(collection, divisor):
#     high = 0
#     intervals = []
#     for t in reversed(collection):
#         if high == 0:
#             high = t
#             continue
#
#         intervals.append((high - t) / divisor)
#         high = t
#     return intervals


def now_millis():
    return int(round(time.time() * 1000))


if __name__ == '__main__':
    unittest.main()
