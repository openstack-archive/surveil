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

import json

import pecan
from pecan import rest


class HostController(rest.RestController):

    def __init__(self, host_id):
        pecan.request.context['host_id'] = host_id
        self._id = host_id

    @pecan.expose("json")
    def get(self):
        """Returns a specific host."""
        host = pecan.request.mongo_connection.shinken.hosts.find_one(
            {"host_name": self._id}
        )
        if host:
            del host['_id']
        return host

    @pecan.expose()
    def put(self):
        """Modify this host."""
        body = json.loads(pecan.request.body.decode())
        pecan.request.mongo_connection.shinken.hosts.update(
            {"host_name": self._id},
            body
        )
        pecan.response.status = 204

    @pecan.expose()
    def delete(self):
        """Delete this host."""
        pecan.request.mongo_connection.shinken.hosts.remove(
            {"host_name": self._id}
        )
        pecan.response.status = 204


class HostsController(rest.RestController):

    @pecan.expose()
    def _lookup(self, host_id, *remainder):
        return HostController(host_id), remainder

    @pecan.expose("json")
    def get_all(self):
        """Returns all host."""
        hosts = [host for host in
                 pecan.request.mongo_connection.shinken.hosts.find()]
        for host in hosts:
            del host['_id']

        return hosts
