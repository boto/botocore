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

"""Builtin event handlers.

This module contains builtin handlers for events emitted by botocore.
"""

import base64
import hashlib
import logging
import re
import xml.etree.cElementTree

import six

from botocore.compat import urlsplit, urlunsplit, unquote, json, quote
from botocore import retryhandler
from botocore import translate
import botocore.auth


logger = logging.getLogger(__name__)
LABEL_RE = re.compile('[a-z0-9][a-z0-9\-]*[a-z0-9]')
RESTRICTED_REGIONS = [
    'us-gov-west-1',
    'fips-us-gov-west-1',
]
REGISTER_FIRST = object()
REGISTER_LAST = object()



def check_for_200_error(response, **kwargs):
    # From: http://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectCOPY.html
    # There are two opportunities for a copy request to return an error. One
    # can occur when Amazon S3 receives the copy request and the other can
    # occur while Amazon S3 is copying the files. If the error occurs before
    # the copy operation starts, you receive a standard Amazon S3 error. If the
    # error occurs during the copy operation, the error response is embedded in
    # the 200 OK response. This means that a 200 OK response can contain either
    # a success or an error. Make sure to design your application to parse the
    # contents of the response and handle it appropriately.
    #
    # So this handler checks for this case.  Even though the server sends a
    # 200 response, conceptually this should be handled exactly like a
    # 500 response (with respect to raising exceptions, retries, etc.)
    # We're connected *before* all the other retry logic handlers, so as long
    # as we switch the error code to 500, we'll retry the error as expected.
    if response is None:
        # A None response can happen if an exception is raised while
        # trying to retrieve the response.  See Endpoint._get_response().
        return
    http_response, parsed = response
    if _looks_like_special_case_error(http_response):
        logger.debug("Error found for response with 200 status code, "
                        "errors: %s, changing status code to "
                        "500.", parsed)
        http_response.status_code = 500


def _looks_like_special_case_error(http_response):
    if http_response.status_code == 200:
        parser = xml.etree.cElementTree.XMLParser(
            target=xml.etree.cElementTree.TreeBuilder(),
            encoding='utf-8')
        parser.feed(http_response.content)
        root = parser.close()
        if root.tag == 'Error':
            return True
    return False


def decode_console_output(parsed, **kwargs):
    try:
        value = base64.b64decode(six.b(parsed['Output'])).decode('utf-8')
        parsed['Output'] = value
    except (ValueError, TypeError, AttributeError):
        logger.debug('Error decoding base64', exc_info=True)


def decode_quoted_jsondoc(value):
    try:
        value = json.loads(unquote(value))
    except (ValueError, TypeError):
        logger.debug('Error loading quoted JSON', exc_info=True)
    return value


def json_decode_template_body(parsed, **kwargs):
    try:
        value = json.loads(parsed['TemplateBody'])
        parsed['TemplateBody'] = value
    except (ValueError, TypeError):
        logger.debug('error loading JSON', exc_info=True)


def calculate_md5(params, **kwargs):
    request_dict = params
    if request_dict['body'] and not 'Content-MD5' in params['headers']:
        md5 = hashlib.md5()
        md5.update(six.b(params['body']))
        value = base64.b64encode(md5.digest()).decode('utf-8')
        params['headers']['Content-MD5'] = value


def sse_md5(params, **kwargs):
    """
    S3 server-side encryption requires the encryption key to be sent to the
    server base64 encoded, as well as a base64-encoded MD5 hash of the
    encryption key. This handler does both if the MD5 has not been set by
    the caller.
    """
    prefix = 'x-amz-server-side-encryption-customer-'
    key = prefix + 'key'
    key_md5 = prefix + 'key-MD5'
    if key in params['headers'] and not key_md5 in params['headers']:
        original = six.b(params['headers'][key])
        md5 = hashlib.md5()
        md5.update(original)
        value = base64.b64encode(md5.digest()).decode('utf-8')
        params['headers'][key] = base64.b64encode(original).decode('utf-8')
        params['headers'][key_md5] = value


def check_dns_name(bucket_name):
    """
    Check to see if the ``bucket_name`` complies with the
    restricted DNS naming conventions necessary to allow
    access via virtual-hosting style.

    Even though "." characters are perfectly valid in this DNS
    naming scheme, we are going to punt on any name containing a
    "." character because these will cause SSL cert validation
    problems if we try to use virtual-hosting style addressing.
    """
    if '.' in bucket_name:
        return False
    n = len(bucket_name)
    if n < 3 or n > 63:
        # Wrong length
        return False
    if n == 1:
        if not bucket_name.isalnum():
            return False
    match = LABEL_RE.match(bucket_name)
    if match is None or match.end() != len(bucket_name):
        return False
    return True


def fix_s3_host(event_name, endpoint, request, auth, **kwargs):
    """
    This handler looks at S3 requests just before they are signed.
    If there is a bucket name on the path (true for everything except
    ListAllBuckets) it checks to see if that bucket name conforms to
    the DNS naming conventions.  If it does, it alters the request to
    use ``virtual hosting`` style addressing rather than ``path-style``
    addressing.  This allows us to avoid 301 redirects for all
    bucket names that can be CNAME'd.
    """
    if auth.auth_path is not None:
        # The auth_path has already been applied (this may be a
        # retried request).  We don't need to perform this
        # customization again.
        return
    parts = urlsplit(request.url)
    auth.auth_path = parts.path
    path_parts = parts.path.split('/')
    if isinstance(auth, botocore.auth.SigV4Auth):
        return
    if len(path_parts) > 1:
        bucket_name = path_parts[1]
        logger.debug('Checking for DNS compatible bucket for: %s',
                     request.url)
        if check_dns_name(bucket_name) and _allowed_region(endpoint.region_name):
            # If the operation is on a bucket, the auth_path must be
            # terminated with a '/' character.
            if len(path_parts) == 2:
                if auth.auth_path[-1] != '/':
                    auth.auth_path += '/'
            path_parts.remove(bucket_name)
            global_endpoint = 's3.amazonaws.com'
            host = bucket_name + '.' + global_endpoint
            new_tuple = (parts.scheme, host, '/'.join(path_parts),
                         parts.query, '')
            new_uri = urlunsplit(new_tuple)
            request.url = new_uri
            logger.debug('URI updated to: %s', new_uri)
        else:
            logger.debug('Not changing URI, bucket is not DNS compatible: %s',
                         bucket_name)


def _allowed_region(region_name):
    return region_name not in RESTRICTED_REGIONS


def register_retries_for_service(service, **kwargs):
    loader = service.session.get_component('data_loader')
    config = _load_retry_config(loader, service.endpoint_prefix)
    if not config:
        return
    logger.debug("Registering retry handlers for service: %s", service)
    session = service.session
    handler = retryhandler.create_retry_handler(
        config, service.endpoint_prefix)
    unique_id = 'retry-config-%s' % service.endpoint_prefix
    session.register('needs-retry.%s' % service.endpoint_prefix,
                     handler, unique_id=unique_id)
    _register_for_operations(config, session,
                             service_name=service.endpoint_prefix)


def _load_retry_config(loader, endpoint_prefix):
    original_config = loader.load_data('aws/_retry')
    retry_config = translate.build_retry_config(
        endpoint_prefix, original_config['retry'],
        original_config['definitions'])
    # TODO: I think I'm missing error conditions here.
    return retry_config


def _register_for_operations(config, session, service_name):
    # There's certainly a tradeoff for registering the retry config
    # for the operations when the service is created.  In practice,
    # there aren't a whole lot of per operation retry configs so
    # this is ok for now.
    for key in config:
        if key == '__default__':
            continue
        handler = retryhandler.create_retry_handler(config, key)
        unique_id = 'retry-config-%s-%s' % (service_name, key)
        session.register('needs-retry.%s.%s' % (service_name, key),
                         handler, unique_id=unique_id)


def signature_overrides(service_data, service_name, session, **kwargs):
    scoped_config = session.get_scoped_config()
    service_config = scoped_config.get(service_name)
    if service_config is None or not isinstance(service_config, dict):
        return
    signature_version_override = service_config.get('signature_version')
    if signature_version_override is not None:
        logger.debug("Switching signature version for service %s "
                     "to version %s based on config file override.",
                     service_name, signature_version_override)
        service_data['signature_version'] = signature_version_override


def add_expect_header(model, params, **kwargs):
    if model.http.get('method', '') not in ['PUT', 'POST']:
        return
    if 'body' in params:
        body = params['body']
        if hasattr(body, 'read'):
            # Any file like object will use an expect 100-continue
            # header regardless of size.
            logger.debug("Adding expect 100 continue header to request.")
            params['headers']['Expect'] = '100-continue'


def quote_source_header(params, **kwargs):
    if params['headers'] and 'x-amz-copy-source' in params['headers']:
        value = params['headers']['x-amz-copy-source']
        params['headers']['x-amz-copy-source'] = quote(
            value.encode('utf-8'), '/~')


def copy_snapshot_encrypted(operation, params, endpoint, **kwargs):
    # The presigned URL that facilities copying an encrypted snapshot.
    # If the user does not provide this value, we will automatically
    # calculate on behalf of the user and inject the PresignedUrl
    # into the requests.
    # The params sent in the event don't quite sync up 100% so we're
    # renaming them here until they can be updated in the event.
    request_dict = params
    params = request_dict['body']
    if 'PresignedUrl' in params:
        # If the customer provided this value, then there's nothing for
        # us to do.
        return
    params['DestinationRegion'] = endpoint.region_name
    # The request will be sent to the destination region, so we need
    # to create an endpoint to the source region and create a presigned
    # url based on the source endpoint.
    region = params['SourceRegion']
    source_endpoint = operation.service.get_endpoint(region)
    presigner = botocore.auth.SigV4QueryAuth(
        credentials=source_endpoint.auth.credentials,
        region_name=region,
        service_name='ec2',
        expires=60 * 60)
    signed_request = source_endpoint.create_request(request_dict, presigner)
    params['PresignedUrl'] = signed_request.url


def json_decode_policies(parsed, model, **kwargs):
    # Any time an IAM operation returns a policy document
    # it is a string that is json that has been urlencoded,
    # i.e urlencode(json.dumps(policy_document)).
    # To give users something more useful, we will urldecode
    # this value and json.loads() the result so that they have
    # the policy document as a dictionary.
    output_shape = model.output_shape
    if output_shape is not None:
        _decode_policy_types(parsed, model.output_shape)


def _decode_policy_types(parsed, shape):
    # IAM consistently uses the policyDocumentType shape to indicate
    # strings that have policy documents.
    shape_name = 'policyDocumentType'
    if shape.type_name == 'structure':
        for member_name, member_shape in shape.members.items():
            if member_shape.type_name == 'string' and \
                    member_shape.name == shape_name:
                parsed[member_name] = decode_quoted_jsondoc(parsed[member_name])
            elif member_name in parsed:
                _decode_policy_types(parsed[member_name], member_shape)
    if shape.type_name == 'list':
        shape_member = shape.member
        for item in parsed:
            _decode_policy_types(item, shape_member)


def parse_get_bucket_location(parsed, http_response, **kwargs):
    # s3.GetBucketLocation cannot be modeled properly.  To
    # account for this we just manually parse the XML document.
    # The "parsed" passed in only has the ResponseMetadata
    # filled out.  This handler will fill in the LocationConstraint
    # value.
    response_body = http_response.content
    parser = xml.etree.cElementTree.XMLParser(
        target=xml.etree.cElementTree.TreeBuilder(),
        encoding='utf-8')
    parser.feed(response_body)
    root = parser.close()
    region = root.text
    parsed['LocationConstraint'] = region


def base64_encode_user_data(params, **kwargs):
    if 'UserData' in params:
        params['UserData'] = base64.b64encode(
            params['UserData'].encode('utf-8')).decode('utf-8')


# This is a list of (event_name, handler).
# When a Session is created, everything in this list will be
# automatically registered with that Session.

BUILTIN_HANDLERS = [
    ('after-call.iam', json_decode_policies),

    ('after-call.ec2.GetConsoleOutput', decode_console_output),
    ('after-call.cloudformation.GetTemplate', json_decode_template_body),
    ('after-call.s3.GetBucketLocation', parse_get_bucket_location),

    ('before-call.s3.PutBucketTagging', calculate_md5),
    ('before-call.s3.PutBucketLifecycle', calculate_md5),
    ('before-call.s3.PutBucketCors', calculate_md5),
    ('before-call.s3.DeleteObjects', calculate_md5),
    ('before-call.s3.UploadPartCopy', quote_source_header),
    ('before-call.s3.CopyObject', quote_source_header),
    ('before-call.s3', add_expect_header),
    ('before-call.ec2.CopySnapshot', copy_snapshot_encrypted),
    ('before-auth.s3', fix_s3_host),
    ('needs-retry.s3.UploadPartCopy', check_for_200_error, REGISTER_FIRST),
    ('needs-retry.s3.CopyObject', check_for_200_error, REGISTER_FIRST),
    ('needs-retry.s3.CompleteMultipartUpload', check_for_200_error,
     REGISTER_FIRST),
    ('service-created', register_retries_for_service),
    ('service-data-loaded', signature_overrides),
    ('before-call.s3.HeadObject', sse_md5),
    ('before-call.s3.GetObject', sse_md5),
    ('before-call.s3.PutObject', sse_md5),
    ('before-call.s3.CopyObject', sse_md5),
    ('before-call.s3.CreateMultipartUpload', sse_md5),
    ('before-call.s3.UploadPart', sse_md5),
    ('before-call.s3.UploadPartCopy', sse_md5),
    ('before-parameter-build.ec2.RunInstances', base64_encode_user_data),
    ('before-parameter-build.autoscaling.CreateLaunchConfiguration',
     base64_encode_user_data),
]
