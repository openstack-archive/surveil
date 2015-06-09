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

from pecan import rest

from surveil.api.controllers.v2.status import hosts as v2_hosts
from surveil.api.controllers.v2.status.metrics import metrics as v2_metrics
from surveil.api.controllers.v2.status import services as v2_services


class StatusController(rest.RestController):
    # events = EventsController()
    hosts = v2_hosts.HostsController()
    services = v2_services.ServicesController()
    metrics = v2_metrics.MetricsController()