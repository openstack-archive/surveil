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

import pecan
from pecan import rest
import wsmeext.pecan as wsme_pecan

from surveil.api.datamodel.status import live_query
from surveil.api.datamodel.status.metrics import metric as m
from surveil.api.handlers.status.metrics import metric_handler
from surveil.api.handlers.status.metrics import metric_name_handler
from surveil.common import util


class MetricsController(rest.RestController):

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose([m.Metric])
    def get(self):
        """Returns all metrics name for a host."""
        handler = metric_name_handler.MetricNameHandler(pecan.request)
        metrics_name = handler.get(pecan.request.context['host_name'])
        return metrics_name

    @pecan.expose()
    def _lookup(self, metric_name, *remainder):
        return MetricController(metric_name), remainder


class MetricController(rest.RestController):

    def __init__(self, metric_name):
        pecan.request.context['metric_name'] = metric_name
        self.metric_name = metric_name

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(m.Metric)
    def get(self):
        """Return the last measure for the metric name on the host."""
        handler = metric_handler.MetricHandler(pecan.request)
        metric = handler.get(
            pecan.request.context['host_name'],
            self.metric_name
        )
        return metric

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose([m.Metric], body=live_query.LiveQuery)
    def post(self, query):
        """Given a live query, returns all matching metrics.

        :param live_query: a live query within the request body.
        """
        handler = metric_handler.MetricHandler(pecan.request)
        metrics = handler.get_all(query=query,
                                  metric_name=self.metric_name,
                                  host_name=pecan.request.context['host_name']
                                  )
        return metrics
