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
import subprocess
import sys
import time
import os
import inspect
import socket

from threading import Thread
from wsgiref import simple_server
import pecan

from oslo_config import cfg
from paste import deploy

CONF = cfg.CONF

OPTS = [
    cfg.StrOpt('api_paste_config',
               default="api_paste.ini",
               help="Configuration file for WSGI definition of API."
               ),
]

CONF.register_opts(OPTS)


def get_pecan_config():
    # Set up the pecan configuration
    return pecan.configuration.conf_from_file(get_config_filename())


def get_config_filename():
    path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    filename = "config.py"
    return os.path.join(path, filename)


def setup_app(pecan_config):
    app_conf = dict(pecan_config.app)

    app = pecan.make_app(
        app_conf.pop('root'),
        logging=getattr(pecan_config, 'logging', {}),
        **app_conf
    )

    return app


def build_server():
    srv = PecanServer()
    srv.run(get_pecan_config(), get_config_filename())


def load_app():
    return deploy.loadapp('config:/etc/surveil/api_paste.ini')


def app_factory(global_config, **local_conf):
    return VersionSelectorApplication()


class VersionSelectorApplication(object):
    def __init__(self):
        pc = get_pecan_config()

        def not_found(environ, start_response):
            start_response('404 Not Found', [])
            return []

        self.v1 = setup_app(pecan_config=pc)
        self.v2 = setup_app(pecan_config=pc)

    def __call__(self, environ, start_response):
        if environ['PATH_INFO'].startswith('/v1/'):
            return self.v1(environ, start_response)
        return self.v2(environ, start_response)


class PecanServer:

    def __init__(self):
        self.config = {}
        self.config_file = ""
        self.server_process = None
        self.should_run = True

    def run(self, pecan_config, config_file):
        self.config = pecan_config
        self.config_file = config_file
        self.watch_and_spawn()

    def create_subprocess(self):
        app = load_app()
        host, port = self.config.server.host, self.config.server.port

        self.server_process = simple_server.make_server(host, port, app)
        self.server_process.serve_forever()

    def watch_and_spawn(self):
        from watchdog.observers import Observer
        from watchdog.events import (
            FileSystemEventHandler, FileSystemMovedEvent, FileModifiedEvent,
            DirModifiedEvent
        )

        print('Monitoring for changes...')
        self.t = Thread(target=self.create_subprocess)
        self.t.start()

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

            def ignore_events(self):
                if not self.wait:
                    self.wait = True
                    t = Thread(target=self.wait_one_sec)
                    t.start()

            def wait_one_sec(self):
                time.sleep(1)
                self.wait = False

            def on_modified(self, event):
                if self.should_reload(event) and not self.wait:
                    self.ignore_events()
                    parent.server_process.shutdown()
                    parent.server_process.server_close()
                    parent.t = Thread(target=parent.create_subprocess)
                    parent.t.start()

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
