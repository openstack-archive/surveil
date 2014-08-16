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

import pecan
import pecan.testing

import unittest

__all__ = ['FunctionalTest']


class FunctionalTest(unittest.TestCase):
    """Used for functional tests.

    Used where you need to test your literal
    application and its integration with the framework.
    """

    def setUp(self):
        self.app = pecan.testing.load_test_app({
            'app': {
                'root': 'surveil.api.controllers.root.RootController',
                'modules': ['surveil.api'],
                'debug': False
            }
        })

    def tearDown(self):
        pecan.set_config({}, overwrite=True)
