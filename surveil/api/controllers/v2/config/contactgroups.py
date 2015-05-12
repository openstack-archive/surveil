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

from surveil.api.datamodel.config import contactgroup
from surveil.api.handlers.config import contactgroup_handler
from surveil.common import util


class ContactGroupsController(rest.RestController):

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose([contactgroup.ContactGroup])
    def get_all(self):
        """Returns all contact groups."""
        handler = contactgroup_handler.ContactGroupHandler(pecan.request)
        contact_groups = handler.get_all()
        return contact_groups

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(contactgroup.ContactGroup, wtypes.text)
    def get_one(self, group_name):
        """Returns a contact group."""
        handler = contactgroup_handler.ContactGroupHandler(pecan.request)
        contactgroup = handler.get(group_name)
        return contactgroup

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(body=contactgroup.ContactGroup, status_code=201)
    def post(self, data):
        """Create a new contact group.

        :param data: a contact group within the request body.
        """
        handler = contactgroup_handler.ContactGroupHandler(pecan.request)
        handler.create(data)

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(contactgroup.ContactGroup, wtypes.text,
                         status_code=204)
    def delete(self, group_name):
        """Delete a specific contact group."""
        handler = contactgroup_handler.ContactGroupHandler(pecan.request)
        handler.delete(group_name)

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(contactgroup.ContactGroup,
                         wtypes.text,
                         body=contactgroup.ContactGroup,
                         status_code=204)
    def put(self, group_name, contactgroup):
        """Update a specific contact group."""
        handler = contactgroup_handler.ContactGroupHandler(pecan.request)
        handler.update(group_name, contactgroup)
