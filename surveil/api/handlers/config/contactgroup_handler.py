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

from surveil.api.datamodel.config import contactgroup
from surveil.api.handlers import handler


class ContactGroupHandler(handler.Handler):
    """Fulfills a request on the contact group resource."""

    def get(self, group_name):
        """Return a contact group."""

        g = self.request.mongo_connection.shinken.contactgroups.find_one(
            {"contactgroup_name": group_name}, {'_id': 0}
        )
        return contactgroup.ContactGroup(**g)

    def update(self, group_name, group):
        """Modify an existing contact group."""
        group_dict = group.as_dict()
        if "contactgroup_name" not in group_dict.keys():
            group_dict['contactgroup_name'] = group_name

        self.request.mongo_connection.shinken.contactgroups.update(
            {"contactgroup_name": group_name},
            {"$set": group_dict},
            upsert=True
        )

    def delete(self, group_name):
        """Delete existing contact group."""
        self.request.mongo_connection.shinken.contactgroups.remove(
            {"contactgroup_name": group_name}
        )

    def create(self, group):
        """Create a new contact group."""
        self.request.mongo_connection.shinken.contactgroups.insert(
            group.as_dict()
        )

    def get_all(self):
        """Return all contact groups."""
        contactgroups = [g for g
                         in self.request.mongo_connection.
                         shinken.contactgroups.find(
                             {"register": {"$ne": "0"}},
                             {'_id': 0}
                         )]
        contactgroups = [contactgroup.ContactGroup(**g) for g in contactgroups]
        return contactgroups
