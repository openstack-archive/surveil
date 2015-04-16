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

import json

import httpretty

from surveil.tests.api import functionalTest


class TestStatusHosts(functionalTest.FunctionalTest):

    def setUp(self):
        super(TestStatusHosts, self).setUp()
        self.influxdb_response = (
            '{"results":[{"series":[{"name":"HOST_STATE","tags":{"host_nam'
            'e":"localhost"},"columns":["time","last_check","last_state_chan'
            'ge","output","state","state_type"],"values":[["201'
            '5-04-19T01:09:24Z",1.429405764e+09,1.429405765316929e+09,"OK '
            '- localhost: rta 0.033ms, lost 0%",0,"HARD"]]},{"name":"'
            'HOST_STATE","tags":{"host_name":"test_keystone"},"columns":["'
            'time","last_check","last_state_change","output","state",'
            '"state_type"],"values":[["2015-04-19T01:09:23Z",1.4294057'
            '63e+09,1.429405765317144e+09,"OK - 127.0.0.1: rta 0.032ms, lo'
            'st 0%",0,"HARD"]]},{"name":"HOST_STATE","tags":{"host_na'
            'me":"ws-arbiter"},"columns":["time","last_check","last_state_ch'
            'ange","output","state","state_type"],"values":[["2'
            '015-04-19T01:09:24Z",1.429405764e+09,1.429405765317063e+09,"O'
            'K - localhost: rta 0.030ms, lost 0%",0,"HARD"]]}]}]}'
        )

    @httpretty.activate
    def test_get_all_hosts(self):
        httpretty.register_uri(httpretty.GET,
                               "http://influxdb:8086/query",
                               body=self.influxdb_response)

        response = self.app.get("/v2/status/hosts")

        expected = [
            {"description": "localhost",
             "last_state_change": 1429405765,
             "plugin_output": "OK - localhost: rta 0.033ms, lost 0%",
             "last_check": 1429405764,
             "state": 0,
             "host_name": "localhost"},
            {"description": "test_keystone",
             "last_state_change": 1429405765,
             "plugin_output": "OK - 127.0.0.1: rta 0.032ms, lost 0%",
             "last_check": 1429405763,
             "state": 0,
             "host_name": "test_keystone"},
            {"description": "ws-arbiter",
             "last_state_change": 1429405765,
             "plugin_output": "OK - localhost: rta 0.030ms, lost 0%",
             "last_check": 1429405764,
             "state": 0,
             "host_name": "ws-arbiter"}]

        self.assertEqual(json.loads(response.body), expected)

    @httpretty.activate
    def test_query_hosts(self):
        httpretty.register_uri(httpretty.GET,
                               "http://influxdb:8086/query",
                               body=self.influxdb_response)

        query = {
            'fields': json.dumps(['host_name', 'last_check']),
            'filters': json.dumps({
                "isnot": {
                    "host_name": ['localhost'],
                    "description": ["test_keystone"]
                }
            })
        }

        response = self.app.post_json("/v2/status/hosts", params=query)

        expected = [{"host_name": "ws-arbiter", "last_check": 1429405764}]

        self.assertEqual(json.loads(response.body), expected)
