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


class NotificationWay(types.Base):
    notificationway_name = wsme.wsattr(wtypes.text, mandatory=True)
    host_notification_period = wsme.wsattr(wtypes.text, mandatory=True)
    service_notification_period = wsme.wsattr(wtypes.text, mandatory=True)
    host_notification_options = wsme.wsattr(wtypes.text, mandatory=True)
    service_notification_options = wsme.wsattr(wtypes.text, mandatory=True)
    host_notification_commands = wsme.wsattr(wtypes.text, mandatory=True)
    service_notification_commands = wsme.wsattr(wtypes.text, mandatory=True)
    min_business_impact = wsme.wsattr(int, mandatory=False)

    @classmethod
    def sample(cls):
        return cls(
            notificationway_name="email_in_day",
            host_notification_period="24x7",
            service_notification_period="24x7",
            host_notification_options="d,u,r,f,s",
            service_notification_options="w,u,c,r,f",
            service_notification_commands="notify-service",
            host_notification_commands="notify-host"
            )
