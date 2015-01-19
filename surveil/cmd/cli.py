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

"""Script to query OpenStack and optionally configure its linked Shinken with discovered elements/devices from Openstack."""

import os
import sys
import argparse
from argparse import RawTextHelpFormatter

#
from pprint import pprint


from keystoneclient.v2_0 import Client
from keystoneclient import session

from novaclient.v1_1 import Client as NovaClient


#############################################################################

parser = argparse.ArgumentParser(
    epilog=__doc__,
    formatter_class=RawTextHelpFormatter,
    # TODO
)

auth_group_help = '''\
The Openstack authentification values to use.
One can use the explicit CLI arguments or also use environments variables.
The environments variable names to use are the same as the CLI arguments, but in upper case and with '_' instead of '-'.
Example:
\t$ export OS_AUTH_URL=http://198.72.123.64:5000/v2.0 survey-cli ..
NB: The CLI arguments take precedence over the environments variables.
'''

auth_group = parser.add_argument_group('OS_AUTH', description=auth_group_help)

add = auth_group.add_argument
add('-U', '--os-username', help="The Openstack USERNAME to use for querying.")
add('-P', '--os-password', help="The Openstack PASSWORD to use for querying.")
add('-u', '--os-auth-url', help="The Openstack AUTH_URL to use for querying.")
add('-t', '--os-tenant-name', help="The Openstack TENANT_NAME to use for querying.")
add('-r', '--os-region-name', help="The Openstack REGION_NAME to use.")


OS_AUTH_PARAMS = tuple(
    act.dest
    for act in auth_group._actions[1:]  # skip the first one which is the group help.
)

#############################################################################

def parse_args(args=None):

    cfg = parser.parse_args(args)

    for param in OS_AUTH_PARAMS:
        value = getattr(cfg, param, None)
        if value is None:
            setattr(cfg, param, os.environ.get(param.upper()))

    return cfg


def main(args=None):

    cfg = parse_args(args)

    # Make the inventory of the OpenStack install
    keystone = Client(
        username=cfg.os_username,
        tenant_name=cfg.os_tenant_name,
        password=cfg.os_password,
        auth_url=cfg.os_auth_url,
    )

    endpoints = keystone.service_catalog.get_endpoints()
    pprint(endpoints)

    sess = session.Session(auth=keystone)


    # for now unused :

    # Compute
    if 'compute' in endpoints:
        nova_urls = [endpoint['publicURL']
                      for endpoint in endpoints['compute']]

    # Image
    if 'image' in endpoints:
        image_urls = [endpoint['publicURL']
                      for endpoint in endpoints['image']]

    # volume
    if 'volume' in endpoints:
        volume_urls = [endpoint['publicURL']
                       for endpoint in endpoints['volume']]

    # identity
    if 'identity' in endpoints:
        identity_urls = [endpoint['publicURL']
                         for endpoint in endpoints['identity']]


    nova_cli = NovaClient(
        username=cfg.os_username,
        api_key=cfg.os_password,
        project_id=cfg.os_tenant_name,
        auth_url=cfg.os_auth_url,

    )
    nova_cli.authenticate()
    # TODO:
    for what in (
        'services', 'flavors', 'hypervisors', 'images',
    ):
        print(getattr(nova_cli, what).list())




if __name__ == '__main__':
    sys.exit(main())
