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

import os
import time
import unittest

from surveil.tests import base

from compose.cli import docker_client
from compose import config as compose_config
from compose import project as compose_project
import requests


@unittest.skipIf(os.environ.get('SURVEIL_INTEGRATION_TESTS', None) != 'True',
                 'Skipping integraiton tests')
class IntegrationTest(base.BaseTestCase):

    def setUp(self):
        surveil_dir = os.path.realpath(os.path.join(os.getcwd() + "/../../../"))
        compose_file = os.path.join(surveil_dir, 'docker-compose.yml')
        project_config = compose_config.load(compose_file)

        self.project = compose_project.Project.from_dicts(
            "surveilintegrationtest",
            project_config,
            docker_client.docker_client()
        )
        self.project.kill()
        self.project.up()

        #  Wait until Surveil is available
        now = time.time()
        while True:
            if time.time() < (now + 180):
                try:
                    resp = requests.get("http://localhost:8080/v2/hello")
                    break
                except Exception:
                    pass
                time.sleep(1)
            else:
                raise Exception("Surveil could not start")

    def tearDown(self):
        self.project.kill()

    def test_hello(self):
        self.assertEqual(
            requests.get("http://localhost:8080/v2/hello").text,
            'Hello World!'
        )
