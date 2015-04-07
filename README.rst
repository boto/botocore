botocore
========

.. image:: https://secure.travis-ci.org/boto/botocore.png?branch=develop
   :target: http://travis-ci.org/boto/botocore

.. image:: https://coveralls.io/repos/boto/botocore/badge.png?branch=develop
   :target: https://coveralls.io/r/boto/botocore?branch=master

A low-level interface to a growing number of Amazon Web Services. The
botocore package is the foundation for
`AWS-CLI <https://github.com/aws/aws-cli>`__.

`Documentation <https://botocore.readthedocs.org/en/latest/>`__

**WARNING**

Botocore is currently under a developer preview, and its API is subject
to change prior to a GA (1.0) release.  Until botocore reaches a 1.0 release,
backwards compatibility is not guaranteed. The plan for GA is as follows:

1. Add client interface to botocore.
2. Add pending deprecation warnings to the use of ``Service`` and ``Operation``
   objects.
3. Change the pending deprecation warnings to deprecation warnings.
4. Create a `clients-only <https://github.com/boto/botocore/tree/clients-only>`_
   branch that completely removes ``Service`` and ``Operation`` objects.
5. Merge ``clients-only`` branch to develop branch, and make an alpha
   release of botocore.
6. Make a beta release of botocore.
7. Make GA release of botocore.

The project is currently at step **4**.

If you need a stable interface, please consider using
`boto <https://github.com/boto/boto>`__.
