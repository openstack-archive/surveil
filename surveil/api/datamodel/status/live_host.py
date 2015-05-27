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


class LiveHost(types.Base):
    host_name = wsme.wsattr(wtypes.text, mandatory=False)
    """The name of the host"""

    address = wsme.wsattr(wtypes.text, mandatory=False)
    """The address of the host"""

    childs = wsme.wsattr([wtypes.text], mandatory=False)
    """The childs of the host"""

    parents = wsme.wsattr([wtypes.text], mandatory=False)
    """The parents of the host"""

    description = wsme.wsattr(wtypes.text, mandatory=False)
    """The description of the host"""

    state = wsme.wsattr(wtypes.text, mandatory=False)
    """The current state of the host"""

    acknowledged = wsme.wsattr(bool, mandatory=False)
    """Wether or not the problem, if any, has been acknowledged"""

    last_check = wsme.wsattr(int, mandatory=False)
    """The last time the host was checked"""

    last_state_change = wsme.wsattr(int, mandatory=False)
    """The last time the state has changed"""

    plugin_output = wsme.wsattr(wtypes.text, mandatory=False)
    """Plugin output of the last check"""

    long_output = wsme.wsattr(wtypes.text, mandatory=False)
    """Plugin long output of the last check"""

    services = wsme.wsattr([wtypes.text], mandatory=False)
    """The services of the host"""

    @classmethod
    def sample(cls):
        return cls(
            host_name='CoolHost',
            address="127.0.0.1",
            childs=['surveil.com'],
            parents=['parent.com'],
            description='Very Nice Host',
            state='OK',
            acknowledged=True,
            last_check=1429220785,
            last_state_change=1429220785,
            plugin_output='PING OK - Packet loss = 0%, RTA = 0.02 ms',
            long_output='The ping was great\nI love epic ping-pong games',
            services=['load', 'cpu', 'disk_usage']
        )
