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
    host_name = wsme.wsattr(wtypes.text, mandatory=True)
    """The name of the host"""

    address = wsme.wsattr(wtypes.text, mandatory=False)
    """The address of the host. Normally, this is an IP address."""

    max_check_attempts = wsme.wsattr(int, mandatory=False, default=3)

    check_period = wsme.wsattr(wtypes.text, mandatory=False, default='24x7')
    """The time period during which active checks of this host can be made."""

    contacts = wsme.wsattr(wtypes.text, mandatory=False, default='')
    """A list of the short names of the contacts that should be notified."""

    contact_groups = wsme.wsattr(wtypes.text, mandatory=False, default='')
    """List of the short names of the contact groups that should be notified"""

    notification_interval = wsme.wsattr(int, mandatory=False, default=30)

    notification_period = wsme.wsattr(wtypes.text, mandatory=False,
                                      default='24x7')

    use = wsme.wsattr(wtypes.text, mandatory=False)
    """The template to use for this host"""

    # TODO(aviau): Custom fields starting without '_' should raise an error.
    custom_fields = wsme.wsattr(
        wtypes.DictType(wtypes.text, wtypes.text),
        mandatory=False
    )
    """Custom fields for the host"""

    def __init__(self, **kwargs):
        super(Host, self).__init__(**kwargs)

        # Custom fields start with '_'. Detect them ans assign them.
        custom_fields = [i for i in kwargs.items()
                         if (isinstance(i[0], str)
                             or isinstance(i[0], unicode))
                         and i[0][0] == '_']

        if len(custom_fields) > 0:
            self.custom_fields = {}
            for item in custom_fields:
                self.custom_fields[item[0]] = item[1]

    def as_dict(self):
        host_dict = super(Host, self).as_dict()
        custom_fields = host_dict.pop("custom_fields", None)
        if custom_fields:
            for item in custom_fields.items():
                host_dict[item[0]] = item[1]
        return host_dict

    @classmethod
    def sample(cls):
        return cls(
            use="generic-host",
            host_name="bogus-router",
            address="192.168.1.254",
            max_check_attempts=5,
            check_period="24x7",
            contacts="admin,carl",
            contact_groups="router-admins",
            notification_interval=30,
            notification_period="24x7",
            custom_fields={"OS_AUTH_URL": "http://localhost:8080/v2"}
        )
