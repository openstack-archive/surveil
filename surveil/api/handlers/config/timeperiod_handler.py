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

from surveil.api.datamodel.config import timeperiod
from surveil.api.handlers import handler


class TimePeriodHandler(handler.Handler):
    """Fulfills a request on the contact resource."""

    def get(self, timeperiod_name):
        """Return a time period."""

        t = self.request.mongo_connection.shinken.timeperiods.find_one(
            {"timeperiod_name": timeperiod_name}, {'_id': 0}
        )
        return timeperiod.TimePeriod(**t)

    def update(self, timeperiod_name, timeperiod):
        """Modify an existing time period."""
        timeperiod_dict = timeperiod.as_dict()
        if "timeperiod_name" not in timeperiod_dict.keys():
            timeperiod_dict['timeperiod_name'] = timeperiod_name

        self.request.mongo_connection.shinken.timeperiods.update(
            {"timeperiod_name": timeperiod_name},
            {"$set": timeperiod_dict},
            upsert=True
        )

    def delete(self, timeperiod_name):
        """Delete existing time period."""
        self.request.mongo_connection.shinken.timeperiods.remove(
            {"timeperiod_name": timeperiod_name}
        )

    def create(self, timeperiod):
        """Create a new time period."""
        self.request.mongo_connection.shinken.timeperiods.insert(
            timeperiod.as_dict()
        )

    def get_all(self):
        """Return all time periods."""
        timeperiods = [t for t
                       in self.request.mongo_connection.
                       shinken.timeperiods.find(
                           {"register": {"$ne": "0"}},
                           {'_id': 0}
                       )]
        timeperiods = [timeperiod.TimePeriod(**t) for t in timeperiods]
        return timeperiods
