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

import requests_mock

from surveil.tests.api import functionalTest


class TestReloadConfigController(functionalTest.FunctionalTest):

    def test_reload_config(self):
        with requests_mock.Mocker() as m:
            m.register_uri(requests_mock.POST,
                           self.ws_arbiter_url + "/reload")

            response = self.post("/v2/config/reload_config")
            self.assertEqual(response.status_int, 200)
            self.assertEqual(
                m.last_request.path,
                '/reload'
            )
