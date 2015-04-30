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

from surveil.api.controllers.v2 import actions as v2_actions
from surveil.api.controllers.v2 import admin as v2_admin
from surveil.api.controllers.v2 import auth as v2_auth
from surveil.api.controllers.v2 import bansho as v2_bansho
from surveil.api.controllers.v2 import config as v2_config
from surveil.api.controllers.v2 import hello as v2_hello
from surveil.api.controllers.v2 import logs as v2_logs
from surveil.api.controllers.v2 import status as v2_status


class V2Controller(object):
    """Version 2 API controller root."""
    actions = v2_actions.ActionsController()
    config = v2_config.ConfigController()
    hello = v2_hello.HelloController()
    status = v2_status.StatusController()
    surveil = v2_admin.AdminController()
    auth = v2_auth.AuthController()
    logs = v2_logs.LogsController()
    bansho = v2_bansho.BanshoController()
