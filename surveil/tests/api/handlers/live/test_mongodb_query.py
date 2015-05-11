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
from surveil.api.handlers.status import live_service_handler
from surveil.api.handlers.status import mongodb_query
from surveil.tests import base


class MongoDBQueryTest(base.BaseTestCase):

    def test_build_mongo_query(self):
        query = live_query.LiveQuery(
            fields=['host_name', 'last_check'],
            filters=json.dumps({
                "isnot": {
                    "state": [0, 1],
                    "last_check": ["test_keystone"]
                }
            })
        )

        lq_filters, lq_fields = live_service_handler._translate_live_query(
            query
        )

        self.assertEqual(
            lq_fields, ['host_name', 'last_chk']
        )

        self.assertEqual(lq_filters,
                         {'isnot': {'state': [0, 1],
                                    'last_chk': ['test_keystone']}})

        query, fields = mongodb_query.build_mongodb_query(lq_filters,
                                                          lq_fields)

        expected_query = {
            "state": {"$nin": [0, 1]},
            "last_chk": {"$nin": ["test_keystone"]}
        }

        expected_fields = {
            "host_name": 1,
            "last_chk": 1
        }

        self.assertEqual(query, expected_query)
        self.assertEqual(fields, expected_fields)
