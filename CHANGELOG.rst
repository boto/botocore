=========
CHANGELOG
=========

1.4.5 - (2016-03-17)
--------------------
* feature:``MeteringMarketplace``: The AWS Marketplace Metering Service enables
  sellers to price their products along new pricing dimensions. After a
  integrating their product with the AWS Marketplace Metering Service, that
  product will emit an hourly record capturing the usage of any single pricing
  dimension. Buyers can easily subscribe to software priced by this new
  dimension on the AWS Marketplace website and only pay for what they use.
* feature:``S3``: Added support for delete marker and abort multipart upload
  lifecycle configuration.
* feature:``IOT``: Added support for Amazon Elasticsearch Service and
  Amazon Cloudwatch actions for the AWS IoT rules engine.
* feature:``CloudHSM``: Added support for tagging resources.


1.4.4 - (2016-03-15)
--------------------
* feature:``DMS``: Added support for AWS Database Migration Service
* feature:``SES``: Added support for white-labeling
* feature:``CodeDeploy``: Added support for BatchGetDeploymentGroups
* feature:``endpoints``: Updated endpoints.json to latest version

1.4.3 - (2016-03-10)
--------------------
* feature:``GameLift``: Update model to latest version
* feature:``IAM``: Update model to latest version
* feature:``Redshift``: Update model to latest version

1.4.2 - (2016-03-08)
--------------------
* feature:``ACM``: Update model to latest version
* feature:``CodeCommit``: Update model to latest version
* feature:``Config``: Update model to latest version
* feature:``DeviceFarm``: Update model to latest version
* feature:``DirectConnect``: Update model to latest version
* feature:``Events``: Update model to latest version
* bugfix:``DynamoDB Local``: Fix issue when using the ``local``
  region with ``dynamodb``
  (`issue 819 <https://github.com/boto/botocore/pull/819>`__)
* bugfix:``CloudSearchDomain``: Fix issue when signing requests
  for ``cloudsearchdomain``
  (`boto3 issue 538 <https://github.com/boto/boto3/issues/538>`__)


1.4.1 - (2016-03-03)
--------------------
* feature:Config: Moved Config to its own class to boost import speed
* feature:``EC2``: Add support for VPC peering with security groups.
* feature:``DirectoryService``: Add SNS event notification support

1.4.0 - (2016-03-01)
--------------------
* feature:Regions: Add ability to list regions and endpoints for services in
  a partition.
  (`issue 812 <https://github.com/boto/botocore/pull/812>`__)
* feature:``DynamoDB``: Add support for DescribeLimits.
* feature:``APIGateway``: Add support for TestInvokeAuthorizer and
  FlushStageAuthorizersCache operations.
* feature:``CloudSearchDomain``: Add support for stats.

1.3.28 - (2016-02-18)
---------------------
* feature:``StorageGateway``: Added support for user-supplied barcodes.
* feature:``CodeDeploy``: Added support for setting up triggers for a deployment
  group.
* bugfix:SSL: Fixed issue where AWS_CA_BUNDLE was not being used.

1.3.27 - (2016-02-16)
---------------------
* feature:``RDS``: Added support for Cross-account Encrypted (KMS) snapshot
  sharing.
* feature:``EMR``: Added support for adding EBS storage to EMR instances.
* bugfix:pagination: Refactored pagination to handle non-string service tokens.
* bugfix:credentials: Fix race condition in credential provider.
