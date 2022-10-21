=========
CHANGELOG
=========

1.27.96
=======

* api-change:``cognito-idp``: This release adds a new "DeletionProtection" field to the UserPool in Cognito. Application admins can configure this value with either ACTIVE or INACTIVE value. Setting this field to ACTIVE will prevent a user pool from accidental deletion.
* api-change:``sagemaker``: CreateInferenceRecommenderjob API now supports passing endpoint details directly, that will help customers to identify the max invocation and max latency they can achieve for their model and the associated endpoint along with getting recommendations on other instances.


1.27.95
=======

* api-change:``devops-guru``: This release adds information about the resources DevOps Guru is analyzing.
* api-change:``globalaccelerator``: Global Accelerator now supports AddEndpoints and RemoveEndpoints operations for standard endpoint groups.
* api-change:``resiliencehub``: In this release, we are introducing support for regional optimization for AWS Resilience Hub applications. It also includes a few documentation updates to improve clarity.
* api-change:``rum``: CloudWatch RUM now supports Extended CloudWatch Metrics with Additional Dimensions


1.27.94
=======

* api-change:``chime-sdk-messaging``: Documentation updates for Chime Messaging SDK
* api-change:``cloudtrail``: This release includes support for exporting CloudTrail Lake query results to an Amazon S3 bucket.
* api-change:``config``: This release adds resourceType enums for AppConfig, AppSync, DataSync, EC2, EKS, Glue, GuardDuty, SageMaker, ServiceDiscovery, SES, Route53 types.
* api-change:``connect``: This release adds API support for managing phone numbers that can be used across multiple AWS regions through telephony traffic distribution.
* api-change:``events``: Update events client to latest version
* api-change:``managedblockchain``: Adding new Accessor APIs for Amazon Managed Blockchain
* api-change:``s3``: Updates internal logic for constructing API endpoints. We have added rule-based endpoints and internal model parameters.
* api-change:``s3control``: Updates internal logic for constructing API endpoints. We have added rule-based endpoints and internal model parameters.
* api-change:``support-app``: This release adds the RegisterSlackWorkspaceForOrganization API. You can use the API to register a Slack workspace for an AWS account that is part of an organization.
* api-change:``workspaces-web``: WorkSpaces Web now supports user access logging for recording session start, stop, and URL navigation.


1.27.93
=======

* api-change:``frauddetector``: Documentation Updates for Amazon Fraud Detector
* api-change:``sagemaker``: This change allows customers to enable data capturing while running a batch transform job, and configure monitoring schedule to monitoring the captured data.
* api-change:``servicediscovery``: Updated the ListNamespaces API to support the NAME and HTTP_NAME filters, and the BEGINS_WITH filter condition.
* api-change:``sesv2``: This release allows subscribers to enable Dedicated IPs (managed) to send email via a fully managed dedicated IP experience. It also adds identities' VerificationStatus in the response of GetEmailIdentity and ListEmailIdentities APIs, and ImportJobs counts in the response of ListImportJobs API.


1.27.92
=======

* api-change:``greengrass``: This change allows customers to specify FunctionRuntimeOverride in FunctionDefinitionVersion. This configuration can be used if the runtime on the device is different from the AWS Lambda runtime specified for that function.
* api-change:``sagemaker``: This release adds support for C7g, C6g, C6gd, C6gn, M6g, M6gd, R6g, and R6gn Graviton instance types in Amazon SageMaker Inference.


1.27.91
=======

* api-change:``mediaconvert``: MediaConvert now supports specifying the minimum percentage of the HRD buffer available at the end of each encoded video segment.


1.27.90
=======

* api-change:``amplifyuibuilder``: We are releasing the ability for fields to be configured as arrays.
* api-change:``appflow``: With this update, you can choose which Salesforce API is used by Amazon AppFlow to transfer data to or from your Salesforce account. You can choose the Salesforce REST API or Bulk API 2.0. You can also choose for Amazon AppFlow to pick the API automatically.
* api-change:``connect``: This release adds support for a secondary email and a mobile number for Amazon Connect instance users.
* api-change:``ds``: This release adds support for describing and updating AWS Managed Microsoft AD set up.
* api-change:``ecs``: Documentation update to address tickets.
* api-change:``guardduty``: Add UnprocessedDataSources to CreateDetectorResponse which specifies the data sources that couldn't be enabled during the CreateDetector request. In addition, update documentations.
* api-change:``iam``: Documentation updates for the AWS Identity and Access Management API Reference.
* api-change:``iotfleetwise``: Documentation update for AWS IoT FleetWise
* api-change:``medialive``: AWS Elemental MediaLive now supports forwarding SCTE-35 messages through the Event Signaling and Management (ESAM) API, and can read those SCTE-35 messages from an inactive source.
* api-change:``mediapackage-vod``: This release adds SPEKE v2 support for MediaPackage VOD. Speke v2 is an upgrade to the existing SPEKE API to support multiple encryption keys, based on an encryption contract selected by the customer.
* api-change:``panorama``: Pause and resume camera stream processing with SignalApplicationInstanceNodeInstances. Reboot an appliance with CreateJobForDevices. More application state information in DescribeApplicationInstance response.
* api-change:``rds-data``: Doc update to reflect no support for schema parameter on BatchExecuteStatement API
* api-change:``ssm-incidents``: Update RelatedItem enum to support Tasks
* api-change:``ssm``: Support of AmazonLinux2022 by Patch Manager
* api-change:``transfer``: This release adds an option for customers to configure workflows that are triggered when files are only partially received from a client due to premature session disconnect.
* api-change:``translate``: This release enables customers to specify multiple target languages in asynchronous batch translation requests.
* api-change:``wisdom``: This release updates the GetRecommendations API to include a trigger event list for classifying and grouping recommendations.


1.27.89
=======

* api-change:``codeguru-reviewer``: Documentation update to replace broken link.
* api-change:``elbv2``: Update elbv2 client to latest version
* api-change:``greengrassv2``: This release adds error status details for deployments and components that failed on a device and adds features to improve visibility into component installation.
* api-change:``quicksight``: Amazon QuickSight now supports SecretsManager Secret ARN in place of CredentialPair for DataSource creation and update. This release also has some minor documentation updates and removes CountryCode as a required parameter in GeoSpatialColumnGroup


1.27.88
=======

* api-change:``resiliencehub``: Documentation change for AWS Resilience Hub. Doc-only update to fix Documentation layout


1.27.87
=======

* api-change:``glue``: This SDK release adds support to sync glue jobs with source control provider. Additionally, a new parameter called SourceControlDetails will be added to Job model.
* api-change:``network-firewall``: StreamExceptionPolicy configures how AWS Network Firewall processes traffic when a network connection breaks midstream
* api-change:``outposts``: This release adds the Asset state information to the ListAssets response. The ListAssets request supports filtering on Asset state.


1.27.86
=======

* api-change:``connect``: Updated the CreateIntegrationAssociation API to support the CASES_DOMAIN IntegrationType.
* api-change:``connectcases``: This release adds APIs for Amazon Connect Cases. Cases allows your agents to quickly track and manage customer issues that require multiple interactions, follow-up tasks, and teams in your contact center.  For more information, see https://docs.aws.amazon.com/cases/latest/APIReference/Welcome.html
* api-change:``ec2``: Added EnableNetworkAddressUsageMetrics flag for ModifyVpcAttribute, DescribeVpcAttribute APIs.
* api-change:``ecs``: Documentation updates to address various Amazon ECS tickets.
* api-change:``s3control``: S3 Object Lambda adds support to allow customers to intercept HeadObject and ListObjects requests and introduce their own compute. These requests were previously proxied to S3.
* api-change:``workmail``: This release adds support for impersonation roles in Amazon WorkMail.


1.27.85
=======

* api-change:``accessanalyzer``: AWS IAM Access Analyzer policy validation introduces new checks for role trust policies. As customers author a policy, IAM Access Analyzer policy validation evaluates the policy for any issues to make it easier for customers to author secure policies.
* api-change:``ec2``: Adding an imdsSupport attribute to EC2 AMIs
* api-change:``snowball``: Adds support for V3_5C. This is a refreshed AWS Snowball Edge Compute Optimized device type with 28TB SSD, 104 vCPU and 416GB memory (customer usable).


1.27.84
=======

* api-change:``codedeploy``: This release allows you to override the alarm configurations when creating a deployment.
* api-change:``devops-guru``: This release adds filter feature on AddNotificationChannel API, enable customer to configure the SNS notification messages by Severity or MessageTypes
* api-change:``dlm``: This release adds support for archival of single-volume snapshots created by Amazon Data Lifecycle Manager policies
* api-change:``sagemaker-runtime``: Update sagemaker-runtime client to latest version
* api-change:``sagemaker``: A new parameter called ExplainerConfig is added to CreateEndpointConfig API to enable SageMaker Clarify online explainability feature.
* api-change:``sso-oidc``: Documentation updates for the IAM Identity Center OIDC CLI Reference.


1.27.83
=======

* api-change:``acm``: This update returns additional certificate details such as certificate SANs and allows sorting in the ListCertificates API.
* api-change:``ec2``: u-3tb1 instances are powered by Intel Xeon Platinum 8176M (Skylake) processors and are purpose-built to run large in-memory databases.
* api-change:``emr-serverless``: This release adds API support to debug Amazon EMR Serverless jobs in real-time with live application UIs
* api-change:``fsx``: This release adds support for Amazon File Cache.
* api-change:``migrationhuborchestrator``: Introducing AWS MigrationHubOrchestrator. This is the first public release of AWS MigrationHubOrchestrator.
* api-change:``polly``: Added support for the new Cantonese voice - Hiujin. Hiujin is available as a Neural voice only.
* api-change:``proton``: This release adds an option to delete pipeline provisioning repositories using the UpdateAccountSettings API
* api-change:``sagemaker``: SageMaker Training Managed Warm Pools let you retain provisioned infrastructure to reduce latency for repetitive training workloads.
* api-change:``secretsmanager``: Documentation updates for Secrets Manager
* api-change:``translate``: This release enables customers to access control rights on Translate resources like Parallel Data and Custom Terminology using Tag Based Authorization.
* api-change:``workspaces``: This release includes diagnostic log uploading feature. If it is enabled, the log files of WorkSpaces Windows client will be sent to Amazon WorkSpaces automatically for troubleshooting. You can use modifyClientProperty api to enable/disable this feature.


1.27.82
=======

* api-change:``ce``: This release is to support retroactive Cost Categories. The new field will enable you to retroactively apply new and existing cost category rules to previous months.
* api-change:``kendra``: My AWS Service (placeholder) - Amazon Kendra now provides a data source connector for DropBox. For more information, see https://docs.aws.amazon.com/kendra/latest/dg/data-source-dropbox.html
* api-change:``location``: This release adds place IDs, which are unique identifiers of places, along with a new GetPlace operation, which can be used with place IDs to find a place again later. UnitNumber and UnitType are also added as new properties of places.


1.27.81
=======

* api-change:``cur``: This release adds two new support regions(me-central-1/eu-south-2) for OSG.
* api-change:``iotfleetwise``: General availability (GA) for AWS IoT Fleetwise. It adds AWS IoT Fleetwise to AWS SDK. For more information, see https://docs.aws.amazon.com/iot-fleetwise/latest/APIReference/Welcome.html.
* api-change:``ssm``: This release includes support for applying a CloudWatch alarm to Systems Manager capabilities like Automation, Run Command, State Manager, and Maintenance Windows.


1.27.80
=======

* api-change:``apprunner``: AWS App Runner adds a Node.js 16 runtime.
* api-change:``ec2``: Letting external AWS customers provide ImageId as a Launch Template override in FleetLaunchTemplateOverridesRequest
* api-change:``lexv2-models``: Update lexv2-models client to latest version
* api-change:``lightsail``: This release adds Instance Metadata Service (IMDS) support for Lightsail instances.
* api-change:``nimble``: Amazon Nimble Studio adds support for on-demand Amazon Elastic Compute Cloud (EC2) G3 and G5 instances, allowing customers to utilize additional GPU instance types for their creative projects.
* api-change:``ssm``: This release adds new SSM document types ConformancePackTemplate and CloudFormation
* api-change:``wafv2``: Add the default specification for ResourceType in ListResourcesForWebACL.


1.27.79
=======

* api-change:``backup-gateway``: Changes include: new GetVirtualMachineApi to fetch a single user's VM, improving ListVirtualMachines to fetch filtered VMs as well as all VMs, and improving GetGatewayApi to now also return the gateway's MaintenanceStartTime.
* api-change:``devicefarm``: This release adds the support for VPC-ENI based connectivity for private devices on AWS Device Farm.
* api-change:``ec2``: Documentation updates for Amazon EC2.
* api-change:``glue``: Added support for S3 Event Notifications for Catalog Target Crawlers.
* api-change:``identitystore``: Documentation updates for the Identity Store CLI Reference.


1.27.78
=======

* api-change:``comprehend``: Amazon Comprehend now supports synchronous mode for targeted sentiment API operations.
* api-change:``s3control``: S3 on Outposts launches support for object versioning for Outposts buckets. With S3 Versioning, you can preserve, retrieve, and restore every version of every object stored in your buckets. You can recover from both unintended user actions and application failures.
* api-change:``sagemaker``: SageMaker now allows customization on Canvas Application settings, including enabling/disabling time-series forecasting and specifying an Amazon Forecast execution role at both the Domain and UserProfile levels.


1.27.77
=======

* api-change:``ec2``: This release adds support for blocked paths to Amazon VPC Reachability Analyzer.


1.27.76
=======

* api-change:``cloudtrail``: This release includes support for importing existing trails into CloudTrail Lake.
* api-change:``ec2``: This release adds CapacityAllocations field to DescribeCapacityReservations
* api-change:``mediaconnect``: This change allows the customer to use the SRT Caller protocol as part of their flows
* api-change:``rds``: This release adds support for Amazon RDS Proxy with SQL Server compatibility.


1.27.75
=======

* api-change:``codestar-notifications``: This release adds tag based access control for the UntagResource API.
* api-change:``ecs``: This release supports new task definition sizes.


1.27.74
=======

* api-change:``dynamodb``: Increased DynamoDB transaction limit from 25 to 100.
* api-change:``ec2``: This feature allows customers to create tags for vpc-endpoint-connections and vpc-endpoint-service-permissions.
* api-change:``sagemaker``: Amazon SageMaker Automatic Model Tuning now supports specifying Hyperband strategy for tuning jobs, which uses a multi-fidelity based tuning strategy to stop underperforming hyperparameter configurations early.


1.27.73
=======

* api-change:``amplifyuibuilder``: Amplify Studio UIBuilder is introducing forms functionality. Forms can be configured from Data Store models, JSON, or from scratch. These forms can then be generated in your project and used like any other React components.
* api-change:``ec2``: This update introduces API operations to manage and create local gateway route tables, CoIP pools, and VIF group associations.


1.27.72
=======

* api-change:``customer-profiles``: Added isUnstructured in response for Customer Profiles Integration APIs
* api-change:``drs``: Fixed the data type of lagDuration that is returned in Describe Source Server API
* api-change:``ec2``: Two new features for local gateway route tables: support for static routes targeting Elastic Network Interfaces and direct VPC routing.
* api-change:``evidently``: This release adds support for the client-side evaluation - powered by AWS AppConfig feature.
* api-change:``kendra``: This release enables our customer to choose the option of Sharepoint 2019 for the on-premise Sharepoint connector.
* api-change:``transfer``: This release introduces the ability to have multiple server host keys for any of your Transfer Family servers that use the SFTP protocol.


1.27.71
=======

* api-change:``eks``: Adding support for local Amazon EKS clusters on Outposts


1.27.70
=======

* api-change:``cloudtrail``: This release adds CloudTrail getChannel and listChannels APIs to allow customer to view the ServiceLinkedChannel configurations.
* api-change:``lexv2-models``: Update lexv2-models client to latest version
* api-change:``lexv2-runtime``: Update lexv2-runtime client to latest version
* api-change:``pi``: Increases the maximum values of two RDS Performance Insights APIs. The maximum value of the Limit parameter of DimensionGroup is 25. The MaxResult maximum is now 25 for the following APIs: DescribeDimensionKeys, GetResourceMetrics, ListAvailableResourceDimensions, and ListAvailableResourceMetrics.
* api-change:``redshift``: This release updates documentation for AQUA features and other description updates.


1.27.69
=======

* api-change:``ec2``: This release adds support to send VPC Flow Logs to kinesis-data-firehose as new destination type
* api-change:``emr-containers``: EMR on EKS now allows running Spark SQL using the newly introduced Spark SQL Job Driver in the Start Job Run API
* api-change:``lookoutmetrics``: Release dimension value filtering feature to allow customers to define dimension filters for including only a subset of their dataset to be used by LookoutMetrics.
* api-change:``medialive``: This change exposes API settings which allow Dolby Atmos and Dolby Vision to be used when running a channel using Elemental Media Live
* api-change:``route53``: Amazon Route 53 now supports the Middle East (UAE) Region (me-central-1) for latency records, geoproximity records, and private DNS for Amazon VPCs in that region.
* api-change:``sagemaker``: This release adds Mode to AutoMLJobConfig.
* api-change:``ssm``: This release adds support for Systems Manager State Manager Association tagging.


1.27.68
=======

* api-change:``dataexchange``: Documentation updates for AWS Data Exchange.
* api-change:``ec2``: Documentation updates for Amazon EC2.
* api-change:``eks``: Adds support for EKS Addons ResolveConflicts "preserve" flag. Also adds new update failed status for EKS Addons.
* api-change:``fsx``: Documentation update for Amazon FSx.
* api-change:``inspector2``: This release adds new fields like fixAvailable, fixedInVersion and remediation to the finding model. The requirement to have vulnerablePackages in the finding model has also been removed. The documentation has been updated to reflect these changes.
* api-change:``iotsitewise``: Allow specifying units in Asset Properties
* api-change:``sagemaker``: SageMaker Hosting now allows customization on ML instance storage volume size, model data download timeout and inference container startup ping health check timeout for each ProductionVariant in CreateEndpointConfig API.
* api-change:``sns``: Amazon SNS introduces the Data Protection Policy APIs, which enable customers to attach a data protection policy to an SNS topic. This allows topic owners to enable the new message data protection feature to audit and block sensitive data that is exchanged through their topics.


1.27.67
=======

* api-change:``identitystore``: Documentation updates for the Identity Store CLI Reference.
* api-change:``sagemaker``: This release adds HyperParameterTuningJob type in Search API.


1.27.66
=======

* api-change:``cognito-idp``: This release adds a new "AuthSessionValidity" field to the UserPoolClient in Cognito. Application admins can configure this value for their users' authentication duration, which is currently fixed at 3 minutes, up to 15 minutes. Setting this field will also apply to the SMS MFA authentication flow.
* api-change:``connect``: This release adds search APIs for Routing Profiles and Queues, which can be used to search for those resources within a Connect Instance.
* api-change:``mediapackage``: Added support for AES_CTR encryption to CMAF origin endpoints
* api-change:``sagemaker``: This release enables administrators to attribute user activity and API calls from Studio notebooks, Data Wrangler and Canvas to specific users even when users share the same execution IAM role.  ExecutionRoleIdentityConfig at Sagemaker domain level enables this feature.


1.27.65
=======

* api-change:``codeguru-reviewer``: Documentation updates to fix formatting issues in CLI and SDK documentation.
* api-change:``controltower``: This release contains the first SDK for AWS Control Tower. It introduces  a new set of APIs: EnableControl, DisableControl, GetControlOperation, and ListEnabledControls.
* api-change:``route53``: Documentation updates for Amazon Route 53.


1.27.64
=======

* api-change:``cloudfront``: Update API documentation for CloudFront origin access control (OAC)
* api-change:``identitystore``: Expand IdentityStore API to support Create, Read, Update, Delete and Get operations for User, Group and GroupMembership resources.
* api-change:``iotthingsgraph``: This release deprecates all APIs of the ThingsGraph service
* api-change:``ivs``: IVS Merge Fragmented Streams. This release adds support for recordingReconnectWindow field in IVS recordingConfigurations. For more information see https://docs.aws.amazon.com/ivs/latest/APIReference/Welcome.html
* api-change:``rds-data``: Documentation updates for RDS Data API
* api-change:``sagemaker``: SageMaker Inference Recommender now accepts Inference Recommender fields: Domain, Task, Framework, SamplePayloadUrl, SupportedContentTypes, SupportedInstanceTypes, directly in our CreateInferenceRecommendationsJob API through ContainerConfig


1.27.63
=======

* enhancement:Endpoints: Deprecate SSL common name
* api-change:``greengrassv2``: Adds topologyFilter to ListInstalledComponentsRequest which allows filtration of components by ROOT or ALL (including root and dependency components). Adds lastStatusChangeTimestamp to ListInstalledComponents response to show the last time a component changed state on a device.
* api-change:``identitystore``: Documentation updates for the Identity Store CLI Reference.
* api-change:``lookoutequipment``: This release adds new apis for providing labels.
* api-change:``macie2``: This release of the Amazon Macie API adds support for using allow lists to define specific text and text patterns to ignore when inspecting data sources for sensitive data.
* api-change:``sso-admin``: Documentation updates for the AWS IAM Identity Center CLI Reference.
* api-change:``sso``: Documentation updates for the AWS IAM Identity Center Portal CLI Reference.


1.27.62
=======

* api-change:``fsx``: Documentation updates for Amazon FSx for NetApp ONTAP.
* api-change:``voice-id``: Amazon Connect Voice ID now detects voice spoofing.  When a prospective fraudster tries to spoof caller audio using audio playback or synthesized speech, Voice ID will return a risk score and outcome to indicate the how likely it is that the voice is spoofed.


1.27.61
=======

* api-change:``mediapackage``: This release adds Ads AdTriggers and AdsOnDeliveryRestrictions to describe calls for CMAF endpoints on MediaPackage.
* api-change:``rds``: Removes support for RDS Custom from DBInstanceClass in ModifyDBInstance


1.27.60
=======

* enhancement:Identity: TokenProvider added for bearer auth support
* api-change:``elbv2``: Update elbv2 client to latest version
* api-change:``gamelift``: This release adds support for eight EC2 local zones as fleet locations; Atlanta, Chicago, Dallas, Denver, Houston, Kansas City (us-east-1-mci-1a), Los Angeles, and Phoenix. It also adds support for C5d, C6a, C6i, and R5d EC2 instance families.
* api-change:``iotwireless``: This release includes a new feature for the customers to enable the LoRa gateways to send out beacons for Class B devices and an option to select one or more gateways for Class C devices when sending the LoRaWAN downlink messages.
* api-change:``ivschat``: Documentation change for IVS Chat API Reference. Doc-only update to add a paragraph on ARNs to the Welcome section.
* api-change:``panorama``: Support sorting and filtering in ListDevices API, and add more fields to device listings and single device detail
* api-change:``sso-oidc``: Updated required request parameters on IAM Identity Center's OIDC CreateToken action.


1.27.59
=======

* api-change:``cloudfront``: Adds support for CloudFront origin access control (OAC), making it possible to restrict public access to S3 bucket origins in all AWS Regions, those with SSE-KMS, and more.
* api-change:``config``: AWS Config now supports ConformancePackTemplate documents in SSM Docs for the deployment and update of conformance packs.
* api-change:``iam``: Documentation updates for AWS Identity and Access Management (IAM).
* api-change:``ivs``: Documentation Change for IVS API Reference - Doc-only update to type field description for CreateChannel and UpdateChannel actions and for Channel data type. Also added Amazon Resource Names (ARNs) paragraph to Welcome section.
* api-change:``quicksight``: Added a new optional property DashboardVisual under ExperienceConfiguration parameter of GenerateEmbedUrlForAnonymousUser and GenerateEmbedUrlForRegisteredUser API operations. This supports embedding of specific visuals in QuickSight dashboards.
* api-change:``transfer``: Documentation updates for AWS Transfer Family


1.27.58
=======

* api-change:``rds``: RDS for Oracle supports Oracle Data Guard switchover and read replica backups.
* api-change:``sso-admin``: Documentation updates to reflect service rename - AWS IAM Identity Center (successor to AWS Single Sign-On)


1.27.57
=======

* api-change:``docdb``: Update document for volume clone
* api-change:``ec2``: R6a instances are powered by 3rd generation AMD EPYC (Milan) processors delivering all-core turbo frequency of 3.6 GHz. C6id, M6id, and R6id instances are powered by 3rd generation Intel Xeon Scalable processor (Ice Lake) delivering all-core turbo frequency of 3.5 GHz.
* api-change:``forecast``: releasing What-If Analysis APIs and update ARN regex pattern to be more strict in accordance with security recommendation
* api-change:``forecastquery``: releasing What-If Analysis APIs
* api-change:``iotsitewise``: Enable non-unique asset names under different hierarchies
* api-change:``lexv2-models``: Update lexv2-models client to latest version
* api-change:``securityhub``: Added new resource details objects to ASFF, including resources for AwsBackupBackupVault, AwsBackupBackupPlan and AwsBackupRecoveryPoint. Added FixAvailable, FixedInVersion and Remediation  to Vulnerability.
* api-change:``support-app``: This is the initial SDK release for the AWS Support App in Slack.


1.27.56
=======

* api-change:``connect``: This release adds SearchSecurityProfiles API which can be used to search for Security Profile resources within a Connect Instance.
* api-change:``ivschat``: Documentation Change for IVS Chat API Reference - Doc-only update to change text/description for tags field.
* api-change:``kendra``: This release adds support for a new authentication type - Personal Access Token (PAT) for confluence server.
* api-change:``lookoutmetrics``: This release is to make GetDataQualityMetrics API publicly available.


1.27.55
=======

* api-change:``chime-sdk-media-pipelines``: The Amazon Chime SDK now supports live streaming of real-time video from the Amazon Chime SDK sessions to streaming platforms such as Amazon IVS and Amazon Elemental MediaLive. We have also added support for concatenation to create a single media capture file.
* api-change:``cloudwatch``: Update cloudwatch client to latest version
* api-change:``cognito-idp``: This change is being made simply to fix the public documentation based on the models. We have included the PasswordChange and ResendCode events, along with the Pass, Fail and InProgress status. We have removed the Success and Failure status which are never returned by our APIs.
* api-change:``dynamodb``: This release adds support for importing data from S3 into a new DynamoDB table
* api-change:``ec2``: This release adds support for VPN log options , a new feature allowing S2S VPN connections to send IKE activity logs to CloudWatch Logs
* api-change:``networkmanager``: Add TransitGatewayPeeringAttachmentId property to TransitGatewayPeering Model


1.27.54
=======

* api-change:``appmesh``: AWS App Mesh release to support Multiple Listener and Access Log Format feature
* api-change:``connectcampaigns``: Updated exceptions for Amazon Connect Outbound Campaign api's.
* api-change:``kendra``: This release adds Zendesk connector (which allows you to specify Zendesk SAAS platform as data source), Proxy Support for Sharepoint and Confluence Server (which allows you to specify the proxy configuration if proxy is required to connect to your Sharepoint/Confluence Server as data source).
* api-change:``lakeformation``: This release adds a new API support "AssumeDecoratedRoleWithSAML" and also release updates the corresponding documentation.
* api-change:``lambda``: Added support for customization of Consumer Group ID for MSK and Kafka Event Source Mappings.
* api-change:``lexv2-models``: Update lexv2-models client to latest version
* api-change:``rds``: Adds support for Internet Protocol Version 6 (IPv6) for RDS Aurora database clusters.
* api-change:``secretsmanager``: Documentation updates for Secrets Manager.


1.27.53
=======

* api-change:``rekognition``: This release adds APIs which support copying an Amazon Rekognition Custom Labels model and managing project policies across AWS account.
* api-change:``servicecatalog``: Documentation updates for Service Catalog


1.27.52
=======

* enhancement:AWSCRT: Upgrade awscrt version to 0.14.0
* api-change:``cloudfront``: Adds Http 3 support to distributions
* api-change:``identitystore``: Documentation updates to reflect service rename - AWS IAM Identity Center (successor to AWS Single Sign-On)
* api-change:``sso``: Documentation updates to reflect service rename - AWS IAM Identity Center (successor to AWS Single Sign-On)
* api-change:``wisdom``: This release introduces a new API PutFeedback that allows submitting feedback to Wisdom on content relevance.


1.27.51
=======

* api-change:``amp``: This release adds log APIs that allow customers to manage logging for their Amazon Managed Service for Prometheus workspaces.
* api-change:``chime-sdk-messaging``: The Amazon Chime SDK now supports channels with up to one million participants with elastic channels.
* api-change:``ivs``: Updates various list api MaxResults ranges
* api-change:``personalize-runtime``: This release provides support for promotions in AWS Personalize runtime.
* api-change:``rds``: Adds support for RDS Custom to DBInstanceClass in ModifyDBInstance


1.27.50
=======

* api-change:``backupstorage``: This is the first public release of AWS Backup Storage. We are exposing some previously-internal APIs for use by external services. These APIs are not meant to be used directly by customers.
* api-change:``glue``: Add support for Python 3.9 AWS Glue Python Shell jobs
* api-change:``privatenetworks``: This is the initial SDK release for AWS Private 5G. AWS Private 5G is a managed service that makes it easy to deploy, operate, and scale your own private mobile network at your on-premises location.


1.27.49
=======

* api-change:``dlm``: This release adds support for excluding specific data (non-boot) volumes from multi-volume snapshot sets created by snapshot lifecycle policies
* api-change:``ec2``: This release adds support for excluding specific data (non-root) volumes from multi-volume snapshot sets created from instances.


1.27.48
=======

* api-change:``cloudwatch``: Update cloudwatch client to latest version
* api-change:``location``: Amazon Location Service now allows circular geofences in BatchPutGeofence, PutGeofence, and GetGeofence  APIs.
* api-change:``sagemaker-a2i-runtime``: Fix bug with parsing ISO-8601 CreationTime in Java SDK in DescribeHumanLoop
* api-change:``sagemaker``: Amazon SageMaker Automatic Model Tuning now supports specifying multiple alternate EC2 instance types to make tuning jobs more robust when the preferred instance type is not available due to insufficient capacity.


1.27.47
=======

* api-change:``glue``: Add an option to run non-urgent or non-time sensitive Glue Jobs on spare capacity
* api-change:``identitystore``: Documentation updates to reflect service rename - AWS IAM Identity Center (successor to AWS Single Sign-On)
* api-change:``iotwireless``: AWS IoT Wireless release support for sidewalk data reliability.
* api-change:``pinpoint``: Adds support for Advance Quiet Time in Journeys. Adds RefreshOnSegmentUpdate and WaitForQuietTime to JourneyResponse.
* api-change:``quicksight``: A series of documentation updates to the QuickSight API reference.
* api-change:``sso-admin``: Documentation updates to reflect service rename - AWS IAM Identity Center (successor to AWS Single Sign-On)
* api-change:``sso-oidc``: Documentation updates to reflect service rename - AWS IAM Identity Center (successor to AWS Single Sign-On)
* api-change:``sso``: Documentation updates to reflect service rename - AWS IAM Identity Center (successor to AWS Single Sign-On)


1.27.46
=======

* enhancement:Lambda: Add support for Trace ID in Lambda environments
* api-change:``chime-sdk-meetings``: Adds support for Tags on Amazon Chime SDK WebRTC sessions
* api-change:``config``: Add resourceType enums for Athena, GlobalAccelerator, Detective and EC2 types
* api-change:``dms``: Documentation updates for Database Migration Service (DMS).
* api-change:``iot``: The release is to support attach a provisioning template to CACert for JITP function,  Customer now doesn't have to hardcode a roleArn and templateBody during register a CACert to enable JITP.


1.27.45
=======

* api-change:``cognito-idp``: Add a new exception type, ForbiddenException, that is returned when request is not allowed
* api-change:``wafv2``: You can now associate an AWS WAF web ACL with an Amazon Cognito user pool.


1.27.44
=======

* api-change:``license-manager-user-subscriptions``: This release supports user based subscription for Microsoft Visual Studio Professional and Enterprise on EC2.
* api-change:``personalize``: This release adds support for incremental bulk ingestion for the Personalize CreateDatasetImportJob API.


1.27.43
=======

* api-change:``config``: Documentation update for PutConfigRule and PutOrganizationConfigRule
* api-change:``workspaces``: This release introduces ModifySamlProperties, a new API that allows control of SAML properties associated with a WorkSpaces directory. The DescribeWorkspaceDirectories API will now additionally return SAML properties in its responses.


1.27.42
=======

* bugfix:TraceId: Rollback bugfix for obeying _X_AMZN_TRACE_ID env var


1.27.41
=======

* bugfix:Config: Obey _X_AMZN_TRACE_ID environment variable instead of _X_AMZ_TRACE_ID
* api-change:``ec2``: Documentation updates for Amazon EC2.
* api-change:``fsx``: Documentation updates for Amazon FSx
* api-change:``shield``: AWS Shield Advanced now supports filtering for ListProtections and ListProtectionGroups.


1.27.40
=======

* api-change:``ec2``: Documentation updates for VM Import/Export.
* api-change:``es``: This release adds support for gp3 EBS (Elastic Block Store) storage.
* api-change:``lookoutvision``: This release introduces support for image segmentation models and updates CPU accelerator options for models hosted on edge devices.
* api-change:``opensearch``: This release adds support for gp3 EBS (Elastic Block Store) storage.


1.27.39
=======

* api-change:``auditmanager``: This release adds an exceeded quota exception to several APIs. We added a ServiceQuotaExceededException for the following operations: CreateAssessment, CreateControl, CreateAssessmentFramework, and UpdateAssessmentStatus.
* api-change:``chime``: Chime VoiceConnector will now support ValidateE911Address which will allow customers to prevalidate their addresses included in their SIP invites for emergency calling
* api-change:``config``: This release adds ListConformancePackComplianceScores API to support the new compliance score feature, which provides a percentage of the number of compliant rule-resource combinations in a conformance pack compared to the number of total possible rule-resource combinations in the conformance pack.
* api-change:``globalaccelerator``: Global Accelerator now supports dual-stack accelerators, enabling support for IPv4 and IPv6 traffic.
* api-change:``marketplace-catalog``: The SDK for the StartChangeSet API will now automatically set and use an idempotency token in the ClientRequestToken request parameter if the customer does not provide it.
* api-change:``polly``: Amazon Polly adds new English and Hindi voice - Kajal. Kajal is available as Neural voice only.
* api-change:``ssm``: Adding doc updates for OpsCenter support in Service Setting actions.
* api-change:``workspaces``: Added CreateWorkspaceImage API to create a new WorkSpace image from an existing WorkSpace.


1.27.38
=======

* api-change:``appsync``: Adds support for a new API to evaluate mapping templates with mock data, allowing you to remotely unit test your AppSync resolvers and functions.
* api-change:``detective``: Added the ability to get data source package information for the behavior graph. Graph administrators can now start (or stop) optional datasources on the behavior graph.
* api-change:``guardduty``: Amazon GuardDuty introduces a new Malware Protection feature that triggers malware scan on selected EC2 instance resources, after the service detects a potentially malicious activity.
* api-change:``lookoutvision``: This release introduces support for the automatic scaling of inference units used by Amazon Lookout for Vision models.
* api-change:``macie2``: This release adds support for retrieving (revealing) sample occurrences of sensitive data that Amazon Macie detects and reports in findings.
* api-change:``rds``: Adds support for using RDS Proxies with RDS for MariaDB databases.
* api-change:``rekognition``: This release introduces support for the automatic scaling of inference units used by Amazon Rekognition Custom Labels models.
* api-change:``securityhub``: Documentation updates for AWS Security Hub
* api-change:``transfer``: AWS Transfer Family now supports Applicability Statement 2 (AS2), a network protocol used for the secure and reliable transfer of critical Business-to-Business (B2B) data over the public internet using HTTP/HTTPS as the transport mechanism.


1.27.37
=======

* api-change:``autoscaling``: Documentation update for Amazon EC2 Auto Scaling.


1.27.36
=======

* api-change:``account``: This release enables customers to manage the primary contact information for their AWS accounts. For more information, see https://docs.aws.amazon.com/accounts/latest/reference/API_Operations.html
* api-change:``ec2``: Added support for EC2 M1 Mac instances. For more information, please visit aws.amazon.com/mac.
* api-change:``iotdeviceadvisor``: Added new service feature (Early access only) - Long Duration Test, where customers can test the IoT device to observe how it behaves when the device is in operation for longer period.
* api-change:``medialive``: Link devices now support remote rebooting. Link devices now support maintenance windows. Maintenance windows allow a Link device to install software updates without stopping the MediaLive channel. The channel will experience a brief loss of input from the device while updates are installed.
* api-change:``rds``: This release adds the "ModifyActivityStream" API with support for audit policy state locking and unlocking.
* api-change:``transcribe``: Remove unsupported language codes for StartTranscriptionJob and update VocabularyFileUri for UpdateMedicalVocabulary


1.27.35
=======

* api-change:``athena``: This feature allows customers to retrieve runtime statistics for completed queries
* api-change:``cloudwatch``: Update cloudwatch client to latest version
* api-change:``dms``: Documentation updates for Database Migration Service (DMS).
* api-change:``docdb``: Enable copy-on-write restore type
* api-change:``ec2-instance-connect``: This release includes a new exception type "EC2InstanceUnavailableException" for SendSSHPublicKey and SendSerialConsoleSSHPublicKey APIs.
* api-change:``frauddetector``: The release introduces Account Takeover Insights (ATI) model. The ATI model detects fraud relating to account takeover. This release also adds support for new variable types: ARE_CREDENTIALS_VALID and SESSION_ID and adds new structures to Model Version APIs.
* api-change:``iotsitewise``: Added asynchronous API to ingest bulk historical and current data into IoT SiteWise.
* api-change:``kendra``: Amazon Kendra now provides Oauth2 support for SharePoint Online. For more information, see https://docs.aws.amazon.com/kendra/latest/dg/data-source-sharepoint.html
* api-change:``network-firewall``: Network Firewall now supports referencing dynamic IP sets from stateful rule groups, for IP sets stored in Amazon VPC prefix lists.
* api-change:``rds``: Adds support for creating an RDS Proxy for an RDS for MariaDB database.


1.27.34
=======

* api-change:``acm-pca``: AWS Certificate Manager (ACM) Private Certificate Authority (PCA) documentation updates
* api-change:``iot``: GA release the ability to enable/disable IoT Fleet Indexing for Device Defender and Named Shadow information, and search them through IoT Fleet Indexing APIs. This includes Named Shadow Selection as a part of the UpdateIndexingConfiguration API.


1.27.33
=======

* api-change:``devops-guru``: Added new APIs for log anomaly detection feature.
* api-change:``glue``: Documentation updates for AWS Glue Job Timeout and Autoscaling
* api-change:``sagemaker-edge``: Amazon SageMaker Edge Manager provides lightweight model deployment feature to deploy machine learning models on requested devices.
* api-change:``sagemaker``: Fixed an issue with cross account QueryLineage
* api-change:``workspaces``: Increased the character limit of the login message from 850 to 2000 characters.


1.27.32
=======

* api-change:``discovery``: Add AWS Agentless Collector details to the GetDiscoverySummary API response
* api-change:``ec2``: Documentation updates for Amazon EC2.
* api-change:``elasticache``: Adding AutoMinorVersionUpgrade in the DescribeReplicationGroups API
* api-change:``kms``: Added support for the SM2 KeySpec in China Partition Regions
* api-change:``mediapackage``: This release adds "IncludeIframeOnlyStream" for Dash endpoints and increases the number of supported video and audio encryption presets for Speke v2
* api-change:``sagemaker``: Amazon SageMaker Edge Manager provides lightweight model deployment feature to deploy machine learning models on requested devices.
* api-change:``sso-admin``: AWS SSO now supports attaching customer managed policies and a permissions boundary to your permission sets. This release adds new API operations to manage and view the customer managed policies and the permissions boundary for a given permission set.


1.27.31
=======

* api-change:``datasync``: Documentation updates for AWS DataSync regarding configuring Amazon FSx for ONTAP location security groups and SMB user permissions.
* api-change:``drs``: Changed existing APIs to allow choosing a dynamic volume type for replicating volumes, to reduce costs for customers.
* api-change:``evidently``: This release adds support for the new segmentation feature.
* api-change:``wafv2``: This SDK release provide customers ability to add sensitivity level for WAF SQLI Match Statements.


1.27.30
=======

* api-change:``athena``: This release updates data types that contain either QueryExecutionId, NamedQueryId or ExpectedBucketOwner. Ids must be between 1 and 128 characters and contain only non-whitespace characters. ExpectedBucketOwner must be 12-digit string.
* api-change:``codeartifact``: This release introduces Package Origin Controls, a mechanism used to counteract Dependency Confusion attacks. Adds two new APIs, PutPackageOriginConfiguration and DescribePackage, and updates the ListPackage, DescribePackageVersion and ListPackageVersion APIs in support of the feature.
* api-change:``config``: Update ResourceType enum with values for Route53Resolver, Batch, DMS, Workspaces, Stepfunctions, SageMaker, ElasticLoadBalancingV2, MSK types
* api-change:``ec2``: This release adds flow logs for Transit Gateway to  allow customers to gain deeper visibility and insights into network traffic through their Transit Gateways.
* api-change:``fms``: Adds support for strict ordering in stateful rule groups in Network Firewall policies.
* api-change:``glue``: This release adds an additional worker type for Glue Streaming jobs.
* api-change:``inspector2``: This release adds support for Inspector V2 scan configurations through the get and update configuration APIs. Currently this allows configuring ECR automated re-scan duration to lifetime or 180 days or 30 days.
* api-change:``kendra``: This release adds AccessControlConfigurations which allow you to redefine your document level access control without the need for content re-indexing.
* api-change:``nimble``: Amazon Nimble Studio adds support for IAM-based access to AWS resources for Nimble Studio components and custom studio components. Studio Component scripts use these roles on Nimble Studio workstation to mount filesystems, access S3 buckets, or other configured resources in the Studio's AWS account
* api-change:``outposts``: This release adds the ShipmentInformation and AssetInformationList fields to the GetOrder API response.
* api-change:``sagemaker``: This release adds support for G5, P4d, and C6i instance types in Amazon SageMaker Inference and increases the number of hyperparameters that can be searched from 20 to 30 in Amazon SageMaker Automatic Model Tuning


1.27.29
=======

* api-change:``appconfig``: Adding Create, Get, Update, Delete, and List APIs for new two new resources: Extensions and ExtensionAssociations.


1.27.28
=======

* api-change:``networkmanager``: This release adds general availability API support for AWS Cloud WAN.


1.27.27
=======

* api-change:``ec2``: Build, manage, and monitor a unified global network that connects resources running across your cloud and on-premises environments using the AWS Cloud WAN APIs.
* api-change:``redshift-serverless``: Removed prerelease language for GA launch.
* api-change:``redshift``: This release adds a new --snapshot-arn field for describe-cluster-snapshots, describe-node-configuration-options, restore-from-cluster-snapshot, authorize-snapshot-acsess, and revoke-snapshot-acsess APIs. It allows customers to give a Redshift snapshot ARN or a Redshift Serverless ARN as input.


1.27.26
=======

* api-change:``backup``: This release adds support for authentication using IAM user identity instead of passed IAM role, identified by excluding the IamRoleArn field in the StartRestoreJob API. This feature applies to only resource clients with a destructive restore nature (e.g. SAP HANA).


1.27.25
=======

* api-change:``chime-sdk-meetings``: Adds support for AppKeys and TenantIds in Amazon Chime SDK WebRTC sessions
* api-change:``dms``: New api to migrate event subscriptions to event bridge rules
* api-change:``iot``: This release adds support to register a CA certificate without having to provide a verification certificate. This also allows multiple AWS accounts to register the same CA in the same region.
* api-change:``iotwireless``: Adds 5 APIs: PutPositionConfiguration, GetPositionConfiguration, ListPositionConfigurations, UpdatePosition, GetPosition for the new Positioning Service feature which enables customers to configure solvers to calculate position of LoRaWAN devices, or specify position of LoRaWAN devices & gateways.
* api-change:``sagemaker``: Heterogeneous clusters: the ability to launch training jobs with multiple instance types. This enables running component of the training job on the instance type that is most suitable for it. e.g. doing data processing and augmentation on CPU instances and neural network training on GPU instances


1.27.24
=======

* api-change:``cloudformation``: My AWS Service (placeholder) - Add a new feature Account-level Targeting for StackSet operation
* api-change:``synthetics``: This release introduces Group feature, which enables users to group cross-region canaries.


1.27.23
=======

* api-change:``config``: Updating documentation service limits
* api-change:``lexv2-models``: Update lexv2-models client to latest version
* api-change:``quicksight``: This release allows customers to programmatically create QuickSight accounts with Enterprise and Enterprise + Q editions. It also releases allowlisting domains for embedding QuickSight dashboards at runtime through the embedding APIs.
* api-change:``rds``: Adds waiters support for DBCluster.
* api-change:``rolesanywhere``: IAM Roles Anywhere allows your workloads such as servers, containers, and applications to obtain temporary AWS credentials and use the same IAM roles and policies that you have configured for your AWS workloads to access AWS resources.
* api-change:``ssm-incidents``: Adds support for tagging incident-record on creation by providing incident tags in the template within a response-plan.


1.27.22
=======

* api-change:``dms``: Added new features for AWS DMS version 3.4.7 that includes new endpoint settings for S3, OpenSearch, Postgres, SQLServer and Oracle.
* api-change:``rds``: Adds support for additional retention periods to Performance Insights.


1.27.21
=======

* api-change:``athena``: This feature introduces the API support for Athena's parameterized query and BatchGetPreparedStatement API.
* api-change:``customer-profiles``: This release adds the optional MinAllowedConfidenceScoreForMerging parameter to the CreateDomain, UpdateDomain, and GetAutoMergingPreview APIs in Customer Profiles. This parameter is used as a threshold to influence the profile auto-merging step of the Identity Resolution process.
* api-change:``emr``: Update emr client to latest version
* api-change:``glue``: This release adds tag as an input of CreateDatabase
* api-change:``kendra``: Amazon Kendra now provides a data source connector for alfresco
* api-change:``mwaa``: Documentation updates for Amazon Managed Workflows for Apache Airflow.
* api-change:``pricing``: Documentation update for GetProducts Response.
* api-change:``wellarchitected``: Added support for UpdateGlobalSettings API. Added status filter to ListWorkloadShares and ListLensShares.
* api-change:``workmail``: This release adds support for managing user availability configurations in Amazon WorkMail.


1.27.20
=======

* api-change:``appstream``: Includes support for StreamingExperienceSettings in CreateStack and UpdateStack APIs
* api-change:``elbv2``: Update elbv2 client to latest version
* api-change:``emr``: Update emr client to latest version
* api-change:``medialive``: This release adds support for automatic renewal of MediaLive reservations at the end of each reservation term. Automatic renewal is optional. This release also adds support for labelling accessibility-focused audio and caption tracks in HLS outputs.
* api-change:``redshift-serverless``: Add new API operations for Amazon Redshift Serverless, a new way of using Amazon Redshift without needing to manually manage provisioned clusters. The new operations let you interact with Redshift Serverless resources, such as create snapshots, list VPC endpoints, delete resource policies, and more.
* api-change:``sagemaker``: This release adds: UpdateFeatureGroup, UpdateFeatureMetadata, DescribeFeatureMetadata APIs; FeatureMetadata type in Search API; LastModifiedTime, LastUpdateStatus, OnlineStoreTotalSizeBytes in DescribeFeatureGroup API.
* api-change:``translate``: Added ListLanguages API which can be used to list the languages supported by Translate.


1.27.19
=======

* api-change:``datasync``: AWS DataSync now supports Amazon FSx for NetApp ONTAP locations.
* api-change:``ec2``: This release adds a new spread placement group to EC2 Placement Groups: host level spread, which spread instances between physical hosts, available to Outpost customers only. CreatePlacementGroup and DescribePlacementGroups APIs were updated with a new parameter: SpreadLevel to support this feature.
* api-change:``finspace-data``: Release new API GetExternalDataViewAccessDetails
* api-change:``polly``: Add 4 new neural voices - Pedro (es-US), Liam (fr-CA), Daniel (de-DE) and Arthur (en-GB).


1.27.18
=======

* api-change:``iot``: This release ease the restriction for the input of tag value to align with AWS standard, now instead of min length 1, we change it to min length 0.


1.27.17
=======

* api-change:``glue``: This release enables the new ListCrawls API for viewing the AWS Glue Crawler run history.
* api-change:``rds-data``: Documentation updates for RDS Data API


1.27.16
=======

* api-change:``lookoutequipment``: This release adds visualizations to the scheduled inference results. Users will be able to see interference results, including diagnostic results from their running inference schedulers.
* api-change:``mediaconvert``: AWS Elemental MediaConvert SDK has released support for automatic DolbyVision metadata generation when converting HDR10 to DolbyVision.
* api-change:``mgn``: New and modified APIs for the Post-Migration Framework
* api-change:``migration-hub-refactor-spaces``: This release adds the new API UpdateRoute that allows route to be updated to ACTIVE/INACTIVE state. In addition, CreateRoute API will now allow users to create route in ACTIVE/INACTIVE state.
* api-change:``sagemaker``: SageMaker Ground Truth now supports Virtual Private Cloud. Customers can launch labeling jobs and access to their private workforce in VPC mode.


1.27.15
=======

* api-change:``apigateway``: Documentation updates for Amazon API Gateway
* api-change:``pricing``: This release introduces 1 update to the GetProducts API. The serviceCode attribute is now required when you use the GetProductsRequest.
* api-change:``transfer``: Until today, the service supported only RSA host keys and user keys. Now with this launch, Transfer Family has expanded the support for ECDSA and ED25519 host keys and user keys, enabling customers to support a broader set of clients by choosing RSA, ECDSA, and ED25519 host and user keys.


1.27.14
=======

* api-change:``ec2``: This release adds support for Private IP VPNs, a new feature allowing S2S VPN connections to use private ip addresses as the tunnel outside ip address over Direct Connect as transport.
* api-change:``ecs``: Amazon ECS UpdateService now supports the following parameters: PlacementStrategies, PlacementConstraints and CapacityProviderStrategy.
* api-change:``wellarchitected``: Adds support for lens tagging, Adds support for multiple helpful-resource urls and multiple improvement-plan urls.


1.27.13
=======

* api-change:``ds``: This release adds support for describing and updating AWS Managed Microsoft AD settings
* api-change:``kafka``: Documentation updates to use Az Id during cluster creation.
* api-change:``outposts``: This release adds the AssetLocation structure to the ListAssets response. AssetLocation includes the RackElevation for an Asset.


1.27.12
=======

* api-change:``connect``: This release updates these APIs: UpdateInstanceAttribute, DescribeInstanceAttribute and ListInstanceAttributes. You can use it to programmatically enable/disable High volume outbound communications using attribute type HIGH_VOLUME_OUTBOUND on the specified Amazon Connect instance.
* api-change:``connectcampaigns``: Added Amazon Connect high volume outbound communications SDK.
* api-change:``dynamodb``: Doc only update for DynamoDB service
* api-change:``dynamodbstreams``: Update dynamodbstreams client to latest version


1.27.11
=======

* api-change:``redshift-data``: This release adds a new --workgroup-name field to operations that connect to an endpoint. Customers can now execute queries against their serverless workgroups.
* api-change:``secretsmanager``: Documentation updates for Secrets Manager
* api-change:``securityhub``: Added Threats field for security findings. Added new resource details for ECS Container, ECS Task, RDS SecurityGroup, Kinesis Stream, EC2 TransitGateway, EFS AccessPoint, CloudFormation Stack, CloudWatch Alarm, VPC Peering Connection and WAF Rules


1.27.10
=======

* api-change:``finspace-data``: This release adds a new set of APIs, GetPermissionGroup, DisassociateUserFromPermissionGroup, AssociateUserToPermissionGroup, ListPermissionGroupsByUser, ListUsersByPermissionGroup.
* api-change:``guardduty``: Adds finding fields available from GuardDuty Console. Adds FreeTrial related operations. Deprecates the use of various APIs related to Master Accounts and Replace them with Administrator Accounts.
* api-change:``servicecatalog-appregistry``: This release adds a new API ListAttributeGroupsForApplication that returns associated attribute groups of an application. In addition, the UpdateApplication and UpdateAttributeGroup APIs will not allow users to update the 'Name' attribute.
* api-change:``workspaces``: Added new field "reason" to OperationNotSupportedException. Receiving this exception in the DeregisterWorkspaceDirectory API will now return a reason giving more context on the failure.


1.27.9
======

* api-change:``budgets``: Add a budgets ThrottlingException. Update the CostFilters value pattern.
* api-change:``lookoutmetrics``: Adding filters to Alert and adding new UpdateAlert API.
* api-change:``mediaconvert``: AWS Elemental MediaConvert SDK has added support for rules that constrain Automatic-ABR rendition selection when generating ABR package ladders.


1.27.8
======

* api-change:``outposts``: This release adds API operations AWS uses to install Outpost servers.


1.27.7
======

* api-change:``frauddetector``: Documentation updates for Amazon Fraud Detector (AWSHawksNest)


1.27.6
======

* api-change:``chime-sdk-meetings``: Adds support for live transcription in AWS GovCloud (US) Regions.


1.27.5
======

* api-change:``dms``: This release adds DMS Fleet Advisor APIs and exposes functionality for DMS Fleet Advisor. It adds functionality to create and modify fleet advisor instances, and to collect and analyze information about the local data infrastructure.
* api-change:``iam``: Documentation updates for AWS Identity and Access Management (IAM).
* api-change:``m2``: AWS Mainframe Modernization service is a managed mainframe service and set of tools for planning, migrating, modernizing, and running mainframe workloads on AWS
* api-change:``neptune``: This release adds support for Neptune to be configured as a global database, with a primary DB cluster in one region, and up to five secondary DB clusters in other regions.
* api-change:``redshift``: Adds new API GetClusterCredentialsWithIAM to return temporary credentials.


1.27.4
======

* api-change:``auditmanager``: This release introduces 2 updates to the Audit Manager API. The roleType and roleArn attributes are now required when you use the CreateAssessment or UpdateAssessment operation. We also added a throttling exception to the RegisterAccount API operation.
* api-change:``ce``: Added two new APIs to support cost allocation tags operations: ListCostAllocationTags, UpdateCostAllocationTagsStatus.


1.27.3
======

* api-change:``chime-sdk-messaging``: This release adds support for searching channels by members via the SearchChannels API, removes required restrictions for Name and Mode in UpdateChannel API and enhances CreateChannel API by exposing member and moderator list as well as channel id as optional parameters.
* api-change:``connect``: This release adds a new API, GetCurrentUserData, which returns real-time details about users' current activity.


1.27.2
======

* api-change:``codeartifact``: Documentation updates for CodeArtifact
* api-change:``voice-id``: Added a new attribute ServerSideEncryptionUpdateDetails to Domain and DomainSummary.
* api-change:``proton``: Add new "Components" API to enable users to Create, Delete and Update AWS Proton components.
* api-change:``connect``: This release adds the following features: 1) New APIs to manage (create, list, update) task template resources, 2) Updates to startTaskContact API to support task templates, and 3) new TransferContact API to programmatically transfer in-progress tasks via a contact flow.
* api-change:``application-insights``: Provide Account Level onboarding support through CFN/CLI
* api-change:``kendra``: Amazon Kendra now provides a data source connector for GitHub. For more information, see https://docs.aws.amazon.com/kendra/latest/dg/data-source-github.html


1.27.1
======

* api-change:``backup-gateway``: Adds GetGateway and UpdateGatewaySoftwareNow API and adds hypervisor name to UpdateHypervisor API
* api-change:``forecast``: Added Format field to Import and Export APIs in Amazon Forecast. Added TimeSeriesSelector to Create Forecast API.
* api-change:``chime-sdk-meetings``: Adds support for centrally controlling each participant's ability to send and receive audio, video and screen share within a WebRTC session.  Attendee capabilities can be specified when the attendee is created and updated during the session with the new BatchUpdateAttendeeCapabilitiesExcept API.
* api-change:``route53``: Add new APIs to support Route 53 IP Based Routing


1.27.0
======

* api-change:``iotsitewise``: This release adds the following new optional field to the IoT SiteWise asset resource: assetDescription.
* api-change:``lookoutmetrics``: Adding backtest mode to detectors using the Cloudwatch data source.
* api-change:``transcribe``: Amazon Transcribe now supports automatic language identification for multi-lingual audio in batch mode.
* feature:Python: Dropped support for Python 3.6
* api-change:``cognito-idp``: Amazon Cognito now supports IP Address propagation for all unauthenticated APIs (e.g. SignUp, ForgotPassword).
* api-change:``drs``: Changed existing APIs and added new APIs to accommodate using multiple AWS accounts with AWS Elastic Disaster Recovery.
* api-change:``sagemaker``: Amazon SageMaker Notebook Instances now support Jupyter Lab 3.


1.26.10
=======

* api-change:``sagemaker``: Amazon SageMaker Notebook Instances now allows configuration of Instance Metadata Service version and Amazon SageMaker Studio now supports G5 instance types.
* api-change:``appflow``: Adding the following features/changes: Parquet output that preserves typing from the source connector, Failed executions threshold before deactivation for scheduled flows, increasing max size of access and refresh token from 2048 to 4096
* api-change:``datasync``: AWS DataSync now supports TLS encryption in transit, file system policies and access points for EFS locations.
* api-change:``emr-serverless``: This release adds support for Amazon EMR Serverless, a serverless runtime environment that simplifies running analytics applications using the latest open source frameworks such as Apache Spark and Apache Hive.


1.26.9
======

* api-change:``lightsail``: Amazon Lightsail now supports the ability to configure a Lightsail Container Service to pull images from Amazon ECR private repositories in your account.
* api-change:``emr-serverless``: This release adds support for Amazon EMR Serverless, a serverless runtime environment that simplifies running analytics applications using the latest open source frameworks such as Apache Spark and Apache Hive.
* api-change:``ec2``: C7g instances, powered by the latest generation AWS Graviton3 processors, provide the best price performance in Amazon EC2 for compute-intensive workloads.
* api-change:``forecast``: Introduced a new field in Auto Predictor as Time Alignment Boundary. It helps in aligning the timestamps generated during Forecast exports


1.26.8
======

* api-change:``secretsmanager``: Documentation updates for Secrets Manager
* api-change:``fsx``: This release adds root squash support to FSx for Lustre to restrict root level access from clients by mapping root users to a less-privileged user/group with limited permissions.
* api-change:``lookoutmetrics``: Adding AthenaSourceConfig for MetricSet APIs to support Athena as a data source.
* api-change:``voice-id``: VoiceID will now automatically expire Speakers if they haven't been accessed for Enrollment, Re-enrollment or Successful Auth for three years. The Speaker APIs now return a "LastAccessedAt" time for Speakers, and the EvaluateSession API returns "SPEAKER_EXPIRED" Auth Decision for EXPIRED Speakers.
* api-change:``cloudformation``: Add a new parameter statusReason to DescribeStackSetOperation output for additional details
* api-change:``apigateway``: Documentation updates for Amazon API Gateway
* api-change:``apprunner``: Documentation-only update added for CodeConfiguration.
* api-change:``sagemaker``: Amazon SageMaker Autopilot adds support for manually selecting features from the input dataset using the CreateAutoMLJob API.


1.26.7
======

* api-change:``mediaconvert``: AWS Elemental MediaConvert SDK has added support for rules that constrain Automatic-ABR rendition selection when generating ABR package ladders.
* api-change:``cognito-idp``: Amazon Cognito now supports requiring attribute verification (ex. email and phone number) before update.
* api-change:``networkmanager``: This release adds Multi Account API support for a TGW Global Network, to enable and disable AWSServiceAccess with AwsOrganizations for Network Manager service and dependency CloudFormation StackSets service.
* api-change:``ivschat``: Doc-only update. For MessageReviewHandler structure, added timeout period in the description of the fallbackResult field
* api-change:``ec2``: Stop Protection feature enables customers to protect their instances from accidental stop actions.


1.26.6
======

* api-change:``elasticache``: Added support for encryption in transit for Memcached clusters. Customers can now launch Memcached cluster with encryption in transit enabled when using Memcached version 1.6.12 or later.
* api-change:``forecast``: New APIs for Monitor that help you understand how your predictors perform over time.
* api-change:``personalize``: Adding modelMetrics as part of DescribeRecommender API response for Personalize.


1.26.5
======

* api-change:``comprehend``: Comprehend releases 14 new entity types for DetectPiiEntities and ContainsPiiEntities APIs.
* api-change:``logs``: Doc-only update to publish the new valid values for log retention


1.26.4
======

* api-change:``gamesparks``: This release adds an optional DeploymentResult field in the responses of GetStageDeploymentIntegrationTests and ListStageDeploymentIntegrationTests APIs.
* enhancement:StreamingBody: Allow StreamingBody to be used as a context manager
* api-change:``lookoutmetrics``: In this release we added SnsFormat to SNSConfiguration to support human readable alert.


1.26.3
======

* api-change:``greengrassv2``: This release adds the new DeleteDeployment API operation that you can use to delete deployment resources. This release also adds support for discontinued AWS-provided components, so AWS can communicate when a component has any issues that you should consider before you deploy it.
* api-change:``quicksight``: API UpdatePublicSharingSettings enables IAM admins to enable/disable account level setting for public access of dashboards. When enabled, owners/co-owners for dashboards can enable public access on their dashboards. These dashboards can only be accessed through share link or embedding.
* api-change:``appmesh``: This release updates the existing Create and Update APIs for meshes and virtual nodes by adding a new IP preference field. This new IP preference field can be used to control the IP versions being used with the mesh and allows for IPv6 support within App Mesh.
* api-change:``batch``: Documentation updates for AWS Batch.
* api-change:``iotevents-data``: Introducing new API for deleting detectors: BatchDeleteDetector.
* api-change:``transfer``: AWS Transfer Family now supports SetStat server configuration option, which provides the ability to ignore SetStat command issued by file transfer clients, enabling customers to upload files without any errors.


1.26.2
======

* api-change:``kms``: Add HMAC best practice tip, annual rotation of AWS managed keys.
* api-change:``glue``: This release adds a new optional parameter called codeGenNodeConfiguration to CRUD job APIs that allows users to manage visual jobs via APIs. The updated CreateJob and UpdateJob will create jobs that can be viewed in Glue Studio as a visual graph. GetJob can be used to get codeGenNodeConfiguration.


1.26.1
======

* api-change:``resiliencehub``: In this release, we are introducing support for Amazon Elastic Container Service, Amazon Route 53, AWS Elastic Disaster Recovery, AWS Backup in addition to the existing supported Services.  This release also supports Terraform file input from S3 and scheduling daily assessments
* api-change:``servicecatalog``: Updated the descriptions for the ListAcceptedPortfolioShares API description and the PortfolioShareType parameters.
* api-change:``discovery``: Add Migration Evaluator Collector details to the GetDiscoverySummary API response
* api-change:``sts``: Documentation updates for AWS Security Token Service.
* api-change:``workspaces-web``: Amazon WorkSpaces Web now supports Administrator timeout control
* api-change:``rekognition``: Documentation updates for Amazon Rekognition.
* api-change:``cloudfront``: Introduced a new error (TooLongCSPInResponseHeadersPolicy) that is returned when the value of the Content-Security-Policy header in a response headers policy exceeds the maximum allowed length.


1.26.0
======

* feature:Loaders: Support for loading gzip compressed model files.
* api-change:``grafana``: This release adds APIs for creating and deleting API keys in an Amazon Managed Grafana workspace.


1.25.13
=======

* api-change:``ivschat``: Documentation-only updates for IVS Chat API Reference.
* api-change:``lambda``: Lambda releases NodeJs 16 managed runtime to be available in all commercial regions.
* api-change:``kendra``: Amazon Kendra now provides a data source connector for Jira. For more information, see https://docs.aws.amazon.com/kendra/latest/dg/data-source-jira.html
* api-change:``transfer``: AWS Transfer Family now accepts ECDSA keys for server host keys
* api-change:``iot``: Documentation update for China region ListMetricValues for IoT
* api-change:``workspaces``: Increased the character limit of the login message from 600 to 850 characters.
* api-change:``finspace-data``: We've now deprecated CreateSnapshot permission for creating a data view, instead use CreateDataView permission.
* api-change:``lightsail``: This release adds support to include inactive database bundles in the response of the GetRelationalDatabaseBundles request.
* api-change:``outposts``: Documentation updates for AWS Outposts.
* api-change:``ec2``: This release introduces a target type Gateway Load Balancer Endpoint for mirrored traffic. Customers can now specify GatewayLoadBalancerEndpoint option during the creation of a traffic mirror target.
* api-change:``ssm-incidents``: Adding support for dynamic SSM Runbook parameter values. Updating validation pattern for engagements. Adding ConflictException to UpdateReplicationSet API contract.


1.25.12
=======

* api-change:``secretsmanager``: Doc only update for Secrets Manager that fixes several customer-reported issues.
* api-change:``ec2``: This release updates AWS PrivateLink APIs to support IPv6 for PrivateLink Services and Endpoints of type 'Interface'.


1.25.11
=======

* api-change:``migration-hub-refactor-spaces``: AWS Migration Hub Refactor Spaces documentation only update to fix a formatting issue.
* api-change:``ec2``: Added support for using NitroTPM and UEFI Secure Boot on EC2 instances.
* api-change:``emr``: Update emr client to latest version
* api-change:``compute-optimizer``: Documentation updates for Compute Optimizer
* api-change:``eks``: Adds BOTTLEROCKET_ARM_64_NVIDIA and BOTTLEROCKET_x86_64_NVIDIA AMI types to EKS managed nodegroups


1.25.10
=======

* api-change:``evidently``: Add detail message inside GetExperimentResults API response to indicate experiment result availability
* api-change:``ssm-contacts``: Fixed an error in the DescribeEngagement example for AWS Incident Manager.
* api-change:``cloudcontrol``: SDK release for Cloud Control API to include paginators for Python SDK.


1.25.9
======

* api-change:``rds``: Various documentation improvements.
* api-change:``redshift``: Introduces new field 'LoadSampleData' in CreateCluster operation. Customers can now specify 'LoadSampleData' option during creation of a cluster, which results in loading of sample data in the cluster that is created.
* api-change:``ec2``: Add new state values for IPAMs, IPAM Scopes, and IPAM Pools.
* api-change:``mediapackage``: This release adds Dvb Dash 2014 as an available profile option for Dash Origin Endpoints.
* api-change:``securityhub``: Documentation updates for Security Hub API reference
* api-change:``location``: Amazon Location Service now includes a MaxResults parameter for ListGeofences requests.


1.25.8
======

* api-change:``ec2``: Amazon EC2 I4i instances are powered by 3rd generation Intel Xeon Scalable processors and feature up to 30 TB of local AWS Nitro SSD storage
* api-change:``kendra``: AWS Kendra now supports hierarchical facets for a query. For more information, see https://docs.aws.amazon.com/kendra/latest/dg/filtering.html
* api-change:``iot``: AWS IoT Jobs now allows you to create up to 100,000 active continuous and snapshot jobs by using concurrency control.
* api-change:``datasync``: AWS DataSync now supports a new ObjectTags Task API option that can be used to control whether Object Tags are transferred.


1.25.7
======

* api-change:``ssm``: This release adds the TargetMaps parameter in SSM State Manager API.
* api-change:``backup``: Adds support to 2 new filters about job complete time for 3 list jobs APIs in AWS Backup
* api-change:``lightsail``: Documentation updates for Lightsail
* api-change:``iotsecuretunneling``: This release introduces a new API RotateTunnelAccessToken that allow revoking the existing tokens and generate new tokens


1.25.6
======

* api-change:``ec2``: Adds support for allocating Dedicated Hosts on AWS  Outposts. The AllocateHosts API now accepts an OutpostArn request  parameter, and the DescribeHosts API now includes an OutpostArn response parameter.
* api-change:``s3``: Documentation only update for doc bug fixes for the S3 API docs.
* api-change:``kinesisvideo``: Add support for multiple image feature related APIs for configuring image generation and notification of a video stream. Add "GET_IMAGES" to the list of supported API names for the GetDataEndpoint API.
* api-change:``sagemaker``: SageMaker Autopilot adds new metrics for all candidate models generated by Autopilot experiments; RStudio on SageMaker now allows users to bring your own development environment in a custom image.
* api-change:``kinesis-video-archived-media``: Add support for GetImages API  for retrieving images from a video stream


1.25.5
======

* api-change:``organizations``: This release adds the INVALID_PAYMENT_INSTRUMENT as a fail reason and an error message.
* api-change:``synthetics``: CloudWatch Synthetics has introduced a new feature to provide customers with an option to delete the underlying resources that Synthetics canary creates when the user chooses to delete the canary.
* api-change:``outposts``: This release adds a new API called ListAssets to the Outposts SDK, which lists the hardware assets in an Outpost.


1.25.4
======

* api-change:``rds``: Feature - Adds support for Internet Protocol Version 6 (IPv6) on RDS database instances.
* api-change:``codeguru-reviewer``: Amazon CodeGuru Reviewer now supports suppressing recommendations from being generated on specific files and directories.
* api-change:``ssm``: Update the StartChangeRequestExecution, adding TargetMaps to the Runbook parameter
* api-change:``mediaconvert``: AWS Elemental MediaConvert SDK nows supports creation of Dolby Vision profile 8.1, the ability to generate black frames of video, and introduces audio-only DASH and CMAF support.
* api-change:``wafv2``: You can now inspect all request headers and all cookies. You can now specify how to handle oversize body contents in your rules that inspect the body.


1.25.3
======

* api-change:``auditmanager``: This release adds documentation updates for Audit Manager. We provided examples of how to use the Custom_ prefix for the keywordValue attribute. We also provided more details about the DeleteAssessmentReport operation.
* api-change:``network-firewall``: AWS Network Firewall adds support for stateful threat signature AWS managed rule groups.
* api-change:``ec2``: This release adds support to query the public key and creation date of EC2 Key Pairs. Additionally, the format (pem or ppk) of a key pair can be specified when creating a new key pair.
* api-change:``braket``: This release enables Braket Hybrid Jobs with Embedded Simulators to have multiple instances.
* api-change:``guardduty``: Documentation update for API description.
* api-change:``connect``: This release introduces an API for changing the current agent status of a user in Connect.


1.25.2
======

* api-change:``rekognition``: This release adds support to configure stream-processor resources for label detections on streaming-videos. UpateStreamProcessor API is also launched with this release, which could be used to update an existing stream-processor.
* api-change:``cloudtrail``: Increases the retention period maximum to 2557 days. Deprecates unused fields of the ListEventDataStores API response. Updates documentation.
* api-change:``lookoutequipment``: This release adds the following new features: 1) Introduces an option for automatic schema creation 2) Now allows for Ingestion of data containing most common errors and allows automatic data cleaning 3) Introduces new API ListSensorStatistics that gives further information about the ingested data
* api-change:``iotwireless``: Add list support for event configurations, allow to get and update event configurations by resource type, support LoRaWAN events; Make NetworkAnalyzerConfiguration as a resource, add List, Create, Delete API support; Add FCntStart attribute support for ABP WirelessDevice.
* api-change:``amplify``: Documentation only update to support the Amplify GitHub App feature launch
* api-change:``chime-sdk-media-pipelines``: For Amazon Chime SDK meetings, the Amazon Chime Media Pipelines SDK allows builders to capture audio, video, and content share streams. You can also capture meeting events, live transcripts, and data messages. The pipelines save the artifacts to an Amazon S3 bucket that you designate.
* api-change:``sagemaker``: Amazon SageMaker Autopilot adds support for custom validation dataset and validation ratio through the CreateAutoMLJob and DescribeAutoMLJob APIs.


1.25.1
======

* api-change:``lightsail``: This release adds support for Lightsail load balancer HTTP to HTTPS redirect and TLS policy configuration.
* api-change:``sagemaker``: SageMaker Inference Recommender now accepts customer KMS key ID for encryption of endpoints and compilation outputs created during inference recommendation.
* api-change:``pricing``: Documentation updates for Price List API
* api-change:``glue``: This release adds documentation for the APIs to create, read, delete, list, and batch read of AWS Glue custom patterns, and for Lake Formation configuration settings in the AWS Glue crawler.
* api-change:``cloudfront``: CloudFront now supports the Server-Timing header in HTTP responses sent from CloudFront. You can use this header to view metrics that help you gain insights about the behavior and performance of CloudFront. To use this header, enable it in a response headers policy.
* api-change:``ivschat``: Adds new APIs for IVS Chat, a feature for building interactive chat experiences alongside an IVS broadcast.
* api-change:``network-firewall``: AWS Network Firewall now enables customers to use a customer managed AWS KMS key for the encryption of their firewall resources.


1.25.0
======

* api-change:``gamelift``: Documentation updates for Amazon GameLift.
* api-change:``mq``: This release adds the CRITICAL_ACTION_REQUIRED broker state and the ActionRequired API property. CRITICAL_ACTION_REQUIRED informs you when your broker is degraded. ActionRequired provides you with a code which you can use to find instructions in the Developer Guide on how to resolve the issue.
* feature:IMDS: Added resiliency mechanisms to IMDS Credential Fetcher
* api-change:``securityhub``: Security Hub now lets you opt-out of auto-enabling the defaults standards (CIS and FSBP) in accounts that are auto-enabled with Security Hub via Security Hub's integration with AWS Organizations.
* api-change:``connect``: This release adds SearchUsers API which can be used to search for users with a Connect Instance
* api-change:``rds-data``: Support to receive SQL query results in the form of a simplified JSON string. This enables developers using the new JSON string format to more easily convert it to an object using popular JSON string parsing libraries.


1.24.46
=======

* api-change:``chime-sdk-meetings``: Include additional exceptions types.
* api-change:``ec2``: Adds support for waiters that automatically poll for a deleted NAT Gateway until it reaches the deleted state.


1.24.45
=======

* api-change:``wisdom``: This release updates the GetRecommendations API to include a trigger event list for classifying and grouping recommendations.
* api-change:``elasticache``: Doc only update for ElastiCache
* api-change:``iottwinmaker``: General availability (GA) for AWS IoT TwinMaker. For more information, see https://docs.aws.amazon.com/iot-twinmaker/latest/apireference/Welcome.html
* api-change:``secretsmanager``: Documentation updates for Secrets Manager
* api-change:``mediatailor``: This release introduces tiered channels and adds support for live sources. Customers using a STANDARD channel can now create programs using live sources.
* api-change:``storagegateway``: This release adds support for minimum of 5 character length virtual tape barcodes.
* api-change:``lookoutmetrics``: Added DetectMetricSetConfig API for detecting configuration required for creating metric set from provided S3 data source.
* api-change:``iotsitewise``: This release adds 3 new batch data query APIs : BatchGetAssetPropertyValue, BatchGetAssetPropertyValueHistory and BatchGetAssetPropertyAggregates
* api-change:``glue``: This release adds APIs to create, read, delete, list, and batch read of Glue custom entity types


1.24.44
=======

* api-change:``macie2``: Sensitive data findings in Amazon Macie now indicate how Macie found the sensitive data that produced a finding (originType).
* api-change:``rds``: Added a new cluster-level attribute to set the capacity range for Aurora Serverless v2 instances.
* api-change:``mgn``: Removed required annotation from input fields in Describe operations requests. Added quotaValue to ServiceQuotaExceededException
* api-change:``connect``: This release adds APIs to search, claim, release, list, update, and describe phone numbers. You can also use them to associate and disassociate contact flows to phone numbers.


1.24.43
=======

* api-change:``textract``: This release adds support for specifying and extracting information from documents using the Queries feature within Analyze Document API
* api-change:``worklink``: Amazon WorkLink is no longer supported. This will be removed in a future version of the SDK.
* api-change:``ssm``: Added offset support for specifying the number of days to wait after the date and time specified by a CRON expression when creating SSM association.
* api-change:``autoscaling``: EC2 Auto Scaling now adds default instance warm-up times for all scaling activities, health check replacements, and other replacement events in the Auto Scaling instance lifecycle.
* api-change:``personalize``: Adding StartRecommender and StopRecommender APIs for Personalize.
* api-change:``kendra``: Amazon Kendra now provides a data source connector for Quip. For more information, see https://docs.aws.amazon.com/kendra/latest/dg/data-source-quip.html
* api-change:``polly``: Amazon Polly adds new Austrian German voice - Hannah. Hannah is available as Neural voice only.
* api-change:``transfer``: This release contains corrected HomeDirectoryMappings examples for several API functions: CreateAccess, UpdateAccess, CreateUser, and UpdateUser,.
* api-change:``kms``: Adds support for KMS keys and APIs that generate and verify HMAC codes
* api-change:``redshift``: Introduces new fields for LogDestinationType and LogExports on EnableLogging requests and Enable/Disable/DescribeLogging responses. Customers can now select CloudWatch Logs as a destination for their Audit Logs.


1.24.42
=======

* api-change:``lightsail``: This release adds support to describe the synchronization status of the account-level block public access feature for your Amazon Lightsail buckets.
* api-change:``rds``: Removes Amazon RDS on VMware with the deletion of APIs related to Custom Availability Zones and Media installation
* api-change:``athena``: This release adds subfields, ErrorMessage, Retryable, to the AthenaError response object in the GetQueryExecution API when a query fails.


1.24.41
=======

* api-change:``batch``: Enables configuration updates for compute environments with BEST_FIT_PROGRESSIVE and SPOT_CAPACITY_OPTIMIZED allocation strategies.
* api-change:``ec2``: Documentation updates for Amazon EC2.
* api-change:``cloudwatch``: Update cloudwatch client to latest version
* api-change:``appstream``: Includes updates for create and update fleet APIs to manage the session scripts locations for Elastic fleets.
* api-change:``glue``: Auto Scaling for Glue version 3.0 and later jobs to dynamically scale compute resources. This SDK change provides customers with the auto-scaled DPU usage
* api-change:``appflow``: Enables users to pass custom token URL parameters for Oauth2 authentication during create connector profile


1.24.40
=======

* api-change:``cloudwatch``: Update cloudwatch client to latest version
* api-change:``fsx``: This release adds support for deploying FSx for ONTAP file systems in a single Availability Zone.


1.24.39
=======

* api-change:``ec2``: X2idn and X2iedn instances are powered by 3rd generation Intel Xeon Scalable processors with an all-core turbo frequency up to 3.5 GHzAmazon EC2. C6a instances are powered by 3rd generation AMD EPYC processors.
* api-change:``devops-guru``: This release adds new APIs DeleteInsight to deletes the insight along with the associated anomalies, events and recommendations.
* api-change:``efs``: Update efs client to latest version
* api-change:``iottwinmaker``: This release adds the following new features: 1) ListEntities API now supports search using ExternalId. 2) BatchPutPropertyValue and GetPropertyValueHistory API now allows users to represent time in sub-second level precisions.


1.24.38
=======

* api-change:``amplifyuibuilder``: In this release, we have added the ability to bind events to component level actions.
* api-change:``apprunner``: This release adds tracing for App Runner services with X-Ray using AWS Distro for OpenTelemetry. New APIs: CreateObservabilityConfiguration, DescribeObservabilityConfiguration, ListObservabilityConfigurations, and DeleteObservabilityConfiguration. Updated APIs: CreateService and UpdateService.
* api-change:``workspaces``: Added API support that allows customers to create GPU-enabled WorkSpaces using EC2 G4dn instances.


1.24.37
=======

* api-change:``mediaconvert``: AWS Elemental MediaConvert SDK has added support for the pass-through of WebVTT styling to WebVTT outputs, pass-through of KLV metadata to supported formats, and improved filter support for processing 444/RGB content.
* api-change:``wafv2``: Add a new CurrentDefaultVersion field to ListAvailableManagedRuleGroupVersions API response; add a new VersioningSupported boolean to each ManagedRuleGroup returned from ListAvailableManagedRuleGroups API response.
* api-change:``mediapackage-vod``: This release adds ScteMarkersSource as an available field for Dash Packaging Configurations. When set to MANIFEST, MediaPackage will source the SCTE-35 markers from the manifest. When set to SEGMENTS, MediaPackage will source the SCTE-35 markers from the segments.


1.24.36
=======

* api-change:``apigateway``: ApiGateway CLI command get-usage now includes usagePlanId, startDate, and endDate fields in the output to match documentation.
* api-change:``personalize``: This release provides tagging support in AWS Personalize.
* api-change:``pi``: Adds support for DocumentDB to the Performance Insights API.
* api-change:``events``: Update events client to latest version
* api-change:``docdb``: Added support to enable/disable performance insights when creating or modifying db instances
* api-change:``sagemaker``: Amazon Sagemaker Notebook Instances now supports G5 instance types


1.24.35
=======

* bugfix:Proxy: Fix failure case for IP proxy addresses using TLS-in-TLS. `boto/botocore#2652 <https://github.com/boto/botocore/pull/2652>`__
* api-change:``config``: Add resourceType enums for AWS::EMR::SecurityConfiguration and AWS::SageMaker::CodeRepository
* api-change:``panorama``: Added Brand field to device listings.
* api-change:``lambda``: This release adds new APIs for creating and managing Lambda Function URLs and adds a new FunctionUrlAuthType parameter to the AddPermission API. Customers can use Function URLs to create built-in HTTPS endpoints on their functions.
* api-change:``kendra``: Amazon Kendra now provides a data source connector for Box. For more information, see https://docs.aws.amazon.com/kendra/latest/dg/data-source-box.html


1.24.34
=======

* api-change:``securityhub``: Added additional ASFF details for RdsSecurityGroup AutoScalingGroup, ElbLoadBalancer, CodeBuildProject and RedshiftCluster.
* api-change:``fsx``: Provide customers more visibility into file system status by adding new "Misconfigured Unavailable" status for Amazon FSx for Windows File Server.
* api-change:``s3control``: Documentation-only update for doc bug fixes for the S3 Control API docs.
* api-change:``datasync``: AWS DataSync now supports Amazon FSx for OpenZFS locations.


1.24.33
=======

* api-change:``iot``: AWS IoT - AWS IoT Device Defender adds support to list metric datapoints collected for IoT devices through the ListMetricValues API
* api-change:``servicecatalog``: This release adds ProvisioningArtifictOutputKeys to DescribeProvisioningParameters to reference the outputs of a Provisioned Product and deprecates ProvisioningArtifactOutputs.
* api-change:``sms``: Revised product update notice for SMS console deprecation.
* api-change:``proton``: SDK release to support tagging for AWS Proton Repository resource
* enhancement:AWSCRT: Upgrade awscrt version to 0.13.8


1.24.32
=======

* api-change:``connect``: This release updates these APIs: UpdateInstanceAttribute, DescribeInstanceAttribute and ListInstanceAttributes. You can use it to programmatically enable/disable multi-party conferencing using attribute type MULTI_PARTY_CONFERENCING on the specified Amazon Connect instance.


1.24.31
=======

* api-change:``cloudcontrol``: SDK release for Cloud Control API in Amazon Web Services China (Beijing) Region, operated by Sinnet, and Amazon Web Services China (Ningxia) Region, operated by NWCD
* api-change:``pinpoint-sms-voice-v2``: Amazon Pinpoint now offers a version 2.0 suite of SMS and voice APIs, providing increased control over sending and configuration. This release is a new SDK for sending SMS and voice messages called PinpointSMSVoiceV2.
* api-change:``workspaces``: Added APIs that allow you to customize the logo, login message, and help links in the WorkSpaces client login page. To learn more, visit https://docs.aws.amazon.com/workspaces/latest/adminguide/customize-branding.html
* api-change:``route53-recovery-cluster``: This release adds a new API "ListRoutingControls" to list routing control states using the highly reliable Route 53 ARC data plane endpoints.
* api-change:``databrew``: This AWS Glue Databrew release adds feature to support ORC as an input format.
* api-change:``auditmanager``: This release adds documentation updates for Audit Manager. The updates provide data deletion guidance when a customer deregisters Audit Manager or deregisters a delegated administrator.
* api-change:``grafana``: This release adds tagging support to the Managed Grafana service. New APIs: TagResource, UntagResource and ListTagsForResource. Updates: add optional field tags to support tagging while calling CreateWorkspace.


1.24.30
=======

* api-change:``iot-data``: Update the default AWS IoT Core Data Plane endpoint from VeriSign signed to ATS signed. If you have firewalls with strict egress rules, configure the rules to grant you access to data-ats.iot.[region].amazonaws.com or data-ats.iot.[region].amazonaws.com.cn.
* api-change:``ec2``: This release simplifies the auto-recovery configuration process enabling customers to set the recovery behavior to disabled or default
* api-change:``fms``: AWS Firewall Manager now supports the configuration of third-party policies that can use either the centralized or distributed deployment models.
* api-change:``fsx``: This release adds support for modifying throughput capacity for FSx for ONTAP file systems.
* api-change:``iot``: Doc only update for IoT that fixes customer-reported issues.


1.24.29
=======

* api-change:``organizations``: This release provides the new CloseAccount API that enables principals in the management account to close any member account within an organization.


1.24.28
=======

* api-change:``medialive``: This release adds support for selecting a maintenance window.
* api-change:``acm-pca``: Updating service name entities


1.24.27
=======

* api-change:``ec2``: This is release adds support for Amazon VPC Reachability Analyzer to analyze path through a Transit Gateway.
* api-change:``ssm``: This Patch Manager release supports creating, updating, and deleting Patch Baselines for Rocky Linux OS.
* api-change:``batch``: Bug Fix: Fixed a bug where shapes were marked as unboxed and were not serialized and sent over the wire, causing an API error from the service.


1.24.26
=======

* api-change:``lambda``: Adds support for increased ephemeral storage (/tmp) up to 10GB for Lambda functions. Customers can now provision up to 10 GB of ephemeral storage per function instance, a 20x increase over the previous limit of 512 MB.
* api-change:``config``: Added new APIs GetCustomRulePolicy and GetOrganizationCustomRulePolicy, and updated existing APIs PutConfigRule, DescribeConfigRule, DescribeConfigRuleEvaluationStatus, PutOrganizationConfigRule, DescribeConfigRule to support a new feature for building AWS Config rules with AWS CloudFormation Guard
* api-change:``transcribe``: This release adds an additional parameter for subtitling with Amazon Transcribe batch jobs: outputStartIndex.


1.24.25
=======

* api-change:``redshift``: This release adds a new [--encrypted | --no-encrypted] field in restore-from-cluster-snapshot API. Customers can now restore an unencrypted snapshot to a cluster encrypted with AWS Managed Key or their own KMS key.
* api-change:``ebs``: Increased the maximum supported value for the Timeout parameter of the StartSnapshot API from 60 minutes to 4320 minutes.  Changed the HTTP error code for ConflictException from 503 to 409.
* api-change:``gamesparks``: Released the preview of Amazon GameSparks, a fully managed AWS service that provides a multi-service backend for game developers.
* api-change:``elasticache``: Doc only update for ElastiCache
* api-change:``transfer``: Documentation updates for AWS Transfer Family to describe how to remove an associated workflow from a server.
* api-change:``auditmanager``: This release updates 1 API parameter, the SnsArn attribute. The character length and regex pattern for the SnsArn attribute have been updated, which enables you to deselect an SNS topic when using the UpdateSettings operation.
* api-change:``ssm``: Update AddTagsToResource, ListTagsForResource, and RemoveTagsFromResource APIs to reflect the support for tagging Automation resources. Includes other minor documentation updates.


1.24.24
=======

* api-change:``location``: Amazon Location Service now includes a MaxResults parameter for GetDevicePositionHistory requests.
* api-change:``polly``: Amazon Polly adds new Catalan voice - Arlet. Arlet is available as Neural voice only.
* api-change:``lakeformation``: The release fixes the incorrect permissions called out in the documentation - DESCRIBE_TAG, ASSOCIATE_TAG, DELETE_TAG, ALTER_TAG. This trebuchet release fixes the corresponding SDK and documentation.
* api-change:``ecs``: Documentation only update to address tickets
* api-change:``ce``: Added three new APIs to support tagging and resource-level authorization on Cost Explorer resources: TagResource, UntagResource, ListTagsForResource.  Added optional parameters to CreateCostCategoryDefinition, CreateAnomalySubscription and CreateAnomalyMonitor APIs to support Tag On Create.


1.24.23
=======

* api-change:``ram``: Document improvements to the RAM API operations and parameter descriptions.
* api-change:``ecr``: This release includes a fix in the DescribeImageScanFindings paginated output.
* api-change:``quicksight``: AWS QuickSight Service Features - Expand public API support for group management.
* api-change:``chime-sdk-meetings``: Add support for media replication to link multiple WebRTC media sessions together to reach larger and global audiences. Participants connected to a replica session can be granted access to join the primary session and can switch sessions with their existing WebRTC connection
* api-change:``mediaconnect``: This release adds support for selecting a maintenance window.


1.24.22
=======

* enhancement:jmespath: Add env markers to get working version of jmespath for python 3.6
* api-change:``glue``: Added 9 new APIs for AWS Glue Interactive Sessions: ListSessions, StopSession, CreateSession, GetSession, DeleteSession, RunStatement, GetStatement, ListStatements, CancelStatement


1.24.21
=======

* enhancement:Dependency: Added support for jmespath 1.0
* api-change:``amplifybackend``: Adding the ability to customize Cognito verification messages for email and SMS in CreateBackendAuth and UpdateBackendAuth. Adding deprecation documentation for ForgotPassword in CreateBackendAuth and UpdateBackendAuth
* api-change:``acm-pca``: AWS Certificate Manager (ACM) Private Certificate Authority (CA) now supports customizable certificate subject names and extensions.
* api-change:``ssm-incidents``: Removed incorrect validation pattern for IncidentRecordSource.invokedBy
* api-change:``billingconductor``: This is the initial SDK release for AWS Billing Conductor. The AWS Billing Conductor is a customizable billing service, allowing you to customize your billing data to match your desired business structure.
* api-change:``s3outposts``: S3 on Outposts is releasing a new API, ListSharedEndpoints, that lists all endpoints associated with S3 on Outpost, that has been shared by Resource Access Manager (RAM).


1.24.20
=======

* api-change:``robomaker``: This release deprecates ROS, Ubuntu and Gazbeo from RoboMaker Simulation Service Software Suites in favor of user-supplied containers and Relaxed Software Suites.
* api-change:``dataexchange``: This feature enables data providers to use the RevokeRevision operation to revoke subscriber access to a given revision. Subscribers are unable to interact with assets within a revoked revision.
* api-change:``ec2``: Adds the Cascade parameter to the DeleteIpam API. Customers can use this parameter to automatically delete their IPAM, including non-default scopes, pools, cidrs, and allocations. There mustn't be any pools provisioned in the default public scope to use this parameter.
* api-change:``cognito-idp``: Updated EmailConfigurationType and SmsConfigurationType to reflect that you can now choose Amazon SES and Amazon SNS resources in the same Region.
* enhancement:AWSCRT: Upgrade awscrt extra to 0.13.5
* api-change:``location``: New HERE style "VectorHereExplore" and "VectorHereExploreTruck".
* api-change:``ecs``: Documentation only update to address tickets
* api-change:``keyspaces``: Fixing formatting issues in CLI and SDK documentation
* api-change:``rds``: Various documentation improvements


1.24.19
=======

* api-change:``kendra``: Amazon Kendra now provides a data source connector for Slack. For more information, see https://docs.aws.amazon.com/kendra/latest/dg/data-source-slack.html
* api-change:``timestream-query``: Amazon Timestream Scheduled Queries now support Timestamp datatype in a multi-measure record.
* enhancement:Stubber: Added support for modeled exception fields when adding errors to a client stub. Implements boto/boto3`#3178 <https://github.com/boto/botocore/issues/3178>`__.
* api-change:``elasticache``: Doc only update for ElastiCache
* api-change:``config``: Add resourceType enums for AWS::ECR::PublicRepository and AWS::EC2::LaunchTemplate


1.24.18
=======

* api-change:``outposts``: This release adds address filters for listSites
* api-change:``lambda``: Adds PrincipalOrgID support to AddPermission API. Customers can use it to manage permissions to lambda functions at AWS Organizations level.
* api-change:``secretsmanager``: Documentation updates for Secrets Manager.
* api-change:``connect``: This release adds support for enabling Rich Messaging when starting a new chat session via the StartChatContact API. Rich Messaging enables the following formatting options: bold, italics, hyperlinks, bulleted lists, and numbered lists.
* api-change:``chime``: Chime VoiceConnector Logging APIs will now support MediaMetricLogs. Also CreateMeetingDialOut now returns AccessDeniedException.


1.24.17
=======

* api-change:``transcribe``: Documentation fix for API `StartMedicalTranscriptionJobRequest`, now showing min sample rate as 16khz
* api-change:``transfer``: Adding more descriptive error types for managed workflows
* api-change:``lexv2-models``: Update lexv2-models client to latest version


1.24.16
=======

* api-change:``comprehend``: Amazon Comprehend now supports extracting the sentiment associated with entities such as brands, products and services from text documents.


1.24.15
=======

* api-change:``eks``: Introducing a new enum for NodeGroup error code: Ec2SubnetMissingIpv6Assignment
* api-change:``keyspaces``: Adding link to CloudTrail section in Amazon Keyspaces Developer Guide
* api-change:``mediaconvert``: AWS Elemental MediaConvert SDK has added support for reading timecode from AVCHD sources and now provides the ability to segment WebVTT at the same interval as the video and audio in HLS packages.


1.24.14
=======

* api-change:``chime-sdk-meetings``: Adds support for Transcribe language identification feature to the StartMeetingTranscription API.
* api-change:``ecs``: Amazon ECS UpdateService API now supports additional parameters: loadBalancers, propagateTags, enableECSManagedTags, and serviceRegistries
* api-change:``migration-hub-refactor-spaces``: AWS Migration Hub Refactor Spaces documentation update.


1.24.13
=======

* api-change:``synthetics``: Allow custom handler function.
* api-change:``transfer``: Add waiters for server online and offline.
* api-change:``devops-guru``: Amazon DevOps Guru now integrates with Amazon CodeGuru Profiler. You can view CodeGuru Profiler recommendations for your AWS Lambda function in DevOps Guru. This feature is enabled by default for new customers as of 3/4/2022. Existing customers can enable this feature with UpdateEventSourcesConfig.
* api-change:``macie``: Amazon Macie Classic (macie) has been discontinued and is no longer available. A new Amazon Macie (macie2) is now available with significant design improvements and additional features.
* api-change:``ec2``: Documentation updates for Amazon EC2.
* api-change:``sts``: Documentation updates for AWS Security Token Service.
* api-change:``connect``: This release updates the *InstanceStorageConfig APIs so they support a new ResourceType: REAL_TIME_CONTACT_ANALYSIS_SEGMENTS. Use this resource type to enable streaming for real-time contact analysis and to associate the Kinesis stream where real-time contact analysis segments will be published.


1.24.12
=======

* api-change:``greengrassv2``: Doc only update that clarifies Create Deployment section.
* api-change:``fsx``: This release adds support for data repository associations to use root ("/") as the file system path
* api-change:``kendra``: Amazon Kendra now suggests spell corrections for a query. For more information, see https://docs.aws.amazon.com/kendra/latest/dg/query-spell-check.html
* api-change:``appflow``: Launching Amazon AppFlow Marketo as a destination connector SDK.
* api-change:``timestream-query``: Documentation only update for SDK and CLI


1.24.11
=======

* api-change:``gamelift``: Minor updates to address errors.
* api-change:``cloudtrail``: Add bytesScanned field into responses of DescribeQuery and GetQueryResults.
* api-change:``athena``: This release adds support for S3 Object Ownership by allowing the S3 bucket owner full control canned ACL to be set when Athena writes query results to S3 buckets.
* api-change:``keyspaces``: This release adds support for data definition language (DDL) operations
* api-change:``ecr``: This release adds support for tracking images lastRecordedPullTime.


1.24.10
=======

* api-change:``mediapackage``: This release adds Hybridcast as an available profile option for Dash Origin Endpoints.
* api-change:``rds``: Documentation updates for Multi-AZ DB clusters.
* api-change:``mgn``: Add support for GP3 and IO2 volume types. Add bootMode to LaunchConfiguration object (and as a parameter to UpdateLaunchConfigurationRequest).
* api-change:``kafkaconnect``: Adds operation for custom plugin deletion (DeleteCustomPlugin) and adds new StateDescription field to DescribeCustomPlugin and DescribeConnector responses to return errors from asynchronous resource creation.


1.24.9
======

* api-change:``finspace-data``: Add new APIs for managing Users and Permission Groups.
* api-change:``amplify``: Add repositoryCloneMethod field for hosting an Amplify app. This field shows what authorization method is used to clone the repo: SSH, TOKEN, or SIGV4.
* api-change:``fsx``: This release adds support for the following FSx for OpenZFS features: snapshot lifecycle transition messages, force flag for deleting file systems with child resources, LZ4 data compression, custom record sizes, and unsetting volume quotas and reservations.
* api-change:``fis``: This release adds logging support for AWS Fault Injection Simulator experiments. Experiment templates can now be configured to send experiment activity logs to Amazon CloudWatch Logs or to an S3 bucket.
* api-change:``route53-recovery-cluster``: This release adds a new API option to enable overriding safety rules to allow routing control state updates.
* api-change:``amplifyuibuilder``: We are adding the ability to configure workflows and actions for components.
* api-change:``athena``: This release adds support for updating an existing named query.
* api-change:``ec2``: This release adds support for new AMI property 'lastLaunchedTime'
* api-change:``servicecatalog-appregistry``: AppRegistry is deprecating Application and Attribute-Group Name update feature. In this release, we are marking the name attributes for Update APIs as deprecated to give a heads up to our customers.


1.24.8
======

* api-change:``elasticache``: Doc only update for ElastiCache
* api-change:``panorama``: Added NTP server configuration parameter to ProvisionDevice operation. Added alternate software fields to DescribeDevice response


1.24.7
======

* api-change:``route53``: SDK doc update for Route 53 to update some parameters with new information.
* api-change:``databrew``: This AWS Glue Databrew release adds feature to merge job outputs into a max number of files for S3 File output type.
* api-change:``transfer``: Support automatic pagination when listing AWS Transfer Family resources.
* api-change:``s3control``: Amazon S3 Batch Operations adds support for new integrity checking capabilities in Amazon S3.
* api-change:``s3``: This release adds support for new integrity checking capabilities in Amazon S3. You can choose from four supported checksum algorithms for data integrity checking on your upload and download requests. In addition, AWS SDK can automatically calculate a checksum as it streams data into S3
* api-change:``fms``: AWS Firewall Manager now supports the configuration of AWS Network Firewall policies with either centralized or distributed deployment models. This release also adds support for custom endpoint configuration, where you can choose which Availability Zones to create firewall endpoints in.
* api-change:``lightsail``: This release adds support to delete and create Lightsail default key pairs that you can use with Lightsail instances.
* api-change:``autoscaling``: You can now hibernate instances in a warm pool to stop instances without deleting their RAM contents. You can now also return instances to the warm pool on scale in, instead of always terminating capacity that you will need later.


1.24.6
======

* api-change:``transfer``: The file input selection feature provides the ability to use either the originally uploaded file or the output file from the previous workflow step, enabling customers to make multiple copies of the original file while keeping the source file intact for file archival.
* api-change:``lambda``: Lambda releases .NET 6 managed runtime to be available in all commercial regions.
* api-change:``textract``: Added support for merged cells and column header for table response.


1.24.5
======

* api-change:``translate``: This release enables customers to use translation settings for formality customization in their synchronous translation output.
* api-change:``wafv2``: Updated descriptions for logging configuration.
* api-change:``apprunner``: AWS App Runner adds a Java platform (Corretto 8, Corretto 11 runtimes) and a Node.js 14 runtime.


1.24.4
======

* api-change:``imagebuilder``: This release adds support to enable faster launching for Windows AMIs created by EC2 Image Builder.
* api-change:``customer-profiles``: This release introduces apis CreateIntegrationWorkflow, DeleteWorkflow, ListWorkflows, GetWorkflow and GetWorkflowSteps. These apis are used to manage and view integration workflows.
* api-change:``dynamodb``: DynamoDB ExecuteStatement API now supports Limit as a request parameter to specify the maximum number of items to evaluate. If specified, the service will process up to the Limit and the results will include a LastEvaluatedKey value to continue the read in a subsequent operation.


1.24.3
======

* api-change:``transfer``: Properties for Transfer Family used with SFTP, FTP, and FTPS protocols. Display Banners are bodies of text that can be displayed before and/or after a user authenticates onto a server using one of the previously mentioned protocols.
* api-change:``gamelift``: Increase string list limit from 10 to 100.
* api-change:``budgets``: This change introduces DescribeBudgetNotificationsForAccount API which returns budget notifications for the specified account


1.24.2
======

* api-change:``iam``: Documentation updates for AWS Identity and Access Management (IAM).
* api-change:``redshift``: SDK release for Cross region datasharing and cost-control for cross region datasharing
* api-change:``evidently``: Add support for filtering list of experiments and launches by status
* api-change:``backup``: AWS Backup add new S3_BACKUP_OBJECT_FAILED and S3_RESTORE_OBJECT_FAILED event types in BackupVaultNotifications events list.


1.24.1
======

* api-change:``ec2``: Documentation updates for EC2.
* api-change:``budgets``: Adds support for auto-adjusting budgets, a new budget method alongside fixed and planned. Auto-adjusting budgets introduces new metadata to configure a budget limit baseline using a historical lookback average or current period forecast.
* api-change:``ce``: AWS Cost Anomaly Detection now supports SNS FIFO topic subscribers.
* api-change:``glue``: Support for optimistic locking in UpdateTable
* api-change:``ssm``: Assorted ticket fixes and updates for AWS Systems Manager.


1.24.0
======

* api-change:``appflow``: Launching Amazon AppFlow SAP as a destination connector SDK.
* feature:Parser: Adding support for parsing int/long types in rest-json response headers.
* api-change:``rds``: Adds support for determining which Aurora PostgreSQL versions support Babelfish.
* api-change:``athena``: This release adds a subfield, ErrorType, to the AthenaError response object in the GetQueryExecution API when a query fails.


1.23.54
=======

* api-change:``ssm``: Documentation updates for AWS Systems Manager.


1.23.53
=======

* api-change:``cloudformation``: This SDK release adds AWS CloudFormation Hooks HandlerErrorCodes
* api-change:``lookoutvision``: This release makes CompilerOptions in Lookout for Vision's StartModelPackagingJob's Configuration object optional.
* api-change:``pinpoint``: This SDK release adds a new paramater creation date for GetApp and GetApps Api call
* api-change:``sns``: Customer requested typo fix in API documentation.
* api-change:``wafv2``: Adds support for AWS WAF Fraud Control account takeover prevention (ATP), with configuration options for the new managed rule group AWSManagedRulesATPRuleSet and support for application integration SDKs for Android and iOS mobile apps.


1.23.52
=======

* api-change:``cloudformation``: This SDK release is for the feature launch of AWS CloudFormation Hooks.


1.23.51
=======

* api-change:``kendra``: Amazon Kendra now provides a data source connector for Amazon FSx. For more information, see https://docs.aws.amazon.com/kendra/latest/dg/data-source-fsx.html
* api-change:``apprunner``: This release adds support for App Runner to route outbound network traffic of a service through an Amazon VPC. New API: CreateVpcConnector, DescribeVpcConnector, ListVpcConnectors, and DeleteVpcConnector. Updated API: CreateService, DescribeService, and UpdateService.
* api-change:``s3control``: This release adds support for S3 Batch Replication. Batch Replication lets you replicate existing objects, already replicated objects to new destinations, and objects that previously failed to replicate. Customers will receive object-level visibility of progress and a detailed completion report.
* api-change:``sagemaker``: Autopilot now generates an additional report with information on the performance of the best model, such as a Confusion matrix and  Area under the receiver operating characteristic (AUC-ROC). The path to the report can be found in CandidateArtifactLocations.


1.23.50
=======

* api-change:``auditmanager``: This release updates 3 API parameters. UpdateAssessmentFrameworkControlSet now requires the controls attribute, and CreateAssessmentFrameworkControl requires the id attribute. Additionally, UpdateAssessmentFramework now has a minimum length constraint for the controlSets attribute.
* api-change:``synthetics``: Adding names parameters to the Describe APIs.
* api-change:``ssm-incidents``: Update RelatedItem enum to support SSM Automation
* api-change:``events``: Update events client to latest version
* enhancement:Lambda Request Header: Adding request header for Lambda recursion detection.


1.23.49
=======

* api-change:``athena``: You can now optionally specify the account ID that you expect to be the owner of your query results output location bucket in Athena. If the account ID of the query results bucket owner does not match the specified account ID, attempts to output to the bucket will fail with an S3 permissions error.
* api-change:``rds``: updates for RDS Custom for Oracle 12.1 support
* api-change:``lakeformation``: Add support for calling Update Table Objects without a TransactionId.


1.23.48
=======

* api-change:``ec2``: adds support for AMIs in Recycle Bin
* api-change:``robomaker``: The release deprecates the use various APIs of RoboMaker Deployment Service in favor of AWS IoT GreenGrass v2.0.
* api-change:``meteringmarketplace``: Add CustomerAWSAccountId to ResolveCustomer API response and increase UsageAllocation limit to 2500.
* api-change:``rbin``: Add EC2 Image recycle bin support.


1.23.47
=======

* api-change:``emr``: Update emr client to latest version
* api-change:``personalize``: Adding minRecommendationRequestsPerSecond attribute to recommender APIs.
* enhancement:Request headers: Adding request headers with retry information.
* api-change:``appflow``: Launching Amazon AppFlow Custom Connector SDK.
* api-change:``dynamodb``: Documentation update for DynamoDB Java SDK.
* api-change:``iot``: This release adds support for configuring AWS IoT logging level per client ID, source IP, or principal ID.
* api-change:``comprehend``: Amazon Comprehend now supports sharing and importing custom trained models from one AWS account to another within the same region.
* api-change:``ce``: Doc-only update for Cost Explorer API that adds INVOICING_ENTITY dimensions
* api-change:``fis``: Added GetTargetResourceType and ListTargetResourceTypesAPI actions. These actions return additional details about resource types and parameters that can be targeted by FIS actions. Added a parameters field for the targets that can be specified in experiment templates.
* api-change:``es``: Allows customers to get progress updates for blue/green deployments
* api-change:``glue``: Launch Protobuf support for AWS Glue Schema Registry
* api-change:``elasticache``: Documentation update for AWS ElastiCache


1.23.46
=======

* api-change:``appconfigdata``: Documentation updates for AWS AppConfig Data.
* api-change:``athena``: This release adds a field, AthenaError, to the GetQueryExecution response object when a query fails.
* api-change:``appconfig``: Documentation updates for AWS AppConfig
* api-change:``cognito-idp``: Doc updates for Cognito user pools API Reference.
* api-change:``secretsmanager``: Feature are ready to release on Jan 28th
* api-change:``sagemaker``: This release added a new NNA accelerator compilation support for Sagemaker Neo.


1.23.45
=======

* api-change:``ec2``: X2ezn instances are powered by Intel Cascade Lake CPUs that deliver turbo all core frequency of up to 4.5 GHz and up to 100 Gbps of networking bandwidth
* api-change:``kafka``: Amazon MSK has updated the CreateCluster and UpdateBrokerStorage API that allows you to specify volume throughput during cluster creation and broker volume updates.
* api-change:``connect``: This release adds support for configuring a custom chat duration when starting a new chat session via the StartChatContact API. The default value for chat duration is 25 hours, minimum configurable value is 1 hour (60 minutes) and maximum configurable value is 7 days (10,080 minutes).
* api-change:``amplify``: Doc only update to the description of basicauthcredentials to describe the required encoding and format.
* api-change:``opensearch``: Allows customers to get progress updates for blue/green deployments


1.23.44
=======

* api-change:``frauddetector``: Added new APIs for viewing past predictions and obtaining prediction metadata including prediction explanations: ListEventPredictions and GetEventPredictionMetadata
* api-change:``ebs``: Documentation updates for Amazon EBS Direct APIs.
* api-change:``codeguru-reviewer``: Added failure state and adjusted timeout in waiter
* api-change:``securityhub``: Adding top level Sample boolean field
* api-change:``sagemaker``: API changes relating to Fail steps in model building pipeline and add PipelineExecutionFailureReason in PipelineExecutionSummary.


1.23.43
=======

* api-change:``fsx``: This release adds support for growing SSD storage capacity and growing/shrinking SSD IOPS for FSx for ONTAP file systems.
* api-change:``efs``: Update efs client to latest version
* api-change:``connect``: This release adds support for custom vocabularies to be used with Contact Lens. Custom vocabularies improve transcription accuracy for one or more specific words.
* api-change:``guardduty``: Amazon GuardDuty expands threat detection coverage to protect Amazon Elastic Kubernetes Service (EKS) workloads.


1.23.42
=======

* api-change:``route53-recovery-readiness``: Updated documentation for Route53 Recovery Readiness APIs.


1.23.41
=======

* enhancement:Exceptions: ProxyConnectionError previously provided the full proxy URL. User info will now be appropriately masked if needed.
* api-change:``mediaconvert``: AWS Elemental MediaConvert SDK has added support for 4K AV1 output resolutions & 10-bit AV1 color, the ability to ingest sidecar Dolby Vision XML metadata files, and the ability to flag WebVTT and IMSC tracks for accessibility in HLS.
* api-change:``transcribe``: Add support for granular PIIEntityTypes when using Batch ContentRedaction.


1.23.40
=======

* api-change:``guardduty``: Amazon GuardDuty findings now include remoteAccountDetails under AwsApiCallAction section if instance credential is exfiltrated.
* api-change:``connect``: This release adds tagging support for UserHierarchyGroups resource.
* api-change:``mediatailor``: This release adds support for multiple Segment Delivery Configurations. Users can provide a list of names and URLs when creating or editing a source location. When retrieving content, users can send a header to choose which URL should be used to serve content.
* api-change:``fis``: Added action startTime and action endTime timestamp fields to the ExperimentAction object
* api-change:``ec2``: C6i, M6i and R6i instances are powered by a third-generation Intel Xeon Scalable processor (Ice Lake) delivering all-core turbo frequency of 3.5 GHz


1.23.39
=======

* api-change:``macie2``: This release of the Amazon Macie API introduces stricter validation of requests to create custom data identifiers.
* api-change:``ec2-instance-connect``: Adds support for ED25519 keys. PushSSHPublicKey Availability Zone parameter is now optional. Adds EC2InstanceStateInvalidException for instances that are not running. This was previously a service exception, so this may require updating your code to handle this new exception.


1.23.38
=======

* api-change:``ivs``: This release adds support for the new Thumbnail Configuration property for Recording Configurations. For more information see https://docs.aws.amazon.com/ivs/latest/userguide/record-to-s3.html
* api-change:``storagegateway``: Documentation update for adding bandwidth throttling support for S3 File Gateways.
* api-change:``location``: This release adds the CalculateRouteMatrix API which calculates routes for the provided departure and destination positions. The release also deprecates the use of pricing plan across all verticals.
* api-change:``cloudtrail``: This release fixes a documentation bug in the description for the readOnly field selector in advanced event selectors. The description now clarifies that users omit the readOnly field selector to select both Read and Write management events.
* api-change:``ec2``: Add support for AWS Client VPN client login banner and session timeout.


1.23.37
=======

* enhancement:Configuration: Adding support for `defaults_mode` configuration. The `defaults_mode` will be used to determine how certain default configuration options are resolved in the SDK.


1.23.36
=======

* api-change:``config``: Update ResourceType enum with values for CodeDeploy, EC2 and Kinesis resources
* api-change:``application-insights``: Application Insights support for Active Directory and SharePoint
* api-change:``honeycode``: Added read and write api support for multi-select picklist. And added errorcode field to DescribeTableDataImportJob API output, when import job fails.
* api-change:``ram``: This release adds the ListPermissionVersions API which lists the versions for a given permission.
* api-change:``lookoutmetrics``: This release adds a new DeactivateAnomalyDetector API operation.


1.23.35
=======

* api-change:``pinpoint``: Adds JourneyChannelSettings to WriteJourneyRequest
* api-change:``lexv2-runtime``: Update lexv2-runtime client to latest version
* api-change:``nimble``: Amazon Nimble Studio now supports validation for Launch Profiles. Launch Profiles now report static validation results after create/update to detect errors in network or active directory configuration.
* api-change:``glue``: This SDK release adds support to pass run properties when starting a workflow run
* api-change:``ssm``: AWS Systems Manager adds category support for DescribeDocument API
* api-change:``elasticache``: AWS ElastiCache for Redis has added a new Engine Log LogType in LogDelivery feature. You can now publish the Engine Log from your Amazon ElastiCache for Redis clusters to Amazon CloudWatch Logs and Amazon Kinesis Data Firehose.


1.23.34
=======

* api-change:``lexv2-models``: Update lexv2-models client to latest version
* api-change:``elasticache``: Doc only update for ElastiCache
* api-change:``honeycode``: Honeycode is releasing new APIs to allow user to create, delete and list tags on resources.
* api-change:``ec2``: Hpc6a instances are powered by a third-generation AMD EPYC processors (Milan) delivering all-core turbo frequency of 3.4 GHz
* api-change:``fms``: Shield Advanced policies for Amazon CloudFront resources now support automatic application layer DDoS mitigation. The max length for SecurityServicePolicyData ManagedServiceData is now 8192 characters, instead of 4096.
* api-change:``pi``: This release adds three Performance Insights APIs. Use ListAvailableResourceMetrics to get available metrics, GetResourceMetadata to get feature metadata, and ListAvailableResourceDimensions to list available dimensions. The AdditionalMetrics field in DescribeDimensionKeys retrieves per-SQL metrics.


1.23.33
=======

* api-change:``finspace-data``: Documentation updates for FinSpace.
* api-change:``rds``: This release adds the db-proxy event type to support subscribing to RDS Proxy events.
* api-change:``ce``: Doc only update for Cost Explorer API that fixes missing clarifications for MatchOptions definitions
* api-change:``kendra``: Amazon Kendra now supports advanced query language and query-less search.
* api-change:``workspaces``: Introducing new APIs for Workspaces audio optimization with Amazon Connect: CreateConnectClientAddIn, DescribeConnectClientAddIns, UpdateConnectClientAddIn and DeleteConnectClientAddIn.
* api-change:``iotevents-data``: This release provides documentation updates for Timer.timestamp in the IoT Events API Reference Guide.
* api-change:``ec2``: EC2 Capacity Reservations now supports RHEL instance platforms (RHEL with SQL Server Standard, RHEL with SQL Server Enterprise, RHEL with SQL Server Web, RHEL with HA, RHEL with HA and SQL Server Standard, RHEL with HA and SQL Server Enterprise)


1.23.32
=======

* api-change:``ec2``: New feature: Updated EC2 API to support faster launching for Windows images. Optimized images are pre-provisioned, using snapshots to launch instances up to 65% faster.
* api-change:``compute-optimizer``: Adds support for new Compute Optimizer capability that makes it easier for customers to optimize their EC2 instances by leveraging multiple CPU architectures.
* api-change:``lookoutmetrics``: This release adds FailureType in the response of DescribeAnomalyDetector.
* api-change:``databrew``: This SDK release adds support for specifying a Bucket Owner for an S3 location.
* api-change:``transcribe``: Documentation updates for Amazon Transcribe.


1.23.31
=======

* api-change:``medialive``: This release adds support for selecting the Program Date Time (PDT) Clock source algorithm for HLS outputs.


1.23.30
=======

* api-change:``ec2``: This release introduces On-Demand Capacity Reservation support for Cluster Placement Groups, adds Tags on instance Metadata, and includes documentation updates for Amazon EC2.
* api-change:``mediatailor``: This release adds support for filler slate when updating MediaTailor channels that use the linear playback mode.
* api-change:``opensearch``: Amazon OpenSearch Service adds support for Fine Grained Access Control for existing domains running Elasticsearch version 6.7 and above
* api-change:``iotwireless``: Downlink Queue Management feature provides APIs for customers to manage the queued messages destined to device inside AWS IoT Core for LoRaWAN. Customer can view, delete or purge the queued message(s). It allows customer to preempt the queued messages and let more urgent messages go through.
* api-change:``es``: Amazon OpenSearch Service adds support for Fine Grained Access Control for existing domains running Elasticsearch version 6.7 and above
* api-change:``mwaa``: This release adds a "Source" field that provides the initiator of an update, such as due to an automated patch from AWS or due to modification via Console or API.
* api-change:``appsync``: AppSync: AWS AppSync now supports configurable batching sizes for AWS Lambda resolvers, Direct AWS Lambda resolvers and pipeline functions


1.23.29
=======

* api-change:``cloudtrail``: This release adds support for CloudTrail Lake, a new feature that lets you run SQL-based queries on events that you have aggregated into event data stores. New APIs have been added for creating and managing event data stores, and creating, running, and managing queries in CloudTrail Lake.
* api-change:``iot``: This release adds an automatic retry mechanism for AWS IoT Jobs. You can now define a maximum number of retries for each Job rollout, along with the criteria to trigger the retry for FAILED/TIMED_OUT/ALL(both FAILED an TIMED_OUT) job.
* api-change:``ec2``: This release adds a new API called ModifyVpcEndpointServicePayerResponsibility which allows VPC endpoint service owners to take payer responsibility of their VPC Endpoint connections.
* api-change:``snowball``: Updating validation rules for interfaces used in the Snowball API to tighten security of service.
* api-change:``lakeformation``: Add new APIs for 3rd Party Support for Lake Formation
* api-change:``appstream``: Includes APIs for App Entitlement management regarding entitlement and entitled application association.
* api-change:``eks``: Amazon EKS now supports running applications using IPv6 address space
* api-change:``quicksight``: Multiple Doc-only updates for Amazon QuickSight.
* api-change:``ecs``: Documentation update for ticket fixes.
* api-change:``sagemaker``: Amazon SageMaker now supports running training jobs on ml.g5 instance types.
* api-change:``glue``: Add Delta Lake target support for Glue Crawler and 3rd Party Support for Lake Formation


1.23.28
=======

* api-change:``rekognition``: This release introduces a new field IndexFacesModelVersion, which is the version of the face detect and storage model that was used when indexing the face vector.
* api-change:``s3``: Minor doc-based updates based on feedback bugs received.
* enhancement:JSONFileCache: Add support for __delitem__ in JSONFileCache
* api-change:``s3control``: Documentation updates for the renaming of Glacier to Glacier Flexible Retrieval.


1.23.27
=======

* api-change:``sagemaker``: The release allows users to pass pipeline definitions as Amazon S3 locations and control the pipeline execution concurrency using ParallelismConfiguration. It also adds support of EMR jobs as pipeline steps.
* api-change:``rds``: Multiple doc-only updates for Relational Database Service (RDS)
* api-change:``mediaconvert``: AWS Elemental MediaConvert SDK has added strength levels to the Sharpness Filter and now permits OGG files to be specified as sidecar audio inputs.
* api-change:``greengrassv2``: This release adds the API operations to manage the Greengrass role associated with your account and to manage the core device connectivity information. Greengrass V2 customers can now depend solely on Greengrass V2 SDK for all the API operations needed to manage their fleets.
* api-change:``detective``: Added and updated API operations to support the Detective integration with AWS Organizations. New actions are used to manage the delegated administrator account and the integration configuration.


1.23.26
=======

* api-change:``nimble``: Amazon Nimble Studio adds support for users to upload files during a streaming session using NICE DCV native client or browser.
* api-change:``chime-sdk-messaging``: The Amazon Chime SDK now supports updating message attributes via channel flows
* api-change:``imagebuilder``: Added a note to infrastructure configuration actions and data types concerning delivery of Image Builder event messages to encrypted SNS topics. The key that's used to encrypt the SNS topic must reside in the account that Image Builder runs under.
* api-change:``workmail``: This release allows customers to change their email monitoring configuration in Amazon WorkMail.
* api-change:``transfer``: Property for Transfer Family used with the FTPS protocol. TLS Session Resumption provides a mechanism to resume or share a negotiated secret key between the control and data connection for an FTPS session.
* api-change:``lookoutmetrics``: This release adds support for Causal Relationships. Added new ListAnomalyGroupRelatedMetrics API operation and InterMetricImpactDetails API data type
* api-change:``mediaconnect``: You can now use the Fujitsu-QoS protocol for your MediaConnect sources and outputs to transport content to and from Fujitsu devices.
* api-change:``qldb``: Amazon QLDB now supports journal exports in JSON and Ion Binary formats. This release adds an optional OutputFormat parameter to the ExportJournalToS3 API.


1.23.25
=======

* api-change:``customer-profiles``: This release adds an optional parameter, ObjectTypeNames to the PutIntegration API to support multiple object types per integration option. Besides, this release introduces Standard Order Objects which contain data from third party systems and each order object belongs to a specific profile.
* api-change:``sagemaker``: This release adds a new ContentType field in AutoMLChannel for SageMaker CreateAutoMLJob InputDataConfig.
* api-change:``forecast``: Adds ForecastDimensions field to the DescribeAutoPredictorResponse
* api-change:``securityhub``: Added new resource details objects to ASFF, including resources for Firewall, and RuleGroup, FirewallPolicy Added additional details for AutoScalingGroup, LaunchConfiguration, and S3 buckets.
* api-change:``location``: Making PricingPlan optional as part of create resource API.
* api-change:``redshift``: This release adds API support for managed Redshift datashares. Customers can now interact with a Redshift datashare that is managed by a different service, such as AWS Data Exchange.
* api-change:``apigateway``: Documentation updates for Amazon API Gateway
* api-change:``devops-guru``: Adds Tags support to DescribeOrganizationResourceCollectionHealth
* api-change:``imagebuilder``: This release adds support for importing and exporting VM Images as part of the Image Creation workflow via EC2 VM Import/Export.
* api-change:``datasync``: AWS DataSync now supports FSx Lustre Locations.
* api-change:``finspace-data``: Make dataset description optional and allow s3 export for dataviews


1.23.24
=======

* api-change:``secretsmanager``: Documentation updates for Secrets Manager


1.23.23
=======

* api-change:``lexv2-models``: Update lexv2-models client to latest version
* api-change:``network-firewall``: This release adds support for managed rule groups.
* api-change:``route53-recovery-control-config``: This release adds tagging supports to Route53 Recovery Control Configuration. New APIs: TagResource, UntagResource and ListTagsForResource. Updates: add optional field `tags` to support tagging while calling CreateCluster, CreateControlPanel and CreateSafetyRule.
* api-change:``ec2``: Adds waiters support for internet gateways.
* api-change:``sms``: This release adds SMS discontinuation information to the API and CLI references.
* api-change:``route53domains``: Amazon Route 53 domain registration APIs now support filtering and sorting in the ListDomains API, deleting a domain by using the DeleteDomain API and getting domain pricing information by using the ListPrices API.
* api-change:``savingsplans``: Adds the ability to specify Savings Plans hourly commitments using five digits after the decimal point.


1.23.22
=======

* api-change:``lookoutvision``: This release adds new APIs for packaging an Amazon Lookout for Vision model as an AWS IoT Greengrass component.
* api-change:``sagemaker``: This release added a new Ambarella device(amba_cv2) compilation support for Sagemaker Neo.
* api-change:``comprehendmedical``: This release adds a new set of APIs (synchronous and batch) to support the SNOMED-CT ontology.
* api-change:``health``: Documentation updates for AWS Health
* api-change:``logs``: This release adds AWS Organizations support as condition key in destination policy for cross account Subscriptions in CloudWatch Logs.
* api-change:``outposts``: This release adds the UpdateOutpost API.
* api-change:``support``: Documentation updates for AWS Support.
* api-change:``iot``: This release allows customer to enable caching of custom authorizer on HTTP protocol for clients that use persistent or Keep-Alive connection in order to reduce the number of Lambda invocations.


1.23.21
=======

* api-change:``location``: This release adds support for Accuracy position filtering, position metadata and autocomplete for addresses and points of interest based on partial or misspelled free-form text.
* api-change:``appsync``: AWS AppSync now supports custom domain names, allowing you to associate a domain name that you own with an AppSync API in your account.
* api-change:``route53``: Add PriorRequestNotComplete exception to UpdateHostedZoneComment API


1.23.20
=======

* api-change:``rekognition``: This release added new KnownGender types for Celebrity Recognition.


1.23.19
=======

* api-change:``ram``: This release adds the ability to use the new ResourceRegionScope parameter on List operations that return lists of resources or resource types. This new parameter filters the results by letting you differentiate between global or regional resource types.
* api-change:``networkmanager``: This release adds API support for AWS Cloud WAN.
* api-change:``amplifyuibuilder``: This release introduces the actions and data types for the new Amplify UI Builder API. The Amplify UI Builder API provides a programmatic interface for creating and configuring user interface (UI) component libraries and themes for use in Amplify applications.


1.23.18
=======

* api-change:``sagemaker``: This release enables - 1/ Inference endpoint configuration recommendations and ability to run custom load tests to meet performance needs. 2/ Deploy serverless inference endpoints. 3/ Query, filter and retrieve end-to-end ML lineage graph, and incorporate model quality/bias detection in ML workflow.
* api-change:``kendra``: Experience Builder allows customers to build search applications without writing code. Analytics Dashboard provides quality and usability metrics for Kendra indexes. Custom Document Enrichment allows customers to build a custom ingestion pipeline to pre-process documents and generate metadata.
* api-change:``directconnect``: Adds SiteLink support to private and transit virtual interfaces. SiteLink is a new Direct Connect feature that allows routing between Direct Connect points of presence.
* api-change:``lexv2-models``: Update lexv2-models client to latest version
* api-change:``ec2``: This release adds support for Amazon VPC IP Address Manager (IPAM), which enables you to plan, track, and monitor IP addresses for your workloads. This release also adds support for VPC Network Access Analyzer, which enables you to analyze network access to resources in your Virtual Private Clouds.
* api-change:``shield``: This release adds API support for Automatic Application Layer DDoS Mitigation for AWS Shield Advanced. Customers can now enable automatic DDoS mitigation in count or block mode for layer 7 protected resources.
* api-change:``sagemaker-runtime``: Update sagemaker-runtime client to latest version
* api-change:``devops-guru``: DevOps Guru now provides detailed, database-specific analyses of performance issues and recommends corrective actions for Amazon Aurora database instances with Performance Insights turned on. You can also use AWS tags to choose which resources to analyze and define your applications.
* api-change:``dynamodb``: Add support for Table Classes and introduce the Standard Infrequent Access table class.


1.23.17
=======

* api-change:``s3``: Introduce Amazon S3 Glacier Instant Retrieval storage class and a new setting in S3 Object Ownership to disable ACLs for bucket and the objects in it.
* api-change:``backup-gateway``: Initial release of AWS Backup gateway which enables you to centralize and automate protection of on-premises VMware and VMware Cloud on AWS workloads using AWS Backup.
* api-change:``iot``: Added the ability to enable/disable IoT Fleet Indexing for Device Defender and Named Shadow information, and search them through IoT Fleet Indexing APIs.
* api-change:``ec2``: This release adds support for Is4gen and Im4gn instances. This release also adds a new subnet attribute, enableLniAtDeviceIndex, to support local network interfaces, which are logical networking components that connect an EC2 instance to your on-premises network.
* api-change:``outposts``: This release adds the SupportedHardwareType parameter to CreateOutpost.
* api-change:``storagegateway``: Added gateway type VTL_SNOW. Added new SNOWBALL HostEnvironment for gateways running on a Snowball device. Added new field HostEnvironmentId to serve as an identifier for the HostEnvironment on which the gateway is running.
* api-change:``kinesis``: Amazon Kinesis Data Streams now supports on demand streams.
* api-change:``glue``: Support for DataLake transactions
* api-change:``accessanalyzer``: AWS IAM Access Analyzer now supports policy validation for resource policies attached to S3 buckets and access points. You can run additional policy checks by specifying the S3 resource type you want to attach to your resource policy.
* api-change:``lakeformation``: This release adds support for row and cell-based access control in Lake Formation. It also adds support for Lake Formation Governed Tables, which support ACID transactions and automatic storage optimizations.
* api-change:``kafka``: This release adds three new V2 APIs. CreateClusterV2 for creating both provisioned and serverless clusters. DescribeClusterV2 for getting information about provisioned and serverless clusters and ListClustersV2 for listing all clusters (both provisioned and serverless) in your account.
* api-change:``redshift-data``: Data API now supports serverless queries.
* api-change:``snowball``: Tapeball is to integrate tape gateway onto snowball, it enables customer to transfer local data on the tape to snowball,and then ingest the data into tape gateway on the cloud.
* api-change:``workspaces-web``: This is the initial SDK release for Amazon WorkSpaces Web. Amazon WorkSpaces Web is a low-cost, fully managed WorkSpace built to deliver secure web-based workloads and software-as-a-service (SaaS) application access to users within existing web browsers.
* api-change:``iottwinmaker``: AWS IoT TwinMaker makes it faster and easier to create, visualize and monitor digital twins of real-world systems like buildings, factories and industrial equipment to optimize operations. Learn more: https://docs.aws.amazon.com/iot-twinmaker/latest/apireference/Welcome.html (New Service) (Preview)
* api-change:``fsx``: This release adds support for the FSx for OpenZFS file system type, FSx for Lustre file systems with the Persistent_2 deployment type, and FSx for Lustre file systems with Amazon S3 data repository associations and automatic export policies.


1.23.16
=======

* api-change:``s3``: Amazon S3 Event Notifications adds Amazon EventBridge as a destination and supports additional event types. The PutBucketNotificationConfiguration API can now skip validation of Amazon SQS, Amazon SNS and AWS Lambda destinations.
* api-change:``wellarchitected``: This update provides support for Well-Architected API users to use custom lens features.
* api-change:``rum``: This is the first public release of CloudWatch RUM
* api-change:``rbin``: This release adds support for Recycle Bin.
* api-change:``iotsitewise``: AWS IoT SiteWise now supports retention configuration for the hot tier storage.
* api-change:``compute-optimizer``: Adds support for the enhanced infrastructure metrics paid feature. Also adds support for two new sets of resource efficiency metrics, including savings opportunity metrics and performance improvement opportunity metrics.
* api-change:``ecr``: This release adds supports for pull through cache rules and enhanced scanning.
* api-change:``evidently``: Introducing Amazon CloudWatch Evidently. This is the first public release of Amazon CloudWatch Evidently.
* api-change:``inspector2``: This release adds support for the new Amazon Inspector API. The new Amazon Inspector can automatically discover and scan Amazon EC2 instances and Amazon ECR container images for software vulnerabilities and unintended network exposure, and report centralized findings across multiple AWS accounts.
* api-change:``ssm``: Added two new attributes to DescribeInstanceInformation called SourceId and SourceType along with new string filters SourceIds and SourceTypes to filter instance records.
* api-change:``ec2``: This release adds support for G5g and M6a instances. This release also adds support for Amazon EBS Snapshots Archive, a feature that enables you to archive your EBS snapshots; and Recycle Bin, a feature that enables you to protect your EBS snapshots against accidental deletion.
* api-change:``dataexchange``: This release enables providers and subscribers to use Data Set, Job, and Asset operations to work with API assets from Amazon API Gateway. In addition, this release enables subscribers to use the SendApiAsset operation to invoke a provider's Amazon API Gateway API that they are entitled to.


1.23.15
=======

* api-change:``migration-hub-refactor-spaces``: This is the initial SDK release for AWS Migration Hub Refactor Spaces
* api-change:``textract``: This release adds support for synchronously analyzing identity documents through a new API: AnalyzeID
* api-change:``personalize-runtime``: This release adds inference support for Recommenders.
* api-change:``personalize``: This release adds API support for Recommenders and BatchSegmentJobs.


1.23.14
=======

* api-change:``autoscaling``: Documentation updates for Amazon EC2 Auto Scaling.
* api-change:``mgn``: Application Migration Service now supports an additional replication method that does not require agent installation on each source server. This option is available for source servers running on VMware vCenter versions 6.7 and 7.0.
* api-change:``ec2``: Documentation updates for EC2.
* api-change:``iotdeviceadvisor``: Documentation update for Device Advisor GetEndpoint API
* api-change:``pinpoint``: Added a One-Time Password (OTP) management feature. You can use the Amazon Pinpoint API to generate OTP codes and send them to your users as SMS messages. Your apps can then call the API to verify the OTP codes that your users input
* api-change:``outposts``: This release adds new APIs for working with Outpost sites and orders.


1.23.13
=======

* api-change:``timestream-query``: Releasing Amazon Timestream Scheduled Queries. It makes real-time analytics more performant and cost-effective for customers by calculating and storing frequently accessed aggregates, and other computations, typically used in operational dashboards, business reports, and other analytics applications
* api-change:``elasticache``: Doc only update for ElastiCache
* api-change:``proton``: This release adds APIs for getting the outputs and provisioned stacks for Environments, Pipelines, and ServiceInstances.  You can now add tags to EnvironmentAccountConnections.  It also adds APIs for working with PR-based provisioning.  Also, it adds APIs for syncing templates with a git repository.
* api-change:``translate``: This release enables customers to use translation settings to mask profane words and phrases in their translation output.
* api-change:``lambda``: Remove Lambda function url apis
* api-change:``imagebuilder``: This release adds support for sharing AMIs with Organizations within an EC2 Image Builder Distribution Configuration.
* api-change:``customer-profiles``: This release introduces a new auto-merging feature for profile matching. The auto-merging configurations can be set via CreateDomain API or UpdateDomain API. You can use GetIdentityResolutionJob API and ListIdentityResolutionJobs API to fetch job status.
* api-change:``autoscaling``: Customers can now configure predictive scaling policies to proactively scale EC2 Auto Scaling groups based on any CloudWatch metrics that more accurately represent the load on the group than the four predefined metrics. They can also use math expressions to further customize the metrics.
* api-change:``timestream-write``: This release adds support for multi-measure records and magnetic store writes. Multi-measure records allow customers to store multiple measures in a single table row. Magnetic store writes enable customers to write late arrival data (data with timestamp in the past) directly into the magnetic store.
* api-change:``iotsitewise``: AWS IoT SiteWise now accepts data streams that aren't associated with any asset properties. You can organize data by updating data stream associations.


1.23.12
=======

* api-change:``redshift``: This release adds support for reserved node exchange with restore/resize
* api-change:``elasticache``: Adding support for r6gd instances for Redis with data tiering. In a cluster with data tiering enabled, when available memory capacity is exhausted, the least recently used data is automatically tiered to solid state drives for cost-effective capacity scaling with minimal performance impact.
* api-change:``opensearch``: This release adds an optional parameter dry-run for the UpdateDomainConfig API to perform basic validation checks, and detect the deployment type that will be required for the configuration change, without actually applying the change.
* api-change:``backup``: This release adds new opt-in settings for advanced features for DynamoDB backups
* api-change:``iot``: This release introduces a new feature, Managed Job Template, for AWS IoT Jobs Service. Customers can now use service provided managed job templates to easily create jobs for supported standard job actions.
* api-change:``iotwireless``: Two new APIs, GetNetworkAnalyzerConfiguration and UpdateNetworkAnalyzerConfiguration, are added for the newly released Network Analyzer feature which enables customers to view real-time frame information and logs from LoRaWAN devices and gateways.
* api-change:``workspaces``: Documentation updates for Amazon WorkSpaces
* api-change:``s3``: Introduce two new Filters to S3 Lifecycle configurations - ObjectSizeGreaterThan and ObjectSizeLessThan. Introduce a new way to trigger actions on noncurrent versions by providing the number of newer noncurrent versions along with noncurrent days.
* api-change:``elbv2``: Update elbv2 client to latest version
* api-change:``macie2``: Documentation updates for Amazon Macie
* api-change:``ec2``: This release adds a new parameter ipv6Native to the allow creation of IPv6-only subnets using the CreateSubnet operation, and the operation ModifySubnetAttribute includes new parameters to modify subnet attributes to use resource-based naming and enable DNS resolutions for Private DNS name.
* api-change:``sqs``: Amazon SQS adds a new queue attribute, SqsManagedSseEnabled, which enables server-side queue encryption using SQS owned encryption keys.
* api-change:``ecs``: Documentation update for ARM support on Amazon ECS.
* api-change:``sts``: Documentation updates for AWS Security Token Service.
* api-change:``finspace-data``: Update documentation for createChangeset API.
* api-change:``dynamodb``: DynamoDB PartiQL now supports ReturnConsumedCapacity, which returns capacity units consumed by PartiQL APIs if the request specified returnConsumedCapacity parameter. PartiQL APIs include ExecuteStatement, BatchExecuteStatement, and ExecuteTransaction.
* api-change:``lambda``: Release Lambda event source filtering for SQS, Kinesis Streams, and DynamoDB Streams.
* api-change:``iotdeviceadvisor``: This release introduces a new feature for Device Advisor: ability to execute multiple test suites in parallel for given customer account. You can use GetEndpoint API to get the device-level test endpoint and call StartSuiteRun with "parallelRun=true" to run suites in parallel.
* api-change:``rds``: Adds support for Multi-AZ DB clusters for RDS for MySQL and RDS for PostgreSQL.


1.23.11
=======

* api-change:``connect``: This release adds support for UpdateContactFlowMetadata, DeleteContactFlow and module APIs. For details, see the Release Notes in the Amazon Connect Administrator Guide.
* api-change:``dms``: Added new S3 endpoint settings to allow to convert the current UTC time into a specified time zone when a date partition folder is created. Using with 'DatePartitionedEnabled'.
* api-change:``es``: This release adds an optional parameter dry-run for the UpdateElasticsearchDomainConfig API to perform basic validation checks, and detect the deployment type that will be required for the configuration change, without actually applying the change.
* api-change:``ssm``: Adds new parameter to CreateActivation API . This parameter is for "internal use only".
* api-change:``chime-sdk-meetings``: Added new APIs for enabling Echo Reduction with Voice Focus.
* api-change:``eks``: Adding missing exceptions to RegisterCluster operation
* api-change:``quicksight``: Add support for Exasol data source, 1 click enterprise embedding and email customization.
* api-change:``cloudformation``: This release include SDK changes for the feature launch of Stack Import to Service Managed StackSet.
* api-change:``rds``: Adds local backup support to Amazon RDS on AWS Outposts.
* api-change:``braket``: This release adds support for Amazon Braket Hybrid Jobs.
* api-change:``s3control``: Added Amazon CloudWatch publishing option for S3 Storage Lens metrics.
* api-change:``finspace-data``: Add new APIs for managing Datasets, Changesets, and Dataviews.


1.23.10
=======

* api-change:``lexv2-runtime``: Update lexv2-runtime client to latest version
* api-change:``cloudformation``: The StackSets ManagedExecution feature will allow concurrency for non-conflicting StackSet operations and queuing the StackSet operations that conflict at a given time for later execution.
* api-change:``redshift``: Added support of default IAM role for CreateCluster, RestoreFromClusterSnapshot and ModifyClusterIamRoles APIs
* api-change:``lambda``: Add support for Lambda Function URLs. Customers can use Function URLs to create built-in HTTPS endpoints on their functions.
* api-change:``appstream``: Includes APIs for managing resources for Elastic fleets: applications, app blocks, and application-fleet associations.
* api-change:``medialive``: This release adds support for specifying a SCTE-35 PID on input. MediaLive now supports SCTE-35 PID selection on inputs containing one or more active SCTE-35 PIDs.
* api-change:``batch``: Documentation updates for AWS Batch.
* api-change:``application-insights``: Application Insights now supports monitoring for HANA


1.23.9
======

* api-change:``ivs``: Add APIs for retrieving stream session information and support for filtering live streams by health.  For more information, see https://docs.aws.amazon.com/ivs/latest/userguide/stream-health.html
* api-change:``lambda``: Added support for CLIENT_CERTIFICATE_TLS_AUTH and SERVER_ROOT_CA_CERTIFICATE as SourceAccessType for MSK and Kafka event source mappings.
* api-change:``chime``: Adds new Transcribe API parameters to StartMeetingTranscription, including support for content identification and redaction (PII & PHI), partial results stabilization, and custom language models.
* api-change:``chime-sdk-meetings``: Adds new Transcribe API parameters to StartMeetingTranscription, including support for content identification and redaction (PII & PHI), partial results stabilization, and custom language models.
* api-change:``lexv2-models``: Update lexv2-models client to latest version
* api-change:``cloudwatch``: Update cloudwatch client to latest version
* api-change:``auditmanager``: This release introduces a new feature for Audit Manager: Dashboard views. You can now view insights data for your active assessments, and quickly identify non-compliant evidence that needs to be remediated.
* api-change:``databrew``: This SDK release adds the following new features: 1) PII detection in profile jobs, 2) Data quality rules, enabling validation of data quality in profile jobs, 3) SQL query-based datasets for Amazon Redshift and Snowflake data sources, and 4) Connecting DataBrew datasets with Amazon AppFlow flows.
* api-change:``redshift-data``: Rolling back Data API serverless features until dependencies are live.
* api-change:``kafka``: Amazon MSK has added a new API that allows you to update the connectivity settings for an existing cluster to enable public accessibility.
* api-change:``forecast``: NEW CreateExplanability API that helps you understand how attributes such as price, promotion, etc. contributes to your forecasted values; NEW CreateAutoPredictor API that trains up to 40% more accurate forecasting model, saves up to 50% of retraining time, and provides model level explainability.
* api-change:``appconfig``: Add Type to support feature flag configuration profiles


1.23.8
======

* api-change:``appconfigdata``: AWS AppConfig Data is a new service that allows you to retrieve configuration deployed by AWS AppConfig. See the AppConfig user guide for more details on getting started. https://docs.aws.amazon.com/appconfig/latest/userguide/what-is-appconfig.html
* api-change:``drs``: Introducing AWS Elastic Disaster Recovery (AWS DRS), a new service that minimizes downtime and data loss with fast, reliable recovery of on-premises and cloud-based applications using affordable storage, minimal compute, and point-in-time recovery.
* api-change:``apigateway``: Documentation updates for Amazon API Gateway.
* api-change:``sns``: Amazon SNS introduces the PublishBatch API, which enables customers to publish up to 10 messages per API request. The new API is valid for Standard and FIFO topics.
* api-change:``redshift-data``: Data API now supports serverless requests.
* api-change:``amplifybackend``: New APIs to support the Amplify Storage category. Add and manage file storage in your Amplify app backend.


1.23.7
======

* api-change:``location``: This release adds the support for Relevance, Distance, Time Zone, Language and Interpolated Address for Geocoding and Reverse Geocoding.
* api-change:``cloudtrail``: CloudTrail Insights now supports ApiErrorRateInsight, which enables customers to identify unusual activity in their AWS account based on API error codes and their rate.


1.23.6
======

* api-change:``migrationhubstrategy``: AWS SDK for Migration Hub Strategy Recommendations. It includes APIs to start the portfolio assessment, import portfolio data for assessment, and to retrieve recommendations. For more information, see the AWS Migration Hub documentation at https://docs.aws.amazon.com/migrationhub/index.html
* api-change:``ec2``: Adds a new VPC Subnet attribute "EnableDns64." When enabled on IPv6 Subnets, the Amazon-Provided DNS Resolver returns synthetic IPv6 addresses for IPv4-only destinations.
* api-change:``wafv2``: Your options for logging web ACL traffic now include Amazon CloudWatch Logs log groups and Amazon S3 buckets.
* api-change:``dms``: Add Settings in JSON format for the source GCP MySQL endpoint
* api-change:``ssm``: Adds support for Session Reason and Max Session Duration for Systems Manager Session Manager.
* api-change:``appstream``: This release includes support for images of AmazonLinux2 platform type.
* api-change:``eks``: Adding Tags support to Cluster Registrations.
* api-change:``transfer``: AWS Transfer Family now supports integrating a custom identity provider using AWS Lambda


1.23.5
======

* api-change:``ec2``: C6i instances are powered by a third-generation Intel Xeon Scalable processor (Ice Lake) delivering all-core turbo frequency of 3.5 GHz. G5 instances feature up to 8 NVIDIA A10G Tensor Core GPUs and second generation AMD EPYC processors.
* api-change:``ssm``: This Patch Manager release supports creating Patch Baselines for RaspberryPi OS (formerly Raspbian)
* api-change:``devops-guru``: Add support for cross account APIs.
* api-change:``connect``: This release adds APIs for creating and managing scheduled tasks. Additionally, adds APIs to describe and update a contact and list associated references.
* api-change:``mediaconvert``: AWS Elemental MediaConvert SDK has added automatic modes for GOP configuration and added the ability to ingest screen recordings generated by Safari on MacOS 12 Monterey.


1.23.4
======

* api-change:``dynamodb``: Updated Help section for "dynamodb update-contributor-insights" API
* api-change:``ec2``: This release provides an additional route target for the VPC route table.
* api-change:``translate``: This release enables customers to import Multi-Directional Custom Terminology and use Multi-Directional Custom Terminology in both real-time translation and asynchronous batch translation.


1.23.3
======

* api-change:``backup``: AWS Backup SDK provides new options when scheduling backups: select supported services and resources that are assigned to a particular tag, linked to a combination of tags, or can be identified by a partial tag value, and exclude resources from their assignments.
* api-change:``ecs``: This release adds support for container instance health.
* api-change:``resiliencehub``: Initial release of AWS Resilience Hub, a managed service that enables you to define, validate, and track the resilience of your applications on AWS


1.23.2
======

* api-change:``batch``: Adds support for scheduling policy APIs.
* api-change:``health``: Documentation updates for AWS Health.
* api-change:``greengrassv2``: This release adds support for Greengrass core devices running Windows. You can now specify name of a Windows user to run a component.


1.23.1
======

* bugfix:urllib3: Fix NO_OP_TICKET import bug in older versions of urllib3


1.23.0
======

* feature:EndpointResolver: Adding support for resolving modeled FIPS and Dualstack endpoints.
* feature:``six``: Updated vendored version of ``six`` from 1.10.0 to 1.16.0
* api-change:``sagemaker``: SageMaker CreateEndpoint and UpdateEndpoint APIs now support additional deployment configuration to manage traffic shifting options and automatic rollback monitoring. DescribeEndpoint now shows new in-progress deployment details with stage status.
* api-change:``chime-sdk-meetings``: Updated format validation for ids and regions.
* api-change:``wafv2``: You can now configure rules to run a CAPTCHA check against web requests and, as needed, send a CAPTCHA challenge to the client.
* api-change:``ec2``: This release adds internal validation on the GatewayAssociationState field


1.22.12
=======

* api-change:``ec2``: DescribeInstances now returns customer-owned IP addresses for instances running on an AWS Outpost.
* api-change:``translate``: This release enable customers to use their own KMS keys to encrypt output files when they submit a batch transform job.
* api-change:``resourcegroupstaggingapi``: Documentation updates and improvements.


1.22.11
=======

* api-change:``chime-sdk-meetings``: The Amazon Chime SDK Meetings APIs allow software developers to create meetings and attendees for interactive audio, video, screen and content sharing in custom meeting applications which use the Amazon Chime SDK.
* api-change:``sagemaker``: ListDevices and DescribeDevice now show Edge Manager agent version.
* api-change:``connect``: This release adds CRUD operation support for Security profile resource in Amazon Connect
* api-change:``iotwireless``: Adding APIs for the FUOTA (firmware update over the air) and multicast for LoRaWAN devices and APIs to support event notification opt-in feature for Sidewalk related events. A few existing APIs need to be modified for this new feature.
* api-change:``ec2``: This release adds a new instance replacement strategy for EC2 Fleet, Spot Fleet. Now you can select an action to perform when your instance gets a rebalance notification. EC2 Fleet, Spot Fleet can launch a replacement then terminate the instance that received notification after a termination delay


1.22.10
=======

* api-change:``finspace``: Adds superuser and data-bundle parameters to CreateEnvironment API
* api-change:``connectparticipant``: This release adds a new boolean attribute - Connect Participant - to the CreateParticipantConnection API, which can be used to mark the participant as connected.
* api-change:``datasync``: AWS DataSync now supports Hadoop Distributed File System (HDFS) Locations
* api-change:``macie2``: This release adds support for specifying the severity of findings that a custom data identifier produces, based on the number of occurrences of text that matches the detection criteria.


1.22.9
======

* api-change:``cloudfront``: CloudFront now supports response headers policies to add HTTP headers to the responses that CloudFront sends to viewers. You can use these policies to add CORS headers, control browser caching, and more, without modifying your origin or writing any code.
* api-change:``connect``: Amazon Connect Chat now supports real-time message streaming.
* api-change:``nimble``: Amazon Nimble Studio adds support for users to stop and start streaming sessions.


1.22.8
======

* api-change:``rekognition``: This Amazon Rekognition Custom Labels release introduces the management of datasets with  projects
* api-change:``networkmanager``: This release adds API support to aggregate resources, routes, and telemetry data across a Global Network.
* api-change:``lightsail``: This release adds support to enable access logging for buckets in the Lightsail object storage service.
* api-change:``neptune``: Adds support for major version upgrades to ModifyDbCluster API


1.22.7
======

* api-change:``transcribe``: Transcribe and Transcribe Call Analytics now support automatic language identification along with custom vocabulary, vocabulary filter, custom language model and PII redaction.
* api-change:``application-insights``: Added Monitoring support for SQL Server Failover Cluster Instance. Additionally, added a new API to allow one-click monitoring of containers resources.
* api-change:``rekognition``: This release added new attributes to Rekognition Video GetCelebrityRecognition API operations.
* api-change:``connect``: Amazon Connect Chat now supports real-time message streaming.
* api-change:``ec2``: Support added for AMI sharing with organizations and organizational units in ModifyImageAttribute API


1.22.6
======

* api-change:``gamelift``: Added support for Arm-based AWS Graviton2 instances, such as M6g, C6g, and R6g.
* api-change:``ecs``: Amazon ECS now supports running Fargate tasks on Windows Operating Systems Families which includes Windows Server 2019 Core and Windows Server 2019 Full.
* api-change:``sagemaker``: This release adds support for RStudio on SageMaker.
* api-change:``connectparticipant``: This release adds a new boolean attribute - Connect Participant - to the CreateParticipantConnection API, which can be used to mark the participant as connected.
* api-change:``ec2``: Added new read-only DenyAllIGWTraffic network interface attribute. Added support for DL1 24xlarge instances powered by Habana Gaudi Accelerators for deep learning model training workloads
* api-change:``ssm-incidents``: Updating documentation, adding new field to ConflictException to indicate earliest retry timestamp for some operations, increase maximum length of nextToken fields


1.22.5
======

* api-change:``autoscaling``: This release adds support for attribute-based instance type selection, a new EC2 Auto Scaling feature that lets customers express their instance requirements as a set of attributes, such as vCPU, memory, and storage.
* api-change:``ec2``: This release adds: attribute-based instance type selection for EC2 Fleet, Spot Fleet, a feature that lets customers express instance requirements as attributes like vCPU, memory, and storage; and Spot placement score, a feature that helps customers identify an optimal location to run Spot workloads.
* api-change:``eks``: EKS managed node groups now support BOTTLEROCKET_x86_64 and BOTTLEROCKET_ARM_64 AMI types.
* api-change:``sagemaker``: This release allows customers to describe one or more versioned model packages through BatchDescribeModelPackage, update project via UpdateProject, modify and read customer metadata properties using Create, Update and Describe ModelPackage and enables cross account registration of model packages.
* enhancement:Session: Added `get_partition_for_region` allowing partition lookup by region name.
* api-change:``textract``: This release adds support for asynchronously analyzing invoice and receipt documents through two new APIs: StartExpenseAnalysis and GetExpenseAnalysis


1.22.4
======

* api-change:``emr-containers``: This feature enables auto-generation of certificate  to secure the managed-endpoint and removes the need for customer provided certificate-arn during managed-endpoint setup.
* api-change:``chime-sdk-messaging``: The Amazon Chime SDK now supports push notifications through Amazon Pinpoint
* api-change:``chime-sdk-identity``: The Amazon Chime SDK now supports push notifications through Amazon Pinpoint


1.22.3
======

* api-change:``rds``: This release adds support for Amazon RDS Custom, which is a new RDS management type that gives you full access to your database and operating system. For more information, see https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/rds-custom.html
* api-change:``auditmanager``: This release introduces a new feature for Audit Manager: Custom framework sharing. You can now share your custom frameworks with another AWS account, or replicate them into another AWS Region under your own account.
* api-change:``ec2``: This release adds support to create a VPN Connection that is not attached to a Gateway at the time of creation. Use this to create VPNs associated with Core Networks, or modify your VPN and attach a gateway using the modify API after creation.
* api-change:``route53resolver``: New API for ResolverConfig, which allows autodefined rules for reverse DNS resolution to be disabled for a VPC


1.22.2
======

* api-change:``quicksight``: Added QSearchBar option for GenerateEmbedUrlForRegisteredUser ExperienceConfiguration to support Q search bar embedding
* api-change:``auditmanager``: This release introduces character restrictions for ControlSet names. We updated regex patterns for the following attributes: ControlSet, CreateAssessmentFrameworkControlSet, and UpdateAssessmentFrameworkControlSet.
* api-change:``chime``: Chime VoiceConnector and VoiceConnectorGroup APIs will now return an ARN.


1.22.1
======

* api-change:``connect``: Released Amazon Connect hours of operation API for general availability (GA). This API also supports AWS CloudFormation. For more information, see Amazon Connect Resource Type Reference in the AWS CloudFormation User Guide.


1.22.0
======

* api-change:``appflow``: Feature to add support for  JSON-L format for S3 as a source.
* api-change:``mediapackage-vod``: MediaPackage passes through digital video broadcasting (DVB) subtitles into the output.
* api-change:``mediaconvert``: AWS Elemental MediaConvert SDK has added support for specifying caption time delta in milliseconds and the ability to apply color range legalization to source content other than AVC video.
* api-change:``mediapackage``: When enabled, MediaPackage passes through digital video broadcasting (DVB) subtitles into the output.
* api-change:``panorama``: General availability for AWS Panorama. AWS SDK for Panorama includes APIs to manage your devices and nodes, and deploy computer vision applications to the edge. For more information, see the AWS Panorama documentation at http://docs.aws.amazon.com/panorama
* feature:Serialization: rest-json serialization defaults aligned across AWS SDKs
* api-change:``directconnect``: This release adds 4 new APIS, which needs to be public able
* api-change:``securityhub``: Added support for cross-Region finding aggregation, which replicates findings from linked Regions to a single aggregation Region. Added operations to view, enable, update, and delete the finding aggregation.


1.21.65
=======

* api-change:``dataexchange``: This release adds support for our public preview of AWS Data Exchange for Amazon Redshift. This enables data providers to list products including AWS Data Exchange datashares for Amazon Redshift, giving subscribers read-only access to provider data in Amazon Redshift.
* api-change:``chime-sdk-messaging``: The Amazon Chime SDK now allows developers to execute business logic on in-flight messages before they are delivered to members of a messaging channel with channel flows.


1.21.64
=======

* api-change:``quicksight``: AWS QuickSight Service  Features    - Add IP Restriction UI and public APIs support.
* enchancement:AWSCRT: Upgrade awscrt extra to 0.12.5
* api-change:``ivs``: Bug fix: remove unsupported maxResults and nextToken pagination parameters from ListTagsForResource


1.21.63
=======

* api-change:``efs``: Update efs client to latest version
* api-change:``glue``: Enable S3 event base crawler API.


1.21.62
=======

* api-change:``elbv2``: Update elbv2 client to latest version
* api-change:``autoscaling``: Amazon EC2 Auto Scaling now supports filtering describe Auto Scaling groups API using tags
* api-change:``sagemaker``: This release updates the provisioning artifact ID to an optional parameter in CreateProject API. The provisioning artifact ID defaults to the latest provisioning artifact ID of the product if you don't provide one.
* api-change:``robomaker``: Adding support to GPU simulation jobs as well as non-ROS simulation jobs.


1.21.61
=======

* api-change:``config``: Adding Config support for AWS::OpenSearch::Domain
* api-change:``ec2``: This release adds support for additional VPC Flow Logs delivery options to S3, such as Apache Parquet formatted files, Hourly partitions and Hive-compatible S3 prefixes
* api-change:``storagegateway``: Adding support for Audit Logs on NFS shares and Force Closing Files on SMB shares.
* api-change:``workmail``: This release adds APIs for adding, removing and retrieving details of mail domains
* api-change:``kinesisanalyticsv2``: Support for Apache Flink 1.13 in Kinesis Data Analytics. Changed the required status of some Update properties to better fit the corresponding Create properties.


1.21.60
=======

* api-change:``cloudsearch``: Adds an additional validation exception for Amazon CloudSearch configuration APIs for better error handling.
* api-change:``ecs``: Documentation only update to address tickets.
* api-change:``mediatailor``: MediaTailor now supports ad prefetching.
* api-change:``ec2``: EncryptionSupport for InstanceStorageInfo added to DescribeInstanceTypes API


1.21.59
=======

* api-change:``elbv2``: Update elbv2 client to latest version
* bugfix:Signing: SigV4QueryAuth and CrtSigV4QueryAuth now properly respect AWSRequest.params while signing boto/botocore`#2521 <https://github.com/boto/botocore/issues/2521>`__
* api-change:``medialive``: This release adds support for Transport Stream files as an input type to MediaLive encoders.
* api-change:``ec2``: Documentation update for Amazon EC2.
* api-change:``frauddetector``: New model type: Transaction Fraud Insights, which is optimized for online transaction fraud. Stored Events, which allows customers to send and store data directly within Amazon Fraud Detector. Batch Import, which allows customers to upload a CSV file of historic event data for processing and storage


1.21.58
=======

* api-change:``lexv2-runtime``: Update lexv2-runtime client to latest version
* api-change:``lexv2-models``: Update lexv2-models client to latest version
* api-change:``secretsmanager``: Documentation updates for Secrets Manager
* api-change:``securityhub``: Added new resource details objects to ASFF, including resources for WAF rate-based rules, EC2 VPC endpoints, ECR repositories, EKS clusters, X-Ray encryption, and OpenSearch domains. Added additional details for CloudFront distributions, CodeBuild projects, ELB V2 load balancers, and S3 buckets.
* api-change:``mediaconvert``: AWS Elemental MediaConvert has added the ability to set account policies which control access restrictions for HTTP, HTTPS, and S3 content sources.
* api-change:``ec2``: This release removes a requirement for filters on SearchLocalGatewayRoutes operations.


1.21.57
=======

* api-change:``kendra``: Amazon Kendra now supports indexing and querying documents in different languages.
* api-change:``grafana``: Initial release of the SDK for Amazon Managed Grafana API.
* api-change:``firehose``: Allow support for Amazon Opensearch Service(successor to Amazon Elasticsearch Service) as a Kinesis Data Firehose delivery destination.
* api-change:``backup``: Launch of AWS Backup Vault Lock, which protects your backups from malicious and accidental actions, works with existing backup policies, and helps you meet compliance requirements.
* api-change:``schemas``: Removing unused request/response objects.
* api-change:``chime``: This release enables customers to configure Chime MediaCapturePipeline via API.


1.21.56
=======

* api-change:``sagemaker``: This release adds a new TrainingInputMode FastFile for SageMaker Training APIs.
* api-change:``amplifybackend``: Adding a new field 'AmplifyFeatureFlags' to the response of the GetBackend operation. It will return a stringified version of the cli.json file for the given Amplify project.
* api-change:``fsx``: This release adds support for Lustre 2.12 to FSx for Lustre.
* api-change:``kendra``: Amazon Kendra now supports integration with AWS SSO


1.21.55
=======

* api-change:``workmail``: This release allows customers to change their inbound DMARC settings in Amazon WorkMail.
* api-change:``location``: Add support for PositionFiltering.
* api-change:``application-autoscaling``: With this release, Application Auto Scaling adds support for Amazon Neptune. Customers can now automatically add or remove Read Replicas of their Neptune clusters to keep the average CPU Utilization at the target value specified by the customers.
* api-change:``ec2``: Released Capacity Reservation Fleet, a feature of Amazon EC2 Capacity Reservations, which provides a way to manage reserved capacity across instance types. For more information: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/cr-fleets.html
* api-change:``glue``: This release adds tag as an input of CreateConnection
* api-change:``backup``: AWS Backup Audit Manager framework report.


1.21.54
=======

* api-change:``codebuild``: CodeBuild now allows you to select how batch build statuses are sent to the source provider for a project.
* api-change:``efs``: Update efs client to latest version
* api-change:``kms``: Added SDK examples for ConnectCustomKeyStore, CreateCustomKeyStore, CreateKey, DeleteCustomKeyStore, DescribeCustomKeyStores, DisconnectCustomKeyStore, GenerateDataKeyPair, GenerateDataKeyPairWithoutPlaintext, GetPublicKey, ReplicateKey, Sign, UpdateCustomKeyStore and Verify APIs


1.21.53
=======

* api-change:``synthetics``: CloudWatch Synthetics now enables customers to choose a customer managed AWS KMS key or an Amazon S3-managed key instead of an AWS managed key (default) for the encryption of artifacts that the canary stores in Amazon S3. CloudWatch Synthetics also supports artifact S3 location updation now.
* api-change:``ssm``: When "AutoApprovable" is true for a Change Template, then specifying --auto-approve (boolean) in Start-Change-Request-Execution will create a change request that bypasses approver review. (except for change calendar restrictions)
* api-change:``apprunner``: This release contains several minor bug fixes.


1.21.52
=======

* api-change:``network-firewall``: This release adds support for strict ordering for stateful rule groups. Using strict ordering, stateful rules are evaluated in the exact order in which you provide them.
* api-change:``dataexchange``: This release enables subscribers to set up automatic exports of newly published revisions using the new EventAction API.
* api-change:``workmail``: This release adds support for mobile device access overrides management in Amazon WorkMail.
* api-change:``account``: This release of the Account Management API enables customers to manage the alternate contacts for their AWS accounts. For more information, see https://docs.aws.amazon.com/accounts/latest/reference/accounts-welcome.html
* api-change:``workspaces``: Added CreateUpdatedWorkspaceImage API to update WorkSpace images with latest software and drivers. Updated DescribeWorkspaceImages API to display if there are updates available for WorkSpace images.
* api-change:``cloudcontrol``: Initial release of the SDK for AWS Cloud Control API
* api-change:``macie2``: Amazon S3 bucket metadata now indicates whether an error or a bucket's permissions settings prevented Amazon Macie from retrieving data about the bucket or the bucket's objects.


1.21.51
=======

* api-change:``lambda``: Adds support for Lambda functions powered by AWS Graviton2 processors. Customers can now select the CPU architecture for their functions.
* api-change:``sesv2``: This release includes the ability to use 2048 bits RSA key pairs for DKIM in SES, either with Easy DKIM or Bring Your Own DKIM.
* api-change:``amp``: This release adds alert manager and rule group namespace APIs


1.21.50
=======

* api-change:``transfer``: Added changes for managed workflows feature APIs.
* api-change:``imagebuilder``: Fix description for AmiDistributionConfiguration Name property, which actually refers to the output AMI name. Also updated for consistent terminology to use "base" image, and another update to fix description text.


1.21.49
=======

* api-change:``appintegrations``: The Amazon AppIntegrations service enables you to configure and reuse connections to external applications.
* api-change:``wisdom``: Released Amazon Connect Wisdom, a feature of Amazon Connect, which provides real-time recommendations and search functionality in general availability (GA).  For more information, see https://docs.aws.amazon.com/wisdom/latest/APIReference/Welcome.html.
* api-change:``pinpoint``: Added support for journey with contact center activity
* api-change:``voice-id``: Released the Amazon Voice ID SDK, for usage with the Amazon Connect Voice ID feature released for Amazon Connect.
* api-change:``connect``: This release updates a set of APIs: CreateIntegrationAssociation, ListIntegrationAssociations, CreateUseCase, and StartOutboundVoiceContact. You can use it to create integrations with Amazon Pinpoint for the Amazon Connect Campaigns use case, Amazon Connect Voice ID, and Amazon Connect Wisdom.
* api-change:``elbv2``: Update elbv2 client to latest version


1.21.48
=======

* api-change:``license-manager``: AWS License Manager now allows customers to get the LicenseArn in the Checkout API Response.
* api-change:``ec2``: DescribeInstances now returns Platform Details, Usage Operation, and Usage Operation Update Time.


1.21.47
=======

* api-change:``mediaconvert``: This release adds style and positioning support for caption or subtitle burn-in from rich text sources such as TTML. This release also introduces configurable image-based trick play track generation.
* api-change:``appsync``: Documented the new OpenSearchServiceDataSourceConfig data type. Added deprecation notes to the ElasticsearchDataSourceConfig data type.
* api-change:``ssm``: Added cutoff behavior support for preventing new task invocations from starting when the maintenance window cutoff time is reached.


1.21.46
=======

* api-change:``imagebuilder``: This feature adds support for specifying GP3 volume throughput and configuring instance metadata options for instances launched by EC2 Image Builder.
* api-change:``wafv2``: Added the regex match rule statement, for matching web requests against a single regular expression.
* api-change:``mediatailor``: This release adds support to configure logs for playback configuration.
* api-change:``lexv2-models``: Update lexv2-models client to latest version
* api-change:``iam``: Added changes to OIDC API about not using port numbers in the URL.
* api-change:``license-manager``: AWS License Manager now allows customers to change their Windows Server or SQL license types from Bring-Your-Own-License (BYOL) to License Included or vice-versa (using the customer's media).
* api-change:``mediapackage-vod``: MediaPackage VOD will now return the current processing statuses of an asset's endpoints. The status can be QUEUED, PROCESSING, PLAYABLE, or FAILED.


1.21.45
=======

* api-change:``comprehend``: Amazon Comprehend now supports versioning of custom models, improved training with ONE_DOC_PER_FILE text documents for custom entity recognition, ability to provide specific test sets during training, and live migration to new model endpoints.
* api-change:``iot``: This release adds support for verifying, viewing and filtering AWS IoT Device Defender detect violations with four verification states.
* api-change:``ecr``: This release adds additional support for repository replication
* api-change:``ec2``: This update adds support for downloading configuration templates using new APIs (GetVpnConnectionDeviceTypes and GetVpnConnectionDeviceSampleConfiguration) and Internet Key Exchange version 2 (IKEv2) parameters for many popular CGW devices.


1.21.44
=======

* api-change:``opensearch``: This release adds an optional parameter in the ListDomainNames API to filter domains based on the engine type (OpenSearch/Elasticsearch).
* api-change:``es``: This release adds an optional parameter in the ListDomainNames API to filter domains based on the engine type (OpenSearch/Elasticsearch).
* api-change:``dms``: Optional flag force-planned-failover added to reboot-replication-instance API call. This flag can be used to test a planned failover scenario used during some maintenance operations.


1.21.43
=======

* api-change:``kafkaconnect``: This is the initial SDK release for Amazon Managed Streaming for Apache Kafka Connect (MSK Connect).
* api-change:``macie2``: This release adds support for specifying which managed data identifiers are used by a classification job, and retrieving a list of managed data identifiers that are available.
* api-change:``robomaker``: Adding support to create container based Robot and Simulation applications by introducing an environment field
* api-change:``s3``: Add support for access point arn filtering in S3 CW Request Metrics
* api-change:``transcribe``: This release adds support for subtitling with Amazon Transcribe batch jobs.
* api-change:``sagemaker``: Add API for users to retry a failed pipeline execution or resume a stopped one.
* api-change:``pinpoint``: This SDK release adds a new feature for Pinpoint campaigns, in-app messaging.


1.21.42
=======

* api-change:``sagemaker``: This release adds support for "Project Search"
* api-change:``ec2``: This release adds support for vt1 3xlarge, 6xlarge and 24xlarge instances powered by Xilinx Alveo U30 Media Accelerators for video transcoding workloads
* api-change:``wafv2``: This release adds support for including rate based rules in a rule group.
* api-change:``chime``: Adds support for SipHeaders parameter for CreateSipMediaApplicationCall.
* api-change:``comprehend``: Amazon Comprehend now allows you to train and run PDF and Word documents for custom entity recognition. With PDF and Word formats, you can extract information from documents containing headers, lists and tables.


1.21.41
=======

* api-change:``iot``: AWS IoT Rules Engine adds OpenSearch action. The OpenSearch rule action lets you stream data from IoT sensors and applications to Amazon OpenSearch Service which is a successor to Amazon Elasticsearch Service.
* api-change:``ec2``: Adds support for T3 instances on Amazon EC2 Dedicated Hosts.
* enhancement:Tagged Unions: Introducing support for the `union` trait on structures in request and response objects.


1.21.40
=======

* api-change:``cloudformation``: Doc only update for CloudFormation that fixes several customer-reported issues.
* api-change:``rds``: This release adds support for providing a custom timeout value for finding a scaling point during autoscaling in Aurora Serverless v1.
* api-change:``ecr``: This release updates terminology around KMS keys.
* api-change:``sagemaker``: This release adds support for "Lifecycle Configurations" to SageMaker Studio
* api-change:``transcribe``: This release adds an API option for startTranscriptionJob and startMedicalTranscriptionJob that allows the user to specify encryption context key value pairs for batch jobs.
* api-change:``quicksight``: Add new data source type for Amazon OpenSearch (successor to Amazon ElasticSearch).


1.21.39
=======

* api-change:``emr``: Update emr client to latest version
* api-change:``codeguru-reviewer``: The Amazon CodeGuru Reviewer API now includes the RuleMetadata data object and a Severity attribute on a RecommendationSummary object. A RuleMetadata object contains information about a rule that generates a recommendation. Severity indicates how severe the issue associated with a recommendation is.
* api-change:``lookoutequipment``: Added OffCondition parameter to CreateModel API


1.21.38
=======

* api-change:``opensearch``: Updated Configuration APIs for Amazon OpenSearch Service (successor to Amazon Elasticsearch Service)
* api-change:``ram``: A minor text-only update that fixes several customer issues.
* api-change:``kafka``: Amazon MSK has added a new API that allows you to update the encrypting and authentication settings for an existing cluster.


1.21.37
=======

* api-change:``elasticache``: Doc only update for ElastiCache
* api-change:``amp``: This release adds tagging support for Amazon Managed Service for Prometheus workspace.
* api-change:``forecast``: Predictor creation now supports selecting an accuracy metric to optimize in AutoML and hyperparameter optimization. This release adds additional accuracy metrics for predictors - AverageWeightedQuantileLoss, MAPE and MASE.
* api-change:``xray``: Updated references to AWS KMS keys and customer managed keys to reflect current terminology.
* api-change:``ssm-contacts``: Added SDK examples for SSM-Contacts.
* api-change:``mediapackage``: SPEKE v2 support for live CMAF packaging type. SPEKE v2 is an upgrade to the existing SPEKE API to support multiple encryption keys, it supports live DASH currently.
* api-change:``eks``: Adding RegisterCluster and DeregisterCluster operations, to support connecting external clusters to EKS.


1.21.36
=======

* api-change:``chime-sdk-identity``: Documentation updates for Chime
* api-change:``chime-sdk-messaging``: Documentation updates for Chime
* api-change:``outposts``: This release adds a new API CreateOrder.
* api-change:``frauddetector``: Enhanced GetEventPrediction API response to include risk scores from imported SageMaker models
* api-change:``codeguru-reviewer``: Added support for CodeInconsistencies detectors


1.21.35
=======

* api-change:``acm-pca``: Private Certificate Authority Service now allows customers to enable an online certificate status protocol (OCSP) responder service on their private certificate authorities. Customers can also optionally configure a custom CNAME for their OCSP responder.
* api-change:``s3control``: S3 Multi-Region Access Points provide a single global endpoint to access a data set that spans multiple S3 buckets in different AWS Regions.
* api-change:``accessanalyzer``: Updates service API, documentation, and paginators to support multi-region access points from Amazon S3.
* api-change:``schemas``: This update include the support for Schema Discoverer to discover the events sent to the bus from another account. The feature will be enabled by default when discoverer is created or updated but can also be opt-in or opt-out  by specifying the value for crossAccount.
* api-change:``securityhub``: New ASFF Resources: AwsAutoScalingLaunchConfiguration, AwsEc2VpnConnection, AwsEcrContainerImage. Added KeyRotationStatus to AwsKmsKey. Added AccessControlList, BucketLoggingConfiguration,BucketNotificationConfiguration and BucketNotificationConfiguration to AwsS3Bucket.
* enhancement:s3: Added support for S3 Multi-Region Access Points
* api-change:``efs``: Update efs client to latest version
* api-change:``transfer``: AWS Transfer Family introduces Managed Workflows for creating, executing, monitoring, and standardizing post file transfer processing
* api-change:``ebs``: Documentation updates for Amazon EBS direct APIs.
* api-change:``quicksight``: This release adds support for referencing parent datasets as sources in a child dataset.
* api-change:``fsx``: Announcing Amazon FSx for NetApp ONTAP, a new service that provides fully managed shared storage in the AWS Cloud with the data access and management capabilities of ONTAP.
* enhancement:Signers: Added support for Sigv4a Signing Algorithm
* api-change:``lex-models``: Lex now supports Korean (ko-KR) locale.


1.21.34
=======

* api-change:``ec2``: Added LaunchTemplate support for the IMDS IPv6 endpoint
* api-change:``cloudtrail``: Documentation updates for CloudTrail
* api-change:``mediatailor``: This release adds support for wall clock programs in LINEAR channels.
* api-change:``config``: Documentation updates for config
* api-change:``servicecatalog-appregistry``: Introduction of GetAssociatedResource API and GetApplication response extension for Resource Groups support.


1.21.33
=======

* api-change:``iot``: Added Create/Update/Delete/Describe/List APIs for a new IoT resource named FleetMetric. Added a new Fleet Indexing query API named GetBucketsAggregation. Added a new field named DisconnectedReason in Fleet Indexing query response. Updated their related documentations.
* api-change:``polly``: Amazon Polly adds new South African English voice - Ayanda. Ayanda is available as Neural voice only.
* api-change:``compute-optimizer``: Documentation updates for Compute Optimizer
* api-change:``sqs``: Amazon SQS adds a new queue attribute, RedriveAllowPolicy, which includes the dead-letter queue redrive permission parameters. It defines which source queues can specify dead-letter queues as a JSON object.
* api-change:``memorydb``: Documentation updates for MemoryDB


1.21.32
=======

* api-change:``codebuild``: Documentation updates for CodeBuild
* api-change:``firehose``: This release adds the Dynamic Partitioning feature to Kinesis Data Firehose service for S3 destinations.
* api-change:``kms``: This release has changes to KMS nomenclature to remove the word master from both the "Customer master key" and "CMK" abbreviation and replace those naming conventions with "KMS key".
* api-change:``cloudformation``: AWS CloudFormation allows you to iteratively develop your applications when failures are encountered without rolling back successfully provisioned resources. By specifying stack failure options, you can troubleshoot resources in a CREATE_FAILED or UPDATE_FAILED status.


1.21.31
=======

* api-change:``s3``: Documentation updates for Amazon S3.
* api-change:``emr``: Update emr client to latest version
* api-change:``ec2``: This release adds the BootMode flag to the ImportImage API and showing the detected BootMode of an ImportImage task.


1.21.30
=======

* api-change:``transcribe``: This release adds support for batch transcription in six new languages - Afrikaans, Danish, Mandarin Chinese (Taiwan), New Zealand English, South African English, and Thai.
* api-change:``rekognition``: This release added new attributes to Rekognition RecognizeCelebities and GetCelebrityInfo API operations.
* api-change:``ec2``: Support added for resizing VPC prefix lists
* api-change:``compute-optimizer``: Adds support for 1) the AWS Graviton (AWS_ARM64) recommendation preference for Amazon EC2 instance and Auto Scaling group recommendations, and 2) the ability to get the enrollment statuses for all member accounts of an organization.


1.21.29
=======

* api-change:``fms``: AWS Firewall Manager now supports triggering resource cleanup workflow when account or resource goes out of policy scope for AWS WAF, Security group, AWS Network Firewall, and Amazon Route 53 Resolver DNS Firewall policies.
* api-change:``ec2``: Support added for IMDS IPv6 endpoint
* api-change:``datasync``: Added include filters to CreateTask and UpdateTask, and added exclude filters to StartTaskExecution, giving customers more granular control over how DataSync transfers files, folders, and objects.
* api-change:``events``: AWS CWEvents adds an enum of EXTERNAL for EcsParameters LaunchType for PutTargets API


1.21.28
=======

* api-change:``mediaconvert``: AWS Elemental MediaConvert SDK has added MBAFF encoding support for AVC video and the ability to pass encryption context from the job settings to S3.
* api-change:``polly``: Amazon Polly adds new New Zealand English voice - Aria. Aria is available as Neural voice only.
* api-change:``transcribe``: This release adds support for feature tagging with Amazon Transcribe batch jobs.
* api-change:``ssm``: Updated Parameter Store property for logging improvements.
* api-change:``iot-data``: Updated Publish with support for new Retain flag and added two new API operations: GetRetainedMessage, ListRetainedMessages.


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

