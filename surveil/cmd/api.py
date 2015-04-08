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
import sys
import time
import inspect
import subprocess
from threading import Thread

import pecan
from wsgiref import simple_server
from oslo_config import cfg

import surveil.api.app as app

CONF = cfg.CONF

OPTS = [
    cfg.StrOpt('api_paste_config',
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
        from watchdog.observers import Observer
        from watchdog.events import (
            FileSystemEventHandler, FileSystemMovedEvent, FileModifiedEvent,
            DirModifiedEvent
        )

        print('Monitoring for changes...')
        self.create_subprocess()

        parent = self

        class AggressiveEventHandler(FileSystemEventHandler):

            def __init__(self):
                self.wait = False

            def should_reload(self, event):
                for t in (
                        FileSystemMovedEvent, FileModifiedEvent, DirModifiedEvent
                ):
                    if isinstance(event, t):
                        return True
                return False

            def ignore_events_one_sec(self):
                if not self.wait:
                    self.wait = True
                    t = Thread(target=self.wait_one_sec)
                    t.start()

            def wait_one_sec(self):
                time.sleep(1)
                self.wait = False

            def on_modified(self, event):
                if self.should_reload(event) and not self.wait:
                    print("Some source files have been modified")
                    print("Restarting server...")
                    self.ignore_events_one_sec()
                    parent.server_process.kill()
                    parent.create_subprocess()

        # Determine a list of file paths to monitor
        paths = self.paths_to_monitor()

        event_handler = AggressiveEventHandler()
        for path, recurse in paths:
            observer = Observer()
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

    def paths_to_monitor(self):
        paths = []

        for package_name in getattr(self.config.app, 'modules', []):
            module = __import__(package_name, fromlist=['app'])
            if hasattr(module, 'app') and hasattr(module.app, 'setup_app'):
                paths.append((
                    os.path.dirname(module.__file__),
                    True
                ))
                break

        paths.append((os.path.dirname(self.config.__file__), False))
        return paths


def get_pecan_config():
    # Set up the pecan configuration
    return pecan.configuration.conf_from_file(get_config_filename())


def get_config_filename():
    path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    filename = "config.py"
    return os.path.join(path, filename)


def main():
    srv = ServerManager()
    srv.run(get_pecan_config(), get_config_filename())
