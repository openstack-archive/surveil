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


class TimeDelta(types.Base):
    """Hold a time."""

    begin = wsme.wsattr(wtypes.text, mandatory=True)
    "The begin time of a measure in RFC3339."

    end = wsme.wsattr(wtypes.text, mandatory=True)
    "The end time of a measure in RFC3339."

    @classmethod
    def sample(cls):
        return cls(
            begin='2015-01-29T21:50:44Z',
            end='2015-01-29T22:50:44Z'
        )