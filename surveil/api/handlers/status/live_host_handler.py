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

import json

from surveil.api.datamodel.status import live_host
from surveil.api.handlers import handler
from surveil.api.handlers.status import mongodb_query

import wsme


class HostHandler(handler.Handler):
    """Fulfills a request on the live hosts."""

    def get(self, host_name):
        """Return a host."""
        mongo_s = self.request.mongo_connection.alignak_live.hosts.find_one(
            {"host_name": host_name}
        )

        return live_host.LiveHost(**_host_dict_from_mongo_item(mongo_s))

    def get_all(self, live_query=None):
        """Return all live hosts."""

        if live_query:
            lq_filters, lq_fields = _translate_live_query(live_query)
        else:
            lq_filters = {}
            lq_fields = {}

        query, fields = mongodb_query.build_mongodb_query(lq_filters,
                                                          lq_fields)

        if fields != {}:
            mongo_dicts = (self.request.mongo_connection.
                           alignak_live.hosts.find(query, fields))
        else:
            mongo_dicts = (self.request.mongo_connection.
                           alignak_live.hosts.find(query))

        host_dicts = [
            _host_dict_from_mongo_item(s) for s in mongo_dicts
        ]

        hosts = []
        for host_dict in host_dicts:
            host = live_host.LiveHost(**host_dict)
            hosts.append(host)

        return hosts


def _translate_live_query(live_query):
    #  Mappings
    mapping = {
        "last_check": "last_chk",
        "description": "display_name",
        "plugin_output": "output",
        "acknowledged": "problem_has_been_acknowledged"
    }

    #  Load the fields
    if live_query.fields != wsme.Unset:
        fields = live_query.fields
    else:
        fields = []

    #  Translate the fields
    lq_fields = []
    for field in fields:
        lq_fields.append(mapping.get(field, field))

    #  Load the filters
    filters = json.loads(live_query.filters)

    #  Translate the filters
    for filter in filters.values():
        for field in filter.keys():
            value = filter.pop(field)
            filter[mapping.get(field, field)] = value

    return filters, lq_fields


def _host_dict_from_mongo_item(mongo_item):
    """Create a dict from a mongodb item."""

    mappings = [
        ('last_chk', 'last_check', int),
        ('last_state_change', 'last_state_change', int),
        ('output', 'plugin_output', str),
        ('problem_has_been_acknowledged', 'acknowledged', bool),
        ('state', 'state', str),
        ('display_name', 'description', str),
    ]

    for field in mappings:
        value = mongo_item.pop(field[0], None)
        if value is not None:
            mongo_item[field[1]] = field[2](value)

    return mongo_item
