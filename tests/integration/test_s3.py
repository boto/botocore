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
import time
import random
from tests import unittest
from collections import defaultdict
import tempfile
import shutil
import threading
try:
    from itertools import izip_longest as zip_longest
except ImportError:
    from itertools import zip_longest

import botocore.session


class BaseS3Test(unittest.TestCase):
    def setUp(self):
        self.session = botocore.session.get_session()
        self.service = self.session.get_service('s3')
        self.endpoint = self.service.get_endpoint('us-east-1')
        self.keys = []

    def create_object(self, key_name, body='foo'):
        self.keys.append(key_name)
        operation = self.service.get_operation('PutObject')
        response = operation.call(
            self.endpoint, bucket=self.bucket_name, key=key_name,
            body=body)[0]
        self.assertEqual(response.status_code, 200)

    def create_multipart_upload(self, key_name):
        operation = self.service.get_operation('CreateMultipartUpload')
        http_response, parsed = operation.call(self.endpoint,
                                               bucket=self.bucket_name,
                                               key=key_name)
        upload_id = parsed['UploadId']
        self.addCleanup(self.service.get_operation('AbortMultipartUpload').call,
                        self.endpoint, upload_id=upload_id,
                        bucket=self.bucket_name, key=key_name)

    def create_object_catch_exceptions(self, key_name):
        try:
            self.create_object(key_name=key_name)
        except Exception as e:
            self.caught_exceptions.append(e)

    def assert_num_uploads_found(self, operation, num_uploads,
                                 max_items=None, num_attempts=5):
        amount_seen = None
        for _ in range(num_attempts):
            pages = operation.paginate(self.endpoint, bucket=self.bucket_name,
                                       max_items=max_items)
            iterators = pages.result_key_iters()
            self.assertEqual(len(iterators), 2)
            self.assertEqual(iterators[0].result_key.expression, 'Uploads')
            # It sometimes takes a while for all the uploads to show up,
            # especially if the upload was just created.  If we don't
            # see the expected amount, we retry up to num_attempts time
            # before failing.
            amount_seen = len(list(iterators[0]))
            if amount_seen == num_uploads:
                # Test passed.
                return
            else:
                # Sleep and try again.
                time.sleep(2)
        self.fail("Expected to see %s uploads, instead saw: %s" % (
            num_uploads, amount_seen))


class TestS3Buckets(BaseS3Test):

    def setUp(self):
        super(TestS3Buckets, self).setUp()
        self.bucket_name = 'botocoretest%s-%s' % (
            int(time.time()), random.randint(1, 1000))
        self.bucket_location = 'us-west-2'

        operation = self.service.get_operation('CreateBucket')
        operation.call(self.endpoint, bucket=self.bucket_name,
            create_bucket_configuration={'LocationConstraint': self.bucket_location})

    def tearDown(self):
        operation = self.service.get_operation('DeleteBucket')
        operation.call(self.endpoint, bucket=self.bucket_name)

    def test_can_make_request(self):
        # Basic smoke test to ensure we can talk to s3.
        operation = self.service.get_operation('ListBuckets')
        http, result = operation.call(self.endpoint)
        self.assertEqual(http.status_code, 200)
        # Can't really assume anything about whether or not they have buckets,
        # but we can assume something about the structure of the response.
        self.assertEqual(sorted(list(result.keys())),
                         ['Buckets', 'Owner', 'ResponseMetadata'])

    def test_can_get_bucket_location(self):
        operation = self.service.get_operation('GetBucketLocation')
        http, result = operation.call(self.endpoint, bucket=self.bucket_name)
        self.assertEqual(http.status_code, 200)
        self.assertIn('LocationConstraint', result)
        # For buckets in us-east-1 (US Classic Region) this will be None
        self.assertEqual(result['LocationConstraint'], self.bucket_location)


class TestS3Objects(BaseS3Test):

    def setUp(self):
        super(TestS3Objects, self).setUp()
        self.bucket_name = 'botocoretest%s-%s' % (
            int(time.time()), random.randint(1, 1000))
        operation = self.service.get_operation('CreateBucket')
        operation.call(self.endpoint, bucket=self.bucket_name)

    def tearDown(self):
        for key in self.keys:
            operation = self.service.get_operation('DeleteObject')
            operation.call(self.endpoint, bucket=self.bucket_name,
                           key=key)
        operation = self.service.get_operation('DeleteBucket')
        operation.call(self.endpoint, bucket=self.bucket_name)

    def increment_auth(self, request, auth, **kwargs):
        self.auth_paths.append(auth.auth_path)

    def test_can_delete_urlencoded_object(self):
        key_name = 'a+b/foo'
        self.create_object(key_name=key_name)
        self.keys.pop()
        bucket_contents = self.service.get_operation('ListObjects').call(
            self.endpoint, bucket=self.bucket_name)[1]['Contents']
        self.assertEqual(len(bucket_contents), 1)
        self.assertEqual(bucket_contents[0]['Key'], 'a+b/foo')

        subdir_contents = self.service.get_operation('ListObjects').call(
            self.endpoint, bucket=self.bucket_name, prefix='a+b')[1]['Contents']
        self.assertEqual(len(subdir_contents), 1)
        self.assertEqual(subdir_contents[0]['Key'], 'a+b/foo')

        operation = self.service.get_operation('DeleteObject')
        response = operation.call(self.endpoint, bucket=self.bucket_name,
                                  key=key_name)[0]
        self.assertEqual(response.status_code, 204)

    def test_can_paginate(self):
        for i in range(5):
            key_name = 'key%s' % i
            self.create_object(key_name)
        # Eventual consistency.
        time.sleep(3)
        operation = self.service.get_operation('ListObjects')
        generator = operation.paginate(self.endpoint, max_keys=1,
                                       bucket=self.bucket_name)
        responses = list(generator)
        self.assertEqual(len(responses), 5, responses)
        data = [r[1] for r in responses]
        key_names = [el['Contents'][0]['Key']
                     for el in data]
        self.assertEqual(key_names, ['key0', 'key1', 'key2', 'key3', 'key4'])

    def test_result_key_iters(self):
        for i in range(5):
            key_name = 'key/%s/%s' % (i, i)
            self.create_object(key_name)
            key_name2 = 'key/%s' % i
            self.create_object(key_name2)
        time.sleep(3)
        operation = self.service.get_operation('ListObjects')
        generator = operation.paginate(self.endpoint, max_keys=2,
                                       prefix='key/',
                                       delimiter='/',
                                       bucket=self.bucket_name)
        iterators = generator.result_key_iters()
        response = defaultdict(list)
        key_names = [i.result_key for i in iterators]
        for vals in zip_longest(*iterators):
            for k, val in zip(key_names, vals):
                response.setdefault(k.expression, [])
                response[k.expression].append(val)
        self.assertIn('Contents', response)
        self.assertIn('CommonPrefixes', response)

    def test_can_get_and_put_object(self):
        self.create_object('foobarbaz', body='body contents')
        time.sleep(3)

        operation = self.service.get_operation('GetObject')
        response = operation.call(self.endpoint, bucket=self.bucket_name,
                                  key='foobarbaz')
        data = response[1]
        self.assertEqual(data['Body'].read().decode('utf-8'), 'body contents')

    def test_get_object_stream_wrapper(self):
        self.create_object('foobarbaz', body='body contents')
        operation = self.service.get_operation('GetObject')
        response = operation.call(self.endpoint, bucket=self.bucket_name,
                                  key='foobarbaz')
        body = response[1]['Body']
        # Am able to set a socket timeout
        body.set_socket_timeout(10)
        self.assertEqual(body.read(amt=1).decode('utf-8'), 'b')
        self.assertEqual(body.read().decode('utf-8'), 'ody contents')

    def test_paginate_max_items(self):
        self.create_multipart_upload('foo/key1')
        self.create_multipart_upload('foo/key1')
        self.create_multipart_upload('foo/key1')
        self.create_multipart_upload('foo/key2')
        self.create_multipart_upload('foobar/key1')
        self.create_multipart_upload('foobar/key2')
        self.create_multipart_upload('bar/key1')
        self.create_multipart_upload('bar/key2')

        operation = self.service.get_operation('ListMultipartUploads')

        # Verify when we have max_items=None, we get back all 8 uploads.
        self.assert_num_uploads_found(operation, max_items=None, num_uploads=8)

        # Verify when we have max_items=1, we get back 1 upload.
        self.assert_num_uploads_found(operation, max_items=1, num_uploads=1)

        # Works similar with build_full_result()
        pages = operation.paginate(self.endpoint,
                                   max_items=1,
                                   bucket=self.bucket_name)
        full_result = pages.build_full_result()
        self.assertEqual(len(full_result['Uploads']), 1)

    def test_paginate_within_page_boundaries(self):
        self.create_object('a')
        self.create_object('b')
        self.create_object('c')
        self.create_object('d')
        operation = self.service.get_operation('ListObjects')
        # First do it without a max keys so we're operating on a single page of
        # results.
        pages = operation.paginate(self.endpoint, max_items=1,
                                   bucket=self.bucket_name)
        first = pages.build_full_result()
        t1 = first['NextToken']

        pages = operation.paginate(self.endpoint, max_items=1,
                                   starting_token=t1,
                                   bucket=self.bucket_name)
        second = pages.build_full_result()
        t2 = second['NextToken']

        pages = operation.paginate(self.endpoint, max_items=1,
                                   starting_token=t2,
                                   bucket=self.bucket_name)
        third = pages.build_full_result()
        t3 = third['NextToken']

        pages = operation.paginate(self.endpoint, max_items=1,
                                   starting_token=t3,
                                   bucket=self.bucket_name)
        fourth = pages.build_full_result()

        self.assertEqual(first['Contents'][-1]['Key'], 'a')
        self.assertEqual(second['Contents'][-1]['Key'], 'b')
        self.assertEqual(third['Contents'][-1]['Key'], 'c')
        self.assertEqual(fourth['Contents'][-1]['Key'], 'd')

    def test_unicode_key_put_list(self):
        # Verify we can upload a key with a unicode char and list it as well.
        key_name = u'\u2713'
        self.create_object(key_name)
        operation = self.service.get_operation('ListObjects')
        parsed = operation.call(self.endpoint, bucket=self.bucket_name)[1]
        self.assertEqual(len(parsed['Contents']), 1)
        self.assertEqual(parsed['Contents'][0]['Key'], key_name)
        operation = self.service.get_operation('GetObject')
        parsed = operation.call(self.endpoint, bucket=self.bucket_name, key=key_name)[1]
        self.assertEqual(parsed['Body'].read().decode('utf-8'), 'foo')

    def test_thread_safe_auth(self):
        self.auth_paths = []
        self.caught_exceptions = []
        self.session.register('before-auth', self.increment_auth)
        self.create_object(key_name='foo1')
        threads = []
        for i in range(10):
            t = threading.Thread(target=self.create_object_catch_exceptions,
                                 args=('foo%s' % i,))
            t.daemon = True
            threads.append(t)
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        self.assertEqual(
            self.caught_exceptions, [],
            "Unexpectedly caught exceptions: %s" % self.caught_exceptions)
        self.assertEqual(
            len(set(self.auth_paths)), 10,
            "Expected 10 unique auth paths, instead received: %s" % (self.auth_paths))

    def test_non_normalized_key_paths(self):
        # The create_object method has assertEqual checks for 200 status.
        self.create_object('key./././name')
        bucket_contents = self.service.get_operation('ListObjects').call(
            self.endpoint, bucket=self.bucket_name)[1]['Contents']
        self.assertEqual(len(bucket_contents), 1)
        self.assertEqual(bucket_contents[0]['Key'], 'key./././name')


class TestS3Regions(BaseS3Test):
    def setUp(self):
        super(TestS3Regions, self).setUp()
        self.tempdir = tempfile.mkdtemp()
        self.endpoint = self.service.get_endpoint('us-west-2')

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def create_bucket_in_region(self, region):
        bucket_name = 'botocoretest%s-%s' % (
            int(time.time()), random.randint(1, 1000))
        operation = self.service.get_operation('CreateBucket')
        response, parsed = operation.call(
            self.endpoint, bucket=bucket_name,
            create_bucket_configuration={'LocationConstraint': 'us-west-2'})
        self.assertEqual(response.status_code, 200)
        self.addCleanup(self.service.get_operation('DeleteBucket').call,
                        bucket=bucket_name, endpoint=self.endpoint)
        return bucket_name

    def test_reset_stream_on_redirects(self):
        # Create a bucket in a non classic region.
        bucket_name = self.create_bucket_in_region('us-west-2')
        # Then try to put a file like object to this location.
        filename = os.path.join(self.tempdir, 'foo')
        with open(filename, 'wb') as f:
            f.write(b'foo' * 1024)
        put_object = self.service.get_operation('PutObject')
        with open(filename, 'rb') as f:
            response, parsed = put_object.call(
                self.endpoint, bucket=bucket_name, key='foo', body=f)
        self.assertEqual(
            response.status_code, 200,
            "Non 200 status code (%s) received: %s" % (
                response.status_code, parsed))

        operation = self.service.get_operation('GetObject')
        data = operation.call(self.endpoint, bucket=bucket_name,
                              key='foo')[1]
        self.assertEqual(data['Body'].read(), b'foo' * 1024)


class TestS3Copy(BaseS3Test):
    def setUp(self):
        super(TestS3Copy, self).setUp()
        self.bucket_name = 'botocoretest%s-%s' % (
            int(time.time()), random.randint(1, 1000))
        self.bucket_location = 'us-west-2'

        operation = self.service.get_operation('CreateBucket')
        operation.call(self.endpoint, bucket=self.bucket_name,
            create_bucket_configuration={'LocationConstraint': self.bucket_location})

    def tearDown(self):
        operation = self.service.get_operation('DeleteBucket')
        operation.call(self.endpoint, bucket=self.bucket_name)

    def test_copy_with_quoted_char(self):
        key_name = 'a+b/foo'
        self.create_object(key_name=key_name)

        operation = self.service.get_operation('CopyObject')
        http, parsed = operation.call(
            self.endpoint, bucket=self.bucket_name, key=key_name + 'bar',
            copy_source='%s/%s' % (self.bucket_name, key_name))
        self.assertEqual(http.status_code, 200)

        # Now verify we can retrieve the copied object.
        operation = self.service.get_operation('GetObject')
        response = operation.call(self.endpoint, bucket=self.bucket_name,
                                  key=key_name + 'bar')
        data = response[1]
        self.assertEqual(data['Body'].read().decode('utf-8'), 'foo')


if __name__ == '__main__':
    unittest.main()
