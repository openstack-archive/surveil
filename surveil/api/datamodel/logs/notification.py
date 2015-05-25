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


class Notification(types.Base):

    time = wsme.wsattr(wtypes.text, mandatory=True)
    """Timestamp of the alert"""

    notification_type = wsme.wsattr(wtypes.text, mandatory=False)

    event_type = wsme.wsattr(wtypes.text, mandatory=True)
    """Type of event. This is only Notification"""

    contact = wsme.wsattr(wtypes.text, mandatory=False)

    host_name = wsme.wsattr(wtypes.text, mandatory=False)
    """Host which the alert is from."""

    service_description = wsme.wsattr(wtypes.text, mandatory=False)
    """Service which raised the alert"""

    notification_method = wsme.wsattr(wtypes.text, mandatory=False)

    @classmethod
    def sample(cls):
        return cls(
            time=1375301662,
            event_type='NOTIFICATION',
            notification_type='HOST',
            contact='Aviau',
            hostname='CoolHost',
            service_desc='Apache Service',
            state='CRITICAL',
            notification_method='notify-service-by-email'
        )
