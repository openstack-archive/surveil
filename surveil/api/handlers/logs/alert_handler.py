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

import datetime
import json

from surveil.api.datamodel.logs import alert
from surveil.api.handlers import handler
from surveil.api.handlers.status.influxdb_query import build_influxdb_query


class AlertHandler(handler.Handler):
    """Handles requests to alert resources."""

    def get_all(self, hostname=None, service_description=None, time_delta=None):
        influx_client = self.request.influxdb_client
        query = build_influxdb_query("", "ALERT", "", "")
        response = influx_client.query(query)

        alerts = []

        for item in response[None]:
            alert_dict = self._alert_dict_from_influx_item(item, hostname, service_description)
            alerts.append(alert.Alert(**alert_dict))

        return alerts

    def _alert_dict_from_influx_item(self, item, hostname, service_description):
        print item
        mappings = [
            ('time', str),
            ('attempts', int),
            ('contact', str),
            ('notification_method', str),
            ('notification_type', str),
            ('output', str),
            ('state', str),
            ('state_type', str),
            ('alert_type', str)
        ]

        alert_dict = {}

        if service_description is not None:
            alert_dict['service_description'] = service_description

        if hostname is not None:
            alert_dict['host_name'] = hostname

        for field in mappings:
            value = item.get(field[0], None)
            if value is not None:
                alert_dict[field[0]] = field[1](value)

        return alert_dict
