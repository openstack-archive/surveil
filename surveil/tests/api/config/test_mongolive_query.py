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
from surveil.api.handlers.config import mongoengine_query
from surveil.tests import base


class MongoliveQueryTest(base.BaseTestCase):

    def test_build_mongo_query(self):
        query = live_query.LiveQuery(
            fields=['host_name', 'last_check'],
            filters=json.dumps({
                "isnot": {
                    "state": ["0", "1"],
                    "host_state": ["2"]
                },
                "is": {
                    "event_type": ["ALERT"]
                },
                "defined": {
                    "name": True
                }
            }),
            paging=paging.Paging(
                page=3,
                size=100
            )

        )

        fields, query, kwargs = mongoengine_query.build_mongoengine_query(
            query)

        self.assertEqual(
            fields,
            ['host_name', 'last_check']
        )

        self.assertEqual(
            query,
            {"state__nin": ["0", "1"],
             "host_state__nin": ["2"],
             "event_type__in": ["ALERT"],
             "name__exists": True, }
        )

        self.assertEqual(
            kwargs,
            slice(300, 400)
        )