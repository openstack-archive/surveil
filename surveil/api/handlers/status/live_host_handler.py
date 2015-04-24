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
from surveil.api.handlers.status import influxdb_query


class HostHandler(handler.Handler):
    """Fulfills a request on the live hosts."""

    def get(self, host_name):
        """Return a host."""
        cli = self.request.influxdb_client
        query = ("SELECT * from HOST_STATE "
                 "WHERE host_name='%s' "
                 "GROUP BY * LIMIT 1") % host_name
        response = cli.query(query)

        host = live_host.LiveHost(
            **self._host_dict_from_influx_item(response.items()[0])
        )
        return host

    def get_all(self, live_query=None):
        """Return all live hosts."""
        cli = self.request.influxdb_client
        query = influxdb_query.build_influxdb_query(
            live_query,
            'HOST_STATE',
            group_by=['host_name', 'address', 'childs'],
            limit=1
        )
        response = cli.query(query)

        host_dicts = []

        for item in response.items():
            host_dict = self._host_dict_from_influx_item(item)
            host_dicts.append(host_dict)

        if live_query:
            host_dicts = influxdb_query.filter_fields(
                host_dicts,
                live_query
            )

        hosts = []
        for host_dict in host_dicts:
            host = live_host.LiveHost(**host_dict)
            hosts.append(host)

        return hosts

    def _host_dict_from_influx_item(self, item):
        points = item[1]
        first_point = next(points)

        tags = item[0][1]

        host_dict = {
            # TAGS
            "host_name": tags['host_name'],
            "address": tags['address'],
            "description": tags['host_name'],
            "childs": json.loads(tags['childs']),

            # Values
            "state": first_point['state'],
            "acknowledged": int(first_point['acknowledged']),
            "last_check": int(first_point['last_check']),
            "last_state_change": int(first_point['last_state_change']),
            "plugin_output": first_point['output']
        }

        return host_dict
