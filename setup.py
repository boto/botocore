#!/usr/bin/env python
import codecs
import os.path
import re

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    return codecs.open(os.path.join(here, *parts), 'r').read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M
    )
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


requires = [
    'jmespath>=0.7.1,<2.0.0',
    'python-dateutil>=2.1,<3.0.0',
    # Prior to Python 3.10, Python doesn't require openssl 1.1.1
    # but urllib3 2.0+ does. This means all botocore users will be
    # broken by default on Amazon Linux 2 and AWS Lambda without this pin.
    'urllib3>=1.25.4,<1.27 ; python_version < "3.10"',
    'urllib3>=1.25.4,!=2.2.0,<3 ; python_version >= "3.10"',
]

extras_require = {
    'crt': ['awscrt==0.22.0'],
}

setup(
    name='botocore',
    version=find_version("botocore", "__init__.py"),
    description='Low-level, data-driven core of boto 3.',
    long_description=open('README.rst').read(),
    author='Amazon Web Services',
    url='https://github.com/boto/botocore',
    scripts=[],
    packages=find_packages(exclude=['tests*']),
    package_data={
        'botocore': ['cacert.pem', 'data/*.json', 'data/*/*.json'],
        'botocore.vendored.requests': ['*.pem'],
    },
    include_package_data=True,
    install_requires=requires,
    extras_require=extras_require,
    license="Apache License 2.0",
    python_requires=">= 3.8",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)
