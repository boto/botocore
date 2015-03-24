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
import mock
import copy

import botocore
import botocore.session
from botocore.hooks import first_non_none_response
from botocore.awsrequest import AWSRequest
from botocore.compat import quote, six
from botocore.model import OperationModel, ServiceModel
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

    def test_disable_signing(self):
        self.assertEqual(handlers.disable_signing(), botocore.UNSIGNED)

    def test_quote_source_header(self):
        for op in ('UploadPartCopy', 'CopyObject'):
            event = self.session.create_event(
                'before-call', 's3', op)
            params = {'headers': {'x-amz-copy-source': 'foo++bar.txt'}}
            m = mock.Mock()
            self.session.emit(event, params=params, model=m)
            self.assertEqual(
                params['headers']['x-amz-copy-source'], 'foo%2B%2Bbar.txt')

    def test_presigned_url_already_present(self):
        params = {'body': {'PresignedUrl': 'https://foo'}}
        handlers.copy_snapshot_encrypted(params, None, None)
        self.assertEqual(params['body']['PresignedUrl'], 'https://foo')

    def test_copy_snapshot_encrypted(self):
        v4query_auth = mock.Mock()

        def add_auth(request):
            request.url += '?PRESIGNED_STUFF'

        v4query_auth.add_auth = add_auth

        request_signer = mock.Mock()
        request_signer._region_name = 'us-east-1'
        request_signer.get_auth.return_value = v4query_auth

        params = {'SourceRegion': 'us-west-2'}
        endpoint = mock.Mock()
        request = AWSRequest()
        request.method = 'POST'
        request.url = 'https://ec2.us-east-1.amazonaws.com'
        request = request.prepare()
        endpoint.create_request.return_value = request

        handlers.copy_snapshot_encrypted({'body': params},
                                         request_signer,
                                         endpoint)
        self.assertEqual(params['PresignedUrl'],
                         'https://ec2.us-west-2.amazonaws.com?PRESIGNED_STUFF')
        # We should also populate the DestinationRegion with the
        # region_name of the endpoint object.
        self.assertEqual(params['DestinationRegion'], 'us-east-1')

    def test_destination_region_always_changed(self):
        # If the user provides a destination region, we will still
        # override the DesinationRegion with the region_name from
        # the endpoint object.
        actual_region = 'us-west-1'
        v4query_auth = mock.Mock()

        def add_auth(request):
            request.url += '?PRESIGNED_STUFF'

        v4query_auth.add_auth = add_auth

        request_signer = mock.Mock()
        request_signer._region_name = actual_region
        request_signer.get_auth.return_value = v4query_auth

        endpoint = mock.Mock()
        request = AWSRequest()
        request.method = 'POST'
        request.url = 'https://ec2.us-east-1.amazonaws.com'
        request = request.prepare()
        endpoint.create_request.return_value = request

        # The user provides us-east-1, but we will override this to
        # endpoint.region_name, of 'us-west-1' in this case.
        params = {'SourceRegion': 'us-west-2', 'DestinationRegion': 'us-east-1'}
        handlers.copy_snapshot_encrypted({'body': params},
                                         request_signer,
                                         endpoint)
        # Always use the DestinationRegion from the endpoint, regardless of
        # whatever value the user provides.
        self.assertEqual(params['DestinationRegion'], actual_region)

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

    def test_sse_params(self):
        for op in ('HeadObject', 'GetObject', 'PutObject', 'CopyObject',
                   'CreateMultipartUpload', 'UploadPart', 'UploadPartCopy'):
            event = self.session.create_event(
                'before-parameter-build', 's3', op)
            params = {'SSECustomerKey': b'bar',
                      'SSECustomerAlgorithm': 'AES256'}
            self.session.emit(event, params=params, model=mock.Mock())
            self.assertEqual(params['SSECustomerKey'], 'YmFy')
            self.assertEqual(params['SSECustomerKeyMD5'],
                             'N7UdGUp1E+RbVvZSTy1R8g==')

    def test_sse_params_as_str(self):
        event = self.session.create_event(
            'before-parameter-build', 's3', 'PutObject')
        params = {'SSECustomerKey': 'bar',
                  'SSECustomerAlgorithm': 'AES256'}
        self.session.emit(event, params=params, model=mock.Mock())
        self.assertEqual(params['SSECustomerKey'], 'YmFy')
        self.assertEqual(params['SSECustomerKeyMD5'],
                            'N7UdGUp1E+RbVvZSTy1R8g==')

    def test_route53_resource_id(self):
        event = self.session.create_event(
            'before-parameter-build', 'route53', 'GetHostedZone')
        params = {'Id': '/hostedzone/ABC123',
                  'HostedZoneId': '/hostedzone/ABC123',
                  'ResourceId': '/hostedzone/DEF456',
                  'DelegationSetId': '/hostedzone/GHI789',
                  'Other': '/hostedzone/foo'}
        operation_def = {
            'name': 'GetHostedZone',
            'input': {
                'shape': 'GetHostedZoneInput'
            }
        }
        service_def = {
            'metadata': {},
            'shapes': {
                'GetHostedZoneInput': {
                    'type': 'structure',
                    'members': {
                        'Id': {
                            'shape': 'ResourceId'
                        },
                        'HostedZoneId': {
                            'shape': 'ResourceId'
                        },
                        'ResourceId': {
                            'shape': 'ResourceId'
                        },
                        'DelegationSetId': {
                            'shape': 'DelegationSetId'
                        },
                        'Other': {
                            'shape': 'String'
                        }
                    }
                },
                'ResourceId': {
                    'type': 'string'
                },
                'DelegationSetId': {
                    'type': 'string'
                },
                'String': {
                    'type': 'string'
                }
            }
        }
        model = OperationModel(operation_def, ServiceModel(service_def))
        self.session.emit(event, params=params, model=model)

        self.assertEqual(params['Id'], 'ABC123')
        self.assertEqual(params['HostedZoneId'], 'ABC123')
        self.assertEqual(params['ResourceId'], 'DEF456')
        self.assertEqual(params['DelegationSetId'], 'GHI789')

        # This one should have been left alone
        self.assertEqual(params['Other'], '/hostedzone/foo')

    def test_route53_resource_id_missing_input_shape(self):
        event = self.session.create_event(
            'before-parameter-build', 'route53', 'GetHostedZone')
        params = {'HostedZoneId': '/hostedzone/ABC123',}
        operation_def = {
            'name': 'GetHostedZone'
        }
        service_def = {
            'metadata': {},
            'shapes': {}
        }
        model = OperationModel(operation_def, ServiceModel(service_def))
        self.session.emit(event, params=params, model=model)

        self.assertEqual(params['HostedZoneId'], '/hostedzone/ABC123')

    def test_run_instances_userdata(self):
        user_data = 'This is a test'
        b64_user_data = base64.b64encode(six.b(user_data)).decode('utf-8')
        event = self.session.create_event(
            'before-parameter-build', 'ec2', 'RunInstances')
        params = dict(ImageId='img-12345678',
                      MinCount=1, MaxCount=5, UserData=user_data)
        self.session.emit(event, params=params)
        result = {'ImageId': 'img-12345678',
                  'MinCount': 1,
                  'MaxCount': 5,
                  'UserData': b64_user_data}
        self.assertEqual(params, result)

    def test_run_instances_userdata_blob(self):
        # Ensure that binary can be passed in as user data.
        # This is valid because you can send gzip compressed files as
        # user data.
        user_data = b'\xc7\xa9This is a test'
        b64_user_data = base64.b64encode(user_data).decode('utf-8')
        event = self.session.create_event(
            'before-parameter-build', 'ec2', 'RunInstances')
        params = dict(ImageId='img-12345678',
                      MinCount=1, MaxCount=5, UserData=user_data)
        self.session.emit(event, params=params)
        result = {'ImageId': 'img-12345678',
                  'MinCount': 1,
                  'MaxCount': 5,
                  'UserData': b64_user_data}
        self.assertEqual(params, result)

    def test_fix_s3_host_initial(self):
        request = AWSRequest(
            method='PUT',headers={},
            url='https://s3-us-west-2.amazonaws.com/bucket/key.txt'
        )
        region_name = 'us-west-2'
        signature_version = 's3'
        handlers.fix_s3_host(
            request=request, signature_version=signature_version,
            region_name=region_name)
        self.assertEqual(request.url, 'https://bucket.s3.amazonaws.com/key.txt')
        self.assertEqual(request.auth_path, '/bucket/key.txt')

    def test_fix_s3_host_only_applied_once(self):
        request = AWSRequest(
            method='PUT',headers={},
            url='https://s3-us-west-2.amazonaws.com/bucket/key.txt'
        )
        region_name = 'us-west-2'
        signature_version = 's3'
        handlers.fix_s3_host(
            request=request, signature_version=signature_version,
            region_name=region_name)
        # Calling the handler again should not affect the end result:
        handlers.fix_s3_host(
            request=request, signature_version=signature_version,
            region_name=region_name)
        self.assertEqual(request.url, 'https://bucket.s3.amazonaws.com/key.txt')
        # This was a bug previously.  We want to make sure that
        # calling fix_s3_host() again does not alter the auth_path.
        # Otherwise we'll get signature errors.
        self.assertEqual(request.auth_path, '/bucket/key.txt')

    def test_register_retry_for_handlers_with_no_endpoint_prefix(self):
        no_endpoint_prefix = {'metadata': {}}
        session = mock.Mock()
        handlers.register_retries_for_service(service_data=no_endpoint_prefix,
                                              session=mock.Mock(),
                                              service_name='foo')
        self.assertFalse(session.register.called)

    def test_register_retry_handlers(self):
        service_data = {
            'metadata': {'endpointPrefix': 'foo'},
        }
        session = mock.Mock()
        loader = mock.Mock()
        session.get_component.return_value = loader
        loader.load_data.return_value = {
            'retry': {
                '__default__': {
                    'max_attempts': 10,
                    'delay': {
                        'type': 'exponential',
                        'base': 2,
                        'growth_factor': 5,
                    },
                },
            },
        }
        handlers.register_retries_for_service(service_data=service_data,
                                              session=session,
                                              service_name='foo')
        session.register.assert_called_with('needs-retry.foo', mock.ANY,
                                            unique_id='retry-config-foo')

    def test_dns_style_not_used_for_get_bucket_location(self):
        original_url = 'https://s3-us-west-2.amazonaws.com/bucket?location'
        request = AWSRequest(
            method='GET',headers={},
            url=original_url,
        )
        signature_version = 's3'
        region_name = 'us-west-2'
        handlers.fix_s3_host(
            request=request, signature_version=signature_version,
            region_name=region_name)
        # The request url should not have been modified because this is
        # a request for GetBucketLocation.
        self.assertEqual(request.url, original_url)

    def test_get_template_has_error_response(self):
        original = {'Error': {'Code': 'Message'}}
        handler_input = copy.deepcopy(original)
        handlers.json_decode_template_body(parsed=handler_input)
        # The handler should not have changed the response because it's
        # an error response.
        self.assertEqual(original, handler_input)

    def test_decode_json_policy(self):
        parsed = {
            'Document': '{"foo": "foobarbaz"}',
            'Other': 'bar',
        }
        service_def = {
            'operations': {
                'Foo': {
                    'output': {'shape': 'PolicyOutput'},
                }
            },
            'shapes': {
                'PolicyOutput': {
                    'type': 'structure',
                    'members': {
                        'Document': {
                            'shape': 'policyDocumentType'
                        },
                        'Other': {
                            'shape': 'stringType'
                        }
                    }
                },
                'policyDocumentType': {
                    'type': 'string'
                },
                'stringType': {
                    'type': 'string'
                },
            }
        }
        model = ServiceModel(service_def)
        op_model = model.operation_model('Foo')
        handlers.json_decode_policies(parsed, op_model)
        self.assertEqual(parsed['Document'], {'foo': 'foobarbaz'})

        no_document = {'Other': 'bar'}
        handlers.json_decode_policies(no_document, op_model)
        self.assertEqual(no_document, {'Other': 'bar'})

    def test_inject_account_id(self):
        params = {}
        handlers.inject_account_id(params)
        self.assertEqual(params['accountId'], '-')

    def test_account_id_not_added_if_present(self):
        params = {'accountId': 'foo'}
        handlers.inject_account_id(params)
        self.assertEqual(params['accountId'], 'foo')

    def test_glacier_version_header_added(self):
        request_dict = {
            'headers': {}
        }
        model = ServiceModel({'metadata': {'apiVersion': '2012-01-01'}})
        handlers.add_glacier_version(model, request_dict)
        self.assertEqual(request_dict['headers']['x-amz-glacier-version'],
                         '2012-01-01')

    def test_glacier_checksums_added(self):
        request_dict = {
            'headers': {},
            'body': six.BytesIO(b'hello world'),
        }
        handlers.add_glacier_checksums(request_dict)
        self.assertIn('x-amz-content-sha256', request_dict['headers'])
        self.assertIn('x-amz-sha256-tree-hash', request_dict['headers'])
        self.assertEqual(
            request_dict['headers']['x-amz-content-sha256'],
            'b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9')
        self.assertEqual(
            request_dict['headers']['x-amz-sha256-tree-hash'],
            'b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9')
        # And verify that the body can still be read.
        self.assertEqual(request_dict['body'].read(), b'hello world')

    def test_tree_hash_added_only_if_not_exists(self):
        request_dict = {
            'headers': {
                'x-amz-sha256-tree-hash': 'pre-exists',
            },
            'body': six.BytesIO(b'hello world'),
        }
        handlers.add_glacier_checksums(request_dict)
        self.assertEqual(request_dict['headers']['x-amz-sha256-tree-hash'],
                         'pre-exists')

    def test_checksum_added_only_if_not_exists(self):
        request_dict = {
            'headers': {
                'x-amz-content-sha256': 'pre-exists',
            },
            'body': six.BytesIO(b'hello world'),
        }
        handlers.add_glacier_checksums(request_dict)
        self.assertEqual(request_dict['headers']['x-amz-content-sha256'],
                         'pre-exists')

    def test_glacier_checksums_support_raw_bytes(self):
        request_dict = {
            'headers': {},
            'body': b'hello world',
        }
        handlers.add_glacier_checksums(request_dict)
        self.assertEqual(
            request_dict['headers']['x-amz-content-sha256'],
            'b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9')
        self.assertEqual(
            request_dict['headers']['x-amz-sha256-tree-hash'],
            'b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9')


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
        service_model = self.session.get_service_model('s3')
        operation = service_model.operation_model('CopyObject')
        responses = self.session.emit(
            'needs-retry.s3.CopyObject',
            response=(mock.Mock(), mock.Mock()), endpoint=mock.Mock(),
            operation=operation, attempts=1, caught_exception=None)
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


if __name__ == '__main__':
    unittest.main()
