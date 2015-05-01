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

from surveil.api.datamodel.config import command
from surveil.api.handlers.config import command_handler
from surveil.common import util


class CommandController(rest.RestController):

    def __init__(self, command_name):
        pecan.request.context['command_name'] = command_name
        self._id = command_name

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(command.Command)
    def get(self):
        """Returns a specific command."""
        handler = command_handler.CommandHandler(pecan.request)
        c = handler.get(self._id)
        return c

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(None, body=command.Command, status_code=204)
    def put(self, data):
        """Modify this command.

        :param data: a command within the request body.
        """
        handler = command_handler.CommandHandler(pecan.request)
        handler.update(self._id, data)

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(None, status_code=204)
    def delete(self):
        """Delete this command."""
        handler = command_handler.CommandHandler(pecan.request)
        handler.delete(self._id)


class CommandsController(rest.RestController):

    @pecan.expose()
    def _lookup(self, command_id, *remainder):
        return CommandController(command_id), remainder

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose([command.Command])
    def get_all(self):
        """Returns all commands."""
        handler = command_handler.CommandHandler(pecan.request)
        commands = handler.get_all()
        return commands

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(command.Command,
                         body=command.Command,
                         status_code=201)
    def post(self, data):
        """Create a new command.

        :param data: a command within the request body.
        """
        handler = command_handler.CommandHandler(pecan.request)
        handler.create(data)
