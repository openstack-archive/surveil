# Copyright 2014 - Savoir-Faire Linux inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from surveil.api.datamodel.status.metrics import metric as m
from surveil.api.handlers import handler


class MetricNameHandler(handler.Handler):
    """Fulfills a request on the metrics."""

    def get(self, host_name, service_description=None):
        """Return all metrics name."""
        service_description = service_description or ''
        query = ("SHOW measurements WHERE host_name='%s' "
                 "AND service_description='%s'"
                 % (host_name, service_description))
        influx_client = self.request.influxdb_client
        response = influx_client.query(query)

        metrics = []
        for item in response[None]:
            metric_dict = self._metrics_name_from_influx_item(item)
            if metric_dict is not None:
                metrics.append(m.Metric(**metric_dict))

        return metrics

    def _metrics_name_from_influx_item(self, item):
        metric_name = None
        mappings = [('metric_name', 'name', str), ]
        for field in mappings:
            value = item.get(field[1], None)
            if value is not None:
                if value.startswith('metric_'):
                    metric_name = {}
                    metric_name[field[0]] = field[2](value[7:])

        return metric_name
