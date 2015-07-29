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

from surveil.api.datamodel import live_query
from surveil.api.datamodel.status import paging
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
            }),
            paging=paging.Paging(size=7, page=4)
        )

        service_mappings = {
            "last_check": "last_chk",
            "description": "service_description",
            "plugin_output": "output",
            "acknowledged": "problem_has_been_acknowledged",
        }
        lq = mongodb_query.translate_live_query(
            query.as_dict(),
            service_mappings
        )

        self.assertEqual(
            lq,
            {'fields': [u'host_name', 'last_chk'],
             'filters': {u'isnot': {u'state': [0, 1],
                                    'last_chk': [u'test_keystone']}},
             'paging': query.paging},
        )

        query, kwargs = mongodb_query.build_mongodb_query(lq)

        expected_query = {
            "state": {"$nin": [0, 1]},
            "last_chk": {"$nin": ["test_keystone"]}
        }

        expected_fields = {
            "host_name": 1,
            "last_chk": 1
        }

        self.assertEqual(query[0], expected_query)
        self.assertEqual(query[1], expected_fields)
        self.assertEqual(kwargs, {'limit': 7, 'skip': 28})
