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

import re
import logging

__version__ = '0.33.0'


class NullHandler(logging.Handler):
    def emit(self, record):
        pass

# Configure default logger to do nothing
log = logging.getLogger('botocore')
log.addHandler(NullHandler())


_first_cap_regex = re.compile('(.)([A-Z][a-z]+)')
_number_cap_regex = re.compile('([a-z])([0-9]+)')
_end_cap_regex = re.compile('([a-z0-9])([A-Z])')

ScalarTypes = ('string', 'integer', 'boolean', 'timestamp', 'float', 'double')


def xform_name(name, sep='_'):
    """
    Convert camel case to a "pythonic" name.
    """
    s1 = _first_cap_regex.sub(r'\1' + sep + r'\2', name)
    s2 = _number_cap_regex.sub(r'\1' + sep + r'\2', s1)
    return _end_cap_regex.sub(r'\1' + sep + r'\2', s2).lower()


class BotoCoreObject(object):

    def __init__(self, **kwargs):
        self.name = ''
        self.py_name = None
        self.cli_name = None
        self.type = None
        self.members = []
        self.documentation = ''
        self.__dict__.update(kwargs)
        if self.py_name is None:
            self.py_name = xform_name(self.name, '_')
        if self.cli_name is None:
            self.cli_name = xform_name(self.name, '-')

    def __repr__(self):
        return '%s:%s' % (self.type, self.name)
