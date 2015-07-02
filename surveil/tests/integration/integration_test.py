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

from __future__ import print_function

import os
import unittest

from surveil.tests import base
from surveil.tests.integration.backend import docker


@unittest.skipIf(os.environ.get('SURVEIL_INTEGRATION_TESTS', None) != 'True',
                 'Skipping integraiton tests')
class MergedIntegrationTest(base.BaseTestCase):

    @classmethod
    def setUpClass(cls):
        test_backend = os.environ.get(
            'SURVEIL_INTEGRATION_TESTS_BACKEND',
            None
        )

        if test_backend == 'DOCKER':
            MergedIntegrationTest.backend = docker.DockerBackend()
        else:
            raise Exception(
                "Could not identify tests backend: '%s'" % test_backend
            )
        cls.backend.setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.backend.tearDownClass()

    def get_surveil_client(self):
        return MergedIntegrationTest.backend.get_surveil_client()


class SeparatedIntegrationTests(MergedIntegrationTest):

    def setUp(self):
        SeparatedIntegrationTests.setUpClass()

    def tearDown(self):
        SeparatedIntegrationTests.tearDownClass()
