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

from surveil.api.handlers import handler


class MongoObjectHandler(handler.Handler):
    """Fulfills a request on a MongoDB resource."""

    def __init__(self,
                 resource_colleciton,
                 resource_key,
                 resource_datamodel,
                 *args,
                 **kwargs):
        super(MongoObjectHandler, self).__init__(*args, **kwargs)
        self.resource_collection = resource_colleciton
        self.resource_key = resource_key
        self.resource_datamodel = resource_datamodel

    def _get_resource_collection(self):
        shinken_db = self.request.mongo_connection.shinken
        resource_colleciton = getattr(shinken_db, self.resource_collection)
        return resource_colleciton

    def get(self, resource_key_value):
        """Return the resource."""
        r = self._get_resource_collection().find_one(
            {self.resource_key: resource_key_value},
            {'_id': 0}
        )
        return self.resource_datamodel(**r)

    def update(self, resource_key_value, resource):
        """Modify an existing resource."""
        resource_dict = resource.as_dict()
        if self.resource_key not in resource_dict.keys():
            resource_dict[self.resource_key] = resource_key_value

        self._get_resource_collection().update(
            {self.resource_key: resource_key_value},
            {"$set": resource_dict},
            upsert=True
        )

    def delete(self, resource_key_value):
        """Delete existing resource."""
        self._get_resource_collection().remove(
            {self.resource_key: resource_key_value}
        )

    def create(self, resource):
        """Create a new resource."""
        self._get_resource_collection().insert(
            resource.as_dict()
        )

    def get_all(self):
        """Return all resources."""
        resources = [r for r
                     in self._get_resource_collection()
                     .find({"register": {"$ne": "0"}},
                           {'_id': 0})]
        resources = [self.resource_datamodel(**r) for r in resources]
        return resources
