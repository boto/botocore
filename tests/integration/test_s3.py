# -*- coding: utf-8 -*-
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
from tests import unittest, temporary_file
from collections import defaultdict
import tempfile
import shutil
import threading
import mock
try:
    from itertools import izip_longest as zip_longest
except ImportError:
    from itertools import zip_longest

from nose.plugins.attrib import attr

from botocore.vendored.requests import adapters
from botocore.vendored.requests.exceptions import ConnectionError
from botocore.compat import six
import botocore.session
import botocore.auth
import botocore.credentials
import botocore.vendored.requests as requests


class BaseS3ClientTest(unittest.TestCase):
    def setUp(self):
        self.session = botocore.session.get_session()
        self.region = 'us-east-1'
        self.client = self.session.create_client('s3', region_name=self.region)
        self.keys = []

    def assert_status_code(self, response, status_code):
        self.assertEqual(
            response['ResponseMetadata']['HTTPStatusCode'],
            status_code
        )

    def create_bucket(self, bucket_name=None):
        bucket_kwargs = {}
        if bucket_name is None:
            bucket_name = 'botocoretest%s-%s' % (int(time.time()),
                                                 random.randint(1, 1000))
        bucket_kwargs = {'Bucket': bucket_name}
        if self.region != 'us-east-1':
            bucket_kwargs['CreateBucketConfiguration'] = {
                'LocationConstraint': self.region,
            }
        response = self.client.create_bucket(**bucket_kwargs)
        self.assert_status_code(response, 200)
        self.addCleanup(self.delete_bucket, bucket_name)
        return bucket_name

    def create_object(self, key_name, body='foo'):
        self.keys.append(key_name)
        self.client.put_object(
            Bucket=self.bucket_name, Key=key_name,
            Body=body)

    def create_multipart_upload(self, key_name):
        parsed = self.client.create_multipart_upload(
            Bucket=self.bucket_name, Key=key_name)
        upload_id = parsed['UploadId']
        self.addCleanup(
            self.client.abort_multipart_upload,
            UploadId=upload_id,
            Bucket=self.bucket_name, Key=key_name)

    def abort_multipart_upload(self, bucket_name, key, upload_id):
        self.client.abort_multipart_upload(
            UploadId=upload_id, Bucket=self.bucket_name, Key=key)

    def delete_object(self, key, bucket_name):
        response = self.client.delete_object(Bucket=bucket_name, Key=key)
        self.assert_status_code(response, 204)

    def delete_bucket(self, bucket_name):
        response = self.client.delete_bucket(Bucket=bucket_name)
        self.assert_status_code(response, 204)

    def create_object_catch_exceptions(self, key_name):
        try:
            self.create_object(key_name=key_name)
        except Exception as e:
            self.caught_exceptions.append(e)

    def assert_num_uploads_found(self, operation, num_uploads,
                                 max_items=None, num_attempts=5):
        amount_seen = None
        paginator = self.client.get_paginator(operation)
        for _ in range(num_attempts):
            pages = paginator.paginate(Bucket=self.bucket_name,
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


class TestS3BaseWithBucket(BaseS3ClientTest):
    def setUp(self):
        super(TestS3BaseWithBucket, self).setUp()
        self.region = 'us-west-2'
        self.bucket_name = self.create_bucket()


class TestS3Buckets(TestS3BaseWithBucket):

    def test_can_make_request(self):
        # Basic smoke test to ensure we can talk to s3.
        result = self.client.list_buckets()
        # Can't really assume anything about whether or not they have buckets,
        # but we can assume something about the structure of the response.
        self.assertEqual(sorted(list(result.keys())),
                         ['Buckets', 'Owner', 'ResponseMetadata'])

    def test_can_get_bucket_location(self):
        result = self.client.get_bucket_location(Bucket=self.bucket_name)
        self.assertIn('LocationConstraint', result)
        # For buckets in us-east-1 (US Classic Region) this will be None
        self.assertEqual(result['LocationConstraint'], self.region)


class TestS3Objects(TestS3BaseWithBucket):
    def tearDown(self):
        for key in self.keys:
            self.client.delete_object(
                Bucket=self.bucket_name, Key=key)
        super(TestS3Objects, self).tearDown()

    def increment_auth(self, request, **kwargs):
        self.auth_paths.append(request.auth_path)

    def test_can_delete_urlencoded_object(self):
        key_name = 'a+b/foo'
        self.create_object(key_name=key_name)
        self.keys.pop()
        bucket_contents = self.client.list_objects(
            Bucket=self.bucket_name)['Contents']
        self.assertEqual(len(bucket_contents), 1)
        self.assertEqual(bucket_contents[0]['Key'], 'a+b/foo')

        subdir_contents = self.client.list_objects(
            Bucket=self.bucket_name, Prefix='a+b')['Contents']
        self.assertEqual(len(subdir_contents), 1)
        self.assertEqual(subdir_contents[0]['Key'], 'a+b/foo')

        response = self.client.delete_object(
            Bucket=self.bucket_name, Key=key_name)
        self.assert_status_code(response, 204)

    @attr('slow')
    def test_can_paginate(self):
        for i in range(5):
            key_name = 'key%s' % i
            self.create_object(key_name)
        # Eventual consistency.
        time.sleep(3)
        paginator = self.client.get_paginator('list_objects')
        generator = paginator.paginate(MaxKeys=1,
                                       Bucket=self.bucket_name)
        responses = list(generator)
        self.assertEqual(len(responses), 5, responses)
        key_names = [el['Contents'][0]['Key']
                     for el in responses]
        self.assertEqual(key_names, ['key0', 'key1', 'key2', 'key3', 'key4'])

    @attr('slow')
    def test_can_paginate_with_page_size(self):
        for i in range(5):
            key_name = 'key%s' % i
            self.create_object(key_name)
        # Eventual consistency.
        time.sleep(3)
        paginator = self.client.get_paginator('list_objects')
        generator = paginator.paginate(page_size=1,
                                       Bucket=self.bucket_name)
        responses = list(generator)
        self.assertEqual(len(responses), 5, responses)
        data = [r for r in responses]
        key_names = [el['Contents'][0]['Key']
                     for el in data]
        self.assertEqual(key_names, ['key0', 'key1', 'key2', 'key3', 'key4'])

    @attr('slow')
    def test_result_key_iters(self):
        for i in range(5):
            key_name = 'key/%s/%s' % (i, i)
            self.create_object(key_name)
            key_name2 = 'key/%s' % i
            self.create_object(key_name2)
        time.sleep(3)
        paginator = self.client.get_paginator('list_objects')
        generator = paginator.paginate(MaxKeys=2,
                                       Prefix='key/',
                                       Delimiter='/',
                                       Bucket=self.bucket_name)
        iterators = generator.result_key_iters()
        response = defaultdict(list)
        key_names = [i.result_key for i in iterators]
        for vals in zip_longest(*iterators):
            for k, val in zip(key_names, vals):
                response.setdefault(k.expression, [])
                response[k.expression].append(val)
        self.assertIn('Contents', response)
        self.assertIn('CommonPrefixes', response)

    @attr('slow')
    def test_can_get_and_put_object(self):
        self.create_object('foobarbaz', body='body contents')
        time.sleep(3)

        data = self.client.get_object(
            Bucket=self.bucket_name, Key='foobarbaz')
        self.assertEqual(data['Body'].read().decode('utf-8'), 'body contents')

    def test_get_object_stream_wrapper(self):
        self.create_object('foobarbaz', body='body contents')
        response = self.client.get_object(
            Bucket=self.bucket_name, Key='foobarbaz')
        body = response['Body']
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

        # Verify when we have max_items=None, we get back all 8 uploads.
        self.assert_num_uploads_found('list_multipart_uploads',
                                      max_items=None, num_uploads=8)

        # Verify when we have max_items=1, we get back 1 upload.
        self.assert_num_uploads_found('list_multipart_uploads',
                                      max_items=1, num_uploads=1)

        paginator = self.client.get_paginator('list_multipart_uploads')
        # Works similar with build_full_result()
        pages = paginator.paginate(max_items=1,
                                   Bucket=self.bucket_name)
        full_result = pages.build_full_result()
        self.assertEqual(len(full_result['Uploads']), 1)

    def test_paginate_within_page_boundaries(self):
        self.create_object('a')
        self.create_object('b')
        self.create_object('c')
        self.create_object('d')
        paginator = self.client.get_paginator('list_objects')
        # First do it without a max keys so we're operating on a single page of
        # results.
        pages = paginator.paginate(max_items=1,
                                   Bucket=self.bucket_name)
        first = pages.build_full_result()
        t1 = first['NextToken']

        pages = paginator.paginate(max_items=1,
                                   starting_token=t1,
                                   Bucket=self.bucket_name)
        second = pages.build_full_result()
        t2 = second['NextToken']

        pages = paginator.paginate(max_items=1,
                                   starting_token=t2,
                                   Bucket=self.bucket_name)
        third = pages.build_full_result()
        t3 = third['NextToken']

        pages = paginator.paginate(max_items=1,
                                   starting_token=t3,
                                   Bucket=self.bucket_name)
        fourth = pages.build_full_result()

        self.assertEqual(first['Contents'][-1]['Key'], 'a')
        self.assertEqual(second['Contents'][-1]['Key'], 'b')
        self.assertEqual(third['Contents'][-1]['Key'], 'c')
        self.assertEqual(fourth['Contents'][-1]['Key'], 'd')

    def test_unicode_key_put_list(self):
        # Verify we can upload a key with a unicode char and list it as well.
        key_name = u'\u2713'
        self.create_object(key_name)
        parsed = self.client.list_objects(Bucket=self.bucket_name)
        self.assertEqual(len(parsed['Contents']), 1)
        self.assertEqual(parsed['Contents'][0]['Key'], key_name)
        parsed = self.client.get_object(
            Bucket=self.bucket_name, Key=key_name)
        self.assertEqual(parsed['Body'].read().decode('utf-8'), 'foo')

    def test_thread_safe_auth(self):
        self.auth_paths = []
        self.caught_exceptions = []
        self.session.register('before-sign', self.increment_auth)
        self.client = self.session.create_client('s3', self.region)
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
            "Expected 10 unique auth paths, instead received: %s" %
            (self.auth_paths))

    def test_non_normalized_key_paths(self):
        # The create_object method has assertEqual checks for 200 status.
        self.create_object('key./././name')
        bucket_contents = self.client.list_objects(
            Bucket=self.bucket_name)['Contents']
        self.assertEqual(len(bucket_contents), 1)
        self.assertEqual(bucket_contents[0]['Key'], 'key./././name')


class TestS3Regions(BaseS3ClientTest):
    def setUp(self):
        self.tempdir = tempfile.mkdtemp()
        self.region = 'us-west-2'
        super(TestS3Regions, self).setUp()

    def tearDown(self):
        shutil.rmtree(self.tempdir)

    def test_reset_stream_on_redirects(self):
        # Create a bucket in a non classic region.
        bucket_name = self.create_bucket()
        # Then try to put a file like object to this location.
        filename = os.path.join(self.tempdir, 'foo')
        with open(filename, 'wb') as f:
            f.write(b'foo' * 1024)
        with open(filename, 'rb') as f:
            self.client.put_object(
                Bucket=bucket_name, Key='foo', Body=f)

        self.addCleanup(self.delete_object, key='foo',
                        bucket_name=bucket_name)

        data = self.client.get_object(
            Bucket=bucket_name, Key='foo')
        self.assertEqual(data['Body'].read(), b'foo' * 1024)


class TestS3Copy(TestS3BaseWithBucket):

    def tearDown(self):
        for key in self.keys:
            self.client.delete_object(
                Bucket=self.bucket_name, Key=key)
        super(TestS3Copy, self).tearDown()

    def test_copy_with_quoted_char(self):
        key_name = 'a+b/foo'
        self.create_object(key_name=key_name)

        key_name2 = key_name + 'bar'
        self.client.copy_object(
            Bucket=self.bucket_name, Key=key_name + 'bar',
            CopySource='%s/%s' % (self.bucket_name, key_name))
        self.keys.append(key_name2)

        # Now verify we can retrieve the copied object.
        data = self.client.get_object(
            Bucket=self.bucket_name, Key=key_name + 'bar')
        self.assertEqual(data['Body'].read().decode('utf-8'), 'foo')

    def test_copy_with_s3_metadata(self):
        key_name = 'foo.txt'
        self.create_object(key_name=key_name)
        copied_key = 'copied.txt'
        parsed = self.client.copy_object(
            Bucket=self.bucket_name, Key=copied_key,
            CopySource='%s/%s' % (self.bucket_name, key_name),
            MetadataDirective='REPLACE',
            Metadata={"mykey": "myvalue", "mykey2": "myvalue2"})
        self.keys.append(copied_key)
        self.assert_status_code(parsed, 200)


# TODO: Convert this test to the presigning function that is to be
# added later
@unittest.skip('Need a method for presigning')
class TestS3Presign(BaseS3ClientTest):
    def setUp(self):
        super(TestS3Presign, self).setUp()
        self.bucket_name = 'botocoretest%s-%s' % (
            int(time.time()), random.randint(1, 1000))

        operation = self.service.get_operation('CreateBucket')
        response = operation.call(self.endpoint, bucket=self.bucket_name)
        self.assertEqual(response[0].status_code, 200)

    def tearDown(self):
        for key in self.keys:
            operation = self.service.get_operation('DeleteObject')
            operation.call(self.endpoint, bucket=self.bucket_name,
                           key=key)
        self.delete_bucket(self.bucket_name)
        super(TestS3Presign, self).tearDown()

    def test_can_retrieve_presigned_object(self):
        key_name = 'mykey'
        self.create_object(key_name=key_name, body='foobar')
        signer = botocore.auth.S3SigV4QueryAuth(
            credentials=self.service.session.get_credentials(),
            region_name='us-east-1', service_name='s3', expires=60)
        op = self.service.get_operation('GetObject')
        params = op.build_parameters(bucket=self.bucket_name, key=key_name)
        request = self.endpoint.create_request(params)
        signer.add_auth(request.original)
        presigned_url = request.original.prepare().url
        # We should now be able to retrieve the contents of 'mykey' using
        # this presigned url.
        self.assertEqual(requests.get(presigned_url).content, b'foobar')


@unittest.skip('Need a method for presigning')
class TestS3PresignFixHost(BaseS3ClientTest):
    def test_presign_does_not_change_host(self):
        endpoint = self.service.get_endpoint('us-west-2')
        key_name = 'mykey'
        bucket_name = 'mybucket'
        signer = botocore.auth.S3SigV4QueryAuth(
            credentials=self.session.get_credentials(),
            region_name='us-west-2', service_name='s3', expires=60)
        op = self.service.get_operation('GetObject')
        params = op.build_parameters(bucket=bucket_name, key=key_name)
        request = endpoint.create_request(params)
        signer.add_auth(request.original)
        presigned_url = request.original.prepare().url
        # We should not have rewritten the host to be s3.amazonaws.com.
        self.assertTrue(presigned_url.startswith(
            'https://s3-us-west-2.amazonaws.com/mybucket/mykey'),
            "Host was suppose to be the us-west-2 endpoint, instead "
            "got: %s" % presigned_url)


class TestCreateBucketInOtherRegion(TestS3BaseWithBucket):
    def tearDown(self):
        for key in self.keys:
            self.client.delete_object(
                Bucket=self.bucket_name, Key=key)

    def test_bucket_in_other_region(self):
        # This verifies expect 100-continue behavior.  We previously
        # had a bug where we did not support this behavior and trying to
        # create a bucket and immediately PutObject with a file like object
        # would actually cause errors.
        client = self.session.create_client('s3', 'us-east-1')
        with temporary_file('w') as f:
            f.write('foobarbaz' * 1024 * 1024)
            f.flush()
            with open(f.name, 'rb') as body_file:
                response = client.put_object(
                    Bucket=self.bucket_name,
                    Key='foo.txt', Body=body_file)
            self.assert_status_code(response, 200)
            self.keys.append('foo.txt')

    def test_bucket_in_other_region_using_http(self):
        client = self.session.create_client(
            's3', 'us-east-1', endpoint_url='http://s3.amazonaws.com/')
        with temporary_file('w') as f:
            f.write('foobarbaz' * 1024 * 1024)
            f.flush()
            with open(f.name, 'rb') as body_file:
                response = client.put_object(
                    Bucket=self.bucket_name,
                    Key='foo.txt', Body=body_file)
            self.assert_status_code(response, 200)
            self.keys.append('foo.txt')


class TestS3SigV4Client(BaseS3ClientTest):
    def setUp(self):
        super(TestS3SigV4Client, self).setUp()
        self.region = 'eu-central-1'
        self.client = self.session.create_client('s3', self.region)
        self.bucket_name = self.create_bucket()
        self.keys = []

    def tearDown(self):
        super(TestS3SigV4Client, self).tearDown()
        for key in self.keys:
            response = self.delete_object(bucket_name=self.bucket_name,
                                          key=key)

    def test_can_get_bucket_location(self):
        # Even though the bucket is in eu-central-1, we should still be able to
        # use the us-east-1 endpoint class to get the bucket location.
        client = self.session.create_client('s3', 'us-east-1')
        # Also keep in mind that while this test is useful, it doesn't test
        # what happens once DNS propogates which is arguably more interesting,
        # as DNS will point us to the eu-central-1 endpoint.
        response = client.get_bucket_location(Bucket=self.bucket_name)
        self.assertEqual(response['LocationConstraint'], 'eu-central-1')

    def test_request_retried_for_sigv4(self):
        body = six.BytesIO(b"Hello world!")

        original_send = adapters.HTTPAdapter.send
        state = mock.Mock()
        state.error_raised = False

        def mock_http_adapter_send(self, *args, **kwargs):
            if not state.error_raised:
                state.error_raised = True
                raise ConnectionError("Simulated ConnectionError raised.")
            else:
                return original_send(self, *args, **kwargs)
        with mock.patch('botocore.vendored.requests.adapters.HTTPAdapter.send',
                        mock_http_adapter_send):
            response = self.client.put_object(Bucket=self.bucket_name,
                                              Key='foo.txt', Body=body)
            self.assert_status_code(response, 200)
            self.keys.append('foo.txt')

    @attr('slow')
    def test_paginate_list_objects_unicode(self):
        key_names = [
            u'non-ascii-key-\xe4\xf6\xfc-01.txt',
            u'non-ascii-key-\xe4\xf6\xfc-02.txt',
            u'non-ascii-key-\xe4\xf6\xfc-03.txt',
            u'non-ascii-key-\xe4\xf6\xfc-04.txt',
        ]
        for key in key_names:
            response = self.client.put_object(Bucket=self.bucket_name,
                                              Key=key, Body='')
            self.assert_status_code(response, 200)
            self.keys.append(key)

        list_objs_paginator = self.client.get_paginator('list_objects')
        key_refs = []
        for response in list_objs_paginator.paginate(Bucket=self.bucket_name,
                                                     page_size=2):
            for content in response['Contents']:
                key_refs.append(content['Key'])

        self.assertEqual(key_names, key_refs)

    @attr('slow')
    def test_paginate_list_objects_safe_chars(self):
        key_names = [
            u'-._~safe-chars-key-01.txt',
            u'-._~safe-chars-key-02.txt',
            u'-._~safe-chars-key-03.txt',
            u'-._~safe-chars-key-04.txt',
        ]
        for key in key_names:
            response = self.client.put_object(Bucket=self.bucket_name,
                                              Key=key, Body='')
            self.assert_status_code(response, 200)
            self.keys.append(key)

        list_objs_paginator = self.client.get_paginator('list_objects')
        key_refs = []
        for response in list_objs_paginator.paginate(Bucket=self.bucket_name,
                                                     page_size=2):
            for content in response['Contents']:
                key_refs.append(content['Key'])

        self.assertEqual(key_names, key_refs)

    def test_create_multipart_upload(self):
        key = 'mymultipartupload'
        response = self.client.create_multipart_upload(
            Bucket=self.bucket_name, Key=key
        )
        self.assert_status_code(response, 200)
        upload_id = response['UploadId']
        self.addCleanup(
            self.abort_multipart_upload,
            bucket_name=self.bucket_name, key=key, upload_id=upload_id
        )

        response = self.client.list_multipart_uploads(
            Bucket=self.bucket_name, Prefix=key
        )

        # Make sure there is only one multipart upload.
        self.assertEqual(len(response['Uploads']), 1)
        # Make sure the upload id is as expected.
        self.assertEqual(response['Uploads'][0]['UploadId'], upload_id)


class TestCanSwitchToSigV4(unittest.TestCase):
    def setUp(self):
        self.environ = {}
        self.environ_patch = mock.patch('os.environ', self.environ)
        self.environ_patch.start()
        self.session = botocore.session.get_session()
        self.tempdir = tempfile.mkdtemp()
        self.config_filename = os.path.join(self.tempdir, 'config_file')
        self.environ['AWS_CONFIG_FILE'] = self.config_filename

    def tearDown(self):
        self.environ_patch.stop()
        shutil.rmtree(self.tempdir)


class TestSSEKeyParamValidation(unittest.TestCase):
    def setUp(self):
        self.session = botocore.session.get_session()
        self.client = self.session.create_client('s3', 'us-west-2')
        self.bucket_name = 'botocoretest%s-%s' % (
            int(time.time()), random.randint(1, 1000))
        self.client.create_bucket(
            Bucket=self.bucket_name,
            CreateBucketConfiguration={
                'LocationConstraint': 'us-west-2',
            }
        )
        self.addCleanup(self.client.delete_bucket, Bucket=self.bucket_name)

    def test_make_request_with_sse(self):
        key_bytes = os.urandom(32)
        # Obviously a bad key here, but we just want to ensure we can use
        # a str/unicode type as a key.
        key_str = 'abcd' * 8

        # Put two objects with an sse key, one with random bytes,
        # one with str/unicode.  Then verify we can GetObject() both
        # objects.
        self.client.put_object(
            Bucket=self.bucket_name, Key='foo.txt',
            Body=six.BytesIO(b'mycontents'), SSECustomerAlgorithm='AES256',
            SSECustomerKey=key_bytes)
        self.addCleanup(self.client.delete_object,
                        Bucket=self.bucket_name, Key='foo.txt')
        self.client.put_object(
            Bucket=self.bucket_name, Key='foo2.txt',
            Body=six.BytesIO(b'mycontents2'), SSECustomerAlgorithm='AES256',
            SSECustomerKey=key_str)
        self.addCleanup(self.client.delete_object,
                        Bucket=self.bucket_name, Key='foo2.txt')

        self.assertEqual(
            self.client.get_object(Bucket=self.bucket_name,
                                   Key='foo.txt',
                                   SSECustomerAlgorithm='AES256',
                                   SSECustomerKey=key_bytes)['Body'].read(),
            b'mycontents')
        self.assertEqual(
            self.client.get_object(Bucket=self.bucket_name,
                                   Key='foo2.txt',
                                   SSECustomerAlgorithm='AES256',
                                   SSECustomerKey=key_str)['Body'].read(),
            b'mycontents2')


class TestS3UTF8Headers(BaseS3ClientTest):
    def test_can_set_utf_8_headers(self):
        bucket_name = self.create_bucket()
        body = six.BytesIO(b"Hello world!")
        response = self.client.put_object(
            Bucket=bucket_name, Key="foo.txt", Body=body,
            ContentDisposition="attachment; filename=5小時接力起跑.jpg;")
        self.assert_status_code(response, 200)
        self.addCleanup(self.client.delete_object,
                        Bucket=bucket_name, Key="foo.txt")


if __name__ == '__main__':
    unittest.main()
