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

from surveil.api.datamodel.status import live_query
from surveil.api.handlers.status import liveQuery_filter as query_filter
from surveil.tests import base


class LiveQueryFilterTest(base.BaseTestCase):

    def setUp(self):
        self.items = [
            {"description": "localhost",
             "last_state_change": 1429400991,
             "plugin_output": "OK - localhost: rta 0.047ms, lost 0%",
             "last_check": 1429400990,
             "state": 0,
             "host_name": "localhost"},
            {"description": "test_keystone",
             "last_state_change": 1429400986,
             "plugin_output": "OK - 127.0.0.1: rta 0.045ms, lost 0%",
             "last_check": 1429400984, "state": 2,
             "host_name": "test_keystone"},
            {"description": "ws-arbiter",
             "last_state_change": 1429400991,
             "plugin_output": "OK - localhost: rta 0.042ms, lost 0%",
             "last_check": 1429400990,
             "state": 2,
             "host_name": "ws-arbiter"}
        ]

    def test_query_builder_filter_isnot(self):
        query = live_query.LiveQuery(
            fields=json.dumps(['host_name', 'last_check']),
            filters=json.dumps({
                "isnot": {
                    "state": [0, 1],
                    "description": ["test_keystone"]
                }
            })
        )

        result = query_filter.filter_dict_list_with_live_query(
            self.items,
            query
        )

        expected = [{"last_check": 1429400990, "host_name": "ws-arbiter"}]

        self.assertItemsEqual(result, expected)

    def test_query_builder_filter_is(self):
        query = live_query.LiveQuery(
            fields=json.dumps(['host_name']),
            filters=json.dumps({
                "is": {
                    "state": [0],
                    "description": ["localhost"]
                }
            })
        )

        result = query_filter.filter_dict_list_with_live_query(
            self.items,
            query
        )

        expected = [{"host_name": "localhost"}]

        self.assertItemsEqual(result, expected)
