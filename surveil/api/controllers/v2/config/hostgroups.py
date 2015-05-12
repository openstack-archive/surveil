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

from surveil.api.datamodel.config import hostgroup
from surveil.api.handlers.config import hostgroup_handler
from surveil.common import util


class HostGroupsController(rest.RestController):

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose([hostgroup.HostGroup])
    def get_all(self):
        """Returns all host groups."""
        handler = hostgroup_handler.HostGroupHandler(pecan.request)
        host_groups = handler.get_all()
        return host_groups

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(hostgroup.HostGroup, wtypes.text)
    def get_one(self, group_name):
        """Returns a host group."""
        handler = hostgroup_handler.HostGroupHandler(pecan.request)
        hostgroup = handler.get(group_name)
        return hostgroup

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(body=hostgroup.HostGroup, status_code=201)
    def post(self, data):
        """Create a new host group.

        :param data: a host group within the request body.
        """
        handler = hostgroup_handler.HostGroupHandler(pecan.request)
        handler.create(data)

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(hostgroup.HostGroup, wtypes.text, status_code=204)
    def delete(self, group_name):
        """Returns a specific host group."""
        handler = hostgroup_handler.HostGroupHandler(pecan.request)
        handler.delete(group_name)

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(hostgroup.HostGroup,
                         wtypes.text,
                         body=hostgroup.HostGroup,
                         status_code=204)
    def put(self, group_name, hostgroup):
        """Update a specific host group."""
        handler = hostgroup_handler.HostGroupHandler(pecan.request)
        handler.update(group_name, hostgroup)
