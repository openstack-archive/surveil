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

from surveil.api.controllers.v1 import commands
from surveil.api.controllers.v1 import hello
from surveil.api.controllers.v1 import hosts
from surveil.api.controllers.v1 import reload_config
from surveil.api.controllers.v1 import services


class V1Controller(object):
    """Version 1 API controller root."""
    hello = hello.HelloController()
    hosts = hosts.HostsController()
    commands = commands.CommandsController()
    services = services.ServicesController()
    reload_config = reload_config.ReloadConfigController()
