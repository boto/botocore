#!/usr/bin/env python
import botocore
import sys

from setuptools import setup, find_packages


requires = ['jmespath>=0.7.1,<1.0.0',
            'python-dateutil>=2.1,<3.0.0',
            'docutils>=0.10']


if sys.version_info[:2] == (2, 6):
    # For python2.6 we have a few other dependencies.
    # First we need an ordered dictionary so we use the
    # 2.6 backport.
    requires.append('ordereddict==1.1')
    # Then we need simplejson.  This is because we need
    # a json version that allows us to specify we want to
    # use an ordereddict instead of a normal dict for the
    # JSON objects.  The 2.7 json module has this.  For 2.6
    # we need simplejson.
    requires.append('simplejson==3.3.0')


setup(
    name='botocore',
    version=botocore.__version__,
    description='Low-level, data-driven core of boto 3.',
    long_description=open('README.rst').read(),
    author='Amazon Web Services',
    url='https://github.com/boto/botocore',
    scripts=[],
    packages=find_packages(exclude=['tests*']),
    package_data={'botocore': ['data/*.json', 'data/*/*.json'],
                  'botocore.vendored.requests': ['*.pem']},
    include_package_data=True,
    install_requires=requires,
    extras_require={
        ':python_version=="2.6"': [
            'ordereddict==1.1',
            'simplejson==3.3.0',
        ]
    },
    license="Apache License 2.0",
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ),
)
