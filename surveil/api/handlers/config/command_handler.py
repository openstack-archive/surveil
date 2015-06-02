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

from surveil.api.datamodel.config import command
from surveil.api.handlers import handler


class CommandHandler(handler.Handler):
    """Fulfills a request on the service resource."""

    def get(self, command_name):
        """Return a command."""
        c = self.request.mongo_connection.shinken.commands.find_one(
            {"command_name": command_name}
        )
        return command.Command(**c)

    def update(self, command_name, command):
        """Modify existing command."""
        command_dict = command.as_dict()
        if "command_name" not in command_dict.keys():
            command_dict['command_name'] = command_name

        self.request.mongo_connection.shinken.commands.update(
            {"command_name": command_name},
            {"$set": command_dict},
            upsert=True
        )

    def delete(self, command_name):
        """Delete an existing command."""
        self.request.mongo_connection.shinken.commands.remove(
            {"command_name": command_name}
        )

    def create(self, data):
        """Create a new command."""
        self.request.mongo_connection.shinken.commands.insert(
            data.as_dict()
        )

    def get_all(self):
        """Return all commands."""
        commands = [c for c
                    in self.request.mongo_connection.shinken.commands.find()]

        return [command.Command(**c) for c in commands]