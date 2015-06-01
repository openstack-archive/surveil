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
import time
import unittest

from surveil.tests import base

from compose.cli import docker_client
from compose import config as compose_config
from compose import project as compose_project
from surveilclient import client as sclient


@unittest.skipIf(os.environ.get('SURVEIL_INTEGRATION_TESTS', None) != 'True',
                 'Skipping integraiton tests')
class MergedIntegrationTest(base.BaseTestCase):

    @classmethod
    def setUpClass(cls):
        surveil_dir = os.path.realpath(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                "../../../")
        )

        compose_file = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            'integration.yml'
        )

        project_config = compose_config.from_dictionary(
            compose_config.load_yaml(compose_file),
            working_dir=surveil_dir,
            filename=compose_file
        )

        cls.project = compose_project.Project.from_dicts(
            "surveilintegrationtest",
            project_config,
            docker_client.docker_client()
        )
        cls.project.kill()
        cls.project.remove_stopped()
        cls.project.build()
        cls.project.up()

        cls.client = sclient.Client(
            'http://localhost:8999/v2',
            auth_url='http://localhost:8999/v2/auth',
            version='2_0'
        )

        #  Wait until Surveil is available
        now = time.time()
        while True:
            print("Waiting for surveil... %s" % int(time.time() - now))
            if time.time() < (now + 180):
                try:
                    #  If 'ws-arbiter' is found, Surveil is ready!
                    configured_hosts = cls.client.status.hosts.list()
                    host_found = False
                    for host in configured_hosts:
                        if host['host_name'].decode() == 'ws-arbiter':
                            host_found = True
                            break
                    if host_found:
                        break

                except Exception:
                    pass
                time.sleep(10)
            else:
                raise Exception("Surveil could not start")

    @classmethod
    def tearDownClass(cls):
        cls.project.kill()
        cls.project.remove_stopped()


class SeparatedIntegrationTests(MergedIntegrationTest):

    def setUp(self):
        SeparatedIntegrationTests.setUpClass()

    def tearDown(self):
        SeparatedIntegrationTests.tearDownClass()
