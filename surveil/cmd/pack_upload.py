# Copyright 2014 - Savoir-Faire Linux inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see `<http://www.gnu.org/licenses/>`.

"""Script to push a Shinken pack to Surveil"""

import argparse
import os
import sys

from surveil.cmd import surveil_from_nagios

from pymongo import mongo_client


def main():
    # Parse the arguments
    parser = argparse.ArgumentParser(
        prog='surveil-pack-upload',
        add_help=False,
    )
    parser.add_argument('--mongo-uri',
                        default='mongodb://localhost:27017',
                        help='Defaults to localhost', type=str)
    parser.add_argument('pack', metavar='[Pack]', type=str, nargs=1,
                        help='Pack directory')

    (options, args) = parser.parse_known_args(sys.argv[1:])

    pack_dir = options.pack[0]
    pack_name = os.path.basename(os.path.normpath(pack_dir))

    surveil_config = surveil_from_nagios.load_config(pack_dir)
    surveil_config = tag_configuration(surveil_config, pack_name)

    # Remove the existing pack from mongodb
    mongo = mongo_client.MongoClient(options.mongo_uri)
    mongo_shinken = mongo.shinken
    for collection in (
            [c for c
             in mongo_shinken.collection_names()
             if not c.startswith("system.")]
    ):
        mongo_shinken[collection].remove({'SURVEIL_PACK_NAME': pack_name})

    # Add the replacement pack
    for config_type in surveil_config:
            mongo_shinken[config_type].insert(
                surveil_config[config_type]
            )


def tag_configuration(config, pack_name):
    for collection in config.values():
        for object in collection:
            object['SURVEIL_PACK_NAME'] = pack_name
    return config

