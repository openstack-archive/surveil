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

from __future__ import print_function
from __future__ import unicode_literals

import subprocess
import sys
import threading
import time

from paste import deploy
import pecan
from pecan import commands
from pecan import configuration
from six.moves import configparser


global_pecan_config_file = None


def setup_app(pecan_config):
    app_conf = dict(pecan_config.app)

    app = pecan.make_app(
        app_conf.pop('root'),
        logging=getattr(pecan_config, 'logging', {}),
        **app_conf
    )

    return app


def app_factory(global_config, **local_conf):
    global global_pecan_config_file
    return VersionSelectorApplication(global_pecan_config_file)


class VersionSelectorApplication(object):
    def __init__(self, pecan_conf_file):
        pc = pecan.configuration.conf_from_file(pecan_conf_file)

        self.v1 = setup_app(pecan_config=pc)
        self.v2 = setup_app(pecan_config=pc)
        self.config = pc

    def __call__(self, environ, start_response):
        if environ['PATH_INFO'].startswith('/v1/'):
            return self.v1(environ, start_response)
        return self.v2(environ, start_response)


class SurveilCommand(commands.ServeCommand):

    def run(self, args):
        global global_pecan_config_file
        global_pecan_config_file = args.pecan_config
        super(commands.ServeCommand, self).run(args)
        app = self.load_app()
        self.args = args
        self.serve(app, app.config)

    def load_app(self):
        config = configparser.ConfigParser()
        config.read(self.args.config_file)
        surveil_cfg = {"surveil_api_config":
                       dict([i for i in config.items("surveil")])}
        configuration.set_config(surveil_cfg, overwrite=True)
        configuration.set_config(self.args.pecan_config, overwrite=False)

        app = deploy.loadapp('config:%s' % self.args.api_paste_config)
        app.config = configuration._runtime_conf
        return app

    def create_subprocess(self):
        self.server_process = subprocess.Popen(
            [arg for arg in sys.argv if arg not in ['--reload', '-r']],
            stdout=sys.stdout, stderr=sys.stderr
        )

    # TODO(future useless): delete this function when
    # https://review.openstack.org/#/c/206213/
    # will be released
    def watch_and_spawn(self, conf):
        import watchdog.events as events
        import watchdog.observers as observers

        print('Monitoring for changes...',
              file=sys.stderr)

        self.create_subprocess()
        parent = self

        class AggressiveEventHandler(events.FileSystemEventHandler):

            def __init__(self):
                self.wait = False

            def should_reload(self, event):
                for t in (
                    events.FileSystemMovedEvent,
                    events.FileModifiedEvent,
                    events.DirModifiedEvent
                ):
                    if isinstance(event, t):
                        return True
                return False

            def ignore_events_one_sec(self):
                if not self.wait:
                    self.wait = True
                    t = threading.Thread(target=self.wait_one_sec)
                    t.start()

            def wait_one_sec(self):
                time.sleep(1)
                self.wait = False

            def on_modified(self, event):
                if self.should_reload(event) and not self.wait:
                    print("Some source files have been modified",
                          file=sys.stderr)
                    print("Restarting server...",
                          file=sys.stderr)
                    parent.server_process.kill()
                    self.ignore_events_one_sec()
                    parent.create_subprocess()

        paths = self.paths_to_monitor(conf)

        event_handler = AggressiveEventHandler()

        for path, recurse in paths:
            observer = observers.Observer()
            observer.schedule(
                event_handler,
                path=path,
                recursive=recurse
            )
            observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
