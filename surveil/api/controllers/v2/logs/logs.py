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


from surveil.api.controllers.v2.logs import alerts
from surveil.api.controllers.v2.logs import downtimes
from surveil.api.controllers.v2.logs import flappings
from surveil.api.controllers.v2.logs import notifications
from surveil.common import util


class LogsController(rest.RestController):
    alerts = alerts.AlertsController()
    downtimes = downtimes.DowntimesController()
    flappings = flappings.FlappingsController()
    notifications = notifications.NotificationsController()

    @util.policy_enforce(['authenticated'])
    @pecan.expose()
    def get_all(self):

        print pecan.request
        # @pecan.expose()
        # def _lookup(self, host_name, *remainder):
        #    return EventController(host_name), remainder
