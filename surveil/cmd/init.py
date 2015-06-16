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

"""Script to reinitialize surveil."""

import optparse
import subprocess
import sys

import pymongo
import surveilclient.client as sc

from surveil.api import config


def main():
    parser = optparse.OptionParser()
    parser.add_option('-d', '--demo',
                      default=False,
                      dest='demo',
                      action="store_true")
    opts, _ = parser.parse_args(sys.argv)

    # Create a basic config in mongodb
    mongo = pymongo.MongoClient(config.surveil_api_config['mongodb_uri'])

    if opts.demo is True:
        # Drop the current shinken config
        mongo.drop_database('shinken')

    if mongo.surveil.init.count() == 0:
        # Mark packs as uploaded
        print("Uploading packs...")
        mongo.surveil.init.insert({"source": "surveil-init script"})

        # Load the shinken packs
        subprocess.call(
            [
                "surveil-pack-upload",
                "--mongo-url=mongo",
                "--mongo-port=27017",
                "/usr/share/monitoring/packs/sfl/openstack-keystone/",
            ]
        )

        subprocess.call(
            [
                "surveil-pack-upload",
                "--mongo-url=mongo",
                "--mongo-port=27017",
                "/usr/share/monitoring/packs/sfl/openstack-glance/",
            ]
        )

        subprocess.call(
            [
                "surveil-pack-upload",
                "--mongo-url=mongo",
                "--mongo-port=27017",
                "/usr/share/monitoring/packs/sfl/generic-host/",
            ]
        )

        subprocess.call(
            [
                "surveil-pack-upload",
                "--mongo-url=mongo",
                "--mongo-port=27017",
                "/usr/share/monitoring/packs/sfl/openstack-nova/",
            ]
        )

        subprocess.call(
            [
                "surveil-pack-upload",
                "--mongo-url=mongo",
                "--mongo-port=27017",
                "/usr/share/monitoring/packs/sfl/openstack-cinder/",
            ]
        )

        subprocess.call(
            [
                "surveil-pack-upload",
                "--mongo-url=mongo",
                "--mongo-port=27017",
                "/usr/share/monitoring/packs/sfl/openstack-host/",
            ]
        )

    else:
        print("Skipping pack upload...")

    cli_surveil = sc.Client('http://localhost:8080/v2',
                            auth_url='http://localhost:8080/v2/auth',
                            version='2_0')

    # if --demo is specified, you get more hosts.
    if opts.demo is True:

        # shinken's ws-arbiter
        cli_surveil.config.hosts.create(
            use="generic-host",
            contact_groups="admins",
            host_name="ws-arbiter",
            address="localhost"
        )
        cli_surveil.config.services.create(
            check_command="check_tcp!7760",
            check_interval="5",
            check_period="24x7",
            contact_groups="admins",
            contacts="admin",
            host_name="ws-arbiter",
            max_check_attempts="5",
            notification_interval="30",
            notification_period="24x7",
            retry_interval="3",
            service_description="check-ws-arbiter"
        )

        # Linux-keystone template
        cli_surveil.config.hosts.create(
            host_name='test_keystone',
            use='linux-keystone',
            address='127.0.0.1',
            custom_fields={
                "_OS_AUTH_URL": "bla",
                "_OS_USERNAME": "bli",
                "_OS_PASSWORD": "blo",
                "_OS_TENANT":   "blu",
                "_KS_SERVICES": "bly",
                "parents": "localhost"
            }
        )

        # Linux-openstackceilometer template
        cli_surveil.config.hosts.create(
            host_name='openstackceilometer-host',
            use='linux-openstackceilometer',
            address='127.0.0.1',
            custom_fields={
                "_OS_AUTH_URL": "bla",
                "_OS_USERNAME": "bli",
                "_OS_PASSWORD": "blo",
                "_OS_TENANT_NAME":   "blu",
                "_KS_SERVICES": "bly",
                "parents": "localhost"
            }
        )

        # DOWN HOST (cant resolve)
        cli_surveil.config.hosts.create(
            host_name='srv-apache-01',
            use='linux-system-nrpe',
            address='srv-apache-01',
            custom_fields={
                "_TRAFFICLIMIT": "100000",
            }
        )

        # DOWN, and parent down (Network outage)
        cli_surveil.config.hosts.create(
            host_name='myparentisdown',
            address='dfgsdgsdgf',
            parents='srv-apache-01',
        )

        # UP host, no template
        cli_surveil.config.hosts.create(
            host_name='google.com',
            address='google.com'
        )

        # NRPE host, UP
        cli_surveil.config.hosts.create(
            host_name='srv-monitoring-01',
            use='linux-system-nrpe',
            address='127.0.0.1',
            custom_fields={
                "_TRAFFICLIMIT": "500000",
            }
        )

        # Has parent, UP
        cli_surveil.config.hosts.create(
            host_name='sw-iwebcore-01',
            parents='srv-monitoring-01',
            use='generic-host',
            address='127.0.0.1',
            custom_fields={
                "_TRAFFICLIMIT": "200000",
            }
        )

        # Has chain of 2 parents, UP
        cli_surveil.config.hosts.create(
            host_name='srv-ldap-01',
            parents='sw-iwebcore-01',
            use='generic-host',
            address='127.0.0.1',
            custom_fields={
                "_TRAFFICLIMIT": "5000000",
            }
        )

        # UP host with down service
        cli_surveil.config.hosts.create(
            use="generic-host",
            contact_groups="admins",
            host_name="myserviceisdown",
            address="localhost"
        )
        cli_surveil.config.services.create(
            check_command="check_tcp!4553",
            check_interval="5",
            check_period="24x7",
            contact_groups="admins",
            contacts="admin",
            host_name="myserviceisdown",
            max_check_attempts="5",
            notification_interval="30",
            notification_period="24x7",
            retry_interval="3",
            service_description="iamadownservice"
        )

    # Reload the shinken config
    cli_surveil.config.reload_config()
