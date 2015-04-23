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

from surveil.api.datamodel.status import live_service
from surveil.api.handlers import handler
from surveil.api.handlers.status import liveQuery_filter as query_filter


class ServiceHandler(handler.Handler):
    """Fulfills a request on live services."""

    def get(self, host_name, service_name):
        """Return a specific service"""
        cli = self.request.influxdb_client
        query = ("SELECT * from SERVICE_STATE "
                 "WHERE host_name='%s' "
                 "AND service_description='%s' "
                 "GROUP BY * LIMIT 1") % (host_name, service_name)
        response = cli.query(query)

        host = live_service.LiveService(
            **self._service_dict_from_influx_item(response.items()[0])
        )
        return host

    def get_all(self, live_query=None):
        """Return all live services."""
        cli = self.request.influxdb_client
        query = (
            "SELECT * from SERVICE_STATE "
            "GROUP BY host_name, service_description "
            "LIMIT 1"
        )

        response = cli.query(query)

        service_dicts = []

        for item in response.items():
            service_dict = self._service_dict_from_influx_item(item)
            service_dicts.append(service_dict)

        if live_query:
            service_dicts = query_filter.filter_dict_list_with_live_query(
                service_dicts,
                live_query
            )

        services = []
        for service_dict in service_dicts:
            service = live_service.LiveService(**service_dict)
            services.append(service)

        return services

    def _service_dict_from_influx_item(self, item):
        tags = item[0][1]
        points = item[1]
        first_point = next(points)

        service_dict = {
            "service_description": tags['service_description'],
            "host_name": tags['host_name'],
            "description": tags['service_description'],
            "state": first_point['state'],
            "acknowledged": int(first_point['acknowledged']),
            "last_check": int(first_point['last_check']),
            "last_state_change": int(first_point['last_state_change']),
            "plugin_output": first_point['output']
        }

        return service_dict
