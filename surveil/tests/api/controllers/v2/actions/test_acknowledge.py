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


class TestAcknowledgeController(functionalTest.FunctionalTest):

    @httpretty.activate
    def test_acknowledge_add(self):
        httpretty.register_uri(httpretty.POST,
                               self.ws_arbiter_url + "/acknowledge")

        ack = {
            "host_name": "localhost"
        }

        response = self.post_json("/v2/actions/acknowledge/", params=ack)

        self.assertEqual(response.status_int, 200)

        self.assert_count_equal_backport(httpretty.last_request().body.decode()
                                         .split('&'),
                                         ['host_name=localhost', 'action=add'])
        self.assertEqual(httpretty.last_request().path,
                         '/acknowledge')

    @httpretty.activate
    def test_acknowledge_delete(self):
        httpretty.register_uri(httpretty.POST,
                               self.ws_arbiter_url + "/downtime")

        ack = {
            "host_name": "localhost",
        }

        response = self.delete_json("/v2/actions/downtime/", params=ack)

        self.assertEqual(response.status_int, 200)

        self.assert_count_equal_backport(httpretty.last_request().body.decode()
                                         .split('&'),
                                         ['host_name=localhost',
                                          'action=delete'])
        self.assertEqual(httpretty.last_request().path,
                         '/downtime')
