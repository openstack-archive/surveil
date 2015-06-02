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

from surveil.api.datamodel.config import servicegroup
from surveil.api.handlers import handler


class ServiceGroupHandler(handler.Handler):
    """Fulfills a request on the service group resource."""

    def get(self, group_name):
        """Return a service group."""

        s = self.request.mongo_connection.shinken.servicegroups.find_one(
            {"servicegroup_name": group_name}, {'_id': 0}
        )
        return servicegroup.ServiceGroup(**s)

    def update(self, group_name, group):
        """Modify an existing service group."""
        group_dict = group.as_dict()
        if "servicegroup_name" not in group_dict.keys():
            group_dict['servicegroup_name'] = group_name

        self.request.mongo_connection.shinken.servicegroups.update(
            {"servicegroup_name": group_name},
            {"$set": group_dict},
            upsert=True
        )

    def delete(self, group_name):
        """Delete existing service group."""
        self.request.mongo_connection.shinken.servicegroups.remove(
            {"servicegroup_name": group_name}
        )

    def create(self, group):
        """Create a new service group."""
        self.request.mongo_connection.shinken.servicegroups.insert(
            group.as_dict()
        )

    def get_all(self):
        """Return all service groups."""
        servicegroups = [c for c
                         in self.request.mongo_connection.
                         shinken.servicegroups.find(
                             {"register": {"$ne": "0"}},
                             {'_id': 0}
                         )]
        servicegroups = [servicegroup.ServiceGroup(**s) for s in servicegroups]
        return servicegroups
