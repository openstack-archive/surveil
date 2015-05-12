# Copyright 2014 - Savoir-Faire Linux inc.
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


class TestTimePeriodsController(functionalTest.FunctionalTest):

    def setUp(self):
        super(TestTimePeriodsController, self).setUp()
        self.timeperiods = [
            {
                'timeperiod_name': 'nonworkhours',
                'sunday': '00:00-24:00',
                'monday': '00:00-09:00,17:00-24:00'
            },
            {
                'timeperiod_name': 'misc-single-days',
                '1999-01-28': '00:00-24:00',
                'day 2': '00:00-24:00',
            },
        ]
        self.mongoconnection.shinken.timeperiods.insert(
            copy.deepcopy(self.timeperiods)
        )

    def test_get_all_timeperiods(self):
        response = self.get('/v2/config/timeperiods')

        self.assert_count_equal_backport(
            json.loads(response.body.decode()),
            [
                {'timeperiod_name': 'misc-single-days',
                 'periods': {'day 2': '00:00-24:00',
                             '1999-01-28': '00:00-24:00'}},
                {'timeperiod_name': 'nonworkhours',
                 'periods': {'sunday': '00:00-24:00',
                             'monday': '00:00-09:00,17:00-24:00'}}
            ]
        )
        self.assertEqual(response.status_int, 200)

    def test_get_one_timeperiod(self):
        response = self.get('/v2/config/timeperiods/nonworkhours')

        self.assertEqual(
            json.loads(response.body.decode()),
            {'timeperiod_name': 'nonworkhours',
             'periods': {'sunday': '00:00-24:00',
                         'monday': '00:00-09:00,17:00-24:00'}}
        )

    def test_create_timeperiod(self):
        t = {"timeperiod_name": 'someperiod',
             "periods": {
                 "monday": "fun day",
                 "tuesday": "pizza day"
             }}

        self.post_json('/v2/config/timeperiods', t)

        self.assertIsNotNone(
            self.mongoconnection.shinken.timeperiods.find_one(
                {"timeperiod_name": 'someperiod',
                 "monday": "fun day",
                 "tuesday": "pizza day"})
        )

    def test_delete_timeperiod(self):
        self.assertIsNotNone(
            self.mongoconnection.shinken.timeperiods.find_one(
                {"timeperiod_name": 'nonworkhours'}
            )
        )

        self.delete('/v2/config/timeperiods/nonworkhours')

        self.assertIsNone(
            self.mongoconnection.shinken.timeperiods.find_one(
                {"timeperiod_name": 'nonworkhours'}
            )
        )

    def test_put_timeperiod(self):
        self.assertEqual(
            self.mongoconnection.shinken.timeperiods.find_one(
                {'timeperiod_name': 'nonworkhours'}
            )['sunday'],
            '00:00-24:00'
        )

        self.put_json(
            '/v2/config/timeperiods/nonworkhours',
            {"timeperiod_name": "nonworkhours",
             "periods": {"sunday": "updated"}}
        )

        self.assertEqual(
            self.mongoconnection.shinken.timeperiods.find_one(
                {'timeperiod_name': 'nonworkhours'}
            )['sunday'],
            'updated'
        )
