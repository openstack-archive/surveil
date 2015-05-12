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
from surveil.api.handlers.status import fields_filter
from surveil.tests import base


class FieldsFilterTest(base.BaseTestCase):

    def test_filter_fields(self):
        items = [
            {"description": "test_keystone",
             "last_state_change": 1429400986,
             "plugin_output": "OK - 127.0.0.1: rta 0.045ms, lost 0%",
             "last_check": 1429400984, "state": 'OK',
             "host_name": "test_keystone"},
        ]

        query = live_query.LiveQuery(
            fields=['host_name', 'last_check'],
            filters=json.dumps({
                "isnot": {
                    "state": [0, 1],
                    "description": ["test_keystone"]
                }
            })
        )

        result = fields_filter.filter_fields(
            items,
            query
        )

        expected = [{"last_check": 1429400984, "host_name": "test_keystone"}]

        self.assert_count_equal_backport(result, expected)
