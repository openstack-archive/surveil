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


class Downtime(types.Base):
    host_name = wsme.wsattr(wtypes.text, mandatory=True)
    """The name of the host"""

    service_description = wsme.wsattr(wtypes.text, mandatory=False)
    """Ther service description"""

    time_stamp = wsme.wsattr(int, mandatory=False)
    """Time stamp for the downtime"""

    start_time = wsme.wsattr(int, mandatory=False)
    """When to start the downtime"""

    end_time = wsme.wsattr(int, mandatory=False)
    """When to end the downtime"""

    fixed = wsme.wsattr(int, mandatory=False)

    duration = wsme.wsattr(int, mandatory=False)
    """The duration of the downtime, in seconds"""

    trigger_id = wsme.wsattr(int, mandatory=False)

    author = wsme.wsattr(wtypes.text, mandatory=False)
    """The author of the downtime"""

    comment = wsme.wsattr(wtypes.text, mandatory=False)
    """Comment for the downtime"""

    @classmethod
    def sample(cls):
        return cls(
            host_name="localhost",
            service_description="ws-arbiter",
            time_stamp=1430150469,
            start_time=1430150469,
            end_time=1430150469,
            fixed=1,
            duration=86400,
            trigger_id=0,
            author='aviau',
            comment='No comment.'
        )
