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


requires = [
    'jmespath>=0.7.1,<1.0.0',
    'python-dateutil>=2.1,<3.0.0',
]


if sys.version_info[:2] == (3, 4):
    # urllib3 dropped support for python 3.4 in point release 1.25.8
    requires.append('urllib3>=1.25.4,<1.25.8')
else:
    requires.append('urllib3>=1.25.4,<1.26')



setup(
    name='botocore',
    version=find_version("botocore", "__init__.py"),
    description='Low-level, data-driven core of boto 3.',
    long_description=open('README.rst').read(),
    author='Amazon Web Services',
    url='https://github.com/boto/botocore',
    scripts=[],
    packages=find_packages(exclude=['tests*']),
    package_data={'botocore': ['cacert.pem', 'data/*.json', 'data/*/*.json'],
                  'botocore.vendored.requests': ['*.pem']},
    include_package_data=True,
    install_requires=requires,
    extras_require={},
    license="Apache License 2.0",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ]
)
