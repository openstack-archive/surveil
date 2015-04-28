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

import time

import wsme
import wsme.types as wtypes

from surveil.api.datamodel import types


class CheckResult(types.Base):
    time_stamp = wsme.wsattr(wtypes.text,
                             mandatory=False,
                             default=str(int(time.time())))
    """The time the check was executed. Defaults to now."""

    return_code = wsme.wsattr(int, mandatory=True)
    """The return code of the check."""

    output = wsme.wsattr(wtypes.text, mandatory=True)
    """The output of the check."""

    @classmethod
    def sample(cls):
        return cls(
            time_stamp="1409087486",
            return_code=0,
            output="CPU Usage 98%|c[cpu]=98%;80;95;0;100"
        )
