===============================
Passing Resources into botocore
===============================

Many of the Google Cloud APIs require a resource description to be provided. This
is done by setting the ``body`` parameter when calling an operation. Simply fill out
a Python dictionary with the required fields, and pass it to the operation.

eg::
  
  my_resource = {
    'key':'value',
  }
  
  some_operation.call(
    body=my_resource_body
  )

For a detailed description of what each method requires, refer to the
`official documentation
<https://developers.google.com/storage/docs/json_api/>`_.