"""Smoke tests to verify basic communication to all AWS services.

If you want to control what services/regions are used you can
also provide two separate env vars:

    * AWS_SMOKE_TEST_REGION - The region used to create clients.
    * AWS_SMOKE_TEST_SERVICES - A CSV list of service names to test.

Otherwise, the ``REGION`` variable specifies the default region
to use and all the services in SMOKE_TESTS/ERROR_TESTS will be tested.

"""
import os
import mock
from pprint import pformat
import warnings
from nose.tools import assert_equals, assert_true

from botocore import xform_name
import botocore.session
from botocore.client import ClientError
from botocore.vendored.requests import adapters
from botocore.vendored.requests.exceptions import ConnectionError


# Mapping of service -> api calls to try.
# Each api call is a dict of OperationName->params.
# Empty params means that the operation will be called with no params.  This is
# used as a quick verification that we can successfully make calls to services.
SMOKE_TESTS = {
 'acm': {'ListCertificates': {}},
 'apigateway': {'GetRestApis': {}},
 'autoscaling': {'DescribeAccountLimits': {},
                 'DescribeAdjustmentTypes': {}},
 'cloudformation': {'DescribeStacks': {},
                    'ListStacks': {}},
 'cloudfront': {'ListDistributions': {},
                'ListStreamingDistributions': {}},
 'cloudhsm': {'ListAvailableZones': {}},
 'cloudsearch': {'DescribeDomains': {},
                 'ListDomainNames': {}},
 'cloudtrail': {'DescribeTrails': {}},
 'cloudwatch': {'ListMetrics': {}},
 'codecommit': {'ListRepositories': {}},
 'codedeploy': {'ListApplications': {}},
 'codepipeline': {'ListActionTypes': {}},
 'codedeploy': {'ListApplications': {}},
 'codecommit': {'ListRepositories': {}},
 'cognito-identity': {'ListIdentityPools': {'MaxResults': 1}},
 'cognito-sync': {'ListIdentityPoolUsage': {}},
 'config': {'DescribeDeliveryChannels': {}},
 'datapipeline': {'ListPipelines': {}},
 'devicefarm': {'ListProjects': {}},
 'directconnect': {'DescribeConnections': {}},
 'ds': {'DescribeDirectories': {}},
 'dynamodb': {'ListTables': {}},
 'dynamodbstreams': {'ListStreams': {}},
 'ec2': {'DescribeRegions': {},
         'DescribeInstances': {}},
  'ecr': {'DescribeRepositories': {}},
 'ecs': {'DescribeClusters': {}},
 'elasticache': {'DescribeCacheClusters': {}},
 'elasticbeanstalk': {'DescribeApplications': {}},
 'elastictranscoder': {'ListPipelines': {}},
 'elb': {'DescribeLoadBalancers': {}},
 'emr': {'ListClusters': {}},
 'es': {'ListDomainNames': {}},
 'events': {'ListRules': {}},
  'firehose': {'ListDeliveryStreams': {}},
 'gamelift': {'ListBuilds': {}},
 'glacier': {'ListVaults': {}},
 'iam': {'ListUsers': {}},
 # Does not work with session credentials so
 # importexport tests are not run.
 #'importexport': {'ListJobs': {}},
 'importexport': {},
 'inspector': {'DescribeCrossAccountAccessRole': {}},
 'iot': {'DescribeEndpoint': {}},
 'kinesis': {'ListStreams': {}},
 'kms': {'ListKeys': {}},
 'lambda': {'ListFunctions': {}},
 'logs': {'DescribeLogGroups': {}},
 'machinelearning': {'DescribeMLModels': {}},
 'opsworks': {'DescribeStacks': {}},
 'rds': {'DescribeDBInstances': {}},
 'redshift': {'DescribeClusters': {}},
 'route53': {'ListHostedZones': {}},
 'route53domains': {'ListDomains': {}},
 's3': {'ListBuckets': {}},
 'sdb': {'ListDomains': {}},
 'ses': {'ListIdentities': {}},
 'sns': {'ListTopics': {}},
 'sqs': {'ListQueues': {}},
 'ssm': {'ListDocuments': {}},
 'storagegateway': {'ListGateways': {}},
 # sts tests would normally go here, but
 # there aren't any calls you can make when
 # using session credentials so we don't run any
 # sts tests.
 'sts': {},
 #'sts': {'GetSessionToken': {}},
 # Subscription needed for support API calls.
 'support': {},
 'swf': {'ListDomains': {'registrationStatus': 'REGISTERED'}},
 'waf': {'ListWebACLs': {'Limit': 1}},
 'workspaces': {'DescribeWorkspaces': {}},
}

# Same thing as the SMOKE_TESTS hash above, except these verify
# that we get an error response back from the server because
# we've sent invalid params.
ERROR_TESTS = {
    'apigateway': {'GetRestApi': {'restApiId': 'fake-id'}},
    'autoscaling': {'CreateLaunchConfiguration': {
        'LaunchConfigurationName': 'foo',
        'ImageId': 'ami-12345678',
        'InstanceType': 'm1.small',
        }},
    'cloudformation': {'CreateStack': {
        'StackName': 'fake',
        'TemplateURL': 'http://s3.amazonaws.com/foo/bar',
        }},
    'cloudfront': {'GetDistribution': {'Id': 'fake-id'}},
    'cloudhsm': {'DescribeHapg': {'HapgArn': 'bogus-arn'}},
    'cloudsearch': {'DescribeIndexFields': {'DomainName': 'fakedomain'}},
    'cloudtrail': {'DeleteTrail': {'Name': 'fake-trail'}},
    'cloudwatch': {'SetAlarmState': {
        'AlarmName': 'abc',
        'StateValue': 'mno',
        'StateReason': 'xyz',
        }},
    'logs': {'GetLogEvents': {'logGroupName': 'a', 'logStreamName': 'b'}},
    'codecommit': {'ListBranches': {'repositoryName': 'fake-repo'}},
    'codedeploy': {'GetDeployment': {'deploymentId': 'fake-id'}},
    'codepipeline': {'GetPipeline': {'name': 'fake-pipeline'}},
    'cognito-identity': {'DescribeIdentityPool': {'IdentityPoolId': 'fake'}},
    'cognito-sync': {'DescribeIdentityPoolUsage': {'IdentityPoolId': 'fake'}},
    'config': {
        'GetResourceConfigHistory': {'resourceType': '', 'resourceId': ''},
        },
    'datapipeline': {'GetPipelineDefinition': {'pipelineId': 'fake'}},
    'devicefarm': {'GetDevice': {'arn': 'arn:aws:devicefarm:REGION::device:f'}},
    'directconnect': {'DescribeConnections': {'connectionId': 'fake'}},
    'ds': {'CreateDirectory': {'Name': 'n', 'Password': 'p', 'Size': '1'}},
    'dynamodb': {'DescribeTable': {'TableName': 'fake'}},
    'dynamodbstreams': {'DescribeStream': {'StreamArn': 'x'*37}},
    'ec2': {'DescribeInstances': {'InstanceIds': ['i-12345678']}},
    'ecs': {'StopTask': {'task': 'fake'}},
    'efs': {'DeleteFileSystem': {'FileSystemId': 'fake'}},
    'elasticache': {'DescribeCacheClusters': {'CacheClusterId': 'fake'}},
    'elasticbeanstalk': {
        'DescribeEnvironmentResources': {'EnvironmentId': 'x'},
        },
    'elb': {'DescribeLoadBalancers': {'LoadBalancerNames': ['fake']}},
    'elastictranscoder': {'ReadJob': {'Id': 'fake'}},
    'emr': {'DescribeCluster': {'ClusterId': 'fake'}},
    'es': {'DescribeElasticsearchDomain': {'DomainName': 'not-a-domain'}},
    'gamelift': {'DescribeBuild': {'BuildId': 'fake-build-id'}},
    'glacier': {'ListVaults': {'accountId': 'fake'}},
    'iam': {'GetUser': {'UserName': 'fake'}},
    'importexport': {'CreateJob': {
        'JobType': 'Import',
        'ValidateOnly': False,
        'Manifest': 'fake',
        }},
    'kinesis': {'DescribeStream': {'StreamName': 'fake'}},
    'kms': {'GetKeyPolicy': {'KeyId': 'fake', 'PolicyName': 'fake'}},
    'lambda': {'Invoke': {'FunctionName': 'fake'}},
    'machinelearning': {'GetBatchPrediction': {'BatchPredictionId': 'fake'}},
    'opsworks': {'DescribeLayers': {'StackId': 'fake'}},
    'rds': {'DescribeDBInstances': {'DBInstanceIdentifier': 'fake'}},
    'redshift': {'DescribeClusters': {'ClusterIdentifier': 'fake'}},
    'route53': {'GetHostedZone': {'Id': 'fake'}},
    'route53domains': {'GetDomainDetail': {'DomainName': 'fake'}},
    's3': {'ListObjects': {'Bucket': 'thisbucketdoesnotexistasdf'}},
    'ses': {'VerifyEmailIdentity': {'EmailAddress': 'fake'}},
    'sdb': {'CreateDomain': {'DomainName': ''}},
    'sns': {
        'ConfirmSubscription': {'TopicArn': 'a', 'Token': 'b'},
        'Publish': {'Message': 'hello', 'TopicArn': 'fake'},
        },
    'sqs': {'GetQueueUrl': {'QueueName': 'fake'}},
    'ssm': {'GetDocument': {'Name': 'fake'}},
    'storagegateway': {'ListVolumes': {'GatewayARN': 'x'*50}},
    'sts': {'GetFederationToken': {'Name': 'fake', 'Policy': 'fake'}},
    'support': {'CreateCase': {
        'subject': 'x',
        'communicationBody': 'x',
        'categoryCode': 'x',
        'serviceCode': 'x',
        'severityCode': 'low',
        }},
    'swf': {'DescribeDomain': {'name': 'fake'}},
    'waf': {'GetWebACL': {'WebACLId': 'fake'}},
    'workspaces': {'DescribeWorkspaces': {'DirectoryId': 'fake'}},
}

REGION = 'us-east-1'
REGION_OVERRIDES = {
    'devicefarm': 'us-west-2',
    'efs': 'us-west-2',
    'inspector': 'us-west-2',
}


def _get_client(session, service):
    if os.environ.get('AWS_SMOKE_TEST_REGION', ''):
        region_name = os.environ['AWS_SMOKE_TEST_REGION']
    else:
        region_name = REGION_OVERRIDES.get(service, REGION)
    return session.create_client(service, region_name=region_name)


def _list_services(dict_entries):
    # List all services in the provided dict_entry.
    # If the AWS_SMOKE_TEST_SERVICES is provided,
    # it's a comma separated list of services you can provide
    # if you only want to run the smoke tests for certain services.
    if 'AWS_SMOKE_TEST_SERVICES' not in os.environ:
        return dict_entries.keys()
    else:
        wanted_services = os.environ.get(
            'AWS_SMOKE_TEST_SERVICES', '').split(',')
        return [key for key in dict_entries if key in wanted_services]


def test_can_make_request_with_client():
    # Same as test_can_make_request, but with Client objects
    # instead of service/operations.
    session = botocore.session.get_session()
    for service_name in _list_services(SMOKE_TESTS):
        client = _get_client(session, service_name)
        for operation_name in SMOKE_TESTS[service_name]:
            kwargs = SMOKE_TESTS[service_name][operation_name]
            method_name = xform_name(operation_name)
            yield _make_client_call, client, method_name, kwargs


def _make_client_call(client, operation_name, kwargs):
    method = getattr(client, operation_name)
    with warnings.catch_warnings(record=True) as caught_warnings:
        response = method(**kwargs)
        assert_equals(len(caught_warnings), 0,
                      "Warnings were emitted during smoke test: %s"
                      % caught_warnings)
        assert_true('Errors' not in response)


def test_can_make_request_and_understand_errors_with_client():
    session = botocore.session.get_session()
    for service_name in _list_services(ERROR_TESTS):
        client = _get_client(session, service_name)
        for operation_name in ERROR_TESTS[service_name]:
            kwargs = ERROR_TESTS[service_name][operation_name]
            method_name = xform_name(operation_name)
            yield _make_error_client_call, client, method_name, kwargs


def _make_error_client_call(client, operation_name, kwargs):
    method = getattr(client, operation_name)
    try:
        response = method(**kwargs)
    except ClientError as e:
        pass
    else:
        raise AssertionError("Expected client error was not raised "
                             "for %s.%s" % (client, operation_name))


def test_client_can_retry_request_properly():
    session = botocore.session.get_session()
    for service_name in _list_services(SMOKE_TESTS):
        client = _get_client(session, service_name)
        for operation_name in SMOKE_TESTS[service_name]:
            kwargs = SMOKE_TESTS[service_name][operation_name]
            yield (_make_client_call_with_errors, client,
                   operation_name, kwargs)


def _make_client_call_with_errors(client, operation_name, kwargs):
    operation = getattr(client, xform_name(operation_name))
    original_send = adapters.HTTPAdapter.send
    def mock_http_adapter_send(self, *args, **kwargs):
        if not getattr(self, '_integ_test_error_raised', False):
            self._integ_test_error_raised = True
            raise ConnectionError("Simulated ConnectionError raised.")
        else:
            return original_send(self, *args, **kwargs)
    with mock.patch('botocore.vendored.requests.adapters.HTTPAdapter.send',
                    mock_http_adapter_send):
        try:
            response = operation(**kwargs)
        except ClientError as e:
            assert False, ('Request was not retried properly, '
                           'received error:\n%s' % pformat(e))
