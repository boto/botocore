=========
CHANGELOG
=========

1.4.12
======

* bugfix:Credentials: Include timezone information when storing refresh time (`#869 <https://github.com/boto/botocore/issues/869>`__)
* feature:EC2: Add support for two new EBS volume types
* feature:``S3``: Add support for s3 accelerate configuration
* feature:CognitoIdentityProvider: Add support for new service, CognitoIdedentityProvider
* feature:S3: Add support for Amazon S3 Transfer Acceleration
* feature:CodeCommit: Add paginators for CodeCommit (`#881 <https://github.com/boto/botocore/issues/881>`__)
* feature:Kinesis: Update Kinesis client to latest version
* feature:ElasticBeanstalk: Add support for automatic platform version upgrades with managed updates
* feature:DeviceFarm: Update DeviceFarm client to latest version
* feature:FireHose: Update FireHose client to latest version


1.4.11
======

* feature:``IoT``: Add methods for managing CA certificates.
* bugfix:``EC2``: Fix issues with checking an incorrect error code in waiters.
* bugfix:Accept Header: Fix issue in overriding Accept header for API Gateway.


1.4.10
======

* feature:``DS``: Added support for Directory Service Conditional Forwarder APIs.
* feature:``Elasticbeanstalk``: Adds support for three additional elements in AWS Elasticbeanstalk's DescribeInstancesHealthResponse: Deployment, AvailabilityZone, and InstanceType. Additionally adds support for increased EnvironmentName length from 23 to 40.
* bugfix:Paginator: Allow non-specified input tokens in old starting token format.


1.4.9
=====

* feature:``Route53``: Added support for metric-based health checks and regional health checks.
* feature:``STS``: Added support for GetCallerIdentity, which returns details about the credentials used to make the API call. The details include name and account, as well as the type of entity making the call, such as an IAM user vs. federated user.
* feature:``S3``: Added support for VersionId in PutObjectAcl (`issue 856 <https://github.com/boto/botocore/pull/856>`__)
* bugfix:``S3``: Add validation to enforce S3 metadata only contains ASCII. (`issue 861 <https://github.com/boto/botocore/pull/861>`__)
* bugfix:Exceptions: Consistently parse errors with no body (`issue 859 <https://github.com/boto/botocore/pull/859>`__)
* bugfix:Config: Handle case where S3 config key is not a dict (`issue 858 <https://github.com/boto/botocore/pull/858>`__)
* bugfix:Examples: Account for empty input shape in examples (`issue 855 <https://github.com/boto/botocore/pull/855>`__)


1.4.8
=====

* feature:``CloudFormation``: Update client to latest version
* feature:``CodeDeploy``: Update client to latest version
* feature:``DMS``: Update client to latest version
* feature:``ElastiCache``: Update client to latest version
* feature:``Elastic Beanstalk``: Update client to latest version
* feature:``Redshift``: Update client to latest version
* feature:``WAF``: Update client to latest version
* bugfix:Pagintor: Fix regression when providing a starting token for a paginator (`issue 849 <https://github.com/boto/botocore/pull/849>`__)
* bugfix:Response Parsing: Handle case when generic HTML error response is received (`issue 850 <https://github.com/boto/botocore/pull/850>`__)
* bugfix:Request serialization: Handle case when non str values are provided for header values when using signature version 4 (`issue 852 <https://github.com/boto/botocore/pull/852>`__)
* bugfix:Retry: Retry HTTP responses with status code 502 (`issue 853 <https://github.com/boto/botocore/pull/853>`__)


1.4.7
=====

* feature:``RDS``: Update client to latest version
* feature:``StorageGateway``: Update client to latest version
* bugfix:Proxy: Handle case where error response from proxy is received (`issue 850 <https://github.com/boto/botocore/pull/850`__)


1.4.6
=====

* feature:``RDS``: Add support for customizing the order in which Aurora Replicas are promoted to primary instance during a failover
* bugfix:Signature Version 4: Fix issue when calculating signature version 4 signature for certain urls (`issue 827 <https://github.com/boto/botocore/pull/827>`__)


1.4.5
=====

* feature:``S3``: Added support for delete marker and abort multipart upload lifecycle configuration.
* feature:``IOT``: Added support for Amazon Elasticsearch Service and Amazon Cloudwatch actions for the AWS IoT rules engine.
* feature:``CloudHSM``: Added support for tagging resources.


1.4.4
=====

* feature:``SES``: Added support for white-labeling
* feature:``CodeDeploy``: Added support for BatchGetDeploymentGroups
* feature:``endpoints``: Updated endpoints.json to latest version


1.4.3
=====

* feature:``IAM``: Update model to latest version
* feature:``Redshift``: Update model to latest version


1.4.2
=====

* feature:``CodeCommit``: Update model to latest version
* feature:``Config``: Update model to latest version
* feature:``DeviceFarm``: Update model to latest version
* feature:``DirectConnect``: Update model to latest version
* feature:``Events``: Update model to latest version
* bugfix:``DynamoDB Local``: Fix issue when using the ``local`` region with ``dynamodb`` (`issue 819 <https://github.com/boto/botocore/pull/819>`__)
* bugfix:``CloudSearchDomain``: Fix issue when signing requests for ``cloudsearchdomain`` (`boto3 issue 538 <https://github.com/boto/boto3/issues/538>`__)


1.4.1
=====

* feature:``EC2``: Add support for VPC peering with security groups.
* feature:``DirectoryService``: Add SNS event notification support


1.4.0
=====

* feature:``DynamoDB``: Add support for DescribeLimits.
* feature:``APIGateway``: Add support for TestInvokeAuthorizer and FlushStageAuthorizersCache operations.
* feature:``CloudSearchDomain``: Add support for stats.


1.3.28
======

* feature:``CodeDeploy``: Added support for setting up triggers for a deployment group.
* bugfix:SSL: Fixed issue where AWS_CA_BUNDLE was not being used.


1.3.27
======

* feature:``EMR``: Added support for adding EBS storage to EMR instances.
* bugfix:pagination: Refactored pagination to handle non-string service tokens.
* bugfix:credentials: Fix race condition in credential provider.

