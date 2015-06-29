# Copyright 2015 - Savoir-Faire Linux inc.
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

import types

import pecan
from pecan import rest
import wsme.types as wtypes
import wsmeext.pecan as wsme_pecan

from surveil.common import util


class CrudController(rest.RestController):
    """Generic Controller that provides standard CRUD functions."""

    def __init__(self,
                 handler,
                 datamodel,
                 resource_description):

        @util.policy_enforce(['authenticated'])
        @wsme_pecan.wsexpose([datamodel])
        def get_all(self):
            h = handler(pecan.request)
            resources = h.get_all()
            return resources
        self.get_all = types.MethodType(
            get_all,
            self,
            "Returns all %s resources" % resource_description
        )

        @util.policy_enforce(['authenticated'])
        @wsme_pecan.wsexpose(datamodel, wtypes.text)
        def get_one(self, resource_name):
            h = handler(pecan.request)
            resource = h.get(resource_name)
            return resource
        self.get_one = types.MethodType(
            get_one,
            self,
            "Returns a specific %s resource" % resource_description
        )

        @util.policy_enforce(['authenticated'])
        @wsme_pecan.wsexpose(body=datamodel, status_code=201)
        def post(self, data):
            h = handler(pecan.request)
            h.create(data)
        self.post = types.MethodType(
            post,
            self,
            """Create a new %s.

             :param data: a %s within the request body.
             """ % (resource_description, resource_description)
        )

        @util.policy_enforce(['authenticated'])
        @wsme_pecan.wsexpose(datamodel, wtypes.text, status_code=204)
        def delete(self, resource_name):
            h = handler(pecan.request)
            h.delete(resource_name)
        self.delete = types.MethodType(
            delete,
            self,
            "Returns a specific %s" % resource_description
        )

        @util.policy_enforce(['authenticated'])
        @wsme_pecan.wsexpose(datamodel,
                             wtypes.text,
                             body=datamodel,
                             status_code=204)
        def put(self, resource_name, resource):
            h = handler(pecan.request)
            h.update(resource_name, resource)
        self.put = types.MethodType(
            put,
            self,
            """Update an existing %s.

             :param data: a %s within the request body.
            """ % (resource_description, resource_description)
        )
