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


class Service(types.Base):
    host_name = wsme.wsattr(wtypes.text, mandatory=True)

    service_description = wsme.wsattr(wtypes.text, mandatory=True)

    check_command = wsme.wsattr(wtypes.text, mandatory=True)

    max_check_attempts = wsme.wsattr(int, mandatory=True)

    check_interval = wsme.wsattr(int, mandatory=True)

    retry_interval = wsme.wsattr(int, mandatory=True)

    check_period = wsme.wsattr(wtypes.text, mandatory=True)

    notification_interval = wsme.wsattr(int, mandatory=True)

    notification_period = wsme.wsattr(wtypes.text, mandatory=True)

    contacts = wsme.wsattr(wtypes.text, mandatory=True)

    contact_groups = wsme.wsattr(wtypes.text, mandatory=True)

    @classmethod
    def sample(cls):
        return cls(
            host_name="sample-server",
            service_description="check-disk-sdb",
            check_command="check-disk!/dev/sdb1",
            max_check_attempts=5,
            check_interval=5,
            retry_interval=3,
            check_period="24x7",
            notification_interval=3,
            notification_period="24x7",
            contacts="surveil-ptl,surveil-bob",
            contact_groups="linux-admins",
        )
