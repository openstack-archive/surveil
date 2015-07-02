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

import time
import os

from novaclient import client as novaclient
from surveilclient import client as sclient


class OpenStackBackend(object):

    def setUpClass(self):

        OS_AUTH_URL = os.environ.get('OS_AUTH_URL', None)
        OS_USERNAME = os.environ.get('OS_USERNAME', None)
        OS_PASSWORD = os.environ.get('OS_PASSWORD', None)
        OS_PROJECT_NAME = os.environ.get('OS_PROJECT_NAME', None)
        OS_REGION_NAME = os.environ.get('OS_REGION_NAME', None)

        if OS_AUTH_URL is None:
            raise Exception("OS_AUTH_URL environment variable not found.")

        if OS_USERNAME is None:
            raise Exception("OS_USERNAME environment variable not found.")

        if OS_PASSWORD is None:
            raise Exception("OS_PASSWORD environment variable not found.")

        if OS_PROJECT_NAME is None:
            raise Exception("OS_PROJECT_NAME environment variable not found.")

        nc = novaclient.Client(
            2,
            OS_USERNAME,
            OS_PASSWORD,
            OS_PROJECT_NAME,
            OS_AUTH_URL,
            region_name=OS_REGION_NAME,
        )

        # Flavor
        fl = os.environ.get("SURVEIL_INTEGRATION_OS_FLAVOR", None)
        if fl is None:
            fourgb_flavors = nc.flavors.findall(ram=4096)
            fl = fourgb_flavors[0]  # Pick any!

        # Image
        image = os.environ.get("SURVEIL_INTEGRATION_OS_IMAGE", None)
        if image is None:
            try:
                image = nc.images.find(name="CentOS 7")
            except Exception:
                raise Exception(
                    "Specify image to use with SURVEIL_INTEGRATION_OS_IMAGE"
                )

        # Network
        network = os.environ.get("SURVEIL_INTEGRATION_OS_NETWORK", None)
        if network is None:
            raise Exception(
                "Specify network to use with SURVEIL_INTEGRATION_OS_NETWORK"
            )

        # User data
        userdata_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'userdata'
        )

        with open(userdata_path, 'r') as userdata:
            self.server = nc.servers.create(
                name="surveil_integration_test",
                image=image,
                flavor=fl,
                userdata=userdata,
                nics=[{"net-id": network}],
            )

        print "SERVERIP" * 10
        print dir(self.server)

        self.surveil_client = sclient.Client(
            'http://localhost:8999/v2',
            auth_url='http://localhost:8999/v2/auth',
            version='2_0'
        )

        #  Wait until Surveil is available
        # now = time.time()
        # while True:
        #     print("Waiting for surveil... %s" % int(time.time() - now))
        #     if time.time() < (now + 280):
        #         try:
        #             #  If 'ws-arbiter' is found, Surveil is ready!
        #             configured_hosts = self.surveil_client.status.hosts.list()
        #             host_found = False
        #             for host in configured_hosts:
        #                 if host['host_name'].decode() == 'ws-arbiter':
        #                     host_found = True
        #                     break
        #             if host_found:
        #                 break
        #         except Exception:
        #             pass
        #         time.sleep(10)
        #     else:
        #         raise Exception("Surveil could not start")

    def tearDownClass(self):
        self.project.kill()
        self.project.remove_stopped()

    def get_surveil_client(self):
        return self.surveil_client