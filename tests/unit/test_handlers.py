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

from tests import BaseSessionTest

import base64
import six
import mock

import botocore.session
from botocore.awsrequest import AWSRequest
from botocore.hooks import first_non_none_response
from botocore.auth import BaseSigner
from botocore.compat import quote
from botocore import handlers


class TestHandlers(BaseSessionTest):

    def test_get_console_output(self):
        parsed = {'Output': base64.b64encode(b'foobar').decode('utf-8')}
        handlers.decode_console_output(parsed)
        self.assertEqual(parsed['Output'], 'foobar')

    def test_get_console_output_cant_be_decoded(self):
        parsed = {'Output': 1}
        handlers.decode_console_output(parsed)
        self.assertEqual(parsed['Output'], 1)

    def test_decode_quoted_jsondoc(self):
        value = quote('{"foo":"bar"}')
        converted_value = handlers.decode_quoted_jsondoc(value)
        self.assertEqual(converted_value, {'foo': 'bar'})

    def test_cant_decode_quoted_jsondoc(self):
        value = quote('{"foo": "missing end quote}')
        converted_value = handlers.decode_quoted_jsondoc(value)
        self.assertEqual(converted_value, value)

    def test_switch_to_sigv4(self):
        event = self.session.create_event('service-data-loaded', 's3')
        mock_session = mock.Mock()
        mock_session.get_scoped_config.return_value = {
            's3': {'signature_version': 's3v4'}
        }
        kwargs = {'service_data': {'signature_version': 's3'},
                  'service_name': 's3', 'session': mock_session}
        self.session.emit(event, **kwargs)
        self.assertEqual(kwargs['service_data']['signature_version'], 's3v4')

    def test_noswitch_to_sigv4(self):
        event = self.session.create_event('service-data-loaded', 's3')
        mock_session = mock.Mock()
        mock_session.get_scoped_config.return_value = {}
        kwargs = {'service_data': {'signature_version': 's3'},
                  'service_name': 's3', 'session': mock_session}
        self.session.emit(event, **kwargs)
        self.assertEqual(kwargs['service_data']['signature_version'], 's3')

    def test_quote_source_header(self):
        for op in ('UploadPartCopy', 'CopyObject'):
            event = self.session.create_event(
                'before-call', 's3', op)
            params = {'headers': {'x-amz-copy-source': 'foo++bar.txt'}}
            m = mock.Mock()
            self.session.emit(event, params=params, model=m)
            self.assertEqual(
                params['headers']['x-amz-copy-source'], 'foo%2B%2Bbar.txt')

    def test_copy_snapshot_encrypted(self):
        operation = mock.Mock()
        source_endpoint = mock.Mock()
        signed_request = mock.Mock()
        signed_request.url = 'SIGNED_REQUEST'
        source_endpoint.auth.credentials = mock.sentinel.credentials
        source_endpoint.create_request.return_value = signed_request
        operation.service.get_endpoint.return_value = source_endpoint
        endpoint = mock.Mock()
        endpoint.region_name = 'us-east-1'

        params = {'SourceRegion': 'us-west-2'}
        handlers.copy_snapshot_encrypted(operation, {'body': params}, endpoint)
        self.assertEqual(params['PresignedUrl'], 'SIGNED_REQUEST')
        # We created an endpoint in the source region.
        operation.service.get_endpoint.assert_called_with('us-west-2')
        # We should also populate the DestinationRegion with the
        # region_name of the endpoint object.
        self.assertEqual(params['DestinationRegion'], 'us-east-1')

    def test_destination_region_left_untouched(self):
        # If the user provides a destination region, we will still
        # override the DesinationRegion with the region_name from
        # the endpoint object.
        operation = mock.Mock()
        source_endpoint = mock.Mock()
        signed_request = mock.Mock()
        signed_request.url = 'SIGNED_REQUEST'
        source_endpoint.auth.credentials = mock.sentinel.credentials
        source_endpoint.create_request.return_value = signed_request
        operation.service.get_endpoint.return_value = source_endpoint
        endpoint = mock.Mock()
        endpoint.region_name = 'us-west-1'

        # The user provides us-east-1, but we will override this to
        # endpoint.region_name, of 'us-west-1' in this case.
        params = {'SourceRegion': 'us-west-2', 'DestinationRegion': 'us-east-1'}
        handlers.copy_snapshot_encrypted(operation, {'body': params}, endpoint)
        # Always use the DestinationRegion from the endpoint, regardless of
        # whatever value the user provides.
        self.assertEqual(params['DestinationRegion'], 'us-west-1')

    def test_500_status_code_set_for_200_response(self):
        http_response = mock.Mock()
        http_response.status_code = 200
        http_response.content = """
            <Error>
              <Code>AccessDenied</Code>
              <Message>Access Denied</Message>
              <RequestId>id</RequestId>
              <HostId>hostid</HostId>
            </Error>
        """
        handlers.check_for_200_error((http_response, {}))
        self.assertEqual(http_response.status_code, 500)

    def test_200_response_with_no_error_left_untouched(self):
        http_response = mock.Mock()
        http_response.status_code = 200
        http_response.content = "<NotAnError></NotAnError>"
        handlers.check_for_200_error((http_response, {}))
        # We don't touch the status code since there are no errors present.
        self.assertEqual(http_response.status_code, 200)

    def test_500_response_can_be_none(self):
        # A 500 response can raise an exception, which means the response
        # object is None.  We need to handle this case.
        handlers.check_for_200_error(None)

    def test_sse_headers(self):
        prefix = 'x-amz-server-side-encryption-customer-'
        for op in ('HeadObject', 'GetObject', 'PutObject', 'CopyObject',
                   'CreateMultipartUpload', 'UploadPart', 'UploadPartCopy'):
            event = self.session.create_event(
                'before-call', 's3', op)
            params = {'headers': {
                prefix + 'algorithm': 'foo',
                prefix + 'key': 'bar'
                }}
            self.session.emit(event, params=params, model=mock.Mock())
            self.assertEqual(
                params['headers'][prefix + 'key'], 'YmFy')
            self.assertEqual(
                params['headers'][prefix + 'key-MD5'],
                'N7UdGUp1E+RbVvZSTy1R8g==')

    def test_fix_s3_host_initial(self):
        endpoint = mock.Mock(region_name='us-west-2')
        request = AWSRequest(
            method='PUT',headers={},
            url='https://s3-us-west-2.amazonaws.com/bucket/key.txt'
        )
        auth = mock.Mock()
        auth.auth_path = None
        handlers.fix_s3_host('foo', endpoint, request, auth)
        self.assertEqual(request.url, 'https://bucket.s3.amazonaws.com/key.txt')
        self.assertEqual(auth.auth_path, '/bucket/key.txt')

    def test_fix_s3_host_only_applied_once(self):
        endpoint = mock.Mock(region_name='us-west-2')
        request = AWSRequest(
            method='PUT',headers={},
            url='https://s3-us-west-2.amazonaws.com/bucket/key.txt'
        )
        auth = mock.Mock()
        auth.auth_path = None
        handlers.fix_s3_host('foo', endpoint, request, auth)
        # Calling the handler again should not affect the end result:
        handlers.fix_s3_host('foo', endpoint, request, auth)
        self.assertEqual(request.url, 'https://bucket.s3.amazonaws.com/key.txt')
        # This was a bug previously.  We want to make sure that
        # calling fix_s3_host() again does not alter the auth_path.
        # Otherwise we'll get signature errors.
        self.assertEqual(auth.auth_path, '/bucket/key.txt')


class TestRetryHandlerOrder(BaseSessionTest):
    def get_handler_names(self, responses):
        names = []
        for response in responses:
            handler = response[0]
            if hasattr(handler, '__name__'):
                names.append(handler.__name__)
            elif hasattr(handler, '__class__'):
                names.append(handler.__class__.__name__)
            else:
                names.append(str(handler))
        return names

    def test_s3_special_case_is_before_other_retry(self):
        service = self.session.get_service('s3')
        operation = service.get_operation('CopyObject')
        responses = self.session.emit(
            'needs-retry.s3.CopyObject',
            response=(mock.Mock(), mock.Mock()), endpoint=mock.Mock(), operation=operation,
            attempts=1, caught_exception=None)
        # This is implementation specific, but we're trying to verify that
        # the check_for_200_error is before any of the retry logic in
        # botocore.retryhandlers.
        # Technically, as long as the relative order is preserved, we don't
        # care about the absolute order.
        names = self.get_handler_names(responses)
        self.assertIn('check_for_200_error', names)
        self.assertIn('RetryHandler', names)
        s3_200_handler = names.index('check_for_200_error')
        general_retry_handler = names.index('RetryHandler')
        self.assertTrue(s3_200_handler < general_retry_handler,
                        "S3 200 error handler was supposed to be before "
                        "the general retry handler, but it was not.")
