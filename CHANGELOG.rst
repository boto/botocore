=========
CHANGELOG
=========

1.21.27
=======

* api-change:``dms``: Amazon AWS DMS service now support Redis target endpoint migration. Now S3 endpoint setting is capable to setup features which are used to be configurable only in extract connection attributes.
* api-change:``frauddetector``: Updated an element of the DescribeModelVersion API response (LogitMetrics -> logOddsMetrics) for clarity. Added new exceptions to several APIs to protect against unlikely scenarios.
* api-change:``iotsitewise``: Documentation updates for AWS IoT SiteWise
* api-change:``dlm``: Added AMI deprecation support for Amazon Data Lifecycle Manager EBS-backed AMI policies.
* api-change:``glue``: Add support for Custom Blueprints
* api-change:``apigateway``: Adding some of the pending releases (1) Adding WAF Filter to GatewayResponseType enum (2) Ensuring consistent error model for all operations (3) Add missing BRE to GetVpcLink operation
* api-change:``backup``: AWS Backup - Features: Evaluate your backup activity and generate audit reports.


1.21.26
=======

* api-change:``eks``: Adds support for EKS add-ons "preserve" flag, which allows customers to maintain software on their EKS clusters after removing it from EKS add-ons management.
* api-change:``comprehend``: Add tagging support for Comprehend async inference job.
* api-change:``robomaker``: Documentation updates for RoboMaker
* api-change:``ec2``: encryptionInTransitSupported added to DescribeInstanceTypes API


1.21.25
=======

* api-change:``ec2``: The ImportImage API now supports the ability to create AMIs with AWS-managed licenses for Microsoft SQL Server for both Windows and Linux.
* api-change:``memorydb``: AWS MemoryDB  SDK now supports all APIs for newly launched MemoryDB service.
* api-change:``application-autoscaling``: This release extends Application Auto Scaling support for replication group of Amazon ElastiCache Redis clusters. Auto Scaling monitors and automatically expands node group count and number of replicas per node group when a critical usage threshold is met or according to customer-defined schedule.
* api-change:``appflow``: This release adds support for SAPOData connector and extends Veeva connector for document extraction.


1.21.24
=======

* api-change:``codebuild``: CodeBuild now allows you to make the build results for your build projects available to the public without requiring access to an AWS account.
* api-change:``route53``: Documentation updates for route53
* api-change:``sagemaker-runtime``: Update sagemaker-runtime client to latest version
* api-change:``route53resolver``: Documentation updates for Route 53 Resolver
* api-change:``sagemaker``: Amazon SageMaker now supports Asynchronous Inference endpoints. Adds PlatformIdentifier field that allows Notebook Instance creation with different platform selections. Increases the maximum number of containers in multi-container endpoints to 15. Adds more instance types to InstanceType field.


1.21.23
=======

* api-change:``cloud9``: Added DryRun parameter to CreateEnvironmentEC2 API. Added ManagedCredentialsActions parameter to UpdateEnvironment API
* api-change:``ec2``: This release adds support for EC2 ED25519 key pairs for authentication
* api-change:``clouddirectory``: Documentation updates for clouddirectory
* api-change:``ce``: This release is a new feature for Cost Categories: Split charge rules. Split charge rules enable you to allocate shared costs between your cost category values.
* api-change:``logs``: Documentation-only update for CloudWatch Logs


1.21.22
=======

* api-change:``iotsitewise``: AWS IoT SiteWise added query window for the interpolation interval. AWS IoT SiteWise computes each interpolated value by using data points from the timestamp of each interval minus the window to the timestamp of each interval plus the window.
* api-change:``s3``: Documentation updates for Amazon S3
* api-change:``codebuild``: CodeBuild now allows you to select how batch build statuses are sent to the source provider for a project.
* api-change:``ds``: This release adds support for describing client authentication settings.
* api-change:``config``: Update ResourceType enum with values for Backup Plan, Selection, Vault, RecoveryPoint; ECS Cluster, Service, TaskDefinition; EFS AccessPoint, FileSystem; EKS Cluster; ECR Repository resources
* api-change:``license-manager``: AWS License Manager now allows end users to call CheckoutLicense API using new CheckoutType PERPETUAL. Perpetual checkouts allow sellers to check out a quantity of entitlements to be drawn down for consumption.


1.21.21
=======

* api-change:``quicksight``: Documentation updates for QuickSight.
* api-change:``emr``: Update emr client to latest version
* api-change:``customer-profiles``: This release introduces Standard Profile Objects, namely Asset and Case which contain values populated by data from third party systems and belong to a specific profile. This release adds an optional parameter, ObjectFilter to the ListProfileObjects API in order to search for these Standard Objects.
* api-change:``elasticache``: This release adds ReplicationGroupCreateTime field to ReplicationGroup which indicates the UTC time when ElastiCache ReplicationGroup is created


1.21.20
=======

* api-change:``sagemaker``: Amazon SageMaker Autopilot adds new metrics for all candidate models generated by Autopilot experiments.
* api-change:``apigatewayv2``: Adding support for ACM imported or private CA certificates for mTLS enabled domain names
* api-change:``apigateway``: Adding support for ACM imported or private CA certificates for mTLS enabled domain names
* api-change:``databrew``: This SDK release adds support for the output of a recipe job results to Tableau Hyper format.
* api-change:``lambda``: Lambda Python 3.9 runtime launch


1.21.19
=======

* api-change:``snow-device-management``: AWS Snow Family customers can remotely monitor and operate their connected AWS Snowcone devices.
* api-change:``ecs``: Documentation updates for ECS.
* api-change:``nimble``: Add new attribute 'ownedBy' in Streaming Session APIs. 'ownedBy' represents the AWS SSO Identity Store User ID of the owner of the Streaming Session resource.
* api-change:``codebuild``: CodeBuild now allows you to make the build results for your build projects available to the public without requiring access to an AWS account.
* api-change:``ebs``: Documentation updates for Amazon EBS direct APIs.
* api-change:``route53``: Documentation updates for route53


1.21.18
=======

* api-change:``chime``: Add support for "auto" in Region field of StartMeetingTranscription API request.
* enchancement:Client: Improve client performance by caching _alias_event_name on EventAliaser


1.21.17
=======

* api-change:``wafv2``: This release adds APIs to support versioning feature of AWS WAF Managed rule groups
* api-change:``rekognition``: This release adds support for four new types of segments (opening credits, content segments, slates, and studio logos), improved accuracy for credits and shot detection and new filters to control black frame detection.
* api-change:``ssm``: Documentation updates for AWS Systems Manager.


1.21.16
=======

* api-change:``synthetics``: Documentation updates for Visual Monitoring feature and other doc ticket fixes.
* api-change:``chime-sdk-identity``: The Amazon Chime SDK Identity APIs allow software developers to create and manage unique instances of their messaging applications.
* api-change:``chime-sdk-messaging``: The Amazon Chime SDK Messaging APIs allow software developers to send and receive messages in custom messaging applications.
* api-change:``connect``: This release adds support for agent status and hours of operation. For details, see the Release Notes in the Amazon Connect Administrator Guide.
* api-change:``lightsail``: This release adds support to track when a bucket access key was last used.
* api-change:``athena``: Documentation updates for Athena.


1.21.15
=======

* api-change:``lexv2-models``: Update lexv2-models client to latest version
* api-change:``autoscaling``: EC2 Auto Scaling adds configuration checks and Launch Template validation to Instance Refresh.


1.21.14
=======

* api-change:``rds``: This release adds AutomaticRestartTime to the DescribeDBInstances and DescribeDBClusters operations. AutomaticRestartTime indicates the time when a stopped DB instance or DB cluster is restarted automatically.
* api-change:``imagebuilder``: Updated list actions to include a list of valid filters that can be used in the request.
* api-change:``transcribe``: This release adds support for call analytics (batch) within Amazon Transcribe.
* api-change:``events``: Update events client to latest version
* api-change:``ssm-incidents``: Documentation updates for Incident Manager.


1.21.13
=======

* api-change:``redshift``: API support for Redshift Data Sharing feature.
* api-change:``iotsitewise``: My AWS Service (placeholder) - This release introduces custom Intervals and offset for tumbling window in metric for AWS IoT SiteWise.
* api-change:``glue``: Add ConcurrentModificationException to create-table, delete-table, create-database, update-database, delete-database
* api-change:``mediaconvert``: AWS Elemental MediaConvert SDK has added control over the passthrough of XDS captions metadata to outputs.
* api-change:``proton``: Docs only add idempotent create apis


1.21.12
=======

* api-change:``ssm-contacts``: Added new attribute in AcceptCode API. AcceptCodeValidation takes in two values - ENFORCE, IGNORE. ENFORCE forces validation of accept code and IGNORE ignores it which is also the default behavior; Corrected TagKeyList length from 200 to 50
* api-change:``greengrassv2``: This release adds support for component system resource limits and idempotent Create operations. You can now specify the maximum amount of CPU and memory resources that each component can use.


1.21.11
=======

* api-change:``appsync``: AWS AppSync now supports a new authorization mode allowing you to define your own authorization logic using an AWS Lambda function.
* api-change:``elbv2``: Update elbv2 client to latest version
* api-change:``secretsmanager``: Add support for KmsKeyIds in the ListSecretVersionIds API response
* api-change:``sagemaker``: API changes with respect to Lambda steps in model building pipelines. Adds several waiters to async Sagemaker Image APIs. Add more instance types to AppInstanceType field


1.21.10
=======

* api-change:``savingsplans``: Documentation update for valid Savings Plans offering ID pattern
* api-change:``ec2``: This release adds support for G4ad xlarge and 2xlarge instances powered by AMD Radeon Pro V520 GPUs and AMD 2nd Generation EPYC processors
* api-change:``chime``: Adds support for live transcription of meetings with Amazon Transcribe and Amazon Transcribe Medical.  The new APIs, StartMeetingTranscription and StopMeetingTranscription, control the generation of user-attributed transcriptions sent to meeting clients via Amazon Chime SDK data messages.
* api-change:``iotsitewise``: Added support for AWS IoT SiteWise Edge. You can now create an AWS IoT SiteWise gateway that runs on AWS IoT Greengrass V2. With the gateway,  you can collect local server and equipment data, process the data, and export the selected data from the edge to the AWS Cloud.
* api-change:``iot``: Increase maximum credential duration of role alias to 12 hours.


1.21.9
======

* api-change:``sso-admin``: Documentation updates for arn:aws:trebuchet:::service:v1:03a2216d-1cda-4696-9ece-1387cb6f6952
* api-change:``cloudformation``: SDK update to support Importing existing Stacks to new/existing Self Managed StackSet - Stack Import feature.


1.21.8
======

* api-change:``route53``: This release adds support for the RECOVERY_CONTROL health check type to be used in conjunction with Route53 Application Recovery Controller.
* api-change:``iotwireless``: Add SidewalkManufacturingSn as an identifier to allow Customer to query WirelessDevice, in the response, AmazonId is added in the case that Sidewalk device is return.
* api-change:``route53-recovery-control-config``: Amazon Route 53 Application Recovery Controller's routing control - Routing Control Configuration APIs help you create and delete clusters, control panels, routing controls and safety rules. State changes (On/Off) of routing controls are not part of configuration APIs.
* api-change:``route53-recovery-readiness``: Amazon Route 53 Application Recovery Controller's readiness check capability continually monitors resource quotas, capacity, and network routing policies to ensure that the recovery environment is scaled and configured to take over when needed.
* api-change:``quicksight``: Add support to use row-level security with tags when embedding dashboards for users not provisioned in QuickSight
* api-change:``iotanalytics``: IoT Analytics now supports creating a dataset resource with IoT SiteWise MultiLayerStorage data stores, enabling customers to query industrial data within the service. This release includes adding JOIN functionality for customers to query multiple data sources in a dataset.
* api-change:``shield``: Change name of DDoS Response Team (DRT) to Shield Response Team (SRT)
* api-change:``lexv2-models``: Update lexv2-models client to latest version
* api-change:``redshift-data``: Added structures to support new Data API operation BatchExecuteStatement, used to execute multiple SQL statements within a single transaction.
* api-change:``route53-recovery-cluster``: Amazon Route 53 Application Recovery Controller's routing control - Routing Control Data Plane APIs help you update the state (On/Off) of the routing controls to reroute traffic across application replicas in a 100% available manner.
* api-change:``batch``: Add support for ListJob filters


1.21.7
======

* api-change:``s3control``: S3 Access Point aliases can be used anywhere you use S3 bucket names to access data in S3
* api-change:``textract``: Adds support for AnalyzeExpense, a new API to extract relevant data such as contact information, items purchased, and vendor name, from almost any invoice or receipt without the need for any templates or configuration.
* api-change:``proton``: Documentation-only update links
* api-change:``identitystore``: Documentation updates for SSO API Ref.
* api-change:``cloudwatch``: Update cloudwatch client to latest version
* api-change:``synthetics``: CloudWatch Synthetics now supports visual testing in its canaries.


1.21.6
======

* api-change:``securityhub``: Added product name, company name, and Region fields for security findings. Added details objects for RDS event subscriptions and AWS ECS services. Added fields to the details for AWS Elasticsearch domains.
* api-change:``imagebuilder``: Update to documentation to reapply missing change to SSM uninstall switch default value and improve description.
* api-change:``s3outposts``: Add on-premise access type support for endpoints


1.21.5
======

* api-change:``medialive``: MediaLive now supports passing through style data on WebVTT caption outputs.
* api-change:``databrew``: This SDK release adds two new features: 1) Output to Native JDBC destinations and 2) Adding configurations to profile jobs
* api-change:``elbv2``: Update elbv2 client to latest version
* api-change:``s3control``: Documentation updates for Amazon S3-control
* api-change:``ec2``: This release allows customers to assign prefixes to their elastic network interface and to reserve IP blocks in their subnet CIDRs. These reserved blocks can be used to assign prefixes to elastic network interfaces or be excluded from auto-assignment.
* api-change:``qldb``: Amazon QLDB now supports ledgers encrypted with customer managed KMS keys. Changes in CreateLedger, UpdateLedger and DescribeLedger APIs to support the changes.


1.21.4
======

* api-change:``kendra``: Amazon Kendra now provides a data source connector for Amazon WorkDocs. For more information, see https://docs.aws.amazon.com/kendra/latest/dg/data-source-workdocs.html
* api-change:``proton``: Documentation updates for AWS Proton
* api-change:``iam``: Documentation updates for AWS Identity and Access Management (IAM).
* api-change:``rds``: Adds the OriginalSnapshotCreateTime field to the DBSnapshot response object. This field timestamps the underlying data of a snapshot and doesn't change when the snapshot is copied.
* api-change:``elbv2``: Update elbv2 client to latest version
* api-change:``lambda``: New ResourceConflictException error code for PutFunctionEventInvokeConfig, UpdateFunctionEventInvokeConfig, and DeleteFunctionEventInvokeConfig operations.
* api-change:``codebuild``: AWS CodeBuild now allows you to set the access permissions for build artifacts, project artifacts, and log files that are uploaded to an Amazon S3 bucket that is owned by another account.
* api-change:``personalize``: My AWS Service (placeholder) - Making minProvisionedTPS an optional parameter when creating a campaign. If not provided, it defaults to 1.
* api-change:``emr``: Update emr client to latest version


1.21.3
======

* api-change:``compute-optimizer``: Documentation updates for Compute Optimizer
* api-change:``ec2``: Added idempotency to the CreateVolume API using the ClientToken request parameter


1.21.2
======

* api-change:``imagebuilder``: Documentation updates for reversal of default value for additional instance configuration SSM switch, plus improved descriptions for semantic versioning.
* api-change:``directconnect``: Documentation updates for directconnect
* api-change:``health``: In the Health API, the maximum number of entities for the EventFilter and EntityFilter data types has changed from 100 to 99. This change is related to an internal optimization of the AWS Health service.
* api-change:``robomaker``: This release allows customers to create a new version of WorldTemplates with support for Doors.
* api-change:``location``: Add five new API operations: UpdateGeofenceCollection, UpdateMap, UpdatePlaceIndex, UpdateRouteCalculator, UpdateTracker.
* api-change:``emr-containers``: Updated DescribeManagedEndpoint and ListManagedEndpoints to return failureReason and stateDetails in API response.


1.21.1
======

* api-change:``appintegrations``: Documentation update for AppIntegrations Service
* api-change:``chime``: This SDK release adds Account Status as one of the attributes in Account API response
* api-change:``auditmanager``: This release relaxes the S3 URL character restrictions in AWS Audit Manager. Regex patterns have been updated for the following attributes: s3RelativePath, destination, and s3ResourcePath. 'AWS' terms have also been replaced with entities to align with China Rebrand documentation efforts.


1.21.0
======

* api-change:``ec2``: This feature enables customers  to specify weekly recurring time window(s) for scheduled events that reboot, stop or terminate EC2 instances.
* api-change:``cognito-idp``: Documentation updates for cognito-idp
* api-change:``ecs``: Documentation updates for support of awsvpc mode on Windows.
* api-change:``lex-models``: Lex now supports the en-IN locale
* api-change:``iotsitewise``: Update the default endpoint for the APIs used to manage asset models, assets, gateways, tags, and account configurations. If you have firewalls with strict egress rules, configure the rules to grant you access to api.iotsitewise.[region].amazonaws.com or api.iotsitewise.[cn-region].amazonaws.com.cn.
* feature:Python: Dropped support for Python 2.7


1.20.112
========

* api-change:``dms``: Release of feature needed for ECA-Endpoint settings. This allows customer to delete a field in endpoint settings by using --exact-settings flag in modify-endpoint api. This also displays default values for certain required fields of endpoint settings in describe-endpoint-settings api.
* api-change:``glue``: Add support for Event Driven Workflows
* api-change:``acm``: Added support for RSA 3072 SSL certificate import
* api-change:``healthlake``: General availability for Amazon HealthLake. StartFHIRImportJob and StartFHIRExportJob APIs now require AWS KMS parameter. For more information, see the Amazon HealthLake Documentation https://docs.aws.amazon.com/healthlake/index.html.
* api-change:``wellarchitected``: This update provides support for Well-Architected API users to mark answer choices as not applicable.
* api-change:``lightsail``: This release adds support for the Amazon Lightsail object storage service, which allows you to create buckets and store objects.


1.20.111
========

* api-change:``amplifybackend``: Added Sign in with Apple OAuth provider.
* api-change:``redshift``: Release new APIs to support new Redshift feature - Authentication Profile
* api-change:``ssm``: Changes to OpsCenter APIs to support a new feature, operational insights.
* api-change:``lex-models``: Customers can now migrate bots built with Lex V1 APIs to V2 APIs. This release adds APIs to initiate and manage the migration of a bot.
* api-change:``directconnect``: This release adds a new filed named awsLogicalDeviceId that it displays the AWS Direct Connect endpoint which terminates a physical connection's BGP Sessions.
* api-change:``pricing``: Documentation updates for api.pricing


1.20.110
========

* api-change:``eks``: Documentation updates for Wesley to support the parallel node upgrade feature.
* api-change:``kendra``: Amazon Kendra now supports Principal Store


1.20.109
========

* api-change:``sagemaker``: Releasing new APIs related to Tuning steps in model building pipelines.
* api-change:``frauddetector``: This release adds support for ML Explainability to display model variable importance value in Amazon Fraud Detector.
* api-change:``mediaconvert``: MediaConvert now supports color, style and position information passthrough from 608 and Teletext to SRT and WebVTT subtitles. MediaConvert now also supports Automatic QVBR quality levels for QVBR RateControlMode.


1.20.108
========

* api-change:``eks``: Added waiters for EKS FargateProfiles.
* api-change:``outposts``: Added property filters for listOutposts
* api-change:``fms``: AWS Firewall Manager now supports route table monitoring, and provides remediation action recommendations to security administrators for AWS Network Firewall policies with misconfigured routes.
* api-change:``mediatailor``: Add ListAlerts for Channel, Program, Source Location, and VOD Source to return alerts for resources.
* api-change:``devops-guru``: Add AnomalyReportedTimeRange field to include open and close time of anomalies.
* api-change:``ssm-contacts``: Updated description for CreateContactChannel contactId.


1.20.107
========

* api-change:``iam``: Documentation updates for AWS Identity and Access Management (IAM).
* api-change:``sts``: Documentation updates for AWS Security Token Service.
* api-change:``mq``: adds support for modifying the maintenance window for brokers.
* api-change:``cloudfront``: Amazon CloudFront now provides two new APIs, ListConflictingAliases and AssociateAlias, that help locate and move Alternate Domain Names (CNAMEs) if you encounter the CNAMEAlreadyExists error code.
* api-change:``chime``: Releasing new APIs for AWS Chime MediaCapturePipeline
* api-change:``iotsitewise``: This release add storage configuration APIs for AWS IoT SiteWise.
* api-change:``storagegateway``: Adding support for oplocks for SMB file shares,  S3 Access Point and S3 Private Link for all file shares and IP address support for file system associations
* api-change:``ec2``: This release adds resource ids and tagging support for VPC security group rules.


1.20.106
========

* api-change:``lambda``: Added support for AmazonMQRabbitMQ as an event source. Added support for VIRTUAL_HOST as SourceAccessType for streams event source mappings.
* api-change:``imagebuilder``: Adds support for specifying parameters to customize components for recipes. Expands configuration of the Amazon EC2 instances that are used for building and testing images, including the ability to specify commands to run on launch, and more control over installation and removal of the SSM agent.
* api-change:``mgn``: Bug fix: Remove not supported EBS encryption type "NONE"
* api-change:``eks``: Adding new error code UnsupportedAddonModification for Addons in EKS
* api-change:``macie2``: Sensitive data findings in Amazon Macie now include enhanced location data for JSON and JSON Lines files
* api-change:``sns``: Documentation updates for Amazon SNS.


1.20.105
========

* api-change:``elbv2``: Update elbv2 client to latest version
* api-change:``ec2``: This release removes network-insights-boundary


1.20.104
========

* api-change:``sagemaker``: SageMaker model registry now supports up to 5 containers and associated environment variables.
* api-change:``sqs``: Documentation updates for Amazon SQS.
* api-change:``ec2``: Adding a new reserved field to support future infrastructure improvements for Amazon EC2 Fleet.


1.20.103
========

* api-change:``autoscaling``: Amazon EC2 Auto Scaling infrastructure improvements and optimizations.
* api-change:``kendra``: Amazon Kendra Enterprise Edition now offered in smaller more granular units to enable customers with smaller workloads. Virtual Storage Capacity units now offer scaling in increments of 100,000 documents (up to 30GB) per unit and Virtual Query Units offer scaling increments of 8,000 queries per day.
* api-change:``mediapackage-vod``: Add support for Widevine DRM on CMAF packaging configurations. Both Widevine and FairPlay DRMs can now be used simultaneously, with CBCS encryption.
* api-change:``ssm-contacts``: Fixes the tag key length range to 128 chars,  tag value length to 256 chars; Adds support for UTF-8 chars for contact and channel names, Allows users to unset name in UpdateContact API; Adds throttling exception to StopEngagement API, validation exception to APIs UntagResource, ListTagsForResource
* api-change:``databrew``: Adds support for the output of job results to the AWS Glue Data Catalog.
* api-change:``servicediscovery``: AWS Cloud Map now allows configuring the TTL of the SOA record for a hosted zone to control the negative caching for new services.


1.20.102
========

* api-change:``sagemaker``: Sagemaker Neo now supports running compilation jobs using customer's Amazon VPC
* api-change:``glue``: Add JSON Support for Glue Schema Registry
* api-change:``redshift``: Added InvalidClusterStateFault to the DisableLogging API, thrown when calling the API on a non available cluster.
* api-change:``mediaconvert``: MediaConvert adds support for HDR10+, ProRes 4444,  and XAVC outputs, ADM/DAMF support for Dolby Atmos ingest, and alternative audio and WebVTT caption ingest via HLS inputs. MediaConvert also now supports creating trickplay outputs for Roku devices for HLS, CMAF, and DASH output groups.


1.20.101
========

* api-change:``proton``: Added waiters for template registration, service operations, and environment deployments.
* api-change:``amplifybackend``: Imports an existing backend authentication resource.
* api-change:``snowball``: AWS Snow Family customers can remotely monitor and operate their connected AWS Snowcone devices. AWS Snowball Edge Storage Optimized customers can now import and export their data using NFS.


1.20.100
========

* api-change:``chime``: Adds EventIngestionUrl field to MediaPlacement
* api-change:``cloud9``: Minor update to AWS Cloud9 documentation to allow correct parsing of outputted text
* api-change:``connect``: Released Amazon Connect quick connects management API for general availability (GA). For more information, see https://docs.aws.amazon.com/connect/latest/APIReference/Welcome.html
* api-change:``dax``: Add support for encryption in transit to DAX clusters.
* api-change:``wafv2``: Added support for 15 new text transformation.
* api-change:``kendra``: Amazon Kendra now supports SharePoint 2013 and SharePoint 2016 when using a SharePoint data source.
* api-change:``securityhub``: Added new resource details for ECS clusters and ECS task definitions. Added additional information for S3 buckets, Elasticsearch domains, and API Gateway V2 stages.
* api-change:``transfer``: Customers can successfully use legacy clients with Transfer Family endpoints enabled for FTPS and FTP behind routers, firewalls, and load balancers by providing a Custom IP address used for data channel communication.
* api-change:``codebuild``: BucketOwnerAccess is currently not supported


1.20.99
=======

* api-change:``docdb``: DocumentDB documentation-only edits
* api-change:``cloud9``: Updated documentation for CreateEnvironmentEC2 to explain that because Amazon Linux AMI has ended standard support as of December 31, 2020, we recommend you choose Amazon Linux 2--which includes long term support through 2023--for new AWS Cloud9 environments.
* api-change:``quicksight``: Releasing new APIs for AWS QuickSight Folders
* api-change:``mediatailor``: Update GetChannelSchedule to return information on ad breaks.
* api-change:``cloudfront``: Amazon CloudFront adds support for a new security policy, TLSv1.2_2021.
* api-change:``license-manager``: AWS License Manager now allows license administrators and end users to communicate to each other by setting custom status reasons when updating the status on a granted license.
* api-change:``ec2``: This release adds support for provisioning your own IP (BYOIP) range in multiple regions. This feature is in limited Preview for this release. Contact your account manager if you are interested in this feature.
* api-change:``events``: Added the following parameters to ECS targets: CapacityProviderStrategy, EnableECSManagedTags, EnableExecuteCommand, PlacementConstraints, PlacementStrategy, PropagateTags, ReferenceId, and Tags
* api-change:``cloudsearch``: This release replaces previous generation CloudSearch instances with equivalent new instances that provide better stability at the same price.
* api-change:``codeguru-reviewer``: Adds support for S3 based full repository analysis and changed lines scan.


1.20.98
=======

* api-change:``cloudformation``: CloudFormation registry service now supports 3rd party public type sharing


1.20.97
=======

* api-change:``kendra``: Amazon Kendra now supports the indexing of web documents for search through the web crawler.
* api-change:``sagemaker``: Enable ml.g4dn instance types for SageMaker Batch Transform and SageMaker Processing
* api-change:``rds``: This release enables Database Activity Streams for RDS Oracle
* api-change:``chime``: This release adds a new API UpdateSipMediaApplicationCall, to update an in-progress call for SipMediaApplication.


1.20.96
=======

* api-change:``kms``: Adds support for multi-Region keys
* api-change:``ec2``: This release adds support for VLAN-tagged network traffic over an Elastic Network Interface (ENI). This feature is in limited Preview for this release. Contact your account manager if you are interested in this feature.
* api-change:``rds``: This release enables fast cloning in Aurora Serverless. You can now clone between Aurora Serverless clusters and Aurora Provisioned clusters.
* api-change:``mediatailor``: Adds AWS Secrets Manager Access Token Authentication for Source Locations


1.20.95
=======

* api-change:``redshift-data``: Redshift Data API service now supports SQL parameterization.
* api-change:``connect``: This release adds new sets of APIs: AssociateBot, DisassociateBot, and ListBots. You can use it to programmatically add an Amazon Lex bot or Amazon Lex V2 bot on the specified Amazon Connect instance
* api-change:``ec2``: EC2 M5n, M5dn, R5n, R5dn metal instances with 100 Gbps network performance and Elastic Fabric Adapter (EFA) for ultra low latency
* api-change:``lexv2-runtime``: Update lexv2-runtime client to latest version
* api-change:``lexv2-models``: Update lexv2-models client to latest version


1.20.94
=======

* api-change:``lookoutmetrics``: Added "LEARNING" status for anomaly detector and updated description for "Offset" parameter in MetricSet APIs.
* api-change:``iotanalytics``: Adds support for data store partitions.
* api-change:``greengrassv2``: We have verified the APIs being released here and are ready to release


1.20.93
=======

* api-change:``ec2``: Amazon EC2 adds new AMI property to flag outdated AMIs
* api-change:``medialive``: AWS MediaLive now supports OCR-based conversion of DVB-Sub and SCTE-27 image-based source captions to WebVTT, and supports ingest of ad avail decorations in HLS input manifests.
* api-change:``mediaconnect``: When you enable source failover, you can now designate one of two sources as the primary source. You can choose between two failover modes to prevent any disruption to the video stream. Merge combines the sources into a single stream. Failover allows switching between a primary and a backup stream.


1.20.92
=======

* api-change:``sagemaker``: Using SageMaker Edge Manager with AWS IoT Greengrass v2 simplifies accessing, maintaining, and deploying models to your devices. You can now create deployable IoT Greengrass components during edge packaging jobs. You can choose to create a device fleet with or without creating an AWS IoT role alias.
* api-change:``appmesh``: AppMesh now supports additional routing capabilities in match and rewrites for Gateway Routes and Routes. Additionally, App Mesh also supports specifying DNS Response Types in Virtual Nodes.
* api-change:``redshift``: Added InvalidClusterStateFault to the ModifyAquaConfiguration API, thrown when calling the API on a non available cluster.
* api-change:``chime``: This SDK release adds support for UpdateAccount API to allow users to update their default license on Chime account.
* api-change:``ec2``: This release adds a new optional parameter connectivityType (public, private) for the CreateNatGateway API. Private NatGateway does not require customers to attach an InternetGateway to the VPC and can be used for communication with other VPCs and on-premise networks.
* api-change:``ram``: AWS Resource Access Manager (RAM) is releasing new field isResourceTypeDefault in ListPermissions and GetPermission response, and adding permissionArn parameter to GetResourceShare request to filter by permission attached
* api-change:``sagemaker-featurestore-runtime``: Release BatchGetRecord API for AWS SageMaker Feature Store Runtime.
* api-change:``cognito-idp``: Amazon Cognito now supports targeted sign out through refresh token revocation
* api-change:``appflow``: Adding MAP_ALL task type support.
* api-change:``managedblockchain``: This release supports KMS customer-managed Customer Master Keys (CMKs) on member-specific Hyperledger Fabric resources.


1.20.91
=======

* api-change:``transfer``: Documentation updates for the AWS Transfer Family service.
* api-change:``personalize-events``: Support for unstructured text inputs in the items dataset to to automatically extract key information from product/content description as an input when creating solution versions.
* api-change:``proton``: This is the initial SDK release for AWS Proton
* api-change:``kendra``: AWS Kendra now supports checking document status.


1.20.90
=======

* api-change:``fsx``: This release adds support for auditing end-user access to files, folders, and file shares using Windows event logs, enabling customers to meet their security and compliance needs.
* api-change:``servicecatalog``: increase max pagesize for List/Search apis
* api-change:``macie2``: This release of the Amazon Macie API introduces stricter validation of S3 object criteria for classification jobs.
* api-change:``cognito-idp``: Documentation updates for cognito-idp


1.20.89
=======

* api-change:``sagemaker``: AWS SageMaker - Releasing new APIs related to Callback steps in model building pipelines. Adds experiment integration to model building pipelines.
* api-change:``glue``: Add SampleSize variable to S3Target to enable s3-sampling feature through API.
* api-change:``personalize``: Update regex validation in kmsKeyArn and s3 path API parameters for AWS Personalize APIs
* api-change:``eks``: Added updateConfig option that allows customers to control upgrade velocity in Managed Node Group.


1.20.88
=======

* api-change:``rds``: Documentation updates for RDS: fixing an outdated link to the RDS documentation in DBInstance$DBInstanceStatus
* api-change:``pi``: The new GetDimensionKeyDetails action retrieves the attributes of the specified dimension group for a DB instance or data source.
* api-change:``cloudtrail``: AWS CloudTrail supports data events on new service resources, including Amazon DynamoDB tables and S3 Object Lambda access points.
* api-change:``medialive``: Add support for automatically setting the H.264 adaptive quantization and GOP B-frame fields.
* api-change:``autoscaling``: Documentation updates for Amazon EC2 Auto Scaling
* api-change:``qldb``: Documentation updates for Amazon QLDB


1.20.87
=======

* api-change:``s3``: S3 Inventory now supports Bucket Key Status
* api-change:``s3control``: Amazon S3 Batch Operations now supports S3 Bucket Keys.
* api-change:``route53resolver``: Documentation updates for Route 53 Resolver
* api-change:``ssm``: Documentation updates for ssm to fix customer reported issue
* api-change:``forecast``: Added optional field AutoMLOverrideStrategy to CreatePredictor API that allows users to customize AutoML strategy. If provided in CreatePredictor request, this field is visible in DescribePredictor and GetAccuracyMetrics responses.


1.20.86
=======

* api-change:``autoscaling``: You can now launch EC2 instances with GP3 volumes when using Auto Scaling groups with Launch Configurations
* api-change:``lightsail``: Documentation updates for Lightsail
* api-change:``ecs``: Documentation updates for Amazon ECS.
* api-change:``docdb``: This SDK release adds support for DocDB global clusters.
* api-change:``iam``: Documentation updates for AWS Identity and Access Management (IAM).
* api-change:``braket``: Introduction of a RETIRED status for devices.


1.20.85
=======

* api-change:``sns``: This release adds SMS sandbox in Amazon SNS and the ability to view all configured origination numbers. The SMS sandbox provides a safe environment for sending SMS messages, without risking your reputation as an SMS sender.
* api-change:``polly``: Amazon Polly adds new Canadian French voice - Gabrielle. Gabrielle is available as Neural voice only.
* api-change:``ec2``: Added idempotency to CreateNetworkInterface using the ClientToken parameter.
* api-change:``iotwireless``: Added six new public customer logging APIs to allow customers to set/get/reset log levels at resource type and resource id level. The log level set from the APIs will be used to filter log messages that can be emitted to CloudWatch in customer accounts.
* api-change:``servicediscovery``: Bugfixes - The DiscoverInstances API operation now provides an option to return all instances for health-checked services when there are no healthy instances available.


1.20.84
=======

* api-change:``lookoutmetrics``: Allowing dot(.) character in table name for RDS and Redshift as source connector.
* api-change:``location``: Adds support for calculation of routes, resource tagging and customer provided KMS keys.
* api-change:``datasync``: Added SecurityDescriptorCopyFlags option that allows for control of which components of SMB security descriptors are copied from source to destination objects.


1.20.83
=======

* api-change:``iotevents-data``: Releasing new APIs for AWS IoT Events Alarms
* api-change:``devicefarm``: Introduces support for using our desktop testing service with applications hosted within your Virtual Private Cloud (VPC).
* api-change:``kendra``: Amazon Kendra now suggests popular queries in order to help guide query typing and help overall accuracy.
* api-change:``iotsitewise``: IoT SiteWise Monitor Portal API updates to add alarms feature configuration.
* api-change:``resource-groups``: Documentation updates for Resource Groups.
* api-change:``lightsail``: Documentation updates for Lightsail
* api-change:``iotevents``: Releasing new APIs for AWS IoT Events Alarms
* api-change:``fsx``: This release adds LZ4 data compression support to FSx for Lustre to reduce storage consumption of both file system storage and file system backups.
* api-change:``sqs``: Documentation updates for Amazon SQS for General Availability of high throughput for FIFO queues.


1.20.82
=======

* api-change:``ec2``: This release removes resource ids and tagging support for VPC security group rules.


1.20.81
=======

* api-change:``qldb``: Support STANDARD permissions mode in CreateLedger and DescribeLedger. Add UpdateLedgerPermissionsMode to update permissions mode on existing ledgers.
* api-change:``cloudfront``: Documentation fix for CloudFront
* api-change:``outposts``: Add ConflictException to DeleteOutpost, CreateOutpost
* api-change:``mwaa``: Adds scheduler count selection for Environments using Airflow version 2.0.2 or later.
* api-change:``ec2``: This release adds resource ids and tagging support for VPC security group rules.
* api-change:``ecs``: The release adds support for registering External instances to your Amazon ECS clusters.
* api-change:``acm-pca``: This release enables customers to store CRLs in S3 buckets with Block Public Access enabled. The release adds the S3ObjectAcl parameter to the CreateCertificateAuthority and UpdateCertificateAuthority APIs to allow customers to choose whether their CRL will be publicly available.


1.20.80
=======

* api-change:``transfer``: AWS Transfer Family customers can now use AWS Managed Active Directory or AD Connector to authenticate their end users, enabling seamless migration of file transfer workflows that rely on AD authentication, without changing end users' credentials or needing a custom authorizer.
* api-change:``iot``: This release includes support for a new feature: Job templates for AWS IoT Device Management Jobs. The release includes job templates as a new resource and APIs for managing job templates.
* api-change:``workspaces``: Adds support for Linux device types in WorkspaceAccessProperties


1.20.79
=======

* api-change:``quicksight``: Add new parameters on RegisterUser and UpdateUser APIs to assign or update external ID associated to QuickSight users federated through web identity.
* api-change:``ce``: Introduced FindingReasonCodes, PlatformDifferences, DiskResourceUtilization and NetworkResourceUtilization to GetRightsizingRecommendation action
* api-change:``compute-optimizer``: Adds support for 1) additional instance types, 2) additional instance metrics, 3) finding reasons for instance recommendations, and 4) platform differences between a current instance and a recommended instance type.
* api-change:``ec2``: This release adds support for creating and managing EC2 On-Demand Capacity Reservations on Outposts.
* api-change:``logs``: This release provides dimensions and unit support for metric filters.


1.20.78
=======

* api-change:``efs``: Update efs client to latest version
* api-change:``s3``: Documentation updates for Amazon S3
* api-change:``forecast``: Updated attribute statistics in DescribeDatasetImportJob response to support Long values
* api-change:``opsworkscm``: New PUPPET_API_CRL attribute returned by DescribeServers API; new EngineVersion of 2019 available for Puppet Enterprise servers.


1.20.77
=======

* api-change:``personalize``: Added new API to stop a solution version creation that is pending or in progress for Amazon Personalize
* api-change:``lexv2-models``: Update lexv2-models client to latest version
* api-change:``quicksight``: Add ARN based Row Level Security support to CreateDataSet/UpdateDataSet APIs.
* api-change:``iam``: Documentation updates for AWS Identity and Access Management (IAM).


1.20.76
=======

* api-change:``kinesisanalyticsv2``: Kinesis Data Analytics now allows rapid iteration on Apache Flink stream processing through the Kinesis Data Analytics Studio feature.
* api-change:``rekognition``: Amazon Rekognition Custom Labels adds support for customer managed encryption, using AWS Key Management Service, of image files copied into the service and files written back to the customer.
* api-change:``iam``: Add pagination to ListUserTags operation
* api-change:``eks``: Update the EKS AddonActive waiter.
* api-change:``autoscaling``: With this release, customers can easily use Predictive Scaling as a policy directly through Amazon EC2 Auto Scaling configurations to proactively scale their applications ahead of predicted demand.
* api-change:``lightsail``: Documentation updates for Amazon Lightsail.


1.20.75
=======

* api-change:``support``: Documentation updates for support
* api-change:``apprunner``: AWS App Runner is a service that provides a fast, simple, and cost-effective way to deploy from source code or a container image directly to a scalable and secure web application in the AWS Cloud.
* api-change:``compute-optimizer``: This release enables compute optimizer to support exporting  recommendations to Amazon S3 for EBS volumes and Lambda Functions.
* api-change:``personalize``: Amazon Personalize now supports the ability to optimize a solution for a custom objective in addition to maximizing relevance.
* api-change:``license-manager``: AWS License Manager now supports periodic report generation.
* api-change:``iotsitewise``: Documentation updates for AWS IoT SiteWise.
* api-change:``lexv2-models``: Update lexv2-models client to latest version


1.20.74
=======

* api-change:``mediaconnect``: MediaConnect now supports JPEG XS for AWS Cloud Digital Interface (AWS CDI) uncompressed workflows, allowing you to establish a bridge between your on-premises live video network and the AWS Cloud.
* api-change:``sagemaker-a2i-runtime``: Documentation updates for Amazon A2I Runtime model
* api-change:``applicationcostprofiler``: APIs for AWS Application Cost Profiler.
* api-change:``neptune``: Neptune support for CopyTagsToSnapshots
* api-change:``iotdeviceadvisor``: AWS IoT Core Device Advisor is fully managed test capability for IoT devices. Device manufacturers can use Device Advisor to test their IoT devices for reliable and secure connectivity with AWS IoT.
* api-change:``elasticache``: Documentation updates for elasticache


1.20.73
=======

* api-change:``events``: Update InputTransformer variable limit from 10 to 100 variables.
* enhancement:``s3``: Block endpoint resolution of clients configured with S3 pseudo-regions (e.g. ``aws-global``, ``s3-external-1``) that will never resolve to a correct access point endpoint.
* api-change:``macie2``: This release of the Amazon Macie API adds support for defining run-time, S3 bucket criteria for classification jobs. It also adds resources for querying data about AWS resources that Macie monitors.
* api-change:``es``: Adds support for cold storage.
* api-change:``securityhub``: Updated descriptions to add notes on array lengths.
* api-change:``detective``: Updated descriptions of array parameters to add the restrictions on the array and value lengths.
* api-change:``transcribe``: Transcribe Medical now supports identification of PHI entities within transcripts
* api-change:``imagebuilder``: Text-only updates for bundled documentation feedback tickets - spring 2021.
* enhancement:FIPS: Add validation to only attempt to connect to FIPS endpoints with a FIPS pseudo-region if the pseudo-region is explicitly known to the SDK.


1.20.72
=======

* api-change:``ec2``: High Memory virtual instances are powered by Intel Sky Lake CPUs and offer up to 12TB of memory.


1.20.71
=======

* api-change:``ssm-incidents``: AWS Systems Manager Incident Manager enables faster resolution of critical application availability and performance issues, management of contacts and post-incident analysis
* api-change:``ssm-contacts``: AWS Systems Manager Incident Manager enables faster resolution of critical application availability and performance issues, management of contacts and post incident analysis
* api-change:``s3control``: Documentation updates for Amazon S3-control


1.20.70
=======

* api-change:``mediaconvert``: AWS Elemental MediaConvert SDK has added support for Kantar SNAP File Audio Watermarking with a Kantar Watermarking account, and Display Definition Segment(DDS) segment data controls for DVB-Sub caption outputs.
* api-change:``ecs``: This release contains updates for Amazon ECS.
* api-change:``codeartifact``: Documentation updates for CodeArtifact
* api-change:``eks``: This release updates create-nodegroup and update-nodegroup-config APIs for adding/updating taints on managed nodegroups.
* api-change:``iotwireless``: Add three new optional fields to support filtering and configurable sub-band in WirelessGateway APIs. The filtering is for all the RF region supported. The sub-band configuration is only applicable to LoRa gateways of US915 or AU915 RF region.
* api-change:``ssm``: This release adds new APIs to associate, disassociate and list related items in SSM OpsCenter; and this release adds DisplayName as a version-level attribute for SSM Documents and introduces two new document types: ProblemAnalysis, ProblemAnalysisTemplate.
* api-change:``kinesisanalyticsv2``: Amazon Kinesis Analytics now supports ListApplicationVersions and DescribeApplicationVersion API for Apache Flink applications
* api-change:``config``: Adds paginator to multiple APIs: By default, the paginator allows user to iterate over the results and allows the CLI to return up to 1000 results.


1.20.69
=======

* api-change:``lakeformation``: This release adds Tag Based Access Control to AWS Lake Formation service
* api-change:``lookoutmetrics``: Enforcing UUID style for parameters that are already in UUID format today. Documentation specifying eventual consistency of lookoutmetrics resources.
* api-change:``connect``: Adds tagging support for Connect APIs CreateIntegrationAssociation and CreateUseCase.


1.20.68
=======

* api-change:``servicediscovery``: Bugfix: Improved input validation for RegisterInstance action, InstanceId field
* api-change:``kafka``: IAM Access Control for Amazon MSK enables you to create clusters that use IAM to authenticate clients and to allow or deny Apache Kafka actions for those clients.
* api-change:``ssm``: SSM feature release - ChangeCalendar integration with StateManager.
* api-change:``snowball``: AWS Snow Family adds APIs for ordering and managing Snow jobs with long term pricing


1.20.67
=======

* api-change:``auditmanager``: This release updates the CreateAssessmentFrameworkControlSet and UpdateAssessmentFrameworkControlSet API data types. For both of these data types, the control set name is now a required attribute.
* api-change:``nimble``: Documentation Updates for Amazon Nimble Studio.
* api-change:``kinesisanalyticsv2``: Amazon Kinesis Analytics now supports RollbackApplication for Apache Flink applications to revert the application to the previous running version
* api-change:``sagemaker``: Amazon SageMaker Autopilot now provides the ability to automatically deploy the best model to an endpoint


1.20.66
=======

* api-change:``finspace``: Documentation updates for FinSpace API.
* api-change:``finspace-data``: Documentation updates for FinSpaceData API.


1.20.65
=======

* api-change:``devops-guru``: Added GetCostEstimation and StartCostEstimation to get the monthly resource usage cost and added ability to view resource health by AWS service name and to search insights be AWS service name.
* api-change:``acm-pca``: This release adds the KeyStorageSecurityStandard parameter to the CreateCertificateAuthority API to allow customers to mandate a security standard to which the CA key will be stored within.
* api-change:``health``: Documentation updates for health
* api-change:``chime``: This release adds the ability to search for and order international phone numbers for Amazon Chime SIP media applications.
* api-change:``sagemaker``: Enable retrying Training and Tuning Jobs that fail with InternalServerError by setting RetryStrategy.


1.20.64
=======

* api-change:``finspace-data``: Update FinSpace Data serviceAbbreviation


1.20.63
=======

* api-change:``finspace-data``: This is the initial SDK release for the data APIs for Amazon FinSpace. Amazon FinSpace is a data management and analytics application for the financial services industry (FSI).
* api-change:``mturk``: Update mturk client to latest version
* api-change:``chime``: Added new BatchCreateChannelMembership API to support multiple membership creation for channels
* api-change:``finspace``: This is the initial SDK release for the management APIs for Amazon FinSpace. Amazon FinSpace is a data management and analytics service for the financial services industry (FSI).
* api-change:``securityhub``: Updated ASFF to add the following new resource details objects: AwsEc2NetworkAcl, AwsEc2Subnet, and AwsElasticBeanstalkEnvironment.


1.20.62
=======

* api-change:``personalize``: Update URL for dataset export job documentation.
* api-change:``marketplace-catalog``: Allows user defined names for Changes in a ChangeSet. Users can use ChangeNames to reference properties in another Change within a ChangeSet. This feature allows users to make changes to an entity when the entity identifier is not yet available while constructing the StartChangeSet request.
* api-change:``forecast``: Added new DeleteResourceTree operation that helps in deleting all the child resources of a given resource including the given resource.
* api-change:``robomaker``: Adds ROS2 Foxy as a supported Robot Software Suite Version and Gazebo 11 as a supported Simulation Software Suite Version
* api-change:``cloudfront``: CloudFront now supports CloudFront Functions, a native feature of CloudFront that enables you to write lightweight functions in JavaScript for high-scale, latency-sensitive CDN customizations.
* api-change:``customer-profiles``: This release introduces GetMatches and MergeProfiles APIs to fetch and merge duplicate profiles


1.20.61
=======

* api-change:``macie2``: The Amazon Macie API now provides S3 bucket metadata that indicates whether a bucket policy requires server-side encryption of objects when objects are uploaded to the bucket.
* api-change:``organizations``: Minor text updates for AWS Organizations API Reference
* api-change:``ecs``: Add support for EphemeralStorage on TaskDefinition and TaskOverride
* api-change:``chime``: Increase AppInstanceUserId length to 64 characters


1.20.60
=======

* api-change:``connect``: Updated max number of tags that can be attached from 200 to 50. MaxContacts is now an optional parameter for the UpdateQueueMaxContact API.
* api-change:``mediapackage-vod``: MediaPackage now offers the option to place your Sequence Parameter Set (SPS), Picture Parameter Set (PPS), and Video Parameter Set (VPS) encoder metadata in every video segment instead of in the init fragment for DASH and CMAF endpoints.
* api-change:``nimble``: Amazon Nimble Studio is a virtual studio service that empowers visual effects, animation, and interactive content teams to create content securely within a scalable, private cloud service.
* api-change:``iotsitewise``: AWS IoT SiteWise interpolation API will get interpolated values for an asset property per specified time interval during a period of time.
* api-change:``cloudformation``: Add CallAs parameter to GetTemplateSummary to enable use with StackSets delegated administrator integration


1.20.59
=======

* api-change:``auditmanager``: This release restricts using backslashes in control, assessment, and framework names. The controlSetName field of the UpdateAssessmentFrameworkControlSet API now allows strings without backslashes.


1.20.58
=======

* api-change:``ec2``: Adding support for Red Hat Enterprise Linux with HA for Reserved Instances.
* api-change:``iotwireless``: Add a new optional field MessageType to support Sidewalk devices in SendDataToWirelessDevice API
* api-change:``kinesisanalyticsv2``: Amazon Kinesis Data Analytics now supports custom application maintenance configuration using UpdateApplicationMaintenanceConfiguration API for Apache Flink applications. Customers will have visibility when their application is under maintenance status using 'MAINTENANCE' application status.
* api-change:``personalize``: Added support for exporting data imported into an Amazon Personalize dataset to a specified data source (Amazon S3 bucket).
* api-change:``mediaconvert``: Documentation updates for mediaconvert
* api-change:``codeguru-reviewer``: Include KMS Key Details in Repository Association APIs to enable usage of customer managed KMS Keys.
* api-change:``glue``: Adding Kafka Client Auth Related Parameters
* api-change:``eks``: This release updates existing Amazon EKS input validation so customers will see an InvalidParameterException instead of a ParamValidationError when they enter 0 for minSize and/or desiredSize. It also adds LaunchTemplate information to update responses and a new "CUSTOM" value for AMIType.


1.20.57
=======

* api-change:``mediapackage``: Add support for Widevine DRM on CMAF origin endpoints. Both Widevine and FairPlay DRMs can now be used simultaneously, with CBCS encryption.
* api-change:``sns``: Amazon SNS adds two new attributes, TemplateId and EntityId, for using sender IDs to send SMS messages to destinations in India.


1.20.56
=======

* api-change:``forecast``: This release adds EstimatedTimeRemaining minutes field to the DescribeDatasetImportJob, DescribePredictor, DescribeForecast API response which denotes the time remaining to complete the job IN_PROGRESS.
* api-change:``securityhub``: Replaced the term "master" with "administrator". Added new actions to replace AcceptInvitation, GetMasterAccount, and DisassociateFromMasterAccount. In Member, replaced MasterId with AdministratorId.
* api-change:``cognito-idp``: Documentation updates for cognito-idp
* api-change:``elasticache``: This release introduces log delivery of Redis slow log from Amazon ElastiCache.


1.20.55
=======

* api-change:``detective``: Added parameters to track the data volume in bytes for a member account. Deprecated the existing parameters that tracked the volume as a percentage of the allowed volume for a behavior graph. Changes reflected in MemberDetails object.
* api-change:``redshift``: Add operations: AddPartner, DescribePartners, DeletePartner, and UpdatePartnerStatus to support tracking integration status with data partners.
* api-change:``groundstation``: Support new S3 Recording Config allowing customers to write downlink data directly to S3.
* api-change:``kendra``: Amazon Kendra now enables users to override index-level boosting configurations for each query.
* api-change:``cloudformation``: Added support for creating and updating stack sets with self-managed permissions from templates that reference macros.


1.20.54
=======

* api-change:``savingsplans``: Added support for Amazon SageMaker in Machine Learning Savings Plans
* api-change:``ce``: Adding support for Sagemaker savings plans in GetSavingsPlansPurchaseRecommendation API


1.20.53
=======

* api-change:``sts``: STS now supports assume role with Web Identity using JWT token length upto 20000 characters
* api-change:``dms``: AWS DMS added support of TLS for Kafka endpoint. Added Describe endpoint setting API for DMS endpoints.


1.20.52
=======

* api-change:``mediaconnect``: For flows that use Listener protocols, you can now easily locate an output's outbound IP address for a private internet. Additionally, MediaConnect now supports the Waiters feature that makes it easier to poll for the status of a flow until it reaches its desired state.
* api-change:``config``: Add exception for DeleteRemediationConfiguration and DescribeRemediationExecutionStatus
* api-change:``route53``: Documentation updates for route53
* api-change:``codestar-connections``: This release adds tagging support for CodeStar Connections Host resources


1.20.51
=======

* api-change:``lightsail``: Documentation updates for Amazon Lightsail.
* api-change:``sts``: This release adds the SourceIdentity parameter that can be set when assuming a role.
* api-change:``comprehendmedical``: The InferICD10CM API now returns TIME_EXPRESSION entities that refer to medical conditions.
* api-change:``rds``: Clarify that enabling or disabling automated backups causes a brief downtime, not an outage.
* api-change:``redshift``: Added support to enable AQUA in Amazon Redshift clusters.


1.20.50
=======

* api-change:``fsx``: Support for cross-region and cross-account backup copies
* api-change:``codebuild``: AWS CodeBuild now allows you to set the access permissions for build artifacts, project artifacts, and log files that are uploaded to an Amazon S3 bucket that is owned by another account.


1.20.49
=======

* api-change:``redshift``: Add support for case sensitive table level restore
* api-change:``ec2``: Add paginator support to DescribeStoreImageTasks and update documentation.
* api-change:``shield``: CreateProtection now throws InvalidParameterException instead of InternalErrorException when system tags (tag with keys prefixed with "aws:") are passed in.


1.20.48
=======

* api-change:``lookoutequipment``: This release introduces support for Amazon Lookout for Equipment.
* api-change:``kinesis-video-archived-media``: Documentation updates for archived.kinesisvideo
* api-change:``robomaker``: This release allows RoboMaker customers to specify custom tools to run with their simulation job
* api-change:``appstream``: This release provides support for image updates
* api-change:``ram``: Documentation updates for AWS RAM resource sharing
* api-change:``customer-profiles``: Documentation updates for Put-Integration API
* api-change:``autoscaling``: Amazon EC2 Auto Scaling announces Warm Pools that help applications to scale out faster by pre-initializing EC2 instances and save money by requiring fewer continuously running instances


1.20.47
=======

* api-change:``storagegateway``: File Gateway APIs now support FSx for Windows as a cloud storage.
* api-change:``accessanalyzer``: IAM Access Analyzer now analyzes your CloudTrail events to identify actions and services that have been used by an IAM entity (user or role) and generates an IAM policy that is based on that activity.
* api-change:``elasticache``: This release adds tagging support for all AWS ElastiCache resources except Global Replication Groups.
* api-change:``ivs``: This release adds support for the Auto-Record to S3 feature. Amazon IVS now enables you to save your live video to Amazon S3.
* api-change:``mgn``: Add new service - Application Migration Service.


1.20.46
=======

* api-change:``ssm``: Supports removing a label or labels from a parameter, enables ScheduledEndTime and ChangeDetails for StartChangeRequestExecution API, supports critical/security/other noncompliant count for patch API.
* api-change:``medialive``: MediaLive VPC outputs update to include Availability Zones, Security groups, Elastic Network Interfaces, and Subnet Ids in channel response
* api-change:``ec2``: This release adds support for storing EBS-backed AMIs in S3 and restoring them from S3 to enable cross-partition copying of AMIs
* api-change:``cloud9``: Documentation updates for Cloud9


1.20.45
=======

* api-change:``auditmanager``: AWS Audit Manager has updated the GetAssessment API operation to include a new response field called userRole. The userRole field indicates the role information and IAM ARN of the API caller.
* api-change:``medialive``: MediaLive now support HTML5 Motion Graphics overlay
* api-change:``appflow``: Added destination properties for Zendesk.


1.20.44
=======

* api-change:``mediapackage``: SPEKE v2 is an upgrade to the existing SPEKE API to support multiple encryption keys, based on an encryption contract selected by the customer.
* api-change:``imagebuilder``: This release adds support for Block Device Mappings for container image builds, and adds distribution configuration support for EC2 launch templates in AMI builds.


1.20.43
=======

* api-change:``route53resolver``: Route 53 Resolver DNS Firewall is a firewall service that allows you to filter and regulate outbound DNS traffic for your VPCs.
* api-change:``mediaconvert``: MediaConvert now supports HLS ingest, sidecar WebVTT ingest, Teletext color & style passthrough to TTML subtitles, TTML to WebVTT subtitle conversion with style, & DRC profiles in AC3 audio.
* api-change:``lightsail``: - This release adds support for state detail for Amazon Lightsail container services.
* api-change:``kendra``: AWS Kendra's ServiceNow data source now supports OAuth 2.0 authentication and knowledge article filtering via a ServiceNow query.
* api-change:``lex-models``: Lex now supports the ja-JP locale
* api-change:``lex-runtime``: Update lex-runtime client to latest version
* api-change:``fms``: Added Firewall Manager policy support for AWS Route 53 Resolver DNS Firewall.
* api-change:``ec2``: VPC Flow Logs Service adds a new API, GetFlowLogsIntegrationTemplate, which generates CloudFormation templates for Athena. For more info, see https://docs.aws.amazon.com/console/vpc/flow-logs/athena
* api-change:``wafv2``: Added support for ScopeDownStatement for ManagedRuleGroups, Labels, LabelMatchStatement, and LoggingFilter. For more information on these features, see the AWS WAF Developer Guide.


1.20.42
=======

* api-change:``iot``: Added ability to prefix search on attribute value for ListThings API.
* api-change:``pricing``: Minor documentation and link updates.
* api-change:``transcribe``: Amazon Transcribe now supports creating custom language models in the following languages: British English (en-GB), Australian English (en-AU), Indian Hindi (hi-IN), and US Spanish (es-US).
* api-change:``cloudhsm``: Minor documentation and link updates.
* api-change:``comprehend``: Support for customer managed KMS encryption of Comprehend custom models
* api-change:``cognito-sync``: Minor documentation updates and link updates.
* api-change:``batch``: AWS Batch adds support for Amazon EFS File System
* api-change:``detective``: Added the ability to assign tag values to Detective behavior graphs. Tag values can be used for attribute-based access control, and for cost allocation for billing.
* api-change:``iotwireless``: Add Sidewalk support to APIs: GetWirelessDevice, ListWirelessDevices, GetWirelessDeviceStatistics. Add Gateway connection status in GetWirelessGatewayStatistics API.
* api-change:``cloudformation``: 1. Added a new parameter RegionConcurrencyType in OperationPreferences. 2. Changed the name of AccountUrl to AccountsUrl in DeploymentTargets parameter.
* api-change:``cloud9``: Add ImageId input parameter to CreateEnvironmentEC2 endpoint. New parameter enables creation of environments with different AMIs.
* api-change:``directconnect``: This release adds MACsec support to AWS Direct Connect
* api-change:``redshift``: Enable customers to share access to their Redshift clusters from other VPCs (including VPCs from other accounts).
* api-change:``workmail``: This release adds support for mobile device access rules management in Amazon WorkMail.
* api-change:``datapipeline``: Minor documentation updates and link updates.
* api-change:``machinelearning``: Minor documentation updates and link updates.


1.20.41
=======

* api-change:``sagemaker``: Amazon SageMaker Autopilot now supports 1) feature importance reports for AutoML jobs and 2) PartialFailures for AutoML jobs
* api-change:``ec2-instance-connect``: Adding support to push SSH keys to the EC2 serial console in order to allow an SSH connection to your Amazon EC2 instance's serial port.
* api-change:``cloudwatch``: Update cloudwatch client to latest version
* api-change:``databrew``: This SDK release adds two new dataset features: 1) support for specifying a database connection as a dataset input 2) support for dynamic datasets that accept configurable parameters in S3 path.
* api-change:``frauddetector``: This release adds support for Batch Predictions in Amazon Fraud Detector.
* api-change:``ec2``: ReplaceRootVolume feature enables customers to replace the EBS root volume of a running instance to a previously known state. Add support to grant account-level access to the EC2 serial console
* api-change:``config``: Adding new APIs to support ConformancePack Compliance CI in Aggregators
* api-change:``pinpoint``: Added support for journey pause/resume, journey updatable import segment and journey quiet time wait.


1.20.40
=======

* api-change:``wafv2``: Added custom request handling and custom response support in rule actions and default action; Added the option to inspect the web request body as parsed and filtered JSON.
* api-change:``iam``: AWS Identity and Access Management GetAccessKeyLastUsed API will throw a custom error if customer public key is not found for access keys.
* api-change:``glue``: Allow Dots in Registry and Schema Names for CreateRegistry, CreateSchema; Fixed issue when duplicate keys are present and not returned as part of QuerySchemaVersionMetadata.
* api-change:``docdb``: This release adds support for Event Subscriptions to DocumentDB.
* api-change:``location``: Amazon Location added support for specifying pricing plan information on resources in alignment with our cost model.


1.20.39
=======

* api-change:``iotwireless``: Support tag-on-create for WirelessDevice.
* api-change:``customer-profiles``: This release adds an optional parameter named FlowDefinition in PutIntegrationRequest.
* api-change:``events``: Add support for SageMaker Model Builder Pipelines Targets to EventBridge
* api-change:``transcribe``: Amazon Transcribe now supports tagging words that match your vocabulary filter for batch transcription.


1.20.38
=======

* api-change:``lookoutmetrics``: Allowing uppercase alphabets for RDS and Redshift database names.


1.20.37
=======

* api-change:``sqs``: Documentation updates for Amazon SQS
* api-change:``rekognition``: This release introduces AWS tagging support for Amazon Rekognition collections, stream processors, and Custom Label models.
* api-change:``sagemaker``: This feature allows customer to specify the environment variables in their CreateTrainingJob requests.
* api-change:``medialive``: EML now supports handling HDR10 and HLG 2020 color space from a Link input.
* api-change:``lookoutmetrics``: Amazon Lookout for Metrics is now generally available. You can use Lookout for Metrics to monitor your data for anomalies. For more information, see the Amazon Lookout for Metrics Developer Guide.
* api-change:``alexaforbusiness``: Added support for enabling and disabling data retention in the CreateProfile and UpdateProfile APIs and retrieving the state of data retention for a profile in the GetProfile API.


1.20.36
=======

* api-change:``ssm``: This release allows SSM Explorer customers to enable OpsData sources across their organization when creating a resource data sync.
* api-change:``route53``: Documentation updates for route53
* bugfix:S3: Fix an issue with XML newline normalization in PutBucketLifecycleConfiguration requests.
* api-change:``s3``: Documentation updates for Amazon S3
* api-change:``s3control``: Documentation updates for s3-control
* api-change:``ec2``: maximumEfaInterfaces added to DescribeInstanceTypes API
* api-change:``greengrass``: Updated the parameters to make name required for CreateGroup API.


1.20.35
=======

* api-change:``ce``: You can now create cost categories with inherited value rules and specify default values for any uncategorized costs.
* api-change:``fis``: Updated maximum allowed size of action parameter from 64 to 1024
* api-change:``redshift``: Removed APIs to control AQUA on clusters.
* api-change:``iam``: Documentation updates for IAM operations and descriptions.
* api-change:``gamelift``: GameLift adds support for using event notifications to monitor game session placements. Specify an SNS topic or use CloudWatch Events to track activity for a game session queue.


1.20.34
=======

* api-change:``ec2``: This release adds support for UEFI boot on selected AMD- and Intel-based EC2 instances.
* api-change:``redshift``: Added support to enable AQUA in Amazon Redshift clusters.
* api-change:``codeartifact``: Documentation updates for CodeArtifact
* api-change:``macie2``: This release of the Amazon Macie API adds support for publishing sensitive data findings to AWS Security Hub and specifying which categories of findings to publish to Security Hub.


1.20.33
=======

* api-change:``sagemaker``: Adding authentication support for pulling images stored in private Docker registries to build containers for real-time inference.
* api-change:``ec2``: X2gd instances are the next generation of memory-optimized instances powered by AWS-designed, Arm-based AWS Graviton2 processors.


1.20.32
=======

* bugfix:s3: Updated mislabeled exceptions for S3 Object Lambda


1.20.31
=======

* api-change:``autoscaling``: Amazon EC2 Auto Scaling Instance Refresh now supports phased deployments.
* api-change:``s3``: S3 Object Lambda is a new S3 feature that enables users to apply their own custom code to process the output of a standard S3 GET request by automatically invoking a Lambda function with a GET request
* api-change:``redshift``: Add new fields for additional information about VPC endpoint for clusters with reallocation enabled, and a new field for total storage capacity for all clusters.
* api-change:``s3control``: S3 Object Lambda is a new S3 feature that enables users to apply their own custom code to process the output of a standard S3 GET request by automatically invoking a Lambda function with a GET request
* api-change:``securityhub``: New object for separate provider and customer values. New objects track S3 Public Access Block configuration and identify sensitive data. BatchImportFinding requests are limited to 100 findings.


1.20.30
=======

* api-change:``sagemaker``: Support new target device ml_eia2 in SageMaker CreateCompilationJob API
* api-change:``batch``: Making serviceRole an optional parameter when creating a compute environment. If serviceRole is not provided then Service Linked Role will be created (or reused if it already exists).


1.20.29
=======

* api-change:``lambda``: Allow empty list for function response types
* api-change:``iam``: Documentation updates for AWS Identity and Access Management (IAM).
* api-change:``mediaconnect``: This release adds support for the SRT-listener protocol on sources and outputs.
* api-change:``accessanalyzer``: This release adds support for the ValidatePolicy API. IAM Access Analyzer is adding over 100 policy checks and actionable recommendations that help you validate your policies during authoring.
* api-change:``mediatailor``: MediaTailor channel assembly is a new manifest-only service that allows you to assemble linear streams using your existing VOD content.
* api-change:``mwaa``: This release adds UPDATE_FAILED and UNAVAILABLE MWAA environment states.
* api-change:``gamelift``: GameLift expands to six new AWS Regions, adds support for multi-location fleets to streamline management of hosting resources, and lets you customize more of the game session placement process.


1.20.28
=======

* api-change:``fis``: Initial release of AWS Fault Injection Simulator, a managed service that enables you to perform fault injection experiments on your AWS workloads
* api-change:``codedeploy``: AWS CodeDeploy can now detect instances running an outdated revision of your application and automatically update them with the latest revision.
* api-change:``emr``: Update emr client to latest version
* api-change:``ecs``: This is for ecs exec feature release which includes two new APIs - execute-command and update-cluster and an AWS CLI customization for execute-command API


1.20.27
=======

* api-change:``mediatailor``: MediaTailor channel assembly is a new manifest-only service that allows you to assemble linear streams using your existing VOD content.
* api-change:``workspaces``: Adds API support for WorkSpaces bundle management operations.
* api-change:``cur``: - Added optional billingViewArn field for OSG.


1.20.26
=======

* api-change:``comprehend``: Update comprehend client to latest version
* api-change:``wafv2``: Update wafv2 client to latest version
* api-change:``medialive``: Update medialive client to latest version
* api-change:``network-firewall``: Update network-firewall client to latest version


1.20.25
=======

* api-change:``accessanalyzer``: Update accessanalyzer client to latest version
* api-change:``ssm``: Update ssm client to latest version
* api-change:``s3``: Update s3 client to latest version
* api-change:``backup``: Update backup client to latest version


1.20.24
=======

* api-change:``rds``: Update rds client to latest version
* api-change:``codeguruprofiler``: Update codeguruprofiler client to latest version
* api-change:``autoscaling``: Update autoscaling client to latest version
* api-change:``iotwireless``: Update iotwireless client to latest version
* api-change:``efs``: Update efs client to latest version


1.20.23
=======

* api-change:``lambda``: Update lambda client to latest version
* api-change:``emr``: Update emr client to latest version
* api-change:``kinesis-video-archived-media``: Update kinesis-video-archived-media client to latest version
* api-change:``s3``: Update s3 client to latest version
* api-change:``s3control``: Update s3control client to latest version
* api-change:``autoscaling``: Update autoscaling client to latest version


1.20.22
=======

* api-change:``license-manager``: Update license-manager client to latest version
* api-change:``network-firewall``: Update network-firewall client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``athena``: Update athena client to latest version
* api-change:``medialive``: Update medialive client to latest version
* api-change:``shield``: Update shield client to latest version
* api-change:``codepipeline``: Update codepipeline client to latest version
* api-change:``appflow``: Update appflow client to latest version


1.20.21
=======

* api-change:``servicediscovery``: Update servicediscovery client to latest version
* api-change:``events``: Update events client to latest version
* api-change:``sagemaker``: Update sagemaker client to latest version
* api-change:``mwaa``: Update mwaa client to latest version


1.20.20
=======

* api-change:``forecast``: Update forecast client to latest version
* api-change:``secretsmanager``: Update secretsmanager client to latest version
* api-change:``macie2``: Update macie2 client to latest version
* api-change:``codebuild``: Update codebuild client to latest version
* api-change:``es``: Update es client to latest version
* api-change:``acm``: Update acm client to latest version
* api-change:``wellarchitected``: Update wellarchitected client to latest version


1.20.19
=======

* api-change:``iotwireless``: Update iotwireless client to latest version
* api-change:``directconnect``: Update directconnect client to latest version
* bugfix:S3: Fix an issue with XML newline normalization that could result in the DeleteObjects operation incorrectly deleting the wrong keys.
* api-change:``managedblockchain``: Update managedblockchain client to latest version
* api-change:``events``: Update events client to latest version
* api-change:``compute-optimizer``: Update compute-optimizer client to latest version
* api-change:``datasync``: Update datasync client to latest version


1.20.18
=======

* api-change:``alexaforbusiness``: Update alexaforbusiness client to latest version
* api-change:``ssm``: Update ssm client to latest version
* api-change:``codepipeline``: Update codepipeline client to latest version
* api-change:``eks``: Update eks client to latest version


1.20.17
=======

* api-change:``s3``: Update s3 client to latest version
* api-change:``sso-admin``: Update sso-admin client to latest version
* api-change:``eks``: Update eks client to latest version
* api-change:``emr``: Update emr client to latest version


1.20.16
=======

* api-change:``databrew``: Update databrew client to latest version
* api-change:``detective``: Update detective client to latest version
* api-change:``lightsail``: Update lightsail client to latest version
* api-change:``imagebuilder``: Update imagebuilder client to latest version
* api-change:``transfer``: Update transfer client to latest version


1.20.15
=======

* api-change:``es``: Update es client to latest version
* api-change:``mediapackage-vod``: Update mediapackage-vod client to latest version
* api-change:``appflow``: Update appflow client to latest version
* api-change:``ecr-public``: Update ecr-public client to latest version
* api-change:``compute-optimizer``: Update compute-optimizer client to latest version


1.20.14
=======

* api-change:``glue``: Update glue client to latest version
* api-change:``redshift-data``: Update redshift-data client to latest version
* api-change:``s3control``: Update s3control client to latest version
* api-change:``autoscaling``: Update autoscaling client to latest version
* api-change:``pinpoint``: Update pinpoint client to latest version
* api-change:``quicksight``: Update quicksight client to latest version
* api-change:``iotevents``: Update iotevents client to latest version
* api-change:``connect``: Update connect client to latest version


1.20.13
=======

* api-change:``sagemaker-runtime``: Update sagemaker-runtime client to latest version
* api-change:``sagemaker``: Update sagemaker client to latest version


1.20.12
=======

* api-change:``rds``: Update rds client to latest version


1.20.11
=======

* api-change:``health``: Update health client to latest version
* api-change:``sagemaker``: Update sagemaker client to latest version
* api-change:``cloudformation``: Update cloudformation client to latest version
* api-change:``codebuild``: Update codebuild client to latest version


1.20.10
=======

* api-change:``ec2``: Update ec2 client to latest version
* api-change:``config``: Update config client to latest version
* api-change:``lookoutvision``: Update lookoutvision client to latest version


1.20.9
======

* api-change:``devops-guru``: Update devops-guru client to latest version
* api-change:``codebuild``: Update codebuild client to latest version


1.20.8
======

* api-change:``lightsail``: Update lightsail client to latest version
* api-change:``medialive``: Update medialive client to latest version
* api-change:``kinesis-video-archived-media``: Update kinesis-video-archived-media client to latest version
* api-change:``config``: Update config client to latest version
* api-change:``pinpoint``: Update pinpoint client to latest version
* api-change:``redshift-data``: Update redshift-data client to latest version
* api-change:``workmailmessageflow``: Update workmailmessageflow client to latest version
* api-change:``mediatailor``: Update mediatailor client to latest version


1.20.7
======

* api-change:``personalize-events``: Update personalize-events client to latest version
* api-change:``eks``: Update eks client to latest version
* api-change:``iam``: Update iam client to latest version
* api-change:``codepipeline``: Update codepipeline client to latest version
* api-change:``detective``: Update detective client to latest version
* api-change:``macie2``: Update macie2 client to latest version
* api-change:``wafv2``: Update wafv2 client to latest version
* api-change:``elbv2``: Update elbv2 client to latest version
* api-change:``appsync``: Update appsync client to latest version
* api-change:``rds``: Update rds client to latest version


1.20.6
======

* api-change:``databrew``: Update databrew client to latest version
* api-change:``rds``: Update rds client to latest version


1.20.5
======

* api-change:``quicksight``: Update quicksight client to latest version
* api-change:``mediaconvert``: Update mediaconvert client to latest version
* api-change:``qldb-session``: Update qldb-session client to latest version
* api-change:``sagemaker``: Update sagemaker client to latest version
* api-change:``gamelift``: Update gamelift client to latest version


1.20.4
======

* api-change:``dataexchange``: Update dataexchange client to latest version
* api-change:``cloudtrail``: Update cloudtrail client to latest version
* api-change:``elbv2``: Update elbv2 client to latest version
* api-change:``ivs``: Update ivs client to latest version
* api-change:``macie2``: Update macie2 client to latest version
* api-change:``globalaccelerator``: Update globalaccelerator client to latest version
* api-change:``iotsitewise``: Update iotsitewise client to latest version
* api-change:``elasticache``: Update elasticache client to latest version


1.20.3
======

* api-change:``macie``: Update macie client to latest version
* api-change:``elbv2``: Update elbv2 client to latest version
* api-change:``organizations``: Update organizations client to latest version


1.20.2
======

* api-change:``quicksight``: Update quicksight client to latest version
* api-change:``appflow``: Update appflow client to latest version
* api-change:``emr-containers``: Update emr-containers client to latest version
* api-change:``dlm``: Update dlm client to latest version
* api-change:``athena``: Update athena client to latest version
* api-change:``ec2``: Update ec2 client to latest version


1.20.1
======

* api-change:``lambda``: Update lambda client to latest version
* api-change:``codebuild``: Update codebuild client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``ce``: Update ce client to latest version
* api-change:``databrew``: Update databrew client to latest version
* api-change:``securityhub``: Update securityhub client to latest version
* api-change:``workmail``: Update workmail client to latest version
* api-change:``auditmanager``: Update auditmanager client to latest version
* api-change:``compute-optimizer``: Update compute-optimizer client to latest version
* api-change:``iotsitewise``: Update iotsitewise client to latest version


1.20.0
======

* api-change:``appmesh``: Update appmesh client to latest version
* api-change:``application-autoscaling``: Update application-autoscaling client to latest version
* api-change:``lookoutvision``: Update lookoutvision client to latest version
* api-change:``organizations``: Update organizations client to latest version
* feature:Python: Dropped support for Python 3.4 and 3.5
* api-change:``s3control``: Update s3control client to latest version
* api-change:``rds-data``: Update rds-data client to latest version
* api-change:``medialive``: Update medialive client to latest version
* api-change:``route53``: Update route53 client to latest version
* api-change:``location``: Update location client to latest version
* enhancement:s3: Amazon S3 now supports AWS PrivateLink, providing direct access to S3 via a private endpoint within your virtual private network.
* api-change:``iotwireless``: Update iotwireless client to latest version


1.19.63
=======

* api-change:``macie2``: Update macie2 client to latest version
* api-change:``connect``: Update connect client to latest version
* api-change:``medialive``: Update medialive client to latest version


1.19.62
=======

* api-change:``wellarchitected``: Update wellarchitected client to latest version
* api-change:``managedblockchain``: Update managedblockchain client to latest version
* api-change:``cloudwatch``: Update cloudwatch client to latest version
* api-change:``databrew``: Update databrew client to latest version
* bugfix:Validator: Fix showing incorrect max-value in error message for range and length value validation
* api-change:``iot``: Update iot client to latest version
* api-change:``robomaker``: Update robomaker client to latest version


1.19.61
=======

* api-change:``elasticache``: Update elasticache client to latest version
* api-change:``customer-profiles``: Update customer-profiles client to latest version
* api-change:``sesv2``: Update sesv2 client to latest version
* api-change:``accessanalyzer``: Update accessanalyzer client to latest version
* api-change:``lightsail``: Update lightsail client to latest version
* api-change:``es``: Update es client to latest version


1.19.60
=======

* api-change:``backup``: Update backup client to latest version


1.19.59
=======

* api-change:``greengrassv2``: Update greengrassv2 client to latest version
* api-change:``redshift``: Update redshift client to latest version
* api-change:``lexv2-runtime``: Update lexv2-runtime client to latest version
* api-change:``rds``: Update rds client to latest version
* api-change:``lexv2-models``: Update lexv2-models client to latest version
* api-change:``ssm``: Update ssm client to latest version
* api-change:``ec2``: Update ec2 client to latest version


1.19.58
=======

* api-change:``securityhub``: Update securityhub client to latest version
* api-change:``kafka``: Update kafka client to latest version
* api-change:``resourcegroupstaggingapi``: Update resourcegroupstaggingapi client to latest version


1.19.57
=======

* api-change:``acm-pca``: Update acm-pca client to latest version
* api-change:``chime``: Update chime client to latest version
* api-change:``ecs``: Update ecs client to latest version


1.19.56
=======

* api-change:``sns``: Update sns client to latest version


1.19.55
=======

* api-change:``pinpoint``: Update pinpoint client to latest version
* api-change:``cognito-identity``: Update cognito-identity client to latest version
* api-change:``s3control``: Update s3control client to latest version
* api-change:``sagemaker``: Update sagemaker client to latest version


1.19.54
=======

* api-change:``frauddetector``: Update frauddetector client to latest version
* api-change:``personalize``: Update personalize client to latest version


1.19.53
=======

* api-change:``appstream``: Update appstream client to latest version
* api-change:``auditmanager``: Update auditmanager client to latest version
* api-change:``ssm``: Update ssm client to latest version
* api-change:``elasticache``: Update elasticache client to latest version
* api-change:``lightsail``: Update lightsail client to latest version


1.19.52
=======

* api-change:``rds``: Update rds client to latest version
* api-change:``kms``: Update kms client to latest version


1.19.51
=======

* api-change:``devops-guru``: Update devops-guru client to latest version
* api-change:``codepipeline``: Update codepipeline client to latest version
* api-change:``mediaconvert``: Update mediaconvert client to latest version


1.19.50
=======

* api-change:``autoscaling``: Update autoscaling client to latest version
* api-change:``transfer``: Update transfer client to latest version
* api-change:``autoscaling-plans``: Update autoscaling-plans client to latest version


1.19.49
=======

* api-change:``ce``: Update ce client to latest version
* api-change:``application-autoscaling``: Update application-autoscaling client to latest version


1.19.48
=======

* api-change:``healthlake``: Update healthlake client to latest version
* api-change:``cloudsearch``: Update cloudsearch client to latest version


1.19.47
=======

* api-change:``servicecatalog``: Update servicecatalog client to latest version


1.19.46
=======

* api-change:``macie2``: Update macie2 client to latest version
* api-change:``elasticache``: Update elasticache client to latest version


1.19.45
=======

* api-change:``acm-pca``: Update acm-pca client to latest version
* api-change:``apigatewayv2``: Update apigatewayv2 client to latest version


1.19.44
=======

* api-change:``cloudfront``: Update cloudfront client to latest version


1.19.43
=======

* api-change:``compute-optimizer``: Update compute-optimizer client to latest version
* api-change:``resource-groups``: Update resource-groups client to latest version
* api-change:``dms``: Update dms client to latest version


1.19.42
=======

* api-change:``ssm``: Update ssm client to latest version
* api-change:``iotwireless``: Update iotwireless client to latest version
* api-change:``rds``: Update rds client to latest version
* api-change:``glue``: Update glue client to latest version
* api-change:``ce``: Update ce client to latest version
* api-change:``connect``: Update connect client to latest version
* api-change:``elasticache``: Update elasticache client to latest version


1.19.41
=======

* api-change:``config``: Update config client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``glue``: Update glue client to latest version
* api-change:``batch``: Update batch client to latest version
* api-change:``managedblockchain``: Update managedblockchain client to latest version
* api-change:``service-quotas``: Update service-quotas client to latest version
* api-change:``s3``: Update s3 client to latest version
* api-change:``connectparticipant``: Update connectparticipant client to latest version
* api-change:``securityhub``: Update securityhub client to latest version
* api-change:``qldb-session``: Update qldb-session client to latest version
* api-change:``outposts``: Update outposts client to latest version
* api-change:``servicecatalog-appregistry``: Update servicecatalog-appregistry client to latest version
* api-change:``dms``: Update dms client to latest version
* api-change:``apigateway``: Update apigateway client to latest version


1.19.40
=======

* api-change:``rds``: Update rds client to latest version
* bugfix:SSO: Fixed timestamp format for SSO credential expirations
* api-change:``personalize-runtime``: Update personalize-runtime client to latest version
* api-change:``ec2``: Update ec2 client to latest version


1.19.39
=======

* api-change:``ec2``: Update ec2 client to latest version
* api-change:``servicecatalog``: Update servicecatalog client to latest version
* api-change:``dlm``: Update dlm client to latest version
* api-change:``kms``: Update kms client to latest version
* api-change:``route53resolver``: Update route53resolver client to latest version
* api-change:``sqs``: Update sqs client to latest version
* api-change:``config``: Update config client to latest version
* api-change:``imagebuilder``: Update imagebuilder client to latest version
* api-change:``route53``: Update route53 client to latest version


1.19.38
=======

* api-change:``ce``: Update ce client to latest version
* api-change:``amp``: Update amp client to latest version
* api-change:``location``: Update location client to latest version
* api-change:``wellarchitected``: Update wellarchitected client to latest version
* api-change:``quicksight``: Update quicksight client to latest version


1.19.37
=======

* api-change:``iotwireless``: Update iotwireless client to latest version
* api-change:``lambda``: Update lambda client to latest version
* api-change:``greengrassv2``: Update greengrassv2 client to latest version
* api-change:``ssm``: Update ssm client to latest version
* api-change:``iotdeviceadvisor``: Update iotdeviceadvisor client to latest version
* api-change:``iot``: Update iot client to latest version
* api-change:``iotanalytics``: Update iotanalytics client to latest version
* api-change:``amp``: Update amp client to latest version
* api-change:``iotfleethub``: Update iotfleethub client to latest version


1.19.36
=======

* api-change:``ec2``: Update ec2 client to latest version
* api-change:``globalaccelerator``: Update globalaccelerator client to latest version
* api-change:``devops-guru``: Update devops-guru client to latest version


1.19.35
=======

* api-change:``guardduty``: Update guardduty client to latest version
* api-change:``iotsitewise``: Update iotsitewise client to latest version
* api-change:``autoscaling``: Update autoscaling client to latest version
* api-change:``cloudwatch``: Update cloudwatch client to latest version
* api-change:``pi``: Update pi client to latest version
* api-change:``cloudtrail``: Update cloudtrail client to latest version


1.19.34
=======

* api-change:``networkmanager``: Update networkmanager client to latest version
* api-change:``kendra``: Update kendra client to latest version
* api-change:``ec2``: Update ec2 client to latest version


1.19.33
=======

* api-change:``globalaccelerator``: Update globalaccelerator client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``redshift``: Update redshift client to latest version


1.19.32
=======

* api-change:``ecr``: Update ecr client to latest version
* api-change:``sagemaker``: Update sagemaker client to latest version
* api-change:``kendra``: Update kendra client to latest version
* api-change:``quicksight``: Update quicksight client to latest version
* api-change:``auditmanager``: Update auditmanager client to latest version
* api-change:``sagemaker-runtime``: Update sagemaker-runtime client to latest version
* api-change:``sagemaker-edge``: Update sagemaker-edge client to latest version
* api-change:``forecast``: Update forecast client to latest version
* api-change:``healthlake``: Update healthlake client to latest version
* api-change:``emr-containers``: Update emr-containers client to latest version


1.19.31
=======

* api-change:``dms``: Update dms client to latest version
* api-change:``servicecatalog-appregistry``: Update servicecatalog-appregistry client to latest version


1.19.30
=======

* api-change:``ssm``: Update ssm client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``workspaces``: Update workspaces client to latest version
* api-change:``license-manager``: Update license-manager client to latest version
* api-change:``lambda``: Update lambda client to latest version
* api-change:``ds``: Update ds client to latest version
* api-change:``kafka``: Update kafka client to latest version
* api-change:``medialive``: Update medialive client to latest version
* api-change:``rds``: Update rds client to latest version


1.19.29
=======

* api-change:``license-manager``: Update license-manager client to latest version
* api-change:``compute-optimizer``: Update compute-optimizer client to latest version
* api-change:``amplifybackend``: Update amplifybackend client to latest version
* api-change:``batch``: Update batch client to latest version


1.19.28
=======

* api-change:``customer-profiles``: Update customer-profiles client to latest version


1.19.27
=======

* api-change:``sagemaker-featurestore-runtime``: Update sagemaker-featurestore-runtime client to latest version
* api-change:``ecr-public``: Update ecr-public client to latest version
* api-change:``honeycode``: Update honeycode client to latest version
* api-change:``eks``: Update eks client to latest version
* api-change:``amplifybackend``: Update amplifybackend client to latest version
* api-change:``lambda``: Update lambda client to latest version
* api-change:``sagemaker``: Update sagemaker client to latest version
* api-change:``lookoutvision``: Update lookoutvision client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``connect``: Update connect client to latest version
* api-change:``connect-contact-lens``: Update connect-contact-lens client to latest version
* api-change:``profile``: Update profile client to latest version
* api-change:``s3``: Update s3 client to latest version
* api-change:``appintegrations``: Update appintegrations client to latest version
* api-change:``ds``: Update ds client to latest version
* api-change:``devops-guru``: Update devops-guru client to latest version


1.19.26
=======

* api-change:``ec2``: Update ec2 client to latest version


1.19.25
=======

* api-change:``mediaconvert``: Update mediaconvert client to latest version
* api-change:``cloudformation``: Update cloudformation client to latest version
* api-change:``appflow``: Update appflow client to latest version
* api-change:``fsx``: Update fsx client to latest version
* api-change:``stepfunctions``: Update stepfunctions client to latest version
* api-change:``timestream-write``: Update timestream-write client to latest version
* api-change:``elasticbeanstalk``: Update elasticbeanstalk client to latest version
* api-change:``batch``: Update batch client to latest version
* api-change:``cloudtrail``: Update cloudtrail client to latest version
* api-change:``cognito-idp``: Update cognito-idp client to latest version
* api-change:``iotsitewise``: Update iotsitewise client to latest version
* api-change:``codebuild``: Update codebuild client to latest version
* api-change:``comprehend``: Update comprehend client to latest version
* api-change:``quicksight``: Update quicksight client to latest version
* api-change:``mwaa``: Update mwaa client to latest version
* api-change:``lex-models``: Update lex-models client to latest version
* api-change:``gamelift``: Update gamelift client to latest version


1.19.24
=======

* api-change:``ec2``: Update ec2 client to latest version
* api-change:``translate``: Update translate client to latest version
* api-change:``kafka``: Update kafka client to latest version
* api-change:``application-insights``: Update application-insights client to latest version
* api-change:``glue``: Update glue client to latest version
* api-change:``signer``: Update signer client to latest version
* api-change:``codestar-connections``: Update codestar-connections client to latest version
* api-change:``codeartifact``: Update codeartifact client to latest version
* api-change:``elasticache``: Update elasticache client to latest version
* api-change:``emr``: Update emr client to latest version
* api-change:``forecast``: Update forecast client to latest version
* api-change:``iot``: Update iot client to latest version
* api-change:``autoscaling``: Update autoscaling client to latest version
* api-change:``ecs``: Update ecs client to latest version
* api-change:``timestream-query``: Update timestream-query client to latest version
* api-change:``sso-admin``: Update sso-admin client to latest version
* api-change:``securityhub``: Update securityhub client to latest version
* api-change:``lambda``: Update lambda client to latest version
* api-change:``outposts``: Update outposts client to latest version
* api-change:``license-manager``: Update license-manager client to latest version
* api-change:``dynamodb``: Update dynamodb client to latest version


1.19.23
=======

* api-change:``servicecatalog-appregistry``: Update servicecatalog-appregistry client to latest version
* api-change:``appmesh``: Update appmesh client to latest version
* api-change:``kafka``: Update kafka client to latest version
* api-change:``macie2``: Update macie2 client to latest version
* api-change:``chime``: Update chime client to latest version
* api-change:``cloudhsmv2``: Update cloudhsmv2 client to latest version
* api-change:``codeguru-reviewer``: Update codeguru-reviewer client to latest version
* api-change:``s3``: Update s3 client to latest version
* api-change:``cognito-identity``: Update cognito-identity client to latest version
* api-change:``connect``: Update connect client to latest version


1.19.22
=======

* api-change:``ce``: Update ce client to latest version
* api-change:``lex-runtime``: Update lex-runtime client to latest version
* api-change:``glue``: Update glue client to latest version
* api-change:``lex-models``: Update lex-models client to latest version
* api-change:``events``: Update events client to latest version
* api-change:``autoscaling``: Update autoscaling client to latest version
* api-change:``ds``: Update ds client to latest version
* api-change:``kinesisanalyticsv2``: Update kinesisanalyticsv2 client to latest version
* api-change:``redshift``: Update redshift client to latest version
* api-change:``medialive``: Update medialive client to latest version
* api-change:``lambda``: Update lambda client to latest version


1.19.21
=======

* api-change:``elasticache``: Update elasticache client to latest version
* api-change:``cloudformation``: Update cloudformation client to latest version
* api-change:``codebuild``: Update codebuild client to latest version
* bugfix:Retry: Fix bug where retries were attempted on any response with an "Error" key.
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``s3control``: Update s3control client to latest version
* api-change:``backup``: Update backup client to latest version
* api-change:``outposts``: Update outposts client to latest version


1.19.20
=======

* api-change:``connect``: Update connect client to latest version
* api-change:``chime``: Update chime client to latest version
* api-change:``fms``: Update fms client to latest version
* api-change:``network-firewall``: Update network-firewall client to latest version
* api-change:``rds``: Update rds client to latest version
* api-change:``macie2``: Update macie2 client to latest version


1.19.19
=======

* api-change:``sagemaker``: Update sagemaker client to latest version
* api-change:``iotsitewise``: Update iotsitewise client to latest version
* api-change:``dms``: Update dms client to latest version
* api-change:``iotsecuretunneling``: Update iotsecuretunneling client to latest version
* api-change:``sns``: Update sns client to latest version
* api-change:``synthetics``: Update synthetics client to latest version
* api-change:``servicecatalog``: Update servicecatalog client to latest version
* api-change:``codepipeline``: Update codepipeline client to latest version
* api-change:``quicksight``: Update quicksight client to latest version


1.19.18
=======

* api-change:``textract``: Update textract client to latest version
* api-change:``shield``: Update shield client to latest version
* api-change:``elbv2``: Update elbv2 client to latest version


1.19.17
=======

* api-change:``personalize-runtime``: Update personalize-runtime client to latest version
* api-change:``servicecatalog-appregistry``: Update servicecatalog-appregistry client to latest version
* api-change:``lex-models``: Update lex-models client to latest version
* api-change:``polly``: Update polly client to latest version
* api-change:``iot``: Update iot client to latest version
* api-change:``robomaker``: Update robomaker client to latest version
* api-change:``lightsail``: Update lightsail client to latest version


1.19.16
=======

* api-change:``mediaconvert``: Update mediaconvert client to latest version
* api-change:``servicecatalog``: Update servicecatalog client to latest version
* api-change:``databrew``: Update databrew client to latest version
* api-change:``forecast``: Update forecast client to latest version
* api-change:``amplify``: Update amplify client to latest version
* api-change:``quicksight``: Update quicksight client to latest version


1.19.15
=======

* api-change:``ec2``: Update ec2 client to latest version
* api-change:``elbv2``: Update elbv2 client to latest version
* api-change:``autoscaling``: Update autoscaling client to latest version
* api-change:``ssm``: Update ssm client to latest version


1.19.14
=======

* api-change:``dynamodb``: Update dynamodb client to latest version
* api-change:``es``: Update es client to latest version
* api-change:``fsx``: Update fsx client to latest version
* api-change:``macie2``: Update macie2 client to latest version
* api-change:``iotanalytics``: Update iotanalytics client to latest version
* api-change:``s3``: Update s3 client to latest version
* api-change:``storagegateway``: Update storagegateway client to latest version
* api-change:``ssm``: Update ssm client to latest version
* api-change:``ecs``: Update ecs client to latest version
* api-change:``datasync``: Update datasync client to latest version


1.19.13
=======

* api-change:``ssm``: Update ssm client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``iotsitewise``: Update iotsitewise client to latest version
* api-change:``medialive``: Update medialive client to latest version
* api-change:``dlm``: Update dlm client to latest version


1.19.12
=======

* api-change:``frauddetector``: Update frauddetector client to latest version
* api-change:``rds``: Update rds client to latest version
* api-change:``kendra``: Update kendra client to latest version
* api-change:``events``: Update events client to latest version
* api-change:``dynamodb``: Update dynamodb client to latest version
* api-change:``lambda``: Update lambda client to latest version
* api-change:``es``: Update es client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``appmesh``: Update appmesh client to latest version


1.19.11
=======

* api-change:``cloudwatch``: Update cloudwatch client to latest version
* api-change:``es``: Update es client to latest version
* api-change:``xray``: Update xray client to latest version
* api-change:``mq``: Update mq client to latest version
* api-change:``iot``: Update iot client to latest version
* api-change:``meteringmarketplace``: Update meteringmarketplace client to latest version
* api-change:``autoscaling``: Update autoscaling client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``servicecatalog``: Update servicecatalog client to latest version


1.19.10
=======

* api-change:``ec2``: Update ec2 client to latest version


1.19.9
======

* api-change:``medialive``: Update medialive client to latest version
* api-change:``dms``: Update dms client to latest version
* api-change:``macie2``: Update macie2 client to latest version
* api-change:``imagebuilder``: Update imagebuilder client to latest version
* api-change:``braket``: Update braket client to latest version
* api-change:``sns``: Update sns client to latest version
* api-change:``elasticache``: Update elasticache client to latest version


1.19.8
======

* api-change:``elbv2``: Update elbv2 client to latest version
* api-change:``codeartifact``: Update codeartifact client to latest version
* api-change:``marketplacecommerceanalytics``: Update marketplacecommerceanalytics client to latest version
* api-change:``apigateway``: Update apigateway client to latest version
* api-change:``sesv2``: Update sesv2 client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``storagegateway``: Update storagegateway client to latest version


1.19.7
======

* api-change:``ec2``: Update ec2 client to latest version
* api-change:``iot``: Update iot client to latest version
* api-change:``workmail``: Update workmail client to latest version


1.19.6
======

* api-change:``glue``: Update glue client to latest version


1.19.5
======

* api-change:``sagemaker``: Update sagemaker client to latest version
* api-change:``neptune``: Update neptune client to latest version
* api-change:``kendra``: Update kendra client to latest version


1.19.4
======

* api-change:``mediatailor``: Update mediatailor client to latest version
* api-change:``quicksight``: Update quicksight client to latest version
* api-change:``macie2``: Update macie2 client to latest version


1.19.3
======

* api-change:``servicecatalog``: Update servicecatalog client to latest version
* api-change:``sns``: Update sns client to latest version
* api-change:``accessanalyzer``: Update accessanalyzer client to latest version
* api-change:``appflow``: Update appflow client to latest version


1.19.2
======

* api-change:``organizations``: Update organizations client to latest version
* api-change:``globalaccelerator``: Update globalaccelerator client to latest version
* api-change:``kendra``: Update kendra client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``cloudfront``: Update cloudfront client to latest version
* api-change:``glue``: Update glue client to latest version


1.19.1
======

* api-change:``elasticbeanstalk``: Update elasticbeanstalk client to latest version
* api-change:``appsync``: Update appsync client to latest version
* api-change:``batch``: Update batch client to latest version


1.19.0
======

* api-change:``backup``: Update backup client to latest version
* api-change:``docdb``: Update docdb client to latest version
* api-change:``cloudfront``: Update cloudfront client to latest version
* api-change:``servicecatalog``: Update servicecatalog client to latest version
* feature:imds: Updated InstanceMetadataFetcher to use custom ipv6 uri as endpoint if envvar or config set
* api-change:``ssm``: Update ssm client to latest version


1.18.18
=======

* api-change:``medialive``: Update medialive client to latest version
* api-change:``organizations``: Update organizations client to latest version


1.18.17
=======

* api-change:``transfer``: Update transfer client to latest version
* api-change:``xray``: Update xray client to latest version
* api-change:``dms``: Update dms client to latest version
* api-change:``macie2``: Update macie2 client to latest version
* api-change:``ssm``: Update ssm client to latest version
* api-change:``groundstation``: Update groundstation client to latest version
* api-change:``rekognition``: Update rekognition client to latest version
* api-change:``ce``: Update ce client to latest version
* api-change:``workspaces``: Update workspaces client to latest version
* api-change:``glue``: Update glue client to latest version
* api-change:``budgets``: Update budgets client to latest version
* api-change:``accessanalyzer``: Update accessanalyzer client to latest version
* api-change:``rds``: Update rds client to latest version
* api-change:``workmail``: Update workmail client to latest version
* api-change:``iot``: Update iot client to latest version


1.18.16
=======

* api-change:``snowball``: Update snowball client to latest version
* api-change:``servicecatalog``: Update servicecatalog client to latest version
* api-change:``eks``: Update eks client to latest version
* api-change:``amplify``: Update amplify client to latest version
* api-change:``medialive``: Update medialive client to latest version


1.18.15
=======

* api-change:``ec2``: Update ec2 client to latest version
* api-change:``events``: Update events client to latest version
* api-change:``sns``: Update sns client to latest version
* api-change:``ce``: Update ce client to latest version
* api-change:``sagemaker``: Update sagemaker client to latest version
* api-change:``rds``: Update rds client to latest version
* api-change:``rekognition``: Update rekognition client to latest version


1.18.14
=======

* api-change:``mediapackage``: Update mediapackage client to latest version
* api-change:``ce``: Update ce client to latest version
* api-change:``compute-optimizer``: Update compute-optimizer client to latest version
* api-change:``elasticache``: Update elasticache client to latest version


1.18.13
=======

* api-change:``dms``: Update dms client to latest version
* api-change:``kinesisanalyticsv2``: Update kinesisanalyticsv2 client to latest version
* api-change:``marketplace-catalog``: Update marketplace-catalog client to latest version
* api-change:``ec2``: Update ec2 client to latest version


1.18.12
=======

* api-change:``dynamodbstreams``: Update dynamodbstreams client to latest version
* api-change:``sagemaker``: Update sagemaker client to latest version
* api-change:``mediaconvert``: Update mediaconvert client to latest version
* api-change:``dynamodb``: Update dynamodb client to latest version
* api-change:``glue``: Update glue client to latest version


1.18.11
=======

* api-change:``batch``: Update batch client to latest version
* api-change:``personalize-events``: Update personalize-events client to latest version
* api-change:``rds``: Update rds client to latest version
* api-change:``elbv2``: Update elbv2 client to latest version
* api-change:``servicediscovery``: Update servicediscovery client to latest version
* api-change:``s3``: Update s3 client to latest version


1.18.10
=======

* api-change:``glue``: Update glue client to latest version
* api-change:``kafka``: Update kafka client to latest version
* api-change:``appsync``: Update appsync client to latest version
* api-change:``emr``: Update emr client to latest version
* api-change:``wafv2``: Update wafv2 client to latest version
* api-change:``quicksight``: Update quicksight client to latest version


1.18.9
======

* api-change:``datasync``: Update datasync client to latest version
* api-change:``s3control``: Update s3control client to latest version
* api-change:``imagebuilder``: Update imagebuilder client to latest version
* api-change:``securityhub``: Update securityhub client to latest version
* api-change:``iot``: Update iot client to latest version
* api-change:``emr``: Update emr client to latest version
* api-change:``s3outposts``: Update s3outposts client to latest version
* api-change:``application-autoscaling``: Update application-autoscaling client to latest version
* api-change:``directconnect``: Update directconnect client to latest version
* api-change:``s3``: Update s3 client to latest version
* api-change:``mediaconnect``: Update mediaconnect client to latest version
* api-change:``pinpoint``: Update pinpoint client to latest version


1.18.8
======

* api-change:``timestream-write``: Update timestream-write client to latest version
* api-change:``connect``: Update connect client to latest version
* api-change:``ssm``: Update ssm client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``schemas``: Update schemas client to latest version
* api-change:``timestream-query``: Update timestream-query client to latest version


1.18.7
======

* api-change:``application-autoscaling``: Update application-autoscaling client to latest version
* api-change:``rds``: Update rds client to latest version


1.18.6
======

* api-change:``frauddetector``: Update frauddetector client to latest version
* api-change:``config``: Update config client to latest version
* api-change:``batch``: Update batch client to latest version
* api-change:``docdb``: Update docdb client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``sts``: Update sts client to latest version


1.18.5
======

* api-change:``transcribe``: Update transcribe client to latest version
* api-change:``textract``: Update textract client to latest version
* api-change:``amplify``: Update amplify client to latest version
* api-change:``eks``: Update eks client to latest version
* api-change:``savingsplans``: Update savingsplans client to latest version
* api-change:``synthetics``: Update synthetics client to latest version


1.18.4
======

* api-change:``translate``: Update translate client to latest version
* api-change:``ce``: Update ce client to latest version
* api-change:``quicksight``: Update quicksight client to latest version
* api-change:``backup``: Update backup client to latest version


1.18.3
======

* api-change:``comprehend``: Update comprehend client to latest version
* api-change:``dynamodbstreams``: Update dynamodbstreams client to latest version
* api-change:``workmail``: Update workmail client to latest version
* api-change:``lex-models``: Update lex-models client to latest version


1.18.2
======

* api-change:``glue``: Update glue client to latest version
* api-change:``resourcegroupstaggingapi``: Update resourcegroupstaggingapi client to latest version
* api-change:``iotsitewise``: Update iotsitewise client to latest version
* api-change:``events``: Update events client to latest version
* api-change:``resource-groups``: Update resource-groups client to latest version
* api-change:``rds``: Update rds client to latest version


1.18.1
======

* api-change:``medialive``: Update medialive client to latest version
* api-change:``sso-admin``: Update sso-admin client to latest version
* api-change:``codestar-connections``: Update codestar-connections client to latest version


1.18.0
======

* api-change:``kendra``: Update kendra client to latest version
* api-change:``cloudfront``: Update cloudfront client to latest version
* api-change:``comprehend``: Update comprehend client to latest version
* api-change:``apigateway``: Update apigateway client to latest version
* api-change:``es``: Update es client to latest version
* api-change:``apigatewayv2``: Update apigatewayv2 client to latest version
* feature:dependency: botocore has removed docutils as a required dependency


1.17.63
=======

* api-change:``servicecatalog``: Update servicecatalog client to latest version
* api-change:``dlm``: Update dlm client to latest version
* api-change:``greengrass``: Update greengrass client to latest version
* api-change:``connect``: Update connect client to latest version
* api-change:``ssm``: Update ssm client to latest version


1.17.62
=======

* api-change:``transcribe``: Update transcribe client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``sagemaker``: Update sagemaker client to latest version
* api-change:``medialive``: Update medialive client to latest version
* api-change:``budgets``: Update budgets client to latest version
* api-change:``kafka``: Update kafka client to latest version
* api-change:``kendra``: Update kendra client to latest version
* api-change:``organizations``: Update organizations client to latest version


1.17.61
=======

* api-change:``ec2``: Update ec2 client to latest version
* api-change:``managedblockchain``: Update managedblockchain client to latest version
* api-change:``stepfunctions``: Update stepfunctions client to latest version
* api-change:``docdb``: Update docdb client to latest version


1.17.60
=======

* api-change:``workspaces``: Update workspaces client to latest version


1.17.59
=======

* api-change:``cloudfront``: Update cloudfront client to latest version
* api-change:``ebs``: Update ebs client to latest version
* api-change:``sso-admin``: Update sso-admin client to latest version
* api-change:``s3``: Update s3 client to latest version


1.17.58
=======

* api-change:``kinesisanalyticsv2``: Update kinesisanalyticsv2 client to latest version
* api-change:``glue``: Update glue client to latest version
* api-change:``redshift-data``: Update redshift-data client to latest version


1.17.57
=======

* api-change:``lex-models``: Update lex-models client to latest version
* api-change:``apigatewayv2``: Update apigatewayv2 client to latest version
* api-change:``codebuild``: Update codebuild client to latest version
* api-change:``quicksight``: Update quicksight client to latest version
* api-change:``elbv2``: Update elbv2 client to latest version


1.17.56
=======

* api-change:``workspaces``: Update workspaces client to latest version
* api-change:``xray``: Update xray client to latest version
* api-change:``ssm``: Update ssm client to latest version


1.17.55
=======

* api-change:``stepfunctions``: Update stepfunctions client to latest version
* api-change:``guardduty``: Update guardduty client to latest version
* api-change:``mediapackage``: Update mediapackage client to latest version
* api-change:``kendra``: Update kendra client to latest version


1.17.54
=======

* api-change:``ec2``: Update ec2 client to latest version
* api-change:``macie2``: Update macie2 client to latest version


1.17.53
=======

* api-change:``codeguru-reviewer``: Update codeguru-reviewer client to latest version
* api-change:``securityhub``: Update securityhub client to latest version


1.17.52
=======

* api-change:``sqs``: Update sqs client to latest version
* api-change:``backup``: Update backup client to latest version
* api-change:``cloudfront``: Update cloudfront client to latest version
* api-change:``ec2``: Update ec2 client to latest version


1.17.51
=======

* api-change:``cur``: Update cur client to latest version
* api-change:``route53``: Update route53 client to latest version
* api-change:``cloudfront``: Update cloudfront client to latest version
* api-change:``emr``: Update emr client to latest version


1.17.50
=======

* api-change:``ec2``: Update ec2 client to latest version
* api-change:``redshift``: Update redshift client to latest version
* api-change:``gamelift``: Update gamelift client to latest version
* api-change:``mediaconvert``: Update mediaconvert client to latest version


1.17.49
=======

* api-change:``appflow``: Update appflow client to latest version
* api-change:``route53resolver``: Update route53resolver client to latest version


1.17.48
=======

* api-change:``iotsitewise``: Update iotsitewise client to latest version
* api-change:``xray``: Update xray client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``logs``: Update logs client to latest version
* api-change:``dms``: Update dms client to latest version
* api-change:``ssm``: Update ssm client to latest version
* api-change:``kafka``: Update kafka client to latest version


1.17.47
=======

* api-change:``chime``: Update chime client to latest version
* api-change:``fsx``: Update fsx client to latest version
* api-change:``apigatewayv2``: Update apigatewayv2 client to latest version


1.17.46
=======

* api-change:``lakeformation``: Update lakeformation client to latest version
* api-change:``storagegateway``: Update storagegateway client to latest version
* api-change:``ivs``: Update ivs client to latest version
* api-change:``organizations``: Update organizations client to latest version
* api-change:``servicecatalog``: Update servicecatalog client to latest version


1.17.45
=======

* api-change:``identitystore``: Update identitystore client to latest version
* api-change:``codebuild``: Update codebuild client to latest version
* api-change:``cognito-idp``: Update cognito-idp client to latest version
* api-change:``datasync``: Update datasync client to latest version
* api-change:``sesv2``: Update sesv2 client to latest version
* api-change:``securityhub``: Update securityhub client to latest version


1.17.44
=======

* api-change:``elbv2``: Update elbv2 client to latest version
* api-change:``quicksight``: Update quicksight client to latest version
* api-change:``kinesis``: Update kinesis client to latest version
* api-change:``ecr``: Update ecr client to latest version
* api-change:``acm``: Update acm client to latest version
* api-change:``robomaker``: Update robomaker client to latest version
* api-change:``elb``: Update elb client to latest version
* api-change:``acm-pca``: Update acm-pca client to latest version


1.17.43
=======

* api-change:``braket``: Update braket client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``license-manager``: Update license-manager client to latest version
* api-change:``sagemaker``: Update sagemaker client to latest version
* api-change:``appstream``: Update appstream client to latest version


1.17.42
=======

* api-change:``rds``: Update rds client to latest version
* api-change:``eks``: Update eks client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``macie2``: Update macie2 client to latest version
* api-change:``cognito-idp``: Update cognito-idp client to latest version
* api-change:``appsync``: Update appsync client to latest version
* api-change:``braket``: Update braket client to latest version


1.17.41
=======

* api-change:``transfer``: Update transfer client to latest version
* api-change:``comprehend``: Update comprehend client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``fsx``: Update fsx client to latest version
* api-change:``workspaces``: Update workspaces client to latest version
* api-change:``lambda``: Update lambda client to latest version
* api-change:``iot``: Update iot client to latest version
* api-change:``cloud9``: Update cloud9 client to latest version


1.17.40
=======

* api-change:``organizations``: Update organizations client to latest version
* api-change:``s3``: Update s3 client to latest version
* api-change:``lambda``: Update lambda client to latest version
* api-change:``ec2``: Update ec2 client to latest version


1.17.39
=======

* api-change:``savingsplans``: Update savingsplans client to latest version
* api-change:``glue``: Update glue client to latest version
* api-change:``ec2``: Update ec2 client to latest version


1.17.38
=======

* api-change:``sms``: Update sms client to latest version
* api-change:``organizations``: Update organizations client to latest version
* api-change:``glue``: Update glue client to latest version
* api-change:``s3``: Update s3 client to latest version


1.17.37
=======

* api-change:``lex-runtime``: Update lex-runtime client to latest version
* api-change:``personalize``: Update personalize client to latest version
* api-change:``personalize-runtime``: Update personalize-runtime client to latest version
* api-change:``lex-models``: Update lex-models client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``personalize-events``: Update personalize-events client to latest version


1.17.36
=======

* api-change:``fsx``: Update fsx client to latest version
* api-change:``appsync``: Update appsync client to latest version
* api-change:``sns``: Update sns client to latest version
* api-change:``resourcegroupstaggingapi``: Update resourcegroupstaggingapi client to latest version
* api-change:``transcribe``: Update transcribe client to latest version


1.17.35
=======

* api-change:``health``: Update health client to latest version


1.17.34
=======

* api-change:``ssm``: Update ssm client to latest version


1.17.33
=======

* api-change:``resourcegroupstaggingapi``: Update resourcegroupstaggingapi client to latest version
* api-change:``storagegateway``: Update storagegateway client to latest version
* api-change:``wafv2``: Update wafv2 client to latest version
* api-change:``chime``: Update chime client to latest version
* api-change:``personalize-runtime``: Update personalize-runtime client to latest version


1.17.32
=======

* api-change:``organizations``: Update organizations client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``codebuild``: Update codebuild client to latest version
* api-change:``kafka``: Update kafka client to latest version
* api-change:``servicecatalog``: Update servicecatalog client to latest version
* api-change:``cloudfront``: Update cloudfront client to latest version
* api-change:``resource-groups``: Update resource-groups client to latest version
* api-change:``guardduty``: Update guardduty client to latest version
* api-change:``sesv2``: Update sesv2 client to latest version


1.17.31
=======

* api-change:``resource-groups``: Update resource-groups client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``firehose``: Update firehose client to latest version
* api-change:``servicediscovery``: Update servicediscovery client to latest version
* api-change:``ecr``: Update ecr client to latest version
* api-change:``guardduty``: Update guardduty client to latest version


1.17.30
=======

* api-change:``ec2``: Update ec2 client to latest version
* api-change:``autoscaling``: Update autoscaling client to latest version
* api-change:``securityhub``: Update securityhub client to latest version
* api-change:``ivs``: Update ivs client to latest version
* api-change:``medialive``: Update medialive client to latest version
* api-change:``rds``: Update rds client to latest version
* api-change:``imagebuilder``: Update imagebuilder client to latest version


1.17.29
=======

* api-change:``glue``: Update glue client to latest version
* api-change:``datasync``: Update datasync client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``frauddetector``: Update frauddetector client to latest version
* api-change:``ssm``: Update ssm client to latest version
* api-change:``dms``: Update dms client to latest version


1.17.28
=======

* api-change:``mediaconnect``: Update mediaconnect client to latest version
* api-change:``sagemaker``: Update sagemaker client to latest version
* api-change:``kendra``: Update kendra client to latest version
* api-change:``fsx``: Update fsx client to latest version
* api-change:``frauddetector``: Update frauddetector client to latest version
* api-change:``mediapackage``: Update mediapackage client to latest version
* api-change:``macie2``: Update macie2 client to latest version
* api-change:``cloudwatch``: Update cloudwatch client to latest version
* api-change:``mq``: Update mq client to latest version


1.17.27
=======

* api-change:``directconnect``: Update directconnect client to latest version
* api-change:``config``: Update config client to latest version
* api-change:``fsx``: Update fsx client to latest version
* api-change:``glue``: Update glue client to latest version
* api-change:``workspaces``: Update workspaces client to latest version
* api-change:``lightsail``: Update lightsail client to latest version


1.17.26
=======

* api-change:``quicksight``: Update quicksight client to latest version
* api-change:``medialive``: Update medialive client to latest version


1.17.25
=======

* api-change:``codeguruprofiler``: Update codeguruprofiler client to latest version


1.17.24
=======

* api-change:``frauddetector``: Update frauddetector client to latest version
* api-change:``rds``: Update rds client to latest version
* api-change:``codebuild``: Update codebuild client to latest version
* api-change:``groundstation``: Update groundstation client to latest version
* api-change:``fms``: Update fms client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``cloudfront``: Update cloudfront client to latest version


1.17.23
=======

* api-change:``connect``: Update connect client to latest version
* api-change:``elasticbeanstalk``: Update elasticbeanstalk client to latest version
* api-change:``appsync``: Update appsync client to latest version
* api-change:``macie2``: Update macie2 client to latest version
* api-change:``application-autoscaling``: Update application-autoscaling client to latest version
* api-change:``ec2``: Update ec2 client to latest version


1.17.22
=======

* enhancement:examples: Pull in latest examples from EFS.


1.17.21
=======

* api-change:``ivs``: Update ivs client to latest version


1.17.20
=======

* api-change:``amplify``: Update amplify client to latest version
* api-change:``wafv2``: Update wafv2 client to latest version
* api-change:``ebs``: Update ebs client to latest version
* api-change:``events``: Update events client to latest version
* api-change:``sagemaker``: Update sagemaker client to latest version
* api-change:``cloudhsmv2``: Update cloudhsmv2 client to latest version
* api-change:``appmesh``: Update appmesh client to latest version
* api-change:``alexaforbusiness``: Update alexaforbusiness client to latest version
* api-change:``sns``: Update sns client to latest version
* api-change:``secretsmanager``: Update secretsmanager client to latest version
* api-change:``comprehend``: Update comprehend client to latest version


1.17.19
=======

* api-change:``ec2``: Update ec2 client to latest version
* api-change:``forecast``: Update forecast client to latest version
* api-change:``ce``: Update ce client to latest version
* api-change:``organizations``: Update organizations client to latest version


1.17.18
=======

* api-change:``storagegateway``: Update storagegateway client to latest version
* api-change:``glue``: Update glue client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``lakeformation``: Update lakeformation client to latest version
* api-change:``efs``: Update efs client to latest version
* api-change:``cloudfront``: Update cloudfront client to latest version


1.17.17
=======

* api-change:``quicksight``: Update quicksight client to latest version
* api-change:``rds``: Update rds client to latest version
* api-change:``iotsitewise``: Update iotsitewise client to latest version


1.17.16
=======

* api-change:``elasticache``: Update elasticache client to latest version
* api-change:``connect``: Update connect client to latest version


1.17.15
=======

* api-change:``imagebuilder``: Update imagebuilder client to latest version
* api-change:``appsync``: Update appsync client to latest version
* api-change:``chime``: Update chime client to latest version
* api-change:``rds``: Update rds client to latest version
* api-change:``securityhub``: Update securityhub client to latest version
* api-change:``codebuild``: Update codebuild client to latest version


1.17.14
=======

* api-change:``ecr``: Update ecr client to latest version
* api-change:``codeguru-reviewer``: Update codeguru-reviewer client to latest version
* api-change:``comprehendmedical``: Update comprehendmedical client to latest version
* api-change:``rds``: Update rds client to latest version
* api-change:``ec2``: Update ec2 client to latest version


1.17.13
=======

* api-change:``codestar-connections``: Update codestar-connections client to latest version
* api-change:``codeguruprofiler``: Update codeguruprofiler client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``autoscaling``: Update autoscaling client to latest version


1.17.12
=======

* api-change:``quicksight``: Update quicksight client to latest version
* api-change:``cognito-idp``: Update cognito-idp client to latest version
* api-change:``sagemaker``: Update sagemaker client to latest version
* api-change:``cloudformation``: Update cloudformation client to latest version
* api-change:``dms``: Update dms client to latest version


1.17.11
=======

* api-change:``glue``: Update glue client to latest version
* api-change:``ec2``: Update ec2 client to latest version


1.17.10
=======

* api-change:``iam``: Update iam client to latest version
* api-change:``organizations``: Update organizations client to latest version
* api-change:``backup``: Update backup client to latest version
* api-change:``emr``: Update emr client to latest version
* api-change:``fsx``: Update fsx client to latest version
* api-change:``amplify``: Update amplify client to latest version
* api-change:``codecommit``: Update codecommit client to latest version
* api-change:``honeycode``: Update honeycode client to latest version
* api-change:``autoscaling``: Update autoscaling client to latest version


1.17.9
======

* api-change:``mediatailor``: Update mediatailor client to latest version
* api-change:``organizations``: Update organizations client to latest version


1.17.8
======

* api-change:``ec2``: Update ec2 client to latest version
* api-change:``emr``: Update emr client to latest version
* api-change:``rekognition``: Update rekognition client to latest version
* api-change:``rds``: Update rds client to latest version
* api-change:``sqs``: Update sqs client to latest version


1.17.7
======

* api-change:``elasticache``: Update elasticache client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``opsworkscm``: Update opsworkscm client to latest version
* api-change:``medialive``: Update medialive client to latest version


1.17.6
======

* api-change:``support``: Update support client to latest version
* api-change:``mediaconvert``: Update mediaconvert client to latest version
* api-change:``meteringmarketplace``: Update meteringmarketplace client to latest version
* api-change:``route53``: Update route53 client to latest version
* api-change:``ssm``: Update ssm client to latest version
* api-change:``rds``: Update rds client to latest version
* api-change:``sesv2``: Update sesv2 client to latest version


1.17.5
======

* api-change:``ec2``: Update ec2 client to latest version
* api-change:``snowball``: Update snowball client to latest version
* api-change:``appmesh``: Update appmesh client to latest version
* api-change:``route53``: Update route53 client to latest version
* api-change:``macie2``: Update macie2 client to latest version


1.17.4
======

* api-change:``cloudfront``: Update cloudfront client to latest version
* api-change:``dataexchange``: Update dataexchange client to latest version
* api-change:``qldb``: Update qldb client to latest version
* api-change:``autoscaling``: Update autoscaling client to latest version
* api-change:``lambda``: Update lambda client to latest version
* api-change:``polly``: Update polly client to latest version


1.17.3
======

* api-change:``chime``: Update chime client to latest version
* api-change:``appconfig``: Update appconfig client to latest version
* api-change:``alexaforbusiness``: Update alexaforbusiness client to latest version
* api-change:``cognito-idp``: Update cognito-idp client to latest version
* api-change:``iot``: Update iot client to latest version


1.17.2
======

* api-change:``apigateway``: Update apigateway client to latest version
* api-change:``glue``: Update glue client to latest version
* api-change:``cloudformation``: Update cloudformation client to latest version
* api-change:``storagegateway``: Update storagegateway client to latest version


1.17.1
======

* api-change:``lex-models``: Update lex-models client to latest version
* api-change:``imagebuilder``: Update imagebuilder client to latest version
* api-change:``iot-data``: Update iot-data client to latest version
* api-change:``ecs``: Update ecs client to latest version


1.17.0
======

* api-change:``macie2``: Update macie2 client to latest version
* api-change:``servicecatalog``: Update servicecatalog client to latest version
* api-change:``codeartifact``: Update codeartifact client to latest version
* api-change:``compute-optimizer``: Update compute-optimizer client to latest version
* api-change:``shield``: Update shield client to latest version
* api-change:``lightsail``: Update lightsail client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``appconfig``: Update appconfig client to latest version
* feature:SSO: Added support for the SSO credential provider. This allows the SDK to retrieve temporary AWS credentials from a profile configured to use SSO credentials.
* api-change:``dlm``: Update dlm client to latest version


1.16.26
=======

* api-change:``transfer``: Update transfer client to latest version


1.16.25
=======

* api-change:``shield``: Update shield client to latest version
* api-change:``servicediscovery``: Update servicediscovery client to latest version


1.16.24
=======

* api-change:``cloudfront``: Update cloudfront client to latest version
* api-change:``pinpoint``: Update pinpoint client to latest version
* api-change:``personalize-runtime``: Update personalize-runtime client to latest version
* api-change:``sagemaker-runtime``: Update sagemaker-runtime client to latest version
* api-change:``elasticbeanstalk``: Update elasticbeanstalk client to latest version
* api-change:``servicecatalog``: Update servicecatalog client to latest version
* api-change:``apigateway``: Update apigateway client to latest version
* api-change:``personalize``: Update personalize client to latest version


1.16.23
=======

* api-change:``ssm``: Update ssm client to latest version
* api-change:``lightsail``: Update lightsail client to latest version
* api-change:``meteringmarketplace``: Update meteringmarketplace client to latest version
* api-change:``mediapackage-vod``: Update mediapackage-vod client to latest version
* api-change:``ec2``: Update ec2 client to latest version


1.16.22
=======

* api-change:``elasticache``: Update elasticache client to latest version
* api-change:``iam``: Update iam client to latest version
* api-change:``directconnect``: Update directconnect client to latest version
* api-change:``es``: Update es client to latest version
* api-change:``glue``: Update glue client to latest version
* api-change:``mediaconvert``: Update mediaconvert client to latest version


1.16.21
=======

* api-change:``guardduty``: Update guardduty client to latest version


1.16.20
=======

* api-change:``fsx``: Update fsx client to latest version
* api-change:``kms``: Update kms client to latest version
* api-change:``sagemaker``: Update sagemaker client to latest version
* api-change:``athena``: Update athena client to latest version
* api-change:``worklink``: Update worklink client to latest version
* api-change:``emr``: Update emr client to latest version


1.16.19
=======

* api-change:``marketplace-catalog``: Update marketplace-catalog client to latest version
* api-change:``kafka``: Update kafka client to latest version
* api-change:``qldb-session``: Update qldb-session client to latest version
* api-change:``workmail``: Update workmail client to latest version


1.16.18
=======

* api-change:``guardduty``: Update guardduty client to latest version
* api-change:``elbv2``: Update elbv2 client to latest version


1.16.17
=======

* api-change:``elasticache``: Update elasticache client to latest version
* api-change:``dlm``: Update dlm client to latest version
* api-change:``quicksight``: Update quicksight client to latest version
* api-change:``ssm``: Update ssm client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``macie``: Update macie client to latest version


1.16.16
=======

* api-change:``autoscaling``: Update autoscaling client to latest version
* api-change:``iotsitewise``: Update iotsitewise client to latest version


1.16.15
=======

* api-change:``synthetics``: Update synthetics client to latest version
* api-change:``codebuild``: Update codebuild client to latest version
* api-change:``s3``: Update s3 client to latest version
* api-change:``ec2``: Update ec2 client to latest version


1.16.14
=======

* api-change:``backup``: Update backup client to latest version
* api-change:``codedeploy``: Update codedeploy client to latest version
* api-change:``securityhub``: Update securityhub client to latest version
* api-change:``chime``: Update chime client to latest version
* api-change:``medialive``: Update medialive client to latest version
* api-change:``application-autoscaling``: Update application-autoscaling client to latest version
* api-change:``appmesh``: Update appmesh client to latest version


1.16.13
=======

* api-change:``transcribe``: Update transcribe client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``health``: Update health client to latest version
* api-change:``chime``: Update chime client to latest version


1.16.12
=======

* api-change:``chime``: Update chime client to latest version
* api-change:``qldb``: Update qldb client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``ecs``: Update ecs client to latest version
* api-change:``dynamodb``: Update dynamodb client to latest version
* api-change:``macie2``: Update macie2 client to latest version


1.16.11
=======

* api-change:``sts``: Update sts client to latest version
* api-change:``ecr``: Update ecr client to latest version
* api-change:``glue``: Update glue client to latest version
* api-change:``cloudformation``: Update cloudformation client to latest version


1.16.10
=======

* api-change:``ec2``: Update ec2 client to latest version
* api-change:``imagebuilder``: Update imagebuilder client to latest version


1.16.9
======

* api-change:``elasticache``: Update elasticache client to latest version
* api-change:``macie2``: Update macie2 client to latest version


1.16.8
======

* api-change:``workmail``: Update workmail client to latest version
* api-change:``iotsitewise``: Update iotsitewise client to latest version
* enchancement:Endpoints: Improved endpoint resolution for clients with unknown regions


1.16.7
======

* api-change:``kendra``: Update kendra client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``codeguru-reviewer``: Update codeguru-reviewer client to latest version


1.16.6
======

* api-change:``sagemaker``: Update sagemaker client to latest version
* api-change:``guardduty``: Update guardduty client to latest version
* api-change:``resourcegroupstaggingapi``: Update resourcegroupstaggingapi client to latest version


1.16.5
======

* api-change:``ssm``: Update ssm client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``codebuild``: Update codebuild client to latest version
* api-change:``lightsail``: Update lightsail client to latest version
* api-change:``route53``: Update route53 client to latest version
* api-change:``appconfig``: Update appconfig client to latest version
* api-change:``logs``: Update logs client to latest version


1.16.4
======

* api-change:``codestar-connections``: Update codestar-connections client to latest version
* api-change:``comprehendmedical``: Update comprehendmedical client to latest version


1.16.3
======

* api-change:``support``: Update support client to latest version
* api-change:``ssm``: Update ssm client to latest version
* api-change:``ec2``: Update ec2 client to latest version


1.16.2
======

* api-change:``apigateway``: Update apigateway client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``s3control``: Update s3control client to latest version


1.16.1
======

* api-change:``efs``: Update efs client to latest version
* api-change:``ssm``: Update ssm client to latest version


1.16.0
======

* api-change:``schemas``: Update schemas client to latest version
* api-change:``iot``: Update iot client to latest version
* api-change:``lambda``: Update lambda client to latest version
* api-change:``storagegateway``: Update storagegateway client to latest version
* api-change:``iotevents``: Update iotevents client to latest version
* feature:Exceptions: Added support for parsing modeled exception fields.
* api-change:``mediaconvert``: Update mediaconvert client to latest version


1.15.49
=======

* api-change:``iotsitewise``: Update iotsitewise client to latest version
* api-change:``waf``: Update waf client to latest version
* api-change:``waf-regional``: Update waf-regional client to latest version
* api-change:``transcribe``: Update transcribe client to latest version
* api-change:``servicediscovery``: Update servicediscovery client to latest version


1.15.48
=======

* api-change:``kinesisvideo``: Update kinesisvideo client to latest version
* api-change:``kinesis-video-archived-media``: Update kinesis-video-archived-media client to latest version
* api-change:``ssm``: Update ssm client to latest version
* api-change:``route53``: Update route53 client to latest version
* api-change:``ecr``: Update ecr client to latest version
* api-change:``medialive``: Update medialive client to latest version


1.15.47
=======

* api-change:``dms``: Update dms client to latest version
* api-change:``dataexchange``: Update dataexchange client to latest version
* api-change:``accessanalyzer``: Update accessanalyzer client to latest version
* api-change:``sagemaker``: Update sagemaker client to latest version


1.15.46
=======

* api-change:``iot``: Update iot client to latest version
* api-change:``dlm``: Update dlm client to latest version
* api-change:``elastic-inference``: Update elastic-inference client to latest version


1.15.45
=======

* api-change:``mediapackage-vod``: Update mediapackage-vod client to latest version
* api-change:``application-autoscaling``: Update application-autoscaling client to latest version
* api-change:``storagegateway``: Update storagegateway client to latest version
* api-change:``rds``: Update rds client to latest version
* api-change:``ram``: Update ram client to latest version
* api-change:``pinpoint``: Update pinpoint client to latest version
* api-change:``transfer``: Update transfer client to latest version
* api-change:``firehose``: Update firehose client to latest version


1.15.44
=======

* api-change:``codeguru-reviewer``: Update codeguru-reviewer client to latest version
* api-change:``redshift``: Update redshift client to latest version
* api-change:``es``: Update es client to latest version
* api-change:``fms``: Update fms client to latest version


1.15.43
=======

* api-change:``route53domains``: Update route53domains client to latest version
* api-change:``guardduty``: Update guardduty client to latest version
* api-change:``ce``: Update ce client to latest version
* api-change:``emr``: Update emr client to latest version


1.15.42
=======

* api-change:``ce``: Update ce client to latest version
* api-change:``glue``: Update glue client to latest version
* api-change:``synthetics``: Update synthetics client to latest version
* api-change:``apigatewayv2``: Update apigatewayv2 client to latest version
* api-change:``iotevents``: Update iotevents client to latest version


1.15.41
=======

* api-change:``opsworkscm``: Update opsworkscm client to latest version
* api-change:``frauddetector``: Update frauddetector client to latest version


1.15.40
=======

* api-change:``iotevents``: Update iotevents client to latest version
* api-change:``imagebuilder``: Update imagebuilder client to latest version
* api-change:``securityhub``: Update securityhub client to latest version
* api-change:``rds``: Update rds client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``sagemaker-a2i-runtime``: Update sagemaker-a2i-runtime client to latest version
* api-change:``sagemaker``: Update sagemaker client to latest version
* api-change:``snowball``: Update snowball client to latest version
* api-change:``lambda``: Update lambda client to latest version
* api-change:``mgh``: Update mgh client to latest version
* api-change:``mediatailor``: Update mediatailor client to latest version
* api-change:``mediaconvert``: Update mediaconvert client to latest version
* api-change:``glue``: Update glue client to latest version


1.15.39
=======

* api-change:``ecs``: Update ecs client to latest version
* api-change:``cloudformation``: Update cloudformation client to latest version
* api-change:``chime``: Update chime client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``codeguruprofiler``: Update codeguruprofiler client to latest version
* api-change:``mediaconvert``: Update mediaconvert client to latest version
* api-change:``migrationhub-config``: Update migrationhub-config client to latest version


1.15.38
=======

* api-change:``apigateway``: Update apigateway client to latest version
* api-change:``codeguru-reviewer``: Update codeguru-reviewer client to latest version
* api-change:``mediaconnect``: Update mediaconnect client to latest version


1.15.37
=======

* api-change:``transcribe``: Update transcribe client to latest version
* api-change:``chime``: Update chime client to latest version
* api-change:``iam``: Update iam client to latest version
* api-change:``elasticbeanstalk``: Update elasticbeanstalk client to latest version


1.15.36
=======

* api-change:``personalize-runtime``: Update personalize-runtime client to latest version
* api-change:``robomaker``: Update robomaker client to latest version


1.15.35
=======

* api-change:``medialive``: Update medialive client to latest version
* api-change:``redshift``: Update redshift client to latest version
* api-change:``gamelift``: Update gamelift client to latest version
* api-change:``cloudwatch``: Update cloudwatch client to latest version
* api-change:``rds``: Update rds client to latest version


1.15.34
=======

* api-change:``iot``: Update iot client to latest version
* api-change:``mediaconnect``: Update mediaconnect client to latest version


1.15.33
=======

* api-change:``opsworkscm``: Update opsworkscm client to latest version
* api-change:``wafv2``: Update wafv2 client to latest version
* api-change:``glue``: Update glue client to latest version
* api-change:``elastic-inference``: Update elastic-inference client to latest version
* api-change:``lambda``: Update lambda client to latest version
* api-change:``mediastore``: Update mediastore client to latest version
* api-change:``pinpoint``: Update pinpoint client to latest version
* api-change:``storagegateway``: Update storagegateway client to latest version
* api-change:``rekognition``: Update rekognition client to latest version
* api-change:``fms``: Update fms client to latest version
* api-change:``organizations``: Update organizations client to latest version
* api-change:``detective``: Update detective client to latest version
* api-change:``appconfig``: Update appconfig client to latest version


1.15.32
=======

* api-change:``accessanalyzer``: Update accessanalyzer client to latest version


1.15.31
=======

* api-change:``globalaccelerator``: Update globalaccelerator client to latest version
* api-change:``kendra``: Update kendra client to latest version
* api-change:``servicecatalog``: Update servicecatalog client to latest version


1.15.30
=======

* api-change:``sagemaker``: Update sagemaker client to latest version
* api-change:``fsx``: Update fsx client to latest version
* api-change:``securityhub``: Update securityhub client to latest version


1.15.29
=======

* api-change:``managedblockchain``: Update managedblockchain client to latest version
* api-change:``ce``: Update ce client to latest version
* api-change:``application-insights``: Update application-insights client to latest version
* api-change:``detective``: Update detective client to latest version
* api-change:``es``: Update es client to latest version
* api-change:``xray``: Update xray client to latest version


1.15.28
=======

* api-change:``athena``: Update athena client to latest version
* api-change:``rds-data``: Update rds-data client to latest version
* api-change:``eks``: Update eks client to latest version
* api-change:``organizations``: Update organizations client to latest version


1.15.27
=======

* api-change:``apigatewayv2``: Update apigatewayv2 client to latest version
* api-change:``eks``: Update eks client to latest version
* api-change:``route53``: Update route53 client to latest version


1.15.26
=======

* api-change:``servicecatalog``: Update servicecatalog client to latest version


1.15.25
=======

* api-change:``outposts``: Update outposts client to latest version
* api-change:``acm``: Update acm client to latest version


1.15.24
=======

* api-change:``rds``: Update rds client to latest version
* api-change:``mediaconnect``: Update mediaconnect client to latest version
* api-change:``personalize``: Update personalize client to latest version


1.15.23
=======

* api-change:``mediaconvert``: Update mediaconvert client to latest version


1.15.22
=======

* api-change:``s3control``: Update s3control client to latest version
* bugfix:Stubber: fixes `#1884 <https://github.com/boto/botocore/issues/1884>`__
* api-change:``cognito-idp``: Update cognito-idp client to latest version
* api-change:``ssm``: Update ssm client to latest version
* api-change:``ecs``: Update ecs client to latest version
* api-change:``elasticache``: Update elasticache client to latest version


1.15.21
=======

* api-change:``appconfig``: Update appconfig client to latest version


1.15.20
=======

* api-change:``lex-models``: Update lex-models client to latest version
* api-change:``securityhub``: Update securityhub client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``apigatewayv2``: Update apigatewayv2 client to latest version
* api-change:``iot``: Update iot client to latest version


1.15.19
=======

* api-change:``efs``: Update efs client to latest version
* api-change:``redshift``: Update redshift client to latest version


1.15.18
=======

* api-change:``serverlessrepo``: Update serverlessrepo client to latest version
* api-change:``iotevents``: Update iotevents client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* enhancement:timezones: Improved timezone parsing for Windows with new fallback method (#1939)
* api-change:``marketplacecommerceanalytics``: Update marketplacecommerceanalytics client to latest version


1.15.17
=======

* api-change:``ec2``: Update ec2 client to latest version
* api-change:``medialive``: Update medialive client to latest version
* api-change:``dms``: Update dms client to latest version


1.15.16
=======

* api-change:``signer``: Update signer client to latest version
* api-change:``guardduty``: Update guardduty client to latest version
* api-change:``appmesh``: Update appmesh client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``robomaker``: Update robomaker client to latest version


1.15.15
=======

* api-change:``eks``: Update eks client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``opsworkscm``: Update opsworkscm client to latest version
* api-change:``guardduty``: Update guardduty client to latest version


1.15.14
=======

* api-change:``pinpoint``: Update pinpoint client to latest version


1.15.13
=======

* api-change:``ec2``: Update ec2 client to latest version


1.15.12
=======

* api-change:``cloudwatch``: Update cloudwatch client to latest version
* api-change:``comprehendmedical``: Update comprehendmedical client to latest version


1.15.11
=======

* api-change:``config``: Update config client to latest version


1.15.10
=======

* api-change:``config``: Update config client to latest version
* api-change:``glue``: Update glue client to latest version
* api-change:``sagemaker-a2i-runtime``: Update sagemaker-a2i-runtime client to latest version
* api-change:``appmesh``: Update appmesh client to latest version
* api-change:``elbv2``: Update elbv2 client to latest version
* api-change:``workdocs``: Update workdocs client to latest version
* api-change:``quicksight``: Update quicksight client to latest version
* api-change:``accessanalyzer``: Update accessanalyzer client to latest version
* api-change:``codeguruprofiler``: Update codeguruprofiler client to latest version


1.15.9
======

* api-change:``lightsail``: Update lightsail client to latest version
* api-change:``globalaccelerator``: Update globalaccelerator client to latest version


1.15.8
======

* api-change:``transcribe``: Update transcribe client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``sagemaker``: Update sagemaker client to latest version
* api-change:``securityhub``: Update securityhub client to latest version


1.15.7
======

* api-change:``stepfunctions``: Update stepfunctions client to latest version
* api-change:``kafka``: Update kafka client to latest version
* api-change:``secretsmanager``: Update secretsmanager client to latest version
* api-change:``outposts``: Update outposts client to latest version


1.15.6
======

* api-change:``iotevents``: Update iotevents client to latest version
* api-change:``docdb``: Update docdb client to latest version
* api-change:``snowball``: Update snowball client to latest version
* api-change:``fsx``: Update fsx client to latest version
* api-change:``events``: Update events client to latest version


1.15.5
======

* api-change:``imagebuilder``: Update imagebuilder client to latest version
* api-change:``wafv2``: Update wafv2 client to latest version
* api-change:``redshift``: Update redshift client to latest version


1.15.4
======

* api-change:``savingsplans``: Update savingsplans client to latest version
* api-change:``appconfig``: Update appconfig client to latest version
* api-change:``pinpoint``: Update pinpoint client to latest version


1.15.3
======

* api-change:``autoscaling``: Update autoscaling client to latest version
* api-change:``servicecatalog``: Update servicecatalog client to latest version
* api-change:``lambda``: Update lambda client to latest version


1.15.2
======

* api-change:``autoscaling``: Update autoscaling client to latest version
* api-change:``chime``: Update chime client to latest version
* api-change:``rds``: Update rds client to latest version


1.15.1
======

* api-change:``cloud9``: Update cloud9 client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``dynamodb``: Update dynamodb client to latest version
* api-change:``rekognition``: Update rekognition client to latest version


1.15.0
======

* feature:retries: Add support for retry modes, including ``standard`` and ``adaptive`` modes (`#1972 <https://github.com/boto/botocore/issues/1972>`__)
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``mediatailor``: Update mediatailor client to latest version
* api-change:``securityhub``: Update securityhub client to latest version
* api-change:``shield``: Update shield client to latest version


1.14.17
=======

* api-change:``mediapackage-vod``: Update mediapackage-vod client to latest version


1.14.16
=======

* api-change:``glue``: Update glue client to latest version
* api-change:``chime``: Update chime client to latest version
* api-change:``workmail``: Update workmail client to latest version
* api-change:``ds``: Update ds client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``es``: Update es client to latest version
* api-change:``neptune``: Update neptune client to latest version


1.14.15
=======

* api-change:``ec2``: Update ec2 client to latest version
* api-change:``cognito-idp``: Update cognito-idp client to latest version
* api-change:``cloudformation``: Update cloudformation client to latest version


1.14.14
=======

* api-change:``docdb``: Update docdb client to latest version
* api-change:``kms``: Update kms client to latest version


1.14.13
=======

* api-change:``robomaker``: Update robomaker client to latest version
* api-change:``imagebuilder``: Update imagebuilder client to latest version
* api-change:``rds``: Update rds client to latest version


1.14.12
=======

* api-change:``ebs``: Update ebs client to latest version
* api-change:``appsync``: Update appsync client to latest version
* api-change:``lex-models``: Update lex-models client to latest version
* api-change:``ecr``: Update ecr client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``codebuild``: Update codebuild client to latest version


1.14.11
=======

* api-change:``groundstation``: Update groundstation client to latest version
* api-change:``mediaconvert``: Update mediaconvert client to latest version
* api-change:``dlm``: Update dlm client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``forecastquery``: Update forecastquery client to latest version
* api-change:``securityhub``: Update securityhub client to latest version
* api-change:``resourcegroupstaggingapi``: Update resourcegroupstaggingapi client to latest version


1.14.10
=======

* api-change:``workmail``: Update workmail client to latest version
* api-change:``iot``: Update iot client to latest version
* api-change:``cloudfront``: Update cloudfront client to latest version
* api-change:``storagegateway``: Update storagegateway client to latest version
* api-change:``ssm``: Update ssm client to latest version
* api-change:``kafka``: Update kafka client to latest version
* api-change:``ec2``: Update ec2 client to latest version


1.14.9
======

* api-change:``ecs``: Update ecs client to latest version
* api-change:``opsworkscm``: Update opsworkscm client to latest version
* api-change:``workspaces``: Update workspaces client to latest version
* api-change:``datasync``: Update datasync client to latest version
* api-change:``eks``: Update eks client to latest version


1.14.8
======

* api-change:``rds``: Update rds client to latest version
* api-change:``iam``: Update iam client to latest version


1.14.7
======

* api-change:``ec2``: Update ec2 client to latest version
* api-change:``codepipeline``: Update codepipeline client to latest version
* api-change:``discovery``: Update discovery client to latest version
* api-change:``iotevents``: Update iotevents client to latest version
* api-change:``marketplacecommerceanalytics``: Update marketplacecommerceanalytics client to latest version


1.14.6
======

* api-change:``lambda``: Update lambda client to latest version
* api-change:``application-insights``: Update application-insights client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``cloudwatch``: Update cloudwatch client to latest version
* api-change:``kms``: Update kms client to latest version
* api-change:``alexaforbusiness``: Update alexaforbusiness client to latest version


1.14.5
======

* api-change:``mediaconvert``: Update mediaconvert client to latest version
* api-change:``neptune``: Update neptune client to latest version
* api-change:``cloudhsmv2``: Update cloudhsmv2 client to latest version
* api-change:``redshift``: Update redshift client to latest version
* api-change:``batch``: Update batch client to latest version
* api-change:``ecs``: Update ecs client to latest version


1.14.4
======

* api-change:``ec2``: Update ec2 client to latest version
* api-change:``sagemaker``: Update sagemaker client to latest version
* api-change:``ds``: Update ds client to latest version


1.14.3
======

* api-change:``securityhub``: Update securityhub client to latest version
* api-change:``ssm``: Update ssm client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``organizations``: Update organizations client to latest version


1.14.2
======

* api-change:``ec2``: Update ec2 client to latest version


1.14.1
======

* api-change:``efs``: Update efs client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``backup``: Update backup client to latest version


1.14.0
======

* api-change:``sagemaker``: Update sagemaker client to latest version
* api-change:``chime``: Update chime client to latest version
* api-change:``transfer``: Update transfer client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* feature:Python: Dropped support for Python 2.6 and 3.3.
* api-change:``workspaces``: Update workspaces client to latest version
* api-change:``rds``: Update rds client to latest version


1.13.50
=======

* api-change:``logs``: Update logs client to latest version


1.13.49
=======

* api-change:``fms``: Update fms client to latest version
* api-change:``translate``: Update translate client to latest version
* api-change:``ce``: Update ce client to latest version


1.13.48
=======

* api-change:``codebuild``: Update codebuild client to latest version
* api-change:``mgh``: Update mgh client to latest version
* api-change:``xray``: Update xray client to latest version


1.13.47
=======

* api-change:``comprehend``: Update comprehend client to latest version
* api-change:``mediapackage``: Update mediapackage client to latest version
* api-change:``ec2``: Update ec2 client to latest version


1.13.46
=======

* api-change:``lex-models``: Update lex-models client to latest version
* api-change:``ecr``: Update ecr client to latest version
* api-change:``lightsail``: Update lightsail client to latest version
* api-change:``ce``: Update ce client to latest version


1.13.45
=======

* api-change:``fsx``: Update fsx client to latest version
* api-change:``health``: Update health client to latest version
* api-change:``detective``: Update detective client to latest version


1.13.44
=======

* api-change:``transcribe``: Update transcribe client to latest version
* api-change:``eks``: Update eks client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``rds``: Update rds client to latest version
* api-change:``ssm``: Update ssm client to latest version
* api-change:``redshift``: Update redshift client to latest version
* api-change:``pinpoint``: Update pinpoint client to latest version
* api-change:``securityhub``: Update securityhub client to latest version
* api-change:``devicefarm``: Update devicefarm client to latest version


1.13.43
=======

* api-change:``transcribe``: Update transcribe client to latest version
* api-change:``dlm``: Update dlm client to latest version
* api-change:``lex-models``: Update lex-models client to latest version
* api-change:``personalize-runtime``: Update personalize-runtime client to latest version
* api-change:``ssm``: Update ssm client to latest version
* api-change:``codestar-connections``: Update codestar-connections client to latest version
* api-change:``gamelift``: Update gamelift client to latest version
* api-change:``ec2``: Update ec2 client to latest version


1.13.42
=======

* api-change:``ec2``: Update ec2 client to latest version
* api-change:``s3``: Update s3 client to latest version
* api-change:``resourcegroupstaggingapi``: Update resourcegroupstaggingapi client to latest version
* api-change:``cloudfront``: Update cloudfront client to latest version
* enhancement:``s3``: Add support for opting into using the us-east-1 regional endpoint.
* api-change:``opsworkscm``: Update opsworkscm client to latest version


1.13.41
=======

* api-change:``kinesisanalyticsv2``: Update kinesisanalyticsv2 client to latest version
* api-change:``ssm``: Update ssm client to latest version
* api-change:``medialive``: Update medialive client to latest version
* api-change:``iot``: Update iot client to latest version
* api-change:``ecs``: Update ecs client to latest version
* api-change:``ec2``: Update ec2 client to latest version


1.13.40
=======

* api-change:``mq``: Update mq client to latest version
* api-change:``comprehendmedical``: Update comprehendmedical client to latest version
* api-change:``ec2``: Update ec2 client to latest version


1.13.39
=======

* api-change:``codebuild``: Update codebuild client to latest version
* api-change:``detective``: Update detective client to latest version
* api-change:``sesv2``: Update sesv2 client to latest version


1.13.38
=======

* api-change:``accessanalyzer``: Update accessanalyzer client to latest version


1.13.37
=======

* api-change:``ec2``: Update ec2 client to latest version


1.13.36
=======

* api-change:``kendra``: Update kendra client to latest version


1.13.35
=======

* bugfix:s3: Add stricter validation to s3 control account id parameter.
* api-change:``quicksight``: Update quicksight client to latest version
* api-change:``kms``: Update kms client to latest version
* api-change:``ssm``: Update ssm client to latest version
* api-change:``kafka``: Update kafka client to latest version


1.13.34
=======

* bugfix:s3: Fixed an issue where the request path was set incorrectly if access point name was present in key path.


1.13.33
=======

* api-change:``kinesisvideo``: Update kinesisvideo client to latest version
* api-change:``kinesis-video-signaling``: Update kinesis-video-signaling client to latest version
* api-change:``apigatewayv2``: Update apigatewayv2 client to latest version


1.13.32
=======

* api-change:``ebs``: Update ebs client to latest version
* api-change:``stepfunctions``: Update stepfunctions client to latest version
* api-change:``application-autoscaling``: Update application-autoscaling client to latest version
* api-change:``lambda``: Update lambda client to latest version
* api-change:``rekognition``: Update rekognition client to latest version
* api-change:``rds``: Update rds client to latest version
* api-change:``sagemaker``: Update sagemaker client to latest version


1.13.31
=======

* api-change:``textract``: Update textract client to latest version
* api-change:``s3control``: Update s3control client to latest version
* api-change:``ecs``: Update ecs client to latest version
* api-change:``s3``: Update s3 client to latest version
* api-change:``outposts``: Update outposts client to latest version
* api-change:``kendra``: Update kendra client to latest version
* api-change:``eks``: Update eks client to latest version
* api-change:``networkmanager``: Update networkmanager client to latest version
* api-change:``compute-optimizer``: Update compute-optimizer client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``frauddetector``: Update frauddetector client to latest version
* api-change:``sagemaker-a2i-runtime``: Update sagemaker-a2i-runtime client to latest version
* api-change:``codeguru-reviewer``: Update codeguru-reviewer client to latest version
* api-change:``codeguruprofiler``: Update codeguruprofiler client to latest version
* api-change:``es``: Update es client to latest version


1.13.30
=======

* api-change:``accessanalyzer``: Update accessanalyzer client to latest version


1.13.29
=======

* api-change:``ec2``: Update ec2 client to latest version
* api-change:``license-manager``: Update license-manager client to latest version
* api-change:``imagebuilder``: Update imagebuilder client to latest version
* api-change:``schemas``: Update schemas client to latest version


1.13.28
=======

* api-change:``rds-data``: Update rds-data client to latest version
* api-change:``ds``: Update ds client to latest version
* api-change:``workspaces``: Update workspaces client to latest version
* api-change:``resourcegroupstaggingapi``: Update resourcegroupstaggingapi client to latest version
* api-change:``cognito-idp``: Update cognito-idp client to latest version
* api-change:``dynamodb``: Update dynamodb client to latest version
* api-change:``elastic-inference``: Update elastic-inference client to latest version
* api-change:``organizations``: Update organizations client to latest version
* api-change:``mediatailor``: Update mediatailor client to latest version
* api-change:``quicksight``: Update quicksight client to latest version
* api-change:``serverlessrepo``: Update serverlessrepo client to latest version


1.13.27
=======

* api-change:``cognito-idp``: Update cognito-idp client to latest version
* api-change:``redshift``: Update redshift client to latest version
* api-change:``elbv2``: Update elbv2 client to latest version
* api-change:``wafv2``: Update wafv2 client to latest version
* api-change:``dlm``: Update dlm client to latest version
* api-change:``iot``: Update iot client to latest version
* api-change:``lex-runtime``: Update lex-runtime client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``athena``: Update athena client to latest version
* api-change:``iotsecuretunneling``: Update iotsecuretunneling client to latest version
* api-change:``ssm``: Update ssm client to latest version
* api-change:``application-insights``: Update application-insights client to latest version
* api-change:``mediapackage-vod``: Update mediapackage-vod client to latest version
* api-change:``appconfig``: Update appconfig client to latest version
* api-change:``mediaconvert``: Update mediaconvert client to latest version
* api-change:``kinesisanalyticsv2``: Update kinesisanalyticsv2 client to latest version
* api-change:``medialive``: Update medialive client to latest version
* api-change:``lambda``: Update lambda client to latest version
* api-change:``cloudwatch``: Update cloudwatch client to latest version
* api-change:``sesv2``: Update sesv2 client to latest version
* api-change:``application-autoscaling``: Update application-autoscaling client to latest version
* api-change:``greengrass``: Update greengrass client to latest version
* api-change:``alexaforbusiness``: Update alexaforbusiness client to latest version
* api-change:``rds``: Update rds client to latest version
* api-change:``ce``: Update ce client to latest version
* api-change:``ram``: Update ram client to latest version
* api-change:``codebuild``: Update codebuild client to latest version
* api-change:``comprehend``: Update comprehend client to latest version
* api-change:``kms``: Update kms client to latest version


1.13.26
=======

* api-change:``acm``: Update acm client to latest version
* api-change:``autoscaling-plans``: Update autoscaling-plans client to latest version
* api-change:``codebuild``: Update codebuild client to latest version
* api-change:``mediapackage-vod``: Update mediapackage-vod client to latest version
* api-change:``emr``: Update emr client to latest version
* api-change:``sns``: Update sns client to latest version
* api-change:``ssm``: Update ssm client to latest version
* api-change:``application-autoscaling``: Update application-autoscaling client to latest version
* api-change:``sts``: Update sts client to latest version
* api-change:``forecast``: Update forecast client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``rekognition``: Update rekognition client to latest version


1.13.25
=======

* bugfix:IMDS metadata: Add 405 case to metadata fetching logic.


1.13.24
=======

* api-change:``glue``: Update glue client to latest version
* api-change:``transcribe``: Update transcribe client to latest version
* api-change:``connectparticipant``: Update connectparticipant client to latest version
* api-change:``dynamodb``: Update dynamodb client to latest version
* api-change:``lex-runtime``: Update lex-runtime client to latest version
* api-change:``connect``: Update connect client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``meteringmarketplace``: Update meteringmarketplace client to latest version
* api-change:``config``: Update config client to latest version
* api-change:``lex-models``: Update lex-models client to latest version
* api-change:``ssm``: Update ssm client to latest version
* api-change:``amplify``: Update amplify client to latest version
* api-change:``appsync``: Update appsync client to latest version


1.13.23
=======

* api-change:``datasync``: Update datasync client to latest version
* api-change:``dlm``: Update dlm client to latest version
* api-change:``mediastore``: Update mediastore client to latest version
* api-change:``cloudtrail``: Update cloudtrail client to latest version
* api-change:``mgh``: Update mgh client to latest version
* api-change:``storagegateway``: Update storagegateway client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``codecommit``: Update codecommit client to latest version
* api-change:``s3``: Update s3 client to latest version
* api-change:``fsx``: Update fsx client to latest version
* api-change:``migrationhub-config``: Update migrationhub-config client to latest version
* api-change:``firehose``: Update firehose client to latest version
* api-change:``transcribe``: Update transcribe client to latest version
* api-change:``ecs``: Update ecs client to latest version
* api-change:``discovery``: Update discovery client to latest version
* api-change:``chime``: Update chime client to latest version
* api-change:``quicksight``: Update quicksight client to latest version


1.13.22
=======

* bugfix:IMDS: Fix regression in IMDS credential resolution. Fixes `#1892 <https://github.com/boto/botocore/issues/1892>`__.


1.13.21
=======

* api-change:``ec2``: Update ec2 client to latest version
* api-change:``cloudformation``: Update cloudformation client to latest version
* api-change:``elbv2``: Update elbv2 client to latest version
* api-change:``lambda``: Update lambda client to latest version
* api-change:``config``: Update config client to latest version
* api-change:``iam``: Update iam client to latest version
* api-change:``codebuild``: Update codebuild client to latest version
* api-change:``iot``: Update iot client to latest version
* api-change:``autoscaling``: Update autoscaling client to latest version


1.13.20
=======

* api-change:``cloudformation``: Update cloudformation client to latest version
* api-change:``s3``: Update s3 client to latest version
* api-change:``rds``: Update rds client to latest version
* api-change:``pinpoint``: Update pinpoint client to latest version
* api-change:``sagemaker``: Update sagemaker client to latest version
* api-change:``sagemaker-runtime``: Update sagemaker-runtime client to latest version
* api-change:``ce``: Update ce client to latest version
* api-change:``ssm``: Update ssm client to latest version


1.13.19
=======

* api-change:``cognito-idp``: Update cognito-idp client to latest version
* api-change:``elbv2``: Update elbv2 client to latest version
* api-change:``workspaces``: Update workspaces client to latest version
* api-change:``ssm``: Update ssm client to latest version
* api-change:``logs``: Update logs client to latest version
* api-change:``guardduty``: Update guardduty client to latest version
* api-change:``emr``: Update emr client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``mediaconvert``: Update mediaconvert client to latest version
* api-change:``eks``: Update eks client to latest version
* api-change:``chime``: Update chime client to latest version


1.13.18
=======

* api-change:``meteringmarketplace``: Update meteringmarketplace client to latest version
* api-change:``cognito-idp``: Update cognito-idp client to latest version
* api-change:``connect``: Update connect client to latest version
* api-change:``ssm``: Update ssm client to latest version
* api-change:``personalize``: Update personalize client to latest version


1.13.17
=======

* api-change:``sesv2``: Update sesv2 client to latest version
* api-change:``dataexchange``: Update dataexchange client to latest version
* api-change:``iot``: Update iot client to latest version
* api-change:``cloudsearch``: Update cloudsearch client to latest version
* api-change:``dlm``: Update dlm client to latest version


1.13.16
=======

* api-change:``transcribe``: Update transcribe client to latest version
* api-change:``marketplace-catalog``: Update marketplace-catalog client to latest version
* api-change:``dynamodb``: Update dynamodb client to latest version
* api-change:``codepipeline``: Update codepipeline client to latest version
* api-change:``elbv2``: Update elbv2 client to latest version


1.13.15
=======

* api-change:``ce``: Update ce client to latest version
* api-change:``cloudformation``: Update cloudformation client to latest version


1.13.14
=======

* api-change:``cognito-identity``: Update cognito-identity client to latest version
* api-change:``ecr``: Update ecr client to latest version


1.13.13
=======

* api-change:``ssm``: Update ssm client to latest version
* api-change:``sso``: Update sso client to latest version
* api-change:``sso-oidc``: Update sso-oidc client to latest version
* api-change:``comprehend``: Update comprehend client to latest version


1.13.12
=======

* api-change:``savingsplans``: Update savingsplans client to latest version


1.13.11
=======

* api-change:``codebuild``: Update codebuild client to latest version
* api-change:``budgets``: Update budgets client to latest version
* api-change:``efs``: Update efs client to latest version
* api-change:``ce``: Update ce client to latest version
* api-change:``savingsplans``: Update savingsplans client to latest version
* api-change:``signer``: Update signer client to latest version


1.13.10
=======

* api-change:``rds``: Update rds client to latest version
* api-change:``codestar-notifications``: Update codestar-notifications client to latest version


1.13.9
======

* api-change:``dax``: Update dax client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``robomaker``: Update robomaker client to latest version


1.13.8
======

* api-change:``pinpoint``: Update pinpoint client to latest version
* api-change:``cloudtrail``: Update cloudtrail client to latest version
* api-change:``dms``: Update dms client to latest version


1.13.7
======

* api-change:``support``: Update support client to latest version
* api-change:``amplify``: Update amplify client to latest version
* api-change:``s3``: Update s3 client to latest version


1.13.6
======

* api-change:``elasticache``: Update elasticache client to latest version


1.13.5
======

* api-change:``cloud9``: Update cloud9 client to latest version
* api-change:``appstream``: Update appstream client to latest version


1.13.4
======

* api-change:``s3``: Update s3 client to latest version


1.13.3
======

* api-change:``elasticache``: Update elasticache client to latest version
* api-change:``transfer``: Update transfer client to latest version
* api-change:``ecr``: Update ecr client to latest version


1.13.2
======

* api-change:``sagemaker``: Update sagemaker client to latest version
* api-change:``gamelift``: Update gamelift client to latest version
* enhancement:``sts``: Add support for configuring the use of regional STS endpoints.
* api-change:``chime``: Update chime client to latest version
* api-change:``appmesh``: Update appmesh client to latest version
* api-change:``ec2``: Update ec2 client to latest version


1.13.1
======

* api-change:``polly``: Update polly client to latest version
* api-change:``connect``: Update connect client to latest version


1.13.0
======

* api-change:``opsworkscm``: Update opsworkscm client to latest version
* api-change:``iotevents``: Update iotevents client to latest version
* feature:``botocore.vendored.requests``: Removed vendored version of ``requests`` (`#1829 <https://github.com/boto/botocore/issues/1829>`__)


1.12.253
========

* api-change:``cloudwatch``: Update cloudwatch client to latest version


1.12.252
========

* api-change:``batch``: Update batch client to latest version
* api-change:``rds``: Update rds client to latest version


1.12.251
========

* api-change:``kafka``: Update kafka client to latest version
* api-change:``marketplacecommerceanalytics``: Update marketplacecommerceanalytics client to latest version
* api-change:``robomaker``: Update robomaker client to latest version


1.12.250
========

* api-change:``kinesis-video-archived-media``: Update kinesis-video-archived-media client to latest version


1.12.249
========

* api-change:``personalize``: Update personalize client to latest version
* api-change:``workspaces``: Update workspaces client to latest version


1.12.248
========

* api-change:``greengrass``: Update greengrass client to latest version


1.12.247
========

* api-change:``ec2``: Update ec2 client to latest version
* api-change:``lex-runtime``: Update lex-runtime client to latest version
* api-change:``fms``: Update fms client to latest version
* api-change:``iotanalytics``: Update iotanalytics client to latest version


1.12.246
========

* api-change:``kafka``: Update kafka client to latest version
* api-change:``elasticache``: Update elasticache client to latest version
* api-change:``mediaconvert``: Update mediaconvert client to latest version


1.12.245
========

* api-change:``organizations``: Update organizations client to latest version
* api-change:``events``: Update events client to latest version
* api-change:``firehose``: Update firehose client to latest version
* api-change:``datasync``: Update datasync client to latest version


1.12.244
========

* api-change:``snowball``: Update snowball client to latest version
* api-change:``directconnect``: Update directconnect client to latest version
* api-change:``firehose``: Update firehose client to latest version
* api-change:``pinpoint``: Update pinpoint client to latest version
* api-change:``glue``: Update glue client to latest version
* api-change:``pinpoint-email``: Update pinpoint-email client to latest version


1.12.243
========

* api-change:``cognito-idp``: Update cognito-idp client to latest version
* api-change:``mediapackage``: Update mediapackage client to latest version
* api-change:``ssm``: Update ssm client to latest version


1.12.242
========

* api-change:``es``: Update es client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``application-autoscaling``: Update application-autoscaling client to latest version
* api-change:``devicefarm``: Update devicefarm client to latest version


1.12.241
========

* api-change:``lightsail``: Update lightsail client to latest version


1.12.240
========

* api-change:``docdb``: Update docdb client to latest version


1.12.239
========

* api-change:``waf``: Update waf client to latest version
* api-change:``rds``: Update rds client to latest version
* api-change:``mq``: Update mq client to latest version


1.12.238
========

* api-change:``amplify``: Update amplify client to latest version
* api-change:``ecs``: Update ecs client to latest version


1.12.237
========

* api-change:``ssm``: Update ssm client to latest version
* api-change:``codepipeline``: Update codepipeline client to latest version


1.12.236
========

* api-change:``globalaccelerator``: Update globalaccelerator client to latest version
* api-change:``dms``: Update dms client to latest version
* api-change:``sagemaker``: Update sagemaker client to latest version


1.12.235
========

* api-change:``transcribe``: Update transcribe client to latest version
* api-change:``comprehendmedical``: Update comprehendmedical client to latest version
* api-change:``datasync``: Update datasync client to latest version


1.12.234
========

* api-change:``rds-data``: Update rds-data client to latest version
* api-change:``redshift``: Update redshift client to latest version


1.12.233
========

* api-change:``workspaces``: Update workspaces client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``greengrass``: Update greengrass client to latest version
* api-change:``rds``: Update rds client to latest version


1.12.232
========

* api-change:``mediaconnect``: Update mediaconnect client to latest version
* api-change:``glue``: Update glue client to latest version
* api-change:``ecs``: Update ecs client to latest version


1.12.231
========

* api-change:``ram``: Update ram client to latest version
* api-change:``waf-regional``: Update waf-regional client to latest version
* api-change:``apigateway``: Update apigateway client to latest version


1.12.230
========

* api-change:``iam``: Update iam client to latest version
* api-change:``athena``: Update athena client to latest version
* api-change:``personalize``: Update personalize client to latest version


1.12.229
========

* api-change:``eks``: Update eks client to latest version
* api-change:``mediaconvert``: Update mediaconvert client to latest version


1.12.228
========

* api-change:``elbv2``: Update elbv2 client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``workmailmessageflow``: Update workmailmessageflow client to latest version
* api-change:``medialive``: Update medialive client to latest version


1.12.227
========

* api-change:``stepfunctions``: Update stepfunctions client to latest version
* api-change:``rds``: Update rds client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``mediaconnect``: Update mediaconnect client to latest version
* api-change:``ses``: Update ses client to latest version
* api-change:``config``: Update config client to latest version


1.12.226
========

* api-change:``storagegateway``: Update storagegateway client to latest version


1.12.225
========

* api-change:``qldb``: Update qldb client to latest version
* api-change:``marketplacecommerceanalytics``: Update marketplacecommerceanalytics client to latest version
* api-change:``appstream``: Update appstream client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``robomaker``: Update robomaker client to latest version
* api-change:``appmesh``: Update appmesh client to latest version
* api-change:``qldb-session``: Update qldb-session client to latest version


1.12.224
========

* api-change:``kinesisanalytics``: Update kinesisanalytics client to latest version


1.12.223
========

* api-change:``config``: Update config client to latest version


1.12.222
========

* api-change:``stepfunctions``: Update stepfunctions client to latest version
* api-change:``transcribe``: Update transcribe client to latest version
* api-change:``eks``: Update eks client to latest version


1.12.221
========

* api-change:``ecs``: Update ecs client to latest version
* api-change:``resourcegroupstaggingapi``: Update resourcegroupstaggingapi client to latest version
* api-change:``gamelift``: Update gamelift client to latest version


1.12.220
========

* api-change:``mq``: Update mq client to latest version
* api-change:``apigatewaymanagementapi``: Update apigatewaymanagementapi client to latest version
* api-change:``ecs``: Update ecs client to latest version


1.12.219
========

* api-change:``codepipeline``: Update codepipeline client to latest version
* api-change:``application-autoscaling``: Update application-autoscaling client to latest version
* api-change:``elasticache``: Update elasticache client to latest version
* api-change:``lambda``: Update lambda client to latest version
* api-change:``ecs``: Update ecs client to latest version


1.12.218
========

* api-change:``sqs``: Update sqs client to latest version
* api-change:``globalaccelerator``: Update globalaccelerator client to latest version
* api-change:``mediaconvert``: Update mediaconvert client to latest version


1.12.217
========

* api-change:``organizations``: Update organizations client to latest version


1.12.216
========

* api-change:``ssm``: Update ssm client to latest version
* api-change:``securityhub``: Update securityhub client to latest version


1.12.215
========

* api-change:``ec2``: Update ec2 client to latest version
* api-change:``mediapackage-vod``: Update mediapackage-vod client to latest version
* api-change:``transcribe``: Update transcribe client to latest version


1.12.214
========

* api-change:``datasync``: Update datasync client to latest version
* api-change:``rds``: Update rds client to latest version


1.12.213
========

* api-change:``forecast``: Update forecast client to latest version
* api-change:``forecastquery``: Update forecastquery client to latest version
* api-change:``personalize-runtime``: Update personalize-runtime client to latest version
* api-change:``elasticache``: Update elasticache client to latest version
* api-change:``rekognition``: Update rekognition client to latest version
* api-change:``sagemaker``: Update sagemaker client to latest version
* api-change:``sqs``: Update sqs client to latest version


1.12.212
========

* api-change:``sagemaker``: Update sagemaker client to latest version
* api-change:``transfer``: Update transfer client to latest version
* api-change:``appstream``: Update appstream client to latest version
* api-change:``alexaforbusiness``: Update alexaforbusiness client to latest version


1.12.211
========

* api-change:``appmesh``: Update appmesh client to latest version
* api-change:``cur``: Update cur client to latest version


1.12.210
========

* api-change:``robomaker``: Update robomaker client to latest version
* api-change:``emr``: Update emr client to latest version
* api-change:``ecs``: Update ecs client to latest version


1.12.209
========

* api-change:``ec2``: Update ec2 client to latest version
* api-change:``appmesh``: Update appmesh client to latest version
* api-change:``athena``: Update athena client to latest version
* api-change:``codecommit``: Update codecommit client to latest version
* api-change:``glue``: Update glue client to latest version
* api-change:``storagegateway``: Update storagegateway client to latest version


1.12.208
========

* api-change:``ec2``: Update ec2 client to latest version


1.12.207
========

* api-change:``appsync``: Update appsync client to latest version


1.12.206
========

* api-change:``autoscaling``: Update autoscaling client to latest version
* api-change:``cloudwatch``: Update cloudwatch client to latest version
* api-change:``application-autoscaling``: Update application-autoscaling client to latest version
* api-change:``rekognition``: Update rekognition client to latest version


1.12.205
========

* api-change:``guardduty``: Update guardduty client to latest version
* api-change:``lex-runtime``: Update lex-runtime client to latest version
* api-change:``redshift``: Update redshift client to latest version
* api-change:``iot``: Update iot client to latest version
* api-change:``mediaconvert``: Update mediaconvert client to latest version


1.12.204
========

* api-change:``lakeformation``: Update lakeformation client to latest version
* api-change:``opsworkscm``: Update opsworkscm client to latest version
* api-change:``glue``: Update glue client to latest version
* api-change:``codebuild``: Update codebuild client to latest version


1.12.203
========

* api-change:``application-insights``: Update application-insights client to latest version


1.12.202
========

* api-change:``batch``: Update batch client to latest version


1.12.201
========

* api-change:``datasync``: Update datasync client to latest version
* api-change:``iot``: Update iot client to latest version
* api-change:``ec2``: Update ec2 client to latest version


1.12.200
========

* api-change:``sts``: Update sts client to latest version
* enhancement:Credentials: Add support for a credential provider that handles resolving credentials via STS AssumeRoleWithWebIdentity


1.12.199
========

* api-change:``polly``: Update polly client to latest version
* api-change:``mediaconvert``: Update mediaconvert client to latest version
* api-change:``route53``: Update route53 client to latest version


1.12.198
========

* bugfix:S3: Fix an issue that would cause S3 list_object_versions to sometimes fail parsing responses with certain key values.
* api-change:``codecommit``: Update codecommit client to latest version


1.12.197
========

* api-change:``ce``: Update ce client to latest version
* api-change:``greengrass``: Update greengrass client to latest version
* api-change:``glue``: Update glue client to latest version
* api-change:``logs``: Update logs client to latest version
* api-change:``mediaconnect``: Update mediaconnect client to latest version
* api-change:``batch``: Update batch client to latest version
* api-change:``ec2``: Update ec2 client to latest version


1.12.196
========

* api-change:``medialive``: Update medialive client to latest version
* api-change:``ecr``: Update ecr client to latest version
* api-change:``mediaconvert``: Update mediaconvert client to latest version


1.12.195
========

* api-change:``ec2``: Update ec2 client to latest version
* api-change:``sts``: Update sts client to latest version
* api-change:``pinpoint``: Update pinpoint client to latest version
* api-change:``glue``: Update glue client to latest version


1.12.194
========

* api-change:``ssm``: Update ssm client to latest version
* api-change:``secretsmanager``: Update secretsmanager client to latest version


1.12.193
========

* api-change:``mq``: Update mq client to latest version
* api-change:``shield``: Update shield client to latest version


1.12.192
========

* bugfix:Dependency: Fixed dependency issue with broken docutils aws/aws-cli`#4332 <https://github.com/boto/botocore/issues/4332>`__


1.12.191
========

* api-change:``sqs``: Update sqs client to latest version
* api-change:``iotevents``: Update iotevents client to latest version


1.12.190
========

* api-change:``comprehend``: Update comprehend client to latest version
* api-change:``codedeploy``: Update codedeploy client to latest version
* api-change:``elasticache``: Update elasticache client to latest version
* api-change:``ecs``: Update ecs client to latest version


1.12.189
========

* api-change:``config``: Update config client to latest version
* api-change:``dms``: Update dms client to latest version
* api-change:``autoscaling``: Update autoscaling client to latest version


1.12.188
========

* api-change:``iam``: Update iam client to latest version
* api-change:``apigatewayv2``: Update apigatewayv2 client to latest version
* api-change:``robomaker``: Update robomaker client to latest version
* api-change:``es``: Update es client to latest version


1.12.187
========

* api-change:``events``: Update events client to latest version


1.12.186
========

* api-change:``quicksight``: Update quicksight client to latest version
* api-change:``glacier``: Update glacier client to latest version
* api-change:``servicecatalog``: Update servicecatalog client to latest version


1.12.185
========

* api-change:``efs``: Update efs client to latest version
* api-change:``cloudwatch``: Update cloudwatch client to latest version
* api-change:``amplify``: Update amplify client to latest version
* api-change:``kinesis-video-archived-media``: Update kinesis-video-archived-media client to latest version
* api-change:``gamelift``: Update gamelift client to latest version
* api-change:``kinesisvideo``: Update kinesisvideo client to latest version
* api-change:``waf``: Update waf client to latest version
* api-change:``config``: Update config client to latest version
* api-change:``waf-regional``: Update waf-regional client to latest version


1.12.184
========

* api-change:``ce``: Update ce client to latest version


1.12.183
========

* api-change:``swf``: Update swf client to latest version
* api-change:``rds``: Update rds client to latest version
* api-change:``s3``: Update s3 client to latest version
* api-change:``ec2``: Update ec2 client to latest version


1.12.182
========

* enhancement:CSM: Support configuration of the host used in client side metrics via AWS_CSM_HOST
* api-change:``appstream``: Update appstream client to latest version
* api-change:``mediastore``: Update mediastore client to latest version


1.12.181
========

* api-change:``docdb``: Update docdb client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``organizations``: Update organizations client to latest version
* api-change:``rds``: Update rds client to latest version


1.12.180
========

* api-change:``alexaforbusiness``: Update alexaforbusiness client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``redshift``: Update redshift client to latest version
* api-change:``workspaces``: Update workspaces client to latest version


1.12.179
========

* api-change:``directconnect``: Update directconnect client to latest version
* api-change:``pinpoint``: Update pinpoint client to latest version
* api-change:``workspaces``: Update workspaces client to latest version
* api-change:``ec2-instance-connect``: Update ec2-instance-connect client to latest version


1.12.178
========

* api-change:``dynamodb``: Update dynamodb client to latest version


1.12.177
========

* api-change:``codecommit``: Update codecommit client to latest version
* api-change:``apigatewayv2``: Update apigatewayv2 client to latest version


1.12.176
========

* api-change:``ec2``: Update ec2 client to latest version
* api-change:``eks``: Update eks client to latest version


1.12.175
========

* api-change:``application-insights``: Update application-insights client to latest version
* api-change:``securityhub``: Update securityhub client to latest version
* api-change:``apigateway``: Update apigateway client to latest version
* api-change:``elbv2``: Update elbv2 client to latest version
* api-change:``fsx``: Update fsx client to latest version
* api-change:``service-quotas``: Update service-quotas client to latest version
* api-change:``resourcegroupstaggingapi``: Update resourcegroupstaggingapi client to latest version
* api-change:``ssm``: Update ssm client to latest version
* api-change:``apigatewayv2``: Update apigatewayv2 client to latest version


1.12.174
========

* api-change:``devicefarm``: Update devicefarm client to latest version
* api-change:``iam``: Update iam client to latest version
* api-change:``mediapackage``: Update mediapackage client to latest version
* api-change:``kinesis-video-media``: Update kinesis-video-media client to latest version


1.12.173
========

* api-change:``health``: Update health client to latest version
* api-change:``glue``: Update glue client to latest version
* api-change:``iotevents-data``: Update iotevents-data client to latest version
* api-change:``opsworks``: Update opsworks client to latest version
* api-change:``rds``: Update rds client to latest version
* api-change:``acm-pca``: Update acm-pca client to latest version


1.12.172
========

* api-change:``eks``: Update eks client to latest version


1.12.171
========

* api-change:``ec2``: Update ec2 client to latest version
* api-change:``resourcegroupstaggingapi``: Update resourcegroupstaggingapi client to latest version


1.12.170
========

* api-change:``neptune``: Update neptune client to latest version
* api-change:``servicecatalog``: Update servicecatalog client to latest version
* api-change:``robomaker``: Update robomaker client to latest version
* bugfix:Paginator: Fixes a bug where pagination tokens with three consecutive underscores would result in a parsing failure. Resolves boto/boto3`#1984 <https://github.com/boto/boto3/issues/1984>`__.


1.12.169
========

* api-change:``cloudfront``: Update cloudfront client to latest version
* api-change:``personalize``: Update personalize client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``appstream``: Update appstream client to latest version


1.12.168
========

* api-change:``appmesh``: Update appmesh client to latest version
* api-change:``elasticache``: Update elasticache client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``guardduty``: Update guardduty client to latest version


1.12.167
========

* api-change:``servicecatalog``: Update servicecatalog client to latest version


1.12.166
========

* api-change:``sagemaker``: Update sagemaker client to latest version


1.12.165
========

* api-change:``codebuild``: Update codebuild client to latest version
* api-change:``personalize-runtime``: Update personalize-runtime client to latest version
* api-change:``codecommit``: Update codecommit client to latest version
* api-change:``personalize-events``: Update personalize-events client to latest version
* api-change:``personalize``: Update personalize client to latest version


1.12.164
========

* api-change:``ec2``: Update ec2 client to latest version


1.12.163
========

* api-change:``ecs``: Update ecs client to latest version
* api-change:``organizations``: Update organizations client to latest version
* api-change:``logs``: Update logs client to latest version
* api-change:``dynamodb``: Update dynamodb client to latest version
* api-change:``guardduty``: Update guardduty client to latest version
* api-change:``ssm``: Update ssm client to latest version
* api-change:``ses``: Update ses client to latest version
* api-change:``mediaconnect``: Update mediaconnect client to latest version


1.12.162
========

* api-change:``glue``: Update glue client to latest version


1.12.161
========

* api-change:``ec2``: Update ec2 client to latest version
* api-change:``storagegateway``: Update storagegateway client to latest version
* api-change:``s3``: Update s3 client to latest version
* api-change:``elasticache``: Update elasticache client to latest version
* api-change:``iam``: Update iam client to latest version


1.12.160
========

* api-change:``ec2``: Update ec2 client to latest version
* api-change:``rds``: Update rds client to latest version


1.12.159
========

* api-change:``iotevents-data``: Update iotevents-data client to latest version
* api-change:``iotevents``: Update iotevents client to latest version
* api-change:``pinpoint-email``: Update pinpoint-email client to latest version
* api-change:``iotanalytics``: Update iotanalytics client to latest version
* api-change:``codecommit``: Update codecommit client to latest version
* api-change:``rds-data``: Update rds-data client to latest version
* api-change:``rds``: Update rds client to latest version
* api-change:``servicecatalog``: Update servicecatalog client to latest version
* api-change:``kafka``: Update kafka client to latest version


1.12.158
========

* api-change:``ssm``: Update ssm client to latest version
* api-change:``securityhub``: Update securityhub client to latest version
* api-change:``iotthingsgraph``: Update iotthingsgraph client to latest version
* api-change:``dlm``: Update dlm client to latest version
* api-change:``rds``: Update rds client to latest version
* api-change:``ec2``: Update ec2 client to latest version


1.12.157
========

* api-change:``groundstation``: Update groundstation client to latest version
* api-change:``transcribe``: Update transcribe client to latest version
* api-change:``chime``: Update chime client to latest version
* api-change:``rds``: Update rds client to latest version
* api-change:``waf``: Update waf client to latest version
* api-change:``pinpoint-email``: Update pinpoint-email client to latest version
* api-change:``robomaker``: Update robomaker client to latest version
* api-change:``sts``: Update sts client to latest version
* api-change:``storagegateway``: Update storagegateway client to latest version


1.12.156
========

* api-change:``mediastore-data``: Update mediastore-data client to latest version
* api-change:``codedeploy``: Update codedeploy client to latest version
* api-change:``opsworkscm``: Update opsworkscm client to latest version


1.12.155
========

* api-change:``waf-regional``: Update waf-regional client to latest version
* api-change:``ec2``: Update ec2 client to latest version


1.12.154
========

* api-change:``efs``: Update efs client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``apigateway``: Update apigateway client to latest version
* api-change:``worklink``: Update worklink client to latest version
* api-change:``rds``: Update rds client to latest version
* api-change:``servicecatalog``: Update servicecatalog client to latest version
* api-change:``devicefarm``: Update devicefarm client to latest version
* api-change:``budgets``: Update budgets client to latest version


1.12.153
========

* api-change:``datasync``: Update datasync client to latest version
* api-change:``alexaforbusiness``: Update alexaforbusiness client to latest version


1.12.152
========

* api-change:``kafka``: Update kafka client to latest version
* api-change:``meteringmarketplace``: Update meteringmarketplace client to latest version
* api-change:``mediapackage-vod``: Update mediapackage-vod client to latest version


1.12.151
========

* api-change:``appstream``: Update appstream client to latest version


1.12.150
========

* api-change:``medialive``: Update medialive client to latest version
* api-change:``s3``: Update s3 client to latest version


1.12.149
========

* api-change:``ec2``: Update ec2 client to latest version
* api-change:``transcribe``: Update transcribe client to latest version
* api-change:``mediapackage``: Update mediapackage client to latest version
* api-change:``codepipeline``: Update codepipeline client to latest version
* enhancement:Environment Variables: Ignore env var credentials is values are empty (`#1680 <https://github.com/boto/botocore/issues/1680>`__)
* api-change:``rds``: Update rds client to latest version


1.12.148
========

* api-change:``comprehend``: Update comprehend client to latest version
* api-change:``chime``: Update chime client to latest version
* api-change:``storagegateway``: Update storagegateway client to latest version
* api-change:``ec2``: Update ec2 client to latest version


1.12.147
========

* api-change:``datasync``: Update datasync client to latest version
* api-change:``iotanalytics``: Update iotanalytics client to latest version
* api-change:``lambda``: Update lambda client to latest version


1.12.146
========

* api-change:``glue``: Update glue client to latest version
* api-change:``sts``: Update sts client to latest version


1.12.145
========

* api-change:``servicecatalog``: Update servicecatalog client to latest version
* api-change:``eks``: Update eks client to latest version
* api-change:``sagemaker``: Update sagemaker client to latest version
* api-change:``kinesisanalytics``: Update kinesisanalytics client to latest version
* api-change:``kinesisanalyticsv2``: Update kinesisanalyticsv2 client to latest version


1.12.144
========

* api-change:``appsync``: Update appsync client to latest version
* api-change:``storagegateway``: Update storagegateway client to latest version
* api-change:``ssm``: Update ssm client to latest version
* api-change:``alexaforbusiness``: Update alexaforbusiness client to latest version


1.12.143
========

* api-change:``config``: Update config client to latest version
* api-change:``iam``: Update iam client to latest version
* api-change:``sts``: Update sts client to latest version
* api-change:``codepipeline``: Update codepipeline client to latest version


1.12.142
========

* api-change:``workmail``: Update workmail client to latest version
* api-change:``medialive``: Update medialive client to latest version
* api-change:``cognito-idp``: Update cognito-idp client to latest version
* api-change:``mediaconvert``: Update mediaconvert client to latest version


1.12.141
========

* api-change:``alexaforbusiness``: Update alexaforbusiness client to latest version
* api-change:``kms``: Update kms client to latest version


1.12.140
========

* api-change:``ecs``: Update ecs client to latest version
* api-change:``xray``: Update xray client to latest version
* api-change:``ec2``: Update ec2 client to latest version


1.12.139
========

* api-change:``neptune``: Update neptune client to latest version
* api-change:``servicecatalog``: Update servicecatalog client to latest version
* api-change:``managedblockchain``: Update managedblockchain client to latest version
* api-change:``s3control``: Update s3control client to latest version
* api-change:``directconnect``: Update directconnect client to latest version
* api-change:``codepipeline``: Update codepipeline client to latest version


1.12.138
========

* api-change:``transfer``: Update transfer client to latest version
* api-change:``ec2``: Update ec2 client to latest version


1.12.137
========

* api-change:``iam``: Update iam client to latest version
* api-change:``sns``: Update sns client to latest version


1.12.136
========

* api-change:``gamelift``: Update gamelift client to latest version
* api-change:``workspaces``: Update workspaces client to latest version
* api-change:``dynamodb``: Update dynamodb client to latest version
* api-change:``inspector``: Update inspector client to latest version
* api-change:``lambda``: Update lambda client to latest version
* api-change:``batch``: Update batch client to latest version


1.12.135
========

* api-change:``mediatailor``: Update mediatailor client to latest version
* api-change:``rds``: Update rds client to latest version
* api-change:``cloudformation``: Update cloudformation client to latest version
* api-change:``ssm``: Update ssm client to latest version
* api-change:``storagegateway``: Update storagegateway client to latest version
* api-change:``route53``: Update route53 client to latest version
* api-change:``alexaforbusiness``: Update alexaforbusiness client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``mediaconnect``: Update mediaconnect client to latest version
* api-change:``textract``: Update textract client to latest version


1.12.134
========

* api-change:``resource-groups``: Update resource-groups client to latest version
* api-change:``transcribe``: Update transcribe client to latest version
* api-change:``workspaces``: Update workspaces client to latest version


1.12.133
========

* api-change:``kafka``: Update kafka client to latest version
* api-change:``cognito-idp``: Update cognito-idp client to latest version
* api-change:``rds``: Update rds client to latest version
* api-change:``worklink``: Update worklink client to latest version
* api-change:``workspaces``: Update workspaces client to latest version
* api-change:``discovery``: Update discovery client to latest version
* api-change:``organizations``: Update organizations client to latest version


1.12.132
========

* api-change:``polly``: Update polly client to latest version
* api-change:``ec2``: Update ec2 client to latest version


1.12.131
========

* api-change:``organizations``: Update organizations client to latest version
* api-change:``mq``: Update mq client to latest version
* api-change:``redshift``: Update redshift client to latest version
* api-change:``storagegateway``: Update storagegateway client to latest version
* api-change:``cloudwatch``: Update cloudwatch client to latest version
* api-change:``cognito-idp``: Update cognito-idp client to latest version


1.12.130
========

* api-change:``mediaconvert``: Update mediaconvert client to latest version
* api-change:``glue``: Update glue client to latest version
* api-change:``comprehend``: Update comprehend client to latest version
* api-change:``iot1click-devices``: Update iot1click-devices client to latest version
* api-change:``medialive``: Update medialive client to latest version


1.12.129
========

* api-change:``eks``: Update eks client to latest version
* api-change:``iam``: Update iam client to latest version


1.12.128
========

* api-change:``batch``: Update batch client to latest version
* api-change:``comprehend``: Update comprehend client to latest version


1.12.127
========

* api-change:``securityhub``: Update securityhub client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``acm``: Update acm client to latest version


1.12.126
========

* api-change:``emr``: Update emr client to latest version
* api-change:``ssm``: Update ssm client to latest version


1.12.125
========

* api-change:``comprehend``: Update comprehend client to latest version
* api-change:``cloudwatch``: Update cloudwatch client to latest version
* api-change:``greengrass``: Update greengrass client to latest version


1.12.124
========

* api-change:``servicecatalog``: Update servicecatalog client to latest version
* api-change:``medialive``: Update medialive client to latest version
* api-change:``pinpoint-email``: Update pinpoint-email client to latest version
* api-change:``workspaces``: Update workspaces client to latest version


1.12.123
========

* api-change:``ec2``: Update ec2 client to latest version
* api-change:``appmesh``: Update appmesh client to latest version
* api-change:``ecs``: Update ecs client to latest version
* api-change:``elbv2``: Update elbv2 client to latest version
* api-change:``transfer``: Update transfer client to latest version
* api-change:``storagegateway``: Update storagegateway client to latest version
* api-change:``s3``: Update s3 client to latest version


1.12.122
========

* api-change:``workmail``: Update workmail client to latest version
* api-change:``glue``: Update glue client to latest version


1.12.121
========

* api-change:``iotanalytics``: Update iotanalytics client to latest version
* api-change:``robomaker``: Update robomaker client to latest version
* api-change:``directconnect``: Update directconnect client to latest version
* api-change:``mediaconvert``: Update mediaconvert client to latest version
* api-change:``transcribe``: Update transcribe client to latest version
* api-change:``fms``: Update fms client to latest version
* api-change:``iot1click-devices``: Update iot1click-devices client to latest version


1.12.120
========

* api-change:``iot1click-projects``: Update iot1click-projects client to latest version
* api-change:``transcribe``: Update transcribe client to latest version


1.12.119
========

* api-change:``iot``: Update iot client to latest version
* api-change:``lightsail``: Update lightsail client to latest version
* api-change:``autoscaling``: Update autoscaling client to latest version
* api-change:``events``: Update events client to latest version
* api-change:``cognito-idp``: Update cognito-idp client to latest version


1.12.118
========

* api-change:``cognito-identity``: Update cognito-identity client to latest version
* api-change:``codepipeline``: Update codepipeline client to latest version
* api-change:``meteringmarketplace``: Update meteringmarketplace client to latest version


1.12.117
========

* api-change:``config``: Update config client to latest version
* api-change:``eks``: Update eks client to latest version


1.12.116
========

* api-change:``dms``: Update dms client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``chime``: Update chime client to latest version


1.12.115
========

* api-change:``ec2``: Update ec2 client to latest version
* api-change:``config``: Update config client to latest version
* api-change:``acm``: Update acm client to latest version
* api-change:``iot``: Update iot client to latest version
* api-change:``acm-pca``: Update acm-pca client to latest version
* api-change:``cloudwatch``: Update cloudwatch client to latest version
* api-change:``sagemaker``: Update sagemaker client to latest version


1.12.114
========

* api-change:``config``: Update config client to latest version
* api-change:``logs``: Update logs client to latest version


1.12.113
========

* api-change:``serverlessrepo``: Update serverlessrepo client to latest version


1.12.112
========

* api-change:``iot``: Update iot client to latest version
* api-change:``quicksight``: Update quicksight client to latest version
* api-change:``glue``: Update glue client to latest version
* api-change:``ce``: Update ce client to latest version
* api-change:``elasticbeanstalk``: Update elasticbeanstalk client to latest version
* api-change:``rekognition``: Update rekognition client to latest version


1.12.111
========

* api-change:``s3``: Update s3 client to latest version
* api-change:``codebuild``: Update codebuild client to latest version
* api-change:``sagemaker``: Update sagemaker client to latest version


1.12.110
========

* api-change:``gamelift``: Update gamelift client to latest version
* api-change:``greengrass``: Update greengrass client to latest version
* api-change:``appmesh``: Update appmesh client to latest version
* api-change:``rds``: Update rds client to latest version
* api-change:``medialive``: Update medialive client to latest version
* api-change:``autoscaling``: Update autoscaling client to latest version
* api-change:``ecs``: Update ecs client to latest version


1.12.109
========

* api-change:``directconnect``: Update directconnect client to latest version
* api-change:``ec2``: Update ec2 client to latest version


1.12.108
========

* api-change:``textract``: Update textract client to latest version
* api-change:``storagegateway``: Update storagegateway client to latest version
* api-change:``medialive``: Update medialive client to latest version
* api-change:``codedeploy``: Update codedeploy client to latest version


1.12.107
========

* api-change:``mediapackage``: Update mediapackage client to latest version
* api-change:``ssm``: Update ssm client to latest version


1.12.106
========

* api-change:``ec2``: Update ec2 client to latest version
* api-change:``autoscaling-plans``: Update autoscaling-plans client to latest version


1.12.105
========

* api-change:``ssm``: Update ssm client to latest version
* api-change:``apigatewayv2``: Update apigatewayv2 client to latest version
* api-change:``alexaforbusiness``: Update alexaforbusiness client to latest version
* api-change:``application-autoscaling``: Update application-autoscaling client to latest version


1.12.104
========

* api-change:``waf-regional``: Update waf-regional client to latest version
* api-change:``waf``: Update waf client to latest version


1.12.103
========

* api-change:``discovery``: Update discovery client to latest version
* api-change:``organizations``: Update organizations client to latest version
* api-change:``resource-groups``: Update resource-groups client to latest version
* api-change:``opsworkscm``: Update opsworkscm client to latest version
* api-change:``pinpoint``: Update pinpoint client to latest version
* api-change:``mediaconvert``: Update mediaconvert client to latest version
* api-change:``cur``: Update cur client to latest version


1.12.102
========

* api-change:``elbv2``: Update elbv2 client to latest version
* api-change:``mediastore``: Update mediastore client to latest version
* api-change:``ce``: Update ce client to latest version
* api-change:``autoscaling``: Update autoscaling client to latest version


1.12.101
========

* api-change:``athena``: Update athena client to latest version
* api-change:``glue``: Update glue client to latest version
* api-change:``stepfunctions``: Update stepfunctions client to latest version
* api-change:``cloud9``: Update cloud9 client to latest version


1.12.100
========

* api-change:``kinesis-video-archived-media``: Update kinesis-video-archived-media client to latest version
* api-change:``workdocs``: Update workdocs client to latest version
* api-change:``codebuild``: Update codebuild client to latest version
* api-change:``cloudwatch``: Update cloudwatch client to latest version
* api-change:``organizations``: Update organizations client to latest version
* api-change:``kinesisvideo``: Update kinesisvideo client to latest version
* api-change:``kinesis-video-media``: Update kinesis-video-media client to latest version
* api-change:``transfer``: Update transfer client to latest version


1.12.99
=======

* api-change:``codecommit``: Update codecommit client to latest version
* api-change:``directconnect``: Update directconnect client to latest version
* api-change:``medialive``: Update medialive client to latest version


1.12.98
=======

* api-change:``iot``: Update iot client to latest version
* api-change:``ssm``: Update ssm client to latest version
* api-change:``ds``: Update ds client to latest version
* enhancement:Paginator: Add additional paginators for CloudFormation
* api-change:``efs``: Update efs client to latest version


1.12.97
=======

* api-change:``athena``: Update athena client to latest version
* api-change:``secretsmanager``: Update secretsmanager client to latest version


1.12.96
=======

* api-change:``chime``: Update chime client to latest version
* api-change:``application-autoscaling``: Update application-autoscaling client to latest version
* api-change:``iot``: Update iot client to latest version


1.12.95
=======

* api-change:``kinesisvideo``: Update kinesisvideo client to latest version
* api-change:``ec2``: Update ec2 client to latest version


1.12.94
=======

* api-change:``rekognition``: Update rekognition client to latest version
* api-change:``mediatailor``: Update mediatailor client to latest version
* api-change:``efs``: Update efs client to latest version


1.12.93
=======

* api-change:``lambda``: Update lambda client to latest version


1.12.92
=======

* api-change:``appstream``: Update appstream client to latest version
* api-change:``codebuild``: Update codebuild client to latest version
* api-change:``mediapackage``: Update mediapackage client to latest version


1.12.91
=======

* api-change:``discovery``: Update discovery client to latest version
* api-change:``ecs``: Update ecs client to latest version
* api-change:``dlm``: Update dlm client to latest version


1.12.90
=======

* api-change:``es``: Update es client to latest version
* api-change:``medialive``: Update medialive client to latest version
* api-change:``gamelift``: Update gamelift client to latest version
* api-change:``robomaker``: Update robomaker client to latest version


1.12.89
=======

* api-change:``ec2``: Update ec2 client to latest version
* api-change:``fsx``: Update fsx client to latest version


1.12.88
=======

* api-change:``shield``: Update shield client to latest version
* api-change:``servicecatalog``: Update servicecatalog client to latest version
* api-change:``ec2``: Update ec2 client to latest version


1.12.87
=======

* api-change:``ecs``: Update ecs client to latest version
* api-change:``application-autoscaling``: Update application-autoscaling client to latest version
* api-change:``workspaces``: Update workspaces client to latest version
* api-change:``codecommit``: Update codecommit client to latest version


1.12.86
=======

* api-change:``devicefarm``: Update devicefarm client to latest version
* api-change:``codecommit``: Update codecommit client to latest version
* api-change:``medialive``: Update medialive client to latest version
* api-change:``mediaconnect``: Update mediaconnect client to latest version


1.12.85
=======

* api-change:``logs``: Update logs client to latest version
* api-change:``elbv2``: Update elbv2 client to latest version
* api-change:``rds``: Update rds client to latest version
* api-change:``codebuild``: Update codebuild client to latest version
* api-change:``sms-voice``: Update sms-voice client to latest version
* api-change:``ecr``: Update ecr client to latest version


1.12.84
=======

* api-change:``worklink``: Update worklink client to latest version
* api-change:``apigatewaymanagementapi``: Update apigatewaymanagementapi client to latest version
* api-change:``acm-pca``: Update acm-pca client to latest version


1.12.83
=======

* api-change:``appstream``: Update appstream client to latest version
* api-change:``discovery``: Update discovery client to latest version
* api-change:``dms``: Update dms client to latest version
* api-change:``fms``: Update fms client to latest version
* api-change:``ssm``: Update ssm client to latest version


1.12.82
=======

* api-change:``glue``: Update glue client to latest version
* api-change:``ec2``: Update ec2 client to latest version


1.12.81
=======

* api-change:``lightsail``: Update lightsail client to latest version
* api-change:``lambda``: Update lambda client to latest version
* api-change:``pinpoint``: Update pinpoint client to latest version
* api-change:``rekognition``: Update rekognition client to latest version


1.12.80
=======

* api-change:``dynamodb``: Update dynamodb client to latest version
* api-change:``ce``: Update ce client to latest version
* api-change:``backup``: Update backup client to latest version


1.12.79
=======

* api-change:``storagegateway``: Update storagegateway client to latest version
* api-change:``mediaconvert``: Update mediaconvert client to latest version


1.12.78
=======

* api-change:``rds-data``: Update rds-data client to latest version
* api-change:``emr``: Update emr client to latest version


1.12.77
=======

* api-change:``iot``: Update iot client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``codedeploy``: Update codedeploy client to latest version
* api-change:``sagemaker``: Update sagemaker client to latest version


1.12.76
=======

* api-change:``docdb``: Update docdb client to latest version
* api-change:``redshift``: Update redshift client to latest version


1.12.75
=======

* api-change:``appmesh``: Update appmesh client to latest version


1.12.74
=======

* api-change:``ecs``: Update ecs client to latest version
* api-change:``devicefarm``: Update devicefarm client to latest version


1.12.73
=======

* api-change:``iotanalytics``: Update iotanalytics client to latest version


1.12.72
=======

* enhancement:Paginator: Added over 400 new paginators.
* api-change:``opsworkscm``: Update opsworkscm client to latest version


1.12.71
=======

* api-change:``acm-pca``: Update acm-pca client to latest version
* api-change:``dynamodb``: Update dynamodb client to latest version
* api-change:``sms-voice``: Update sms-voice client to latest version
* api-change:``stepfunctions``: Update stepfunctions client to latest version


1.12.70
=======

* api-change:``medialive``: Update medialive client to latest version
* enhancement:EndpointDiscovery: Add a config option, ``endpoint_discovery_enabled``, for automatically discovering endpoints
* api-change:``comprehend``: Update comprehend client to latest version
* api-change:``firehose``: Update firehose client to latest version
* api-change:``transcribe``: Update transcribe client to latest version
* api-change:``cognito-idp``: Update cognito-idp client to latest version


1.12.69
=======

* api-change:``sagemaker``: Update sagemaker client to latest version
* api-change:``waf-regional``: Update waf-regional client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``waf``: Update waf client to latest version


1.12.68
=======

* api-change:``apigatewayv2``: Update apigatewayv2 client to latest version
* bugfix:Credentials: Fixes an issue where credentials would be checked when creating an anonymous client. Fixes `#1472 <https://github.com/boto/botocore/issues/1472>`__
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``elasticbeanstalk``: Update elasticbeanstalk client to latest version
* api-change:``globalaccelerator``: Update globalaccelerator client to latest version
* enhancement:StreamingBody: Support iterating lines from a streaming response body with CRLF line endings
* api-change:``apigatewaymanagementapi``: Update apigatewaymanagementapi client to latest version


1.12.67
=======

* api-change:``quicksight``: Update quicksight client to latest version
* api-change:``ecr``: Update ecr client to latest version


1.12.66
=======

* api-change:``alexaforbusiness``: Update alexaforbusiness client to latest version
* api-change:``redshift``: Update redshift client to latest version
* api-change:``cloudformation``: Update cloudformation client to latest version


1.12.65
=======

* api-change:``organizations``: Update organizations client to latest version
* api-change:``pinpoint-email``: Update pinpoint-email client to latest version


1.12.64
=======

* api-change:``route53``: Update route53 client to latest version
* api-change:``glue``: Update glue client to latest version
* api-change:``sagemaker``: Update sagemaker client to latest version
* api-change:``eks``: Update eks client to latest version


1.12.63
=======

* api-change:``mediastore``: Update mediastore client to latest version
* api-change:``ecs``: Update ecs client to latest version
* api-change:``connect``: Update connect client to latest version


1.12.62
=======

* api-change:``ec2``: Update ec2 client to latest version
* enhancement:AssumeRole: Add support for duration_seconds when assuming a role in the config file (`#1600 <https://github.com/boto/botocore/issues/1600>`__).
* api-change:``iam``: Update iam client to latest version
* api-change:``servicecatalog``: Update servicecatalog client to latest version
* api-change:``alexaforbusiness``: Update alexaforbusiness client to latest version


1.12.61
=======

* api-change:``elbv2``: Update elbv2 client to latest version
* api-change:``medialive``: Update medialive client to latest version
* api-change:``codebuild``: Update codebuild client to latest version
* api-change:``rds``: Update rds client to latest version


1.12.60
=======

* api-change:``mq``: Update mq client to latest version
* api-change:``ce``: Update ce client to latest version
* api-change:``mediatailor``: Update mediatailor client to latest version


1.12.59
=======

* api-change:``health``: Update health client to latest version
* api-change:``s3``: Update s3 client to latest version


1.12.58
=======

* api-change:``devicefarm``: Update devicefarm client to latest version
* api-change:``storagegateway``: Update storagegateway client to latest version
* api-change:``mediaconvert``: Update mediaconvert client to latest version
* api-change:``servicecatalog``: Update servicecatalog client to latest version


1.12.57
=======

* bugfix:s3: Add md5 header injection to new operations that require it
* api-change:``s3``: Update s3 client to latest version


1.12.56
=======

* api-change:``elbv2``: Update elbv2 client to latest version
* api-change:``stepfunctions``: Update stepfunctions client to latest version
* api-change:``xray``: Update xray client to latest version
* api-change:``lambda``: Update lambda client to latest version
* api-change:``events``: Update events client to latest version
* api-change:``serverlessrepo``: Update serverlessrepo client to latest version
* api-change:``kafka``: Update kafka client to latest version
* api-change:``s3``: Update s3 client to latest version


1.12.55
=======

* api-change:``ec2``: Update ec2 client to latest version
* api-change:``appmesh``: Update appmesh client to latest version
* api-change:``license-manager``: Update license-manager client to latest version
* api-change:``servicediscovery``: Update servicediscovery client to latest version
* api-change:``sagemaker``: Update sagemaker client to latest version
* api-change:``lightsail``: Update lightsail client to latest version


1.12.54
=======

* api-change:``securityhub``: Update securityhub client to latest version
* api-change:``rds``: Update rds client to latest version
* api-change:``fsx``: Update fsx client to latest version
* api-change:``dynamodb``: Update dynamodb client to latest version


1.12.53
=======

* api-change:``meteringmarketplace``: Update meteringmarketplace client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``codedeploy``: Update codedeploy client to latest version
* api-change:``translate``: Update translate client to latest version
* api-change:``logs``: Update logs client to latest version
* api-change:``kinesisanalytics``: Update kinesisanalytics client to latest version
* api-change:``comprehendmedical``: Update comprehendmedical client to latest version
* api-change:``mediaconnect``: Update mediaconnect client to latest version
* api-change:``kinesisanalyticsv2``: Update kinesisanalyticsv2 client to latest version
* api-change:``ecs``: Update ecs client to latest version


1.12.52
=======

* api-change:``iot``: Update iot client to latest version
* api-change:``sms``: Update sms client to latest version
* api-change:``s3``: Update s3 client to latest version
* api-change:``iotanalytics``: Update iotanalytics client to latest version
* api-change:``greengrass``: Update greengrass client to latest version
* api-change:``kms``: Update kms client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``globalaccelerator``: Update globalaccelerator client to latest version


1.12.51
=======

* api-change:``amplify``: Update amplify client to latest version
* api-change:``transfer``: Update transfer client to latest version
* api-change:``snowball``: Update snowball client to latest version
* api-change:``robomaker``: Update robomaker client to latest version
* api-change:``s3``: Update s3 client to latest version
* api-change:``datasync``: Update datasync client to latest version


1.12.50
=======

* api-change:``rekognition``: Update rekognition client to latest version


1.12.49
=======

* api-change:``autoscaling-plans``: Update autoscaling-plans client to latest version
* api-change:``xray``: Update xray client to latest version
* api-change:``devicefarm``: Update devicefarm client to latest version
* api-change:``ssm``: Update ssm client to latest version
* api-change:``medialive``: Update medialive client to latest version
* api-change:``redshift``: Update redshift client to latest version
* api-change:``rds-data``: Update rds-data client to latest version
* api-change:``appsync``: Update appsync client to latest version
* api-change:``cloudwatch``: Update cloudwatch client to latest version
* api-change:``quicksight``: Update quicksight client to latest version
* api-change:``cloudfront``: Update cloudfront client to latest version


1.12.48
=======

* api-change:``lightsail``: Update lightsail client to latest version
* api-change:``workspaces``: Update workspaces client to latest version
* api-change:``workdocs``: Update workdocs client to latest version
* api-change:``batch``: Update batch client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``devicefarm``: Update devicefarm client to latest version
* api-change:``rds``: Update rds client to latest version
* api-change:``cloudformation``: Update cloudformation client to latest version
* api-change:``lambda``: Update lambda client to latest version
* api-change:``config``: Update config client to latest version
* api-change:``cloudtrail``: Update cloudtrail client to latest version
* api-change:``mediaconvert``: Update mediaconvert client to latest version
* api-change:``iot``: Update iot client to latest version


1.12.47
=======

* api-change:``ssm``: Update ssm client to latest version
* api-change:``comprehend``: Update comprehend client to latest version
* api-change:``workspaces``: Update workspaces client to latest version
* api-change:``ce``: Update ce client to latest version
* api-change:``ecs``: Update ecs client to latest version


1.12.46
=======

* api-change:``s3``: Update s3 client to latest version
* api-change:``sms-voice``: Update sms-voice client to latest version
* api-change:``redshift``: Update redshift client to latest version
* api-change:``rds``: Update rds client to latest version
* api-change:``dms``: Update dms client to latest version
* api-change:``codebuild``: Update codebuild client to latest version
* api-change:``s3control``: Update s3control client to latest version
* api-change:``directconnect``: Update directconnect client to latest version
* api-change:``ram``: Update ram client to latest version
* api-change:``pinpoint``: Update pinpoint client to latest version
* api-change:``route53resolver``: Update route53resolver client to latest version
* api-change:``comprehend``: Update comprehend client to latest version
* api-change:``transcribe``: Update transcribe client to latest version
* api-change:``ecs``: Update ecs client to latest version
* api-change:``iam``: Update iam client to latest version


1.12.45
=======

* api-change:``resource-groups``: Update resource-groups client to latest version
* api-change:``autoscaling``: Update autoscaling client to latest version
* api-change:``mediatailor``: Update mediatailor client to latest version
* api-change:``sns``: Update sns client to latest version
* api-change:``sagemaker``: Update sagemaker client to latest version
* api-change:``servicecatalog``: Update servicecatalog client to latest version
* api-change:``ec2``: Update ec2 client to latest version


1.12.44
=======

* api-change:``chime``: Update chime client to latest version
* api-change:``budgets``: Update budgets client to latest version
* api-change:``redshift``: Update redshift client to latest version


1.12.43
=======

* api-change:``polly``: Update polly client to latest version
* api-change:``batch``: Update batch client to latest version
* api-change:``firehose``: Update firehose client to latest version
* api-change:``cloudformation``: Update cloudformation client to latest version
* api-change:``budgets``: Update budgets client to latest version
* api-change:``codepipeline``: Update codepipeline client to latest version
* api-change:``rds``: Update rds client to latest version


1.12.42
=======

* api-change:``mediapackage``: Update mediapackage client to latest version


1.12.41
=======

* api-change:``medialive``: Update medialive client to latest version
* api-change:``dlm``: Update dlm client to latest version
* api-change:``events``: Update events client to latest version


1.12.40
=======

* api-change:``dms``: Update dms client to latest version
* api-change:``ce``: Update ce client to latest version
* api-change:``ec2``: Update ec2 client to latest version


1.12.39
=======

* api-change:``codebuild``: Update codebuild client to latest version
* api-change:``pinpoint``: Update pinpoint client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``pinpoint-email``: Update pinpoint-email client to latest version
* api-change:``apigateway``: Update apigateway client to latest version
* api-change:``waf-regional``: Update waf-regional client to latest version
* bugfix:session config: Added the default session configuration tuples back to session.session_vars_map.


1.12.38
=======

* api-change:``eks``: Update eks client to latest version
* enhancement:Configuration: Added new configuration provider methods allowing for more flexibility in how a botocore session loads a particular configuration value.
* api-change:``serverlessrepo``: Update serverlessrepo client to latest version


1.12.37
=======

* api-change:``rekognition``: Update rekognition client to latest version
* api-change:``clouddirectory``: Update clouddirectory client to latest version


1.12.36
=======

* api-change:``servicecatalog``: Update servicecatalog client to latest version
* enhancement:Exceptions: Add the ability to pickle botocore exceptions (`834 <https://github.com/boto/botocore/issues/834>`__)


1.12.35
=======

* api-change:``mediastore-data``: Update mediastore-data client to latest version
* api-change:``secretsmanager``: Update secretsmanager client to latest version
* api-change:``greengrass``: Update greengrass client to latest version
* api-change:``config``: Update config client to latest version


1.12.34
=======

* api-change:``chime``: Update chime client to latest version
* api-change:``rds``: Update rds client to latest version
* api-change:``dms``: Update dms client to latest version


1.12.33
=======

* api-change:``sagemaker``: Update sagemaker client to latest version
* api-change:``alexaforbusiness``: Update alexaforbusiness client to latest version
* api-change:``ssm``: Update ssm client to latest version


1.12.32
=======

* api-change:``ec2``: Update ec2 client to latest version


1.12.31
=======

* api-change:``codestar``: Update codestar client to latest version
* api-change:``alexaforbusiness``: Update alexaforbusiness client to latest version


1.12.30
=======

* api-change:``ec2``: Update ec2 client to latest version


1.12.29
=======

* api-change:``inspector``: Update inspector client to latest version
* api-change:``shield``: Update shield client to latest version


1.12.28
=======

* api-change:``workspaces``: Update workspaces client to latest version
* api-change:``ssm``: Update ssm client to latest version


1.12.27
=======

* api-change:``medialive``: Update medialive client to latest version
* api-change:``route53``: Update route53 client to latest version
* api-change:``appstream``: Update appstream client to latest version


1.12.26
=======

* api-change:``events``: Update events client to latest version
* api-change:``apigateway``: Update apigateway client to latest version


1.12.25
=======

* api-change:``glue``: Update glue client to latest version
* api-change:``lightsail``: Update lightsail client to latest version
* api-change:``resource-groups``: Update resource-groups client to latest version


1.12.24
=======

* api-change:``rds``: Update rds client to latest version
* api-change:``lambda``: Update lambda client to latest version
* api-change:``servicecatalog``: Update servicecatalog client to latest version


1.12.23
=======

* api-change:``cloudtrail``: Update cloudtrail client to latest version


1.12.22
=======

* api-change:``athena``: Update athena client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``transcribe``: Update transcribe client to latest version
* api-change:``mediaconvert``: Update mediaconvert client to latest version
* api-change:``directconnect``: Update directconnect client to latest version


1.12.21
=======

* api-change:``transcribe``: Update transcribe client to latest version
* api-change:``comprehend``: Update comprehend client to latest version
* api-change:``es``: Update es client to latest version


1.12.20
=======

* enhancement:TLS: Added support for configuring a client certificate and key when establishing TLS connections.
* api-change:``ssm``: Update ssm client to latest version
* bugfix:InstanceMetadataFetcher: Fix failure to retry on empty credentials and invalid JSON returned from IMDS `1049 <https://github.com/boto/botocore/issues/1049>`__ `1403 <https://github.com/boto/botocore/issues/1403>`__


1.12.19
=======

* api-change:``iot``: Update iot client to latest version
* api-change:``iot-jobs-data``: Update iot-jobs-data client to latest version


1.12.18
=======

* api-change:``ds``: Update ds client to latest version


1.12.17
=======

* api-change:``ssm``: Update ssm client to latest version
* api-change:``codebuild``: Update codebuild client to latest version
* enhancement:HTTP Session: Added the ability to enable TCP Keepalive via the shared config file's ``tcp_keepalive`` option.
* api-change:``apigateway``: Update apigateway client to latest version
* api-change:``storagegateway``: Update storagegateway client to latest version


1.12.16
=======

* api-change:``sagemaker``: Update sagemaker client to latest version
* api-change:``secretsmanager``: Update secretsmanager client to latest version


1.12.15
=======

* api-change:``rekognition``: Update rekognition client to latest version
* api-change:``guardduty``: Update guardduty client to latest version


1.12.14
=======

* api-change:``codestar``: Update codestar client to latest version
* api-change:``ec2``: Update ec2 client to latest version


1.12.13
=======

* api-change:``mq``: Update mq client to latest version
* api-change:``apigateway``: Update apigateway client to latest version
* enhancement:Event: Add the `before-send` event which allows finalized requests to be inspected before being sent across the wire and allows for custom responses to be returned.
* api-change:``codecommit``: Update codecommit client to latest version


1.12.12
=======

* api-change:``sqs``: Update sqs client to latest version
* api-change:``glue``: Update glue client to latest version
* api-change:``opsworkscm``: Update opsworkscm client to latest version
* api-change:``rds``: Update rds client to latest version


1.12.11
=======

* api-change:``ec2``: Update ec2 client to latest version
* api-change:``cloudfront``: Update cloudfront client to latest version
* api-change:``ds``: Update ds client to latest version


1.12.10
=======

* api-change:``connect``: Update connect client to latest version
* api-change:``rds``: Update rds client to latest version


1.12.9
======

* api-change:``mediaconvert``: Update mediaconvert client to latest version


1.12.8
======

* api-change:``rds``: Update rds client to latest version
* api-change:``ds``: Update ds client to latest version
* api-change:``ec2``: Update ec2 client to latest version


1.12.7
======

* api-change:``cloudwatch``: Update cloudwatch client to latest version
* api-change:``s3``: Update s3 client to latest version
* api-change:``organizations``: Update organizations client to latest version


1.12.6
======

* bugfix:Serialization: Fixes `#1557 <https://github.com/boto/botocore/issues/1557>`__. Fixed a regression in serialization where request bodies would be improperly encoded.
* api-change:``es``: Update es client to latest version
* api-change:``rekognition``: Update rekognition client to latest version


1.12.5
======

* api-change:``codebuild``: Update codebuild client to latest version
* api-change:``elastictranscoder``: Update elastictranscoder client to latest version
* api-change:``ecs``: Update ecs client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``cloudwatch``: Update cloudwatch client to latest version
* api-change:``secretsmanager``: Update secretsmanager client to latest version
* api-change:``elasticache``: Update elasticache client to latest version


1.12.4
======

* enhancement:s3: Adds encoding and decoding handlers for ListObjectsV2 `#1552 <https://github.com/boto/botocore/issues/1552>`__
* api-change:``polly``: Update polly client to latest version


1.12.3
======

* api-change:``ses``: Update ses client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``fms``: Update fms client to latest version
* api-change:``connect``: Update connect client to latest version


1.12.2
======

* api-change:``opsworkscm``: Update opsworkscm client to latest version
* api-change:``ssm``: Update ssm client to latest version


1.12.1
======

* api-change:``redshift``: Update redshift client to latest version
* api-change:``cloudhsmv2``: Update cloudhsmv2 client to latest version


1.12.0
======

* api-change:``logs``: Update logs client to latest version
* api-change:``config``: Update config client to latest version
* feature:Events: This migrates the event system to using sevice ids instead of either client name or endpoint prefix. This prevents issues that might arise when a service changes their endpoint prefix, also fixes a long-standing bug where you could not register an event to a particular service if it happened to share its endpoint prefix with another service (e.g. ``autoscaling`` and ``application-autoscaling`` both use the endpoint prefix ``autoscaling``). Please see the `upgrade notes <https://botocore.amazonaws.com/v1/documentation/api/latest/index.html#upgrade-notes>`_ to determine if you are impacted and how to proceed if you are.


1.11.9
======

* api-change:``apigateway``: Update apigateway client to latest version
* api-change:``codecommit``: Update codecommit client to latest version
* api-change:``mediaconvert``: Update mediaconvert client to latest version


1.11.8
======

* api-change:``rds``: Update rds client to latest version
* api-change:``s3``: Update s3 client to latest version
* api-change:``appstream``: Update appstream client to latest version
* api-change:``dynamodb``: Update dynamodb client to latest version
* api-change:``elb``: Update elb client to latest version


1.11.7
======

* api-change:``rds``: Update rds client to latest version
* api-change:``rekognition``: Update rekognition client to latest version


1.11.6
======

* api-change:``waf-regional``: Update waf-regional client to latest version
* api-change:``waf``: Update waf client to latest version
* api-change:``eks``: Update eks client to latest version


1.11.5
======

* api-change:``codebuild``: Update codebuild client to latest version
* api-change:``sagemaker``: Update sagemaker client to latest version
* bugfix:signing: Fix an issue where mixed endpoint casing could cause a SigV4 signature mismatch.


1.11.4
======

* api-change:``glue``: Update glue client to latest version
* api-change:``sagemaker-runtime``: Update sagemaker-runtime client to latest version
* api-change:``mediapackage``: Update mediapackage client to latest version


1.11.3
======

* api-change:``glue``: Update glue client to latest version
* api-change:``xray``: Update xray client to latest version


1.11.2
======

* api-change:``iot``: Update iot client to latest version
* api-change:``signer``: Update signer client to latest version
* api-change:``redshift``: Update redshift client to latest version
* api-change:``iotanalytics``: Update iotanalytics client to latest version


1.11.1
======

* api-change:``glue``: Update glue client to latest version


1.11.0
======

* api-change:``events``: Update events client to latest version
* api-change:``cognito-idp``: Update cognito-idp client to latest version
* feature:urllib3: The vendored version of requests and urllib3 are no longer being used and botocore now has a direct dependency on newer versions of upstream urllib3.


1.10.84
=======

* api-change:``iot``: Update iot client to latest version
* api-change:``rekognition``: Update rekognition client to latest version
* api-change:``lex-models``: Update lex-models client to latest version
* api-change:``iotanalytics``: Update iotanalytics client to latest version
* api-change:``medialive``: Update medialive client to latest version


1.10.83
=======

* api-change:``snowball``: Update snowball client to latest version


1.10.82
=======

* api-change:``ec2``: Update ec2 client to latest version
* api-change:``dlm``: Update dlm client to latest version
* api-change:``rds``: Update rds client to latest version
* api-change:``elasticbeanstalk``: Update elasticbeanstalk client to latest version


1.10.81
=======

* api-change:``mediaconvert``: Update mediaconvert client to latest version
* api-change:``dynamodb``: Update dynamodb client to latest version


1.10.80
=======

* api-change:``dax``: Update dax client to latest version
* api-change:``secretsmanager``: Update secretsmanager client to latest version
* api-change:``sagemaker``: Update sagemaker client to latest version


1.10.79
=======

* api-change:``discovery``: Update discovery client to latest version
* api-change:``ssm``: Update ssm client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``redshift``: Update redshift client to latest version
* api-change:``mediaconvert``: Update mediaconvert client to latest version


1.10.78
=======

* api-change:``devicefarm``: Update devicefarm client to latest version


1.10.77
=======

* api-change:``es``: Update es client to latest version
* api-change:``autoscaling``: Update autoscaling client to latest version
* api-change:``cloudfront``: Update cloudfront client to latest version


1.10.76
=======

* api-change:``sagemaker``: Update sagemaker client to latest version


1.10.75
=======

* api-change:``rds``: Update rds client to latest version
* api-change:``mediaconvert``: Update mediaconvert client to latest version


1.10.74
=======

* api-change:``rds``: Update rds client to latest version
* api-change:``dax``: Update dax client to latest version
* api-change:``ecs``: Update ecs client to latest version


1.10.73
=======

* api-change:``secretsmanager``: Update secretsmanager client to latest version
* api-change:``ssm``: Update ssm client to latest version


1.10.72
=======

* api-change:``logs``: Update logs client to latest version
* api-change:``codebuild``: Update codebuild client to latest version
* api-change:``ssm``: Update ssm client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``pinpoint``: Update pinpoint client to latest version


1.10.71
=======

* api-change:``health``: Update health client to latest version
* api-change:``dynamodb``: Update dynamodb client to latest version


1.10.70
=======

* api-change:``alexaforbusiness``: Update alexaforbusiness client to latest version


1.10.69
=======

* api-change:``polly``: Update polly client to latest version
* api-change:``ssm``: Update ssm client to latest version
* api-change:``kinesis``: Update kinesis client to latest version
* api-change:``resource-groups``: Update resource-groups client to latest version


1.10.68
=======

* api-change:``storagegateway``: Update storagegateway client to latest version
* api-change:``transcribe``: Update transcribe client to latest version


1.10.67
=======

* api-change:``kms``: Update kms client to latest version
* api-change:``mediaconvert``: Update mediaconvert client to latest version
* api-change:``es``: Update es client to latest version
* api-change:``iot``: Update iot client to latest version
* api-change:``connect``: Update connect client to latest version


1.10.66
=======

* api-change:``directconnect``: Update directconnect client to latest version
* api-change:``glue``: Update glue client to latest version
* api-change:``iot``: Update iot client to latest version
* api-change:``cloudhsmv2``: Update cloudhsmv2 client to latest version
* api-change:``sagemaker``: Update sagemaker client to latest version
* api-change:``mq``: Update mq client to latest version
* enhancment:Timestamp Serialization: Support explicit timestamp serialization per timestamp shape.
* api-change:``glacier``: Update glacier client to latest version


1.10.65
=======

* api-change:``ssm``: Update ssm client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``greengrass``: Update greengrass client to latest version
* api-change:``inspector``: Update inspector client to latest version
* api-change:``codebuild``: Update codebuild client to latest version
* api-change:``redshift``: Update redshift client to latest version


1.10.64
=======

* api-change:``ecs``: Update ecs client to latest version
* api-change:``elbv2``: Update elbv2 client to latest version
* api-change:``ec2``: Update ec2 client to latest version


1.10.63
=======

* api-change:``dynamodb``: Update dynamodb client to latest version


1.10.62
=======

* api-change:``config``: Update config client to latest version
* api-change:``dlm``: Update dlm client to latest version


1.10.61
=======

* api-change:``mediapackage``: Update mediapackage client to latest version


1.10.60
=======

* api-change:``iotanalytics``: Update iotanalytics client to latest version


1.10.59
=======

* api-change:``sagemaker``: Update sagemaker client to latest version
* api-change:``polly``: Update polly client to latest version
* api-change:``comprehend``: Update comprehend client to latest version
* api-change:``snowball``: Update snowball client to latest version


1.10.58
=======

* api-change:``kinesisvideo``: Update kinesisvideo client to latest version
* api-change:``appstream``: Update appstream client to latest version
* api-change:``kinesis-video-archived-media``: Update kinesis-video-archived-media client to latest version


1.10.57
=======

* api-change:``iam``: Update iam client to latest version
* api-change:``dlm``: Update dlm client to latest version
* api-change:``appsync``: Update appsync client to latest version
* api-change:``efs``: Update efs client to latest version
* api-change:``codebuild``: Update codebuild client to latest version
* api-change:``emr``: Update emr client to latest version


1.10.56
=======

* api-change:``ssm``: Update ssm client to latest version
* api-change:``s3``: Update s3 client to latest version
* api-change:``apigateway``: Update apigateway client to latest version
* api-change:``ce``: Update ce client to latest version


1.10.55
=======

* api-change:``ec2``: Update ec2 client to latest version
* api-change:``codebuild``: Update codebuild client to latest version
* api-change:``glue``: Update glue client to latest version
* api-change:``opsworks``: Update opsworks client to latest version
* api-change:``appstream``: Update appstream client to latest version


1.10.54
=======

* api-change:``application-autoscaling``: Update application-autoscaling client to latest version


1.10.53
=======

* api-change:``application-autoscaling``: Update application-autoscaling client to latest version
* api-change:``lambda``: Update lambda client to latest version
* api-change:``dms``: Update dms client to latest version
* api-change:``ce``: Update ce client to latest version
* api-change:``transcribe``: Update transcribe client to latest version


1.10.52
=======

* api-change:``mediaconvert``: Update mediaconvert client to latest version
* api-change:``serverlessrepo``: Update serverlessrepo client to latest version


1.10.51
=======

* api-change:``sagemaker``: Update sagemaker client to latest version
* api-change:``pinpoint``: Update pinpoint client to latest version


1.10.50
=======

* api-change:``ec2``: Update ec2 client to latest version
* api-change:``redshift``: Update redshift client to latest version
* api-change:``acm``: Update acm client to latest version


1.10.49
=======

* api-change:``ssm``: Update ssm client to latest version


1.10.48
=======

* api-change:``elasticbeanstalk``: Update elasticbeanstalk client to latest version
* api-change:``storagegateway``: Update storagegateway client to latest version
* api-change:``lambda``: Update lambda client to latest version


1.10.47
=======

* api-change:``cloudfront``: Update cloudfront client to latest version
* api-change:``comprehend``: Update comprehend client to latest version
* api-change:``codepipeline``: Update codepipeline client to latest version
* api-change:``secretsmanager``: Update secretsmanager client to latest version
* enhancement:StreamingResponses: Add ``iter_lines()`` and ``iter_chunks()`` to streaming responses (`#1195 <https://github.com/boto/botocore/issues/1195>`__)


1.10.46
=======

* api-change:``secretsmanager``: Update secretsmanager client to latest version
* api-change:``s3``: Update s3 client to latest version
* api-change:``inspector``: Update inspector client to latest version


1.10.45
=======

* api-change:``appstream``: Update appstream client to latest version
* api-change:``alexaforbusiness``: Update alexaforbusiness client to latest version


1.10.44
=======

* api-change:``clouddirectory``: Update clouddirectory client to latest version


1.10.43
=======

* api-change:``ssm``: Update ssm client to latest version
* api-change:``macie``: Update macie client to latest version
* api-change:``neptune``: Update neptune client to latest version


1.10.42
=======

* api-change:``acm-pca``: Update acm-pca client to latest version
* api-change:``rds``: Update rds client to latest version
* api-change:``medialive``: Update medialive client to latest version


1.10.41
=======

* api-change:``rekognition``: Update rekognition client to latest version


1.10.40
=======

* api-change:``mediaconvert``: Update mediaconvert client to latest version


1.10.39
=======

* api-change:``iotanalytics``: Update iotanalytics client to latest version
* api-change:``dynamodb``: Update dynamodb client to latest version
* api-change:``apigateway``: Update apigateway client to latest version


1.10.38
=======

* api-change:``ssm``: Update ssm client to latest version
* api-change:``servicecatalog``: Update servicecatalog client to latest version


1.10.37
=======

* api-change:``ecs``: Update ecs client to latest version
* api-change:``devicefarm``: Update devicefarm client to latest version


1.10.36
=======

* api-change:``storagegateway``: Update storagegateway client to latest version
* api-change:``rds``: Update rds client to latest version
* api-change:``clouddirectory``: Update clouddirectory client to latest version


1.10.35
=======

* api-change:``mediatailor``: Update mediatailor client to latest version


1.10.34
=======

* api-change:``medialive``: Update medialive client to latest version


1.10.33
=======

* api-change:``polly``: Update polly client to latest version
* api-change:``ce``: Update ce client to latest version
* api-change:``secretsmanager``: Update secretsmanager client to latest version
* api-change:``shield``: Update shield client to latest version
* api-change:``rds``: Update rds client to latest version


1.10.32
=======

* api-change:``ec2``: Update ec2 client to latest version
* api-change:``sagemaker``: Update sagemaker client to latest version
* api-change:``mgh``: Update mgh client to latest version
* api-change:``mediaconvert``: Update mediaconvert client to latest version
* api-change:``appstream``: Update appstream client to latest version
* api-change:``eks``: Update eks client to latest version


1.10.31
=======

* api-change:``ds``: Update ds client to latest version
* api-change:``mediatailor``: Update mediatailor client to latest version
* api-change:``sns``: Update sns client to latest version
* api-change:``redshift``: Update redshift client to latest version
* api-change:``iot``: Update iot client to latest version


1.10.30
=======

* api-change:``neptune``: Update neptune client to latest version
* api-change:``elbv2``: Update elbv2 client to latest version


1.10.29
=======

* api-change:``pi``: Update pi client to latest version


1.10.28
=======

* api-change:``iot``: Update iot client to latest version
* api-change:``config``: Update config client to latest version
* api-change:``appstream``: Update appstream client to latest version
* api-change:``glue``: Update glue client to latest version


1.10.27
=======

* api-change:``secretsmanager``: Update secretsmanager client to latest version
* api-change:``codebuild``: Update codebuild client to latest version
* api-change:``rds``: Update rds client to latest version
* api-change:``elbv2``: Update elbv2 client to latest version


1.10.26
=======

* api-change:``inspector``: Update inspector client to latest version
* enhancement:Credentials: Disable proxy configuration when fetching container credentials
* api-change:``ecs``: Update ecs client to latest version


1.10.25
=======

* api-change:``cloudformation``: Update cloudformation client to latest version


1.10.24
=======

* api-change:``iot``: Update iot client to latest version
* api-change:``ses``: Update ses client to latest version


1.10.23
=======

* api-change:``ec2``: Update ec2 client to latest version
* api-change:``cognito-idp``: Update cognito-idp client to latest version
* api-change:``codedeploy``: Update codedeploy client to latest version


1.10.22
=======

* api-change:``servicecatalog``: Update servicecatalog client to latest version
* api-change:``secretsmanager``: Update secretsmanager client to latest version


1.10.21
=======

* api-change:``config``: Update config client to latest version


1.10.20
=======

* api-change:``organizations``: Update organizations client to latest version
* api-change:``iot1click-devices``: Update iot1click-devices client to latest version
* api-change:``codebuild``: Update codebuild client to latest version
* api-change:``iot1click-projects``: Update iot1click-projects client to latest version


1.10.19
=======

* api-change:``firehose``: Update firehose client to latest version


1.10.18
=======

* api-change:``gamelift``: Update gamelift client to latest version


1.10.17
=======

* api-change:``rds``: Update rds client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``budgets``: Update budgets client to latest version


1.10.16
=======

* api-change:``rds``: Update rds client to latest version
* api-change:``ec2``: Update ec2 client to latest version


1.10.15
=======

* api-change:``alexaforbusiness``: Update alexaforbusiness client to latest version
* api-change:``s3``: Update s3 client to latest version
* api-change:``budgets``: Update budgets client to latest version
* api-change:``es``: Update es client to latest version


1.10.14
=======

* api-change:``guardduty``: Update guardduty client to latest version


1.10.13
=======

* api-change:``config``: Update config client to latest version
* api-change:``secretsmanager``: Update secretsmanager client to latest version
* api-change:``appsync``: Update appsync client to latest version


1.10.12
=======

* api-change:``acm``: Update acm client to latest version
* api-change:``codepipeline``: Update codepipeline client to latest version
* api-change:``ssm``: Update ssm client to latest version
* api-change:``ec2``: Update ec2 client to latest version


1.10.11
=======

* api-change:``guardduty``: Update guardduty client to latest version
* api-change:``alexaforbusiness``: Update alexaforbusiness client to latest version
* api-change:``route53domains``: Update route53domains client to latest version
* api-change:``workspaces``: Update workspaces client to latest version
* api-change:``sagemaker``: Update sagemaker client to latest version
* api-change:``dynamodb``: Update dynamodb client to latest version


1.10.10
=======

* api-change:``glacier``: Update glacier client to latest version
* api-change:``secretsmanager``: Update secretsmanager client to latest version


1.10.9
======

* api-change:``rekognition``: Update rekognition client to latest version
* api-change:``xray``: Update xray client to latest version
* api-change:``codedeploy``: Update codedeploy client to latest version


1.10.8
======

* api-change:``secretsmanager``: Update secretsmanager client to latest version
* api-change:``elasticbeanstalk``: Update elasticbeanstalk client to latest version


1.10.7
======

* api-change:``iotanalytics``: Update iotanalytics client to latest version
* api-change:``iot``: Update iot client to latest version
* api-change:``autoscaling-plans``: Update autoscaling-plans client to latest version


1.10.6
======

* api-change:``medialive``: Update medialive client to latest version
* api-change:``firehose``: Update firehose client to latest version


1.10.5
======

* api-change:``ce``: Update ce client to latest version
* api-change:``codepipeline``: Update codepipeline client to latest version
* api-change:``ssm``: Update ssm client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``secretsmanager``: Update secretsmanager client to latest version
* api-change:``rds``: Update rds client to latest version
* api-change:``devicefarm``: Update devicefarm client to latest version


1.10.4
======

* api-change:``ssm``: Update ssm client to latest version
* api-change:``workmail``: Update workmail client to latest version
* api-change:``dms``: Update dms client to latest version
* api-change:``mediapackage``: Update mediapackage client to latest version
* api-change:``glue``: Update glue client to latest version


1.10.3
======

* api-change:``clouddirectory``: Update clouddirectory client to latest version


1.10.2
======

* api-change:``batch``: Update batch client to latest version


1.10.1
======

* enhancement:shield: Added paginator for list_protections operation.
* api-change:``ssm``: Update ssm client to latest version


1.10.0
======

* api-change:``s3``: Update s3 client to latest version
* api-change:``sagemaker``: Update sagemaker client to latest version
* api-change:``acm``: Update acm client to latest version
* api-change:``config``: Update config client to latest version
* api-change:``transcribe``: Update transcribe client to latest version
* api-change:``secretsmanager``: Update secretsmanager client to latest version
* api-change:``acm-pca``: Update acm-pca client to latest version
* api-change:``cloudwatch``: Update cloudwatch client to latest version
* feature:s3: Add support for S3 Select. Amazon S3 Select is an Amazon S3 feature that makes it easy to retrieve specific data from the contents of an object using simple SQL expressions without having to retrieve the entire object. With this release of the Amazon S3 SDK, S3 Select API (SelectObjectContent) is now generally available in all public regions. This release supports retrieval of a subset of data using SQL clauses, like SELECT and WHERE, from delimited text files and JSON objects in Amazon S3 through the SelectObjectContent API available in AWS S3 SDK.
* api-change:``fms``: Update fms client to latest version


1.9.23
======

* api-change:``lambda``: Update lambda client to latest version
* api-change:``devicefarm``: Update devicefarm client to latest version
* api-change:``translate``: Update translate client to latest version


1.9.22
======

* api-change:``cloudfront``: Update cloudfront client to latest version
* api-change:``apigateway``: Update apigateway client to latest version
* api-change:``es``: Update es client to latest version


1.9.21
======

* api-change:``connect``: Update connect client to latest version
* api-change:``acm``: Update acm client to latest version


1.9.20
======

* api-change:``greengrass``: Update greengrass client to latest version
* api-change:``cloudformation``: Update cloudformation client to latest version
* api-change:``ssm``: Update ssm client to latest version
* api-change:``alexaforbusiness``: Update alexaforbusiness client to latest version


1.9.19
======

* api-change:``mturk``: Update mturk client to latest version
* api-change:``sts``: Update sts client to latest version
* api-change:``iam``: Update iam client to latest version


1.9.18
======

* api-change:``acm``: Update acm client to latest version


1.9.17
======

* api-change:``dynamodb``: Update dynamodb client to latest version
* bugfix:``s3``: Fix bug where invalid head_object requests would cause an infinite loop (alternate fix to `#1400 <https://github.com/boto/botocore/issues/1400>`__)


1.9.16
======

* api-change:``rds``: Update rds client to latest version


1.9.15
======

* api-change:``ecs``: Update ecs client to latest version
* api-change:``appstream``: Update appstream client to latest version
* api-change:``codebuild``: Update codebuild client to latest version


1.9.14
======

* bugfix:``s3``: Fix regression in redirects in using wrong region


1.9.13
======

* bugfix:s3: Fixed a bug where head object and bucket calls would attempt redirects incorrectly.
* api-change:``serverlessrepo``: Update serverlessrepo client to latest version


1.9.12
======

* api-change:``ce``: Update ce client to latest version
* enhancement:Credentials: Add the ability to disable fetching credentials from EC2 metadata by setting the environment variable AWS_EC2_METADATA_DISABLED to 'true'.
* api-change:``config``: Update config client to latest version
* api-change:``elasticbeanstalk``: Update elasticbeanstalk client to latest version
* api-change:``glue``: Update glue client to latest version
* api-change:``medialive``: Update medialive client to latest version
* bugfix:Credentials: Fix a race condition related to assuming a role for the first time (`#1405 <https://github.com/boto/botocore/pull/1405>`__)
* api-change:``events``: Update events client to latest version
* api-change:``ecs``: Update ecs client to latest version


1.9.11
======

* api-change:``elasticbeanstalk``: Update elasticbeanstalk client to latest version


1.9.10
======

* api-change:``sagemaker``: Update sagemaker client to latest version
* api-change:``organizations``: Update organizations client to latest version
* api-change:``pinpoint``: Update pinpoint client to latest version


1.9.9
=====

* api-change:``lightsail``: Update lightsail client to latest version


1.9.8
=====

* api-change:``servicediscovery``: Update servicediscovery client to latest version


1.9.7
=====

* api-change:``cloudhsmv2``: Update cloudhsmv2 client to latest version
* api-change:``discovery``: Update discovery client to latest version
* api-change:``iot``: Update iot client to latest version
* api-change:``redshift``: Update redshift client to latest version


1.9.6
=====

* api-change:``pinpoint``: Update pinpoint client to latest version
* api-change:``ecs``: Update ecs client to latest version
* api-change:``rds``: Update rds client to latest version
* api-change:``mgh``: Update mgh client to latest version


1.9.5
=====

* api-change:``medialive``: Update medialive client to latest version


1.9.4
=====

* api-change:``ecs``: Update ecs client to latest version


1.9.3
=====

* api-change:``ssm``: Update ssm client to latest version
* api-change:``servicecatalog``: Update servicecatalog client to latest version
* api-change:``events``: Update events client to latest version
* api-change:``storagegateway``: Update storagegateway client to latest version
* api-change:``ec2``: Update ec2 client to latest version


1.9.2
=====

* api-change:``application-autoscaling``: Update application-autoscaling client to latest version


1.9.1
=====

* api-change:``ecr``: Update ecr client to latest version


1.9.0
=====

* enhancement:Stubber: Added the ability to add items to response metadata with the stubber.
* api-change:``sts``: Update sts client to latest version
* api-change:``route53``: Update route53 client to latest version
* feature:``s3``: Default to virtual hosted addressing regardless of signature version (boto/botocore`#1387 <https://github.com/boto/botocore/issues/1387>`__)


1.8.50
======

* api-change:``appstream``: Update appstream client to latest version


1.8.49
======

* api-change:``elbv2``: Update elbv2 client to latest version
* api-change:``ce``: Update ce client to latest version


1.8.48
======

* api-change:``ec2``: Update ec2 client to latest version
* api-change:``serverlessrepo``: Update serverlessrepo client to latest version
* api-change:``codecommit``: Update codecommit client to latest version


1.8.47
======

* api-change:``autoscaling``: Update autoscaling client to latest version
* api-change:``waf-regional``: Update waf-regional client to latest version
* api-change:``waf``: Update waf client to latest version


1.8.46
======

* api-change:``config``: Update config client to latest version


1.8.45
======

* api-change:``rds``: Update rds client to latest version


1.8.44
======

* api-change:``mediaconvert``: Update mediaconvert client to latest version
* api-change:``gamelift``: Update gamelift client to latest version


1.8.43
======

* api-change:``appsync``: Update appsync client to latest version
* api-change:``lex-models``: Update lex-models client to latest version


1.8.42
======

* api-change:``glacier``: Update glacier client to latest version
* api-change:``route53``: Update route53 client to latest version


1.8.41
======

* api-change:``guardduty``: Update guardduty client to latest version
* api-change:``cognito-idp``: Update cognito-idp client to latest version
* api-change:``rds``: Update rds client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``kms``: Update kms client to latest version


1.8.40
======

* api-change:``lex-runtime``: Update lex-runtime client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``lex-models``: Update lex-models client to latest version


1.8.39
======

* api-change:``ds``: Update ds client to latest version
* api-change:``appstream``: Update appstream client to latest version
* api-change:``medialive``: Update medialive client to latest version
* api-change:``budgets``: Update budgets client to latest version
* api-change:``gamelift``: Update gamelift client to latest version
* api-change:``dynamodb``: Update dynamodb client to latest version
* api-change:``dms``: Update dms client to latest version
* api-change:``mediastore``: Update mediastore client to latest version


1.8.38
======

* api-change:``servicediscovery``: Update servicediscovery client to latest version
* api-change:``servicecatalog``: Update servicecatalog client to latest version
* api-change:``ssm``: Update ssm client to latest version
* api-change:``glue``: Update glue client to latest version


1.8.37
======

* api-change:``cloud9``: Update cloud9 client to latest version
* api-change:``acm``: Update acm client to latest version
* api-change:``kinesis``: Update kinesis client to latest version
* api-change:``opsworks``: Update opsworks client to latest version


1.8.36
======

* api-change:``mturk``: Update mturk client to latest version
* api-change:``medialive``: Update medialive client to latest version
* api-change:``devicefarm``: Update devicefarm client to latest version


1.8.35
======

* api-change:``lambda``: Update lambda client to latest version
* api-change:``codebuild``: Update codebuild client to latest version
* api-change:``alexaforbusiness``: Update alexaforbusiness client to latest version
* bugfix:Presign: Fix issue where some events were not fired during the presigning of a request thus not including a variety of customizations (`#1340 <https://github.com/boto/botocore/issues/1340>`__)
* enhancement:Credentials: Improved error message when the source profile for an assume role is misconfigured. Fixes aws/aws-cli`#2763 <https://github.com/aws/aws-cli/issues/2763>`__
* api-change:``guardduty``: Update guardduty client to latest version
* enhancment:Paginator: Added paginators for a number of services where the result key is unambiguous.


1.8.34
======

* api-change:``budgets``: Update budgets client to latest version


1.8.33
======

* api-change:``glue``: Update glue client to latest version
* api-change:``transcribe``: Update transcribe client to latest version


1.8.32
======

* api-change:``sagemaker``: Update sagemaker client to latest version


1.8.31
======

* api-change:``ec2``: Update ec2 client to latest version
* api-change:``autoscaling-plans``: Update autoscaling-plans client to latest version


1.8.30
======

* api-change:``application-autoscaling``: Update application-autoscaling client to latest version
* api-change:``autoscaling-plans``: Update autoscaling-plans client to latest version
* api-change:``rds``: Update rds client to latest version


1.8.29
======

* api-change:``lambda``: Update lambda client to latest version
* enhancement:cloudformation get_template template body ordering: fixes boto/boto3`#1378 <https://github.com/boto/boto3/issues/1378>`__


1.8.28
======

* api-change:``glue``: Update glue client to latest version


1.8.27
======

* api-change:``ssm``: Update ssm client to latest version
* api-change:``elbv2``: Update elbv2 client to latest version
* api-change:``rds``: Update rds client to latest version
* api-change:``elb``: Update elb client to latest version


1.8.26
======

* api-change:``kms``: Update kms client to latest version


1.8.25
======

* api-change:``ds``: Update ds client to latest version


1.8.24
======

* api-change:``route53``: Update route53 client to latest version
* api-change:``discovery``: Update discovery client to latest version
* api-change:``codedeploy``: Update codedeploy client to latest version


1.8.23
======

* api-change:``ssm``: Update ssm client to latest version
* api-change:``inspector``: Update inspector client to latest version
* api-change:``snowball``: Update snowball client to latest version


1.8.22
======

* api-change:``rds``: Update rds client to latest version


1.8.21
======

* api-change:``workspaces``: Update workspaces client to latest version


1.8.20
======

* api-change:``ecs``: Update ecs client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``inspector``: Update inspector client to latest version
* api-change:``sagemaker``: Update sagemaker client to latest version


1.8.19
======

* api-change:``ec2``: Update ec2 client to latest version
* enhancement:Paginator: Added paginator support for lambda list aliases operation.
* api-change:``kinesisanalytics``: Update kinesisanalytics client to latest version
* api-change:``codebuild``: Update codebuild client to latest version


1.8.18
======

* api-change:``iot``: Update iot client to latest version
* api-change:``config``: Update config client to latest version


1.8.17
======

* api-change:``route53``: Update route53 client to latest version
* api-change:``apigateway``: Update apigateway client to latest version
* api-change:``mediastore-data``: Update mediastore-data client to latest version


1.8.16
======

* bugfix:presigned-url: Fixes a bug where content-type would be set on presigned requests for query services.
* api-change:``cloudwatch``: Update cloudwatch client to latest version


1.8.15
======

* api-change:``appstream``: Update appstream client to latest version


1.8.14
======

* api-change:``ses``: Update ses client to latest version
* enhancement:credentials: Moved the JSONFileCache from the CLI into botocore so that it can be used without importing from the cli.
* api-change:``apigateway``: Update apigateway client to latest version


1.8.13
======

* api-change:``codedeploy``: Update codedeploy client to latest version
* bugfix:sagemaker-runtime: Renamed the runtime.sagemaker service to sagemaker-runtime to be more consistent with existing services. The old service name is now aliased to sagemaker-runtime to maintain backwards compatibility.
* bugfix:Stubber: This change makes the error handling more verbose in the case where  a stubbed method has been called, but the Stubber is not expecting a call.
* api-change:``workmail``: Update workmail client to latest version


1.8.12
======

* api-change:``sagemaker``: Update sagemaker client to latest version
* api-change:``cognito-idp``: Update cognito-idp client to latest version
* api-change:``lex-models``: Update lex-models client to latest version


1.8.11
======

* api-change:``cloudwatch``: Update cloudwatch client to latest version
* api-change:``appstream``: Update appstream client to latest version
* api-change:``ecs``: Update ecs client to latest version


1.8.10
======

* api-change:``ses``: Update ses client to latest version
* api-change:``es``: Update es client to latest version


1.8.9
=====

* api-change:``elasticbeanstalk``: Update elasticbeanstalk client to latest version
* api-change:``clouddirectory``: Update clouddirectory client to latest version


1.8.8
=====

* api-change:``iot``: Update iot client to latest version
* api-change:``servicediscovery``: Update servicediscovery client to latest version
* api-change:``servicecatalog``: Update servicecatalog client to latest version


1.8.7
=====

* api-change:``budgets``: Update budgets client to latest version
* api-change:``ecs``: Update ecs client to latest version


1.8.6
=====

* api-change:``cloud9``: Update cloud9 client to latest version
* api-change:``lambda``: Update lambda client to latest version
* api-change:``apigateway``: Update apigateway client to latest version
* api-change:``alexaforbusiness``: Update alexaforbusiness client to latest version
* api-change:``serverlessrepo``: Update serverlessrepo client to latest version
* api-change:``ec2``: Update ec2 client to latest version


1.8.5
=====

* api-change:``autoscaling``: Update autoscaling client to latest version
* api-change:``waf``: Update waf client to latest version
* api-change:``waf-regional``: Update waf-regional client to latest version
* api-change:``resource-groups``: Update resource-groups client to latest version
* api-change:``ssm``: Update ssm client to latest version
* api-change:``lightsail``: Update lightsail client to latest version
* api-change:``ec2``: Update ec2 client to latest version


1.8.4
=====

* api-change:``kinesis-video-media``: Update kinesis-video-media client to latest version
* api-change:``translate``: Update translate client to latest version
* api-change:``sagemaker``: Update sagemaker client to latest version
* api-change:``iot-jobs-data``: Update iot-jobs-data client to latest version
* api-change:``s3``: Update s3 client to latest version
* api-change:``ecs``: Update ecs client to latest version
* api-change:``runtime.sagemaker``: Update runtime.sagemaker client to latest version
* api-change:``kinesisvideo``: Update kinesisvideo client to latest version
* api-change:``comprehend``: Update comprehend client to latest version
* api-change:``greengrass``: Update greengrass client to latest version
* api-change:``glacier``: Update glacier client to latest version
* api-change:``kinesis-video-archived-media``: Update kinesis-video-archived-media client to latest version
* api-change:``dynamodb``: Update dynamodb client to latest version
* bugfix:Credentials: Fixed a bug causing issues in configuring the process provider on windows when paths were used.
* api-change:``iot``: Update iot client to latest version
* api-change:``rekognition``: Update rekognition client to latest version


1.8.3
=====

* api-change:``apigateway``: Update apigateway client to latest version
* api-change:``appsync``: Update appsync client to latest version
* api-change:``cognito-idp``: Update cognito-idp client to latest version
* api-change:``guardduty``: Update guardduty client to latest version
* api-change:``batch``: Update batch client to latest version
* bugfix:rekognition: Fixed a bug causing the rekognition paginator to not return FaceModelVersions.
* api-change:``lambda``: Update lambda client to latest version
* api-change:``mq``: Update mq client to latest version
* api-change:``codedeploy``: Update codedeploy client to latest version
* bugfix:Credentials: Fixes an issue where cache keys would be too long to use as file names.
* api-change:``ec2``: Update ec2 client to latest version


1.8.2
=====

* api-change:``mediapackage``: Update mediapackage client to latest version
* api-change:``medialive``: Update medialive client to latest version
* api-change:``mediastore``: Update mediastore client to latest version
* api-change:``mediaconvert``: Update mediaconvert client to latest version
* api-change:``mediastore-data``: Update mediastore-data client to latest version


1.8.1
=====

* bugfix:Credentials: Fixes a bug causing cached credentials to break in the CLI on Windows. Fixes aws/aws-cli`#2978 <https://github.com/boto/botocore/issues/2978>`__
* api-change:``acm``: Update acm client to latest version


1.8.0
=====

* api-change:``rekognition``: Update rekognition client to latest version
* api-change:``emr``: Update emr client to latest version
* api-change:``xray``: Update xray client to latest version
* feature:Credentials: When creating an assume role profile, you can now specify a credential source outside of the config file using the `credential_source` key.
* api-change:``shield``: Update shield client to latest version
* api-change:``cloudformation``: Update cloudformation client to latest version
* feature:Credentials: When creating an assume role profile, you can now specify another assume role profile as the source. This allows for chaining assume role calls.
* api-change:``codebuild``: Update codebuild client to latest version
* feature:credentials: Adds support for the process credential provider, allowing users to specify a process to call to get credentials.
* api-change:``apigateway``: Update apigateway client to latest version
* api-change:``storagegateway``: Update storagegateway client to latest version
* enhancement:Response: Allow reads of zero on streaming bodies, fixes `#1309 <https://github.com/boto/botocore/issues/1309>`__.


1.7.48
======

* api-change:``workdocs``: Update workdocs client to latest version
* api-change:``kinesis``: Update kinesis client to latest version
* api-change:``codecommit``: Update codecommit client to latest version
* api-change:``apigateway``: Update apigateway client to latest version
* api-change:``firehose``: Update firehose client to latest version
* api-change:``ce``: Update ce client to latest version


1.7.47
======

* api-change:``s3``: Update s3 client to latest version
* api-change:``dms``: Update dms client to latest version
* api-change:``rds``: Update rds client to latest version
* api-change:``elbv2``: Update elbv2 client to latest version
* api-change:``application-autoscaling``: Update application-autoscaling client to latest version


1.7.46
======

* api-change:``opsworkscm``: Update opsworkscm client to latest version
* api-change:``route53``: Update route53 client to latest version
* api-change:``glue``: Update glue client to latest version
* api-change:``organizations``: Update organizations client to latest version
* api-change:``application-autoscaling``: Update application-autoscaling client to latest version
* api-change:``ec2``: Update ec2 client to latest version


1.7.45
======

* api-change:``ses``: Update ses client to latest version
* api-change:``apigateway``: Update apigateway client to latest version
* api-change:``stepfunctions``: Update stepfunctions client to latest version
* api-change:``polly``: Update polly client to latest version


1.7.44
======

* api-change:``ecs``: Update ecs client to latest version
* api-change:``lightsail``: Update lightsail client to latest version
* api-change:``ssm``: Update ssm client to latest version
* api-change:``route53``: Update route53 client to latest version


1.7.43
======

* api-change:``ec2``: Update ec2 client to latest version


1.7.42
======

* api-change:``application-autoscaling``: Update application-autoscaling client to latest version
* api-change:``elasticache``: Update elasticache client to latest version
* api-change:``batch``: Update batch client to latest version
* api-change:``ec2``: Update ec2 client to latest version


1.7.41
======

* api-change:``elbv2``: Update elbv2 client to latest version
* api-change:``s3``: Update s3 client to latest version
* api-change:``rds``: Update rds client to latest version


1.7.40
======

* api-change:``stepfunctions``: Update stepfunctions client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``kms``: Update kms client to latest version
* api-change:``organizations``: Update organizations client to latest version
* api-change:``pricing``: Update pricing client to latest version


1.7.39
======

* api-change:``ecs``: Update ecs client to latest version


1.7.38
======

* api-change:``apigateway``: Update apigateway client to latest version


1.7.37
======

* api-change:``acm``: Update acm client to latest version
* api-change:``cloudhsmv2``: Update cloudhsmv2 client to latest version
* api-change:``directconnect``: Update directconnect client to latest version


1.7.36
======

* api-change:``ec2``: Update ec2 client to latest version
* api-change:``cloudfront``: Update cloudfront client to latest version


1.7.35
======

* api-change:``elasticache``: Update elasticache client to latest version
* api-change:``pinpoint``: Update pinpoint client to latest version
* api-change:``config``: Update config client to latest version
* api-change:``glue``: Update glue client to latest version


1.7.34
======

* api-change:``organizations``: Update organizations client to latest version


1.7.33
======

* api-change:``ec2``: Update ec2 client to latest version


1.7.32
======

* api-change:``ssm``: Update ssm client to latest version
* bugfix:sigv4: Strip out the default port and http auth info when computing the host header for sigv4 signing.
* api-change:``sqs``: Update sqs client to latest version


1.7.31
======

* api-change:``lightsail``: Update lightsail client to latest version


1.7.30
======

* api-change:``es``: Update es client to latest version


1.7.29
======

* api-change:``waf``: Update waf client to latest version
* api-change:``cloudhsm``: Update cloudhsm client to latest version
* api-change:``es``: Update es client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``waf-regional``: Update waf-regional client to latest version
* api-change:``rds``: Update rds client to latest version


1.7.28
======

* api-change:``polly``: Update polly client to latest version
* api-change:``dms``: Update dms client to latest version
* api-change:``codecommit``: Update codecommit client to latest version
* api-change:``elasticbeanstalk``: Update elasticbeanstalk client to latest version
* bugfix:Paginator: Fixes an issue when `build_full_result` is used repeatedly that results in the same token being returned multiple times.
* api-change:``rds``: Update rds client to latest version


1.7.27
======

* api-change:``ecr``: Update ecr client to latest version
* api-change:``ses``: Update ses client to latest version


1.7.26
======

* api-change:``ec2``: Update ec2 client to latest version
* api-change:``elbv2``: Update elbv2 client to latest version
* api-change:``opsworkscm``: Update opsworkscm client to latest version


1.7.25
======

* api-change:``sqs``: Update sqs client to latest version
* bugfix:serializer: Update query serializer to automatically include the application/x-www-form-urlencoded; charset=utf-8 Content-Type header.


1.7.24
======

* api-change:``redshift``: Update redshift client to latest version


1.7.23
======

* api-change:``route53domains``: Update route53domains client to latest version
* api-change:``kinesisanalytics``: Update kinesisanalytics client to latest version


1.7.22
======

* api-change:``ssm``: Update ssm client to latest version
* api-change:``ec2``: Update ec2 client to latest version


1.7.21
======

* api-change:``cloudhsm``: Update cloudhsm client to latest version


1.7.20
======

* api-change:``organizations``: Update organizations client to latest version
* api-change:``route53``: Update route53 client to latest version
* api-change:``codebuild``: Update codebuild client to latest version
* api-change:``mturk``: Update mturk client to latest version
* api-change:``appstream``: Update appstream client to latest version


1.7.19
======

* api-change:``pinpoint``: Update pinpoint client to latest version


1.7.18
======

* api-change:``cloudformation``: Update cloudformation client to latest version


1.7.17
======

* api-change:``config``: Update config client to latest version
* api-change:``ecs``: Update ecs client to latest version
* api-change:``rds``: Update rds client to latest version


1.7.16
======

* api-change:``ec2``: Update ec2 client to latest version
* api-change:``logs``: Update logs client to latest version
* api-change:``budgets``: Update budgets client to latest version


1.7.15
======

* api-change:``appstream``: Update appstream client to latest version
* api-change:``greengrass``: Update greengrass client to latest version
* api-change:``rds``: Update rds client to latest version
* api-change:``codepipeline``: Update codepipeline client to latest version
* api-change:``lex-runtime``: Update lex-runtime client to latest version


1.7.14
======

* api-change:``ec2``: Update ec2 client to latest version


1.7.13
======

* api-change:``ec2``: Update ec2 client to latest version
* api-change:``iam``: Update iam client to latest version
* api-change:``ses``: Update ses client to latest version


1.7.12
======

* api-change:``apigateway``: Update apigateway client to latest version


1.7.11
======

* api-change:``servicecatalog``: Update servicecatalog client to latest version
* api-change:``codebuild``: Update codebuild client to latest version
* api-change:``organizations``: Update organizations client to latest version


1.7.10
======

* api-change:``autoscaling``: Update autoscaling client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``batch``: Update batch client to latest version
* api-change:``events``: Update events client to latest version


1.7.9
=====

* api-change:``ec2``: Update ec2 client to latest version


1.7.8
=====

* api-change:``devicefarm``: Update devicefarm client to latest version


1.7.7
=====

* api-change:``logs``: Update logs client to latest version


1.7.6
=====

* api-change:``ec2``: Update ec2 client to latest version
* api-change:``lex-models``: Update lex-models client to latest version
* api-change:``application-autoscaling``: Update application-autoscaling client to latest version
* api-change:``elbv2``: Update elbv2 client to latest version
* api-change:``route53``: Update route53 client to latest version


1.7.5
=====

* api-change:``budgets``: Update budgets client to latest version


1.7.4
=====

* api-change:``codestar``: Update codestar client to latest version


1.7.3
=====

* api-change:``ssm``: Update ssm client to latest version
* api-change:``mobile``: Update mobile client to latest version
* api-change:``gamelift``: Update gamelift client to latest version


1.7.2
=====

* api-change:``codebuild``: Update codebuild client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``elbv2``: Update elbv2 client to latest version
* api-change:``lex-models``: Update lex-models client to latest version


1.7.1
=====

* api-change:``application-autoscaling``: Update application-autoscaling client to latest version
* api-change:``organizations``: Update organizations client to latest version


1.7.0
=====

* api-change:``ec2``: Update ec2 client to latest version
* feature:Waiter: Expose configurable waiter interface
* api-change:``config``: Update config client to latest version


1.6.8
=====

* api-change:``gamelift``: Update gamelift client to latest version
* api-change:``cloudformation``: Update cloudformation client to latest version
* api-change:``rds``: Update rds client to latest version


1.6.7
=====

* api-change:``rekognition``: Update rekognition client to latest version


1.6.6
=====

* api-change:``appstream``: Update appstream client to latest version


1.6.5
=====

* bugfix:Paginator: Fix Athena GetQueryResults paginator
* api-change:``ssm``: Update ssm client to latest version


1.6.4
=====

* api-change:``route53``: Update route53 client to latest version
* api-change:``firehose``: Update firehose client to latest version


1.6.3
=====

* api-change:``gamelift``: Update gamelift client to latest version


1.6.2
=====

* api-change:``ec2``: Update ec2 client to latest version


1.6.1
=====

* api-change:``cloudhsmv2``: Update cloudhsmv2 client to latest version
* api-change:``ssm``: Update ssm client to latest version
* api-change:``glue``: Update glue client to latest version
* api-change:``mgh``: Update mgh client to latest version
* api-change:``efs``: Update efs client to latest version
* api-change:``storagegateway``: Update storagegateway client to latest version
* api-change:``batch``: Update batch client to latest version


1.6.0
=====

* api-change:``ec2``: Update ec2 client to latest version
* feature:retries: Add ability to configure the maximum amount of retry attempts a client call can make. (`#1260 <https://github.com/boto/botocore/pull/1260>`__)
* api-change:``cognito-idp``: Update cognito-idp client to latest version
* api-change:``codedeploy``: Update codedeploy client to latest version


1.5.95
======

* api-change:``clouddirectory``: Update clouddirectory client to latest version
* api-change:``codebuild``: Update codebuild client to latest version


1.5.94
======

* api-change:``rds``: Update rds client to latest version


1.5.93
======

* bugfix:Paginator: Ensure that the page size type matches the type expected by the service. Fixes `#1063 <https://github.com/boto/botocore/issues/1063>`__.
* bugfix:Exceptions: Default to 'Unknown' when error response is missing 'Error' key
* api-change:``elasticbeanstalk``: Update elasticbeanstalk client to latest version


1.5.92
======

* api-change:``ses``: Update ses client to latest version
* api-change:``pinpoint``: Update pinpoint client to latest version
* api-change:``codedeploy``: Update codedeploy client to latest version
* api-change:``config``: Update config client to latest version


1.5.91
======

* api-change:``ssm``: Update ssm client to latest version
* api-change:``inspector``: Update inspector client to latest version


1.5.90
======

* api-change:``ec2``: Update ec2 client to latest version
* api-change:``kinesisanalytics``: Update kinesisanalytics client to latest version


1.5.89
======

* api-change:``dynamodb``: Update dynamodb client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``cloudwatch``: Update cloudwatch client to latest version


1.5.88
======

* api-change:``clouddirectory``: Update clouddirectory client to latest version
* api-change:``cloudformation``: Update cloudformation client to latest version


1.5.87
======

* api-change:``appstream``: Update appstream client to latest version
* api-change:``ec2``: Update ec2 client to latest version


1.5.86
======

* api-change:``emr``: Update emr client to latest version


1.5.85
======

* api-change:``budgets``: Update budgets client to latest version


1.5.84
======

* api-change:``lambda``: Update lambda client to latest version
* bugfix:Paginator: Fixed a bug causing running `build_full_results` multiple times to incorrectly generate the `NextToken` value.
* api-change:``cognito-idp``: Update cognito-idp client to latest version


1.5.83
======

* api-change:``discovery``: Update discovery client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``marketplacecommerceanalytics``: Update marketplacecommerceanalytics client to latest version


1.5.82
======

* api-change:``ec2``: Update ec2 client to latest version
* api-change:``apigateway``: Update apigateway client to latest version
* api-change:``lex-models``: Update lex-models client to latest version


1.5.81
======

* enhancement:SSM: Added a paginator for describe_parameters.
* enchancement:Organizations: Added paginators for Organizations.
* enhancement:IoT: Add paginators for IoT.
* api-change:``swf``: Update swf client to latest version
* api-change:``autoscaling``: Update autoscaling client to latest version
* enhancement:Athena: Added paginators for Athena.


1.5.80
======

* api-change:``kinesis``: Update kinesis client to latest version
* api-change:``kms``: Update kms client to latest version
* api-change:``ds``: Update ds client to latest version
* api-change:``ssm``: Update ssm client to latest version


1.5.79
======

* api-change:``cloudwatch``: Update cloudwatch client to latest version
* api-change:``route53``: Update route53 client to latest version


1.5.78
======

* api-change:``s3``: Update s3 client to latest version
* api-change:``marketplacecommerceanalytics``: Update marketplacecommerceanalytics client to latest version


1.5.77
======

* api-change:``ssm``: Update ssm client to latest version
* api-change:``gamelift``: Update gamelift client to latest version
* api-change:``events``: Update events client to latest version


1.5.76
======

* bugfix:Config: Fixes a bug resulting from copy/deepcopy not returning the same object for botocore.UNSIGNED. Fixes boto/boto3`#1144 <https://github.com/boto/botocore/issues/1144>`__
* api-change:``servicecatalog``: Update servicecatalog client to latest version


1.5.75
======

* api-change:``lambda``: Update lambda client to latest version


1.5.74
======

* api-change:``lightsail``: Update lightsail client to latest version
* api-change:``route53``: Update route53 client to latest version
* api-change:``codepipeline``: Update codepipeline client to latest version
* api-change:``dms``: Update dms client to latest version


1.5.73
======

* api-change:``dax``: Update dax client to latest version
* api-change:``waf``: Update waf client to latest version
* api-change:``ssm``: Update ssm client to latest version
* api-change:``route53``: Update route53 client to latest version
* api-change:``waf-regional``: Update waf-regional client to latest version


1.5.72
======

* api-change:``workdocs``: Update workdocs client to latest version


1.5.71
======

* enhancement:s3: All S3 requests will now use SigV4 by default so that we can take advantage of stronger security algorithms and improved access key isolation.
* api-change:``organizations``: Update organizations client to latest version


1.5.70
======

* api-change:``xray``: Update xray client to latest version


1.5.69
======

* api-change:``iot``: Update iot client to latest version
* api-change:``servicecatalog``: Update servicecatalog client to latest version
* api-change:``ecs``: Update ecs client to latest version
* api-change:``ec2``: Update ec2 client to latest version


1.5.68
======

* api-change:``clouddirectory``: Update clouddirectory client to latest version
* api-change:``application-autoscaling``: Update application-autoscaling client to latest version


1.5.67
======

* api-change:``config``: Update config client to latest version


1.5.66
======

* api-change:``rds``: Update rds client to latest version


1.5.65
======

* api-change:``opsworks``: Update opsworks client to latest version


1.5.64
======

* api-change:``rekognition``: Update rekognition client to latest version
* api-change:``iot``: Update iot client to latest version
* api-change:``pinpoint``: Update pinpoint client to latest version


1.5.63
======

* api-change:``greengrass``: Update greengrass client to latest version
* api-change:``codebuild``: Update codebuild client to latest version


1.5.62
======

* api-change:``cloudfront``: Update cloudfront client to latest version
* api-change:``iot``: Update iot client to latest version
* api-change:``acm``: Update acm client to latest version


1.5.61
======

* api-change:``iot``: Update iot client to latest version
* api-change:``appstream``: Update appstream client to latest version


1.5.60
======

* api-change:``workdocs``: Update workdocs client to latest version
* api-change:``kinesisanalytics``: Update kinesisanalytics client to latest version


1.5.59
======

* api-change:``cognito-idp``: Update cognito-idp client to latest version
* api-change:``codedeploy``: Update codedeploy client to latest version
* api-change:``lex-models``: Update lex-models client to latest version
* api-change:``elbv2``: Update elbv2 client to latest version


1.5.58
======

* api-change:``rds``: Update rds client to latest version


1.5.57
======

* api-change:``clouddirectory``: Update clouddirectory client to latest version


1.5.56
======

* api-change:``appstream``: Update appstream client to latest version
* api-change:``rekognition``: Update rekognition client to latest version


1.5.55
======

* api-change:``storagegateway``: Update storagegateway client to latest version
* api-change:``iam``: Update iam client to latest version
* api-change:``sts``: Update sts client to latest version


1.5.54
======

* api-change:``dms``: Update dms client to latest version


1.5.53
======

* api-change:``resourcegroupstaggingapi``: Update resourcegroupstaggingapi client to latest version


1.5.52
======

* api-change:``athena``: Update athena client to latest version
* api-change:``lightsail``: Update lightsail client to latest version


1.5.51
======

* api-change:``polly``: Update polly client to latest version
* api-change:``autoscaling``: Update autoscaling client to latest version
* api-change:``events``: Update events client to latest version
* api-change:``logs``: Update logs client to latest version


1.5.50
======

* api-change:``gamelift``: Update gamelift client to latest version
* api-change:``codedeploy``: Update codedeploy client to latest version
* api-change:``inspector``: Update inspector client to latest version
* api-change:``kms``: Update kms client to latest version


1.5.49
======

* api-change:``ssm``: Update ssm client to latest version


1.5.48
======

* api-change:``lex-models``: Update lex-models client to latest version
* api-change:``elb``: Update elb client to latest version
* api-change:``organizations``: Update organizations client to latest version
* api-change:``elbv2``: Update elbv2 client to latest version


1.5.47
======

* api-change:``codestar``: Update codestar client to latest version
* api-change:``workspaces``: Update workspaces client to latest version
* enhancement:Credentials: Add support for environment variable credential expiration.


1.5.46
======

* api-change:``marketplace-entitlement``: Update marketplace-entitlement client to latest version
* api-change:``lambda``: Update lambda client to latest version
* api-change:``ecs``: Update ecs client to latest version


1.5.45
======

* api-change:``cloudformation``: Update cloudformation client to latest version
* api-change:``snowball``: Update snowball client to latest version
* api-change:``sqs``: Update sqs client to latest version
* api-change:``rekognition``: Update rekognition client to latest version
* bugfix:Paginator: Fixes bug where pagination would fail if the pagination token contained bytes.
* api-change:``rds``: Update rds client to latest version


1.5.44
======

* enhancement:rds: Add rds database presigner.
* api-change:``rds``: Update rds client to latest version


1.5.43
======

* api-change:``appstream``: Update appstream client to latest version
* bugfix:Auth: Fix bug in Signature Version 4 signer when a header value has consecutive spaces
* api-change:``kinesis``: Update kinesis client to latest version


1.5.42
======

* api-change:``route53``: Update route53 client to latest version
* api-change:``directconnect``: Update directconnect client to latest version
* api-change:``devicefarm``: Update devicefarm client to latest version
* api-change:``kms``: Update kms client to latest version
* api-change:``route53domains``: Update route53domains client to latest version


1.5.41
======

* api-change:``codestar``: Update codestar client to latest version
* api-change:``lambda``: Update lambda client to latest version
* api-change:``apigateway``: Update apigateway client to latest version
* api-change:``lex-models``: Update lex-models client to latest version
* api-change:``iam``: Update iam client to latest version
* api-change:``rekognition``: Update rekognition client to latest version
* api-change:``polly``: Update polly client to latest version
* api-change:``ec2``: Update ec2 client to latest version


1.5.40
======

* bugfix:mturk: Fix naming on list_hits_for_qualification_type for mturk. The old method name will still be supported.
* api-change:``lambda``: Update lambda client to latest version


1.5.39
======

* api-change:``gamelift``: Update gamelift client to latest version
* api-change:``batch``: Update batch client to latest version
* api-change:``apigateway``: Update apigateway client to latest version
* api-change:``opsworks``: Update opsworks client to latest version


1.5.38
======

* api-change:``redshift``: Update redshift client to latest version


1.5.37
======

* api-change:``elbv2``: Update elbv2 client to latest version


1.5.36
======

* api-change:``elasticache``: Update elasticache client to latest version


1.5.35
======

* api-change:``cloudwatch``: Update cloudwatch client to latest version


1.5.34
======

* api-change:``lex-runtime``: Update lex-runtime client to latest version


1.5.33
======

* api-change:``clouddirectory``: Update clouddirectory client to latest version


1.5.32
======

* api-change:``cloudfront``: Update cloudfront client to latest version
* api-change:``storagegateway``: Update storagegateway client to latest version
* api-change:``resourcegroupstaggingapi``: Update resourcegroupstaggingapi client to latest version
* api-change:``cloudformation``: Update cloudformation client to latest version
* api-change:``config``: Update config client to latest version


1.5.31
======

* api-change:``batch``: Update batch client to latest version
* api-change:``ec2``: Update ec2 client to latest version


1.5.30
======

* api-change:``ssm``: Update ssm client to latest version
* bugfix:config: Fix a bug in loading config files from paths that contain non-ascii characters. Fixes aws/aws-cli`#2395 <https://github.com/boto/botocore/issues/2395>`__


1.5.29
======

* api-change:``cloudtrail``: Update cloudtrail client to latest version
* api-change:``application-autoscaling``: Update application-autoscaling client to latest version


1.5.28
======

* api-change:``discovery``: Update discovery client to latest version
* api-change:``lambda``: Update lambda client to latest version


1.5.27
======

* api-change:``pinpoint``: Update pinpoint client to latest version
* api-change:``directconnect``: Update directconnect client to latest version
* enhancement:Credentials: Add support for localhost when using container credential provider (`#1160 <https://github.com/boto/botocore/issues/1160>`__)
* api-change:``codebuild``: Update codebuild client to latest version
* api-change:``marketplacecommerceanalytics``: Update marketplacecommerceanalytics client to latest version
* api-change:``rekognition``: Update rekognition client to latest version


1.5.26
======

* api-change:``budgets``: Update budgets client to latest version
* api-change:``apigateway``: Update apigateway client to latest version
* api-change:``codedeploy``: Update codedeploy client to latest version
* api-change:``events``: Update events client to latest version
* api-change:``rds``: Update rds client to latest version


1.5.25
======

* api-change:``devicefarm``: Update devicefarm client to latest version
* api-change:``events``: Update events client to latest version


1.5.24
======

* api-change:``codedeploy``: Update codedeploy client to latest version
* api-change:``emr``: Update emr client to latest version


1.5.23
======

* api-change:``clouddirectory``: Update clouddirectory client to latest version
* api-change:``apigateway``: Update apigateway client to latest version


1.5.22
======

* api-change:``organizations``: Update organizations client to latest version
* api-change:``workdocs``: Update workdocs client to latest version


1.5.21
======

* api-change:``rds``: Update rds client to latest version


1.5.20
======

* api-change:``budgets``: Update budgets client to latest version
* api-change:``cloudtrail``: Update cloudtrail client to latest version
* api-change:``opsworkscm``: Update opsworkscm client to latest version


1.5.19
======

* api-change:``waf``: Update waf client to latest version
* api-change:``mturk``: Update mturk client to latest version
* api-change:``iam``: Update iam client to latest version
* api-change:``organizations``: Update organizations client to latest version
* api-change:``waf-regional``: Update waf-regional client to latest version
* api-change:``dynamodb``: Update dynamodb client to latest version
* api-change:``gamelift``: Update gamelift client to latest version
* api-change:``elasticbeanstalk``: Update elasticbeanstalk client to latest version
* api-change:``ec2``: Update ec2 client to latest version
* api-change:``dynamodbstreams``: Update dynamodbstreams client to latest version


1.5.18
======

* api-change:``es``: Update es client to latest version


1.5.17
======

* api-change:``ec2``: Update ec2 client to latest version


1.5.16
======

* api-change:``clouddirectory``: Update clouddirectory client to latest version
* api-change:``gamelift``: Update gamelift client to latest version
* api-change:``elasticbeanstalk``: Update elasticbeanstalk client to latest version
* api-change:``route53``: Update route53 client to latest version


1.5.15
======

* api-change:``ec2``: Update ec2 client to latest version


1.5.14
======

* api-change:``directconnect``: Update directconnect client to latest version


1.5.13
======

* api-change:``config``: Update config client to latest version
* api-change:``cognito-identity``: Update cognito-identity client to latest version


1.5.12
======

* feature:``kms``: Update kms client to latest version


1.5.11
======

* feature:``ec2``: Update ec2 client to latest version


1.5.10
======

* feature:``storagegateway``: Update storagegateway client to latest version
* feature:Waiter: Adds several new waiters.
* feature:``clouddirectory``: Update clouddirectory client to latest version
* feature:``lex-runtime``: Update lex-runtime client to latest version


1.5.9
=====

* feature:``rekognition``: Update rekognition client to latest version
* feature:``ec2``: Update ec2 client to latest version


1.5.8
=====

* feature:``lex-runtime``: Update lex-runtime client to latest version
* feature:Paginator: Added paginators for multiple services


1.5.7
=====

* feature:``ec2``: Update ec2 client to latest version
* feature:``clouddirectory``: Update clouddirectory client to latest version
* feature:``codedeploy``: Update codedeploy client to latest version
* feature:``rds``: Update rds client to latest version


1.5.6
=====

* feature:``elbv2``: Update elbv2 client to latest version
* feature:``rds``: Update rds client to latest version


1.5.5
=====

* feature:``codebuild``: Update codebuild client to latest version
* feature:``ecs``: Update ecs client to latest version
* feature:``codecommit``: Update codecommit client to latest version


1.5.4
=====

* feature:``health``: Update health client to latest version
* feature:``acm``: Update acm client to latest version


1.5.3
=====

* feature:``ec2``: Update ec2 client to latest version


1.5.2
=====

* feature:``rds``: Update rds client to latest version


1.5.1
=====

* feature:``glacier``: Update glacier client to latest version
* feature:``dynamodb``: Update dynamodb client to latest version
* feature:``route53``: Update route53 client to latest version
* feature:``polly``: Update polly client to latest version
* feature:``rekognition``: Update rekognition client to latest version


1.5.0
=====

* feature:Exceptions: Add modeled exceptions on client via ``Client.exceptions`` property
* feature:``dynamodb``: Update dynamodb client to latest version
* feature:``config``: Update config client to latest version
* feature:``cur``: Update cur client to latest version
* feature:``elasticache``: Update elasticache client to latest version


1.4.93
======

* feature:``rds``: Update rds client to latest version
* feature:``marketplacecommerceanalytics``: Update marketplacecommerceanalytics client to latest version
* feature:``config``: Update config client to latest version
* feature:``iam``: Update iam client to latest version
* feature:``lambda``: Update lambda client to latest version
* feature:``dynamodbstreams``: Update dynamodbstreams client to latest version
* feature:``efs``: Update efs client to latest version
* feature:``rekognition``: Update rekognition client to latest version


1.4.92
======

* feature:``codedeploy``: Update codedeploy client to latest version
* bugfix:Paginator: Fix a paginator bug involving optional tokens (`#1057 <https://github.com/boto/botocore/issues/1057>`__)
* feature:``ecs``: Update ecs client to latest version


1.4.91
======

* feature:``iam``: Update iam client to latest version
* feature:``apigateway``: Update apigateway client to latest version
* feature:``ds``: Update ds client to latest version
* feature:``elasticbeanstalk``: Update elasticbeanstalk client to latest version
* feature:``kms``: Update kms client to latest version


1.4.90
======

* feature:``rds``: Update rds client to latest version
* feature:``ecr``: Update ecr client to latest version


1.4.89
======

* feature:``storagegateway``: Update storagegateway client to latest version
* feature:``firehose``: Update firehose client to latest version
* feature:``route53``: Update route53 client to latest version


1.4.88
======

* feature:``discovery``: Update discovery client to latest version
* feature:``cognito-identity``: Update cognito-identity client to latest version
* feature:``inspector``: Update inspector client to latest version
* feature:``sqs``: Update sqs client to latest version
* feature:``cloudformation``: Update cloudformation client to latest version


1.4.87
======

* feature:``ssm``: Update ssm client to latest version
* feature:user-agent: Default user agent now includes the environment variable $AWS_EXECUTION_ENVIRONMENT
* bugfix:Python 3.6: Adds compatibility with the new Python 3.6 HTTPConnection.
* bugfix:sigv4: Do not sign x-amzn-trace-id as it can be mutated along the way.
* feature:``cognito-idp``: Update cognito-idp client to latest version


1.4.86
======

* feature:``dms``: Update dms client to latest version
* feature:``rds``: Update rds client to latest version
* feature:``logs``: Update logs client to latest version
* feature:``marketplacecommerceanalytics``: Update marketplacecommerceanalytics client to latest version
* feature:``elasticbeanstalk``: Update elasticbeanstalk client to latest version
* feature:``sts``: Update sts client to latest version
* feature:``batch``: Update batch client to latest version


1.4.85
======

* feature:cloudfront: Add lambda function associations to cache behaviors.
* feature:rds: Add cluster create data to DBCluster APIs.
* feature:waf-regional: With this new feature, customers can use AWS WAF directly on Application Load Balancers in a VPC within available regions to protect their websites and web services from malicious attacks such as SQL injection, Cross Site Scripting, bad bots, etc.


1.4.84
======

* feature:``config``: Update config client to latest version
* feature:health: Add paginators for Health.
* feature:``sqs``: Update sqs client to latest version
* feature:``s3``: Update s3 client to latest version


1.4.83
======

* feature:``pinpoint``: Update pinpoint client to latest version
* feature:``ec2``: Update ec2 client to latest version
* feature:``sts``: Update sts client to latest version
* feature:``config``: Update config client to latest version


1.4.82
======

* bugfix:Exceptions: Allow parsing of json error responses with non-json bodies.
* feature:opsworks-cm: Added waiter for Opsworks CM


1.4.81
======

* feature:parameter: Automatically inject an idempotency token into parameters marked with the idempotencyToken trait
* feature:``appstream``: Update appstream client to latest version
* feature:``directconnect``: Update directconnect client to latest version
* feature:``elasticbeanstalk``: Update elasticbeanstalk client to latest version
* feature:``shield``: Update shield client to latest version
* feature:``opsworkscm``: Update opsworkscm client to latest version
* feature:``lambda``: Update lambda client to latest version
* feature:``codebuild``: Update codebuild client to latest version
* feature:``xray``: Update xray client to latest version
* feature:``stepfunctions``: Update stepfunctions client to latest version
* feature:``ssm``: Update ssm client to latest version
* feature:``health``: Update health client to latest version
* feature:``ec2``: Update ec2 client to latest version
* feature:``apigateway``: Update apigateway client to latest version
* feature:``pinpoint``: Update pinpoint client to latest version


1.4.80
======

* feature:``lightsail``: Update lightsail client to latest version
* feature:``polly``: Update polly client to latest version
* feature:``snowball``: Update snowball client to latest version
* feature:``rekognition``: Update rekognition client to latest version


1.4.79
======

* bugfix:s3: fixes `#1059 <https://github.com/boto/botocore/issues/1059>`__ (presigned s3v4 URL bug related to blank query parameters being filtered incorrectly)
* feature:``s3``: Update s3 client to latest version
* bugfix:Presigner: Support presigning rest-json services.


1.4.78
======

* feature:``s3``: Update s3 client to latest version
* feature:``glacier``: Update glacier client to latest version
* feature:``cloudformation``: Update cloudformation client to latest version
* feature:``route53``: Update route53 client to latest version


1.4.77
======

* feature:``cloudtrail``: Update cloudtrail client to latest version
* feature:``ecs``: Update ecs client to latest version


1.4.76
======

* feature:``application-autoscaling``: Update application-autoscaling client to latest version
* feature:``elastictranscoder``: Update elastictranscoder client to latest version
* feature:``lambda``: Update lambda client to latest version
* feature:``emr``: Update emr client to latest version
* feature:``gamelift``: Update gamelift client to latest version


1.4.75
======

* feature:Loader: Support loading json extra files.
* feature:``meteringmarketplace``: Update meteringmarketplace client to latest version
* feature:``cloudwatch``: Update cloudwatch client to latest version
* feature:``apigateway``: Update apigateway client to latest version
* feature:``sqs``: Update sqs client to latest version


1.4.74
======

* feature:``route53``: Update route53 client to latest version
* feature:``servicecatalog``: Update servicecatalog client to latest version


1.4.73
======

* feature:``kinesis``: Update kinesis client to latest version
* feature:``ds``: Update ds client to latest version
* feature:``elasticache``: Update elasticache client to latest version


1.4.72
======

* feature:``cognito-idp``: Update cognito-idp client to latest version
* feature:Paginator: Add paginators for AWS WAF


1.4.71
======

* bugfix:Parsers: ResponseMetadata will now always be populated, provided the response was able to be parsed into a dict.
* feature:``cloudformation``: Update cloudformation client to latest version
* feature:``logs``: Update logs client to latest version


1.4.70
======

* feature:``directconnect``: Update directconnect client to latest version


1.4.69
======

* feature:``ses``: Update ses client to latest version


1.4.68
======

* feature:``cloudformation``: Update cloudformation client to latest version
* feature:Stub: Made ANY usable for nested parameters


1.4.67
======

* feature:``elbv2``: Update elbv2 client to latest version
* feature:``autoscaling``: Update autoscaling client to latest version


1.4.66
======

* feature:``sms``: Update sms client to latest version
* feature:``ecs``: Update ecs client to latest version


1.4.65
======

* bugfix:Waiters: Add back missing fail fail states to cloudformation waiters (`#1056 <https://github.com/boto/botocore/issues/1056>`__)
* feature:``waf``: Update waf client to latest version
* feature:``budgets``: Update budgets client to latest version


1.4.64
======

* feature:``cloudfront``: Update cloudfront client to latest version
* feature:``iot``: Update iot client to latest version
* feature:``config``: Update config client to latest version
* feature:``rds``: Update rds client to latest version
* feature:``kinesisanalytics``: Update kinesisanalytics client to latest version


1.4.63
======

* feature:``route53``: Update route53 client to latest version
* feature:regions: Add support us-east-2


1.4.62
======

* feature:``elasticbeanstalk``: Update elasticbeanstalk client to latest version
* feature:``acm``: Update acm client to latest version
* feature:``gamelift``: Update gamelift client to latest version


1.4.61
======

* feature:``ecr``: Update ecr client to latest version
* feature:``cloudfront``: Update cloudfront client to latest version
* feature:``codedeploy``: Update codedeploy client to latest version
* feature:``sns``: Update sns client to latest version
* feature:``apigateway``: Update apigateway client to latest version
* feature:Client Meta: Add partition to client meta object (`#1027 <https://github.com/boto/botocore/issues/1027>`__)
* feature:``elasticache``: Update elasticache client to latest version
* feature:``kms``: Update kms client to latest version
* feature:``rds``: Update rds client to latest version
* feature:``gamelift``: Update gamelift client to latest version


1.4.60
======

* feature:``opsworks``: Update opsworks client to latest version
* feature:``devicefarm``: Update devicefarm client to latest version
* feature:``kms``: Update kms client to latest version
* feature:``s3``: Update s3 client to latest version
* feature:``waf``: Update waf client to latest version
* feature:``cognito-idp``: Update cognito-idp client to latest version


1.4.58
======

* feature:``snowball``: Update snowball client to latest version
* feature:``s3``: Update s3 client to latest version
* feature:``ec2``: Update ec2 client to latest version


1.4.57
======

* feature:``cloudformation``: Update cloudformation client to latest version
* feature:``codepipeline``: Update codepipeline client to latest version
* feature:``kms``: Update kms client to latest version
* feature:``efs``: Update efs client to latest version


1.4.56
======

* feature:``redshift``: Update redshift client to latest version
* feature:Stubber: Add ability to specify expected params when using `add_client_error` (`#1025 <https://github.com/boto/botocore/issues/1025>`__)
* feature:``emr``: Update emr client to latest version
* feature:``codedeploy``: Update codedeploy client to latest version
* feature:``rds``: Update rds client to latest version


1.4.55
======

* feature:``iot``: Update iot client to latest version
* feature:``rds``: Update rds client to latest version


1.4.54
======

* feature:EC2: Add `NetworkAclExists` waiter (`#1019 <https://github.com/boto/botocore/issues/1019>`__)
* feature:Paginator: Add paginators for Application Auto Scaling service (`#1029 <https://github.com/boto/botocore/issues/1029>`__)
* feature:Config: Add `max_pool_connections` to client config (`#773 <https://github.com/boto/botocore/issues/773>`__, `#766 <https://github.com/boto/botocore/issues/766>`__, `#1026 <https://github.com/boto/botocore/issues/1026>`__)
* feature:``ec2``: Update ec2 client to latest version
* feature:``servicecatalog``: Update servicecatalog client to latest version


1.4.53
======

* feature:``support``: Update support client to latest version
* feature:``cloudfront``: Update cloudfront client to latest version
* feature:``sns``: Update sns client to latest version


1.4.52
======

* feature:``codepipeline``: Update codepipeline client to latest version
* feature:``ec2``: Update ec2 client to latest version
* feature:``rds``: Update rds client to latest version
* feature:``sns``: Update sns client to latest version
* feature:``ecr``: Update ecr client to latest version


1.4.51
======

* feature:``rds``: Update rds client to latest version
* feature:ResponseMetadata: Add MaxAttemptsReached and RetryAttempts keys to the returned ResonseMetadata dictionary (`#1024 <https://github.com/boto/botocore/issues/1024>`__, `#965 <https://github.com/boto/botocore/issues/965>`__, `#926 <https://github.com/boto/botocore/issues/926>`__)
* feature:``application-autoscaling``: Update application-autoscaling client to latest version
* feature:``cognito-idp``: Update cognito-idp client to latest version
* feature:Waiters: Add last_response attribute to WaiterError (`#1023 <https://github.com/boto/botocore/issues/1023>`__, `#957 <https://github.com/boto/botocore/issues/957>`__)
* feature:``config``: Update config client to latest version
* feature:``gamelift``: Update gamelift client to latest version


1.4.50
======

* feature:``autoscaling``: Update autoscaling client to latest version
* feature:``codepipeline``: Update codepipeline client to latest version
* feature:``ssm``: Update ssm client to latest version
* feature:``cloudfront``: Update cloudfront client to latest version
* feature:``route53``: Update route53 client to latest version


1.4.49
======

* feature:``rds``: Update rds client to latest version
* feature:``opsworks``: Update opsworks client to latest version


1.4.48
======

* feature:``ec2``: Update ec2 client to latest version
* feature:``iam``: Update iam client to latest version
* feature:``workspaces``: Update workspaces client to latest version


1.4.47
======

* feature:``elbv2``: Update elbv2 client to latest version
* feature:``apigateway``: Update apigateway client to latest version
* feature:``ecs``: Update ecs client to latest version
* feature:``acm``: Update acm client to latest version
* feature:``kms``: Update kms client to latest version


1.4.45
======

* feature:``kms``: Update kms client to latest version
* feature:``kinesisanalytics``: Update kinesisanalytics client to latest version
* feature:``autoscaling``: Update autoscaling client to latest version
* feature:``elb``: Update elb client to latest version
* feature:``ecs``: Update ecs client to latest version
* feature:s3: Add support for s3 dualstack configuration
* feature:``snowball``: Update snowball client to latest version
* feature:``elbv2``: Update elbv2 client to latest version


1.4.44
======

* feature:``marketplacecommerceanalytics``: Update marketplacecommerceanalytics client to latest version
* feature:``ecr``: Update ecr client to latest version
* feature:``cloudfront``: Update cloudfront client to latest version


1.4.43
======

* feature:``lambda``: Update lambda client to latest version
* feature:``gamelift``: Update gamelift client to latest version
* feature:``rds``: Update rds client to latest version


1.4.42
======

* bugfix:Serialization: Account for boolean in query string serialization
* feature:``rds``: Update rds client to latest version
* feature:``iot``: Update iot client to latest version
* feature:``ds``: Update ds client to latest version
* feature:``meteringmarketplace``: Update meteringmarketplace client to latest version
* feature:``route53domains``: Update route53domains client to latest version
* feature:``application-autoscaling``: Update application-autoscaling client to latest version
* feature:``emr``: Update emr client to latest version
* feature:``cloudwatch``: Update cloudwatch client to latest version
* feature:``logs``: Update logs client to latest version
* feature:``machinelearning``: Update machinelearning client to latest version


1.4.41
======

* feature:``ds``: Update ds client to latest version
* feature:``ses``: Update ses client to latest version
* bugfix:s3: S3 region redirector will now honor the orginial url scheme.
* feature:``sts``: Update sts client to latest version
* feature:``cognito-idp``: Update cognito-idp client to latest version
* feature:``ec2``: Update ec2 client to latest version
* feature:``es``: Update es client to latest version
* feature:``apigateway``: Update apigateway client to latest version
* bugfix:Credentials: Raise error when partial hard coded creds are provided when creating a client.


1.4.40
======

* feature:``s3``: Update s3 client to latest version
* feature:codedeploy: Add a waiter to wait on successful deployments.
* feature:``iot``: Update iot client to latest version


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

