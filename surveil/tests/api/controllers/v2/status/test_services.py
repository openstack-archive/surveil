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
                "state": 0,
                "last_check": 1429220785,
                "last_state_change": 1429220785,
                "plugin_output": 'HTTP OK - GOT NICE RESPONSE'
            },
            {
                "host_name": 'someserver',
                "service_description": 'servicesomething',
                "description": 'Serves  lots of Stuff',
                "state": 1,
                "last_check": 1429220785,
                "last_state_change": 1429220785,
                "plugin_output": 'Hi there'
            },
        ]
        self.mongoconnection.shinken_live.services.insert(
            copy.deepcopy(self.services)
        )

    def test_get_all_services(self):
        response = self.get("/v2/status/services")
        self.assertItemsEqual(json.loads(response.body), self.services)

    def test_query_services(self):
        query = {
            'fields': json.dumps(['host_name', 'service_description']),
            'filters': json.dumps({
                "isnot": {
                    "host_name": ['ws-arbiter'],
                },
                "is": {
                    "service_description": ["Apache"]
                }
            })
        }

        response = self.post_json("/v2/status/services", params=query)

        expected = [
            {'host_name': 'Webserver',
             'service_description': 'Apache'}
        ]

        self.assertEqual(json.loads(response.body), expected)
