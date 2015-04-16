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


class ServerManager:

    def __init__(self):
        self.config = {}
        self.config_file = ""
        self.server_process = None
        self.should_run = True

    def run(self, pecan_config, config_file):
        self.config = pecan_config
        self.config_file = config_file

        if '--reload' in sys.argv:
            self.watch_and_spawn()
        else:
            self.start_server()

    def create_subprocess(self):
        self.server_process = subprocess.Popen(['surveil-api'])

    def start_server(self):
        pecan_app = app.load_app()
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


def main():
    srv = ServerManager()
    srv.run(app.get_pecan_config(), app.get_config_filename())
