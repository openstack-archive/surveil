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
import sys

import influxdb
import pecan
from pecan import configuration
import pymongo
from six.moves import configparser
import surveilclient.client as sc

from surveil.cmd import pack_upload


def main():
    parser = optparse.OptionParser()
    parser.add_option('-d', '--demo',
                      default=False,
                      dest='demo',
                      help="Create fake hosts in Alignak",
                      action="store_true")
    parser.add_option('-i', '--influxdb',
                      default=False,
                      dest='influxdb',
                      help="Pre-create the InfluxDB database",
                      action='store_true')
    parser.add_option('-m', '--mongodb',
                      default=False,
                      dest='mongodb',
                      help="Drop the existing Alignak MongoDB database",
                      action='store_true')
    parser.add_option('-p', '--packs',
                      default=False,
                      dest='packs',
                      help="Upload/Update configuration packs to MongoDB",
                      action='store_true')
    parser.add_option('--pecan_config', '-P',
                      default='/etc/surveil/config.py',
                      dest='pecan_config',
                      help='Pecan config file (config.py)')
    parser.add_option('--config_file', '-c',
                      default='/etc/surveil/surveil.cfg',
                      dest='config_file',
                      help='Pecan config file (surveil.cfg)')

    opts, _ = parser.parse_args(sys.argv)

    surveil_api_url = 'http://localhost:5311/v2'
    surveil_auth_url = 'http://localhost:5311/v2/auth'
    surveil_api_version = '2_0'

    config = configparser.ConfigParser()
    config.read(opts.config_file)
    surveil_cfg = {"surveil_api_config":
                   dict([i for i in config.items("surveil")])}
    configuration.set_config(surveil_cfg, overwrite=True)
    configuration.set_config(opts.pecan_config, overwrite=False)

    cli_surveil = sc.Client(surveil_api_url,
                            auth_url=surveil_auth_url,
                            version=surveil_api_version)

    # Create a basic config in mongodb
    mongo = pymongo.MongoClient(pecan.conf.surveil_api_config['mongodb_uri'])

    if opts.mongodb is True:
        # Drop the current shinken config
        print("Dropping existing Alignak MongoDB database...")
        mongo.drop_database('shinken')

    if opts.influxdb is True:
        print("Pre-creating InfluxDB database...")
        # Create the InfluxDB database
        influx_client = influxdb.InfluxDBClient.from_DSN(
            pecan.conf.surveil_api_config['influxdb_uri']
        )

        databases = influx_client.get_list_database()
        if not any(db['name'] == influx_client._database for db in databases):
            influx_client.create_database(influx_client._database)

    if opts.packs:
        print ("Uploading packs...")
        # Load the shinken packs
        pack_upload.upload_pack(
            "/usr/share/monitoring/packs/sfl/openstack-keystone-http/",
            cli_surveil
        )

        pack_upload.upload_pack(
            "/usr/share/monitoring/packs/sfl/openstack-glance-http/",
            cli_surveil
        )
        pack_upload.upload_pack(
            "/usr/share/monitoring/packs/sfl/generic-host/",
            cli_surveil
        )
        pack_upload.upload_pack(
            "/usr/share/monitoring/packs/sfl/linux-system-nrpe/",
            cli_surveil
        )
        pack_upload.upload_pack(
            "/usr/share/monitoring/packs/sfl/openstack-nova-http/",
            cli_surveil
        )
        pack_upload.upload_pack(
            "/usr/share/monitoring/packs/sfl/openstack-cinder-http/",
            cli_surveil
        )
        pack_upload.upload_pack(
            "/usr/share/monitoring/packs/sfl/openstack-host/",
            cli_surveil
        )

    # if --demo is specified, you get more hosts.
    if opts.demo is True:
        print("Creating demo configuration...")
        # shinken's ws-arbiter
        cli_surveil.config.hosts.create(
            use=["generic-host"],
            contact_groups=["admins"],
            host_name="ws-arbiter",
            address="localhost"
        )
        cli_surveil.config.services.create(
            check_command="check_tcp!7760",
            check_interval="5",
            check_period="24x7",
            contact_groups=["admins"],
            contacts=["admin"],
            host_name=["ws-arbiter"],
            max_check_attempts="5",
            notification_interval="30",
            notification_period="24x7",
            retry_interval="3",
            service_description="check-ws-arbiter"
        )

        # Passive checks host
        cli_surveil.config.hosts.create(
            host_name='passive_check_host',
            use=['generic-host'],
            address='127.0.0.1',
            passive_checks_enabled='1'
        )

        # Linux-keystone template
        cli_surveil.config.hosts.create(
            host_name='test_keystone',
            use=['openstack-keystone-http'],
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

        # openstack-host template
        cli_surveil.config.hosts.create(
            host_name='openstackceilometer-host',
            use=['openstack-host'],
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
            use=['linux-system-nrpe'],
            address='srv-apache-01',
            custom_fields={
                "_TRAFFICLIMIT": "100000",
            }
        )

        # DOWN, and parent down (Network outage)
        cli_surveil.config.hosts.create(
            host_name='myparentisdown',
            address='dfgsdgsdgf',
            parents=['srv-apache-01'],
        )

        # UP host, no template
        cli_surveil.config.hosts.create(
            host_name='google.com',
            address='google.com'
        )

        # NRPE host, UP
        cli_surveil.config.hosts.create(
            host_name='srv-monitoring-01',
            use=['linux-system-nrpe'],
            address='127.0.0.1',
            custom_fields={
                "_TRAFFICLIMIT": "500000",
            }
        )

        # Has parent, UP
        cli_surveil.config.hosts.create(
            host_name='sw-iwebcore-01',
            parents=['srv-monitoring-01'],
            use=['generic-host'],
            address='127.0.0.1',
            custom_fields={
                "_TRAFFICLIMIT": "200000",
            }
        )

        # Has chain of 2 parents, UP
        cli_surveil.config.hosts.create(
            host_name='srv-ldap-01',
            parents=['sw-iwebcore-01'],
            use=['generic-host'],
            address='127.0.0.1',
            custom_fields={
                "_TRAFFICLIMIT": "5000000",
            }
        )

        # UP host with down service
        cli_surveil.config.hosts.create(
            use=["generic-host"],
            contact_groups=["admins"],
            host_name="myserviceisdown",
            address="localhost"
        )
        cli_surveil.config.services.create(
            check_command="check_tcp!4553",
            check_interval="5",
            check_period="24x7",
            contact_groups=["admins"],
            contacts=["admin"],
            host_name=["myserviceisdown"],
            max_check_attempts="5",
            notification_interval="30",
            notification_period="24x7",
            retry_interval="3",
            service_description="iamadownservice"
        )

    # Reload the shinken config
    cli_surveil.config.reload_config()

if __name__ == "__main__":
    main()
