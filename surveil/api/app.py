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

import argparse
import os
import subprocess
import sys
import threading
import time
from wsgiref import simple_server


from paste import deploy
import pecan


def get_pecan_config(conffile):
    # Set up the pecan configuration
    return pecan.configuration.conf_from_file(conffile)


def setup_app(pecan_config):
    app_conf = dict(pecan_config.app)

    app = pecan.make_app(
        app_conf.pop('root'),
        logging=getattr(pecan_config, 'logging', {}),
        **app_conf
    )

    return app


def load_app(api_paste_config):
    return deploy.loadapp('config:%s' % api_paste_config)


def app_factory(global_config, **local_conf):
    return VersionSelectorApplication(global_pecan_config_file)


class VersionSelectorApplication(object):
    def __init__(self, pecan_conf_file):
        pc = get_pecan_config(pecan_conf_file)

        self.v1 = setup_app(pecan_config=pc)
        self.v2 = setup_app(pecan_config=pc)

    def __call__(self, environ, start_response):
        if environ['PATH_INFO'].startswith('/v1/'):
            return self.v1(environ, start_response)
        return self.v2(environ, start_response)


class ServerManager:

    def __init__(self, pecan_config_file, api_paste_config, auto_reload=False):
        global global_pecan_config_file
        self.server_process = None
        self.should_run = True
        self.pecan_config_file = global_pecan_config_file = pecan_config_file
        self.config = get_pecan_config(pecan_config_file)
        self.api_paste_config = api_paste_config
        self.auto_reload = auto_reload


    def run(self):
        if self.auto_reload:
            self.watch_and_spawn()
        else:
            self.start_server()

    def create_subprocess(self):
        self.server_process = subprocess.Popen(
            [arg for arg in sys.argv if arg not in ['--reload', '-r']],
            stdout=sys.stdout, stderr=sys.stderr
        )

    def start_server(self):
        pecan_app = load_app(self.api_paste_config)
        host, port = self.config.server.host, self.config.server.port
        srv = simple_server.make_server(host, port, pecan_app)
        srv.serve_forever()

    def watch_and_spawn(self):
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

        path = self.path_to_monitor()

        event_handler = AggressiveEventHandler()

        observer = observers.Observer()
        observer.schedule(
            event_handler,
            path=path,
            recursive=True
        )
        observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass

    def path_to_monitor(self):
        module = __import__('surveil')
        return os.path.dirname(module.__file__)

