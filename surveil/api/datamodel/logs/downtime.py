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

    time = wsme.wsattr(wtypes.text, mandatory=True)
    """Timestamp of the alert"""

    event_type = wsme.wsattr(wtypes.text, mandatory=True)
    """Type of event. This is only DOWNTIME"""

    downtime_type = wsme.wsattr(wtypes.text, mandatory=False)
    """Type of alert. This is only HOST or SERVICE"""

    host_name = wsme.wsattr(wtypes.text, mandatory=False)
    """Host which the alert is from."""

    state = wsme.wsattr(wtypes.text, mandatory=False)
    """State of the service or host who raised the alert"""

    output = wsme.wsattr(wtypes.text, mandatory=False)
    """Additionnal output of the alert."""

    @classmethod
    def sample(cls):
        return cls(
            time=1375301662,
            event_type='DOWNTIME',
            hostname='CoolHost',
            state='CRITICAL',
            output='WARNING - load average: 5.04, 4.67, 5.04',
            downtime_type='HOST'
        )
