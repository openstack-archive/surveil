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

from surveil.api.datamodel.config import hostgroup
from surveil.api.handlers import handler


class HostGroupHandler(handler.Handler):
    """Fulfills a request on the host group resource."""

    def get(self, group_name):
        """Return a host group."""

        g = self.request.mongo_connection.shinken.hostgroups.find_one(
            {"hostgroup_name": group_name}, {'_id': 0}
        )
        return hostgroup.HostGroup(**g)

    def update(self, group_name, group):
        """Modify an existing host group."""
        group_dict = group.as_dict()
        if "hostgroup_name" not in group_dict.keys():
            group_dict['hostgroup_name'] = group_name

        self.request.mongo_connection.shinken.hostgroups.update(
            {"hostgroup_name": group_name},
            {"$set": group_dict},
            upsert=True
        )

    def delete(self, group_name):
        """Delete existing host group."""
        self.request.mongo_connection.shinken.hostgroups.remove(
            {"hostgroup_name": group_name}
        )

    def create(self, group):
        """Create a new host group."""
        self.request.mongo_connection.shinken.hostgroups.insert(
            group.as_dict()
        )

    def get_all(self):
        """Return all host groups."""
        hostgroups = [g for g
                      in self.request.mongo_connection.
                      shinken.hostgroups.find(
                          {"register": {"$ne": "0"}},
                          {'_id': 0}
                      )]
        hostgroups = [hostgroup.HostGroup(**g) for g in hostgroups]
        return hostgroups
