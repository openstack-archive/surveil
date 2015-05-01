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

import pecan
from pecan import rest
import wsmeext.pecan as wsme_pecan

from surveil.api.datamodel.config import service
from surveil.api.handlers.config import service_handler
from surveil.common import util


class ServicesController(rest.RestController):

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose([service.Service])
    def get_all(self):
        """Returns all services."""
        handler = service_handler.ServiceHandler(pecan.request)
        services = handler.get_all()
        return services

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(service.Service,
                         body=service.Service,
                         status_code=201)
    def post(self, data):
        """Create a new service.

        :param data: a service within the request body.
        """
        handler = service_handler.ServiceHandler(pecan.request)
        services = handler.create(data)
        return services
