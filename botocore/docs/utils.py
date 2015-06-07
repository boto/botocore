# Copyright 2015 Amazon.com, Inc. or its affiliates. All Rights Reserved.
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
from collections import namedtuple


def py_type_name(type_name):
    """Get the Python type name for a given model type.

        >>> py_type_name('list')
        'list'
        >>> py_type_name('structure')
        'dict'

    :rtype: string
    """
    return {
        'blob': 'bytes',
        'character': 'string',
        'double': 'float',
        'long': 'integer',
        'map': 'dict',
        'structure': 'dict',
        'timestamp': 'datetime',
    }.get(type_name, type_name)


def py_default(type_name):
    """Get the Python default value for a given model type.

        >>> py_default('string')
        '\'string\''
        >>> py_default('list')
        '[...]'
        >>> py_default('unknown')
        '...'

    :rtype: string
    """
    return {
        'double': '123.0',
        'long': '123',
        'integer': '123',
        'string': "'string'",
        'blob': "b'bytes'",
        'boolean': 'True|False',
        'list': '[...]',
        'map': '{...}',
        'structure': '{...}',
        'timestamp': 'datetime(2015, 1, 1)',
    }.get(type_name, '...')


def get_official_service_name(service_model):
    """Generate the official name of an AWS Service

    :param service_model: The service model representing the service
    """
    official_name = service_model.metadata.get('serviceFullName')
    short_name = service_model.metadata.get('serviceAbbreviation', '')
    if short_name.startswith('Amazon'):
        short_name = short_name[7:]
    if short_name.startswith('AWS'):
        short_name = short_name[4:]
    if short_name and short_name.lower() not in official_name.lower():
        official_name += ' ({0})'.format(short_name)
    return official_name


_DocumentedShape = namedtuple(
    'DocumentedShape', ['name', 'type_name', 'documentation', 'metadata',
                        'members', 'required_members'])


class DocumentedShape (_DocumentedShape):
    """Use this class to inject new shapes into a model for documentation"""
    def __new__(cls, name, type_name, documentation, metadata=None,
                members=None, required_members=None):
        if metadata is None:
            metadata = []
        if members is None:
            members = []
        if required_members is None:
            required_members = []
        return super(DocumentedShape, cls).__new__(
            cls, name, type_name, documentation, metadata, members,
            required_members)


class AutoPopulatedParam(object):
    def __init__(self, name, param_description=None):
        self.name = name
        self.param_description = param_description
        if param_description is None:
            self.param_description = (
                'Note this parameter is autopopulated. There is no '
                'need to include in method call.\n')

    def document_auto_populated_param(self, event_name, section, **kwargs):
        """This documents the auto populated parameters

        It will remove any required marks for the parameter, remove the
        parameter from the example, and add a snippet about the parameter
        being autopopulated in the description.
        """
        if event_name.startswith('docs.request-params'):
            if self.name in section.available_sections:
                section = section.get_section(self.name)
                if 'is-required' in section.available_sections:
                    section.delete_section('is-required')
                description_section = section.get_section(
                    'param-documentation')
                description_section.writeln(self.param_description)
        elif event_name.startswith('docs.request-example'):
            section = section.get_section('structure-value')
            if self.name in section.available_sections:
                section.delete_section(self.name)
