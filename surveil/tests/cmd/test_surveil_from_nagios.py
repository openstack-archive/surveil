# Copyright 2014 - Savoir-Faire Linux inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import os

from surveil.cmd import surveil_from_nagios
from surveil.tests import base as base_test


class TestSurveilFromNagios(base_test.BaseTestCase):

    def setUp(self):
        self.nagios_config_folder = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'nagios_config'
        )

    def test_surveil_from_nagios_config_cfg(self):
        surveil_cfg = surveil_from_nagios.load_config(
            self.nagios_config_folder
        )

        self.assert_count_equal_backport(
            surveil_cfg,
            [
                ('timeperiods',
                 [
                     {
                         'alias': 'Normal Work Hours',
                         'timeperiod_name': 'workhours',
                         'periods': {
                             'tuesday': '09:00-17:00',
                             'friday': '09:00-17:00',
                             'thursday': '09:00-17:00',
                             'wednesday': '09:00-17:00',
                             'monday': '09:00-17:00'
                         }
                     }
                 ]),
                ('hosts',
                 [
                     {
                         'name': 'generic-host',
                         'custom_fields': {}},
                     {
                         'use': ['generic-host'],
                         'custom_fields': {}},
                     {
                         'use': ['generic-host', 'non-existing-thing'],
                         'contact_groups': ['admins'],
                         'host_name': 'localhost',
                         'check_interval': 324,
                         'address': 'localhost',
                         'custom_fields': {
                             '_custom_yolo': 'sdfsdf'
                         }
                     },

                 ]),
                ('services',
                 [
                     {'host_name': ['test']},
                     {'host_name': ['hai']}
                 ])
            ]
        )

    def test_load_single_file(self):
        other_file_path = os.path.join(
            self.nagios_config_folder,
            'other_file.cfg'
        )

        single_file_config = surveil_from_nagios.load_config(
            other_file_path
        )

        self.assertEqual(
            single_file_config,
            [('services', [{'host_name': ['hai']}])]
        )