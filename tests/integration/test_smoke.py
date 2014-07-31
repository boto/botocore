"""Smoke tests to verify basic communication to all AWS services."""
import botocore.session

from nose.tools import assert_equals


REGION = 'us-east-1'
SMOKE_TESTS = {
 'autoscaling': {'DescribeAccountLimits': {},
                 'DescribeAdjustmentTypes': {}},
 'cloudformation': {'DescribeStacks': {},
                    'ListStacks': {}},
 'cloudfront': {'ListDistributions': {},
                'ListStreamingDistributions': {}},
 'cloudsearch': {'DescribeDomains': {},
                 'ListDomainNames': {}},
 'cloudtrail': {'DescribeTrails': {}},
 'cloudwatch': {'ListMetrics': {}},
 'cognito-identity': {'ListIdentityPools': {'maxResults': 1}},
 'cognito-sync': {'ListIdentityPoolUsage': {}},
 'datapipeline': {'ListPipelines': {}},
 'directconnect': {'DescribeConnections': {}},
 'dynamodb': {'ListTables': {}},
 'ec2': {'DescribeRegions': {},
         'DescribeInstances': {}},
 'elasticache': {'DescribeCacheClusters': {}},
 'elasticbeanstalk': {'DescribeApplications': {}},
 'elastictranscoder': {'ListPipelines': {}},
 'elb': {'DescribeLoadBalancers': {}},
 'emr': {'ListClusters': {}},
 'iam': {'ListUsers': {}},
 # Does not work with session credentials so
 # importexport tests are not run.
 #'importexport': {'ListJobs': {}},
 'importexport': {},
 'kinesis': {'ListStreams': {}},
 'logs': {'DescribeLogGroups': {}},
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
 'storagegateway': {'ListGateways': {}},
 # sts tests would normally go here, but
 # there aren't any calls you can make when
 # using session credentials so we don't run any
 # sts tests.
 'sts': {},
 #'sts': {'GetSessionToken': {}},
 # Subscription needed for support API calls.
 'support': {},
 'swf': {'ListDomains': {'RegistrationStatus': 'REGISTERED'}},
}


def test_can_make_request():
    session = botocore.session.get_session()
    for service_name in SMOKE_TESTS:
        service = session.get_service(service_name)
        endpoint = service.get_endpoint(REGION)
        for operation_name in SMOKE_TESTS[service_name]:
            kwargs = SMOKE_TESTS[service_name][operation_name]
            yield _make_call, service, endpoint, operation_name, kwargs


def _make_call(service, endpoint, operation_name, kwargs):
    operation = service.get_operation(operation_name)
    response, parsed = operation.call(endpoint, **kwargs)
    assert_equals(response.status_code, 200)
