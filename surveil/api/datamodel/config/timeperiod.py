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
    timeperiod_name = wsme.wsattr(wtypes.text, mandatory=False)
    exclude = wsme.wsattr(wtypes.ArrayType(wtypes.text),
                          mandatory=False)
    alias = wsme.wsattr(wtypes.text, mandatory=False)

    periods = wsme.wsattr(
        wtypes.DictType(wtypes.text, wtypes.text),
        mandatory=False
    )

    @classmethod
    def sample(cls):
        return cls(
            timeperiod_name='nonworkhours',
            periods={
                "sunday": "0:00-24:00",
                "february 10": "00:00-24:00"
            }
        )
