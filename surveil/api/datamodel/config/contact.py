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


class Contact(types.Base):
    contact_name = wsme.wsattr(wtypes.text, mandatory=True)

    host_notifications_enabled = wsme.wsattr(int, mandatory=False)

    service_notifications_enabled = wsme.wsattr(int, mandatory=False)

    host_notification_period = wsme.wsattr(wtypes.text, mandatory=False)

    service_notification_period = wsme.wsattr(wtypes.text, mandatory=False)

    host_notification_options = wsme.wsattr(wtypes.text, mandatory=False)

    service_notification_options = wsme.wsattr(wtypes.text, mandatory=False)

    host_notification_commands = wsme.wsattr(wtypes.text, mandatory=False)

    service_notification_commands = wsme.wsattr(wtypes.text, mandatory=False)

    email = wsme.wsattr(wtypes.text, mandatory=False)

    pager = wsme.wsattr(wtypes.text, mandatory=False)

    can_submit_commands = wsme.wsattr(int, mandatory=False)

    is_admin = wsme.wsattr(int, mandatory=False)

    retain_status_information = wsme.wsattr(int, mandatory=False)

    retain_nonstatus_information = wsme.wsattr(int, mandatory=False)

    min_business_impact = wsme.wsattr(int, mandatory=False)

    @classmethod
    def sample(cls):
        return cls(
            contact_name='admin',
            host_notifications_enabled=1,
            service_notifications_enabled=1,
        )
