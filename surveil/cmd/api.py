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

"""Starter script for the Surveil API service."""

import os
from wsgiref import simple_server

import pecan

from surveil.api import app as api_app
from surveil.api import config as api_config


# TODO(aviau): Load conf from oslo
def get_pecan_config():
    # Set up the pecan configuration
    filename = api_config.__file__.replace('.pyc', '.py')
    return pecan.configuration.conf_from_file(filename)


def main():
    cfg = get_pecan_config()

    app = api_app.setup_app(cfg)

    # Create the WSGI server and start it
    host, port = cfg.server.host, cfg.server.port
    srv = simple_server.make_server(host, port, app)

    # TODO(aviau): Logging. don't print :o)
    print 'Starting server in PID %s' % os.getpid()

    if host == '0.0.0.0':
        print (
            'serving on 0.0.0.0:%(port)s, view at http://127.0.0.1:%(port)s' %
            dict(port=port)
        )
    else:
        print (
            'serving on http://%(host)s:%(port)s' % dict(host=host, port=port)
        )

    srv.serve_forever()