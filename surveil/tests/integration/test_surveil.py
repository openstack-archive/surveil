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
        """Delete a host and asserts that is is not monitored by Alignak."""
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

    def test_update_host(self):
        """Update a host and asserts that is is monitored by Alignak."""
        self.test_create_host()

        self.get_surveil_client().config.hosts.update(
            host_name='integrationhosttest',
            host={'host_name': 'host_name_up',
                  'address': '127.0.1.1'}
        )

        self.get_surveil_client().config.reload_config()

        def function():
            status_host = (self.get_surveil_client().
                           config.hosts.get(host_name='host_name_up'))
            self.assertTrue(
                status_host['host_name'].decode() == 'host_name_up' and
                status_host['address'].decode() == '127.0.1.1' and
                status_host['use'].decode() == 'generic-host'
            )

        self.assertTrue(
            self.try_for_x_seconds(
                function,
                time_to_wait=180,
                cooldown=10,
                exception=AssertionError,
                message="Host is not updated."
            )
        )

    def test_passive_check(self):
        """Test  monitoring a host with passive checks."""
        self.test_create_host()

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
        """Test documentation tutorial monitoring with your custom plugins."""
        commands = [
            "mkdir /usr/lib/monitoring/plugins/custom/",
            "echo -e '#!/bin/bash\necho " +
            "DISK $1 OK - free space: / 3326 MB (56%);"
            " | /=2643MB;5948;5958;0;5968" +
            "' | sudo tee /usr/lib/monitoring/plugins/"
            "custom/check_example",
            'chmod +x /usr/lib/monitoring/plugins/custom/'
            'check_example'
        ]

        self.execute_command(commands, 'alignak')

        self.test_create_host()
        self.get_surveil_client().config.commands.create(
            command_name='check_integrationhosttest',
            command_line='$CUSTOMPLUGINSDIR$/check_example $HOSTADDRESS$'
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
            service_description="check_integrationhosttest"
        )

        self.get_surveil_client().config.reload_config()

        def function():
            status_services = self.get_surveil_client().status.services.list()
            self.assertFalse(
                any(service['host_name'].decode() == 'integrationhosttest' and
                    service['service_description'].decode() ==
                    'check_integrationhosttest' and
                    service['plugin_output'].decode() ==
                    "DISK 127.0.1.1 OK - free space: / 3326 MB (56%);"
                    "| /=2643MB;5948;5958;0;5968"
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

    def test_list_metrics_name_host(self):
        """Test if a host with use=generic-host have the good metrics name."""
        self.test_create_host()

        def function():
            metrics_name_hosts = (
                self.get_surveil_client().status.hosts.metrics.get(
                    host_name='integrationhosttest')
            )
            self.assertTrue(
                any(metric_name['metric_name'].decode() == 'rtmin'
                    for metric_name in metrics_name_hosts)
            )

        self.assertTrue(
            self.try_for_x_seconds(
                function,
                time_to_wait=360,
                cooldown=10,
                exception=AssertionError,
                message="No metric name for host created"
            )
        )