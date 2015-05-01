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

from surveil.common import util


class DowntimesController(rest.RestController):

    # curl -X GET  http://127.0.0.1:8080/v2/titilambert/myproject/builds/
    # @wsme_pecan.wsexpose([Host])
    @util.policy_enforce(['authenticated'])
    @pecan.expose()
    def get_all(self):
        """Returns all downtimes from a specific host."""
        return "ALLL DT"