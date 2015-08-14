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

import pymongo

from surveil.api.handlers import handler


class StatusHandler(handler.Handler):
    """This handler creates MongoDB indexes."""

    def __init__(self, *args, **kwargs):
        super(StatusHandler, self).__init__(*args, **kwargs)

        try:
            self.request.mongo_connection.admin.command(
                'setParameter',
                textSearchEnabled=True
            )
        except Exception:
            pass

        self.request.mongo_connection.alignak_live.hosts.ensure_index(
            [("$**", pymongo.TEXT)]
        )

        self.request.mongo_connection.alignak_live.services.ensure_index(
            [("$**", pymongo.TEXT)]
        )
