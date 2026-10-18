.. ref_config:

================
Config Reference
================

botocore.config
---------------

.. autoclass:: botocore.config.Config
   :members:

Explicit request compression
----------------------------

For operations that advertise gzip support, you can request compression even
when the serialized body is smaller than the automatic compression threshold::

    from botocore.config import Config

    config = Config(request_compression_encoding='gzip')

Pass this configuration when creating the client. Leaving
``request_compression_encoding`` unset preserves automatic compression.
Explicit gzip raises ``InvalidConfigError`` if the operation does not advertise
gzip, the request cannot be compressed, or compression is disabled. Only gzip is
supported; zstd is not currently available.

This option does not enable server support. The service endpoint must accept
compressed requests and advertise that capability in its operation model.
