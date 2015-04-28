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


class ContactGroup(types.Base):
    contactgroup_name = wsme.wsattr(wtypes.text, mandatory=True)
    members = wsme.wsattr(wtypes.text, mandatory=False)
    alias = wsme.wsattr(wtypes.text, mandatory=False)
    contactgroup_members = wsme.wsattr(wtypes.text, mandatory=False)

    @classmethod
    def sample(cls):
        return cls(
            contactgroup_name='novell-admins',
            alias='Novell Administrators',
            members='jdoe,rtobert,tzach'
        )
