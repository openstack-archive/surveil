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

from surveil.api.handlers import handler
from surveil.api.handlers import mongo_object_handler
from surveil.api.datamodel.config import command as command_datamodel
import mongoengine


class Command(mongoengine.Document):
    meta = {'collection': 'commands'}
    command_name = mongoengine.StringField()
    command_line = mongoengine.StringField()


class CommandHandler(mongo_object_handler.MongoObjectHandler):
    """Fulfills a request on the Command resource."""

    def __init__(self, *args, **kwargs):
        super(CommandHandler, self).__init__(
            'commands',
            'command_name',
            command_datamodel.Command,
            *args,
            **kwargs
        )

    def get(self, resource_key_value):
        """Return the resource."""
        c = Command.objects(command_name=resource_key_value).first()
        return c
