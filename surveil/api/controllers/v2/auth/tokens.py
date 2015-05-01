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

import json

import pecan
from pecan import rest


class TokensController(rest.RestController):

    @pecan.expose()
    def post(self):
        """Retrieve an auth token."""

        access = {
            "access": {
                "token": {
                    "issued_at": "2014-01-30T15:30:58.819584",
                    "expires": "2014-01-31T15:30:58Z",
                    "id": "aaaaa-bbbbb-ccccc-dddd",
                    "tenant": {
                        "description": "Hey!",
                        "enabled": True,
                        "id": "fc394f2ab2df4114bde39905f800dc57",
                        "name": "demo"
                    }
                }
            }
        }
        return json.dumps(access)
