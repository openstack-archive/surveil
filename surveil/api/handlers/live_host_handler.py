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
import sys
from surveil.api.handlers import handler
from influxdb import InfluxDBClient
from surveil.api.datamodel import live_host


class HostHandler(handler.Handler):
    """Fulfills a request on the service resource."""

    def get_all(self, host_name=None):
        """Return all live hosts."""

        cli = InfluxDBClient('influxdb', 8086, 'root', 'root', 'db')

        series = cli.get_list_series()

        host_names = []

        for serie in series:
            tags = serie.get('tags', {})

            print(tags, file=sys.stderr)

            host_name = tags[0].get('host_name', None)
            if host_name and host_name not in host_names:
                host_names.append(host_name)

        hosts = []
        for host_name in host_names:
            hosts.append(live_host.LiveHost(host_name=host_name))

        return hosts
