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

import httpretty

from surveil.tests.api import functionalTest


class TestDowntimeController(functionalTest.FunctionalTest):

    @httpretty.activate
    def test_downtime_post(self):
        httpretty.register_uri(httpretty.POST,
                               self.ws_arbiter_url + "/downtime")

        dt = {
            "host_name": "localhost",
            "duration": 86400
        }

        response = self.post_json("/v2/actions/downtime/", params=dt)

        self.assertEqual(response.status_int, 200)

        self.assertEqual(httpretty.last_request().body,
                         'duration=86400&action=add&host_name=localhost')
        self.assertEqual(httpretty.last_request().path,
                         '/downtime')

    @httpretty.activate
    def test_downtime_delete(self):
        httpretty.register_uri(httpretty.POST,
                               self.ws_arbiter_url + "/downtime")

        dt = {
            "host_name": "localhost",
            "duration": 86400
        }

        response = self.delete_json("/v2/actions/downtime/", params=dt)

        self.assertEqual(response.status_int, 200)

        self.assertEqual(httpretty.last_request().body,
                         'duration=86400&action=delete&host_name=localhost')
        self.assertEqual(httpretty.last_request().path,
                         '/downtime')
