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

import influxdb
from pecan import hooks
import pymongo


class DBHook(hooks.PecanHook):

    def __init__(self, mongo_url, ws_arbiter_url, influxdb_url):
        self.mongo_url = mongo_url
        self.ws_arbiter_url = ws_arbiter_url
        self.influxdb_url = influxdb_url

    def before(self, state):
        self.mongoclient = pymongo.MongoClient(self.mongo_url)

        state.request.mongo_connection = self.mongoclient
        state.request.ws_arbiter_url = self.ws_arbiter_url
        state.request.influxdb_client = influxdb.InfluxDBClient.from_DSN(
            self.influxdb_url
        )

    def after(self, state):
        self.mongoclient.close()
