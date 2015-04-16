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

import os

import mongomock
from oslo_config import cfg
import pecan
from pecan import hooks
import pecan.testing

from surveil.tests import base


__all__ = ['FunctionalTest']


class FunctionalTest(base.BaseTestCase):
    """Used for functional tests.

    Used where you need to test your literal
    application and its integration with the framework.
    """

    def setUp(self):

        self.mongoconnection = mongomock.Connection()
        self.ws_arbiter_url = "http://localhost:7760"

        class TestHook(hooks.PecanHook):
            def __init__(self, mongoclient, wsarbiterurl):
                self.mongoclient = mongoclient
                self.ws_arbiter_url = wsarbiterurl

            def before(self, state):
                state.request.mongo_connection = self.mongoclient
                state.request.ws_arbiter_url = self.ws_arbiter_url


        app_hooks = [
            TestHook(
                self.mongoconnection,
                self.ws_arbiter_url
            )
        ]

        policy_path = os.path.dirname(os.path.realpath(__file__))

        opts = [
            cfg.StrOpt('config_dir', default=policy_path),
            cfg.StrOpt('config_file', default='policy.json'),
            cfg.StrOpt('project', default='surveil'),
        ]

        cfg.CONF.register_opts(opts)

        self.app = pecan.testing.load_test_app({
            'app': {
                'root': 'surveil.api.controllers.root.RootController',
                'modules': ['surveil.api'],
                'debug': False,
                'hooks': app_hooks
            }
        })

    def tearDown(self):
        pecan.set_config({}, overwrite=True)
