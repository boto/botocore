# -*- coding: utf-8 -*-
# Copyright 2012-2015 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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
from tests import unittest, temporary_file, random_chars
import os
import time
from collections import defaultdict
import tempfile
import shutil
import threading
import mock
from tarfile import TarFile
from contextlib import closing

from nose.plugins.attrib import attr

from botocore.vendored.requests import adapters
from botocore.vendored.requests.exceptions import ConnectionError
from botocore.compat import six, zip_longest
import botocore.session
import botocore.auth
import botocore.credentials
import botocore.vendored.requests as requests
from botocore.client import Config


def random_bucketname():
    # 63 is the max bucket length.
    bucket_name = 'botocoretest'
    return bucket_name + random_chars(63 - len(bucket_name))


def recursive_delete(client, bucket_name):
    # Recursively deletes a bucket and all of its contents.
    objects = client.get_paginator('list_objects').paginate(
        Bucket=bucket_name)
    for key in objects.search('Contents[].Key'):
        if key is not None:
            client.delete_object(Bucket=bucket_name, Key=key)
    client.delete_bucket(Bucket=bucket_name)


class BaseS3ClientTest(unittest.TestCase):
    def setUp(self):
        self.session = botocore.session.get_session()
        self.region = 'us-east-1'
        self.client = self.session.create_client('s3', region_name=self.region)

    def assert_status_code(self, response, status_code):
        self.assertEqual(
            response['ResponseMetadata']['HTTPStatusCode'],
            status_code
        )

    def create_bucket(self, region_name, bucket_name=None):
        bucket_kwargs = {}
        if bucket_name is None:
            bucket_name = random_bucketname()
        bucket_kwargs = {'Bucket': bucket_name}
        if region_name != 'us-east-1':
            bucket_kwargs['CreateBucketConfiguration'] = {
                'LocationConstraint': region_name,
            }
        response = self.client.create_bucket(**bucket_kwargs)
        self.assert_status_code(response, 200)
        self.addCleanup(recursive_delete, self.client, bucket_name)
        return bucket_name

    def make_tempdir(self):
        tempdir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, tempdir)
        return tempdir


class TestS3BaseWithBucket(BaseS3ClientTest):
    def setUp(self):
        super(TestS3BaseWithBucket, self).setUp()
        self.bucket_name = self.create_bucket(self.region)
        self.caught_exceptions = []

    def create_object(self, key_name, body='foo'):
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
                                       PaginationConfig={
                                           'MaxItems': max_items})
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


class TestS3Buckets(TestS3BaseWithBucket):
    def setUp(self):
        super(TestS3Buckets, self).setUp()

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
        self.assertEqual(result['LocationConstraint'], None)


class TestS3Objects(TestS3BaseWithBucket):

    def increment_auth(self, request, **kwargs):
        self.auth_paths.append(request.auth_path)

    def test_can_delete_urlencoded_object(self):
        key_name = 'a+b/foo'
        self.create_object(key_name=key_name)
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
        generator = paginator.paginate(PaginationConfig={'PageSize': 1},
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

        # Verify when we have MaxItems=None, we get back all 8 uploads.
        self.assert_num_uploads_found('list_multipart_uploads',
                                      max_items=None, num_uploads=8)

        # Verify when we have MaxItems=1, we get back 1 upload.
        self.assert_num_uploads_found('list_multipart_uploads',
                                      max_items=1, num_uploads=1)

        paginator = self.client.get_paginator('list_multipart_uploads')
        # Works similar with build_full_result()
        pages = paginator.paginate(PaginationConfig={'MaxItems': 1},
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
        pages = paginator.paginate(PaginationConfig={'MaxItems': 1},
                                   Bucket=self.bucket_name)
        first = pages.build_full_result()
        t1 = first['NextToken']

        pages = paginator.paginate(
            PaginationConfig={'MaxItems': 1, 'StartingToken': t1},
            Bucket=self.bucket_name)
        second = pages.build_full_result()
        t2 = second['NextToken']

        pages = paginator.paginate(
            PaginationConfig={'MaxItems': 1, 'StartingToken': t2},
            Bucket=self.bucket_name)
        third = pages.build_full_result()
        t3 = third['NextToken']

        pages = paginator.paginate(
            PaginationConfig={'MaxItems': 1, 'StartingToken': t3},
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
        super(TestS3Regions, self).setUp()
        self.region = 'us-west-2'
        self.client = self.session.create_client(
            's3', region_name=self.region)

    def test_reset_stream_on_redirects(self):
        # Create a bucket in a non classic region.
        bucket_name = self.create_bucket(self.region)
        # Then try to put a file like object to this location.
        tempdir = self.make_tempdir()
        filename = os.path.join(tempdir, 'foo')
        with open(filename, 'wb') as f:
            f.write(b'foo' * 1024)
        with open(filename, 'rb') as f:
            self.client.put_object(
                Bucket=bucket_name, Key='foo', Body=f)

        data = self.client.get_object(
            Bucket=bucket_name, Key='foo')
        self.assertEqual(data['Body'].read(), b'foo' * 1024)


class TestS3Copy(TestS3BaseWithBucket):

    def test_copy_with_quoted_char(self):
        key_name = 'a+b/foo'
        self.create_object(key_name=key_name)

        key_name2 = key_name + 'bar'
        self.client.copy_object(
            Bucket=self.bucket_name, Key=key_name2,
            CopySource='%s/%s' % (self.bucket_name, key_name))

        # Now verify we can retrieve the copied object.
        data = self.client.get_object(
            Bucket=self.bucket_name, Key=key_name2)
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
        self.assert_status_code(parsed, 200)


class BaseS3PresignTest(BaseS3ClientTest):

    def setup_bucket(self):
        self.key = 'myobject'
        self.bucket_name = self.create_bucket(self.region)
        self.create_object(key_name=self.key)

    def create_object(self, key_name, body='foo'):
        self.client.put_object(
            Bucket=self.bucket_name, Key=key_name,
            Body=body)


class TestS3PresignUsStandard(BaseS3PresignTest):
    def setUp(self):
        super(TestS3PresignUsStandard, self).setUp()
        self.region = 'us-east-1'
        self.client_config = Config(
            region_name=self.region, signature_version='s3')
        self.client = self.session.create_client(
            's3', config=self.client_config)
        self.setup_bucket()

    def test_presign_sigv2(self):
        presigned_url = self.client.generate_presigned_url(
            'get_object', Params={'Bucket': self.bucket_name, 'Key': self.key})
        self.assertTrue(
            presigned_url.startswith(
                'https://%s.s3.amazonaws.com/%s' % (
                    self.bucket_name, self.key)),
            "Host was suppose to use DNS style, instead "
            "got: %s" % presigned_url)
        # Try to retrieve the object using the presigned url.
        self.assertEqual(requests.get(presigned_url).content, b'foo')

    def test_presign_with_existing_query_string_values(self):
        content_disposition = 'attachment; filename=foo.txt;'
        presigned_url = self.client.generate_presigned_url(
            'get_object', Params={
                'Bucket': self.bucket_name, 'Key': self.key,
                'ResponseContentDisposition': content_disposition})
        response = requests.get(presigned_url)
        self.assertEqual(response.headers['Content-Disposition'],
                         content_disposition)
        self.assertEqual(response.content, b'foo')

    def test_presign_sigv4(self):
        self.client_config.signature_version = 's3v4'
        self.client = self.session.create_client(
            's3', config=self.client_config)
        presigned_url = self.client.generate_presigned_url(
            'get_object', Params={'Bucket': self.bucket_name, 'Key': self.key})
        self.assertTrue(
            presigned_url.startswith(
                'https://s3.amazonaws.com/%s/%s' % (
                    self.bucket_name, self.key)),
            "Host was suppose to be the us-east-1 endpoint, instead "
            "got: %s" % presigned_url)
        # Try to retrieve the object using the presigned url.
        self.assertEqual(requests.get(presigned_url).content, b'foo')

    def test_presign_post_sigv2(self):

        # Create some of the various supported conditions.
        conditions = [
            {"acl": "public-read"},
        ]

        # Create the fields that follow the policy.
        fields = {
            'acl': 'public-read',
        }

        # Retrieve the args for the presigned post.
        post_args = self.client.generate_presigned_post(
            self.bucket_name, self.key, Fields=fields,
            Conditions=conditions)

        # Make sure that the form can be posted successfully.
        files = {'file': ('baz', 'some data')}

        # Make sure the correct endpoint is being used
        self.assertTrue(
            post_args['url'].startswith(
                'https://%s.s3.amazonaws.com' % self.bucket_name),
            "Host was suppose to use DNS style, instead "
            "got: %s" % post_args['url'])

        # Try to retrieve the object using the presigned url.
        r = requests.post(
            post_args['url'], data=post_args['fields'], files=files)
        self.assertEqual(r.status_code, 204)

    def test_presign_post_sigv4(self):
        self.client_config.signature_version = 's3v4'
        self.client = self.session.create_client(
            's3', config=self.client_config)

        # Create some of the various supported conditions.
        conditions = [
            {"acl": 'public-read'},
        ]

        # Create the fields that follow the policy.
        fields = {
            'acl': 'public-read',
        }

        # Retrieve the args for the presigned post.
        post_args = self.client.generate_presigned_post(
            self.bucket_name, self.key, Fields=fields,
            Conditions=conditions)

        # Make sure that the form can be posted successfully.
        files = {'file': ('baz', 'some data')}

        # Make sure the correct endpoint is being used
        self.assertTrue(
            post_args['url'].startswith(
                'https://s3.amazonaws.com/%s' % self.bucket_name),
            "Host was suppose to use us-east-1 endpoint, instead "
            "got: %s" % post_args['url'])

        r = requests.post(
            post_args['url'], data=post_args['fields'], files=files)
        self.assertEqual(r.status_code, 204)


class TestS3PresignNonUsStandard(BaseS3PresignTest):

    def setUp(self):
        super(TestS3PresignNonUsStandard, self).setUp()
        self.region = 'us-west-2'
        self.client_config = Config(
            region_name=self.region, signature_version='s3')
        self.client = self.session.create_client(
            's3', config=self.client_config)
        self.setup_bucket()

    def test_presign_sigv2(self):
        presigned_url = self.client.generate_presigned_url(
            'get_object', Params={'Bucket': self.bucket_name, 'Key': self.key})
        self.assertTrue(
            presigned_url.startswith(
                'https://%s.s3.amazonaws.com/%s' % (
                    self.bucket_name, self.key)),
            "Host was suppose to use DNS style, instead "
            "got: %s" % presigned_url)
        # Try to retrieve the object using the presigned url.
        self.assertEqual(requests.get(presigned_url).content, b'foo')

    def test_presign_sigv4(self):
        self.client_config.signature_version = 's3v4'
        self.client = self.session.create_client(
            's3', config=self.client_config)
        presigned_url = self.client.generate_presigned_url(
            'get_object', Params={'Bucket': self.bucket_name, 'Key': self.key})

        self.assertTrue(
            presigned_url.startswith(
                'https://s3-us-west-2.amazonaws.com/%s/%s' % (
                    self.bucket_name, self.key)),
            "Host was suppose to be the us-west-2 endpoint, instead "
            "got: %s" % presigned_url)
        # Try to retrieve the object using the presigned url.
        self.assertEqual(requests.get(presigned_url).content, b'foo')

    def test_presign_post_sigv2(self):
        # Create some of the various supported conditions.
        conditions = [
            {"acl": "public-read"},
        ]

        # Create the fields that follow the policy.
        fields = {
            'acl': 'public-read',
        }

        # Retrieve the args for the presigned post.
        post_args = self.client.generate_presigned_post(
            self.bucket_name, self.key, Fields=fields, Conditions=conditions)

        # Make sure that the form can be posted successfully.
        files = {'file': ('baz', 'some data')}

        # Make sure the correct endpoint is being used
        self.assertTrue(
            post_args['url'].startswith(
                'https://%s.s3.amazonaws.com' % self.bucket_name),
            "Host was suppose to use DNS style, instead "
            "got: %s" % post_args['url'])

        r = requests.post(
            post_args['url'], data=post_args['fields'], files=files)
        self.assertEqual(r.status_code, 204)

    def test_presign_post_sigv4(self):
        self.client_config.signature_version = 's3v4'
        self.client = self.session.create_client(
            's3', config=self.client_config)

        # Create some of the various supported conditions.
        conditions = [
            {"acl": "public-read"},
        ]

        # Create the fields that follow the policy.
        fields = {
            'acl': 'public-read',
        }

        # Retrieve the args for the presigned post.
        post_args = self.client.generate_presigned_post(
            self.bucket_name, self.key, Fields=fields, Conditions=conditions)

        # Make sure that the form can be posted successfully.
        files = {'file': ('baz', 'some data')}

        # Make sure the correct endpoint is being used
        self.assertTrue(
            post_args['url'].startswith(
                'https://s3-us-west-2.amazonaws.com/%s' % self.bucket_name),
            "Host was suppose to use DNS style, instead "
            "got: %s" % post_args['url'])

        r = requests.post(
            post_args['url'], data=post_args['fields'], files=files)
        self.assertEqual(r.status_code, 204)


class TestCreateBucketInOtherRegion(TestS3BaseWithBucket):

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


class TestS3SigV4Client(BaseS3ClientTest):
    def setUp(self):
        super(TestS3SigV4Client, self).setUp()
        self.region = 'eu-central-1'
        self.client = self.session.create_client('s3', self.region)
        self.bucket_name = self.create_bucket(self.region)

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

        list_objs_paginator = self.client.get_paginator('list_objects')
        key_refs = []
        for response in list_objs_paginator.paginate(Bucket=self.bucket_name,
                                                     PaginationConfig={
                                                         'PageSize': 2}):
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

        list_objs_paginator = self.client.get_paginator('list_objects')
        key_refs = []
        for response in list_objs_paginator.paginate(Bucket=self.bucket_name,
                                                     PaginationConfig={
                                                         'PageSize': 2}):
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
            self.client.abort_multipart_upload,
            Bucket=self.bucket_name, Key=key, UploadId=upload_id
        )

        response = self.client.list_multipart_uploads(
            Bucket=self.bucket_name, Prefix=key
        )

        # Make sure there is only one multipart upload.
        self.assertEqual(len(response['Uploads']), 1)
        # Make sure the upload id is as expected.
        self.assertEqual(response['Uploads'][0]['UploadId'], upload_id)


class TestSSEKeyParamValidation(BaseS3ClientTest):
    def setUp(self):
        self.session = botocore.session.get_session()
        self.client = self.session.create_client('s3', 'us-west-2')
        self.bucket_name = self.create_bucket('us-west-2')

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
        bucket_name = self.create_bucket(self.region)
        body = six.BytesIO(b"Hello world!")
        response = self.client.put_object(
            Bucket=bucket_name, Key="foo.txt", Body=body,
            ContentDisposition="attachment; filename=5小時接力起跑.jpg;")
        self.assert_status_code(response, 200)
        self.addCleanup(self.client.delete_object,
                        Bucket=bucket_name, Key="foo.txt")


class TestSupportedPutObjectBodyTypes(TestS3BaseWithBucket):

    def create_client(self):
        # Even though the default signature_version is s3,
        # we're being explicit in case this ever changes.
        client_config = Config(signature_version='s3')
        return self.session.create_client('s3', self.region,
                                          config=client_config)

    def assert_can_put_object(self, body):
        client = self.create_client()
        response = client.put_object(
            Bucket=self.bucket_name, Key='foo',
            Body=body)
        self.assert_status_code(response, 200)
        self.addCleanup(client.delete_object, Bucket=self.bucket_name,
                        Key='foo')

    def test_can_put_unicode_content(self):
        self.assert_can_put_object(body=u'\u2713')

    def test_can_put_non_ascii_bytes(self):
        self.assert_can_put_object(body=u'\u2713'.encode('utf-8'))

    def test_can_put_binary_file(self):
        tempdir = self.make_tempdir()
        filename = os.path.join(tempdir, 'foo')
        with open(filename, 'wb') as f:
            f.write(u'\u2713'.encode('utf-8'))
        with open(filename, 'rb') as binary_file:
            self.assert_can_put_object(body=binary_file)

    def test_can_put_extracted_file_from_tar(self):
        tempdir = self.make_tempdir()
        tarname = os.path.join(tempdir, 'mytar.tar')
        filename = os.path.join(tempdir, 'foo')

        # Set up a file to add the tarfile.
        with open(filename, 'w') as f:
            f.write('bar')

        # Setup the tar file by adding the file to it.
        # Note there is no context handler for TarFile in python 2.6
        try:
            tar = TarFile(tarname, 'w')
            tar.add(filename, 'foo')
        finally:
            tar.close()

        # See if an extracted file can be uploaded to s3.
        try:
            tar = TarFile(tarname, 'r')
            with closing(tar.extractfile('foo')) as f:
                self.assert_can_put_object(body=f)
        finally:
            tar.close()


class TestSupportedPutObjectBodyTypesSigv4(TestSupportedPutObjectBodyTypes):
    def create_client(self):
        client_config = Config(signature_version='s3v4')
        return self.session.create_client('s3', self.region,
                                          config=client_config)


if __name__ == '__main__':
    unittest.main()
