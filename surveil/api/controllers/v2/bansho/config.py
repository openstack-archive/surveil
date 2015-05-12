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
import wsme.types as wtypes
import wsmeext.pecan as wsme_pecan

from surveil.api.handlers.bansho import config_handler
from surveil.common import util


class ConfigController(rest.RestController):

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(wtypes.text)
    def get(self):
        """Retrieve user config, empty dict if no config exists."""
        user_name = pecan.request.headers.get('X-User-Id')
        handler = config_handler.ConfigHandler(pecan.request)
        config = handler.get(user_name)
        return config

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(body=wtypes.text,)
    def post(self, config):
        """Save user config.

        :param config: JSON config object
        """
        user_name = pecan.request.headers.get('X-User-Id')
        handler = config_handler.ConfigHandler(pecan.request)
        handler.update(user_name, config)
