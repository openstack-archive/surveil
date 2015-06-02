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

from surveil.api.datamodel.config import service
from surveil.api.handlers import handler


class ServiceHandler(handler.Handler):
    """Fulfills a request on the service resource."""

    def get(self, host_name, service_description):
        """Return a service."""
        mongo_s = self.request.mongo_connection.shinken.services.find_one(
            {"host_name": host_name,
             "service_description": service_description}
        )
        return service.Service(**mongo_s)

    def update(self, id, data):
        """Modify existing host."""
        host_dict = data.as_dict()
        if "host_name" not in host_dict.keys():
            host_dict['host_name'] = id

        self.request.mongo_connection.shinken.hosts.update(
            {"host_name": id},
            {"$set": host_dict},
            upsert=True
        )

    def delete(self, host_name, service_description):
        """Delete existing service."""
        self.request.mongo_connection.shinken.services.remove(
            {"host_name": host_name,
             "service_description": service_description}
        )

    def create(self, data):
        """Create a new service."""
        self.request.mongo_connection.shinken.services.insert(
            data.as_dict()
        )

    def get_all(self, host_name=None):
        """Return all services."""
        filters = {"register": {"$ne": "0"}}

        if host_name is not None:
            filters['host_name'] = host_name

        services = [
            s for s
            in self.request.mongo_connection.
            # Don't return templates
            shinken.services.find(filters)
        ]
        return [service.Service(**s) for s in services]
