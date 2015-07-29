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
import wsmeext.pecan as wsme_pecan

from surveil.api.datamodel.config import businessimpactmodulation as mod
from surveil.api.datamodel import live_query as lq
from surveil.api.handlers.config import businessimpactmodulation_handler as bh
from surveil.common import util


class BusinessImpactModulationsController(rest.RestController):

    @pecan.expose()
    def _lookup(self, businessimpactmodulation_name, *remainder):
        return BusinessImpactModulationController(
            businessimpactmodulation_name), remainder

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose([mod.BusinessImpactModulation], body=lq.LiveQuery)
    def post(self, data):
        """Returns all business impact modulations."""
        handler = bh.BusinessImpactModulationHandler(pecan.request)
        modulations = handler.get_all(data)
        return modulations

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(mod.BusinessImpactModulation,
                         body=mod.BusinessImpactModulation,
                         status_code=201)
    def put(self, data):
        """Create a new business impact modulation.

        :param data: a business impact modulation within the request body.
        """
        handler = bh.BusinessImpactModulationHandler(pecan.request)
        handler.create(data)


class BusinessImpactModulationController(rest.RestController):

    def __init__(self, business_impact_modulation_name):
        pecan.request.context['business_impact_modulation_name'] = (
            business_impact_modulation_name)
        self._id = business_impact_modulation_name

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(mod.BusinessImpactModulation)
    def get(self):
        """Returns a specific business impact modulation."""
        handler = bh.BusinessImpactModulationHandler(pecan.request)
        modulation = handler.get(
            {"business_impact_modulation_name": self._id}
        )
        return modulation

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(None, status_code=204)
    def delete(self):
        """Delete this business impact modulation."""
        handler = bh.BusinessImpactModulationHandler(pecan.request)
        handler.delete(
            {"business_impact_modulation_name": self._id}
        )

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(None,
                         body=mod.BusinessImpactModulation,
                         status_code=204)
    def put(self, modulation):
        """Update a specific business impact modulation."""
        handler = bh.BusinessImpactModulationHandler(pecan.request)
        handler.update(
            {"business_impact_modulation_name": self._id},
            modulation
        )
