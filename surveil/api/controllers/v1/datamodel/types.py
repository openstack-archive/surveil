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

import inspect

import wsme
from wsme import types as wtypes


class Base(wtypes.Base):
    """Base class for all API types."""

    def as_dict(self):
        keys = [
            member[0] for member
            in inspect.getmembers(self.__class__)
            if member[0][0] is not '_' and type(member[1]) is wtypes.wsattr
        ]
        return self.as_dict_from_keys(keys)

    def as_dict_from_keys(self, keys):
        return dict((k, getattr(self, k))
                    for k in keys
                    if hasattr(self, k) and
                    getattr(self, k) != wsme.Unset)
