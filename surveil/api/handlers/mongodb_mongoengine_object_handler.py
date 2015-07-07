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
                 resource_storage,
                 *args,
                 **kwargs):
        super(MongoObjectHandler, self).__init__(*args, **kwargs)
        self.resource_collection = resource_colleciton
        self.resource_key = resource_key
        self.resource_datamodel = resource_datamodel
        self.resource_storage = resource_storage

    def _get_resource_collection(self):
        shinken_db = self.request.mongo_connection.shinken
        resource_colleciton = getattr(shinken_db, self.resource_collection)
        return resource_colleciton

    def get(self, resource_key_value):
        """Return the resource."""
        return self.resource_storage.objects.get(
            **{self.resource_key: resource_key_value}
        )

    def update(self, resource_key_value, resource):
        """Modify an existing resource."""
        r = self.get(resource_key_value)
        resource_dict = resource.as_dict()
        for key, value in resource_dict.items():
            setattr(r, key, value)
        r.save()

    def delete(self, resource_key_value):
        """Delete existing resource."""
        r = self.get(resource_key_value)
        r.delete()
        r.save()

    def create(self, resource):
        """Create a new resource."""
        r = self.resource_storage(**resource.as_dict())
        r.save()

    def get_all(self):
        """Return all resources."""
        return [r for r in self.resource_storage.objects()]
