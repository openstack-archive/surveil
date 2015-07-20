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

from surveil.tests import base as base_test
from surveil.cmd import surveil_from_nagios


class TestSurveilFromNagios(base_test.BaseTestCase):

    def setUp(self):
        self.nagios_config_folder = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'nagios_config'
        )

    def test_surveil_from_nagios_config_cfg(self):
        f = open(os.path.join(self.nagios_config_folder, 'config.cfg'), 'r')
        config_string = f.read()
        f.close()

        nagios_cfg = surveil_from_nagios.load_config(config_string)
        surveil_cfg = surveil_from_nagios.transform_config(nagios_cfg)

        self.assertEqual(
            surveil_cfg,
            {
                'hosts': [
                    {
                        'contact_groups': [
                            'admins'
                        ],
                        'use': [
                            'generic-host'
                        ],
                        'host_name': 'localhost',
                        'check_interval': 324,
                        'address': 'localhost'}
                ],
                'services': [
                    {
                        'host_name': [
                        'test'
                        ]
                    }
                ],
                'timeperiods': [
                    {
                        'timeperiod_name': 'workhours',
                        'alias': 'Normal Work Hours'
                    }
                ]
            }
        )