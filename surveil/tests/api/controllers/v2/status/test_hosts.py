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

from surveil.tests.api import functionalTest


class TestStatusHosts(functionalTest.FunctionalTest):

    def setUp(self):
        super(TestStatusHosts, self).setUp()
        self.host = [
            {
                "display_name": "localhost",
                "address": "127.0.0.1",
                "childs": [],
                "parents": ['parent.com'],
                "last_chk": 1.429405764e+09,
                "last_state_change": 1.429405765316929e+09,
                "plugin_output": "OK - localhost: rta 0.033ms, lost 0%",
                "state": 0,
                "state_type": "HARD",
                "problem_has_been_acknowledged": True,
                "host_name": "localhost",
            },
            {
                "display_name": "test_keystone",
                "address": "127.0.0.1",
                "childs": [],
                "parents": ['parent.com'],
                "last_chk": 1.429405763e+09,
                "last_state_change": 1.429405765317144e+09,
                "plugin_output":  "OK - 127.0.0.1: rta 0.032ms, lost 0%",
                "state": 0,
                "state_type": "HARD",
                "problem_has_been_acknowledged": True,
                "host_name": "test_keystone",
            },
            {
                "display_name": "ws-arbiter",
                "address": "127.0.0.1",
                "childs": ['test_keystone'],
                "parents": ['parent.com'],
                "last_chk": 1.429405764e+09,
                "last_state_change": 1.429405765317063e+09,
                "plugin_output": "OK - localhost: rta 0.030ms, lost 0%",
                "state": 0,
                "state_type": "HARD",
                "problem_has_been_acknowledged": True,
                "host_name": "ws-arbiter",
            },
        ]
        self.mongoconnection.shinken_live.hosts.insert(
            copy.deepcopy(self.host)
        )

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

    def test_get_all_hosts(self):
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
             "acknowledged": True,
             "host_name": "localhost"},
            {"description": "test_keystone",
             "address": "127.0.0.1",
             "childs": [],
             "parents": ['parent.com'],
             "last_state_change": 1429405765,
             "plugin_output": "OK - 127.0.0.1: rta 0.032ms, lost 0%",
             "last_check": 1429405763,
             "state": 0,
             "acknowledged": True,
             "host_name": "test_keystone"},
            {"description": "ws-arbiter",
             "address": "127.0.0.1",
             "childs": ['test_keystone'],
             "parents": ['parent.com'],
             "last_state_change": 1429405765,
             "plugin_output": "OK - localhost: rta 0.030ms, lost 0%",
             "last_check": 1429405764,
             "state": 0,
             "acknowledged": True,
             "host_name": "ws-arbiter"}]

        self.assertItemsEqual(json.loads(response.body), expected)

    def test_query_hosts(self):
        query = {
            'fields': ['host_name', 'last_check'],
            'filters': json.dumps({
                "isnot": {
                    "host_name": ['localhost'],
                    "description": ['test_keystone']
                }
            })
        }

        response = self.post_json("/v2/status/hosts", params=query)

        expected = [{"host_name": "ws-arbiter", "last_check": 1429405764}]

        self.assertItemsEqual(json.loads(response.body), expected)

    def test_get_specific_host(self):

        response = self.get("/v2/status/hosts/localhost")

        expected = {"childs": ["test_keystone"],
                    "parents": ['parent.com'],
                    "description": "localhost",
                    "last_state_change": 1429812192,
                    "acknowledged": True,
                    "plugin_output": "OK - localhost: rta 0.044ms, lost 0%",
                    "last_check": 1429812191,
                    "state": 0,
                    "host_name": "localhost",
                    "address": "localhost"}

        self.assertItemsEqual(json.loads(response.body), expected)

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
