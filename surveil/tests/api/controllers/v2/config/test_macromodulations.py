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


class TestMacroModulationController(functionalTest.FunctionalTest):

    def setUp(self):
        super(TestMacroModulationController, self).setUp()
        self.modulations = [
            {
                'macromodulation_name': 'HighDuringNight',
                'modulation_period': 'night',
                '_CRITICAL': 20,
                '_WARNING': 10,
            },
            {
                'macromodulation_name': 'LowDuringNight',
                'modulation_period': 'night',
                '_CRITICAL': 10,
                '_WARNING': 20,
            }
        ]
        self.mongoconnection.shinken.macromodulations.insert(
            copy.deepcopy(self.modulations)
        )

    def test_get_all_macromodulations(self):
        response = self.get('/v2/config/macromodulations')

        self.assert_count_equal_backport(
            [
                {
                    'macromodulation_name': 'HighDuringNight',
                    'modulation_period': 'night',
                    'macros': {
                        '_CRITICAL': 20,
                        '_WARNING': 10}},
                {
                    'macromodulation_name': 'LowDuringNight',
                    'modulation_period': 'night',
                    'macros': {
                        '_CRITICAL': 10,
                        '_WARNING': 20}}
            ],
            json.loads(response.body.decode())

        )
        self.assertEqual(response.status_int, 200)

    def test_get_one_macromodulation(self):
        response = self.get('/v2/config/macromodulations/HighDuringNight')

        self.assertEqual(
            json.loads(response.body.decode()),
            {'macromodulation_name': 'HighDuringNight',
             'modulation_period': 'night',
             'macros': {
                 '_CRITICAL': 20,
                 '_WARNING': 10}}
        )

    def test_create_macromodulation(self):
        m = {
            'macromodulation_name': 'TEST_CREATE_MODULATION',
            'modulation_period': 'night',
            'macros': {
                '_CRITICAL': 10,
                '_WARNING': 20
            }
        }

        self.post_json('/v2/config/macromodulations', m)

        self.assertIsNotNone(
            self.mongoconnection.shinken.macromodulations.find_one(
                {
                    'macromodulation_name': 'TEST_CREATE_MODULATION',
                    '_CRITICAL': 10,
                    '_WARNING': 20
                }
            )
        )

    def test_delete_macromodulation(self):
        self.assertIsNotNone(
            self.mongoconnection.shinken.macromodulations.find_one(
                {"macromodulation_name": 'HighDuringNight'}
            )
        )

        self.delete('/v2/config/macromodulations/HighDuringNight')

        self.assertIsNone(
            self.mongoconnection.shinken.macromodulations.find_one(
                {"macromodulation_name": 'HighDuringNight'}
            )
        )

    def test_put_macromodulation(self):
        self.assertEqual(
            self.mongoconnection.shinken.macromodulations.find_one(
                {'macromodulation_name': 'HighDuringNight'}
            )['modulation_period'],
            'night'
        )

        self.put_json(
            '/v2/config/macromodulations/HighDuringNight',
            {"macromodulation_name": "HighDuringNight",
             "modulation_period": "TESTUPDATE"}
        )

        self.assertEqual(
            self.mongoconnection.shinken.macromodulations.find_one(
                {'macromodulation_name': 'HighDuringNight'}
            )['modulation_period'],
            'TESTUPDATE'
        )
