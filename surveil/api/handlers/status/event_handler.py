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
        query = influxdb_query.build_influxdb_query(live_query, "EVENT",
                                                    multiple_series=True)
        return influxdb_query.paging(influx_client.query(query), event.Event, live_query)