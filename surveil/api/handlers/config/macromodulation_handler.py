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

from surveil.api.datamodel.config import macromodulation
from surveil.api.handlers import handler


class MacroModulationHandler(handler.Handler):
    """Fulfills a request on the macro modulation resource."""

    def get(self, modulation_name):
        """Return a macro modulation."""

        m = self.request.mongo_connection.shinken.macromodulations.find_one(
            {"macromodulation_name": modulation_name}, {'_id': 0}
        )
        return macromodulation.MacroModulation(**m)

    def update(self, modulation_name, modulation):
        """Modify an existing macro modulation."""
        modulation_dict = modulation.as_dict()
        if "macromodulation_name" not in modulation_dict.keys():
            modulation_dict['contactgroup_name'] = modulation_name

        self.request.mongo_connection.shinken.macromodulations.update(
            {"macromodulation_name": modulation_name},
            {"$set": modulation_dict},
            upsert=True
        )

    def delete(self, modulation_name):
        """Delete existing macro modulation."""
        self.request.mongo_connection.shinken.macromodulations.remove(
            {"macromodulation_name": modulation_name}
        )

    def create(self, modulation):
        """Create a new macro modulation."""
        self.request.mongo_connection.shinken.macromodulations.insert(
            modulation.as_dict()
        )

    def get_all(self):
        """Return all macro modulation objects."""
        modulations = [m for m
                       in self.request.mongo_connection.
                       shinken.macromodulations.find(
                           # Don't return templates
                           {
                               "register": {"$ne": "0"}
                           },
                           {
                               "_id": 0
                           }
                       )
                       ]

        modulations = [macromodulation.MacroModulation(**m)
                       for m in modulations]

        return modulations
