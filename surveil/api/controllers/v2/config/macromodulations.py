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

from surveil.api.datamodel.config import macromodulation
from surveil.api.handlers.config import macromodulation_handler
from surveil.common import util


class MacroModulationController(rest.RestController):

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose([macromodulation.MacroModulation])
    def get_all(self):
        """Returns all macro modulation objects."""
        handler = macromodulation_handler.MacroModulationHandler(pecan.request)
        modulations = handler.get_all()
        return modulations

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(macromodulation.MacroModulation, wtypes.text)
    def get_one(self, timeperiod_name):
        """Returns a specific macro modulation."""
        handler = macromodulation_handler.MacroModulationHandler(pecan.request)
        modulation = handler.get(timeperiod_name)
        return modulation

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(body=macromodulation.MacroModulation, status_code=201)
    def post(self, data):
        """Create a new macro modulation object.

        :param data: a macro modulation within the request body.
        """
        handler = macromodulation_handler.MacroModulationHandler(pecan.request)
        handler.create(data)

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(macromodulation.MacroModulation,
                         wtypes.text,
                         status_code=204)
    def delete(self, modulation_name):
        """Returns a specific macro modulation."""
        handler = macromodulation_handler.MacroModulationHandler(pecan.request)
        handler.delete(modulation_name)

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(macromodulation.MacroModulation,
                         wtypes.text,
                         body=macromodulation.MacroModulation,
                         status_code=204)
    def put(self, modulation_name, modulation):
        """Update a specific macro modulation."""
        handler = macromodulation_handler.MacroModulationHandler(pecan.request)
        handler.update(modulation_name, modulation)
