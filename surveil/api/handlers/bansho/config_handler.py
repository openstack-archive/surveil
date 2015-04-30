# Copyright 2015 - Savoir-Faire Linux inc.
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


class ConfigHandler(handler.Handler):
    """Fulfills a request on the bansho config ressource."""

    def get(self, user_name):
        """Returns user config, empty dict by default."""
        user_name = str(user_name)
        c = self.request.mongo_connection.surveil.bansho.config.find_one(
            {"user_name": user_name}, {'_id': 0}
        )
        config = (c or {}).get('config', {})
        return config

    def update(self, user_name, config):
        """Modify user config."""
        user_name = str(user_name)

        config_dict = {
            "user_name": user_name,
            "config": config
        }

        c = self.request.mongo_connection.surveil.bansho.config.find_one(
            {"user_name": user_name}, {'_id': 0}
        )

        if c is None:
            self.request.mongo_connection.surveil.bansho.config.insert(
                config_dict
            )
        else:
            self.request.mongo_connection.surveil.bansho.config.update(
                {"user_name": user_name},
                config_dict
            )
