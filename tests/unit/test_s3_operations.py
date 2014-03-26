#!/usr/bin/env python
# Copyright (c) 2012-2013 Mitch Garnaat http://garnaat.org/
# Copyright 2012-2014 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

import os
from tests import BaseSessionTest
import botocore.session

XMLBODY1 = ('<CreateBucketConfiguration><LocationConstraint>sa-east-1'
            '</LocationConstraint></CreateBucketConfiguration>')
XMLBODY2 = ('<LifecycleConfiguration><Rule><ID>archive-objects-glacier-'
            'immediately-upon-creation</ID><Prefix>glacierobjects/</Prefix>'
            '<Status>Enabled</Status><Transition><Days>0</Days>'
            '<StorageClass>GLACIER</StorageClass></Transition></Rule>'
            '</LifecycleConfiguration>')
XMLBODY3 = ('<Tagging><TagSet><Tag><Key>key1</Key><Value>value1</Value></Tag>'
            '<Tag><Key>key2</Key><Value>value2</Value></Tag></TagSet></Tagging>')
XMLBODY4 = ('<CORSConfiguration><CORSRule><AllowedHeader>*</AllowedHeader>'
            '<AllowedMethod>PUT</AllowedMethod><AllowedMethod>POST</AllowedMethod>'
            '<AllowedMethod>DELETE</AllowedMethod>'
            '<AllowedOrigin>http://www.example1.com</AllowedOrigin>'
            '<ExposeHeader>x-amz-server-side-encryption</ExposeHeader>'
            '<MaxAgeSeconds>3000</MaxAgeSeconds></CORSRule><CORSRule>'
            '<AllowedMethod>GET</AllowedMethod><AllowedOrigin>*</AllowedOrigin>'
            '</CORSRule></CORSConfiguration>')
XMLBODY5 = ('<BucketLoggingStatus><LoggingEnabled><TargetBucket>mybucketlogs'
            '</TargetBucket><TargetGrants><Grant><Grantee '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
            'xsi:type="AmazonCustomerByEmail"><EmailAddress>user@company.com'
            '</EmailAddress></Grantee><Permission>READ</Permission></Grant>'
            '</TargetGrants><TargetPrefix>mybucket-access_log-/</TargetPrefix>'
            '</LoggingEnabled></BucketLoggingStatus>')
XMLBODY6 = ('<VersioningConfiguration>'
            '<Status>Enabled</Status>'
            '<MfaDelete>Enabled</MfaDelete>'
            '</VersioningConfiguration>')
XMLBODY7 = ('<Delete><Object><Key>foobar</Key>'
           '</Object><Object><Key>fiebaz</Key></Object>'
            '</Delete>')
XMLBODY8 = ('<WebsiteConfiguration>'
            '<ErrorDocument><Key>SomeErrorDocument.html</Key></ErrorDocument>'
            '<IndexDocument><Suffix>index.html</Suffix></IndexDocument>'
            '</WebsiteConfiguration>')
XMLBODY9 = ('<LifecycleConfiguration><Rule><ID>archive-objects-glacier-'
            'immediately-upon-creation</ID><Prefix></Prefix>'
            '<Status>Enabled</Status><Transition><Days>0</Days>'
            '<StorageClass>GLACIER</StorageClass></Transition></Rule>'
            '</LifecycleConfiguration>')

POLICY = ('{"Version": "2008-10-17","Statement": [{"Sid": "AddPerm",'
          '"Effect": "Allow","Principal": {"AWS": "*"},'
          '"Action": "s3:GetObject", "Resource": "arn:aws:s3:::BUCKET_NAME/*"'
          '}]}')


class TestS3Operations(BaseSessionTest):

    maxDiff = None

    def setUp(self):
        super(TestS3Operations, self).setUp()
        self.s3 = self.session.get_service('s3')
        self.endpoint = self.s3.get_endpoint('us-east-1')
        self.bucket_name = 'foo'
        self.key_name = 'bar'

    def test_create_bucket_location(self):
        op = self.s3.get_operation('CreateBucket')
        config = {'LocationConstraint': 'sa-east-1'}
        params = op.build_parameters(bucket=self.bucket_name,
                                     acl='public-read',
                                     create_bucket_configuration=config)
        headers = {'x-amz-acl': 'public-read'}
        uri_params = {'Bucket': self.bucket_name}
        self.assertEqual(params['headers'], headers)
        self.assertEqual(params['uri_params'], uri_params)
        self.assertEqual(params['payload'].getvalue(), XMLBODY1)

    def test_create_bucket_lifecycle(self):
        op = self.s3.get_operation('PutBucketLifecycle')
        config = {'Rules': [
                      {'ID': 'archive-objects-glacier-immediately-upon-creation',
                       'Prefix': 'glacierobjects/',
                       'Status': 'Enabled',
                       'Transition': {'Days': 0,
                                      'StorageClass': 'GLACIER'}
                       }
                    ]
                  }
        params = op.build_parameters(bucket=self.bucket_name,
                                     lifecycle_configuration=config)
        # There is a handler for the before-call event that will
        # add the Content-MD5 header to the parameters if it is not
        # already there.  We are going to fire the event here to
        # simulate that and make sure the right header is added.
        self.session.emit('before-call.s3.PutBucketLifecycle', params=params)
        uri_params = {'Bucket': self.bucket_name}
        headers = {'Content-MD5': '5bNG1b31rFf4z+aleBKqWw=='}
        self.assertEqual(params['uri_params'], uri_params)
        self.assertEqual(params['payload'].getvalue(), XMLBODY2)
        self.assertEqual(params['headers'], headers)

    def test_create_entire_bucket_lifecycle(self):
        op = self.s3.get_operation('PutBucketLifecycle')
        config = {'Rules': [
                      {'ID': 'archive-objects-glacier-immediately-upon-creation',
                       'Prefix': None,
                       'Status': 'Enabled',
                       'Transition': {'Days': 0,
                                      'StorageClass': 'GLACIER'}
                       }
                    ]
                  }
        params = op.build_parameters(bucket=self.bucket_name,
                                     lifecycle_configuration=config)
        # There is a handler for the before-call event that will
        # add the Content-MD5 header to the parameters if it is not
        # already there.  We are going to fire the event here to
        # simulate that and make sure the right header is added.
        self.session.emit('before-call.s3.PutBucketLifecycle', params=params)
        uri_params = {'Bucket': self.bucket_name}
        headers = {'Content-MD5': 'RLlxIC2KsifRLSfsrCKkVg=='}
        self.assertEqual(params['uri_params'], uri_params)
        self.assertEqual(params['payload'].getvalue(), XMLBODY9)
        self.assertEqual(params['headers'], headers)

    def test_put_bucket_tagging(self):
        op = self.s3.get_operation('PutBucketTagging')
        tag_set = {'TagSet': [
                    {
                      'Key': 'key1',
                      'Value': 'value1'},
                    {
                      'Key': 'key2',
                      'Value': 'value2'}]}
        params = op.build_parameters(bucket=self.bucket_name,
                                     tagging=tag_set)
        # There is a handler for the before-call event that will
        # add the Content-MD5 header to the parameters if it is not
        # already there.  We are going to fire the event here to
        # simulate that and make sure the right header is added.
        self.session.emit('before-call.s3.PutBucketTagging', params=params)
        uri_params = {'Bucket': self.bucket_name}
        headers = {'Content-MD5': '5s++BGwLE2moBAK9duxpFw=='}
        self.assertEqual(params['uri_params'], uri_params)
        self.assertEqual(params['payload'].getvalue(), XMLBODY3)
        self.assertEqual(params['headers'], headers)

    def test_put_bucket_cors(self):
        op = self.s3.get_operation('PutBucketCors')
        cors = {"CORSRules": [
                {
                    "AllowedHeaders": ["*"],
                    "AllowedMethods": ["PUT", "POST", "DELETE"],
                    "AllowedOrigins": ["http://www.example1.com"],
                    "MaxAgeSeconds": 3000,
                    "ExposeHeaders": ["x-amz-server-side-encryption"]
                    },
                {
                    "AllowedMethods": ["GET"],
                    "AllowedOrigins": ["*"]
                    }
                ]
                }
        params = op.build_parameters(bucket=self.bucket_name,
                                     cors_configuration=cors)
        # There is a handler for the before-call event that will
        # add the Content-MD5 header to the parameters if it is not
        # already there.  We are going to fire the event here to
        # simulate that and make sure the right header is added.
        self.session.emit('before-call.s3.PutBucketCors', params=params)
        uri_params = {'Bucket': self.bucket_name}
        headers = {'Content-MD5': 'uj9D08gqRQUY0al4Po043w=='}
        self.assertEqual(params['uri_params'], uri_params)
        self.assertEqual(params['payload'].getvalue(), XMLBODY4)
        self.assertEqual(params['headers'], headers)

    def test_put_bucket_website(self):
        op = self.s3.get_operation('PutBucketWebsite')
        website = {"IndexDocument": {'Suffix': 'index.html'},
                   "ErrorDocument": {'Key': 'SomeErrorDocument.html'}}
        params = op.build_parameters(bucket=self.bucket_name,
                                     website_configuration=website)
        uri_params = {'Bucket': self.bucket_name}
        self.assertEqual(params['uri_params'], uri_params)
        self.assertEqual(params['payload'].getvalue(), XMLBODY8)

    def test_delete_objects(self):
        op = self.s3.get_operation('DeleteObjects')
        delete = {"Objects": [
                {
                    "Key": "foobar"
                    },
                {
                    "Key": "fiebaz"
                    }
                ]
                  }
        params = op.build_parameters(bucket=self.bucket_name,
                                     delete=delete)
        # There is a handler for the before-call event that will
        # add the Content-MD5 header to the parameters if it is not
        # already there.  We are going to fire the event here to
        # simulate that and make sure the right header is added.
        self.session.emit('before-call.s3.DeleteObjects', params=params)
        uri_params = {'Bucket': self.bucket_name}
        headers = {'Content-MD5': '1qryost37c7QBmno21C08w=='}
        self.assertEqual(params['uri_params'], uri_params)
        self.assertEqual(params['payload'].getvalue(), XMLBODY7)
        self.assertEqual(params['headers'], headers)

    def test_put_bucket_policy(self):
        op = self.s3.get_operation('PutBucketPolicy')
        params = op.build_parameters(bucket=self.bucket_name,
                                     policy=POLICY)
        uri_params = {'Bucket': self.bucket_name}
        self.assertEqual(params['uri_params'], uri_params)
        self.assertEqual(params['payload'].getvalue(), POLICY)
        self.assertEqual(params['headers'], {})

    def test_put_bucket_logging(self):
        op = self.s3.get_operation('PutBucketLogging')
        logging = {'LoggingEnabled':
                       {'TargetBucket': 'mybucketlogs',
                        'TargetPrefix': 'mybucket-access_log-/',
                        'TargetGrants':
                            [{'Grantee':
                                  {'Type': 'AmazonCustomerByEmail',
                                   'EmailAddress': 'user@company.com'},
                              'Permission': 'READ'}]}}
        params = op.build_parameters(bucket=self.bucket_name,
                                     bucket_logging_status=logging)
        uri_params = {'Bucket': self.bucket_name}
        self.assertEqual(params['uri_params'], uri_params)
        self.assertEqual(params['payload'].getvalue(), XMLBODY5)
        self.assertEqual(params['headers'], {})

    def test_put_bucket_versioning_mfa(self):
        op = self.s3.get_operation('PutBucketVersioning')
        mfa = {'MfaDelete': 'Enabled',
               'Status': 'Enabled'}
        params = op.build_parameters(bucket=self.bucket_name,
                                     versioning_configuration=mfa,
                                     mfa="GAK000000000 123456")
        uri_params = {'Bucket': self.bucket_name}
        self.assertEqual(params['uri_params'], uri_params)
        self.assertEqual(params['payload'].getvalue(), XMLBODY6)
        self.assertEqual(params['headers'], {'x-amz-mfa': 'GAK000000000 123456'})

    def test_put_object(self):
        op = self.s3.get_operation('PutObject')
        file_path = os.path.join(os.path.dirname(__file__),
                                 'put_object_data')
        fp = open(file_path, 'rb')
        params = op.build_parameters(bucket=self.bucket_name,
                                     key=self.key_name,
                                     body=fp,
                                     acl='public-read',
                                     content_language='piglatin',
                                     content_type='text/plain')
        headers = {'x-amz-acl': 'public-read',
                   'Content-Language': 'piglatin',
                   'Content-Type': 'text/plain'}
        uri_params = {'Bucket': 'foo', 'Key': 'bar'}
        self.assertEqual(params['headers'], headers)
        self.assertEqual(params['uri_params'], uri_params)
        self.assertEqual(params['payload'].getvalue(), fp)

    def test_complete_multipart_upload(self):
        op = self.s3.get_operation('CompleteMultipartUpload')
        parts = {
            'Parts': [
                {'ETag': '123', 'PartNumber': 1},
                {'ETag': '124', 'PartNumber': 2},
            ]
        }
        params = op.build_parameters(bucket=self.bucket_name,
                                     key=self.key_name,
                                     upload_id='upload_id',
                                     multipart_upload=parts)
        xml_payload = params['payload'].getvalue()
        # We should not see the <Parts><Part><...></Part></Parts>
        # element in the xml_payload.
        # Directly to Part, skipping Parts.
        self.assertIn('<CompleteMultipartUpload><Part>', xml_payload)
        self.assertIn('</Part></CompleteMultipartUpload>', xml_payload)
        # Explicitly check that <Parts> is not in the payload anywhere.
        self.assertNotIn('<Parts>', xml_payload)
        self.assertNotIn('</Parts>', xml_payload)
