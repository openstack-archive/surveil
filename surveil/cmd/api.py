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
import sys

from oslo_config import cfg
from pecan.commands import base

from surveil.api import app

CONF = cfg.CONF

OPTS = [
    cfg.StrOpt(
        'api_paste_config',
        default="api_paste.ini",
        help="Configuration file for WSGI definition of API."
    ),
]

CONF.register_opts(OPTS)


class SurveilCommandRunner(base.CommandRunner):

    def __init__(self):
        super(SurveilCommandRunner, self).__init__()
        self.parser = argparse.ArgumentParser(description='Surveil API server')
        self.parser.add_argument('--reload', '-r', action='store_true',
                                 help='Automatically reload as code changes')
        self.parser.add_argument('--pecan_config', '-p',
                                 default='/etc/surveil/config.py',
                                 help='Pecan config file (config.py)')
        self.parser.add_argument('--api_paste_config', '-a',
                                 default='/etc/surveil/api_paste.ini',
                                 help='API Paste config file (api_paste.ini)')
        self.parser.add_argument('--config_file', '-c',
                                 default='/etc/surveil/surveil.cfg',
                                 help='Pecan config file (surveil.cfg)')

    def run(self, args):
        namespace = self.parser.parse_args(args)
        # Get absolute paths
        namespace.pecan_config = os.path.join(os.getcwd(),
                                              namespace.pecan_config)
        namespace.api_paste_config = os.path.join(os.getcwd(),
                                                  namespace.api_paste_config)
        namespace.config_file = os.path.join(os.getcwd(),
                                             namespace.config_file)

        # Check conf files exist
        if not os.path.isfile(namespace.pecan_config):
            print("Bad config file: %s" % namespace.pecan_config,
                  file=sys.stderr)
            sys.exit(1)
        if not os.path.isfile(namespace.api_paste_config):
            print("Bad config file: %s" % namespace.api_paste_config,
                  file=sys.stderr)
            sys.exit(2)
        if not os.path.isfile(namespace.config_file):
            print("Bad config file: %s" % namespace.config_file,
                  file=sys.stderr)
            sys.exit(1)

        app.SurveilCommand().run(namespace)

    @classmethod
    def handle_command_line(cls):  # pragma: nocover
        runner = SurveilCommandRunner()
        runner.run(sys.argv[1:])
