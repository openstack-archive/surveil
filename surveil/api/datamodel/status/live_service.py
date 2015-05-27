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


class LiveService(types.Base):
    host_name = wsme.wsattr(wtypes.text, mandatory=False)
    """The host for the service"""

    service_description = wsme.wsattr(wtypes.text, mandatory=False)
    """The name of the service"""

    description = wsme.wsattr(wtypes.text, mandatory=False)
    """The description of the sevice"""

    state = wsme.wsattr(wtypes.text, mandatory=False)
    """The current state of the service"""

    acknowledged = wsme.wsattr(bool, mandatory=False)
    """Wether or not the problem, if any, has been acknowledged"""

    last_check = wsme.wsattr(int, mandatory=False)
    """The last time the service was checked"""

    last_state_change = wsme.wsattr(int, mandatory=False)
    """The last time the state has changed"""

    plugin_output = wsme.wsattr(wtypes.text, mandatory=False)
    """Plugin output of the last check"""

    long_output = wsme.wsattr(wtypes.text, mandatory=False)
    """Plugin long output of the last check"""

    @classmethod
    def sample(cls):
        return cls(
            host_name='Webserver',
            service_description='Apache',
            description='Serves Stuff',
            state='OK',
            last_check=1429220785,
            last_state_change=1429220785,
            plugin_output='HTTP OK - GOT NICE RESPONSE',
            acknowledged=True,
            long_output='Serves /var/www/\nServes /home/webserver/www/'
        )
