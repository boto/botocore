#!/usr/bin/env python
# Copyright 2013 Google, Inc. or its affiliates. All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish, dis-
# tribute, sublicense, and/or sell copies of the Software, and to permit
# persons to whom the Software is furnished to do so, subject to the fol-
# lowing conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABIL-
# ITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT
# SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#

import botocore.session
import botocore.exceptions
import unittest



class TestAddresses(unittest.TestCase):

    def setUp(self):
        self.session = botocore.session.get_session()
        self.gce = self.session.get_service('gce')
        self.endpoint = self.gce.get_endpoint()

    def test_addresses_aggregatedList(self):
        op = self.gce.get_operation('compute.addresses.aggregatedList')
        params = op.build_parameters(project='project')
        self.assertTrue('project' in params['uri_params'])

    def test_addresses_aggregatedList_missing_params(self):
        op = self.gce.get_operation('compute.addresses.aggregatedList')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )

    def test_addresses_delete(self):
        op = self.gce.get_operation('compute.addresses.delete')
        params = op.build_parameters(project='project',
		region='region',
		address='address')
        self.assertTrue('project' in params['uri_params'])
        self.assertTrue('region' in params['uri_params'])
        self.assertTrue('address' in params['uri_params'])

    def test_addresses_delete_missing_params(self):
        op = self.gce.get_operation('compute.addresses.delete')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			region='region'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			address='address'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project',
			region='region'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project',
			address='address'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			region='region',
			address='address'
        )

    def test_addresses_get(self):
        op = self.gce.get_operation('compute.addresses.get')
        params = op.build_parameters(project='project',
		region='region',
		address='address')
        self.assertTrue('project' in params['uri_params'])
        self.assertTrue('region' in params['uri_params'])
        self.assertTrue('address' in params['uri_params'])

    def test_addresses_get_missing_params(self):
        op = self.gce.get_operation('compute.addresses.get')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			region='region'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			address='address'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project',
			region='region'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project',
			address='address'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			region='region',
			address='address'
        )

    def test_addresses_insert(self):
        op = self.gce.get_operation('compute.addresses.insert')
        params = op.build_parameters(body='body',
		project='project',
		region='region')
        self.assertTrue(params['payload'])
        self.assertTrue('project' in params['uri_params'])
        self.assertTrue('region' in params['uri_params'])

    def test_addresses_insert_missing_params(self):
        op = self.gce.get_operation('compute.addresses.insert')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			region='region'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			region='region'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project',
			region='region'
        )

    def test_addresses_list(self):
        op = self.gce.get_operation('compute.addresses.list')
        params = op.build_parameters(region='region',
		project='project')
        self.assertTrue('region' in params['uri_params'])
        self.assertTrue('project' in params['uri_params'])

    def test_addresses_list_missing_params(self):
        op = self.gce.get_operation('compute.addresses.list')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			region='region'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project'
        )

class TestDisks(unittest.TestCase):

    def setUp(self):
        self.session = botocore.session.get_session()
        self.gce = self.session.get_service('gce')
        self.endpoint = self.gce.get_endpoint()

    def test_disks_aggregatedList(self):
        op = self.gce.get_operation('compute.disks.aggregatedList')
        params = op.build_parameters(project='project')
        self.assertTrue('project' in params['uri_params'])

    def test_disks_aggregatedList_missing_params(self):
        op = self.gce.get_operation('compute.disks.aggregatedList')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )

    def test_disks_createSnapshot(self):
        op = self.gce.get_operation('compute.disks.createSnapshot')
        params = op.build_parameters(body='body',
		project='project',
		disk='disk',
		zone='zone')
        self.assertTrue(params['payload'])
        self.assertTrue('project' in params['uri_params'])
        self.assertTrue('disk' in params['uri_params'])
        self.assertTrue('zone' in params['uri_params'])

    def test_disks_createSnapshot_missing_params(self):
        op = self.gce.get_operation('compute.disks.createSnapshot')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			disk='disk'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			zone='zone'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			disk='disk'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			zone='zone'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project',
			disk='disk'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project',
			zone='zone'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			disk='disk',
			zone='zone'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			project='project',
			disk='disk'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			project='project',
			zone='zone'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			disk='disk',
			zone='zone'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project',
			disk='disk',
			zone='zone'
        )

    def test_disks_delete(self):
        op = self.gce.get_operation('compute.disks.delete')
        params = op.build_parameters(project='project',
		disk='disk',
		zone='zone')
        self.assertTrue('project' in params['uri_params'])
        self.assertTrue('disk' in params['uri_params'])
        self.assertTrue('zone' in params['uri_params'])

    def test_disks_delete_missing_params(self):
        op = self.gce.get_operation('compute.disks.delete')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			disk='disk'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			zone='zone'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project',
			disk='disk'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project',
			zone='zone'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			disk='disk',
			zone='zone'
        )

    def test_disks_get(self):
        op = self.gce.get_operation('compute.disks.get')
        params = op.build_parameters(project='project',
		disk='disk',
		zone='zone')
        self.assertTrue('project' in params['uri_params'])
        self.assertTrue('disk' in params['uri_params'])
        self.assertTrue('zone' in params['uri_params'])

    def test_disks_get_missing_params(self):
        op = self.gce.get_operation('compute.disks.get')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			disk='disk'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			zone='zone'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project',
			disk='disk'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project',
			zone='zone'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			disk='disk',
			zone='zone'
        )

    def test_disks_insert(self):
        op = self.gce.get_operation('compute.disks.insert')
        params = op.build_parameters(body='body',
		project='project',
		zone='zone')
        self.assertTrue(params['payload'])
        self.assertTrue('project' in params['uri_params'])
        self.assertTrue('zone' in params['uri_params'])

    def test_disks_insert_missing_params(self):
        op = self.gce.get_operation('compute.disks.insert')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			zone='zone'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			zone='zone'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project',
			zone='zone'
        )

    def test_disks_list(self):
        op = self.gce.get_operation('compute.disks.list')
        params = op.build_parameters(project='project',
		zone='zone')
        self.assertTrue('project' in params['uri_params'])
        self.assertTrue('zone' in params['uri_params'])

    def test_disks_list_missing_params(self):
        op = self.gce.get_operation('compute.disks.list')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			zone='zone'
        )

class TestFirewalls(unittest.TestCase):

    def setUp(self):
        self.session = botocore.session.get_session()
        self.gce = self.session.get_service('gce')
        self.endpoint = self.gce.get_endpoint()

    def test_firewalls_delete(self):
        op = self.gce.get_operation('compute.firewalls.delete')
        params = op.build_parameters(firewall='firewall',
		project='project')
        self.assertTrue('firewall' in params['uri_params'])
        self.assertTrue('project' in params['uri_params'])

    def test_firewalls_delete_missing_params(self):
        op = self.gce.get_operation('compute.firewalls.delete')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			firewall='firewall'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project'
        )

    def test_firewalls_get(self):
        op = self.gce.get_operation('compute.firewalls.get')
        params = op.build_parameters(firewall='firewall',
		project='project')
        self.assertTrue('firewall' in params['uri_params'])
        self.assertTrue('project' in params['uri_params'])

    def test_firewalls_get_missing_params(self):
        op = self.gce.get_operation('compute.firewalls.get')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			firewall='firewall'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project'
        )

    def test_firewalls_insert(self):
        op = self.gce.get_operation('compute.firewalls.insert')
        params = op.build_parameters(body='body',
		project='project')
        self.assertTrue(params['payload'])
        self.assertTrue('project' in params['uri_params'])

    def test_firewalls_insert_missing_params(self):
        op = self.gce.get_operation('compute.firewalls.insert')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project'
        )

    def test_firewalls_list(self):
        op = self.gce.get_operation('compute.firewalls.list')
        params = op.build_parameters(project='project')
        self.assertTrue('project' in params['uri_params'])

    def test_firewalls_list_missing_params(self):
        op = self.gce.get_operation('compute.firewalls.list')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )

    def test_firewalls_patch(self):
        op = self.gce.get_operation('compute.firewalls.patch')
        params = op.build_parameters(body='body',
		firewall='firewall',
		project='project')
        self.assertTrue(params['payload'])
        self.assertTrue('firewall' in params['uri_params'])
        self.assertTrue('project' in params['uri_params'])

    def test_firewalls_patch_missing_params(self):
        op = self.gce.get_operation('compute.firewalls.patch')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			firewall='firewall'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			firewall='firewall'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			firewall='firewall',
			project='project'
        )

    def test_firewalls_update(self):
        op = self.gce.get_operation('compute.firewalls.update')
        params = op.build_parameters(body='body',
		firewall='firewall',
		project='project')
        self.assertTrue(params['payload'])
        self.assertTrue('firewall' in params['uri_params'])
        self.assertTrue('project' in params['uri_params'])

    def test_firewalls_update_missing_params(self):
        op = self.gce.get_operation('compute.firewalls.update')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			firewall='firewall'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			firewall='firewall'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			firewall='firewall',
			project='project'
        )

class TestGlobaloperations(unittest.TestCase):

    def setUp(self):
        self.session = botocore.session.get_session()
        self.gce = self.session.get_service('gce')
        self.endpoint = self.gce.get_endpoint()

    def test_globalOperations_aggregatedList(self):
        op = self.gce.get_operation('compute.globalOperations.aggregatedList')
        params = op.build_parameters(project='project')
        self.assertTrue('project' in params['uri_params'])

    def test_globalOperations_aggregatedList_missing_params(self):
        op = self.gce.get_operation('compute.globalOperations.aggregatedList')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )

    def test_globalOperations_delete(self):
        op = self.gce.get_operation('compute.globalOperations.delete')
        params = op.build_parameters(project='project',
		operation='operation')
        self.assertTrue('project' in params['uri_params'])
        self.assertTrue('operation' in params['uri_params'])

    def test_globalOperations_delete_missing_params(self):
        op = self.gce.get_operation('compute.globalOperations.delete')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			operation='operation'
        )

    def test_globalOperations_get(self):
        op = self.gce.get_operation('compute.globalOperations.get')
        params = op.build_parameters(project='project',
		operation='operation')
        self.assertTrue('project' in params['uri_params'])
        self.assertTrue('operation' in params['uri_params'])

    def test_globalOperations_get_missing_params(self):
        op = self.gce.get_operation('compute.globalOperations.get')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			operation='operation'
        )

    def test_globalOperations_list(self):
        op = self.gce.get_operation('compute.globalOperations.list')
        params = op.build_parameters(project='project')
        self.assertTrue('project' in params['uri_params'])

    def test_globalOperations_list_missing_params(self):
        op = self.gce.get_operation('compute.globalOperations.list')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )

class TestImages(unittest.TestCase):

    def setUp(self):
        self.session = botocore.session.get_session()
        self.gce = self.session.get_service('gce')
        self.endpoint = self.gce.get_endpoint()

    def test_images_delete(self):
        op = self.gce.get_operation('compute.images.delete')
        params = op.build_parameters(project='project',
		image='image')
        self.assertTrue('project' in params['uri_params'])
        self.assertTrue('image' in params['uri_params'])

    def test_images_delete_missing_params(self):
        op = self.gce.get_operation('compute.images.delete')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			image='image'
        )

    def test_images_deprecate(self):
        op = self.gce.get_operation('compute.images.deprecate')
        params = op.build_parameters(body='body',
		project='project',
		image='image')
        self.assertTrue(params['payload'])
        self.assertTrue('project' in params['uri_params'])
        self.assertTrue('image' in params['uri_params'])

    def test_images_deprecate_missing_params(self):
        op = self.gce.get_operation('compute.images.deprecate')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			image='image'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			image='image'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project',
			image='image'
        )

    def test_images_get(self):
        op = self.gce.get_operation('compute.images.get')
        params = op.build_parameters(project='project',
		image='image')
        self.assertTrue('project' in params['uri_params'])
        self.assertTrue('image' in params['uri_params'])

    def test_images_get_missing_params(self):
        op = self.gce.get_operation('compute.images.get')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			image='image'
        )

    def test_images_insert(self):
        op = self.gce.get_operation('compute.images.insert')
        params = op.build_parameters(body='body',
		project='project')
        self.assertTrue(params['payload'])
        self.assertTrue('project' in params['uri_params'])

    def test_images_insert_missing_params(self):
        op = self.gce.get_operation('compute.images.insert')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project'
        )

    def test_images_list(self):
        op = self.gce.get_operation('compute.images.list')
        params = op.build_parameters(project='project')
        self.assertTrue('project' in params['uri_params'])

    def test_images_list_missing_params(self):
        op = self.gce.get_operation('compute.images.list')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )

class TestInstances(unittest.TestCase):

    def setUp(self):
        self.session = botocore.session.get_session()
        self.gce = self.session.get_service('gce')
        self.endpoint = self.gce.get_endpoint()

    def test_instances_addAccessConfig(self):
        op = self.gce.get_operation('compute.instances.addAccessConfig')
        params = op.build_parameters(body='body',
		instance='instance',
		zone='zone',
		project='project',
		network_interface='network_interface')
        self.assertTrue(params['payload'])
        self.assertTrue('instance' in params['uri_params'])
        self.assertTrue('zone' in params['uri_params'])
        self.assertTrue('project' in params['uri_params'])
        self.assertTrue('networkInterface' in params['uri_params'])

    def test_instances_addAccessConfig_missing_params(self):
        op = self.gce.get_operation('compute.instances.addAccessConfig')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			instance='instance'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			zone='zone'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			network_interface='network_interface'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			instance='instance'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			zone='zone'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			network_interface='network_interface'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			instance='instance',
			zone='zone'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			instance='instance',
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			instance='instance',
			network_interface='network_interface'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			zone='zone',
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			zone='zone',
			network_interface='network_interface'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project',
			network_interface='network_interface'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			instance='instance',
			zone='zone'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			instance='instance',
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			instance='instance',
			network_interface='network_interface'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			zone='zone',
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			zone='zone',
			network_interface='network_interface'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			project='project',
			network_interface='network_interface'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			instance='instance',
			zone='zone',
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			instance='instance',
			zone='zone',
			network_interface='network_interface'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			instance='instance',
			project='project',
			network_interface='network_interface'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			zone='zone',
			project='project',
			network_interface='network_interface'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			instance='instance',
			zone='zone',
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			instance='instance',
			zone='zone',
			network_interface='network_interface'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			instance='instance',
			project='project',
			network_interface='network_interface'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			zone='zone',
			project='project',
			network_interface='network_interface'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			instance='instance',
			zone='zone',
			project='project',
			network_interface='network_interface'
        )

    def test_instances_aggregatedList(self):
        op = self.gce.get_operation('compute.instances.aggregatedList')
        params = op.build_parameters(project='project')
        self.assertTrue('project' in params['uri_params'])

    def test_instances_aggregatedList_missing_params(self):
        op = self.gce.get_operation('compute.instances.aggregatedList')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )

    def test_instances_attachDisk(self):
        op = self.gce.get_operation('compute.instances.attachDisk')
        params = op.build_parameters(body='body',
		instance='instance',
		zone='zone',
		project='project')
        self.assertTrue(params['payload'])
        self.assertTrue('instance' in params['uri_params'])
        self.assertTrue('zone' in params['uri_params'])
        self.assertTrue('project' in params['uri_params'])

    def test_instances_attachDisk_missing_params(self):
        op = self.gce.get_operation('compute.instances.attachDisk')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			instance='instance'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			zone='zone'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			instance='instance'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			zone='zone'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			instance='instance',
			zone='zone'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			instance='instance',
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			zone='zone',
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			instance='instance',
			zone='zone'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			instance='instance',
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			zone='zone',
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			instance='instance',
			zone='zone',
			project='project'
        )

    def test_instances_delete(self):
        op = self.gce.get_operation('compute.instances.delete')
        params = op.build_parameters(project='project',
		instance='instance',
		zone='zone')
        self.assertTrue('project' in params['uri_params'])
        self.assertTrue('instance' in params['uri_params'])
        self.assertTrue('zone' in params['uri_params'])

    def test_instances_delete_missing_params(self):
        op = self.gce.get_operation('compute.instances.delete')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			instance='instance'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			zone='zone'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project',
			instance='instance'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project',
			zone='zone'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			instance='instance',
			zone='zone'
        )

    def test_instances_deleteAccessConfig(self):
        op = self.gce.get_operation('compute.instances.deleteAccessConfig')
        params = op.build_parameters(access_config='access_config',
		instance='instance',
		zone='zone',
		project='project',
		network_interface='network_interface')
        self.assertTrue('accessConfig' in params['uri_params'])
        self.assertTrue('instance' in params['uri_params'])
        self.assertTrue('zone' in params['uri_params'])
        self.assertTrue('project' in params['uri_params'])
        self.assertTrue('networkInterface' in params['uri_params'])

    def test_instances_deleteAccessConfig_missing_params(self):
        op = self.gce.get_operation('compute.instances.deleteAccessConfig')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			access_config='access_config'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			instance='instance'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			zone='zone'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			network_interface='network_interface'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			access_config='access_config',
			instance='instance'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			access_config='access_config',
			zone='zone'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			access_config='access_config',
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			access_config='access_config',
			network_interface='network_interface'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			instance='instance',
			zone='zone'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			instance='instance',
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			instance='instance',
			network_interface='network_interface'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			zone='zone',
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			zone='zone',
			network_interface='network_interface'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project',
			network_interface='network_interface'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			access_config='access_config',
			instance='instance',
			zone='zone'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			access_config='access_config',
			instance='instance',
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			access_config='access_config',
			instance='instance',
			network_interface='network_interface'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			access_config='access_config',
			zone='zone',
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			access_config='access_config',
			zone='zone',
			network_interface='network_interface'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			access_config='access_config',
			project='project',
			network_interface='network_interface'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			instance='instance',
			zone='zone',
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			instance='instance',
			zone='zone',
			network_interface='network_interface'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			instance='instance',
			project='project',
			network_interface='network_interface'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			zone='zone',
			project='project',
			network_interface='network_interface'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			access_config='access_config',
			instance='instance',
			zone='zone',
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			access_config='access_config',
			instance='instance',
			zone='zone',
			network_interface='network_interface'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			access_config='access_config',
			instance='instance',
			project='project',
			network_interface='network_interface'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			access_config='access_config',
			zone='zone',
			project='project',
			network_interface='network_interface'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			instance='instance',
			zone='zone',
			project='project',
			network_interface='network_interface'
        )

    def test_instances_detachDisk(self):
        op = self.gce.get_operation('compute.instances.detachDisk')
        params = op.build_parameters(project='project',
		device_name='device_name',
		zone='zone',
		instance='instance')
        self.assertTrue('project' in params['uri_params'])
        self.assertTrue('deviceName' in params['uri_params'])
        self.assertTrue('zone' in params['uri_params'])
        self.assertTrue('instance' in params['uri_params'])

    def test_instances_detachDisk_missing_params(self):
        op = self.gce.get_operation('compute.instances.detachDisk')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			device_name='device_name'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			zone='zone'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			instance='instance'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project',
			device_name='device_name'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project',
			zone='zone'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project',
			instance='instance'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			device_name='device_name',
			zone='zone'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			device_name='device_name',
			instance='instance'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			zone='zone',
			instance='instance'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project',
			device_name='device_name',
			zone='zone'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project',
			device_name='device_name',
			instance='instance'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project',
			zone='zone',
			instance='instance'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			device_name='device_name',
			zone='zone',
			instance='instance'
        )

    def test_instances_get(self):
        op = self.gce.get_operation('compute.instances.get')
        params = op.build_parameters(project='project',
		instance='instance',
		zone='zone')
        self.assertTrue('project' in params['uri_params'])
        self.assertTrue('instance' in params['uri_params'])
        self.assertTrue('zone' in params['uri_params'])

    def test_instances_get_missing_params(self):
        op = self.gce.get_operation('compute.instances.get')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			instance='instance'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			zone='zone'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project',
			instance='instance'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project',
			zone='zone'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			instance='instance',
			zone='zone'
        )

    def test_instances_getSerialPortOutput(self):
        op = self.gce.get_operation('compute.instances.getSerialPortOutput')
        params = op.build_parameters(project='project',
		instance='instance',
		zone='zone')
        self.assertTrue('project' in params['uri_params'])
        self.assertTrue('instance' in params['uri_params'])
        self.assertTrue('zone' in params['uri_params'])

    def test_instances_getSerialPortOutput_missing_params(self):
        op = self.gce.get_operation('compute.instances.getSerialPortOutput')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			instance='instance'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			zone='zone'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project',
			instance='instance'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project',
			zone='zone'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			instance='instance',
			zone='zone'
        )

    def test_instances_insert(self):
        op = self.gce.get_operation('compute.instances.insert')
        params = op.build_parameters(body='body',
		project='project',
		zone='zone')
        self.assertTrue(params['payload'])
        self.assertTrue('project' in params['uri_params'])
        self.assertTrue('zone' in params['uri_params'])

    def test_instances_insert_missing_params(self):
        op = self.gce.get_operation('compute.instances.insert')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			zone='zone'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			zone='zone'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project',
			zone='zone'
        )

    def test_instances_list(self):
        op = self.gce.get_operation('compute.instances.list')
        params = op.build_parameters(project='project',
		zone='zone')
        self.assertTrue('project' in params['uri_params'])
        self.assertTrue('zone' in params['uri_params'])

    def test_instances_list_missing_params(self):
        op = self.gce.get_operation('compute.instances.list')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			zone='zone'
        )

    def test_instances_setMetadata(self):
        op = self.gce.get_operation('compute.instances.setMetadata')
        params = op.build_parameters(body='body',
		instance='instance',
		zone='zone',
		project='project')
        self.assertTrue(params['payload'])
        self.assertTrue('instance' in params['uri_params'])
        self.assertTrue('zone' in params['uri_params'])
        self.assertTrue('project' in params['uri_params'])

    def test_instances_setMetadata_missing_params(self):
        op = self.gce.get_operation('compute.instances.setMetadata')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			instance='instance'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			zone='zone'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			instance='instance'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			zone='zone'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			instance='instance',
			zone='zone'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			instance='instance',
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			zone='zone',
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			instance='instance',
			zone='zone'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			instance='instance',
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			zone='zone',
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			instance='instance',
			zone='zone',
			project='project'
        )

    def test_instances_setTags(self):
        op = self.gce.get_operation('compute.instances.setTags')
        params = op.build_parameters(body='body',
		instance='instance',
		zone='zone',
		project='project')
        self.assertTrue(params['payload'])
        self.assertTrue('instance' in params['uri_params'])
        self.assertTrue('zone' in params['uri_params'])
        self.assertTrue('project' in params['uri_params'])

    def test_instances_setTags_missing_params(self):
        op = self.gce.get_operation('compute.instances.setTags')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			instance='instance'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			zone='zone'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			instance='instance'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			zone='zone'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			instance='instance',
			zone='zone'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			instance='instance',
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			zone='zone',
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			instance='instance',
			zone='zone'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			instance='instance',
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body',
			zone='zone',
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			instance='instance',
			zone='zone',
			project='project'
        )

class TestKernels(unittest.TestCase):

    def setUp(self):
        self.session = botocore.session.get_session()
        self.gce = self.session.get_service('gce')
        self.endpoint = self.gce.get_endpoint()

    def test_kernels_get(self):
        op = self.gce.get_operation('compute.kernels.get')
        params = op.build_parameters(project='project',
		kernel='kernel')
        self.assertTrue('project' in params['uri_params'])
        self.assertTrue('kernel' in params['uri_params'])

    def test_kernels_get_missing_params(self):
        op = self.gce.get_operation('compute.kernels.get')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			kernel='kernel'
        )

    def test_kernels_list(self):
        op = self.gce.get_operation('compute.kernels.list')
        params = op.build_parameters(project='project')
        self.assertTrue('project' in params['uri_params'])

    def test_kernels_list_missing_params(self):
        op = self.gce.get_operation('compute.kernels.list')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )

class TestMachinetypes(unittest.TestCase):

    def setUp(self):
        self.session = botocore.session.get_session()
        self.gce = self.session.get_service('gce')
        self.endpoint = self.gce.get_endpoint()

    def test_machineTypes_aggregatedList(self):
        op = self.gce.get_operation('compute.machineTypes.aggregatedList')
        params = op.build_parameters(project='project')
        self.assertTrue('project' in params['uri_params'])

    def test_machineTypes_aggregatedList_missing_params(self):
        op = self.gce.get_operation('compute.machineTypes.aggregatedList')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )

    def test_machineTypes_get(self):
        op = self.gce.get_operation('compute.machineTypes.get')
        params = op.build_parameters(project='project',
		machine_type='machine_type',
		zone='zone')
        self.assertTrue('project' in params['uri_params'])
        self.assertTrue('machineType' in params['uri_params'])
        self.assertTrue('zone' in params['uri_params'])

    def test_machineTypes_get_missing_params(self):
        op = self.gce.get_operation('compute.machineTypes.get')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			machine_type='machine_type'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			zone='zone'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project',
			machine_type='machine_type'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project',
			zone='zone'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			machine_type='machine_type',
			zone='zone'
        )

    def test_machineTypes_list(self):
        op = self.gce.get_operation('compute.machineTypes.list')
        params = op.build_parameters(project='project',
		zone='zone')
        self.assertTrue('project' in params['uri_params'])
        self.assertTrue('zone' in params['uri_params'])

    def test_machineTypes_list_missing_params(self):
        op = self.gce.get_operation('compute.machineTypes.list')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			zone='zone'
        )

class TestNetworks(unittest.TestCase):

    def setUp(self):
        self.session = botocore.session.get_session()
        self.gce = self.session.get_service('gce')
        self.endpoint = self.gce.get_endpoint()

    def test_networks_delete(self):
        op = self.gce.get_operation('compute.networks.delete')
        params = op.build_parameters(project='project',
		network='network')
        self.assertTrue('project' in params['uri_params'])
        self.assertTrue('network' in params['uri_params'])

    def test_networks_delete_missing_params(self):
        op = self.gce.get_operation('compute.networks.delete')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			network='network'
        )

    def test_networks_get(self):
        op = self.gce.get_operation('compute.networks.get')
        params = op.build_parameters(project='project',
		network='network')
        self.assertTrue('project' in params['uri_params'])
        self.assertTrue('network' in params['uri_params'])

    def test_networks_get_missing_params(self):
        op = self.gce.get_operation('compute.networks.get')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			network='network'
        )

    def test_networks_insert(self):
        op = self.gce.get_operation('compute.networks.insert')
        params = op.build_parameters(body='body',
		project='project')
        self.assertTrue(params['payload'])
        self.assertTrue('project' in params['uri_params'])

    def test_networks_insert_missing_params(self):
        op = self.gce.get_operation('compute.networks.insert')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project'
        )

    def test_networks_list(self):
        op = self.gce.get_operation('compute.networks.list')
        params = op.build_parameters(project='project')
        self.assertTrue('project' in params['uri_params'])

    def test_networks_list_missing_params(self):
        op = self.gce.get_operation('compute.networks.list')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )

class TestProjects(unittest.TestCase):

    def setUp(self):
        self.session = botocore.session.get_session()
        self.gce = self.session.get_service('gce')
        self.endpoint = self.gce.get_endpoint()

    def test_projects_get(self):
        op = self.gce.get_operation('compute.projects.get')
        params = op.build_parameters(project='project')
        self.assertTrue('project' in params['uri_params'])

    def test_projects_get_missing_params(self):
        op = self.gce.get_operation('compute.projects.get')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )

    def test_projects_setCommonInstanceMetadata(self):
        op = self.gce.get_operation('compute.projects.setCommonInstanceMetadata')
        params = op.build_parameters(body='body',
		project='project')
        self.assertTrue(params['payload'])
        self.assertTrue('project' in params['uri_params'])

    def test_projects_setCommonInstanceMetadata_missing_params(self):
        op = self.gce.get_operation('compute.projects.setCommonInstanceMetadata')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project'
        )

class TestRegionoperations(unittest.TestCase):

    def setUp(self):
        self.session = botocore.session.get_session()
        self.gce = self.session.get_service('gce')
        self.endpoint = self.gce.get_endpoint()

    def test_regionOperations_delete(self):
        op = self.gce.get_operation('compute.regionOperations.delete')
        params = op.build_parameters(project='project',
		operation='operation',
		region='region')
        self.assertTrue('project' in params['uri_params'])
        self.assertTrue('operation' in params['uri_params'])
        self.assertTrue('region' in params['uri_params'])

    def test_regionOperations_delete_missing_params(self):
        op = self.gce.get_operation('compute.regionOperations.delete')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			operation='operation'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			region='region'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project',
			operation='operation'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project',
			region='region'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			operation='operation',
			region='region'
        )

    def test_regionOperations_get(self):
        op = self.gce.get_operation('compute.regionOperations.get')
        params = op.build_parameters(project='project',
		operation='operation',
		region='region')
        self.assertTrue('project' in params['uri_params'])
        self.assertTrue('operation' in params['uri_params'])
        self.assertTrue('region' in params['uri_params'])

    def test_regionOperations_get_missing_params(self):
        op = self.gce.get_operation('compute.regionOperations.get')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			operation='operation'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			region='region'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project',
			operation='operation'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project',
			region='region'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			operation='operation',
			region='region'
        )

    def test_regionOperations_list(self):
        op = self.gce.get_operation('compute.regionOperations.list')
        params = op.build_parameters(region='region',
		project='project')
        self.assertTrue('region' in params['uri_params'])
        self.assertTrue('project' in params['uri_params'])

    def test_regionOperations_list_missing_params(self):
        op = self.gce.get_operation('compute.regionOperations.list')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			region='region'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project'
        )

class TestRegions(unittest.TestCase):

    def setUp(self):
        self.session = botocore.session.get_session()
        self.gce = self.session.get_service('gce')
        self.endpoint = self.gce.get_endpoint()

    def test_regions_get(self):
        op = self.gce.get_operation('compute.regions.get')
        params = op.build_parameters(project='project',
		region='region')
        self.assertTrue('project' in params['uri_params'])
        self.assertTrue('region' in params['uri_params'])

    def test_regions_get_missing_params(self):
        op = self.gce.get_operation('compute.regions.get')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			region='region'
        )

    def test_regions_list(self):
        op = self.gce.get_operation('compute.regions.list')
        params = op.build_parameters(project='project')
        self.assertTrue('project' in params['uri_params'])

    def test_regions_list_missing_params(self):
        op = self.gce.get_operation('compute.regions.list')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )

class TestRoutes(unittest.TestCase):

    def setUp(self):
        self.session = botocore.session.get_session()
        self.gce = self.session.get_service('gce')
        self.endpoint = self.gce.get_endpoint()

    def test_routes_delete(self):
        op = self.gce.get_operation('compute.routes.delete')
        params = op.build_parameters(project='project',
		route='route')
        self.assertTrue('project' in params['uri_params'])
        self.assertTrue('route' in params['uri_params'])

    def test_routes_delete_missing_params(self):
        op = self.gce.get_operation('compute.routes.delete')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			route='route'
        )

    def test_routes_get(self):
        op = self.gce.get_operation('compute.routes.get')
        params = op.build_parameters(project='project',
		route='route')
        self.assertTrue('project' in params['uri_params'])
        self.assertTrue('route' in params['uri_params'])

    def test_routes_get_missing_params(self):
        op = self.gce.get_operation('compute.routes.get')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			route='route'
        )

    def test_routes_insert(self):
        op = self.gce.get_operation('compute.routes.insert')
        params = op.build_parameters(body='body',
		project='project')
        self.assertTrue(params['payload'])
        self.assertTrue('project' in params['uri_params'])

    def test_routes_insert_missing_params(self):
        op = self.gce.get_operation('compute.routes.insert')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			body='body'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project'
        )

    def test_routes_list(self):
        op = self.gce.get_operation('compute.routes.list')
        params = op.build_parameters(project='project')
        self.assertTrue('project' in params['uri_params'])

    def test_routes_list_missing_params(self):
        op = self.gce.get_operation('compute.routes.list')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )

class TestSnapshots(unittest.TestCase):

    def setUp(self):
        self.session = botocore.session.get_session()
        self.gce = self.session.get_service('gce')
        self.endpoint = self.gce.get_endpoint()

    def test_snapshots_delete(self):
        op = self.gce.get_operation('compute.snapshots.delete')
        params = op.build_parameters(project='project',
		snapshot='snapshot')
        self.assertTrue('project' in params['uri_params'])
        self.assertTrue('snapshot' in params['uri_params'])

    def test_snapshots_delete_missing_params(self):
        op = self.gce.get_operation('compute.snapshots.delete')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			snapshot='snapshot'
        )

    def test_snapshots_get(self):
        op = self.gce.get_operation('compute.snapshots.get')
        params = op.build_parameters(project='project',
		snapshot='snapshot')
        self.assertTrue('project' in params['uri_params'])
        self.assertTrue('snapshot' in params['uri_params'])

    def test_snapshots_get_missing_params(self):
        op = self.gce.get_operation('compute.snapshots.get')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			snapshot='snapshot'
        )

    def test_snapshots_list(self):
        op = self.gce.get_operation('compute.snapshots.list')
        params = op.build_parameters(project='project')
        self.assertTrue('project' in params['uri_params'])

    def test_snapshots_list_missing_params(self):
        op = self.gce.get_operation('compute.snapshots.list')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )

class TestZoneoperations(unittest.TestCase):

    def setUp(self):
        self.session = botocore.session.get_session()
        self.gce = self.session.get_service('gce')
        self.endpoint = self.gce.get_endpoint()

    def test_zoneOperations_delete(self):
        op = self.gce.get_operation('compute.zoneOperations.delete')
        params = op.build_parameters(project='project',
		operation='operation',
		zone='zone')
        self.assertTrue('project' in params['uri_params'])
        self.assertTrue('operation' in params['uri_params'])
        self.assertTrue('zone' in params['uri_params'])

    def test_zoneOperations_delete_missing_params(self):
        op = self.gce.get_operation('compute.zoneOperations.delete')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			operation='operation'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			zone='zone'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project',
			operation='operation'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project',
			zone='zone'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			operation='operation',
			zone='zone'
        )

    def test_zoneOperations_get(self):
        op = self.gce.get_operation('compute.zoneOperations.get')
        params = op.build_parameters(project='project',
		operation='operation',
		zone='zone')
        self.assertTrue('project' in params['uri_params'])
        self.assertTrue('operation' in params['uri_params'])
        self.assertTrue('zone' in params['uri_params'])

    def test_zoneOperations_get_missing_params(self):
        op = self.gce.get_operation('compute.zoneOperations.get')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			operation='operation'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			zone='zone'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project',
			operation='operation'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project',
			zone='zone'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			operation='operation',
			zone='zone'
        )

    def test_zoneOperations_list(self):
        op = self.gce.get_operation('compute.zoneOperations.list')
        params = op.build_parameters(project='project',
		zone='zone')
        self.assertTrue('project' in params['uri_params'])
        self.assertTrue('zone' in params['uri_params'])

    def test_zoneOperations_list_missing_params(self):
        op = self.gce.get_operation('compute.zoneOperations.list')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			zone='zone'
        )

class TestZones(unittest.TestCase):

    def setUp(self):
        self.session = botocore.session.get_session()
        self.gce = self.session.get_service('gce')
        self.endpoint = self.gce.get_endpoint()

    def test_zones_get(self):
        op = self.gce.get_operation('compute.zones.get')
        params = op.build_parameters(project='project',
		zone='zone')
        self.assertTrue('project' in params['uri_params'])
        self.assertTrue('zone' in params['uri_params'])

    def test_zones_get_missing_params(self):
        op = self.gce.get_operation('compute.zones.get')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			project='project'
        )
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters,
			zone='zone'
        )

    def test_zones_list(self):
        op = self.gce.get_operation('compute.zones.list')
        params = op.build_parameters(project='project')
        self.assertTrue('project' in params['uri_params'])

    def test_zones_list_missing_params(self):
        op = self.gce.get_operation('compute.zones.list')
        self.assertRaises(
            botocore.exceptions.MissingParametersError,                
            op.build_parameters
        )