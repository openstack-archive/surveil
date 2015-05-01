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

import copy
import json

from surveil.api.datamodel.config import command
from surveil.tests.api import functionalTest


class TestCommandController(functionalTest.FunctionalTest):

    def setUp(self):
        super(TestCommandController, self).setUp()
        self.commands = [
            {u"command_name": u"check_test1",
             u"command_line": u"/test/test1/test.py"},
            {u"command_name": u"check_test2",
             u"command_line": u"/test/test2/test.py"},
        ]
        self.mongoconnection.shinken.commands.insert(
            copy.deepcopy(self.commands)
        )

    def test_get_all_commands(self):
        response = self.get('/v2/config/commands')

        self.assert_count_equal_backport(
            json.loads(response.body.decode()),
            self.commands
        )
        self.assertEqual(response.status_int, 200)

    def test_get_specific_command(self):

        response = self.get('/v2/config/commands/check_test2')

        self.assert_count_equal_backport(
            json.loads(response.body.decode()),
            self.commands[1]
        )
        self.assertEqual(response.status_int, 200)

    def test_update_command(self):
        put_body = {"command_line": "test_put",
                    "command_name": "check_test2"}
        response = self.put_json(
            "/v2/config/commands/check_test2", params=put_body
        )

        expected_command = {u"command_name": u"check_test2",
                            u"command_line": u"test_put"}

        mongo_command = command.Command(
            **self.mongoconnection.shinken.commands.find_one(
                {'command_name': 'check_test2'}
            )
        )

        self.assertEqual(expected_command, mongo_command.as_dict())
        self.assertEqual(response.status_int, 204)

    def test_delete_command(self):
        response = self.delete('/v2/config/commands/check_test2')

        expected_commands = [
            {u"command_name": u"check_test1",
             u"command_line": u"/test/test1/test.py"}
        ]
        mongo_commands = [command.Command(**c).as_dict() for c
                          in self.mongoconnection.shinken.commands.find()]

        self.assertEqual(expected_commands, mongo_commands)
        self.assertEqual(response.status_int, 204)

    def test_add_command(self):
        new_command = {
            "command_name": "newcommand",
            "command_line": "/usr/bin/newcommand -hello"
        }
        response = self.post_json(
            "/v2/config/commands",
            params=new_command
        )

        commands = [command.Command(**c).as_dict() for c
                    in self.mongoconnection.shinken.commands.find()]

        self.assertTrue(new_command in commands)
        self.assertEqual(response.status_int, 201)
