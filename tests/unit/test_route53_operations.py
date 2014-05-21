#!/usr/bin/env python
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

from tests import BaseSessionTest


CREATE_HOSTED_ZONE_PAYLOAD="""<CreateHostedZoneRequest xmlns="https://route53.amazonaws.com/doc/2013-04-01/"><Name>foobar.com</Name><CallerReference>foobar</CallerReference><HostedZoneConfig><Comment>blahblahblah</Comment></HostedZoneConfig></CreateHostedZoneRequest>"""
CREATE_RRSET_PAYLOAD="""<ChangeResourceRecordSetsRequest xmlns="https://route53.amazonaws.com/doc/2013-04-01/"><ChangeBatch><Comment>Adding TXT record</Comment><Changes><Change><Action>CREATE</Action><ResourceRecordSet><Name>midocs.com</Name><Type>TXT</Type><TTL>600</TTL><ResourceRecords><ResourceRecord><Value>"v=foobar"</Value></ResourceRecord></ResourceRecords></ResourceRecordSet></Change></Changes></ChangeBatch></ChangeResourceRecordSetsRequest>"""
DELETE_RRSET_PAYLOAD="""<ChangeResourceRecordSetsRequest xmlns="https://route53.amazonaws.com/doc/2013-04-01/"><ChangeBatch><Comment>Adding TXT record</Comment><Changes><Change><Action>DELETE</Action><ResourceRecordSet><Name>midocs.com</Name><Type>TXT</Type><TTL>600</TTL><ResourceRecords><ResourceRecord><Value>"v=foobar"</Value></ResourceRecord></ResourceRecords></ResourceRecordSet></Change></Changes></ChangeBatch></ChangeResourceRecordSetsRequest>"""
CREATE_HEALTH_CHECK_PAYLOAD="""<CreateHealthCheckRequest xmlns="https://route53.amazonaws.com/doc/2013-04-01/"><CallerReference>foobar</CallerReference><HealthCheckConfig><IPAddress>192.168.10.0</IPAddress><Port>8888</Port><Type>HTTP</Type><ResourcePath>foo/bar</ResourcePath><FullyQualifiedDomainName>foobar.com</FullyQualifiedDomainName></HealthCheckConfig></CreateHealthCheckRequest>"""


class TestRoute53Operations(BaseSessionTest):

    def setUp(self):
        super(TestRoute53Operations, self).setUp()
        self.environ['AWS_ACCESS_KEY_ID'] = 'foo'
        self.environ['AWS_SECRET_ACCESS_KEY'] = 'bar'
        self.route53 = self.session.get_service('route53')
        self.endpoint = self.route53.get_endpoint('us-east-1')
        self.hosted_zone_name = 'foobar.com'

    def test_create_hosted_zone(self):
        op = self.route53.get_operation('CreateHostedZone')
        hzc = {'Comment': 'blahblahblah'}
        params = op.build_parameters(name=self.hosted_zone_name,
                                     caller_reference='foobar',
                                     hosted_zone_config=hzc)
        self.maxDiff = None
        self.assertEqual(params['payload'].getvalue(),
                         CREATE_HOSTED_ZONE_PAYLOAD)

    def test_create_resource_record_sets(self):
        op = self.route53.get_operation('ChangeResourceRecordSets')
        batch = {"Comment": "Adding TXT record",
                 "Changes": [{"Action":"CREATE",
                              "ResourceRecordSet":{
                                "Name":"midocs.com",
                                "Type":"TXT",
                                "TTL":600,
                                "ResourceRecords":[
                                  {"Value":"\"v=foobar\""}]}}]}
        params = op.build_parameters(hosted_zone_id='1111',
                                     change_batch=batch)
        self.maxDiff = None
        self.assertEqual(params['payload'].getvalue(),
                         CREATE_RRSET_PAYLOAD)

    def test_delete_resource_record_sets(self):
        op = self.route53.get_operation('ChangeResourceRecordSets')
        batch = {"Comment": "Adding TXT record",
                 "Changes": [{"Action":"DELETE",
                              "ResourceRecordSet":{
                                "Name":"midocs.com",
                                "Type":"TXT",
                                "TTL":600,
                                "ResourceRecords":[
                                  {"Value":"\"v=foobar\""}]}}]}
        params = op.build_parameters(hosted_zone_id='1111',
                                     change_batch=batch)
        self.maxDiff = None
        self.assertEqual(params['payload'].getvalue(),
                         DELETE_RRSET_PAYLOAD)

    def test_create_healthcheck(self):
        op = self.route53.get_operation('CreateHealthCheck')
        hc_config = {'IPAddress': '192.168.10.0',
                     'Port': 8888,
                     'Type': 'HTTP',
                     'ResourcePath': 'foo/bar',
                     'FullyQualifiedDomainName': 'foobar.com'}
        params = op.build_parameters(caller_reference='foobar',
                                     health_check_config=hc_config)
        self.maxDiff = None
        self.assertEqual(params['payload'].getvalue(),
                         CREATE_HEALTH_CHECK_PAYLOAD)
