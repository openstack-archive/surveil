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

from surveil.api.datamodel.config import notificationway
from surveil.api.handlers import mongo_object_handler


class NotificationWayHandler(mongo_object_handler.MongoObjectHandler):
    """Fulfills a request on the Notification Way resource."""

    def __init__(self, *args, **kwargs):
        super(NotificationWayHandler, self).__init__(
            'notificationways',
            'notificationway_name',
            notificationway.NotificationWay,
            *args,
            **kwargs
        )
