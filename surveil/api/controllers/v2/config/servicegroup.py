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
from surveil.api.datamodel import live_query as lq
from surveil.api.handlers.config import servicegroup_handler
from surveil.common import util


class ServiceGroupsController(rest.RestController):

    @pecan.expose()
    def _lookup(self, servicegroup_name, *remainder):
        return ServiceGroupController(servicegroup_name), remainder

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose([servicegroup.ServiceGroup], body=lq.LiveQuery)
    def post(self, data):
        """Returns all service groups."""
        handler = servicegroup_handler.ServiceGroupHandler(pecan.request)
        service_groups = handler.get_all(data)
        return service_groups

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(body=servicegroup.ServiceGroup, status_code=201)
    def put(self, data):
        """Create a new service group.

        :param data: a service group within the request body.
        """
        handler = servicegroup_handler.ServiceGroupHandler(pecan.request)
        handler.create(data)


class ServiceGroupController(rest.RestController):

    def __init__(self, servicegroup_name):
        pecan.request.context['servicegroup_name'] = servicegroup_name
        self._id = servicegroup_name

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(None, status_code=204)
    def delete(self):
        """Returns a specific service group."""
        handler = servicegroup_handler.ServiceGroupHandler(pecan.request)
        handler.delete({"servicegroup_name": self._id})

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(None,
                         body=servicegroup.ServiceGroup,
                         status_code=204)
    def put(self, servicegroup):
        """Update a specific service group."""
        handler = servicegroup_handler.ServiceGroupHandler(pecan.request)
        handler.update({"servicegroup_name": self._id}, servicegroup)

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(servicegroup.ServiceGroup, wtypes.text)
    def get(self):
        """Returns a service group."""
        handler = servicegroup_handler.ServiceGroupHandler(pecan.request)
        servicegroup = handler.get({"servicegroup_name": self._id})
        return servicegroup