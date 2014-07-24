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
import logging
import time
import threading

from botocore.vendored.requests.sessions import Session
from botocore.vendored.requests.utils import get_environ_proxies
import six

import botocore.response
import botocore.exceptions
from botocore.auth import AUTH_TYPE_MAPS
from botocore.exceptions import UnknownSignatureVersionError
from botocore.awsrequest import AWSRequest
from botocore.compat import urljoin, json, quote


logger = logging.getLogger(__name__)
DEFAULT_TIMEOUT = 60

class Endpoint(object):
    """
    Represents an endpoint for a particular service in a specific
    region.  Only an endpoint can make requests.

    :ivar service: The Service object that describes this endpoints
        service.
    :ivar host: The fully qualified endpoint hostname.
    :ivar session: The session object.
    """

    def __init__(self, service, region_name, host, auth, proxies=None,
                 verify=True, timeout=DEFAULT_TIMEOUT):
        self.service = service
        self.session = self.service.session
        self.region_name = region_name
        self.host = host
        self.verify = verify
        self.auth = auth
        if proxies is None:
            proxies = {}
        self.proxies = proxies
        self.http_session = Session()
        self.timeout = timeout
        self._lock = threading.Lock()

    def __repr__(self):
        return '%s(%s)' % (self.service.endpoint_prefix, self.host)

    def make_request(self, operation, params):
        logger.debug("Making request for %s (verify_ssl=%s) with params: %s",
                     operation, self.verify, params)
        prepared_request = self.create_request(operation, params)
        return self._send_request(prepared_request, operation)

    def create_request(self, operation, params, signer=None):
        # To decide if we need to do auth or not we check the
        # signature_version attribute on both the service and
        # the operation are not None and we make sure there is an
        # auth class associated with the endpoint.
        # If any of these are not true, we skip auth.
        if signer is not None:
            # If the user explicitly specifies a signer, then we will sign
            # the request.
            signer = signer
        else:
            do_auth = (getattr(self.service, 'signature_version', None) and
                    getattr(operation, 'signature_version', True) and
                    self.auth)
            if do_auth:
                signer = self.auth
            else:
                # If we're not suppose to sign the request, then we set the signer
                # to None.
                signer = None
        request = self._create_request_object(operation, params)
        prepared_request = self.prepare_request(request, signer)
        return prepared_request

    def _create_request_object(self, operation, params):
        raise NotImplementedError('_create_request_object')

    def prepare_request(self, request, signer):
        if signer is not None:
            with self._lock:
                # Parts of the auth signing code aren't thread safe (things
                # that manipulate .auth_path), so we're using a lock here to
                # prevent race conditions.
                event = self.session.create_event(
                    'before-auth', self.service.endpoint_prefix)
                self.session.emit(event, endpoint=self,
                                  request=request, auth=signer)
                signer.add_auth(request=request)
        prepared_request = request.prepare()
        return prepared_request

    def _send_request(self, request, operation):
        attempts = 1
        response, exception = self._get_response(request, operation, attempts)
        while self._needs_retry(attempts, operation, response, exception):
            attempts += 1
            # If there is a stream associated with the request, we need
            # to reset it before attempting to send the request again.
            # This will ensure that we resend the entire contents of the
            # body.
            request.reset_stream()
            response, exception = self._get_response(request, operation,
                                                     attempts)
        return response

    def _get_response(self, request, operation, attempts):
        try:
            logger.debug("Sending http request: %s", request)
            http_response = self.http_session.send(
                request, verify=self.verify,
                stream=operation.is_streaming(),
                proxies=self.proxies, timeout=self.timeout)
        except Exception as e:
            logger.debug("Exception received when sending HTTP request.",
                         exc_info=True)
            return (None, e)
        # This returns the http_response and the parsed_data.
        return (botocore.response.get_response(self.session, operation,
                                               http_response), None)

    def _needs_retry(self, attempts, operation, response=None,
                     caught_exception=None):
        event = self.session.create_event(
            'needs-retry', self.service.endpoint_prefix, operation.name)
        handler_response = self.session.emit_first_non_none_response(
            event, response=response, endpoint=self,
            operation=operation, attempts=attempts,
            caught_exception=caught_exception)
        if handler_response is None:
            return False
        else:
            # Request needs to be retried, and we need to sleep
            # for the specified number of times.
            logger.debug("Response received to retry, sleeping for "
                         "%s seconds", handler_response)
            time.sleep(handler_response)
            return True


class QueryEndpoint(Endpoint):
    """
    This class handles only AWS/Query style services.
    """

    def _create_request_object(self, operation, params):
        params['Action'] = operation.name
        params['Version'] = self.service.api_version
        user_agent = self.session.user_agent()
        request = AWSRequest(method='POST', url=self.host,
                             data=params, headers={'User-Agent': user_agent})
        return request


class JSONEndpoint(Endpoint):
    """
    This class handles only AWS/JSON style services.
    """

    ResponseContentTypes = ['application/x-amz-json-1.1',
                            'application/json']

    def _create_request_object(self, operation, params):
        user_agent = self.session.user_agent()
        target = '%s.%s' % (self.service.target_prefix, operation.name)
        json_version = '1.0'
        if hasattr(self.service, 'json_version'):
            json_version = str(self.service.json_version)
        content_type = 'application/x-amz-json-%s' % json_version
        content_encoding = 'amz-1.0'
        data = json.dumps(params)
        request = AWSRequest(method='POST', url=self.host,
                             data=data,
                             headers={'User-Agent': user_agent,
                                      'X-Amz-Target': target,
                                      'Content-Type': content_type,
                                      'Content-Encoding': content_encoding})
        return request


class RestEndpoint(Endpoint):

    def build_uri(self, operation, params):
        logger.debug('Building URI for rest endpoint.')
        uri = operation.http['uri']
        if '?' in uri:
            path, query_params = uri.split('?')
        else:
            path = uri
            query_params = ''
        logger.debug('Templated URI path: %s', path)
        logger.debug('Templated URI query_params: %s', query_params)
        path_components = []
        for pc in path.split('/'):
            if pc:
                pc = six.text_type(pc).format(**params['uri_params'])
            path_components.append(pc)
        path = quote('/'.join(path_components).encode('utf-8'), safe='/~')
        query_param_components = []
        for qpc in query_params.split('&'):
            if qpc:
                if '=' in qpc:
                    key_name, value_name = qpc.split('=')
                else:
                    key_name = qpc
                    value_name = None
                if value_name:
                    value_name = value_name.strip('{}')
                    if value_name in params['uri_params']:
                        value = params['uri_params'][value_name]
                        if isinstance(value, six.string_types):
                            value = quote(value.encode('utf-8'), safe='/~')
                        query_param_components.append('%s=%s' % (
                            key_name, value))
                else:
                    query_param_components.append(key_name)
        query_params = '&'.join(query_param_components)
        logger.debug('Rendered path: %s', path)
        logger.debug('Rendered query_params: %s', query_params)
        return path + '?' + query_params

    def _create_request_object(self, operation, params):
        user_agent = self.session.user_agent()
        params['headers']['User-Agent'] = user_agent
        uri = self.build_uri(operation, params)
        uri = urljoin(self.host, uri)
        payload = None
        if params['payload']:
            payload = params['payload'].getvalue()
        if payload is None:
            request = AWSRequest(method=operation.http['method'],
                                 url=uri, headers=params['headers'])
        else:
            request = AWSRequest(method=operation.http['method'],
                                 url=uri, headers=params['headers'],
                                 data=payload)
        return request


def _get_proxies(url):
    # We could also support getting proxies from a config file,
    # but for now proxy support is taken from the environment.
    return get_environ_proxies(url)


def get_endpoint(service, region_name, endpoint_url, verify=None):
    cls = SERVICE_TO_ENDPOINT.get(service.type)
    if cls is None:
        raise botocore.exceptions.UnknownServiceStyle(
            service_style=service.type)
    service_name = getattr(service, 'signing_name', service.endpoint_prefix)
    auth = None
    if hasattr(service, 'signature_version'):
        auth = _get_auth(service.signature_version,
                         credentials=service.session.get_credentials(),
                         service_name=service_name,
                         region_name=region_name,
                         service_object=service)
    proxies = _get_proxies(endpoint_url)
    verify = _get_verify_value(verify)
    return cls(service, region_name, endpoint_url, auth=auth, proxies=proxies,
               verify=verify)


def _get_verify_value(verify):
    # This is to account for:
    # https://github.com/kennethreitz/requests/issues/1436
    # where we need to honor REQUESTS_CA_BUNDLE because we're creating our
    # own request objects.
    # First, if verify is not None, then the user explicitly specified
    # a value so this automatically wins.
    if verify is not None:
        return verify
    # Otherwise use the value from REQUESTS_CA_BUNDLE, or default to
    # True if the env var does not exist.
    return os.environ.get('REQUESTS_CA_BUNDLE', True)


def _get_auth(signature_version, credentials, service_name, region_name,
              service_object):
    cls = AUTH_TYPE_MAPS.get(signature_version)
    if cls is None:
        raise UnknownSignatureVersionError(signature_version=signature_version)
    else:
        kwargs = {'credentials': credentials}
        if cls.REQUIRES_REGION:
            if region_name is None:
                envvar_name = service_object.session.session_var_map['region'][1]
                raise botocore.exceptions.NoRegionError(env_var=envvar_name)
            kwargs['region_name'] = region_name
            kwargs['service_name'] = service_name
        return cls(**kwargs)


SERVICE_TO_ENDPOINT = {
    'query': QueryEndpoint,
    'json': JSONEndpoint,
    'rest-xml': RestEndpoint,
    'rest-json': RestEndpoint,
}
