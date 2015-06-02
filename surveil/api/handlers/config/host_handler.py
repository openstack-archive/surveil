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

from surveil.api.datamodel.config import host
from surveil.api.handlers import handler


class HostHandler(handler.Handler):
    """Fulfills a request on the host resource."""

    def get(self, host_name):
        """Return a host."""

        h = self.request.mongo_connection.shinken.hosts.find_one(
            {"host_name": host_name}, {'_id': 0}
        )
        return host.Host(**h)

    def update(self, host_name, host):
        """Modify existing host."""
        host_dict = host.as_dict()
        if "host_name" not in host_dict.keys():
            host_dict['host_name'] = host_name

        self.request.mongo_connection.shinken.hosts.update(
            {"host_name": host_name},
            {"$set": host_dict},
            upsert=True
        )

    def delete(self, host_name):
        """Delete existing host."""
        self.request.mongo_connection.shinken.hosts.remove(
            {"host_name": host_name}
        )

    def create(self, host):
        """Create a new host."""
        self.request.mongo_connection.shinken.hosts.insert(
            host.as_dict()
        )

    def get_all(self):
        """Return all hosts."""
        hosts = [h for h
                 in self.request.mongo_connection.
                 shinken.hosts.find(
                     {"register": {"$ne": "0"}},  # Don't return templates
                     {'_id': 0}
                 )]
        hosts = [host.Host(**h) for h in hosts]
        return hosts