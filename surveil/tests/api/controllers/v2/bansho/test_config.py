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

import copy
import json

from surveil.tests.api import functionalTest


class TestConfigController(functionalTest.FunctionalTest):

    def setUp(self):
        super(TestConfigController, self).setUp()
        self.config = [
            {
                "user_name": "bob",
                "config": {"k": "v",
                           "k2": "v2"}
            }
        ]
        self.mongoconnection.surveil.bansho.config.insert(
            copy.deepcopy(self.config)
        )

    def test_get_post_get(self):

        # At first, conf is empty
        self.assertIsNone(
            self.mongoconnection.surveil.bansho.config.find_one(
                {"user_name": "surveil-default-user"}
            )
        )
        response = self.get('/v2/bansho/config')
        self.assertEqual({}, json.loads(response.body.decode()))

        # Now, post config
        config = {"key": "val",
                  "morekey": "moreval"}
        self.post_json('/v2/bansho/config', params=config)

        # Now config is what we gave to the API
        response = self.get('/v2/bansho/config')
        self.assertEqual(config, json.loads(response.body.decode()))
        self.assertIsNotNone(
            self.mongoconnection.surveil.bansho.config.find_one(
                {"user_name": "surveil-default-user"}
            )
        )
