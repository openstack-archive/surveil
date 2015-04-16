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

from __future__ import print_function
from surveil.api.handlers import handler
from surveil.api.datamodel import live_host


class HostHandler(handler.Handler):
    """Fulfills a request on the service resource."""

    def get_all(self, host_name=None):
        """Return all live hosts."""
        cli = self.request.influxdb_client
        query = cli.query("SELECT * from HOST_STATE GROUP BY host_name LIMIT 1")

        hosts = []

        for item in query.items():
            host_name = item[0][1]['host_name']
            first_entry = next(item[1])

            state = first_entry['state_id']
            last_check = int(first_entry['last_chk'])
            last_state_change = int(first_entry['last_state_change'])
            plugin_output = first_entry['output']

            host = live_host.LiveHost(
                host_name=host_name,
                description=host_name,
                state=state,
                last_check=last_check,
                last_state_change=last_state_change,
                plugin_output=plugin_output
            )

            hosts.append(host)

        return hosts
