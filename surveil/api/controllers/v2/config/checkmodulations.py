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
from surveil.api.handlers.config import checkmodulation_handler
from surveil.common import util


class CheckModulationsController(rest.RestController):

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose([checkmodulation.CheckModulation])
    def get_all(self):
        """Returns all  check modulations."""
        handler = checkmodulation_handler.CheckModulationHandler(pecan.request)
        checkmodulations = handler.get_all()
        return checkmodulations

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(checkmodulation.CheckModulation, wtypes.text)
    def get_one(self, checkmodulation_name):
        """Returns a specific check modulation."""
        handler = checkmodulation_handler.CheckModulationHandler(pecan.request)
        checkmodulation = handler.get(checkmodulation_name)
        return checkmodulation

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(body=checkmodulation.CheckModulation, status_code=201)
    def post(self, data):
        """Create a new check modulation.

        :param data: a check modulation within the request body.
        """
        handler = checkmodulation_handler.CheckModulationHandler(pecan.request)
        handler.create(data)

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(checkmodulation.CheckModulation,
                         wtypes.text, status_code=204)
    def delete(self, checkmodulation_name):
        """Returns a specific check modulation."""
        handler = checkmodulation_handler.CheckModulationHandler(pecan.request)
        handler.delete(checkmodulation_name)

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(checkmodulation.CheckModulation,
                         wtypes.text,
                         body=checkmodulation.CheckModulation,
                         status_code=204)
    def put(self, checkmodulation_name, checkmodulation):
        """Update a specific check modulation."""
        handler = checkmodulation_handler.CheckModulationHandler(pecan.request)
        handler.update(checkmodulation_name, checkmodulation)