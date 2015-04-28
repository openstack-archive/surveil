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

import wsme
import wsme.types as wtypes

from surveil.api.datamodel import types


class TimePeriod(types.Base):
    timeperiod_name = wsme.wsattr(wtypes.text, mandatory=True)
    exclude = wsme.wsattr(wtypes.text, mandatory=False)

    periods = wsme.wsattr(
        wtypes.DictType(wtypes.text, wtypes.text),
        mandatory=False
    )

    def __init__(self, **kwargs):
        super(TimePeriod, self).__init__(**kwargs)

        periods = [i for i in kwargs.items() if isinstance(i[0], str)
                   and i[0] not in ['timeperiod_name', 'exclude', 'periods']]
        if len(periods) > 0:
            self.periods = {}
            for item in periods:
                self.periods[item[0]] = item[1]

    def as_dict(self):
        timeperiod_dict = super(TimePeriod, self).as_dict()
        periods = timeperiod_dict.pop("periods", None)
        if periods:
            for item in periods.items():
                timeperiod_dict[item[0]] = item[1]
        return timeperiod_dict

    @classmethod
    def sample(cls):
        return cls(
            timeperiod_name='nonworkhours',
            periods={
                "sunday": "0:00-24:00",
                "february 10": "00:00-24:00"
            }
        )
