import queue
import time
import threading
from multiprocessing import Lock


class ApiRateManager:
    """
    Internal API rate management for botocore library. Allows consumers
    to set a rate that API calls are made by all boto3.resource client types, configurable
    in milliseconds.

    So multi-threaded applications such as ScoutSuite – https://github.com/nccgroup/ScoutSuite – can fix the period
    between API calls in order to avoid rate limiting by AWS. This period can
    be changed dynamically at run time in order for consumers to create utilities
    that respond in real time to being rate limited if appropriate.

    Using an incremental back-off strategy tends to exacerbate the problem of AWS rate limiting
    applications that hit the APIs at a high rate, as it continues to hit the APIs while backing off
    and so continues to cause issues until it reaches a rate that is acceptable.

    By allowing the consumer to set the rate at the application level, rather than the network level,
    it is possible for end users to set a rate that they know will not cause issues on their particular platform.
    """

    def __init__(self, rate_millis):
        """
        :type rate_millis: int
        :param rate_millis: The rate in milliseconds that requests for the APIs are popped from the Queue
        """

        self.process_q = False
        self.queue = queue.Queue(0)
        self.queue_process = None
        self.rate_millis = float(rate_millis)
        self.spent_waiters = []  # type Waiter
        self.step_time = 0  # type: int
        self.steps = []  # type: int
        self.queued = 0  # type: int
        self.mutex = Lock()
        self.debug = False  # type: bool

    class Waiter:
        """
        Manage the queue and notify the consumer when at the head of it.
        """

        def __init__(self):
            self.registered = True
            self.waiting = True
            self.timeout = 0

        @staticmethod
        def now():
            return int(round(time.time() * 1000))

        def waiting(self):
            """
            Consumer must wait while in the q. de_register the waiter
            after consumer discovers wait is over so that it is cleaned away.
            :return: Boolean. True if still waiting
            """
            if self.waiting is False:
                self.registered = False
            return self.waiting

    def debug(self, debug):
        self.debug = debug

    def enqueue(self):
        """
        Create a Waiter() for the caller and return a reference
        Set the timeout based on the Q size. Caller then waits while waiter.waiting
        :return: waiter. Consumer uses this to check if waiting and timeout if required
        """
        waiter = ApiRateManager.Waiter()
        with self.mutex:
            self.queue.put(waiter)
            self.queued += 1
            if self.step_time == 0:
                # waiter.timeout = self.now() + ((self.queued + 100) * self.rate_millis)
                waiter.timeout = self.now() + ((self.queued * 5) * self.rate_millis)
            else:
                # waiter.timeout = self.step_time + ((self.queued + 100) * self.rate_millis)
                waiter.timeout = self.step_time + ((self.queued * 5) * self.rate_millis)

        return waiter

    def next_step(self):
        """
        Return the absolute time of the next step in epoch milliseconds
        :return: long: Time of the next step in epoch millis
        """
        return self.now() + self.rate_millis

    def new_thread(self):
        return threading.Thread(target=self.process_queue)

    @staticmethod
    def now():
        return int(round(time.time() * 1000))

    def process_spent_waiters(self):
        """
        Clean away any spent waiters
        """
        for waiter in self.spent_waiters:
            if waiter.registered is False:
                self.spent_waiters.remove(waiter)

    def process_queue(self):
        """
        Move the waiter at the head of the queue to the spent_waiters list so
        that it persists until the caller checks waiting status and finds False.
        """

        while self.process_q is True:
            self.step_time = self.next_step()
            if self.debug is True:
                self.steps.append(self.step_time)
            if not self.queue.empty():
                with self.mutex:
                    waiter = self.queue.get_nowait()
                    waiter.waiting = False
                    self.spent_waiters.append(waiter)
                    self.queue.task_done()
                    self.queued -= 1
                    self.process_spent_waiters()

            while self.now() <= self.step_time:
                pass

    def reset_rate(self, rate):
        self.stop()
        self.rate_millis = rate
        self.start()

    def start(self):
        """
        Start processing the queue in a background thread
        """
        self.process_q = True
        self.queue_process = self.new_thread()
        self.queue_process.start()

    def stop(self, soft_stop=False):
        """
        Kill the queue processor thread
        :type soft_stop: Boolean
        :param soft_stop: Attempt to wait for the Q to empty before killing the thread
        """
        if soft_stop is True:
            timeout = self.now() + (self.queue.qsize() * 50)
            while self.queue.qsize() > 0 and self.now() < timeout:
                pass

        self.process_q = False
        self.queue_process.join(5)
