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


class Host(types.Base):
    host_name = wsme.wsattr(wtypes.text, mandatory=False)
    """The name of the host"""

    address = wsme.wsattr(wtypes.text, mandatory=False)
    """The address of the host. Normally, this is an IP address."""

    max_check_attempts = wsme.wsattr(int, mandatory=False)

    check_period = wsme.wsattr(wtypes.text, mandatory=False)
    """The time period during which active checks of this host can be made."""

    contacts = wsme.wsattr(wtypes.ArrayType(wtypes.text), mandatory=False)
    """A list of the short names of the contacts that should be notified."""

    contact_groups = wsme.wsattr(wtypes.ArrayType(wtypes.text),
                                 mandatory=False)
    """List of the short names of contact groups that should be notified"""

    notification_interval = wsme.wsattr(int, mandatory=False)

    notification_period = wsme.wsattr(wtypes.text, mandatory=False)

    use = wsme.wsattr(wtypes.ArrayType(wtypes.text), mandatory=False)
    """The template to use for this host"""

    name = wsme.wsattr(wtypes.text, mandatory=False)

    # TODO(aviau): int!
    register = wsme.wsattr(wtypes.text, mandatory=False)

    check_interval = wsme.wsattr(int, mandatory=False)

    retry_interval = wsme.wsattr(int, mandatory=False)

    passive_checks_enabled = wsme.wsattr(wtypes.text, mandatory=False)

    # TODO(aviau): Custom fields starting without '_' should raise an error.
    custom_fields = wsme.wsattr(
        wtypes.DictType(wtypes.text, wtypes.text),
        mandatory=False
    )
    """Custom fields for the host"""

    @classmethod
    def sample(cls):
        return cls(
            use=["generic-host"],
            host_name="bogus-router",
            address="192.168.1.254",
            max_check_attempts=5,
            check_period="24x7",
            contacts=["admin",
                      "carl"],
            contact_groups=["router-admins"],
            notification_interval=30,
            notification_period="24x7",
            custom_fields={"OS_AUTH_URL": "http://localhost:8080/v2"}
        )
