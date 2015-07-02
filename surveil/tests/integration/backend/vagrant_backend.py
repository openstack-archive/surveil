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

import os
import time

from surveilclient import client as sclient
import vagrant


class VagrantBackend(object):

    def setUpClass(self):
        vagrantfile_dir = os.path.realpath(
            os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                "../../../../contrib/vagrant-surveil-devstack"
            )
        )

        self.vagrant = vagrant.Vagrant(root=vagrantfile_dir)
        self.vagrant.up()

        hostname = self.vagrant.hostname()
        surveil_endpoint = hostname + ':5311/v2'
        surveil_auth_endpoint = surveil_endpoint + '/auth'

        print hostname
        print surveil_endpoint
        print surveil_auth_endpoint

        self.surveil_client = sclient.Client(
            surveil_endpoint,
            surveil_auth_endpoint,
            version='v2_0'
        )

        #  Wait until Surveil is available
        now = time.time()
        while True:
            print("Waiting for surveil... %s" % int(time.time() - now))
            if time.time() < (now + 280):
                try:
                    #  If 'ws-arbiter' is found, Surveil is ready!
                    configured_hosts = self.surveil_client.status.hosts.list()
                    host_found = False
                    for host in configured_hosts:
                        if host['host_name'].decode() == 'ws-arbiter':
                            host_found = True
                            break
                    if host_found:
                        break
                except Exception:
                    pass
                time.sleep(10)
            else:
                raise Exception("Surveil could not start")

    def tearDownClass(self):
        self.vagrant.suspend()
        self.vagrant.destroy()

    def get_surveil_client(self):
        return self.surveil_client