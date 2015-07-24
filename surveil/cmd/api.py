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

from __future__ import print_function
from __future__ import unicode_literals
import argparse
import os
import subprocess
import sys
import threading
import time
from wsgiref import simple_server

from oslo_config import cfg

import surveil.api.app as app

CONF = cfg.CONF

OPTS = [
    cfg.StrOpt(
        'api_paste_config',
        default="api_paste.ini",
        help="Configuration file for WSGI definition of API."
    ),
]

CONF.register_opts(OPTS)



def main():
    parser = argparse.ArgumentParser(description='Surveil API server')
    parser.add_argument('--reload', '-r', action='store_true',
                   help='Automatically reload as code changes')
    parser.add_argument('--config', '-c',
                       default='/etc/surveil/config.py',
                       help='Pecan config file (config.py)')
    parser.add_argument('--api_paste_config', '-a',
                       default='/etc/surveil/api_paste.ini',
                       help='API Paste config file (api_paste.ini)')
    args = parser.parse_args(sys.argv[1:])

    # Get absolute paths
    config_file_path = os.path.join(os.getcwd(), args.config)
    api_paste_config_file_path = os.path.join(os.getcwd(), args.api_paste_config)

    # Check conf files exist
    if not os.path.isfile(config_file_path):
        print("Bad config file: %s" % config_file_path, file=sys.stderr)
        sys.exit(1)
    if not os.path.isfile(api_paste_config_file_path):
        print("Bad config file: %s" % args.api_paste_config, file=sys.stderr)
        sys.exit(2)

    srv = app.ServerManager(config_file_path,
                            api_paste_config_file_path,
                            auto_reload=args.reload)
    srv.run()
