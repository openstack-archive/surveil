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

from __future__ import print_function
import json

from surveil.api.datamodel.status import live_host
from surveil.api.handlers import handler
from surveil.api.handlers.status import fields_filter
from surveil.api.handlers.status import mongodb_query


class HostHandler(handler.Handler):
    """Fulfills a request on the live hosts."""

    def get(self, host_name):
        """Return a host."""
        h = self.request.mongo_connection.shinken_live.hosts.find_one(
            {"host_name": host_name}, {'_id': 0}
        )

        host_dicts=[]
        for item in h:
            host_dict = self._host_dict_from_mongo_item(item)
            host_dicts.append(host_dict)

        return host_dicts



    def get_all(self, live_query=None):
        """Return all live hosts."""
        if live_query:
            query = mongodb_query.build_mongodb_query(live_query)
        else:
            query = {}

        response = (self.request.mongo_connection.
                      shinken_live.hosts.find(query))

        host_dicts = []

        for item in response:
            host_dict = self._host_dict_from_mongo_item(item)
            host_dicts.append(host_dict)


        if live_query:
            host_dicts = fields_filter.filter_fields(
                host_dicts,
                live_query
            )

        hosts = []
        for host_dict in host_dicts:
            host = live_host.LiveHost(**host_dict)
            hosts.append(host)

        return hosts

    def _host_dict_from_mongo_item(self, mongo_item):
        last_chk = mongo_item.pop('last_chk', None)
        if last_chk:
            mongo_item['last_check'] = int(last_chk)

        last_state_change = mongo_item.pop('last_state_change', None)
        if last_state_change:
            mongo_item['last_state_change'] = int(last_state_change)

        output = mongo_item.pop('output', None)
        if output:
            mongo_item['plugin_output'] = output

        childs = mongo_item.pop('childs', None)
        if childs:
            mongo_item['childs'] = json.loads(childs)

        parents = mongo_item.pop('parents', None)
        if parents:
            mongo_item['parents'] = json.loads(parents)



        return mongo_item
