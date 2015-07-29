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

from surveil.api.datamodel.config import contact
from surveil.api.datamodel import live_query as lq
from surveil.api.handlers.config import contact_handler
from surveil.common import util


class ContactsController(rest.RestController):

    @pecan.expose()
    def _lookup(self, contact_name, *remainder):
        return ContactController(contact_name), remainder

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose([contact.Contact], body=lq.LiveQuery)
    def post(self, data):
        """Returns all contacts."""
        handler = contact_handler.ContactHandler(pecan.request)
        hosts = handler.get_all(data)
        return hosts

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(body=contact.Contact, status_code=201)
    def put(self, data):
        """Create a new contact.

        :param data: a contact within the request body.
        """
        handler = contact_handler.ContactHandler(pecan.request)
        handler.create(data)


class ContactController(rest.RestController):

    def __init__(self, contact_name):
        pecan.request.context['contact_name'] = contact_name
        self._id = contact_name

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(None, status_code=204)
    def delete(self):
        """Returns a specific contact."""
        handler = contact_handler.ContactHandler(pecan.request)
        handler.delete({"contact_name": self._id})

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(None,
                         body=contact.Contact,
                         status_code=204)
    def put(self, contact):
        """Returns a specific contact."""
        handler = contact_handler.ContactHandler(pecan.request)
        handler.update({"contact_name": self._id}, contact)

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(contact.Contact, wtypes.text)
    def get(self):
        """Returns a specific contact."""
        handler = contact_handler.ContactHandler(pecan.request)
        contact = handler.get({"contact_name": self._id})
        return contact