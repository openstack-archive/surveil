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

from surveil.api.datamodel.config import realm
from surveil.api.handlers import handler


class RealmHandler(handler.Handler):
    """Fulfills a request on the realm resource."""

    def get(self, realm_name):
        """Return a realm."""

        r = self.request.mongo_connection.shinken.realms.find_one(
            {"realm_name": realm_name}, {'_id': 0}
        )
        return realm.Realm(**r)

    def update(self, realm_name, realm):
        """Modify an existing realm."""
        realm_dict = realm.as_dict()
        if "realm_name" not in realm_dict.keys():
            realm_dict['realm_name'] = realm_name

        self.request.mongo_connection.shinken.realms.update(
            {"realm_name": realm_name},
            {"$set": realm_dict},
            upsert=True
        )

    def delete(self, realm_name):
        """Delete existing realm."""
        self.request.mongo_connection.shinken.realms.remove(
            {"realm_name": realm_name}
        )

    def create(self, realm):
        """Create a new realm."""
        self.request.mongo_connection.shinken.realms.insert(
            realm.as_dict()
        )

    def get_all(self):
        """Return all realms."""
        realms = [c for c
                  in self.request.mongo_connection.
                  shinken.realms.find(
                      {"register": {"$ne": "0"}},  # Don't return templates
                      {'_id': 0}
                  )]
        realms = [realm.Realm(**r) for r in realms]
        return realms
