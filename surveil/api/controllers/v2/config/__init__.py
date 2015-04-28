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

from surveil.api.controllers.v2.config import commands
from surveil.api.controllers.v2.config import contacts
from surveil.api.controllers.v2.config import hosts
from surveil.api.controllers.v2.config import reload_config
from surveil.api.controllers.v2.config import services
from surveil.api.controllers.v2.config import timeperiods

from pecan import rest


class ConfigController(rest.RestController):
    """Root config controller."""
    hosts = hosts.HostsController()
    commands = commands.CommandsController()
    services = services.ServicesController()
    reload_config = reload_config.ReloadConfigController()
    contacts = contacts.ContactsController()
    timeperiods = timeperiods.TimePeriodsController()
    # hostgroups = HostGroupsController()
    # contactgroups = ContactGroupsController()
    # servicegroups = ServiceGroupsController()
    # realms = RealmsController()
    # notificationways = NotificationWayController()
    # engine = EngineController()
