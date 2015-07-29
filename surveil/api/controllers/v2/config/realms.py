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
from surveil.api.datamodel import live_query as lq
from surveil.api.handlers.config import realm_handler
from surveil.common import util


class RealmsController(rest.RestController):

    @pecan.expose()
    def _lookup(self, realm_name, *remainder):
        return RealmController(realm_name), remainder

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose([realm.Realm], body=lq.LiveQuery)
    def post(self, data):
        """Returns all realms."""
        handler = realm_handler.RealmHandler(pecan.request)
        realms = handler.get_all(data)
        return realms

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(body=realm.Realm, status_code=201)
    def put(self, data):
        """Create a new realm.

        :param data: a realm within the request body.
        """
        handler = realm_handler.RealmHandler(pecan.request)
        handler.create(data)


class RealmController(rest.RestController):

    def __init__(self, realm_name):
        pecan.request.context['realm_name'] = realm_name
        self._id = realm_name

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(None, status_code=204)
    def delete(self):
        """Deletes a specific realm."""
        handler = realm_handler.RealmHandler(pecan.request)
        handler.delete({"realm_name": self._id})

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(None,
                         body=realm.Realm,
                         status_code=204)
    def put(self, realm):
        """Updates a specific realm."""
        handler = realm_handler.RealmHandler(pecan.request)
        handler.update(
            {"realm_name": self._id},
            realm
        )

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(realm.Realm, wtypes.text)
    def get(self):
        """Returns a specific realm."""
        handler = realm_handler.RealmHandler(pecan.request)
        realm = handler.get({"realm_name": self._id})
        return realm