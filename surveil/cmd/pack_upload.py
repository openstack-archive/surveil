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
import fnmatch
import os
import sys

from pymongo import mongo_client
from alignak.objects import config


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
    pack_sub_dir = os.path.join(pack_dir, 'pack')
    pack_name = os.path.basename(os.path.normpath(pack_dir))

    # Find the .cfg files
    cfg_files = [
        os.path.join(dirpath, f)
        for dirpath, dirnames, files in os.walk(pack_sub_dir)
        for f in fnmatch.filter(files, '*.cfg')
    ]

    # Load the config
    conf = config.Config()
    loaded_conf = conf.read_config(cfg_files)
    raw_objects = conf.read_config_buf(loaded_conf)

    # Remove the empty items
    non_empty_config = {k: v for k, v in raw_objects.items() if v}

    for config_type in non_empty_config:
        for config_item in non_empty_config[config_type]:
            # Tag the config objects
            config_item['SURVEIL_PACK_NAME'] = pack_name

            # Replace lists with csv
            items_to_modify = (
                [i for i in config_item.items() if isinstance(i[1], list)]
            )
            for i in items_to_modify:
                config_item[i[0]] = ','.join(i[1])

    # Remove the existing pack from mongodb
    mongo = mongo_client.MongoClient(options.mongo_uri)
    mongo_shinken = mongo.shinken
    for collection in (
            mongo_shinken.collection_names(include_system_collections=False)
    ):
        mongo_shinken[collection].remove({'SURVEIL_PACK_NAME': pack_name})

    # Add the replacement pack
    for config_type in non_empty_config:
            mongo_shinken[config_type + 's'].insert(
                non_empty_config[config_type]
            )
