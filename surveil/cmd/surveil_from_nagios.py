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

from __future__ import print_function

import argparse
import collections
import fnmatch
import json
import os
import re
import sys

import six
import wsme

from surveil.api.datamodel.config import businessimpactmodulation
from surveil.api.datamodel.config import checkmodulation
from surveil.api.datamodel.config import command
from surveil.api.datamodel.config import contact
from surveil.api.datamodel.config import contactgroup
from surveil.api.datamodel.config import host
from surveil.api.datamodel.config import hostgroup
from surveil.api.datamodel.config import macromodulation
from surveil.api.datamodel.config import notificationway
from surveil.api.datamodel.config import realm
from surveil.api.datamodel.config import service
from surveil.api.datamodel.config import servicegroup
from surveil.api.datamodel.config import timeperiod


def main():
    # Parse the arguments
    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument(
        'path',
        metavar='[path]',
        type=str,
        nargs=1,
        help='Configuration path'
    )

    (options, args) = parser.parse_known_args(sys.argv[1:])

    pack_dir = options.path[0]

    surveil_config = load_config(pack_dir)

    print(json.dumps(surveil_config, indent=4, sort_keys=True))


def load_config(path):
    """From a directory, returns Surveil configuration"""

    if os.path.isdir(path):
        # Find the .cfg files
        cfg_files = [
            os.path.join(dirpath, f)
            for dirpath, dirnames, files in os.walk(path)
            for f in fnmatch.filter(files, '*.cfg')
        ]
    else:
        cfg_files = [path]

    nagios_config = collections.OrderedDict()

    for cfg_file in sorted(cfg_files):
        # Open the file
        f = open(cfg_file, 'r')
        config_string = f.read()
        f.close()

        # Load the config
        file_config = _load_nagios_config(config_string)

        # Append to the loaded config
        for object_type, objects in file_config.items():
            nagios_config[object_type] = nagios_config.get(
                object_type,
                []
            ) + objects

    surveil_config = _transform_config(nagios_config)

    sorted_surveil_config = _sort_config(surveil_config)

    return sorted_surveil_config


def _load_nagios_config(config_string):
    """Given a nagios configuration string, returns a python dict"""
    config = collections.OrderedDict()

    # Find all config objects
    config_objects = re.finditer(
        r'define\s(?P<object_type>\w*)\s*{(?P<object_properties>[^{}]*)}',
        config_string
    )

    # For each object in the file...
    for object_match in config_objects:
        object_type = object_match.group("object_type")

        config_object = {}

        # For each property of the object...
        for property_match in re.finditer(
                r'(?P<property>[^\s]+)\s*(?P<value>.*?)\s*\n',
                object_match.group("object_properties")
        ):

            config_object[
                property_match.group('property')
            ] = property_match.group('value')

        # Append the config object
        config[object_type + 's'] = config.get(
            object_type + 's', []
        ) + [config_object]

    return config


def _transform_config(nagios_config):
    """Given a nagios config dict, returns surveil configuration"""
    transformed_config = collections.OrderedDict()

    for object_type, objects in nagios_config.items():
        for config_object in objects:

            # PROPERTY NAMES TRANSFORMATIONS
            name_transformed_obj = _transform_property_names(
                config_object,
                object_type
            )

            # PROPERTY TYPES TRANSORMATIONS
            type_transformed_obj = _transform_property_types(
                name_transformed_obj,
                object_type
            )

            transformed_config[object_type] = transformed_config.get(
                object_type,
                []
            ) + [type_transformed_obj]

    return transformed_config


def _transform_property_types(config_object, object_type):
    transformed_object = collections.OrderedDict()

    datamodels = {
        "businessimpactmodulations": businessimpactmodulation.BusinessImpactModulation,
        "checkmodulations": checkmodulation.CheckModulation,
        "commands": command.Command,
        "contacts": contact.Contact,
        "contactgroups": contactgroup.ContactGroup,
        "hosts": host.Host,
        "hostgroups": hostgroup.HostGroup,
        "macromodulations": macromodulation.MacroModulation,
        "notificationways": notificationway.NotificationWay,
        "realms": realm.Realm,
        "services": service.Service,
        "servicegroups": servicegroup.ServiceGroup,
        "timeperiods": timeperiod.TimePeriod,
    }
    object_datamodel = datamodels[object_type]
    object_wsmeattrs = object_datamodel._wsme_attributes
    for attribute in object_wsmeattrs:

        if attribute.name in config_object:
            # COMMA-SEPARATED => List
            if isinstance(attribute._get_datatype(), wsme.types.ArrayType):
                transformed_object[attribute.name] = config_object[attribute.name].split(',')
            # Integers
            elif attribute._get_datatype() in six.integer_types:
                transformed_object[attribute.name] = int(config_object[attribute.name])
            # Strings
            else:
                transformed_object[attribute.name] = config_object[attribute.name]

    return transformed_object


def _transform_property_names(config_object, object_type):
    transformed_object = collections.OrderedDict()

    # HOSTS
    if object_type in ['hosts', 'services']:
        transformed_object['custom_fields'] = {}
        for property, value in config_object.items():
            if property.startswith('_'):
                transformed_object['custom_fields'][property] = value
            else:
                transformed_object[property] = value
    # TIMEPERIODS
    elif object_type == 'timeperiods':
        transformed_object['periods'] = {}
        properties = [p.name for p in timeperiod.TimePeriod._wsme_attributes]
        for property, value in config_object.items():
            if property not in properties:
                transformed_object['periods'][property] = value
            else:
                transformed_object[property] = value
    # OTHER OBJECTS
    else:
        for property, value in config_object.items():
            transformed_object[property] = value
    return transformed_object


def _sort_config(surveil_config):

    # Sort object types
    correct_order = {
        "realms": 0,
        "timeperiods": 1,
        "macromodulations": 2,
        "commands": 3,
        "checkmodulations": 4,
        "businessimpactmodulations": 5,
        "notificationways": 6,
        "contacts": 7,
        "contactgroups": 8,
        "hosts": 9,
        "services": 10,
        "hostgroups": 11,
        "servicegroups": 12,
    }
    sorted_object_types = sorted(surveil_config.items(),
                                 key=lambda x: correct_order.get(x[0], 99))

    sorted_config = []

    # Sort objects
    for item in sorted_object_types:
        object_type = item[0]
        objects = item[1]

        if object_type in ['hosts', 'services']:
            objects = _sort_objects(objects)

        sorted_config.append((object_type, objects))

    return sorted_config


def _sort_objects(objects):
    sorted_objects = []
    while len(objects) > 0:
        for object in objects:
            host_dependencies = object.get('use', [])
            unsolved_dependencies = [
                d for d in host_dependencies
                if not any(o.get('name', None) == d
                           for o in sorted_objects)
            ]

            if len(unsolved_dependencies) == 0:
                break

        sorted_objects.append(object)
        objects.remove(object)

    return sorted_objects


if __name__ == "__main__":
    main()
