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

import copy
import json

import httpretty

from surveil.tests.api import functionalTest


class TestStatusHosts(functionalTest.FunctionalTest):

    def setUp(self):
        super(TestStatusHosts, self).setUp()
        self.influxdb_response = json.dumps({
            "results": [
                {
                    "series": [
                        {"name": "LIVE_HOST_STATE",
                         "tags": {"host_name": "localhost",
                                  "address": "127.0.0.1",
                                  "childs": '[]',
                                  "parents": '["parent.com"]'},
                         "columns": [
                             "time",
                             "last_check",
                             "last_state_change",
                             "output",
                             "state",
                             "state_type",
                             "acknowledged"
                         ],
                         "values":[
                             ["2015-04-19T01:09:24Z",
                              1.429405764e+09,
                              1.429405765316929e+09,
                              "OK - localhost: rta 0.033ms, lost 0%",
                              0,
                              "HARD",
                              0]
                         ]},
                        {"name": "LIVE_HOST_STATE",
                         "tags": {"host_name": "test_keystone",
                                  "address": "127.0.0.1",
                                  "childs": '[]',
                                  "parents": '["parent.com"]'},
                         "columns": [
                             "time",
                             "last_check",
                             "last_state_change",
                             "output",
                             "state",
                             "state_type",
                             "acknowledged"
                         ],
                         "values":[
                             ["2015-04-19T01:09:23Z",
                              1.429405763e+09,
                              1.429405765317144e+09,
                              "OK - 127.0.0.1: rta 0.032ms, lost 0%",
                              0,
                              "HARD",
                              0]
                         ]},
                        {"name": "LIVE_HOST_STATE",
                         "tags": {"host_name": "ws-arbiter",
                                  "address": "127.0.0.1",
                                  "childs": '["test_keystone"]',
                                  "parents": '["parent.com"]'},
                         "columns": [
                             "time",
                             "last_check",
                             "last_state_change",
                             "output",
                             "state",
                             "state_type",
                             "acknowledged"
                         ],
                         "values":[
                             ["2015-04-19T01:09:24Z",
                              1.429405764e+09,
                              1.429405765317063e+09,
                              "OK - localhost: rta 0.030ms, lost 0%",
                              0,
                              "HARD",
                              0]
                         ]}
                    ]
                }
            ]
        })

        self.services = [
            {
                "host_name": 'Webserver',
                "service_description": 'Apache',
                "description": 'Serves Stuff',
                "state": 'OK',
                "last_check": 1429220785,
                "last_state_change": 1429220785,
                "plugin_output": 'HTTP OK - GOT NICE RESPONSE'
            },
            {
                "host_name": 'someserver',
                "service_description": 'servicesomething',
                "description": 'Serves  lots of Stuff',
                "state": 'OK',
                "last_check": 1429220785,
                "last_state_change": 1429220785,
                "plugin_output": 'Hi there'
            },
        ]
        self.mongoconnection.shinken_live.services.insert(
            copy.deepcopy(self.services)
        )

    @httpretty.activate
    def test_get_all_hosts(self):
        httpretty.register_uri(httpretty.GET,
                               "http://influxdb:8086/query",
                               body=self.influxdb_response)

        response = self.get("/v2/status/hosts")

        expected = [
            {"description": "localhost",
             "address": "127.0.0.1",
             "childs": [],
             "parents": ['parent.com'],
             "last_state_change": 1429405765,
             "plugin_output": "OK - localhost: rta 0.033ms, lost 0%",
             "last_check": 1429405764,
             "state": 0,
             "acknowledged": 0,
             "host_name": "localhost"},
            {"description": "test_keystone",
             "address": "127.0.0.1",
             "childs": [],
             "parents": ['parent.com'],
             "last_state_change": 1429405765,
             "plugin_output": "OK - 127.0.0.1: rta 0.032ms, lost 0%",
             "last_check": 1429405763,
             "state": 0,
             "acknowledged": 0,
             "host_name": "test_keystone"},
            {"description": "ws-arbiter",
             "address": "127.0.0.1",
             "childs": ['test_keystone'],
             "parents": ['parent.com'],
             "last_state_change": 1429405765,
             "plugin_output": "OK - localhost: rta 0.030ms, lost 0%",
             "last_check": 1429405764,
             "state": 0,
             "acknowledged": 0,
             "host_name": "ws-arbiter"}]

        self.assertItemsEqual(json.loads(response.body), expected)
        self.assertEqual(
            httpretty.last_request().querystring['q'],
            ["SELECT * FROM LIVE_HOST_STATE "
             "GROUP BY host_name, address, childs, parents "
             "ORDER BY time DESC LIMIT 1"]
        )

    @httpretty.activate
    def test_query_hosts(self):
        influxdb_response = json.dumps({
            "results": [
                {
                    "series": [
                        {"name": "LIVE_HOST_STATE",
                         "tags": {"host_name": "ws-arbiter",
                                  "address": "127.0.0.1",
                                  "childs": '["test_keystone"]',
                                  "parents": '["parent.com"]'},
                         "columns": [
                             "time",
                             "last_check",
                             "last_state_change",
                             "output",
                             "state",
                             "state_type",
                             "acknowledged"
                         ],
                         "values":[
                             ["2015-04-19T01:09:24Z",
                              1.429405764e+09,
                              1.429405765317063e+09,
                              "OK - localhost: rta 0.030ms, lost 0%",
                              0,
                              "HARD",
                              0]
                         ]}
                    ]
                }
            ]
        })
        httpretty.register_uri(httpretty.GET,
                               "http://influxdb:8086/query",
                               body=influxdb_response)

        query = {
            'fields': ['host_name', 'last_check'],
            'filters': json.dumps({
                "isnot": {
                    "host_name": ['localhost'],
                    "description": ["test_keystone"]
                }
            })
        }

        response = self.post_json("/v2/status/hosts", params=query)

        expected = [{"host_name": "ws-arbiter", "last_check": 1429405764}]

        self.assertItemsEqual(json.loads(response.body), expected)

        self.assertEqual(
            httpretty.last_request().querystring['q'],
            ["SELECT * FROM LIVE_HOST_STATE WHERE host_name!='localhost' "
             "AND description!='test_keystone' "
             "GROUP BY host_name, address, childs, parents "
             "ORDER BY time DESC "
             "LIMIT 1"]
        )

    @httpretty.activate
    def test_get_specific_host(self):
        influx_response = json.dumps(
            {"results": [
                {"series": [
                    {"name": "LIVE_HOST_STATE",
                     "tags": {"address": "localhost",
                              "childs": "[\"test_keystone\"]",
                              "parents": '["parent.com"]',
                              "host_name": "localhost"},
                     "columns": ["time",
                                 "acknowledged",
                                 "last_check",
                                 "last_state_change",
                                 "output",
                                 "state",
                                 "state_type"],
                     "values":[["2015-04-23T18:03:11Z",
                                0,
                                1.429812191e+09,
                                1.429812192166997e+09,
                                "OK - localhost: rta 0.044ms, lost 0%",
                                0,
                                "HARD"]]}]}]}
        )

        httpretty.register_uri(httpretty.GET,
                               "http://influxdb:8086/query",
                               body=influx_response)

        response = self.get("/v2/status/hosts/localhost")

        expected = {"childs": ["test_keystone"],
                    "parents": ['parent.com'],
                    "description": "localhost",
                    "last_state_change": 1429812192,
                    "acknowledged": 0,
                    "plugin_output": "OK - localhost: rta 0.044ms, lost 0%",
                    "last_check": 1429812191,
                    "state": 0,
                    "host_name": "localhost",
                    "address": "localhost"}

        self.assertItemsEqual(json.loads(response.body), expected)

        self.assertEqual(
            httpretty.last_request().querystring['q'],
            ["SELECT * from LIVE_HOST_STATE WHERE host_name='localhost'"
             " GROUP BY * "
             "ORDER BY time DESC "
             "LIMIT 1"]
        )

    def test_get_specific_host_service(self):
        response = self.get(
            "/v2/status/hosts/someserver/services/servicesomething"
        )
        expected = {'description': 'check-ws-arbiter',
                    'last_state_change': 1429823532,
                    'plugin_output': ('TCP OK - 0.000 second '
                                      'response time on port 7760'),
                    'last_check': 1429823531,
                    'state': 'OK',
                    'host_name': 'ws-arbiter',
                    'service_description': 'check-ws-arbiter'}
        self.assertItemsEqual(json.loads(response.body), expected)
