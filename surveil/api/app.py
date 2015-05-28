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

from __future__ import unicode_literals

import os

from paste import deploy
import pecan


def get_config_filename():
    abspath = os.path.abspath(__file__)
    path = os.path.dirname(abspath)
    filename = "config.py"
    return os.path.join(path, filename)


def get_pecan_config():
    # Set up the pecan configuration
    return pecan.configuration.conf_from_file(get_config_filename())


def setup_app(pecan_config):
    app_conf = dict(pecan_config.app)

    app = pecan.make_app(
        app_conf.pop('root'),
        logging=getattr(pecan_config, 'logging', {}),
        **app_conf
    )

    return app


def load_app():
    return deploy.loadapp('config:/etc/surveil/api_paste.ini')


def app_factory(global_config, **local_conf):
    return VersionSelectorApplication()


class VersionSelectorApplication(object):
    def __init__(self):
        pc = get_pecan_config()

        self.v1 = setup_app(pecan_config=pc)
        self.v2 = setup_app(pecan_config=pc)

    def __call__(self, environ, start_response):
        if environ['PATH_INFO'].startswith('/v1/'):
            return self.v1(environ, start_response)
        return self.v2(environ, start_response)
