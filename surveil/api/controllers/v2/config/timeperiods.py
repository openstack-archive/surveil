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

from surveil.api.datamodel.config import timeperiod
from surveil.api.handlers.config import timeperiod_handler
from surveil.common import util


class TimePeriodsController(rest.RestController):

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose([timeperiod.TimePeriod])
    def get_all(self):
        """Returns all time periods."""
        handler = timeperiod_handler.TimePeriodHandler(pecan.request)
        time_periods = handler.get_all()
        return time_periods

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(timeperiod.TimePeriod, wtypes.text)
    def get_one(self, timeperiod_name):
        """Returns a specific time period."""
        handler = timeperiod_handler.TimePeriodHandler(pecan.request)
        timeperiod = handler.get(timeperiod_name)
        return timeperiod

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(body=timeperiod.TimePeriod, status_code=201)
    def post(self, data):
        """Create a new time period.

        :param data: a time period within the request body.
        """
        handler = timeperiod_handler.TimePeriodHandler(pecan.request)
        handler.create(data)

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(timeperiod.TimePeriod, wtypes.text, status_code=204)
    def delete(self, timeperiod_name):
        """Returns a specific time period."""
        handler = timeperiod_handler.TimePeriodHandler(pecan.request)
        handler.delete(timeperiod_name)

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(timeperiod.TimePeriod,
                         wtypes.text,
                         body=timeperiod.TimePeriod,
                         status_code=204)
    def put(self, timeperiod_name, timeperiod):
        """Update a specific time period."""
        handler = timeperiod_handler.TimePeriodHandler(pecan.request)
        handler.update(timeperiod_name, timeperiod)
