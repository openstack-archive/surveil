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
from surveil.api.handlers.status import influxdb_query
from surveil.tests import base


class LiveQueryFilterTest(base.BaseTestCase):

    def test_build_where_clause(self):
        filters = {
            "is": {
                "state": [0],
                "description": ["test_keystone"]
            }
        }

        result = influxdb_query._build_where_clause(
            filters
        )

        expected = "WHERE state=0 AND description='test_keystone'"

        self.assert_count_equal_backport(result, expected)

    def test_build_where_clause_no_filters(self):
        filters = {}

        result = influxdb_query._build_where_clause(
            filters
        )

        expected = ""

        self.assert_count_equal_backport(result, expected)

    def test_build_influx_query(self):
        query = live_query.LiveQuery(
            fields=['host_name', 'last_check'],
            filters=json.dumps({}),
        )
        measurement = 'ALERT'
        group_by = ['*', 'host_name']
        limit = 10

        result = influxdb_query.build_influxdb_query(query,
                                                     measurement,
                                                     group_by=group_by,
                                                     limit=limit)

        expected = "SELECT * FROM ALERT GROUP BY *, host_name LIMIT 10"

        self.assert_count_equal_backport(result, expected)

    def test_build_influx_query_orderby(self):
        query = live_query.LiveQuery(
            fields=['host_name', 'last_check'],
            filters=json.dumps({}),
        )
        measurement = 'ALERT'
        group_by = ['*', 'host_name']
        order_by = ['time DESC']
        limit = 10

        result = influxdb_query.build_influxdb_query(query,
                                                     measurement,
                                                     group_by=group_by,
                                                     order_by=order_by,
                                                     limit=limit)

        expected = ("SELECT * FROM ALERT "
                    "GROUP BY *, host_name "
                    "ORDER BY time DESC LIMIT 10")

        self.assert_count_equal_backport(result, expected)
