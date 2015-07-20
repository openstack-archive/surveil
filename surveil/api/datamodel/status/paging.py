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

from surveil.api.datamodel import types


class Paging(types.Base):

    size = wsme.wsattr(int, mandatory=True)
    """Size of the result."""

    page = wsme.wsattr(int, mandatory=True)
    """Page number."""

    @classmethod
    def sample(cls):
        return cls(
            page=1,
            size=100
        )
