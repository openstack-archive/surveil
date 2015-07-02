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
        config_hosts = self.get_surveil_client().status.hosts.list()

        self.assertFalse(
            any(host['host_name'] == 'integrationhosttest'
                for host in config_hosts)
        )

        self.get_surveil_client().config.hosts.create(
            host_name='integrationhosttest',
            address='127.0.0.1',
            use='generic-host',
        )

        self.get_surveil_client().config.reload_config()

        def function():
            status_hosts = self.get_surveil_client().status.hosts.list()
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

        self.get_surveil_client().config.hosts.delete(
            'integrationhosttest'
        )

        self.get_surveil_client().config.reload_config()

        def function():
            status_hosts = (self.get_surveil_client().status.hosts.list())
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

    def test_passive_check(self):
        self.get_surveil_client().config.hosts.create(
            host_name='integrationhosttest',
            address='127.0.0.1',
            use='generic-host',
        )
        self.get_surveil_client().config.commands.create(
            command_name='check_integrationhosttest',
            command_line='/usr/lib/monitoring/plugins/sfl/check_example'
        )
        self.get_surveil_client().config.services.create(
            check_command="check_integrationhosttest",
            check_interval="5",
            check_period="24x7",
            contact_groups="admins",
            contacts="admin",
            host_name="integrationhosttest",
            max_check_attempts="5",
            notification_interval="30",
            notification_period="24x7",
            retry_interval="3",
            service_description="check_integrationhosttest",
            passive_checks_enabled="1"
        )

        self.get_surveil_client().config.reload_config()
        self.get_surveil_client().status.services.submit_check_result(
            host_name='integrationhosttest',
            service_description='check_integrationhosttest',
            output="Hello",
            return_code=0
        )

        def function():
            status_services = self.get_surveil_client().status.services.list()
            self.assertFalse(
                any(service['host_name'].decode() == 'integrationhosttest' and
                    service['service_description'].decode() ==
                    'check_integrationhosttest' and
                    service['plugin_output'].decode() == 'Hello' and
                    service['state'].decode() == 'OK'
                    for service in status_services)
            )

        self.assertTrue(
            self.try_for_x_seconds(
                function,
                time_to_wait=180,
                cooldown=10,
                exception=AssertionError,
                message="submit check result fail"
            )
        )

    def test_custom_plugins(self):
        self.get_surveil_client().config.hosts.create(
            host_name='integrationhosttest',
            address='127.0.0.1',
            use='generic-host',
        )
        self.get_surveil_client().config.commands.create(
            command_name='check_integrationhosttest',
            command_line='/usr/lib/monitoring/plugins/sfl/check_example'
        )
        self.get_surveil_client().config.services.create(
            check_command="check_integrationhosttest",
            check_interval="5",
            check_period="24x7",
            contact_groups="admins",
            contacts="admin",
            host_name="integrationhosttest",
            max_check_attempts="5",
            notification_interval="30",
            notification_period="24x7",
            retry_interval="3",
            service_description="check_integrationhosttest",
            passive_checks_enabled="1"
        )

        self.get_surveil_client().config.reload_config()

        def function():
            status_services = self.get_surveil_client().status.services.list()
            self.assertFalse(
                any(service['host_name'].decode() == 'integrationhosttest' and
                    service['service_description'].decode() ==
                    'check_integrationhosttest' and
                    service['plugin_output'].decode() ==
                    "DISK OK - free space: / 3326 MB (56%);"
                    " | /=2643MB;5948;5958;0;5968"
                    for service in status_services)
            )

        self.assertTrue(
            self.try_for_x_seconds(
                function,
                time_to_wait=180,
                cooldown=10,
                exception=AssertionError,
                message="Custom Plugins is not used"
            )
        )