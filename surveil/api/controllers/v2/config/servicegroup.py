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

from surveil.api.datamodel.config import servicegroup
from surveil.api.handlers.config import servicegroup_handler
from surveil.common import util


class ServiceGroupsController(rest.RestController):

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose([servicegroup.ServiceGroup])
    def get_all(self):
        """Returns all service groups."""
        handler = servicegroup_handler.ServiceGroupHandler(pecan.request)
        service_groups = handler.get_all()
        return service_groups

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(servicegroup.ServiceGroup, wtypes.text)
    def get_one(self, group_name):
        """Returns a service group."""
        handler = servicegroup_handler.ServiceGroupHandler(pecan.request)
        servicegroup = handler.get(group_name)
        return servicegroup

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(body=servicegroup.ServiceGroup, status_code=201)
    def post(self, data):
        """Create a new service group.

        :param data: a service group within the request body.
        """
        handler = servicegroup_handler.ServiceGroupHandler(pecan.request)
        handler.create(data)

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(servicegroup.ServiceGroup, wtypes.text,
                         status_code=204)
    def delete(self, group_name):
        """Returns a specific service group."""
        handler = servicegroup_handler.ServiceGroupHandler(pecan.request)
        handler.delete(group_name)

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(servicegroup.ServiceGroup,
                         wtypes.text,
                         body=servicegroup.ServiceGroup,
                         status_code=204)
    def put(self, group_name, servicegroup):
        """Update a specific service group."""
        handler = servicegroup_handler.ServiceGroupHandler(pecan.request)
        handler.update(group_name, servicegroup)
