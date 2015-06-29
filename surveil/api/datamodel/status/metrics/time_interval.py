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

import wsme
import wsme.types as wtypes

from surveil.api.datamodel import types


class TimeInterval(types.Base):
    """Hold a time."""

    start_time = wsme.wsattr(wtypes.text, mandatory=True)
    "The starting time."

    end_time = wsme.wsattr(wtypes.text, mandatory=True)
    "The ending time."

    @classmethod
    def sample(cls):
        return cls(
            start_time='2015-01-29T21:50:44Z',
            end_time='2015-01-29T22:50:44Z'
        )
