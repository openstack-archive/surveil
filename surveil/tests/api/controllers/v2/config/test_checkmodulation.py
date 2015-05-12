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


class TestCheckModulationsController(functionalTest.FunctionalTest):

    def setUp(self):
        super(TestCheckModulationsController, self).setUp()
        self.checkmodulations = [
            {
                'checkmodulation_name': 'ping_night',
                'check_command': 'check_ping_night',
                'check_period': 'night'
            },
            {
                'checkmodulation_name': 'ping_day',
                'check_command': 'check_ping_day',
                'check_period': 'day',
            },
        ]
        self.mongoconnection.shinken.checkmodulations.insert(
            copy.deepcopy(self.checkmodulations)
        )

    def test_get_all_checkmodulations(self):
        response = self.get('/v2/config/checkmodulations')

        self.assert_count_equal_backport(
            json.loads(response.body.decode()),
            [
                {'checkmodulation_name': 'ping_day',
                 'check_command': 'check_ping_day',
                 'check_period': 'day'},
                {'checkmodulation_name': 'ping_night',
                 'check_command': 'check_ping_night',
                 'check_period': 'night'}
            ]
        )
        self.assertEqual(response.status_int, 200)

    def test_get_one_checkmodulation(self):
        response = self.get('/v2/config/checkmodulations/ping_night')

        self.assertEqual(
            json.loads(response.body.decode()),
            {'checkmodulation_name': 'ping_night',
             'check_command': 'check_ping_night',
             'check_period': 'night'}
        )

    def test_create_checkmodulation(self):
        t = {"checkmodulation_name": "ping_evening",
             "check_command": "check_ping_evening",
             "check_period": "evening"
             }

        self.post_json('/v2/config/checkmodulations', t)
        self.assertIsNotNone(
            self.mongoconnection.shinken.checkmodulations.find_one(
                {"checkmodulation_name": 'ping_evening',
                 "check_command": "check_ping_evening",
                 "check_period": "evening"})
        )

    def test_delete_checkmodulation(self):
        self.assertIsNotNone(
            self.mongoconnection.shinken.checkmodulations.find_one(
                {"checkmodulation_name": 'ping_night'}
            )
        )

        self.delete('/v2/config/checkmodulations/ping_night')

        self.assertIsNone(
            self.mongoconnection.shinken.checkmodulations.find_one(
                {"checkmodulation_name": 'ping_night'}
            )
        )

    def test_put_checkmodulation(self):
        self.assertEqual(
            self.mongoconnection.shinken.checkmodulations.find_one(
                {'checkmodulation_name': 'ping_night'}
            )['check_command'],
            'check_ping_night'
        )

        self.put_json(
            '/v2/config/checkmodulations/ping_night',
            {"checkmodulation_name": "ping_night",
             "check_command": "updated",
             "check_period": 'night'}
        )

        self.assertEqual(
            self.mongoconnection.shinken.checkmodulations.find_one(
                {'checkmodulation_name': 'ping_night'}
            )['check_command'],
            'updated'
        )
