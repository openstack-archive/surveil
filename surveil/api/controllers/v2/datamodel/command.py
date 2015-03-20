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

import wsme
import wsme.types as wtypes

from surveil.api.controllers.v1.datamodel import types


# import shinken.objects
# Command = type(
#     'Command',
#     (wtypes.Base,),
#     {key: wtypes.text for key in shinken.objects.Command.properties.keys()}
# )


class Command(types.Base):
    command_name = wsme.wsattr(wtypes.text, mandatory=True)
    """The name of the command"""

    command_line = wsme.wsattr(wtypes.text, mandatory=True)
    """This directive is used to define what is actually executed by Shinken"""

    @classmethod
    def sample(cls):
        return cls(
            command_name="check_http",
            command_line="/bin/check_http"
        )
