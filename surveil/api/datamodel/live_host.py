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

from surveil.api.controllers.v1.datamodel import types


class LiveHost(types.Base):
    host_name = wsme.wsattr(wtypes.text, mandatory=True)
    """The name of the host"""

    description = wsme.wsattr(wtypes.text, mandatory=False)
    """The description of the host"""

    host_state = wsme.wsattr(int, mandatory=False)
    """The current state of the host"""

    last_check = wsme.wsattr(int, mandatory=False)
    """The last time the host was checked"""

    last_state_change = wsme.wsattr(int, mandatory=False)
    """The last time the state has changed"""

    plugin_output = wsme.wsattr(wtypes.text, mandatory=False)
    """Plugin output of the last check"""

    @classmethod
    def sample(cls):
        return cls(
            host_name='CoolHost',
            description='Very Nice Host',
            host_state='',
            last_check=1429220785,
            last_state_change=1429220785,
            plugin_output='All good! Check passed'
        )
