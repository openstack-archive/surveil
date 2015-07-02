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

import pecan
from pecan import rest
import requests
import wsmeext.pecan as wsme_pecan

from surveil.api.datamodel import checkresult
from surveil.common import util


class CheckResultsSubController(rest.RestController):

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(body=checkresult.CheckResult, status_code=204)
    def post(self, data):
        """Submit a new check result.

        :param data: a check result within the request body.
        """
        result = data.as_dict()
        result['host_name'] = pecan.request.context['host_name']

        requests.post(
            pecan.request.ws_arbiter_url + "/push_check_result",
            data=result
        )
