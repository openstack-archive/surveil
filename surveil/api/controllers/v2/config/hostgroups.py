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
from surveil.api.datamodel import live_query as lq
from surveil.api.handlers.config import hostgroup_handler
from surveil.common import util


class HostGroupsController(rest.RestController):

    @pecan.expose()
    def _lookup(self, hostgroup_name, *remainder):
        return HostGroupController(hostgroup_name), remainder

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose([hostgroup.HostGroup], body=lq.LiveQuery)
    def post(self, data):
        """Returns all host groups."""
        handler = hostgroup_handler.HostGroupHandler(pecan.request)
        host_groups = handler.get_all(data)
        return host_groups

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(body=hostgroup.HostGroup, status_code=201)
    def put(self, data):
        """Create a new host group.

        :param data: a host group within the request body.
        """
        handler = hostgroup_handler.HostGroupHandler(pecan.request)
        handler.create(data)


class HostGroupController(rest.RestController):

    def __init__(self, hostgroup_name):
        pecan.request.context['hostgroup_name'] = hostgroup_name
        self._id = hostgroup_name

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(None, status_code=204)
    def delete(self):
        """Returns a specific host group."""
        handler = hostgroup_handler.HostGroupHandler(pecan.request)
        handler.delete({"hostgroup_name": self._id})

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(None,
                         body=hostgroup.HostGroup,
                         status_code=204)
    def put(self,  hostgroup):
        """Update a specific host group."""
        handler = hostgroup_handler.HostGroupHandler(pecan.request)
        handler.update({"hostgroup_name": self._id}, hostgroup)

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(hostgroup.HostGroup, wtypes.text)
    def get(self):
        """Returns a host group."""
        handler = hostgroup_handler.HostGroupHandler(pecan.request)
        hostgroup = handler.get({"hostgroup_name": self._id})
        return hostgroup