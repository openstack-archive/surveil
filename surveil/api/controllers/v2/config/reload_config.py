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

import pecan
from pecan import rest
import requests
import wsmeext.pecan as wsme_pecan

from surveil.api.datamodel import info
from surveil.common import util


class ReloadConfigController(rest.RestController):

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(info.Info)
    def post(self):
        """Reloads Shinken's config."""

        requests.post(
            pecan.request.ws_arbiter_url + "/reload"
        )

        return info.Info(message='Arbiter reloading.')
