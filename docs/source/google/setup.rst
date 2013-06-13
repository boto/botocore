===============================================
Setting up Google Cloud Services Authentication
===============================================

All of Google Cloud services require **Open Authentication 2.0** (OAuth2.0).

This page will describe the possible methods for setting up your workstations to interact with Google Cloud services.

Environment Setup
-----------------

*Optional* - Consider using virtual Python environments to avoid polluting global Python packages.

`virtualenv
<https://pypi.python.org/pypi/virtualenv>`_

`virtualenvwrapper
<http://virtualenvwrapper.readthedocs.org/en/latest/>`_

One-time Setup
--------------

There are currently two supported methods of setting up botocore to interact with Google Cloud Platform services:

1. Using Service Accounts.
2. Using Installed Application credentials.

*The preferred method is to use Service Account authentication for your application.*
 
Method 1: Service Account
.........................

**Use Case**: Installing an application or service on a large number of servers.

The Installed Application method may cause your program to run into rate-limits
if it is deployed to a large number of servers, thus using a Service Account is recommended.

Install pycrypto
****************

Requires: ``pycrypto`` >= 2.6

Install `pip
<http://www.pip-installer.org/en/latest/installing.html>`_

Run: ``pip install pycrypto``

Install private key
*******************
**IMPORTANT**: See `Service Accounts
<https://developers.google.com/console/help/#service_accounts>`_
for instructions on setting up a Service Account.

Set up a new Service Account through the `API Console
<https://code.google.com/apis/console/‎>`_, or use an existing account.

When you set up a Service Account, you will be prompted
to download a private key file (int ``.p12`` format). 
Convert the private key file ``.p12`` into ``.pem`` format using the following
command: 

``openssl pkcs12 -in YOURPRIVKEY.p12 -nodes -nocerts | openssl rsa -out PRIV.pem``

Move the ``PRIV.pem`` key into a safe location, such as ``~/.boto_config/`` then
add the following lines to your botocore configuration file::
  [Credentials]
  gcp_service_account_email=SERVICE_ACCOUNT_CLIENT_EMAIL
  gcp_private_key_file=~/.boto_config/PRIV.pem
  gcp_scopes=REQUESTED_SCOPES (comma separated)

*Note*: The default password for the .p12 key files for service accounts is: ``notasecret``

*Note 2*: Botocore configuration file is typically placed in one of the following locations:

- ``/etc/boto.cfg``
- ``~/.boto``
- ``BOTO_CONFIG environment variable``

Method 2: Installed Application
...............................

*To be completed...*


