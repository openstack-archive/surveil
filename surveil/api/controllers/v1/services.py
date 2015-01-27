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

from surveil.api.controllers.v1.datamodel import service


class ServicesController(rest.RestController):

    @wsme_pecan.wsexpose([service.Service])
    def get_all(self):
        """Returns all services."""
        services = [
            s for s
            in pecan.request.mongo_connection.
            # Don't return templates
            shinken.services.find({"register": {"$ne": "0"}})
        ]

        return [service.Service(**s) for s in services]

    @wsme_pecan.wsexpose(service.Service,
                         body=service.Service,
                         status_code=201)
    def post(self, data):
        """Create a new service.

        :param data: a service within the request body.
        """
        pecan.request.mongo_connection.shinken.services.insert(
            data.as_dict()
        )
