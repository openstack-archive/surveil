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

"""Script to query OpenStack and optionally configure its linked Shinken
with discovered elements/devices from Openstack."""


import argparse
import os
import sys
import urlparse

import keystoneclient.v2_0 as kc
import surveilclient.client as sc


#############################################################################

parser = argparse.ArgumentParser(
    epilog=__doc__,
    formatter_class=argparse.RawTextHelpFormatter,
    # TODO(gst): continue..
)

auth_group_help = '''The Openstack authentification values to use.
One can use the explicit CLI arguments or also use environments variables.
The environment variable to use are the same as the CLI arguments, but
in upper case, without the leading '--' and with others '-' replaced by '_'.
Example:
\t$ export OS_AUTH_URL=http://198.72.123.64:5000/v2.0 survey-cli ..
NB: The CLI arguments take precedence over the environment variables.
'''

auth_group = parser.add_argument_group('OS_AUTH', description=auth_group_help)

add = auth_group.add_argument

add('-A', '--api-url',
    help="The Surveil API URL (http(s)://HOST(:PORT)/(URI)).")
add('-U', '--os-username', help="The Openstack USERNAME to use for querying.")
add('-P', '--os-password', help="The Openstack PASSWORD to use for querying.")
add('-u', '--os-auth-url', help="The Openstack AUTH_URL to use for querying.")
add('-t', '--os-tenant-name',
    help="The Openstack TENANT_NAME to use for querying.")
add('-r', '--os-region-name', help="The Openstack REGION_NAME to use.")


OS_AUTH_PARAMS = tuple(
    act.dest
    for act in auth_group._actions[1:]
    # skip the first one which is the group help itself.
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
    keystone = kc.Client(
        username=cfg.os_username,
        tenant_name=cfg.os_tenant_name,
        password=cfg.os_password,
        auth_url=cfg.os_auth_url,
    )

    endpoints = keystone.service_catalog.get_endpoints()

    cli_surveil = sc.Client(cfg.api_url, version='1_0')

    for ep in endpoints.get('identity', []):

        cli_surveil.hosts.create(
            host_name='OS_keystone_host_%s' % ep['id'],
            use='linux-keystone',
            address=urlparse.urlparse(ep['publicURL']).hostname,
            custom_fields={
                '_OS_AUTH_URL': ep['publicURL'],
                '_OS_USERNAME': cfg.os_username,
                '_OS_PASSWORD': cfg.os_password,
                '_OS_TENANT_NAME': cfg.os_tenant_name,
                '_KS_SERVICES': 'identity',
            }
        )

    for ep in endpoints.get('image', []):
        cli_surveil.hosts.create(
            host_name='OS_glance_host_%s' % ep['id'],
            use='linux-glance',
            address=urlparse.urlparse(ep['publicURL']).hostname,
            custom_fields={
                '_OS_AUTH_URL': ep['publicURL'],
                '_OS_USERNAME': cfg.os_username,
                '_OS_PASSWORD': cfg.os_password,
                '_OS_TENANT_NAME': cfg.os_tenant_name,
                '_OS_GLANCE_URL': ep['publicURL'] + '/v1',
            }
        )

    # Reload the surveil config
    cli_surveil.reload_config()

if __name__ == '__main__':
    sys.exit(main())
