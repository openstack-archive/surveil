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

from surveil.api.datamodel.config import host as host_datamodel
from surveil.api.handlers import mongodb_mongoengine_object_handler
from surveil.api.storage.mongodb.config import host as host_storage


class HostHandler(mongodb_mongoengine_object_handler.MongoObjectHandler):
    """Fulfills a request on the Host resource."""

    def __init__(self, *args, **kwargs):
        super(HostHandler, self).__init__(
            host_datamodel.Host,
            host_storage.Host,
            *args,
            **kwargs
        )
