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
import fnmatch
import os
import sys

from pymongo import mongo_client
from shinken.objects import config


def main():
    # Parse the arguments
    parser = argparse.ArgumentParser(
        prog='surveil-pack-upload',
        add_help=False,
    )
    parser.add_argument('--mongo-url',
                        default='localhost',
                        help='Defaults to localhost', type=str)
    parser.add_argument('--mongo-port',
                        default=27017,
                        help='Defaults to 27017', type=int)
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
    buff_conf = conf.read_config_buf(loaded_conf)

    # Remove the empty items
    non_empty_config = {k: v for k, v in buff_conf.items() if v}

    # Tag the config
    for config_type in non_empty_config:
        for config_item in non_empty_config[config_type]:
            config_item['SURVEIL_PACK_NAME'] = pack_name

    # Remove the existing pack from mongodb
    mongo = mongo_client.MongoClient(host=options.mongo_url, port=options.mongo_port)
    mongo_shinken = mongo.shinken
    for collection in \
            mongo_shinken.collection_names(include_system_collections=False):
        mongo_shinken[collection].remove({'SURVEIL_PACK_NAME': pack_name})

    # Add the replacement pack
    for config_type in non_empty_config:
            mongo_shinken[config_type + 's'].insert(
                non_empty_config[config_type]
            )

