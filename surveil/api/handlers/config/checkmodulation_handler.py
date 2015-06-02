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

from surveil.api.datamodel.config import checkmodulation
from surveil.api.handlers import handler


class CheckModulationHandler(handler.Handler):
    """Fulfills a request on the check modulation resource."""

    def get(self, checkmodulation_name):
        """Return a check modulation."""
        c = self.request.mongo_connection.shinken.checkmodulations.find_one(
            {"checkmodulation_name": checkmodulation_name}
        )
        return checkmodulation.CheckModulation(**c)

    def update(self, checkmodulation_name, checkmodulation):
        """Modify existing check modulation."""
        checkmodulation_dict = checkmodulation.as_dict()
        if "checkmodulation_name" not in checkmodulation_dict.keys():
            checkmodulation_dict['checkmodulation_name'] = checkmodulation_name

        self.request.mongo_connection.shinken.checkmodulations.update(
            {"checkmodulation_name": checkmodulation_name},
            {"$set": checkmodulation_dict},
            upsert=True
        )

    def delete(self, checkmodulation_name):
        """Delete an existing check modulation."""
        self.request.mongo_connection.shinken.checkmodulations.remove(
            {"checkmodulation_name": checkmodulation_name}
        )

    def create(self, data):
        """Create a new check modulation."""
        self.request.mongo_connection.shinken.checkmodulations.insert(
            data.as_dict()
        )

    def get_all(self):
        """Return all check modulation."""
        find = self.request.mongo_connection.shinken.checkmodulations.find()
        checkmodulations = [c for c in find]

        return [checkmodulation.CheckModulation(**c) for c in checkmodulations]
