# Copyright 2015 - Savoir-Faire Linux inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import copy
import json


from surveil.api.datamodel.config import servicegroup
from surveil.tests.api import functionalTest


class TestServiceGroupsController(functionalTest.FunctionalTest):

    def setUp(self):
        super(TestServiceGroupsController, self).setUp()
        self.groups = [
            {
                'servicegroup_name': 'dbservices',
                'members': ['service1'],
                'servicegroup_members': []
            },
            {
                'servicegroup_name': 'otherservices',
                'members': ['service1',
                            'service2'],
                'servicegroup_members': []
            },
        ]
        self.mongoconnection.shinken.servicegroups.insert(
            copy.deepcopy(self.groups)
        )

        self.services = [
            {'service_description': "service1"},
            {'service_description': "service2"}
        ]
        self.mongoconnection.shinken.services.insert(
            copy.deepcopy(self.services)
        )

    def test_get_all_servicegroups(self):
        response = self.post_json('/v2/config/servicegroups', params={})

        self.assert_count_equal_backport(
            json.loads(response.body.decode()),
            self.groups
        )
        self.assertEqual(response.status_int, 200)

    def test_get_one_servicegroup(self):
        response = self.get('/v2/config/servicegroups/dbservices')

        self.assertEqual(
            json.loads(response.body.decode()),
            self.groups[0]
        )

    def test_create_servicegroup(self):
        s = servicegroup.ServiceGroup(
            servicegroup_name='John',
            members=['service1'],
        )

        self.put_json('/v2/config/servicegroups', s.as_dict())

        self.assertIsNotNone(
            self.mongoconnection.shinken.servicegroups.find_one(s.as_dict())
        )

    def test_delete_servicegroup(self):
        self.assertIsNotNone(
            self.mongoconnection.shinken.servicegroups.find_one(self.groups[0])
        )

        self.delete('/v2/config/servicegroups/dbservices')

        self.assertIsNone(
            self.mongoconnection.shinken.servicegroups.find_one(self.groups[0])
        )

    def test_put_servicegroup(self):
        self.assertEqual(
            self.mongoconnection.shinken.servicegroups.find_one(
                {'servicegroup_name': 'dbservices'}
            )['members'],
            ['service1']
        )

        self.put_json(
            '/v2/config/servicegroups/dbservices',
            {"servicegroup_name": "dbservices",
             "members": ["service2"]}
        )

        self.assertEqual(
            self.mongoconnection.shinken.servicegroups.find_one(
                {'servicegroup_name': 'dbservices'}
            )['members'],
            ['service2']
        )
