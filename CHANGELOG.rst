=========
CHANGELOG
=========

Next Release (TBD)
------------------
* feature:Regions: Add ability to list regions and endpoints for services in
  a partition.
  (`issue 812 <https://github.com/boto/botocore/pull/812>`__)

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
