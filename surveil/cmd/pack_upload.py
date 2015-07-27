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

"""Script to push a Shinken pack to Surveil"""

import argparse
import sys

import surveilclient.client as sc

from surveil.cmd import surveil_from_nagios


def main():
    # Parse the arguments
    parser = argparse.ArgumentParser(
        prog='surveil-pack-upload',
        add_help=False,
    )
    parser.add_argument('--surveil_api_url',
                        default='http://localhost:5311/v2',
                        type=str)
    parser.add_argument('--surveil_auth_url',
                        default='http://localhost:5311/v2/auth',
                        type=str)
    parser.add_argument('--surveil_api_version',
                        default='2_0',
                        type=str)
    parser.add_argument('pack',
                        metavar='[Pack]',
                        type=str,
                        nargs=1,
                        help='Pack directory')

    (options, args) = parser.parse_known_args(sys.argv[1:])

    cli_surveil = sc.Client(options.surveil_api_url,
                            auth_url=options.surveil_auth_url,
                            version=options.surveil_api_version)

    upload_pack(options.pack[0], cli_surveil)


def upload_pack(pack_dir, client):
    # pack_name = os.path.basename(os.path.normpath(pack_dir))

    surveil_config = surveil_from_nagios.load_config(pack_dir)

    config_manager = client.config
    for object_type, objects in surveil_config:
        object_manager = getattr(config_manager, object_type)
        for object in objects:
            object_manager.create(**object)
