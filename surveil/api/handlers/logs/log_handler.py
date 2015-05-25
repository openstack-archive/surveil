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

from surveil.api.handlers import handler


class LogHandler(handler.Handler):
    """Fulfills a request on the macro modulation resource."""

    def get_all(self, modulation_name):
        influx_client = self.request.influxdb_client
        query = build_influxdb_query("", "ALERT", "", "")
        response = influx_client.query(query)

        alerts = []

        for item in response[None]:
            alert_dict = self._alert_dict_from_influx_item(item, hostname, service_description)
            alerts.append(alert.Alert(**alert_dict))

        return alerts
