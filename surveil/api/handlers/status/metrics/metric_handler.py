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

from surveil.api.datamodel.status import live_query as q
from surveil.api.datamodel.status.metrics import metric as m
from surveil.api.handlers import handler
from surveil.api.handlers.status import influxdb_query


class MetricHandler(handler.Handler):
    """Fulfills a request on the metrics."""

    def get(self, host_name, metric_name, service_description=None):
        """Return the last metric."""
        query = self._build_metric_query(
            host_name,
            metric_name,
            service_description=service_description,
            limit=1)

        influx_client = self.request.influxdb_client
        response = influx_client.query(query)

        metrics = []
        for item in response[None]:
            metric_dict = self._metric_dict_from_influx_item(item, metric_name)
            metric = m.Metric(**metric_dict)
            metrics.append(metric)

        if metric_name:
            metrics = metrics[0] or ''
        return metrics

    def get_all(self, metric_name,
                host_name, service_description=None,
                query=q.LiveQuery()):
        """Return all metrics."""
        query = self._build_metric_query(
            host_name,
            metric_name,
            service_description=service_description,
            query=query)
        influx_client = self.request.influxdb_client
        response = influx_client.query(query)

        metrics = []
        for item in response[None]:
            metric_dict = self._metric_dict_from_influx_item(item, metric_name)
            metric = m.Metric(**metric_dict)
            metrics.append(metric)

        return metrics

    def _build_metric_query(self, host_name, metric_name,
                            service_description=None,
                            query=None, limit=None):
        filters = {
            "is": {
                "host_name": [host_name]
            }
        }

        group_by = []
        if service_description:
            filters["is"]["service_description"] = [service_description]
        else:
            group_by.append('service_description')

        return influxdb_query.build_influxdb_query(query,
                                                   'metric_' + metric_name,
                                                   order_by=["time desc"],
                                                   group_by=group_by,
                                                   additional_filters=filters,
                                                   limit=limit,
                                                   )

    def _metric_dict_from_influx_item(self, item, metric_name=None):
        metric_dict = {"metric_name": str(metric_name)}
        mappings = [
            ('min', str),
            ('max', str),
            ('critical', str),
            ('warning', str),
            ('value', str),
            ('unit', str),
        ]

        for field in mappings:
            value = item.get(field[0], None)
            if value is not None:
                if field[0] == 'name':
                    if value.startswith('metric_'):
                        metric_dict = {}
                        metric_dict[field[1]] = field[2](value[7:])
                else:
                    metric_dict[field[0]] = field[1](value)

        return metric_dict
