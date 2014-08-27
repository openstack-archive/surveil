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

from pecan import hooks


class DBHook(hooks.PecanHook):

    def __init__(self, mongo_connection, ws_arbiter_url):
        self.mongo_connection = mongo_connection
        self.ws_arbiter_url = ws_arbiter_url

    def before(self, state):
        state.request.mongo_connection = self.mongo_connection
        state.request.ws_arbiter_url = self.ws_arbiter_url
