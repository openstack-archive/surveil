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

AlertType = wsme.types.Enum(unicode, u'HOST', u'SERVICE')
EventType = wsme.types.Enum(unicode, u'ALERT', u'ALERTTEST')
StateType = wsme.types.Enum(unicode, u'SOFT', u'HARD')


class Alert(types.Base):
    # childs = wsme.wsattr([wtypes.text], mandatory=False)
    # """The childs of the host"""

    # parents = wsme.wsattr([wtypes.text], mandatory=False)
    # """The parents of the host"""

    time = wsme.wsattr(int, mandatory=True)
    """Timestamp of the alert"""

    alert_type = wsme.wsattr(AlertType, mandatory=True)
    """Type of alert. This is possibly only HOST or SERVICE"""

    # event_type = wsme.wsattr(EventType, mandatory=True)
    # """Type of event. This is possibly only ALERT"""

    hostname = wsme.wsattr(unicode, mandatory=False)
    """Host which the alert is from."""

    # service_desc = wsme.wsattr(unicode, mandatory=False)
    # """Service which raised the alert"""

    state = wsme.wsattr(unicode, mandatory=False)
    """State of the service or host who raised the alert"""

    state_type = wsme.wsattr(StateType, mandatory=False)
    """Confirmness level of the state [SOFT|HARD]"""

    attempts = wsme.wsattr(int, mandatory=False)
    """Number of attempts to confirm state"""

    output = wsme.wsattr(unicode, mandatory=False)
    """Additionnal output of the alert."""

    notification_type = wsme.wsattr(AlertType, mandatory=False)
    notification_method = wsme.wsattr(unicode, mandatory=False)

    @classmethod
    def sample(cls):
        return cls(
            time=1375301662,
            alert_type='SERVICE',
            # event_type='ALERT',
            hostname='CoolHost',
            # service_desc='Apache Service',
            state='CRITICAL',
            state_type='HARD',
            attempts='4',
            output='WARNING - load average: 5.04, 4.67, 5.04',
            notification_type='SERVICE',
            notification_method='notify-by-email'
        )
