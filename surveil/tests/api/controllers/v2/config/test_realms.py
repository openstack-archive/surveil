# Copyright 2014 - Savoir-Faire Linux inc.
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


from surveil.api.datamodel.config import realm
from surveil.tests.api import functionalTest


class TestRealmsController(functionalTest.FunctionalTest):

    def setUp(self):
        super(TestRealmsController, self).setUp()
        self.realms = [
            {
                'realm_name': 'World',
                'realm_members': 'Europe,America,Asia',
                'default': 0
            },
            {
                'realm_name': 'Anti-world',
                'realm_members': 'void,black-hole',
                'default': 1
            },
        ]
        self.mongoconnection.shinken.realms.insert(
            copy.deepcopy(self.realms)
        )

    def test_get_all_realms(self):
        response = self.get('/v2/config/realms')

        self.assert_count_equal_backport(
            json.loads(response.body.decode()),
            self.realms
        )
        self.assertEqual(response.status_int, 200)

    def test_get_one_realm(self):
        response = self.get('/v2/config/realms/World')

        self.assertEqual(
            json.loads(response.body.decode()),
            self.realms[0]
        )

    def test_create_realm(self):
        r = realm.Realm(
            realm_name='John',
            realm_members="marie,bob,joe",
            default=1
        )

        self.post_json('/v2/config/realms', r.as_dict())

        self.assertIsNotNone(
            self.mongoconnection.shinken.realms.find_one(r.as_dict())
        )

    def test_delete_realm(self):
        self.assertIsNotNone(
            self.mongoconnection.shinken.realms.find_one(self.realms[0])
        )

        self.delete('/v2/config/realms/World')

        self.assertIsNone(
            self.mongoconnection.shinken.realms.find_one(self.realms[0])
        )

    def test_put_realm(self):
        self.assertEqual(
            self.mongoconnection.shinken.realms.find_one(
                {'realm_name': 'World'}
            )['realm_members'],
            'Europe,America,Asia'
        )

        self.put_json(
            '/v2/config/realms/World',
            {"realm_name": "World",
             "realm_members": "updated",
             "default": 0}
        )

        self.assertEqual(
            self.mongoconnection.shinken.realms.find_one(
                {'realm_name': 'World'}
            )['realm_members'],
            'updated'
        )
