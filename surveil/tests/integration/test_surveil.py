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

import requests

from surveil.tests.integration import integration_test


class TestMergedIngegrationSurveil(
    integration_test.MergedIntegrationTest
):

    def test_hello(self):
        self.assertEqual(
            requests.get("http://localhost:8999/v2/hello").text,
            'Hello World!'
        )


class TestSeparatedIntegrationSurveil(
    integration_test.SeparatedIntegrationTests
):

    def test_create_host(self):
        """Creates a host and asserts that is is monitored by Alignak."""
        config_hosts = (TestSeparatedIntegrationSurveil.
                        client.status.hosts.list())

        self.assertFalse(
            any(host['host_name'] == 'integrationhosttest'
                for host in config_hosts)
        )

        TestSeparatedIntegrationSurveil.client.config.hosts.create(
            host_name='integrationhosttest',
            address='127.0.0.1',
        )

        TestSeparatedIntegrationSurveil.client.config.reload_config()

        def function():
            status_hosts = (TestSeparatedIntegrationSurveil.
                            client.status.hosts.list())
            self.assertTrue(
                any(host['host_name'].decode() == 'integrationhosttest'
                    for host in status_hosts)

            )

        self.assertTrue(
            self.try_for_x_seconds(
                function,
                time_to_wait=180,
                cooldown=10,
                exception=AssertionError,
                message="Could not find host in status."
            )
        )

    def test_delete_host(self):
        self.test_create_host()

        TestSeparatedIntegrationSurveil.client.config.hosts.delete(
            'integrationhosttest'
        )

        TestSeparatedIntegrationSurveil.client.config.reload_config()

        def function():
            status_hosts = (TestSeparatedIntegrationSurveil.
                            client.status.hosts.list())
            self.assertFalse(
                any(host['host_name'].decode() == 'integrationhosttest'
                    for host in status_hosts)
            )

        self.assertTrue(
            self.try_for_x_seconds(
                function,
                time_to_wait=180,
                cooldown=10,
                exception=AssertionError,
                message="Host was not deleted"
            )
        )
