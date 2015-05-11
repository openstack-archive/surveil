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

from surveil.api.datamodel.status import live_service
from surveil.api.handlers import handler
from surveil.api.handlers.status import mongodb_query

import wsme


class ServiceHandler(handler.Handler):
    """Fulfills a request on live services."""

    def get(self, host_name, service_description):
        """Return a specific service."""
        mongo_s = self.request.mongo_connection.shinken_live.services.find_one(
            {"host_name": host_name,
             "service_description": service_description},
        )
        return live_service.LiveService(**mongo_s)

    def get_all(self, live_query=None):
        """Return all live services."""

        if live_query:
            lq_filters, lq_fields = _translate_live_query(live_query)
        else:
            lq_filters = {}
            lq_fields = {}

        query, fields = mongodb_query.build_mongodb_query(lq_filters,
                                                          lq_fields)

        if fields != {}:
            mongo_dicts = (self.request.mongo_connection.
                           shinken_live.services.find(query, fields))
        else:
            mongo_dicts = (self.request.mongo_connection.
                           shinken_live.services.find(query))

        service_dicts = [
            _service_dict_from_mongo_item(s) for s in mongo_dicts
        ]

        services = []
        for service_dict in service_dicts:
            service = live_service.LiveService(**service_dict)
            services.append(service)

        return services


def _translate_live_query(live_query):
    #  Mappings
    mapping = {
        "last_check": "last_chk",
        "description": "service_description",
        "output": "plugin_output",
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


def _service_dict_from_mongo_item(mongo_item):
    last_chk = mongo_item.pop('last_chk', None)
    if last_chk:
        mongo_item['last_check'] = int(last_chk)

    last_state_change = mongo_item.pop('last_state_change', None)
    if last_state_change:
        mongo_item['last_state_change'] = int(last_state_change)

    output = mongo_item.pop('output', None)
    if output:
        mongo_item['plugin_output'] = output

    return mongo_item
