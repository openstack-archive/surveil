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

from surveil.api.datamodel.status.metrics import live_metric
from surveil.api.handlers import handler
from surveil.api.handlers.status.metrics import influxdb_time_query


class MetricHandler(handler.Handler):
    """Fulfills a request on the metrics."""

    def get(self, metric_name, host_name, service_description=None):

        """Return a metric."""
        cli = self.request.influxdb_client

        if service_description is None:
            query = ("SELECT * FROM metric_%s "
                     "WHERE host_name= '%s' "
                     "GROUP BY service_description "
                     "ORDER BY time DESC "
                     "LIMIT 1" % (metric_name, host_name))
        else:
            query = ("SELECT * FROM metric_%s "
                     "WHERE host_name= '%s' "
                     "AND service_description= '%s'"
                     "ORDER BY time DESC "
                     "LIMIT 1" % (metric_name, host_name, service_description))

        response = cli.query(query)
        metric = live_metric.LiveMetric(
            **self._metric_dict_from_influx_item(response.items()[0],
                                                 metric_name)
        )

        return metric

    def get_all(self, metric_name, time, host_name=None,
                service_description=None):
        """Return all metrics."""

        cli = self.request.influxdb_client
        query = influxdb_time_query.build_influxdb_query(
            metric_name,
            time,
            host_name,
            service_description
        )
        response = cli.query(query)

        metric_dicts = []

        for item in response.items():
            metric_dict = self._metric_dict_from_influx_item(item, metric_name)
            metric_dicts.append(metric_dict)

        metrics = []
        for metric_dict in metric_dicts:
            metric = live_metric.LiveMetric(**metric_dict)
            metrics.append(metric)

        return metrics

    def _metric_dict_from_influx_item(self, item, metric_name):
        points = item[1]
        first_point = next(points)

        metric_dict = {
            "metric_name": str(metric_name),
            "min": str(first_point.get('min', None)),
            "max": str(first_point.get('max', None)),
            "critical": str(first_point.get('critical', None)),
            "warning": str(first_point.get('warning', None)),
            "value": str(first_point.get('value', None)),
            "unit": str(first_point.get('unit', None))
        }
        return metric_dict
