# Copyright 2013 Google, Inc. or its affiliates. All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, dis-
# tribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the fol-
# lowing conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#

#Flag indicating availability of pycrpyto required for Service Accounts
SERVICE_ACCOUNTS_AVAILABLE = True

import base64

try:
    from httplib import HTTPSConnection
except:
    from http.client import HTTPSConnection
import json
import logging
import os
import time
import urllib

logger = logging.getLogger(__name__)

try:
    from Crypto.Hash import SHA256
    from Crypto.PublicKey import RSA
    from Crypto.Signature import PKCS1_v1_5
except ImportError:
    logger.warning("pycrypto not found: Service Accounts unavailable")
    SERVICE_ACCOUNTS_AVAILABLE = False


class OAuth2(object):
    """see: https://developers.google.com/accounts/docs/OAuth2ServiceAccount"""

    def __init__(self, credentials):
        self._credentials = credentials

    def get_new_access_token_from_refresh(self):
        """
        Uses a refresh token to get a new access token
        """
        conn = HTTPSConnection('accounts.google.com')
        params = urllib.urlencode({
           'grant_type': 'refresh_token',
           'client_id':self._credentials.gcp_client_id,
           'client_secret':self._credentials.gcp_client_secret,
           'refresh_token':self._credentials.gcp_refresh_token,
        })
        headers = {'Content-Type':'application/x-www-form-urlencoded'}
        conn.request('POST', '/o/oauth2/token', params, headers=headers)
        content = conn.getresponse()
        data = content.read()
        conn.close()
        if content.status in [200, 201]:
            return json.loads(data)
        else:
            return None

    def get_new_access_token(self):
        """Returns a JSON object containing authentication response
        
        Contains either an error string, or access token information
        """
        if not SERVICE_ACCOUNTS_AVAILABLE:
            logger.warning('pycrypto requirement not satisfied.')
            return None

        if not self._credentials:
            logger.warning('No Google Service Account Credentials found!')
            return None

        if not self.verify_service_credentials_reqs():
            logger.warning('Invalid Google Service Account Credentials.')
            return None

        #This header never changes. 
        header = "{'alg':'RS256','typ':'JWT'}"

        #Get a base64 encoded version of the header
        header_enc = base64.urlsafe_b64encode(header).rstrip('=')

        #Build the claim_set
        claim_set = {
            'iss':self._credentials.gcp_account,
            'scope':' '.join(self._credentials.gcp_scopes),
            'aud':'https://accounts.google.com/o/oauth2/token',
            'exp':int(time.time() + 3600),
            'iat':int(time.time())
        }

        #Encode in utf-8
        claim_set = json.dumps(claim_set)

        #Encode in base64
        claim_set_enc = base64.urlsafe_b64encode(claim_set).rstrip('=')

        #Build the signature input
        message = header_enc + '.' + claim_set_enc

        #Compute the signature payload
        key_path = os.path.expandvars(self._credentials.gcp_private_key_file)
        key_path = os.path.expanduser(key_path)
        key = RSA.importKey(open(key_path).read())
        hash_func = SHA256.new(message)
        signer = PKCS1_v1_5.new(key)
        signature = base64.urlsafe_b64encode(signer.sign(hash_func)).rstrip('=')

        #Compile the JWT assertion string
        jwt = message + '.' + signature

        #Connect to the authentication server with the JWT credentials
        conn = HTTPSConnection('accounts.google.com')
        params = urllib.urlencode({
            'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
            'assertion': jwt
        })
        headers = {'Content-Type':'application/x-www-form-urlencoded'}
        conn.request('POST', '/o/oauth2/token', params, headers=headers)
        content = conn.getresponse()
        json_data = content.read()
        conn.close()

        #Build our JSON response
        response = json.loads(json_data)

        return response

    def verify_service_credentials_reqs(self):
        if not hasattr(self._credentials, 'gcp_account'):
            return False
        elif not self._credentials.gcp_account:
            return False
        if not hasattr(self._credentials, 'gcp_private_key_file'):
            return False
        elif not self._credentials.gcp_private_key_file:
            return False
        if not hasattr(self._credentials, 'gcp_scopes'):
            return False
        elif not self._credentials.gcp_scopes:
            return False
        return True
