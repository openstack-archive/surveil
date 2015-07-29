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
import wsme.types as wtypes
import wsmeext.pecan as wsme_pecan

from surveil.api.datamodel.config import checkmodulation
from surveil.api.datamodel import live_query as lq
from surveil.api.handlers.config import checkmodulation_handler
from surveil.common import util


class CheckModulationsController(rest.RestController):

    @pecan.expose()
    def _lookup(self, checkmodulation_name, *remainder):
        return CheckModulationController(checkmodulation_name), remainder

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose([checkmodulation.CheckModulation], body=lq.LiveQuery)
    def post(self, data):
        """Returns all  check modulations."""
        handler = checkmodulation_handler.CheckModulationHandler(pecan.request)
        checkmodulations = handler.get_all(data)
        return checkmodulations

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(body=checkmodulation.CheckModulation, status_code=201)
    def put(self, data):
        """Create a new check modulation.

        :param data: a check modulation within the request body.
        """
        handler = checkmodulation_handler.CheckModulationHandler(pecan.request)
        handler.create(data)


class CheckModulationController(rest.RestController):

    def __init__(self, check_modulation_name):
        pecan.request.context['check_modulation_name'] = check_modulation_name
        self._id = check_modulation_name

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(None, status_code=204)
    def delete(self):
        """Returns a specific check modulation."""
        handler = checkmodulation_handler.CheckModulationHandler(pecan.request)
        handler.delete({"checkmodulation_name": self._id})

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(None,
                         body=checkmodulation.CheckModulation,
                         status_code=204)
    def put(self, checkmodulation):
        """Update a specific check modulation."""
        handler = checkmodulation_handler.CheckModulationHandler(pecan.request)
        handler.update(
            {"checkmodulation_name": self._id},
            checkmodulation
        )

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(checkmodulation.CheckModulation, wtypes.text)
    def get(self):
        """Returns a specific check modulation."""
        handler = checkmodulation_handler.CheckModulationHandler(pecan.request)
        checkmodulation = handler.get(
            {"checkmodulation_name": self._id}
        )
        return checkmodulation