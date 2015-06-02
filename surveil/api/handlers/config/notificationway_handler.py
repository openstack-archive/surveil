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
from surveil.api.handlers import handler


class NotificationWayHandler(handler.Handler):
    def get(self, notificationway_name):
        """Return a notification way."""

        g = self.request.mongo_connection.shinken.notificationways.find_one(
            {"notificationway_name": notificationway_name}, {'_id': 0}
        )
        return notificationway.NotificationWay(**g)

    def update(self, notificationway_name, notificationway):
        """Modify an existing notification way."""
        notificationway_dict = notificationway.as_dict()
        if "notificationway_name" not in notificationway_dict.keys():
            notificationway_dict['notificationway_name'] = notificationway_name

        self.request.mongo_connection.shinken.notificationways.update(
            {"notificationway_name": notificationway_name},
            {"$set": notificationway_dict},
            upsert=True
        )

    def delete(self, notificationway_name):
        """Delete existing notification way."""
        self.request.mongo_connection.shinken.notificationways.remove(
            {"notificationway_name": notificationway_name}
        )

    def create(self, notificationway):
        """Create a new notification way."""
        self.request.mongo_connection.shinken.notificationways.insert(
            notificationway.as_dict()
        )

    def get_all(self):
        """Return all notification way."""
        notificationways = [
            g for g in self.request.mongo_connection
            .shinken.notificationways.find(
                {"register": {"$ne": "0"}},
                {'_id': 0}
            )]
        notificationways = [
            notificationway.NotificationWay(**g) for g in notificationways
        ]

        return notificationways
