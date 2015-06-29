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

from __future__ import print_function
import sys
import types

import pecan
from pecan import rest
import wsme.types as wtypes
import wsmeext.pecan as wsme_pecan

from surveil.common import util


class CrudController(rest.RestController):
    """Generic Controller that provides standard CRUD functions"""

    def __init__(self,
                 handler,
                 datamodel):

        @util.policy_enforce(['authenticated'])
        @wsme_pecan.wsexpose([datamodel])
        def get_all(self):
            """Returns all resources."""
            h = handler(pecan.request)
            resources = h.get_all()
            return resources
        self.get_all = types.MethodType(get_all, self)

        @util.policy_enforce(['authenticated'])
        @wsme_pecan.wsexpose(datamodel, wtypes.text)
        def get_one(self, resource_name):
            """Returns a specific resource."""
            h = handler(pecan.request)
            resource = h.get(resource_name)
            return resource
        self.get_one = types.MethodType(get_one, self)

        @util.policy_enforce(['authenticated'])
        @wsme_pecan.wsexpose(body=datamodel, status_code=201)
        def post(self, data):
            """Create a new resource.

            :param data: a resource within the request body.
            """
            h = handler(pecan.request)
            h.create(data)
        self.post = types.MethodType(post, self)

        @util.policy_enforce(['authenticated'])
        @wsme_pecan.wsexpose(datamodel, wtypes.text, status_code=204)
        def delete(self, resource_name):
            """Returns a specific resource."""
            h = handler(pecan.request)
            h.delete(resource_name)
        self.delete = types.MethodType(delete, self)

        @util.policy_enforce(['authenticated'])
        @wsme_pecan.wsexpose(datamodel,
                             wtypes.text,
                             body=datamodel,
                             status_code=204)
        def put(self, resource_name, resource):
            """Returns a specific resource."""
            h = handler(pecan.request)
            h.update(resource_name, resource)
        self.put = types.MethodType(put, self)
