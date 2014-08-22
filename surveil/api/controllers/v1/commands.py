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

import pecan
from pecan import rest
import wsmeext.pecan as wsme_pecan

from surveil.api.controllers.v1.datamodel import command


class CommandController(rest.RestController):

    def __init__(self, command_name):
        pecan.request.context['command_name'] = command_name
        self._id = command_name

    @wsme_pecan.wsexpose(command.Command)
    def get(self):
        """Returns a specific command."""
        c = pecan.request.mongo_connection.shinken.commands.find_one(
            {"command_name": self._id}
        )
        return command.Command(**c)

    @wsme_pecan.wsexpose(None, body=command.Command, status_code=204)
    def put(self, data):
        """Modify this command.

        :param data: a command within the request body.
        """

        command_dict = data.as_dict()
        if "command_name" not in command_dict.keys():
            command_dict['command_name'] = self._id

        pecan.request.mongo_connection.shinken.commands.update(
            {"command_name": self._id},
            command_dict
        )

    @wsme_pecan.wsexpose(None, status_code=204)
    def delete(self):
        """Delete this command."""
        pecan.request.mongo_connection.shinken.commands.remove(
            {"command_name": self._id}
        )


class CommandsController(rest.RestController):

    @pecan.expose()
    def _lookup(self, command_id, *remainder):
        return CommandController(command_id), remainder

    @wsme_pecan.wsexpose([command.Command])
    def get_all(self):
        """Returns all commands."""
        commands = [c for c
                    in pecan.request.mongo_connection.shinken.commands.find()]

        return [command.Command(**c) for c in commands]

    @wsme_pecan.wsexpose(command.Command,
                         body=command.Command,
                         status_code=201)
    def post(self, data):
        """Create a new command.

        :param data: a command within the request body.
        """
        pecan.request.mongo_connection.shinken.commands.insert(
            data.as_dict()
        )