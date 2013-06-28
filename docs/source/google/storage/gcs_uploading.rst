========================
Uploading Objects in GCS
========================

Overview
********

Uploading Objects to Google Cloud Storage is a non-trivial task. This page will describe
a simple method as a starting point for uploading data to Google Cloud Storage.

In particular, the examples for the following three methods will be provided:

- Simple Uploading
- Multipart Uploading
- Resumable Uploading

For more information on these methods, please visit the `official documentation
<https://developers.google.com/storage/docs/json_api/v1/how-tos/upload>`_.

Basic Example Class
-------------------

Create a base class for performing uploads::

  class UploadExample(object):
      def __init__(self, session):
          self.session = session
          #Get the Google Cloud Storage service
          self.svc = self.session.get_service('gcs')

Simple Upload
-------------

Define a class capable of handling `simple
<https://developers.google.com/storage/docs/json_api/v1/how-tos/upload#simple>`_
uploading::

  class Simple(UploadExample):
    def __init__(self, session):
        super(Simple, self).__init__(session)

    def download(self, bucket, name, retrieve_metadata=False):
        operation = self.svc.get_operation('storage.objects.get')
        endpoint = self.svc.get_endpoint()
        resp = data = None
        if retrieve_metadata:
            resp, data = operation.call(
                endpoint,
                bucket=bucket,
                object=name
            )
            return resp, data
        else:
            #Adding alt='media' returns object data, not metadata
            resp, data = operation.call(
                endpoint,
                bucket=bucket,
                object=name,
                alt='media'
            )
            #Must grab the content
            return resp, data._content
    
Multipart Upload
----------------

Define a template and class capable of handling `multipart
<https://developers.google.com/storage/docs/json_api/v1/how-tos/upload#multipart>`_ uploading::

  MULITPART_TEMPLATE = \
  """--{2}
  Content-Type: application/json; charset=UTF-8
  
  {0}
  
  --{2}
  Content-Type: {3}
  
  {1}
  --{2}--"""

  class Multipart(Simple):
    def __init__(self, session):
        super(Multipart, self).__init__(session)

    def upload(self, bucket, name, metadata, content, content_type='text/plain'):
        operation = self.svc.get_operation('storage.objects.insert')
        endpoint = self.svc.get_endpoint()
        if type(content) == file:
            content = content.read()

        #Stringify the metadata
        metadata = repr(metadata)

        #Set the upload type to be multipart
        upload_type = 'multipart'
        boundary = 'my_boundary'
        
        #Set the content-type header
        true_content_type = 'multipart/related; boundary="%s"' % boundary

        #Construct the payload using the multipart template
        body_content = bytearray(MULITPART_TEMPLATE.format(
            metadata,
            content,
            boundary,
            content_type
        ))

        #Make the request
        resp, data = operation.call(
            endpoint,
            upload_type=upload_type,
            bucket=bucket,
            name=name,
            content_type=true_content_type,
            content_length=len(body_content),
            body=body_content
        )
        return resp, data
        
Resumable Upload
----------------

*Note*: This only a demo solution, and should only serve as a starting point to more efficient implementations.

Define a class capable of handling `resumable
<https://developers.google.com/storage/docs/json_api/v1/how-tos/upload#resumable>`_ uploading::

  class Resumable(Simple):
    def __init__(self, session):
        super(Resumable, self).__init__(session)

    def upload(self, bucket, name, metadata, content, content_type='text/plain'):
               
        #Operation for initial request and metadata upload
        operation = self.svc.get_operation('storage.objects.insert')
        
        #Operation for transferring object data
        resume = self.svc.get_operation('storage.objects.insert.resume')
        endpoint = self.svc.get_endpoint()

        #stringify the metadata
        metadata = repr(metadata)

        if type(content) == file:
            content = content.read()

        content = bytearray(content)

        msg_length = len(content)

        if metadata:
            resp, _ = operation.call(
                endpoint,
                bucket=bucket,
                upload_type='resumable',
                name=name,
                content_type='application/json; charset=UTF-8',
                content_length=len(metadata),
                x_upload_content_type=content_type,
                x_upload_content_length=msg_length,
                body=metadata
            )
        else:
            resp, _ = operation.call(
                endpoint,
                bucket=bucket,
                upload_type='resumable',
                name=name,
                content_type='application/json; charset=UTF-8',
                content_length=0,
                x_upload_content_type=content_type,
                x_upload_content_length=msg_length
            )

        #Grab the upload_id from the location
        loc = resp.headers['location']
        upload_id = parse_qs(urlsplit(loc).query)['upload_id'][0]

        #Keep track of number of send attempts
        attempts = 0

        #Keep track of the number of bytes sent
        start = 0
        end = msg_length
        resp = data = None
        while True:
            if start == 0:
                #Make initial request, trying to send all data
                resp, data = resume.call(
                    endpoint,
                    bucket=bucket,
                    upload_type='resumable',
                    upload_id=upload_id,
                    name=name,
                    content_length=end - start,
                    content_type=content_type,
                    body=content
                )
            else:
                #Partial data has been uploaded. Upload the remaining
                resp, data = resume.call(
                    endpoint,
                    bucket=bucket,
                    upload_type='resumable',
                    upload_id=upload_id,
                    name=name,
                    content_length=end - start,
                    content_range='%s-%s/%s' % (start,
                                                msg_length - 1,
                                                msg_length),
                    body=content[start:]
                )
            if resp.status_code in [200, 201]:
                #Success!
                break
            elif resp.status_code == 400:
                #Bad request
                break
            elif resp.status_code == 404:
                #One should manually attempt again
                break
            else:
                if resp.status_code in range(500, 505):
                    #Request upload status
                    resp, data = resume.call(
                        endpoint,
                        bucket=bucket,
                        upload_type='resumable',
                        upload_id=upload_id,
                        content_range='*/%s' % msg_length,
                    )
                    #Check the upload status
                    if resp.status_code == 308:
                        start = int(resp.headers['Range'].split('-')[1]) + 1
                        #Reset exponential backoff, received a range response
                        attempts = 0
                    #It's possible that it completed uploading, but client
                    #didn't receive response from the server
                    elif resp.status_code in [200, 201]:
                        #Success!
                        break
                #Exponential backoff
                time.sleep(2 ** attempts + random.random())
                attempts = attempts + 1
                if attempts == 4:
                    break
        return resp, data
        
        
Performing Uploads and Downloads
--------------------------------

The following code illustrates how one could upload and download data using
the classes defined above::

  def run_demo():

    MY_BUCKET = 'your_bucket_name'

    #Create some data to send
    data = "This is a demo message"

    metadata = {
        'metadata':{
            'key':'value',
            'key2':'v2'
        }
    }

    simple_data_name = 'simpledata'
    multi_data_name = 'multidata'
    resumable_data_name = 'resumedata'


    #Get a global session
    session = botocore.session.get_session()

    #Upload and download an object via the simple method
    simple = Simple(session)
    simple.upload(bucket, simple_data_name, data)
    _ , downloaded_data = simple.download(MY_BUCKET, simple_data_name)

    assert downloaded_data == data

    #Upload using the multipart method
    multi = Multipart(session)
    multi.upload(bucket, multi_data_name, metadata, data)

    #Download the object data
    _ , downloaded_data = multi.download(MY_BUCKET, multi_data_name)
    assert data == downloaded_data

    #Download the metadata
    _, downloaded_metadata = multi.download(bucket, multi_data_name, True)
    assert metadata['metadata'] == downloaded_metadata['metadata']

    #Upload using the resumable method
    resume = Resumable(session)
    resume.upload(bucket, resumable_data_name, metadata, data)

    #Download the object data
    _ , downloaded_data = resume.download(MY_BUCKET, resumable_data_name)
    assert data == downloaded_data

    #Download the metadata
    _ , downloaded_metadata = resume.download(bucket, resumable_data_name, True)
    assert metadata['metadata'] == downloaded_metadata['metadata']

    #SUCCESS
