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

from surveil.api.datamodel.status import event
from surveil.api.handlers import handler
from surveil.api.handlers.status import influxdb_query


class EventHandler(handler.Handler):
    """Fulfills a request on the events resource."""

    def get_all(self, live_query=None):
        """Return all logs."""
        influx_client = self.request.influxdb_client
        query = influxdb_query.build_influxdb_query(live_query, "EVENT")
        response = influx_client.query(query)

        events = []

        for item in response.items():
            tags = item[0][1]
            for point in response.get_points(tags=tags):
                point.update(tags)
                event_dict = self._event_dict_from_influx_item(point)
                events.append(event.Event(**event_dict))

        return events

    def _event_dict_from_influx_item(self, item):
        mappings = [
            'time',
            'event_type',
            'host_name',
            'service_description',
            'state',
            'state_type',
            'attempts',
            'downtime_type',
            'notification_type',
            'notification_method',
            'contact',
            'alert_type',
            'output',
            'acknowledgement'
        ]

        event_dict = {}

        for field in mappings:
            value = item.get(field, None)
            if value is not None and value != "":
                event_dict[field] = value

        return event_dict
