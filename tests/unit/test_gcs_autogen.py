#!/usr/bin/env python
# Copyright 2013 Google, Inc. or its affiliates. All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, dis-
# tribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the fol-
# lowing conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#

import botocore.session
import botocore.exceptions
import unittest



class TestBucketaccesscontrols(unittest.TestCase):

    def setUp(self):
        self.session = botocore.session.get_session()
        self.gcs = self.session.get_service('gcs')

    def test_bucketAccessControls_delete(self):
        op = self.gcs.get_operation('storage.bucketAccessControls.delete')
        params = op.build_parameters(bucket='bucket',
		entity='entity')
        self.assertTrue('bucket' in params['uri_params'])
        self.assertTrue('entity' in params['uri_params'])

    def test_bucketAccessControls_delete_missing_params(self):
        op = self.gcs.get_operation('storage.bucketAccessControls.delete')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			bucket='bucket'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			entity='entity'
        )

    def test_bucketAccessControls_get(self):
        op = self.gcs.get_operation('storage.bucketAccessControls.get')
        params = op.build_parameters(bucket='bucket',
		entity='entity')
        self.assertTrue('bucket' in params['uri_params'])
        self.assertTrue('entity' in params['uri_params'])

    def test_bucketAccessControls_get_missing_params(self):
        op = self.gcs.get_operation('storage.bucketAccessControls.get')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			bucket='bucket'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			entity='entity'
        )

    def test_bucketAccessControls_insert(self):
        op = self.gcs.get_operation('storage.bucketAccessControls.insert')
        params = op.build_parameters(body='body',
		bucket='bucket')
        self.assertTrue(params['payload'])
        self.assertTrue('bucket' in params['uri_params'])

    def test_bucketAccessControls_insert_missing_params(self):
        op = self.gcs.get_operation('storage.bucketAccessControls.insert')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			bucket='bucket'
        )

    def test_bucketAccessControls_list(self):
        op = self.gcs.get_operation('storage.bucketAccessControls.list')
        params = op.build_parameters(bucket='bucket')
        self.assertTrue('bucket' in params['uri_params'])

    def test_bucketAccessControls_list_missing_params(self):
        op = self.gcs.get_operation('storage.bucketAccessControls.list')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )

    def test_bucketAccessControls_patch(self):
        op = self.gcs.get_operation('storage.bucketAccessControls.patch')
        params = op.build_parameters(body='body',
		bucket='bucket',
		entity='entity')
        self.assertTrue(params['payload'])
        self.assertTrue('bucket' in params['uri_params'])
        self.assertTrue('entity' in params['uri_params'])

    def test_bucketAccessControls_patch_missing_params(self):
        op = self.gcs.get_operation('storage.bucketAccessControls.patch')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			bucket='bucket'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			entity='entity'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			bucket='bucket'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			entity='entity'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			bucket='bucket',
			entity='entity'
        )

    def test_bucketAccessControls_update(self):
        op = self.gcs.get_operation('storage.bucketAccessControls.update')
        params = op.build_parameters(body='body',
		bucket='bucket',
		entity='entity')
        self.assertTrue(params['payload'])
        self.assertTrue('bucket' in params['uri_params'])
        self.assertTrue('entity' in params['uri_params'])

    def test_bucketAccessControls_update_missing_params(self):
        op = self.gcs.get_operation('storage.bucketAccessControls.update')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			bucket='bucket'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			entity='entity'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			bucket='bucket'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			entity='entity'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			bucket='bucket',
			entity='entity'
        )

class TestBuckets(unittest.TestCase):

    def setUp(self):
        self.session = botocore.session.get_session()
        self.gcs = self.session.get_service('gcs')

    def test_buckets_delete(self):
        op = self.gcs.get_operation('storage.buckets.delete')
        params = op.build_parameters(bucket='bucket')
        self.assertTrue('bucket' in params['uri_params'])

    def test_buckets_delete_missing_params(self):
        op = self.gcs.get_operation('storage.buckets.delete')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )

    def test_buckets_get(self):
        op = self.gcs.get_operation('storage.buckets.get')
        params = op.build_parameters(bucket='bucket')
        self.assertTrue('bucket' in params['uri_params'])

    def test_buckets_get_missing_params(self):
        op = self.gcs.get_operation('storage.buckets.get')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )

    def test_buckets_insert(self):
        op = self.gcs.get_operation('storage.buckets.insert')
        params = op.build_parameters(body='body',
		project='project')
        self.assertTrue(params['payload'])
        self.assertTrue('project' in params['uri_params'])

    def test_buckets_insert_missing_params(self):
        op = self.gcs.get_operation('storage.buckets.insert')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project'
        )

    def test_buckets_list(self):
        op = self.gcs.get_operation('storage.buckets.list')
        params = op.build_parameters(project='project')
        self.assertTrue('project' in params['uri_params'])

    def test_buckets_list_missing_params(self):
        op = self.gcs.get_operation('storage.buckets.list')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )

    def test_buckets_patch(self):
        op = self.gcs.get_operation('storage.buckets.patch')
        params = op.build_parameters(body='body',
		bucket='bucket')
        self.assertTrue(params['payload'])
        self.assertTrue('bucket' in params['uri_params'])

    def test_buckets_patch_missing_params(self):
        op = self.gcs.get_operation('storage.buckets.patch')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			bucket='bucket'
        )

    def test_buckets_update(self):
        op = self.gcs.get_operation('storage.buckets.update')
        params = op.build_parameters(body='body',
		bucket='bucket')
        self.assertTrue(params['payload'])
        self.assertTrue('bucket' in params['uri_params'])

    def test_buckets_update_missing_params(self):
        op = self.gcs.get_operation('storage.buckets.update')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			bucket='bucket'
        )

class TestChannels(unittest.TestCase):

    def setUp(self):
        self.session = botocore.session.get_session()
        self.gcs = self.session.get_service('gcs')

    def test_channels_stop(self):
        op = self.gcs.get_operation('storage.channels.stop')
        params = op.build_parameters(body='body')
        self.assertTrue(params['payload'])

    def test_channels_stop_missing_params(self):
        op = self.gcs.get_operation('storage.channels.stop')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )

class TestDefaultobjectaccesscontrols(unittest.TestCase):

    def setUp(self):
        self.session = botocore.session.get_session()
        self.gcs = self.session.get_service('gcs')

    def test_defaultObjectAccessControls_delete(self):
        op = self.gcs.get_operation('storage.defaultObjectAccessControls.delete')
        params = op.build_parameters(bucket='bucket',
		entity='entity')
        self.assertTrue('bucket' in params['uri_params'])
        self.assertTrue('entity' in params['uri_params'])

    def test_defaultObjectAccessControls_delete_missing_params(self):
        op = self.gcs.get_operation('storage.defaultObjectAccessControls.delete')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			bucket='bucket'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			entity='entity'
        )

    def test_defaultObjectAccessControls_get(self):
        op = self.gcs.get_operation('storage.defaultObjectAccessControls.get')
        params = op.build_parameters(bucket='bucket',
		entity='entity')
        self.assertTrue('bucket' in params['uri_params'])
        self.assertTrue('entity' in params['uri_params'])

    def test_defaultObjectAccessControls_get_missing_params(self):
        op = self.gcs.get_operation('storage.defaultObjectAccessControls.get')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			bucket='bucket'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			entity='entity'
        )

    def test_defaultObjectAccessControls_insert(self):
        op = self.gcs.get_operation('storage.defaultObjectAccessControls.insert')
        params = op.build_parameters(body='body',
		bucket='bucket')
        self.assertTrue(params['payload'])
        self.assertTrue('bucket' in params['uri_params'])

    def test_defaultObjectAccessControls_insert_missing_params(self):
        op = self.gcs.get_operation('storage.defaultObjectAccessControls.insert')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			bucket='bucket'
        )

    def test_defaultObjectAccessControls_list(self):
        op = self.gcs.get_operation('storage.defaultObjectAccessControls.list')
        params = op.build_parameters(bucket='bucket')
        self.assertTrue('bucket' in params['uri_params'])

    def test_defaultObjectAccessControls_list_missing_params(self):
        op = self.gcs.get_operation('storage.defaultObjectAccessControls.list')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )

    def test_defaultObjectAccessControls_patch(self):
        op = self.gcs.get_operation('storage.defaultObjectAccessControls.patch')
        params = op.build_parameters(body='body',
		bucket='bucket',
		entity='entity')
        self.assertTrue(params['payload'])
        self.assertTrue('bucket' in params['uri_params'])
        self.assertTrue('entity' in params['uri_params'])

    def test_defaultObjectAccessControls_patch_missing_params(self):
        op = self.gcs.get_operation('storage.defaultObjectAccessControls.patch')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			bucket='bucket'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			entity='entity'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			bucket='bucket'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			entity='entity'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			bucket='bucket',
			entity='entity'
        )

    def test_defaultObjectAccessControls_update(self):
        op = self.gcs.get_operation('storage.defaultObjectAccessControls.update')
        params = op.build_parameters(body='body',
		bucket='bucket',
		entity='entity')
        self.assertTrue(params['payload'])
        self.assertTrue('bucket' in params['uri_params'])
        self.assertTrue('entity' in params['uri_params'])

    def test_defaultObjectAccessControls_update_missing_params(self):
        op = self.gcs.get_operation('storage.defaultObjectAccessControls.update')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			bucket='bucket'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			entity='entity'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			bucket='bucket'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			entity='entity'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			bucket='bucket',
			entity='entity'
        )

class TestObjectaccesscontrols(unittest.TestCase):

    def setUp(self):
        self.session = botocore.session.get_session()
        self.gcs = self.session.get_service('gcs')

    def test_objectAccessControls_delete(self):
        op = self.gcs.get_operation('storage.objectAccessControls.delete')
        params = op.build_parameters(object='object',
		bucket='bucket',
		entity='entity')
        self.assertTrue('object' in params['uri_params'])
        self.assertTrue('bucket' in params['uri_params'])
        self.assertTrue('entity' in params['uri_params'])

    def test_objectAccessControls_delete_missing_params(self):
        op = self.gcs.get_operation('storage.objectAccessControls.delete')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			object='object'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			bucket='bucket'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			entity='entity'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			object='object',
			bucket='bucket'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			object='object',
			entity='entity'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			bucket='bucket',
			entity='entity'
        )

    def test_objectAccessControls_get(self):
        op = self.gcs.get_operation('storage.objectAccessControls.get')
        params = op.build_parameters(object='object',
		bucket='bucket',
		entity='entity')
        self.assertTrue('object' in params['uri_params'])
        self.assertTrue('bucket' in params['uri_params'])
        self.assertTrue('entity' in params['uri_params'])

    def test_objectAccessControls_get_missing_params(self):
        op = self.gcs.get_operation('storage.objectAccessControls.get')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			object='object'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			bucket='bucket'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			entity='entity'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			object='object',
			bucket='bucket'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			object='object',
			entity='entity'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			bucket='bucket',
			entity='entity'
        )

    def test_objectAccessControls_insert(self):
        op = self.gcs.get_operation('storage.objectAccessControls.insert')
        params = op.build_parameters(body='body',
		object='object',
		bucket='bucket')
        self.assertTrue(params['payload'])
        self.assertTrue('object' in params['uri_params'])
        self.assertTrue('bucket' in params['uri_params'])

    def test_objectAccessControls_insert_missing_params(self):
        op = self.gcs.get_operation('storage.objectAccessControls.insert')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			object='object'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			bucket='bucket'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			object='object'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			bucket='bucket'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			object='object',
			bucket='bucket'
        )

    def test_objectAccessControls_list(self):
        op = self.gcs.get_operation('storage.objectAccessControls.list')
        params = op.build_parameters(object='object',
		bucket='bucket')
        self.assertTrue('object' in params['uri_params'])
        self.assertTrue('bucket' in params['uri_params'])

    def test_objectAccessControls_list_missing_params(self):
        op = self.gcs.get_operation('storage.objectAccessControls.list')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			object='object'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			bucket='bucket'
        )

    def test_objectAccessControls_patch(self):
        op = self.gcs.get_operation('storage.objectAccessControls.patch')
        params = op.build_parameters(body='body',
		object='object',
		bucket='bucket',
		entity='entity')
        self.assertTrue(params['payload'])
        self.assertTrue('object' in params['uri_params'])
        self.assertTrue('bucket' in params['uri_params'])
        self.assertTrue('entity' in params['uri_params'])

    def test_objectAccessControls_patch_missing_params(self):
        op = self.gcs.get_operation('storage.objectAccessControls.patch')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			object='object'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			bucket='bucket'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			entity='entity'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			object='object'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			bucket='bucket'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			entity='entity'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			object='object',
			bucket='bucket'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			object='object',
			entity='entity'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			bucket='bucket',
			entity='entity'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			object='object',
			bucket='bucket'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			object='object',
			entity='entity'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			bucket='bucket',
			entity='entity'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			object='object',
			bucket='bucket',
			entity='entity'
        )

    def test_objectAccessControls_update(self):
        op = self.gcs.get_operation('storage.objectAccessControls.update')
        params = op.build_parameters(body='body',
		object='object',
		bucket='bucket',
		entity='entity')
        self.assertTrue(params['payload'])
        self.assertTrue('object' in params['uri_params'])
        self.assertTrue('bucket' in params['uri_params'])
        self.assertTrue('entity' in params['uri_params'])

    def test_objectAccessControls_update_missing_params(self):
        op = self.gcs.get_operation('storage.objectAccessControls.update')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			object='object'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			bucket='bucket'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			entity='entity'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			object='object'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			bucket='bucket'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			entity='entity'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			object='object',
			bucket='bucket'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			object='object',
			entity='entity'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			bucket='bucket',
			entity='entity'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			object='object',
			bucket='bucket'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			object='object',
			entity='entity'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			bucket='bucket',
			entity='entity'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			object='object',
			bucket='bucket',
			entity='entity'
        )

class TestObjects(unittest.TestCase):

    def setUp(self):
        self.session = botocore.session.get_session()
        self.gcs = self.session.get_service('gcs')

    def test_objects_compose(self):
        op = self.gcs.get_operation('storage.objects.compose')
        params = op.build_parameters(body='body',
		destination_bucket='destination_bucket',
		destination_object='destination_object')
        self.assertTrue(params['payload'])
        self.assertTrue('destinationBucket' in params['uri_params'])
        self.assertTrue('destinationObject' in params['uri_params'])

    def test_objects_compose_missing_params(self):
        op = self.gcs.get_operation('storage.objects.compose')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			destination_bucket='destination_bucket'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			destination_object='destination_object'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			destination_bucket='destination_bucket'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			destination_object='destination_object'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			destination_bucket='destination_bucket',
			destination_object='destination_object'
        )

    def test_objects_copy(self):
        op = self.gcs.get_operation('storage.objects.copy')
        params = op.build_parameters(body='body',
		source_object='source_object',
		source_bucket='source_bucket',
		destination_bucket='destination_bucket',
		destination_object='destination_object')
        self.assertTrue(params['payload'])
        self.assertTrue('sourceObject' in params['uri_params'])
        self.assertTrue('sourceBucket' in params['uri_params'])
        self.assertTrue('destinationBucket' in params['uri_params'])
        self.assertTrue('destinationObject' in params['uri_params'])

    def test_objects_copy_missing_params(self):
        op = self.gcs.get_operation('storage.objects.copy')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			source_object='source_object'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			source_bucket='source_bucket'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			destination_bucket='destination_bucket'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			destination_object='destination_object'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			source_object='source_object'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			source_bucket='source_bucket'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			destination_bucket='destination_bucket'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			destination_object='destination_object'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			source_object='source_object',
			source_bucket='source_bucket'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			source_object='source_object',
			destination_bucket='destination_bucket'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			source_object='source_object',
			destination_object='destination_object'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			source_bucket='source_bucket',
			destination_bucket='destination_bucket'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			source_bucket='source_bucket',
			destination_object='destination_object'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			destination_bucket='destination_bucket',
			destination_object='destination_object'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			source_object='source_object',
			source_bucket='source_bucket'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			source_object='source_object',
			destination_bucket='destination_bucket'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			source_object='source_object',
			destination_object='destination_object'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			source_bucket='source_bucket',
			destination_bucket='destination_bucket'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			source_bucket='source_bucket',
			destination_object='destination_object'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			destination_bucket='destination_bucket',
			destination_object='destination_object'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			source_object='source_object',
			source_bucket='source_bucket',
			destination_bucket='destination_bucket'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			source_object='source_object',
			source_bucket='source_bucket',
			destination_object='destination_object'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			source_object='source_object',
			destination_bucket='destination_bucket',
			destination_object='destination_object'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			source_bucket='source_bucket',
			destination_bucket='destination_bucket',
			destination_object='destination_object'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			source_object='source_object',
			source_bucket='source_bucket',
			destination_bucket='destination_bucket'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			source_object='source_object',
			source_bucket='source_bucket',
			destination_object='destination_object'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			source_object='source_object',
			destination_bucket='destination_bucket',
			destination_object='destination_object'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			source_bucket='source_bucket',
			destination_bucket='destination_bucket',
			destination_object='destination_object'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			source_object='source_object',
			source_bucket='source_bucket',
			destination_bucket='destination_bucket',
			destination_object='destination_object'
        )

    def test_objects_delete(self):
        op = self.gcs.get_operation('storage.objects.delete')
        params = op.build_parameters(object='object',
		bucket='bucket')
        self.assertTrue('object' in params['uri_params'])
        self.assertTrue('bucket' in params['uri_params'])

    def test_objects_delete_missing_params(self):
        op = self.gcs.get_operation('storage.objects.delete')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			object='object'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			bucket='bucket'
        )

    def test_objects_get(self):
        op = self.gcs.get_operation('storage.objects.get')
        params = op.build_parameters(object='object',
		bucket='bucket')
        self.assertTrue('object' in params['uri_params'])
        self.assertTrue('bucket' in params['uri_params'])

    def test_objects_get_missing_params(self):
        op = self.gcs.get_operation('storage.objects.get')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			object='object'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			bucket='bucket'
        )

    def test_objects_insert(self):
        op = self.gcs.get_operation('storage.objects.insert')
        params = op.build_parameters(upload_type='upload_type',
		bucket='bucket')
        self.assertTrue('uploadType' in params['uri_params'])
        self.assertTrue('bucket' in params['uri_params'])

    def test_objects_insert_missing_params(self):
        op = self.gcs.get_operation('storage.objects.insert')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			upload_type='upload_type'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			bucket='bucket'
        )

    def test_objects_insert_resume(self):
        op = self.gcs.get_operation('storage.objects.insert.resume')
        params = op.build_parameters(name='name',
		upload_type='upload_type',
		content_length='content_length',
		bucket='bucket',
		upload_id='upload_id')
        self.assertTrue('name' in params['uri_params'])
        self.assertTrue('uploadType' in params['uri_params'])
        self.assertTrue('bucket' in params['uri_params'])
        self.assertTrue('upload_id' in params['uri_params'])

    def test_objects_insert_resume_missing_params(self):
        op = self.gcs.get_operation('storage.objects.insert.resume')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			name='name'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			upload_type='upload_type'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			content_length='content_length'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			bucket='bucket'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			upload_id='upload_id'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			name='name',
			upload_type='upload_type'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			name='name',
			content_length='content_length'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			name='name',
			bucket='bucket'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			name='name',
			upload_id='upload_id'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			upload_type='upload_type',
			content_length='content_length'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			upload_type='upload_type',
			bucket='bucket'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			upload_type='upload_type',
			upload_id='upload_id'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			content_length='content_length',
			bucket='bucket'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			content_length='content_length',
			upload_id='upload_id'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			bucket='bucket',
			upload_id='upload_id'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			name='name',
			upload_type='upload_type',
			content_length='content_length'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			name='name',
			upload_type='upload_type',
			bucket='bucket'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			name='name',
			upload_type='upload_type',
			upload_id='upload_id'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			name='name',
			content_length='content_length',
			bucket='bucket'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			name='name',
			content_length='content_length',
			upload_id='upload_id'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			name='name',
			bucket='bucket',
			upload_id='upload_id'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			upload_type='upload_type',
			content_length='content_length',
			bucket='bucket'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			upload_type='upload_type',
			content_length='content_length',
			upload_id='upload_id'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			upload_type='upload_type',
			bucket='bucket',
			upload_id='upload_id'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			content_length='content_length',
			bucket='bucket',
			upload_id='upload_id'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			name='name',
			upload_type='upload_type',
			content_length='content_length',
			bucket='bucket'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			name='name',
			upload_type='upload_type',
			content_length='content_length',
			upload_id='upload_id'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			name='name',
			upload_type='upload_type',
			bucket='bucket',
			upload_id='upload_id'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			name='name',
			content_length='content_length',
			bucket='bucket',
			upload_id='upload_id'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			upload_type='upload_type',
			content_length='content_length',
			bucket='bucket',
			upload_id='upload_id'
        )

    def test_objects_list(self):
        op = self.gcs.get_operation('storage.objects.list')
        params = op.build_parameters(bucket='bucket')
        self.assertTrue('bucket' in params['uri_params'])

    def test_objects_list_missing_params(self):
        op = self.gcs.get_operation('storage.objects.list')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )

    def test_objects_patch(self):
        op = self.gcs.get_operation('storage.objects.patch')
        params = op.build_parameters(body='body',
		object='object',
		bucket='bucket')
        self.assertTrue(params['payload'])
        self.assertTrue('object' in params['uri_params'])
        self.assertTrue('bucket' in params['uri_params'])

    def test_objects_patch_missing_params(self):
        op = self.gcs.get_operation('storage.objects.patch')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			object='object'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			bucket='bucket'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			object='object'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			bucket='bucket'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			object='object',
			bucket='bucket'
        )

    def test_objects_update(self):
        op = self.gcs.get_operation('storage.objects.update')
        params = op.build_parameters(body='body',
		object='object',
		bucket='bucket')
        self.assertTrue(params['payload'])
        self.assertTrue('object' in params['uri_params'])
        self.assertTrue('bucket' in params['uri_params'])

    def test_objects_update_missing_params(self):
        op = self.gcs.get_operation('storage.objects.update')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			object='object'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			bucket='bucket'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			object='object'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			bucket='bucket'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			object='object',
			bucket='bucket'
        )

    def test_objects_watchAll(self):
        op = self.gcs.get_operation('storage.objects.watchAll')
        params = op.build_parameters(body='body',
		bucket='bucket')
        self.assertTrue(params['payload'])
        self.assertTrue('bucket' in params['uri_params'])

    def test_objects_watchAll_missing_params(self):
        op = self.gcs.get_operation('storage.objects.watchAll')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			bucket='bucket'
        )