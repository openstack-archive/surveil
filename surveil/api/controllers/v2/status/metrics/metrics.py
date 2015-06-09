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

import pecan
from pecan import rest
import wsmeext.pecan as wsme_pecan


from surveil.api.datamodel.status.metrics import live_metric
from surveil.api.handlers.status.metrics import live_metric_handler
from surveil.common import util


class MetricsController(rest.RestController):

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose([live_metric.LiveMetric])
    def get_all(self):
        """Returns all hosts."""
        handler = live_metric_handler.MetricHandler(pecan.request)
        metrics = handler.get_metric_without_service_description()
        return metrics