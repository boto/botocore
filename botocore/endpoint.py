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
from botocore.exceptions import UnknownSignatureVersionError, UnknownEndpointError
from botocore.awsrequest import AWSRequest
from botocore.compat import urljoin, json, quote
from botocore.utils import percent_encode_sequence
from botocore.hooks import first_non_none_response


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

    def __init__(self, region_name, host, auth, user_agent, signature_version,
                 endpoint_prefix, event_emitter, proxies=None, verify=True,
                 timeout=DEFAULT_TIMEOUT):
        self._endpoint_prefix = endpoint_prefix
        self._signature_version = signature_version
        self._event_emitter = event_emitter
        self._user_agent = user_agent
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
        return '%s(%s)' % (self._endpoint_prefix, self.host)

    def make_request(self, operation_model, request_dict):
        logger.debug("Making request for %s (verify_ssl=%s) with params: %s",
                     operation_model, self.verify, request_dict)
        prepared_request = self.create_request(request_dict)
        return self._send_request(prepared_request, operation_model)

    def _choose_signer(self, signer=None):
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
            do_auth = self._signature_version and self.auth
            if do_auth:
                signer = self.auth
            else:
                # If we're not suppose to sign the request, then we set the
                # signer to None.
                signer = None
        return signer

    def create_request(self, params, signer=None):
        signer = self._choose_signer(signer)
        request = self._create_request_object(params)
        prepared_request = self.prepare_request(request, signer)
        return prepared_request

    def _create_request_object(self, request_dict):
        r = request_dict
        user_agent = self._user_agent
        headers = r['headers']
        headers['User-Agent'] = user_agent
        url = urljoin(self.host, r['url_path'])
        if r['query_string']:
            encoded_query_string = percent_encode_sequence(r['query_string'])
            if '?' not in url:
                url += '?%s' % encoded_query_string
            else:
                url += '&%s' % encoded_query_string
        request = AWSRequest(method=r['method'], url=url,
                             data=r['body'],
                             headers=headers)
        return request

    def prepare_request(self, request, signer):
        if signer is not None:
            with self._lock:
                # Parts of the auth signing code aren't thread safe (things
                # that manipulate .auth_path), so we're using a lock here to
                # prevent race conditions.
                event_name = 'before-auth.%s' % self._endpoint_prefix
                self._event_emitter.emit(
                    event_name, endpoint=self, request=request, auth=signer)
                signer.add_auth(request=request)
        prepared_request = request.prepare()
        return prepared_request

    def _send_request(self, request, operation_model):
        attempts = 1
        response, exception = self._get_response(request, operation_model, attempts)
        while self._needs_retry(attempts, operation_model, response, exception):
            attempts += 1
            # If there is a stream associated with the request, we need
            # to reset it before attempting to send the request again.
            # This will ensure that we resend the entire contents of the
            # body.
            request.reset_stream()
            # Resign the request when retried.
            signer = self._choose_signer()
            request = self.prepare_request(request.original, signer)
            response, exception = self._get_response(request, operation_model,
                                                     attempts)
        return response

    def _get_response(self, request, operation_model, attempts):
        try:
            logger.debug("Sending http request: %s", request)
            http_response = self.http_session.send(
                request, verify=self.verify,
                stream=operation_model.has_streaming_output,
                proxies=self.proxies, timeout=self.timeout)
        except Exception as e:
            logger.debug("Exception received when sending HTTP request.",
                         exc_info=True)
            return (None, e)
        # This returns the http_response and the parsed_data.
        return (botocore.response.get_response(operation_model,
                                               http_response), None)

    def _needs_retry(self, attempts, operation_model, response=None,
                     caught_exception=None):
        event_name = 'needs-retry.%s.%s' % (self._endpoint_prefix,
                                            operation_model.name)
        responses = self._event_emitter.emit(
            event_name, response=response, endpoint=self,
            operation=operation_model, attempts=attempts,
            caught_exception=caught_exception)
        handler_response = first_non_none_response(responses)
        if handler_response is None:
            return False
        else:
            # Request needs to be retried, and we need to sleep
            # for the specified number of times.
            logger.debug("Response received to retry, sleeping for "
                         "%s seconds", handler_response)
            time.sleep(handler_response)
            return True


def _get_proxies(url):
    # We could also support getting proxies from a config file,
    # but for now proxy support is taken from the environment.
    return get_environ_proxies(url)


def get_endpoint(service, region_name, endpoint_url, verify=None):
    service_name = getattr(service, 'signing_name', service.endpoint_prefix)
    endpoint_prefix = service.endpoint_prefix
    signature_version = getattr(service, 'signature_version', None)
    session = service.session
    credentials = session.get_credentials()
    event_emitter = session.get_component('event_emitter')
    user_agent = session.user_agent()
    auth = None
    return get_endpoint_complex(service_name, endpoint_prefix,
                                signature_version, credentials,
                                region_name, endpoint_url, verify, user_agent,
                                event_emitter)


def get_endpoint_complex(service_name, endpoint_prefix, signature_version,
                         credentials, region_name, endpoint_url, verify,
                         user_agent, event_emitter):
    auth = None
    if signature_version is not None:
        auth = _get_auth(signature_version,
                         credentials=credentials,
                         service_name=service_name,
                         region_name=region_name)
    proxies = _get_proxies(endpoint_url)
    verify = _get_verify_value(verify)
    return Endpoint(region_name, endpoint_url, auth=auth,
               user_agent=user_agent,
               endpoint_prefix=endpoint_prefix,
               event_emitter=event_emitter,
               signature_version=signature_version,
               proxies=proxies,
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


def _get_auth(signature_version, credentials, service_name, region_name):
    cls = AUTH_TYPE_MAPS.get(signature_version)
    if cls is None:
        raise UnknownSignatureVersionError(signature_version=signature_version)
    else:
        kwargs = {'credentials': credentials}
        if cls.REQUIRES_REGION:
            if region_name is None:
                raise botocore.exceptions.NoRegionError(
                    env_var='AWS_DEFAULT_REGION')
            kwargs['region_name'] = region_name
            kwargs['service_name'] = service_name
        return cls(**kwargs)


class EndpointCreator(object):
    def __init__(self, endpoint_resolver, configured_region, event_emitter,
                 credentials, user_agent):
        self._endpoint_resolver = endpoint_resolver
        self._configured_region = configured_region
        self._event_emitter = event_emitter
        self._credentials = credentials
        self._user_agent = user_agent

    def create_endpoint(self, service_model, region_name=None, is_secure=True,
                        endpoint_url=None, verify=None, credentials=None):
        if region_name is None:
            region_name = self._configured_region
        # Use the endpoint resolver heuristics to build the endpoint url.
        scheme = 'https' if is_secure else 'http'
        try:
            endpoint = self._endpoint_resolver.construct_endpoint(
                service_model.endpoint_prefix,
                region_name, scheme=scheme)
        except UnknownEndpointError:
            if endpoint_url is not None:
                # If the user provides an endpoint_url, it's ok
                # if the heuristics didn't find anything.  We use the
                # user provided endpoint_url.
                endpoint = {'uri': endpoint_url, 'properties': {}}
            else:
                raise
        # We only support the credentialScope.region in the properties
        # bag right now, so if it's available, it will override the
        # provided region name.
        region_name_override = endpoint['properties'].get(
            'credentialScope', {}).get('region')
        signature_version = service_model.signature_version
        if 'signatureVersion' in endpoint['properties']:
            signature_version = endpoint['properties']['signatureVersion']
        if region_name_override is not None:
            # Letting the heuristics rule override the region_name
            # allows for having a default region of something like us-west-2
            # for IAM, but we still will know to use us-east-1 for sigv4.
            region_name = region_name_override
        if endpoint_url is not None:
            # If the user provides an endpoint url, we'll use that
            # instead of what the heuristics rule gives us.
            final_endpoint_url = endpoint_url
        else:
            final_endpoint_url = endpoint['uri']
        return self._get_endpoint(service_model, region_name,
                                  signature_version, final_endpoint_url,
                                  verify, credentials)

    def _get_endpoint(self, service_model, region_name, signature_version,
                      endpoint_url, verify, user_provided_creds):
        service_name = service_model.signing_name
        endpoint_prefix = service_model.endpoint_prefix
        credentials = self._credentials
        if user_provided_creds is not None:
            # Credentials provided via create_endpoint() override the
            # credentials provided when the EndpointCreator was created.
            credentials = user_provided_creds
        user_agent = self._user_agent
        event_emitter = self._event_emitter
        user_agent = self._user_agent
        return get_endpoint_complex(service_name, endpoint_prefix,
                                    signature_version, credentials,
                                    region_name, endpoint_url,
                                    verify, user_agent, event_emitter)
