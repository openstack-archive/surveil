# Copyright 2015 - Savoir-Faire Linux inc.
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

from surveil.api.datamodel.logs import log
from surveil.api.handlers import handler
from surveil.api.handlers.status import influxdb_query


class LogHandler(handler.Handler):

    """Fulfills a request on the macro modulation resource."""

    def get_all(self, live_query=None):
        """Return all logs."""
        influx_client = self.request.influxdb_client
        query = influxdb_query.build_influxdb_query(live_query, "ALERT")
        response = influx_client.query(query)

        logs = []

        for item in response.items():
            tags = item[0][1]
            for point in response.get_points(tags=tags):
                point.update(tags)
                log_dict = self._log_dict_from_influx_item(point)
                logs.append(log.Log(**log_dict))

        return logs

    def _log_dict_from_influx_item(self, item):
        mappings = [
            ('time', str),
            ('event_type', str),
            ('host_name', str),
            ('service_description', str),
            ('state', str),
            ('state_type', str),
            ('attempts', int),
            ('downtime_type', str),
            ('notification_type', str),
            ('notification_method', str),
            ('contact', str),
            ('alert_type', str),
            ('output', str),
            ('acknowledgement', str)
        ]

        log_dict = {}

        for field in mappings:
            value = item.get(field[0], None)
            if value is not None:
                log_dict[field[0]] = field[1](value)

        return log_dict
