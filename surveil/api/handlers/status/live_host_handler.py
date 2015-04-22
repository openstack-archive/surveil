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
import json

from surveil.api.datamodel.status import live_host
from surveil.api.handlers import handler
from surveil.api.handlers.status import liveQuery_filter as query_filter


class HostHandler(handler.Handler):
    """Fulfills a request on the live hosts."""

    def get_all(self, live_query=None):
        """Return all live hosts."""
        cli = self.request.influxdb_client
        query = ("SELECT * from HOST_STATE "
                 "GROUP BY host_name, address, childs "
                 "LIMIT 1")
        response = cli.query(query)

        host_dicts = []

        for item in response.items():
            first_entry = next(item[1])

            host_dict = {
                # TAGS
                "host_name": item[0][1]['host_name'],
                "address": item[0][1]['address'],
                "description": item[0][1]['host_name'],
                "childs": json.loads(item[0][1]['childs']),

                # Values
                "state": first_entry['state'],
                "acknowledged": int(first_entry['acknowledged']),
                "last_check": int(first_entry['last_check']),
                "last_state_change": int(first_entry['last_state_change']),
                "plugin_output": first_entry['output']
            }

            host_dicts.append(host_dict)

        if live_query:
            host_dicts = query_filter.filter_dict_list_with_live_query(
                host_dicts,
                live_query
            )

        hosts = []
        for host_dict in host_dicts:
            host = live_host.LiveHost(**host_dict)
            hosts.append(host)

        return hosts
