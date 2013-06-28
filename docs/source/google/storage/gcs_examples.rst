============
GCS Examples
============

For parameters, please refer to the `latest docs
<https://developers.google.com/storage/docs/json_api/v1/>`_.

Name Requirements
*****************

*Note*: Parameter names in operation calls should be formatted as python_naming, not camelCase.

For example, if the API specifies a parameter ``machineType``, you should pass
it in to the functions as ``machine_type``.

**This ONLY applies to passing parameters into a call function.**

eg::

  op.call(
    machine_type = MACHINE_TYPE
  )
  
**not**::

  op.call(
    machineType = MACHINE_TYPE
  )

Operation Examples
******************

Creating a bucket::
  
  PROJECT = 'your project name'
  
  import botocore.session
  
  session = botocore.session.get_session()
  gcs = session.get_service('gcs') 
  endpoint = gcs.get_endpoint()
  create_bucket = gcs.get_operation('storage.buckets.insert')
  
  bucket_name = 'my_unique_bucket_name'
  
  bucket = {
     'name':bucket_name
  }
  
  response, data = op.call(
    endpoint,
    project=PROJECT,
    zone=DEFAULT_ZONE,
    body=bucket
  )