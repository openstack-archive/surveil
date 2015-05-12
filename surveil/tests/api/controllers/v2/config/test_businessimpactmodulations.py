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


class TestBusinessImpactModulationController(functionalTest.FunctionalTest):

    def setUp(self):
        super(TestBusinessImpactModulationController, self).setUp()
        self.modulations = [
            {
                'business_impact_modulation_name': 'LowImpactOnNight',
                'business_impact': 1,
                'modulation_period': 'night'
            },
            {
                'business_impact_modulation_name': 'LowImpactOnDay',
                'business_impact': 1,
                'modulation_period': 'day'
            },
        ]
        self.mongoconnection.shinken.businessimpactmodulations.insert(
            copy.deepcopy(self.modulations)
        )

    def test_get_all_modulations(self):
        response = self.get('/v2/config/businessimpactmodulations')

        self.assert_count_equal_backport(
            json.loads(response.body.decode()),
            [
                {'business_impact': 1,
                 'business_impact_modulation_name': 'LowImpactOnDay',
                 'modulation_period': 'day'},
                {'business_impact': 1,
                 'business_impact_modulation_name': 'LowImpactOnNight',
                 'modulation_period': 'night'},
            ]
        )
        self.assertEqual(response.status_int, 200)

    def test_get_one_modulation(self):
        response = self.get(
            '/v2/config/businessimpactmodulations/LowImpactOnDay'
        )

        self.assertEqual(
            json.loads(response.body.decode()),
            {'business_impact': 1,
             'business_impact_modulation_name': 'LowImpactOnDay',
             'modulation_period': 'day'}
        )

    def test_create_modulation(self):
        m = {'business_impact': 1,
             'business_impact_modulation_name': 'testtt',
             'modulation_period': 'day'}

        self.assertIsNone(
            self.mongoconnection.shinken.businessimpactmodulations.find_one(m)
        )

        self.post_json('/v2/config/businessimpactmodulations', m)

        self.assertIsNotNone(
            self.mongoconnection.shinken.businessimpactmodulations.find_one(m)
        )

    def test_delete_modulation(self):
        self.assertIsNotNone(
            self.mongoconnection.shinken.businessimpactmodulations.find_one(
                {"business_impact_modulation_name": 'LowImpactOnNight'}
            )
        )

        self.delete('/v2/config/businessimpactmodulations/LowImpactOnNight')

        self.assertIsNone(
            self.mongoconnection.shinken.timeperiods.find_one(
                {"business_impact_modulation_name": 'LowImpactOnNight'}
            )
        )

    def test_put_modulation(self):
        self.assertEqual(
            self.mongoconnection.shinken.businessimpactmodulations.find_one(
                {'business_impact_modulation_name': 'LowImpactOnNight'}
            )['modulation_period'],
            'night'
        )

        self.put_json(
            '/v2/config/businessimpactmodulations/LowImpactOnNight',
            {"business_impact_modulation_name": "LowImpactOnNight",
             'business_impact': 1,
             "modulation_period": 'updated'}
        )

        self.assertEqual(
            self.mongoconnection.shinken.businessimpactmodulations.find_one(
                {'business_impact_modulation_name': 'LowImpactOnNight'}
            )['modulation_period'],
            'updated'
        )
