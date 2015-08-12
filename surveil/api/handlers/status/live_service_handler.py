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

from surveil.api.datamodel.status import live_service
from surveil.api.handlers.status import mongodb_query
from surveil.api.handlers.status import status_handler


class ServiceHandler(status_handler.StatusHandler):
    """Fulfills a request on live services."""

    def get(self, host_name, service_description):
        """Return a specific service."""
        mongo_s = self.request.mongo_connection.alignak_live.services.find_one(
            {"host_name": host_name,
             "service_description": service_description},
        )
        return live_service.LiveService(**mongo_s)

    def get_all(self, live_query=None):
        """Return all live services."""

        service_mappings = {
            "last_check": "last_chk",
            "description": "service_description",
            "plugin_output": "output",
            "acknowledged": "problem_has_been_acknowledged",
        }

        if live_query:
            lq = mongodb_query.translate_live_query(live_query.as_dict(),
                                                    service_mappings)
        else:
            lq = {}

        query, kwargs = mongodb_query.build_mongodb_query(lq)

        mongo_dicts = (self.request.mongo_connection.
                       alignak_live.services.find(*query, **kwargs))

        service_dicts = [
            _service_dict_from_mongo_item(s) for s in mongo_dicts
        ]

        services = []
        for service_dict in service_dicts:
            service = live_service.LiveService(**service_dict)
            services.append(service)

        return services


def _service_dict_from_mongo_item(mongo_item):
    """Create a dict from a mongodb item."""

    mappings = [
        ('last_chk', 'last_check', int),
        ('last_state_change', 'last_state_change', float),
        ('output', 'plugin_output', str),
        ('problem_has_been_acknowledged', 'acknowledged', bool),
    ]

    for field in mappings:
        value = mongo_item.pop(field[0], None)
        if value is not None:
            mongo_item[field[1]] = field[2](value)

    return mongo_item
