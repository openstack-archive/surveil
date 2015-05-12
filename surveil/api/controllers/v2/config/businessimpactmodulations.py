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

from surveil.api.datamodel.config import businessimpactmodulation as mod
from surveil.api.handlers.config import businessimpactmodulation_handler as bh
from surveil.common import util


class BusinessImpactModulationsController(rest.RestController):

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose([mod.BusinessImpactModulation])
    def get_all(self):
        """Returns all business impact modulations."""
        handler = bh.BusinessImpactModulationHandler(pecan.request)
        modulations = handler.get_all()
        return modulations

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(mod.BusinessImpactModulation, wtypes.text)
    def get_one(self, modulation_name):
        """Returns a specific business impact modulation."""
        handler = bh.BusinessImpactModulationHandler(pecan.request)
        modulation = handler.get(modulation_name)
        return modulation

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(body=mod.BusinessImpactModulation, status_code=201)
    def post(self, data):
        """Create a new business impact modulation.

        :param data: a business impact modulation within the request body.
        """
        handler = bh.BusinessImpactModulationHandler(pecan.request)
        handler.create(data)

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(mod.BusinessImpactModulation,
                         wtypes.text,
                         status_code=204)
    def delete(self, modulation_name):
        """Returns a specific business impact modulation."""
        handler = bh.BusinessImpactModulationHandler(pecan.request)
        handler.delete(modulation_name)

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(mod.BusinessImpactModulation,
                         wtypes.text,
                         body=mod.BusinessImpactModulation,
                         status_code=204)
    def put(self, modulaion_name, modulation):
        """Update a specific business impact modulation."""
        handler = bh.BusinessImpactModulationHandler(pecan.request)
        handler.update(modulaion_name, modulation)
