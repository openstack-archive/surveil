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

import pecan
from pecan import rest
import wsmeext.pecan as wsme_pecan

from surveil.api.controllers.v1.datamodel import host


class HostController(rest.RestController):

    def __init__(self, host_id):
        pecan.request.context['host_id'] = host_id
        self._id = host_id

    @wsme_pecan.wsexpose(host.Host)
    def get(self):
        """Returns a specific host."""
        h = pecan.request.mongo_connection.shinken.hosts.find_one(
            {"host_name": self._id}
        )
        return host.Host(**h)

    @wsme_pecan.wsexpose(None, body=host.Host, status_code=204)
    def put(self, data):
        """Modify this host.

        :param data: a host within the request body.
        """

        host_dict = data.as_dict()
        if "host_name" not in host_dict.keys():
            host_dict['host_name'] = self._id

        pecan.request.mongo_connection.shinken.hosts.update(
            {"host_name": self._id},
            host_dict
        )

    @wsme_pecan.wsexpose(None, status_code=204)
    def delete(self):
        """Delete this host."""
        pecan.request.mongo_connection.shinken.hosts.remove(
            {"host_name": self._id}
        )


class HostsController(rest.RestController):

    @pecan.expose()
    def _lookup(self, host_id, *remainder):
        return HostController(host_id), remainder

    @wsme_pecan.wsexpose([host.Host])
    def get_all(self):
        """Returns all hosts."""
        hosts = [h for h
                 in pecan.request.mongo_connection.shinken.hosts.find()]

        return [host.Host(**h) for h in hosts]

    @wsme_pecan.wsexpose(host.Host, body=host.Host, status_code=201)
    def post(self, data):
        """Create a new host.

        :param data: a host within the request body.
        """
        pecan.request.mongo_connection.shinken.hosts.insert(
            data.as_dict()
        )