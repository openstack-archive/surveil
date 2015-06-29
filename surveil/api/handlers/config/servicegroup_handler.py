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

from surveil.api.datamodel.config import servicegroup
from surveil.api.handlers import mongo_object_handler


class ServiceGroupHandler(mongo_object_handler.MongoObjectHandler):
    """Fulfills a request on the Service Group resource."""

    def __init__(self, *args, **kwargs):
        super(ServiceGroupHandler, self).__init__(
            'servicegroups',
            'servicegroup_name',
            servicegroup.ServiceGroup,
            *args,
            **kwargs
        )
