import boto3
import statistics
import time
import unittest
import warnings
from botocore.exceptions import ClientError, BotoCoreError
from multiprocessing import Lock
from threading import Thread


class MyTestCase(unittest.TestCase):

    test_metrics = []
    thread_end_times = []
    mutex = Lock()
    RATE = 250

    def setUp(self):
        warnings.filterwarnings(action="ignore", message="unclosed", category=ResourceWarning)
        self.session = boto3.Session(profile_name='ds-nonprod')
        self.credentials = self.session.get_credentials().__dict__

        # Uncomment for MFA token prompt, e.g. Credentials not in environment vars
        # This was tested in Pycharm with a run config containing the AWS credentials as ENV vars
        # sts_client = session.client('sts')
        # sts_client.get_caller_identity()

        # Create an EC2 client with a latency value for api rate of 250ms
        self.client = connect_service('ec2', self.credentials, self.session.region_name, None, False, self.RATE)
        self.client.api_rate_mgr.debug = True

    def make_api_call(self, client, thread_id):
        try:
            result = client.describe_instances()
        except (BotoCoreError, ClientError) as err:
            print(f'ERROR: Thread {thread_id} caused an exception. msg({err})')
        finally:
            with self.mutex:
                self.thread_end_times.append(client.api_rate_mgr.now())

    def test_10_threads_join_queue(self):

        threads = []

        # Ten threads
        for i in range(10):
            threads.append(Thread(target=self.make_api_call, args=[self.client, i]))

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        self.client.api_rate_mgr.stop(True)

        self.record_test_metrics()

    def test_print_metric(self):
        self.print_test_metrics()

    def record_test_metrics(self):
        total = 0
        for t in self.thread_end_times:
            total += t

        avg = get_step_average(self.thread_end_times) / 1000
        avg_step_str = '{0: <25}'.format('Average thread time') + "= {:.2f}".format(avg)
        act_step = '{0: <25}'.format('Set step interval') + "= {:.2f}".format(self.RATE / 1000)

        dev = "{:.2f}".format(statistics.stdev(get_intervals(self.client.api_rate_mgr.steps, 1000)))
        std_dev = '{0: <25}'.format('Step Standard Deviation') + f'= {dev}'

        num_steps = '{0: <25}'.format('Number of steps in queue') + f'= {len(self.client.api_rate_mgr.steps)}'

        self.test_metrics.append(
            self.TestMetric(
                test_name=self._testMethodName,
                std_dev=std_dev,
                act_step=act_step,
                avg_steps=avg_step_str,
                num_steps=num_steps
            )
        )

    def print_test_metrics(self):
        for metrics in self.test_metrics:
            print('\n' + metrics.test_name)
            print('\t' + metrics.std_dev)
            print('\t' + metrics.act_step)
            print('\t' + metrics.avg_steps)
            print('\t' + metrics.num_steps)

    class TestMetric:
        """
        Record the metrics for a run
        """
        def __init__(self, **kwargs):
            self.test_name = kwargs['test_name']
            self.std_dev = kwargs['std_dev']
            self.act_step = kwargs['act_step']
            self.avg_steps = kwargs['avg_steps']
            self.num_steps = kwargs['num_steps']


def get_step_average(steps):
    total = 0
    intervals = get_intervals(steps, 1)
    for interval in intervals:
        total = total + interval

    return total / intervals.__len__()


def get_intervals(collection, divisor):
    high = 0
    intervals = []
    for t in reversed(collection):
        if high == 0:
            high = t
            continue

        intervals.append((high - t) / divisor)
        high = t
    return intervals


def now_millis():
    return int(round(time.time() * 1000))


def connect_service(service, credentials, region_name=None, config=None, silent=False, api_rate=0):
    """
    Instantiates an AWS API client

    :param api_rate:                    The period between API calls in ms
    :param service:                     Service targeted, e.g. ec2
    :param credentials:                 Id, secret, token
    :param region_name:                 Region desired, e.g. us-east-2
    :param config:                      Configuration (optional)
    :param silent:                      Whether or not to print messages

    :return: api_client:                The AWS client
    """
    api_client = None
    try:
        client_params = {'service_name': service.lower(), 'api_rate': api_rate}
        session_params = {'aws_access_key_id': credentials.get('access_key'),
                          'aws_secret_access_key': credentials.get('secret_key'),
                          'aws_session_token': credentials.get('token')}
        if region_name:
            client_params['region_name'] = region_name
            session_params['region_name'] = region_name
        if config:
            client_params['config'] = config

        aws_session = boto3.session.Session(**session_params)
        if not silent:
            info_message = 'Connecting to AWS %s' % service
            if region_name:
                info_message = info_message + ' in %s' % region_name
            print('%s...' % info_message)
        api_client = aws_session.client(**client_params)
    except Exception as e:
        print(e)
    return api_client


if __name__ == '__main__':
    unittest.main()
