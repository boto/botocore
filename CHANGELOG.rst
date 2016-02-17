=========
CHANGELOG
=========

1.3.27
======
* feature:``aws rds``: Added support for Cross-account Encrypted (KMS) snapshot
  sharing.
* feature:``aws emr``: Added support for adding EBS storage to EMR instances.
* bugfix:pagination: Refactored pagination to handle non-string service tokens
* bugfix:credentials: Fix race condition in credential provider
