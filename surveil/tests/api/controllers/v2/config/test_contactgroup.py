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


from surveil.api.datamodel.config import contactgroup
from surveil.tests.api import functionalTest


class TestContactGroupsController(functionalTest.FunctionalTest):

    def setUp(self):
        super(TestContactGroupsController, self).setUp()
        self.groups = [
            {
                'contactgroup_name': 'novell-admins',
                'members': 'jdoe,rtobert,tzach',
            },
            {
                'contactgroup_name': 'linux-adminx',
                'members': 'linus,richard',
            },
        ]
        self.mongoconnection.shinken.contactgroups.insert(
            copy.deepcopy(self.groups)
        )

    def test_get_all_contactgroups(self):
        response = self.get('/v2/config/contactgroups')

        self.assert_count_equal_backport(
            json.loads(response.body.decode()),
            self.groups
        )
        self.assertEqual(response.status_int, 200)

    def test_get_one_contactgroup(self):
        response = self.get('/v2/config/contactgroups/novell-admins')

        self.assertEqual(
            json.loads(response.body.decode()),
            self.groups[0]
        )

    def test_create_contactgroup(self):
        g = contactgroup.ContactGroup(
            contactgroup_name='John',
            members="marie,bob,joe",
        )

        self.post_json('/v2/config/contactgroups', g.as_dict())

        self.assertIsNotNone(
            self.mongoconnection.shinken.contactgroups.find_one(g.as_dict())
        )

    def test_delete_contactgroup(self):
        self.assertIsNotNone(
            self.mongoconnection.shinken.contactgroups.find_one(self.groups[0])
        )

        self.delete('/v2/config/contactgroups/novell-admins')

        self.assertIsNone(
            self.mongoconnection.shinken.contactgroups.find_one(self.groups[0])
        )

    def test_put_contactgroup(self):
        self.assertEqual(
            self.mongoconnection.shinken.contactgroups.find_one(
                {'contactgroup_name': 'novell-admins'}
            )['members'],
            'jdoe,rtobert,tzach'
        )

        self.put_json(
            '/v2/config/contactgroups/novell-admins',
            {"contactgroup_name": "novell-admins",
             "members": "updated"}
        )

        self.assertEqual(
            self.mongoconnection.shinken.contactgroups.find_one(
                {'contactgroup_name': 'novell-admins'}
            )['members'],
            'updated'
        )
