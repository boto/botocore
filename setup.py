#!/usr/bin/env python
import codecs
import os.path
import re
import sys

from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    return codecs.open(os.path.join(here, *parts), 'r').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


requires = ['jmespath>=0.7.1,<1.0.0',
            'docutils>=0.10,<0.16']

python_version = sys.version_info[:2]

if python_version == (2, 6):
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
    requires.append('python-dateutil>=2.1,<2.7.0')
else:
    requires.append('python-dateutil>=2.1,<3.0.0')

if python_version == (2, 6):
    # Requests has officially stopped support for
    # Python 2.6 starting from version 2.20.0
    requires.append('requests==2.19.1')
elif python_version == (3, 3):
    # Requests has implicitly stopped stopped support
    # for Python 3.3 starting from version 2.19.0
    requires.append('requests==2.18.4')
elif python_version == (3, 4):
    # Requests has officially stopped support for
    # for Python 3.4 starting from version 2.22.0
    requires.append('requests==2.21.0')
else:
    requires.append('requests==2.22.0')


if python_version == (2, 6):
    requires.append('urllib3>=1.20,<1.24')
elif python_version == (3, 3):
    requires.append('urllib3>=1.20,<1.23')
else:
    requires.append('urllib3>=1.20,<1.26')


setup(
    name='botocore',
    version=find_version("botocore", "__init__.py"),
    description='Low-level, data-driven core of boto 3.',
    long_description=open('README.rst').read(),
    author='Amazon Web Services',
    url='https://github.com/boto/botocore',
    scripts=[],
    packages=find_packages(exclude=['tests*']),
    package_data={'botocore': ['cacert.pem', 'data/*.json', 'data/*/*.json']},
    include_package_data=True,
    install_requires=requires,
    extras_require={
        ':python_version=="2.6"': [
            'ordereddict==1.1',
            'simplejson==3.3.0',
        ]
    },
    license="Apache License 2.0",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)
