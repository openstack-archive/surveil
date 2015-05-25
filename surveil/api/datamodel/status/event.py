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


class Event(types.Base):

    time = wsme.wsattr(wtypes.text, mandatory=True)
    """Timestamp of the alert"""

    event_type = wsme.wsattr(wtypes.text, mandatory=True)
    """Type of event. This is only ALERT"""

    host_name = wsme.wsattr(wtypes.text, mandatory=False)
    """Host which the alert is from."""

    service_description = wsme.wsattr(wtypes.text, mandatory=False)
    """Service which raised the alert"""

    state = wsme.wsattr(wtypes.text, mandatory=False)
    """State of the service or host who raised the alert"""

    # Alerts
    state_type = wsme.wsattr(wtypes.text, mandatory=False)
    """Confirmness level of the state [SOFT|HARD]"""

    attempts = wsme.wsattr(int, mandatory=False)
    """Number of attempts to confirm state"""

    # Downtime
    downtime_type = wsme.wsattr(wtypes.text, mandatory=False)
    """Type of alert. This is only HOST or SERVICE"""

    # Notifications
    notification_type = wsme.wsattr(wtypes.text, mandatory=False)

    notification_method = wsme.wsattr(wtypes.text, mandatory=False)

    contact = wsme.wsattr(wtypes.text, mandatory=False)

    acknowledgement = wsme.wsattr(wtypes.text, mandatory=False)

    # Alert, Flapping
    alert_type = wsme.wsattr(wtypes.text, mandatory=False)
    """Type of alert. This is only HOST or SERVICE"""

    # Alerts, Downtime, Flapping
    output = wsme.wsattr(wtypes.text, mandatory=False)
    """Additional output of the alert."""

    @classmethod
    def sample(cls):
        return cls(
            time='2015-06-04T18:55:12Z',
            event_type='ALERT',
            alert_type='SERVICE',
            host_name='CoolHost',
            service_description='Apache Service',
            state='CRITICAL',
            state_type='HARD',
            attempts=4,
            output='WARNING - load average: 5.04, 4.67, 5.04',
            notification_method='notify-service-by-email',
            notification_type=''
        )
