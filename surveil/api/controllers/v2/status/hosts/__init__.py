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

from surveil.api.controllers.v2 import logs
from surveil.api.controllers.v2.status.hosts import config
from surveil.api.controllers.v2.status import metrics


class HostsController(rest.RestController):

    @pecan.expose()
    def get_all(self):
        """Returns all hosts."""
        return "ALLL HOSSSSSSSST"

    @pecan.expose()
    def _lookup(self, host_name, *remainder):
        return HostController(host_name), remainder


class HostController(rest.RestController):

    # services = ServicesController()
    # See init for controller creation. We need host_name to instanciate it
    # externalcommands = ExternalCommandsController()
    config = config.ConfigController()
    events = logs.LogsController()
    metrics = metrics.MetricsController()

    def __init__(self, host_name):
        pecan.request.context['host_name'] = host_name
        self._id = host_name

    @pecan.expose()
    def get(self):
        """Returns a specific host."""

        output = '{"host_name": "myhostname", "alias": %s}' % self._id

        return output
