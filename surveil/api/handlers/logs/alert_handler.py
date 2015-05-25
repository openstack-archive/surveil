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


class AlertHandler(handler.Handler):
    """Handles requests to alert resources."""

    def get(self):
        influx = self.request.influxdb_client
        query = ("SELECT * FROM ALERT "
                 "GROUP BY * "
                 "ORDER BY time DESC ")

    def update(self):
        pass

    def delete(self):
        pass

    def create(self):
        pass

    def get_all(self):
        influx = self.request.influxdb_client
        query = ("SELECT * FROM ALERT "
                 "GROUP BY *")
        response = influx.query(query)

        print response.raw

        items = response.items()[0][1]
        alert_dicts = [self._alert_dict_from_influx_item(item) for item in items]
        alerts = [alert.Alert(**a) for a in alert_dicts]

        return alerts

    def _alert_dict_from_influx_item(self, item):
        item['time'] = self._influx_to_unix_timestamp(item['time'])
        return item


    @staticmethod
    def _influx_to_unix_timestamp(influx_datetime):
        dt = datetime.datetime.strptime(influx_datetime,
                                        "%Y-%m-%dT%H:%M:%SZ")
        unix_ts = dt.strftime("%s")
        return unix_ts
