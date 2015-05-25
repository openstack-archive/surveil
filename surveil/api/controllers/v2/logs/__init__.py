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

from surveil.api.datamodel.logs import log
from surveil.api.datamodel.status import live_query
from surveil.api.handlers.logs import log_handler
from surveil.common import util


class LogsController(rest.RestController):

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose([log.Log])
    def get_all(self):
        """Returns all hosts."""
        handler = log_handler.LogHandler(pecan.request)
        logs = handler.get_all()
        return logs

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose([log.Log], body=live_query.LiveQuery)
    def post(self, query):
        """Given a LiveQuery, returns all matching logs."""
        handler = log_handler.LogHandler(pecan.request)
        logs = handler.get_all(live_query=query)
        return logs
