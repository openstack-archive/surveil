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


class TestStatusServices(functionalTest.FunctionalTest):

    def setUp(self):
        super(TestStatusServices, self).setUp()
        self.services = [
            {
                "host_name": 'Webserver',
                "service_description": 'Apache',
                "description": 'Serves Stuff',
                "state": 'OK',
                "last_chk": 1429220785,
                "last_state_change": 1429220785,
                "plugin_output": 'HTTP OK - GOT NICE RESPONSE',
                "long_output": 'The response\nwas really\nnice',
                "problem_has_been_acknowledged": True,
            },
            {
                "host_name": 'someserver',
                "service_description": 'servicesomething',
                "description": 'Serves  lots of Stuff',
                "state": 'UNKNOWN',
                "last_chk": 1429220785,
                "last_state_change": 1429220785,
                "plugin_output": 'Hi there',
                "long_output": 'I am;\nthe servicessomthing;\noutput;',
                "problem_has_been_acknowledged": False,
            },
        ]
        self.mongoconnection.shinken_live.services.insert(
            copy.deepcopy(self.services)
        )

    def test_get_all_services(self):
        response = self.get("/v2/status/services")

        expected = [
            {
                "host_name": 'Webserver',
                "service_description": 'Apache',
                "description": 'Serves Stuff',
                "state": 'OK',
                "last_check": 1429220785,
                "last_state_change": 1429220785,
                "plugin_output": 'HTTP OK - GOT NICE RESPONSE',
                "long_output": 'The response\nwas really\nnice',
                'acknowledged': True,
            },
            {
                "host_name": 'someserver',
                "service_description": 'servicesomething',
                "description": 'Serves  lots of Stuff',
                "state": 'UNKNOWN',
                "last_check": 1429220785,
                "last_state_change": 1429220785,
                "plugin_output": 'Hi there',
                "long_output": 'I am;\nthe servicessomthing;\noutput;',
                'acknowledged': False,
            },
        ]

        self.assertEqual(json.loads(response.body.decode()),
                         expected)

    def test_query_services(self):
        query = {
            'fields': ['host_name', 'service_description'],
            'filters': json.dumps({
                "isnot": {
                    "host_name": ['ws-arbiter'],
                },
                "is": {
                    "service_description": ["Apache"],
                    "acknowledged": [True],
                }
            })
        }

        response = self.post_json("/v2/status/services", params=query)

        expected = [
            {'host_name': 'Webserver',
             'service_description': 'Apache'}
        ]

        self.assertEqual(json.loads(response.body.decode()),
                         expected)
