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
from botocore.vendored.requests.exceptions import ConnectionError
from botocore.vendored import six

from botocore.exceptions import BaseEndpointResolverError
from botocore.exceptions import EndpointConnectionError
from botocore.awsrequest import AWSRequest
from botocore.compat import filter_ssl_warnings, urlsplit
from botocore.compat import urlunsplit
from botocore.utils import percent_encode_sequence
from botocore.utils import is_valid_endpoint_url
from botocore.hooks import first_non_none_response
from botocore.response import StreamingBody
from botocore import parsers


logger = logging.getLogger(__name__)
DEFAULT_TIMEOUT = 60
NOT_SET = object()
filter_ssl_warnings()


def convert_to_response_dict(http_response, operation_model):
    """Convert an HTTP response object to a request dict.

    This converts the requests library's HTTP response object to
    a dictionary.

    :type http_response: botocore.vendored.requests.model.Response
    :param http_response: The HTTP response from an AWS service request.

    :rtype: dict
    :return: A response dictionary which will contain the following keys:
        * headers (dict)
        * status_code (int)
        * body (string or file-like object)

    """
    response_dict = {
        'headers': http_response.headers,
        'status_code': http_response.status_code,
    }
    if response_dict['status_code'] >= 300:
        response_dict['body'] = http_response.content
    elif operation_model.has_streaming_output:
        response_dict['body'] = StreamingBody(
            http_response.raw, response_dict['headers'].get('content-length'))
    else:
        response_dict['body'] = http_response.content
    return response_dict


class PreserveAuthSession(Session):
    def rebuild_auth(self, prepared_request, response):
        pass


class RequestCreator(object):
    """This object can convert a request dict to an AWSRequest class."""

    def create_request_object(self, request_dict, user_agent, endpoint_url):
        """

        :type request_dict: dict
        :param request_dict:  The request dict (created from the ``serialize``
            module).

        :type user_agent: string
        :param user_agent: The user agent to use for this request.

        :type endpoint_url: string
        :param endpoint_url: The full endpoint url, which contains at least
            the scheme, the hostname, and optionally any path components.

        :rtype: ``botocore.awsrequest.AWSRequest``
        :return: An AWSRequest object based on the request_dict.

        """
        r = request_dict
        headers = r['headers']
        headers['User-Agent'] = user_agent
        url = self._urljoin(endpoint_url, r['url_path'])
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

    def _urljoin(self, endpoint_url, url_path):
        p = urlsplit(endpoint_url)
        # <part>   - <index>
        # scheme   - p[0]
        # netloc   - p[1]
        # path     - p[2]
        # query    - p[3]
        # fragment - p[4]
        if not url_path or url_path == '/':
            # If there's no path component, ensure the URL ends with
            # a '/' for backwards compatibility.
            if not p[2]:
                return endpoint_url + '/'
            return endpoint_url
        if p[2].endswith('/') and url_path.startswith('/'):
            new_path = p[2][:-1] + url_path
        else:
            new_path = p[2] + url_path
        reconstructed = urlunsplit((p[0], p[1], new_path, p[3], p[4]))
        return reconstructed


class Endpoint(object):
    """
    Represents an endpoint for a particular service in a specific
    region.  Only an endpoint can make requests.

    :ivar service: The Service object that describes this endpoints
        service.
    :ivar host: The fully qualified endpoint hostname.
    :ivar session: The session object.
    """

    def __init__(self, region_name, host, user_agent,
                 endpoint_prefix, event_emitter, proxies=None, verify=True,
                 timeout=DEFAULT_TIMEOUT, response_parser_factory=None):
        self._endpoint_prefix = endpoint_prefix
        self._event_emitter = event_emitter
        self._user_agent = user_agent
        self.region_name = region_name
        self.host = host
        self.verify = verify
        if proxies is None:
            proxies = {}
        self.proxies = proxies
        self.http_session = PreserveAuthSession()
        self.timeout = timeout
        self._lock = threading.Lock()
        if response_parser_factory is None:
            response_parser_factory = parsers.ResponseParserFactory()
        self._response_parser_factory = response_parser_factory
        self._request_creator = RequestCreator()

    def __repr__(self):
        return '%s(%s)' % (self._endpoint_prefix, self.host)

    def make_request(self, operation_model, request_dict):
        logger.debug("Making request for %s (verify_ssl=%s) with params: %s",
                     operation_model, self.verify, request_dict)
        return self._send_request(request_dict, operation_model)

    def create_request(self, params, operation_model=None):
        request = self._request_creator.create_request_object(
            params, self._user_agent, self.host)
        if operation_model:
            event_name = 'request-created.{endpoint_prefix}.{op_name}'.format(
                endpoint_prefix=self._endpoint_prefix,
                op_name=operation_model.name)
            self._event_emitter.emit(event_name, request=request,
                                     operation_name=operation_model.name)
        prepared_request = self.prepare_request(request)
        return prepared_request

    def _encode_headers(self, headers):
        # In place encoding of headers to utf-8 if they are unicode.
        for key, value in headers.items():
            if isinstance(value, six.text_type):
                headers[key] = value.encode('utf-8')

    def prepare_request(self, request):
        self._encode_headers(request.headers)
        return request.prepare()

    def _send_request(self, request_dict, operation_model):
        attempts = 1
        request = self.create_request(request_dict, operation_model)
        success_response, exception = self._get_response(
            request, operation_model, attempts)
        while self._needs_retry(attempts, operation_model,
                                success_response, exception):
            attempts += 1
            # If there is a stream associated with the request, we need
            # to reset it before attempting to send the request again.
            # This will ensure that we resend the entire contents of the
            # body.
            request.reset_stream()
            # Create a new request when retried (including a new signature).
            request = self.create_request(
                request_dict, operation_model=operation_model)
            success_response, exception = self._get_response(
                request, operation_model, attempts)
        if exception is not None:
            raise exception
        else:
            return success_response

    def _get_response(self, request, operation_model, attempts):
        # This will return a tuple of (success_response, exception)
        # and success_response is itself a tuple of
        # (http_response, parsed_dict).
        # If an exception occurs then the success_response is None.
        # If no exception occurs then exception is None.
        try:
            logger.debug("Sending http request: %s", request)
            http_response = self.http_session.send(
                request, verify=self.verify,
                stream=operation_model.has_streaming_output,
                proxies=self.proxies, timeout=self.timeout)
        except ConnectionError as e:
            # For a connection error, if it looks like it's a DNS
            # lookup issue, 99% of the time this is due to a misconfigured
            # region/endpoint so we'll raise a more specific error message
            # to help users.
            if self._looks_like_dns_error(e):
                endpoint_url = e.request.url
                better_exception = EndpointConnectionError(
                    endpoint_url=endpoint_url, error=e)
                return (None, better_exception)
            else:
                return (None, e)
        except Exception as e:
            logger.debug("Exception received when sending HTTP request.",
                         exc_info=True)
            return (None, e)
        # This returns the http_response and the parsed_data.
        response_dict = convert_to_response_dict(http_response,
                                                 operation_model)
        parser = self._response_parser_factory.create_parser(
            operation_model.metadata['protocol'])
        return ((http_response, parser.parse(response_dict,
                                             operation_model.output_shape)),
                None)

    def _looks_like_dns_error(self, e):
        return 'gaierror' in str(e) and e.request is not None

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
    session = service.session
    event_emitter = session.get_component('event_emitter')
    user_agent = session.user_agent()
    return get_endpoint_complex(service_name, endpoint_prefix,
                                region_name, endpoint_url, verify, user_agent,
                                event_emitter)


def get_endpoint_complex(service_name, endpoint_prefix,
                         region_name, endpoint_url, verify,
                         user_agent, event_emitter,
                         response_parser_factory=None):
    proxies = _get_proxies(endpoint_url)
    verify = _get_verify_value(verify)
    return Endpoint(
        region_name, endpoint_url,
        user_agent=user_agent,
        endpoint_prefix=endpoint_prefix,
        event_emitter=event_emitter,
        proxies=proxies,
        verify=verify,
        response_parser_factory=response_parser_factory)


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


class EndpointCreator(object):
    def __init__(self, endpoint_resolver, configured_region, event_emitter,
                 user_agent):
        self._endpoint_resolver = endpoint_resolver
        self._configured_region = configured_region
        self._event_emitter = event_emitter
        self._user_agent = user_agent

    def create_endpoint(self, service_model, region_name=None, is_secure=True,
                        endpoint_url=None, verify=None, credentials=None,
                        response_parser_factory=None,
                        signature_version=NOT_SET):
        if region_name is None:
            region_name = self._configured_region
        # Use the endpoint resolver heuristics to build the endpoint url.
        scheme = 'https' if is_secure else 'http'
        try:
            endpoint = self._endpoint_resolver.construct_endpoint(
                service_model.endpoint_prefix,
                region_name, scheme=scheme)
        except BaseEndpointResolverError:
            if endpoint_url is not None:
                # If the user provides an endpoint_url, it's ok
                # if the heuristics didn't find anything.  We use the
                # user provided endpoint_url.
                endpoint = {'uri': endpoint_url, 'properties': {}}
            else:
                raise

        region_name = self._determine_region_name(endpoint, region_name,
                                                  endpoint_url)
        if endpoint_url is not None:
            # If the user provides an endpoint url, we'll use that
            # instead of what the heuristics rule gives us.
            final_endpoint_url = endpoint_url
        else:
            final_endpoint_url = endpoint['uri']
        if not is_valid_endpoint_url(final_endpoint_url):
            raise ValueError("Invalid endpoint: %s" % final_endpoint_url)
        return self._get_endpoint(service_model, region_name,
                                  final_endpoint_url, verify,
                                  response_parser_factory)

    def _determine_region_name(self, endpoint_config, region_name=None,
                               endpoint_url=None):
        # This is a helper function to determine region name to use.
        # It will take into account whether the user passes in a region
        # name, whether their is a rule in the endpoint JSON, or
        # an endpoint url was provided.

        # TODO: Once we completely move to clients. We will remove region
        # as public attribute from endpoints and as a result move this helper
        # function to clients becuase region is really only important for
        # signing.

        # We only support the credentialScope.region in the properties
        # bag right now, so if it's available, it will override the
        # provided region name.
        region_name_override = endpoint_config['properties'].get(
            'credentialScope', {}).get('region')

        if endpoint_url is not None:
            # If an endpoint_url is provided, do not use region name
            # override if a region
            # was provided by the user.
            if region_name is not None:
                region_name_override = None

        if region_name_override is not None:
            # Letting the heuristics rule override the region_name
            # allows for having a default region of something like us-west-2
            # for IAM, but we still will know to use us-east-1 for sigv4.
            region_name = region_name_override

        return region_name

    def _get_endpoint(self, service_model, region_name, endpoint_url,
                      verify, response_parser_factory):
        service_name = service_model.signing_name
        endpoint_prefix = service_model.endpoint_prefix
        user_agent = self._user_agent
        event_emitter = self._event_emitter
        user_agent = self._user_agent
        return get_endpoint_complex(service_name, endpoint_prefix,
                                    region_name, endpoint_url,
                                    verify, user_agent, event_emitter,
                                    response_parser_factory)
