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


class Provider(object):

    def __init__(self, session, name):
        self.session = session
        self.name = name
        self._services = None

    def __repr__(self):
        return 'Provider(%s)' % self.name

    @property
    def services(self):
        if self._services is None:
            self._services = [self.session.get_service(sn) for
                              sn in self.session.get_available_services()]
        return self._services


def get_provider(session, provider_name):
    return Provider(session, provider_name)
