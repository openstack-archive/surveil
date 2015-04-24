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
from surveil.api.handlers.status import influxdb_query as query_filter
from surveil.tests import base


class LiveQueryFilterTest(base.BaseTestCase):

    def test_filter_fields(self):
        items = [
            {"description": "test_keystone",
             "last_state_change": 1429400986,
             "plugin_output": "OK - 127.0.0.1: rta 0.045ms, lost 0%",
             "last_check": 1429400984, "state": 2,
             "host_name": "test_keystone"},
            ]
        query = live_query.LiveQuery(
            fields=json.dumps(['host_name', 'last_check']),
            filters=json.dumps({
                "isnot": {
                    "state": [0, 1],
                    "description": ["test_keystone"]
                }
            })
        )

        result = query_filter.filter_fields(
            items,
            query
        )

        expected = [{"last_check": 1429400984, "host_name": "test_keystone"}]

        self.assertItemsEqual(result, expected)

    def test_build_where_clause(self):
        filters = {
            "is": {
                "state": [0],
                "description": ["test_keystone"]
            }
        }

        result = query_filter._build_where_clause(
            filters
        )

        expected = "WHERE state=0 AND description='test_keystone'"

        self.assertItemsEqual(result, expected)

    def test_build_where_clause_no_filters(self):
        filters = {}

        result = query_filter._build_where_clause(
            filters
        )

        expected = ""

        self.assertItemsEqual(result, expected)

    def test_build_influx_query(self):
        query = live_query.LiveQuery(
            fields=json.dumps(['host_name', 'last_check']),
            filters=json.dumps({}),
        )
        measurement = 'ALERT'
        group_by = ['*', 'host_name']
        limit = 10

        result = query_filter.build_influxdb_query(query,
                                                   measurement,
                                                   group_by,
                                                   limit)

        expected = "SELECT * FROM ALERT GROUP BY *, host_name LIMIT 10"

        self.assertItemsEqual(result, expected)
