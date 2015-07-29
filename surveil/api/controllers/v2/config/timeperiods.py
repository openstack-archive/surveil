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
from surveil.api.datamodel import live_query as lq
from surveil.api.handlers.config import timeperiod_handler
from surveil.common import util


class TimePeriodsController(rest.RestController):

    @pecan.expose()
    def _lookup(self, timeperiod_name, *remainder):
        return TimePeriodController(timeperiod_name), remainder

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose([timeperiod.TimePeriod], body=lq.LiveQuery)
    def post(self, data):
        """Returns all time periods."""
        handler = timeperiod_handler.TimePeriodHandler(pecan.request)
        time_periods = handler.get_all(data)
        return time_periods

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(body=timeperiod.TimePeriod, status_code=201)
    def put(self, data):
        """Create a new time period.

        :param data: a time period within the request body.
        """
        handler = timeperiod_handler.TimePeriodHandler(pecan.request)
        handler.create(data)


class TimePeriodController(rest.RestController):

    def __init__(self, timeperiod_name):
        pecan.request.context['timeperiod_name'] = timeperiod_name
        self._id = timeperiod_name

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(None, status_code=204)
    def delete(self):
        """Returns a specific time period."""
        handler = timeperiod_handler.TimePeriodHandler(pecan.request)
        handler.delete({"timeperiod_name": self._id})

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(None, body=timeperiod.TimePeriod,
                         status_code=204)
    def put(self, timeperiod):
        """Update a specific time period."""
        handler = timeperiod_handler.TimePeriodHandler(pecan.request)
        handler.update({"timeperiod_name": self._id}, timeperiod)

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(timeperiod.TimePeriod, wtypes.text)
    def get(self):
        """Returns a specific time period."""
        handler = timeperiod_handler.TimePeriodHandler(pecan.request)
        timeperiod = handler.get({"timeperiod_name": self._id})
        return timeperiod