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

"""Script to initialize Surveil dependencies."""

import os
# from keystoneclient.v2_0 import client as keystone_client
# from keystoneclient import session
# from novaclient.v1_1 import client as nova_client

from surveil.api import config


def main():
    # Create a basic config in mongodb
    mongo = config.app_hooks[0].mongo_connection

    # Drop the current shinken config
    mongo.drop_database('shinken')

    mongo_shinken = mongo.shinken
    mongo_hosts = mongo_shinken.hosts
    mongo_services = mongo_shinken.services

    mongo_hosts.insert(
        {"use": "generic-host", "contact_groups": "admins",
         "host_name": "surveil", "address": "localhost"}
    )

    mongo_services.insert(
        {"check_command": "check_tcp!8080", "check_interval": "5",
         "check_period": "24x7", "contact_groups": "admins",
         "contacts": "admin", "host_name": "surveil",
         "max_check_attempts": "5", "notification_interval": "30",
         "notification_period": "24x7", "retry_interval": "3",
         "service_description": "check-surveil-api"}
    )

'''
    # Make the inventory of the OpenStack install
    keystone = keystone_client.Client(
        username=os.environ['OS_USERNAME'],
        tenant_name=os.environ['OS_TENANT_NAME'],
        password=os.environ['OS_PASSWORD'],
        auth_url=os.environ['OS_AUTH_URL'],
    )
    endpoints = keystone.service_catalog.get_endpoints()
    sess = session.Session(auth=keystone)

    # Compute
    if 'compute' in endpoints.keys():
        nova_urls = [endpoint['publicURL'] for endpoint in endpoints['compute']]
        # TODO: add compute hosts to surveil

    # Image
    if 'image' in endpoints.keys():
        image_urls = [endpoint['publicURL'] for endpoint in endpoints['image']]
        # TODO: add image hosts to surveil

    # volume
    if 'volume' in endpoints.keys():
        volume_urls = [endpoint['publicURL'] for endpoint in endpoints['volume']]
        # TODO: add image hosts to surveil

    # identity
    if 'identity' in endpoints.keys():
        identity_urls = [endpoint['publicURL'] for endpoint in endpoints['identity']]
        # TODO: add identity hosts to surveil

'''
