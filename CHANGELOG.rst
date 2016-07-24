=========
CHANGELOG
=========

1.4.39
======

* feature:``acm``: Update acm client to latest version
* feature:``elastictranscoder``: Update elastictranscoder client to latest version
* feature:``cloudformation``: Update cloudformation client to latest version
* feature:``config``: Update config client to latest version
* feature:``application-autoscaling``: Update application-autoscaling client to latest version


1.4.38
======

* feature:``ssm``: Update ssm client to latest version
* feature:``devicefarm``: Update devicefarm client to latest version


1.4.37
======

* feature:``dms``: Update dms client to latest version
* feature:``ecs``: Update ecs client to latest version
* Feature:Credential Provider: Add support for ECS metadata credential provider.
* feature:``rds``: Update rds client to latest version


1.4.36
======

* feature:``servicecatalog``: Update servicecatalog client to latest version
* feature:``opsworks``: Update opsworks client to latest version
* feature:``ds``: Update ds client to latest version
* feature:``config``: Update config client to latest version


1.4.35
======

* feature:``iam``: Update iam client to latest version
* feature:``codepipeline``: Update codepipeline client to latest version
* feature:``efs``: Update efs client to latest version


1.4.34
======

* feature:``dms``: Update dms client to latest version
* feature:``ssm``: Update ssm client to latest version


1.4.33
======

* feature:``sns``: Update sns client to latest version
* feature:``route53``: Update route53 client to latest version
* feature:``ec2``: Update ec2 client to latest version
* feature:``gamelift``: Update gamelift client to latest version
* feature:``efs``: Update efs client to latest version
* feature:``iot``: Update iot client to latest version


1.4.32
======

* bugfix:S3: Fixed a bug where the S3 region redirector was potentially causing a memory leak on python 2.6.
* feature:``s3``: Update s3 client to latest version


1.4.31
======

* bugfix:RequestSigner: `RequestSigner.generate_presigned_url` now requires the operation name to be passed in. This does not affect using `generate_presigned_url` through a client.
* feature:``rds``: Update rds client to latest version
* feature:``directconnect``: Update directconnect client to latest version
* feature:RequestSigner: Allow `botocore.UNSIGNED` to be used with `generate_presigned_url` and `generate_presigned_post`.
* feature:``ec2``: Update ec2 client to latest version
* feature:``cognito-identity``: Update cognito-identity client to latest version
* feature:``iam``: Update iam client to latest version


1.4.30
======

* bugfix:AssumeRole: Fix regression introduced in `#920 <https://github.com/boto/botocore/issues/920>`__ where assume role responses error out when attempting to cache a response. (`#961 <https://github.com/boto/botocore/issues/961>`__)


1.4.29
======

* feature:ResponseMetadata: Add http response headers to the response metadata.
* feature:``codepipeline``: Update codepipeline client to latest version
* feature:s3: Automatically redirect S3 sigv4 requests sent to the wrong region.
* feature:``opsworks``: Update opsworks client to latest version
* feature:s3: Use MD5 to sign S3 bodies by default.
* bugfix:EC2: Replace chars in the EC2 console output we can't decode with replacement chars.  We were previously returning either the decoded content or the original base64 encoded content.  We now will consistently return decoded output, any any chars we can't decode are substituted with a replacement char. (`#953 <https://github.com/boto/botocore/issues/953>`__)


1.4.28
======

* feature:``cloudtrail``: Update cloudtrail client to latest version
* feature:``acm``: Update acm client to latest version
* bugfix:Stubber: Fix regression in comparing multiple expected parameters
* feature:``rds``: Update rds client to latest version
* feature:``ses``: Update ses client to latest version


1.4.27
======

* feature:Stubber: Allow certain paramters to be ignored by specifying stub.ANY. Resolves `#931 <https://github.com/boto/botocore/issues/931>`__
* feature:``s3``: Update s3 client to latest version


1.4.26
======

* feature:Config: Add ``parameter_validation`` option in config file to disable parameter validation when making API calls (`#905 <https://github.com/boto/botocore/issues/905>`__)
* feature:``dynamodbstreams``: Update dynamodbstreams client to latest version
* bugfix:s3: Make the stubber work with get_bucket_location
* feature:``iot``: Update iot client to latest version
* feature:``machinelearning``: Update machinelearning client to latest version


1.4.25
======

* feature:Stubber: Allow adding additional keys to the service error response.
* feature:``ec2``: Update ec2 client to latest version
* feature:``application-autoscaling``: Update application-autoscaling client to latest version


1.4.24
======

* feature:``elasticache``: Update elasticache client to latest version


1.4.23
======

* feature:``rds``: Update rds client to latest version
* feature:``ec2``: Update ec2 client to latest version


1.4.22
======

* feature:``firehose``: Update firehose client to latest version
* feature:``ec2``: Update ec2 client to latest version
* feature:``ecs``: Update ecs client to latest version


1.4.21
======

* feature:``application-autoscaling``: Adds support for Application Auto Scaling. Application Auto Scaling is a general purpose Auto Scaling service for supported elastic AWS resources. With Application Auto Scaling, you can automatically scale your AWS resources, with an experience similar to that of Auto Scaling.
* feature:endpoints: Updated endpoints.json to latest.


1.4.20
======

* feature:``dynamodb``: Update dynamodb client to latest version
* bugfix:Waiters: Fix ``JMESPathTypeError`` exception being raised (`#906 <https://github.com/boto/botocore/issues/906>`__, `#907 <https://github.com/boto/botocore/issues/907>`__)
* feature:``workspaces``: Update workspaces client to latest version
* feature:s3: Add paginator for ListObjectsV2
* feature:``discovery``: Update discovery client to latest version
* feature:iam: Add missing paginators. Fixes `#919 <https://github.com/boto/botocore/issues/919>`__.


1.4.19
======

* feature:``ec2``: Update ec2 client to latest version
* feature:``ssm``: Update ssm client to latest version
* feature:``discovery``: Update discovery client to latest version
* feature:``cloudformation``: Update cloudformation client to latest version


1.4.18
======

* feature:``storagegateway``: Update storagegateway client to latest version
* feature:``directconnect``: Update directconnect client to latest version
* feature:``emr``: Update emr client to latest version
* feature:``sqs``: Update sqs client to latest version
* feature:``iam``: Update iam client to latest version


1.4.17
======

* feature:``kms``: Update kms client to latest version
* feature:``sts``: Update sts client to latest version
* feature:``apigateway``: Update apigateway client to latest version
* feature:``ecs``: Update ecs client to latest version
* feature:``s3``: Update s3 client to latest version
* feature:``cloudtrail``: Update cloudtrail client to latest version


1.4.16
======

* feature:``inspector``: Update inspector client to latest version
* feature:``codepipeline``: Update codepipeline client to latest version
* feature:``opsworks``: Add InstanceRegistered waiter
* feature:``elasticbeanstalk``: Update elasticbeanstalk client to latest version


1.4.15
======

* feature:``route53domains``: Update route53domains client to latest version
* feature:``opsworks``: Update opsworks client to latest version


1.4.14
======

* feature:``ecr``: Update ecr client to latest version
* bugfix:``aws kinesis``: Fix issue where "EnhancedMonitoring" was not displayed when running ``aws kinesis describe-stream`` (`#1929 <https://github.com/aws/aws-cli/issues/1929>`__)
* feature:``acm``: Update acm client to latest version
* feature:``ec2``: Update ec2 client to latest version
* feature:``sts``: Update sts client to latest version
* bugfix:Serializer: In the rest xml parser, we were converting the input we recieve into a `str`, which was causing failures on python 2 when multibyte unicode strings were passed in. The fix is to simply use `six.text_type`, which is `unicode` on 2 and `str` on 3. The string will be encoded into the default encoding later on in the serializer. Fixes `#868 <https://github.com/boto/botocore/issues/868>`__
* feature:``cognito-idp``: Update cognito-idp client to latest version


1.4.13
======

* feature:EMR: Add support for smart targeted resize feature
* feature:IOT: Add SQL RulesEngine version support
* feature:ACM: Add tagging support for ACM


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

