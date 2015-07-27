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
from pecan.commands.base import CommandRunner

import surveil.api.app as app

from surveil.api.app import SurveilCommand

CONF = cfg.CONF

OPTS = [
    cfg.StrOpt(
        'api_paste_config',
        default="api_paste.ini",
        help="Configuration file for WSGI definition of API."
    ),
]

CONF.register_opts(OPTS)


class SurveilCommandRunner(CommandRunner):

    def __init__(self):
        super(SurveilCommandRunner, self).__init__()
        self.parser = argparse.ArgumentParser(description='Surveil API server')
        self.parser.add_argument('--reload', '-r', action='store_true',
                   help='Automatically reload as code changes')
        self.parser.add_argument('--config-file', '-c',
                       default='/etc/surveil/config.py',
                       help='Pecan config file (config.py)')
        self.parser.add_argument('--api_paste_config', '-a',
                       default='/etc/surveil/api_paste.ini',
                       help='API Paste config file (api_paste.ini)')

    def run(self, args):
        namespace = self.parser.parse_args(args)
        # Get absolute paths
        config_file_path = os.path.join(os.getcwd(), namespace.config_file)
        namespace.config_file = config_file_path
        api_paste_config_file_path = os.path.join(os.getcwd(), namespace.api_paste_config)
        namespace.api_paste_config = api_paste_config_file_path

        # Check conf files exist
        if not os.path.isfile(config_file_path):
            print("Bad config file: %s" % namespace.config_file_path, file=sys.stderr)
            sys.exit(1)
        if not os.path.isfile(api_paste_config_file_path):
            print("Bad config file: %s" % namespace.api_paste_config, file=sys.stderr)
            sys.exit(2)

        SurveilCommand().run(namespace)

    @classmethod
    def handle_command_line(cls):  # pragma: nocover
        runner = SurveilCommandRunner()
        runner.run(sys.argv[1:])
