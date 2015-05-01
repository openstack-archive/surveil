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


from surveil.api.datamodel.config import contact
from surveil.tests.api import functionalTest


class TestContactsController(functionalTest.FunctionalTest):

    def setUp(self):
        super(TestContactsController, self).setUp()
        self.contacts = [
            {
                'contact_name': 'bobby',
                'email': 'bob@bob.com'
            },
            {
                'contact_name': 'marie',
                'email': 'marie@marie.com'
            },
        ]
        self.mongoconnection.shinken.contacts.insert(
            copy.deepcopy(self.contacts)
        )

    def test_get_all_contacts(self):
        response = self.get('/v2/config/contacts')

        self.assert_count_equal_backport(
            json.loads(response.body.decode()),
            self.contacts
        )
        self.assertEqual(response.status_int, 200)

    def test_get_one_contact(self):
        response = self.get('/v2/config/contacts/bobby')

        self.assertEqual(
            json.loads(response.body.decode()),
            self.contacts[0]
        )

    def test_create_contact(self):
        c = contact.Contact(
            contact_name='John'
        )

        self.post_json('/v2/config/contacts', c.as_dict())

        self.assertIsNotNone(
            self.mongoconnection.shinken.contacts.find_one(c.as_dict())
        )

    def test_delete_contact(self):
        self.assertIsNotNone(
            self.mongoconnection.shinken.contacts.find_one(self.contacts[0])
        )

        self.delete('/v2/config/contacts/bobby')

        self.assertIsNone(
            self.mongoconnection.shinken.contacts.find_one(self.contacts[0])
        )

    def test_put_contact(self):
        self.assertEqual(
            self.mongoconnection.shinken.contacts.find_one(
                {'contact_name': 'bobby'}
            )['email'],
            'bob@bob.com'
        )

        self.put_json(
            '/v2/config/contacts/bobby',
            {"contact_name": "bobby", "email": "updated@bob.com"}
        )

        self.assertEqual(
            self.mongoconnection.shinken.contacts.find_one(
                {'contact_name': 'bobby'}
            )['email'],
            'updated@bob.com'
        )
