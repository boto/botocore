============
GCE Examples
============

For parameters, please refer to the `latest docs
<https://developers.google.com/compute/docs/reference/latest/>`_.

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

Creating an instance::

  import botocore.session
  
  API_VERSION = 'v1beta15'
  GCE_URL = 'https://www.googleapis.com/compute/%s/projects/' % (API_VERSION)
  DEFAULT_ZONE = 'us-central1-a'
  
  # New instance properties
  DEFAULT_MACHINE_TYPE = 'n1-standard-1'
  DEFAULT_IMAGE = 'debian'
  DEFAULT_IMAGES = {
      'debian': 'debian-7-wheezy-v20130507',
      'centos': 'centos-6-v20130104'
  }
  DEFAULT_NETWORK = 'default'
  DEFAULT_SERVICE_EMAIL = 'default'
  DEFAULT_SCOPES = ['https://www.googleapis.com/auth/devstorage.full_control',
                    'https://www.googleapis.com/auth/compute']

  #Name of your project
  PROJECT = 'your project name'
  
  session = botocore.session.get_session()
  gce = session.get_service('gce') 
  endpoint = gce.get_endpoint()
  create_instance = gce.get_operation('compute.instances.insert')
  
  instance_name = 'my_instance'

  project_url       = '%s%s' % (GCE_URL, PROJECT)
  image_url         = '%s%s/global/images/%s' % (GCE_URL, 'debian-cloud', DEFAULT_IMAGES['debian'])
  machine_type_url  = '%s/zones/%s/machineTypes/%s' % (project_url, DEFAULT_ZONE, DEFAULT_MACHINE_TYPE)
  network_url       = '%s/global/networks/%s' % (project_url, DEFAULT_NETWORK)

  #Set up the instance resource
  instance = {
  'name': instance_name,
  'machineType': machine_type_url,
  'image': image_url,
  'networkInterfaces': [{
    'accessConfigs': [{
      'type': 'ONE_TO_ONE_NAT',
      'name': 'External NAT'
     }],
    'network': network_url
  }],
  'serviceAccounts': [{
       'email': DEFAULT_SERVICE_EMAIL,
       'scopes': DEFAULT_SCOPES
  }]
  }
  
  resp, data = create_instance.call(
      endpoint,
      project=PROJECT,
      zone=DEFAULT_ZONE,
      body=instance
  )

Deleting an instance::
  
  PROJECT = 'your project name'
  DEFAULT_ZONE = 'us-central1-a'

  session = botocore.session.get_session()
  gce = session.get_service('gce') 
  endpoint = gce.get_endpoint()
  op = self.svc.get_operation('compute.instances.delete')
  
  instance_name = 'my_instance'
  
  resp, data = op.call(
      endpoint,
      project=PROJECT,
      zone=DEFAULT_ZONE,
      instance=instance_name
  )

Creating a disk::
  
  PROJECT = 'your project name'
  DEFAULT_ZONE = 'us-central1-a'
  
  import botocore.session
  
  session = botocore.session.get_session()
  gce = session.get_service('gce') 
  endpoint = gce.get_endpoint()
  operation = svc.get_operation('compute.disks.insert')
  
  disk_resource = {
    'name': 'my_new_disk',
    'description': 'My cool new disk!',
    'sizeGb': '1'
  }
  
  response, data = op.call(
    endpoint,
    project=PROJECT,
    zone=DEFAULT_ZONE,
    body=disk_resource
  )
  
Deleting a disk::

  PROJECT = 'your project name'
  DEFAULT_ZONE = 'us-central1-a'
  
  import botocore.session
  
  session = botocore.session.get_session()
  gce = session.get_service('gce') 
  endpoint = gce.get_endpoint()
  operation = svc.get_operation('compute.disks.delete')

  response, data = op.call(
    endpoint,
    project=PROJECT,
    zone=DEFAULT_ZONE,
    disk='my_new_disk'
  )