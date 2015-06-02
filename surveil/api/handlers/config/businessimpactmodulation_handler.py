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

from surveil.api.datamodel.config import businessimpactmodulation
from surveil.api.handlers import handler


class BusinessImpactModulationHandler(handler.Handler):
    """Fulfills a request on the business impact modulation resource."""

    def get(self, name):
        """Return a business impact modulation."""

        t = (self.request.mongo_connection.
             shinken.businessimpactmodulations).find_one(
            {"business_impact_modulation_name": name},
            {'_id': 0}
        )
        return businessimpactmodulation.BusinessImpactModulation(**t)

    def update(self, name, modulation):
        """Modify an existing business impact modulation."""
        modulation_dict = modulation.as_dict()
        if "business_impact_modulation_name" not in modulation_dict.keys():
            modulation_dict['business_impact_modulation_name'] = modulation

        self.request.mongo_connection.shinken.businessimpactmodulations.update(
            {"business_impact_modulation_name": name},
            {"$set": modulation_dict},
            upsert=True
        )

    def delete(self, name):
        """Delete existing business impact modulation."""
        self.request.mongo_connection.shinken.businessimpactmodulations.remove(
            {"business_impact_modulation_name": name}
        )

    def create(self, modulation):
        """Create a new business impact modulation."""
        self.request.mongo_connection.shinken.businessimpactmodulations.insert(
            modulation.as_dict()
        )

    def get_all(self):
        """Return all business impact modulations."""
        modulations = [m for m
                       in self.request.mongo_connection.
                       shinken.businessimpactmodulations.find(
                           {"register": {"$ne": "0"}},
                           {'_id': 0}
                       )]
        modulations = [businessimpactmodulation.BusinessImpactModulation(**m)
                       for m in modulations]
        return modulations
