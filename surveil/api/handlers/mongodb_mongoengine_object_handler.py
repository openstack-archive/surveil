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

from surveil.api.handlers.config import mongoengine_query
from surveil.api.handlers import handler


class MongoObjectHandler(handler.Handler):
    """Fulfills a request on a MongoDB resource."""

    def __init__(self,
                 resource_datamodel,
                 resource_storage,
                 *args,
                 **kwargs):
        super(MongoObjectHandler, self).__init__(*args, **kwargs)
        self.resource_datamodel = resource_datamodel
        self.resource_storage = resource_storage

    def _get_mongoengine_object(self, identifier):
        return self.resource_storage.objects.get(**identifier)

    def _get_dict(self, mongoengine_object):
        json_object = mongoengine_object.to_mongo().to_dict()
        json_object.pop('_id', None)
        return json_object

    def get(self, identifier):
        """Return the resource."""
        mongoengine_object = self._get_mongoengine_object(identifier)
        resource_dict = self._get_dict(mongoengine_object)
        return self.resource_datamodel(**resource_dict)

    def update(self, identifier, resource):
        """Modify an existing resource."""
        r = self._get_mongoengine_object(identifier)
        resource_dict = resource.as_dict()
        for key, value in resource_dict.items():
            setattr(r, key, value)
        r.save()

    def delete(self, identifier):
        """Delete existing resource."""
        r = self._get_mongoengine_object(identifier)
        r.delete()
        r.save()

    def create(self, resource):
        """Create a new resource."""
        r = self.resource_storage(**resource.as_dict())
        r.save()

    def get_all(self, lq={}):
        """Return all resources."""

        fields, query, kwargs = mongoengine_query.build_mongoengine_query(lq)

        resp = [
            self.resource_datamodel(**self._get_dict(r))
            for r
            in self.resource_storage.objects(**query)
        ][kwargs]

        resp_field = []

        if fields:
            for obj in resp:
                obj_with_field = {}
                for field in fields:
                    obj_with_field[field] = obj[field]
                resp_field.append(obj_with_field)

        else:
            resp_field = resp

        return resp_field
