# Copyright 2014 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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

import botocore
import botocore.auth

from botocore.exceptions import UnknownSignatureVersionError

class RequestSigner(object):
    """
    An object to sign requests before they go out over the wire using
    one of the authentication mechanisms defined in ``auth.py``. This
    class fires two events scoped to a service and operation name:

    * choose-signer: Allows overriding the auth signer name.
    * before-sign: Allows mutating the request before signing.

    Together these events allow for customization of the request
    signing pipeline, including overrides, request path manipulation,
    and disabling signing per operation.

    :type service_name: string
    :param service_name: Name of the service, e.g. ``S3``
    :type region_name: string
    :param region_name: Name of the service region, e.g. ``us-east-1``
    :type signing_name: string
    :param signing_name: Service signing name. This is usually the
                         same as the service name, but can differ. E.g.
                         ``emr`` vs. ``elasticmapreduce``.
    :type signature_version: string
    :param signature_version: Signature name like ``v4``.
    :type credentials: :py:class:`~botocore.credentials.Credentials`
    :param credentials: User credentials with which to sign requests.
    :type event_emitter: :py:class:`~botocore.hooks.BaseEventHooks`
    :param event_emitter: Extension mechanism to fire events.
    """
    def __init__(self, service_name, region_name, signing_name,
                 signature_version, credentials, event_emitter):
        self._service_name = service_name
        self._region_name = region_name
        self._signing_name = signing_name
        self._signature_version = signature_version
        self._credentials = credentials
        self._event_emitter = event_emitter

        # Used to cache auth instances since one request signer
        # can be used for many requests in a single client.
        self._cache = {}

    def sign(self, operation_name, request):
        """
        Sign a request before it goes out over the wire.

        :type operation_name: string
        :param operation_name: The name of the current operation, e.g.
                               ``ListBuckets``.
        :type request: AWSRequest
        :param request: The request object to be sent over the wire.
        """
        signature_version = self._signature_version

        # Allow overriding signature version. A response of a blank
        # string means no signing is performed. A response of ``None``
        # means that the default signing method is used.
        handler, response = self._event_emitter.emit_until_response(
            'choose-signer.{0}.{1}'.format(self._service_name, operation_name),
            signing_name=self._signing_name, region_name=self._region_name,
            signature_version=signature_version)
        if response is not None:
            signature_version = response

        # Allow mutating request before signing
        self._event_emitter.emit(
            'before-sign.{0}.{1}'.format(self._service_name, operation_name),
            request=request, signing_name=self._signing_name,
            region_name=self._region_name,
            signature_version=signature_version, request_signer=self)

        # Sign the request if the signature version isn't None or blank
        if signature_version != botocore.UNSIGNED:
            signer = self.get_auth(self._signing_name, self._region_name,
                                    signature_version)
            signer.add_auth(request=request)

    def get_auth(self, signing_name, region_name, signature_version=None):
        """
        Get an auth instance which can be used to sign a request
        using the given signature version.

        :type signing_name: string
        :param signing_name: Service signing name. This is usually the
                             same as the service name, but can differ. E.g.
                             ``emr`` vs. ``elasticmapreduce``.
        :type region_name: string
        :param region_name: Name of the service region, e.g. ``us-east-1``
        :type signature_version: string
        :param signature_version: Signature name like ``v4``.
        :rtype: :py:class:`~botocore.auth.BaseSigner`
        :return: Auth instance to sign a request.
        """
        if signature_version is None:
            signature_version = self._signature_version

        key = '{0}.{1}.{2}'.format(signature_version, region_name,
                                   signing_name)
        if key in self._cache:
            return self._cache[key]

        cls = botocore.auth.AUTH_TYPE_MAPS.get(signature_version)
        if cls is None:
            raise UnknownSignatureVersionError(
                signature_version=signature_version)
        else:
            kwargs = {'credentials': self._credentials}
            if cls.REQUIRES_REGION:
                if self._region_name is None:
                    raise botocore.exceptions.NoRegionError(
                        env_var='AWS_DEFAULT_REGION')
                kwargs['region_name'] = region_name
                kwargs['service_name'] = signing_name
            auth = cls(**kwargs)
            self._cache[key] = auth
            return auth
