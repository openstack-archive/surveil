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


import pecan
from pecan import rest
import wsme.types as wtypes
import wsmeext.pecan as wsme_pecan

from surveil.api.datamodel.config import realm
from surveil.api.handlers.config import realm_handler
from surveil.common import util


class RealmsController(rest.RestController):

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose([realm.Realm])
    def get_all(self):
        """Returns all realms."""
        handler = realm_handler.RealmHandler(pecan.request)
        realms = handler.get_all()
        return realms

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(realm.Realm, wtypes.text)
    def get_one(self, realm_name):
        """Returns a specific realm."""
        handler = realm_handler.RealmHandler(pecan.request)
        realm = handler.get(realm_name)
        return realm

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(body=realm.Realm, status_code=201)
    def post(self, data):
        """Create a new realm.

        :param data: a realm within the request body.
        """
        handler = realm_handler.RealmHandler(pecan.request)
        handler.create(data)

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(realm.Realm, wtypes.text, status_code=204)
    def delete(self, realm_name):
        """Deletes a specific realm."""
        handler = realm_handler.RealmHandler(pecan.request)
        handler.delete(realm_name)

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(realm.Realm,
                         wtypes.text,
                         body=realm.Realm,
                         status_code=204)
    def put(self, realm_name, realm):
        """Updates a specific realm."""
        handler = realm_handler.RealmHandler(pecan.request)
        handler.update(realm_name, realm)
