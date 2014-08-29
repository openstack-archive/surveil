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


class Host(types.Base):
    host_name = wsme.wsattr(wtypes.text, mandatory=True)
    """The name of the host"""

    address = wsme.wsattr(wtypes.text, mandatory=True)
    """The address of the host. Normally, this is an IP address."""

    max_check_attempts = wsme.wsattr(int, mandatory=True)

    check_period = wsme.wsattr(wtypes.text, mandatory=True)
    """The time period during which active checks of this host can be made."""

    contacts = wsme.wsattr(wtypes.text, mandatory=True)
    """A list of the short names of the contacts that should be notified."""

    contact_groups = wsme.wsattr(wtypes.text, mandatory=True)
    """List of the short names of the contact groups that should be notified"""

    notification_interval = wsme.wsattr(int, mandatory=True)

    notification_period = wsme.wsattr(wtypes.text, mandatory=True)

    @classmethod
    def sample(cls):
        return cls(
            host_name="bogus-router",
            address="192.168.1.254",
            max_check_attempts=5,
            check_period="24x7",
            contacts="admin,carl",
            contact_groups="router-admins",
            notification_interval=30,
            notification_period="24x7",
        )
