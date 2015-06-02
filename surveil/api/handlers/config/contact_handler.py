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

from surveil.api.datamodel.config import contact
from surveil.api.handlers import handler


class ContactHandler(handler.Handler):
    """Fulfills a request on the contact resource."""

    def get(self, contact_name):
        """Return a contact."""

        c = self.request.mongo_connection.shinken.contacts.find_one(
            {"contact_name": contact_name}, {'_id': 0}
        )
        return contact.Contact(**c)

    def update(self, contact_name, contact):
        """Modify an existing contact."""
        contact_dict = contact.as_dict()
        if "contact_name" not in contact_dict.keys():
            contact_dict['contact_name'] = contact_name

        self.request.mongo_connection.shinken.contacts.update(
            {"contact_name": contact_name},
            {"$set": contact_dict},
            upsert=True
        )

    def delete(self, contact_name):
        """Delete existing contact."""
        self.request.mongo_connection.shinken.contacts.remove(
            {"contact_name": contact_name}
        )

    def create(self, contact):
        """Create a new contact."""
        self.request.mongo_connection.shinken.contacts.insert(
            contact.as_dict()
        )

    def get_all(self):
        """Return all contacts."""
        contacts = [c for c
                    in self.request.mongo_connection.
                    shinken.contacts.find(
                        {"register": {"$ne": "0"}},  # Don't return templates
                        {'_id': 0}
                    )]
        contacts = [contact.Contact(**c) for c in contacts]
        return contacts