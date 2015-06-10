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

from surveil.api.datamodel.config import host
from surveil.api.datamodel.config import service
from surveil.api.handlers.config import host_handler
from surveil.api.handlers.config import service_handler
from surveil.common import util


class HostServiceSubController(rest.RestController):

    def __init__(self, service_description):
        pecan.request.context['service_description'] = service_description
        self._id = service_description

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(service.Service)
    def get(self):
        """Returns a specific service."""
        handler = service_handler.ServiceHandler(pecan.request)
        s = handler.get(
            pecan.request.context['host_name'],
            pecan.request.context['service_description']
        )
        return s

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(None, status_code=204)
    def delete(self):
        """Delete a specific service."""
        handler = service_handler.ServiceHandler(pecan.request)
        handler.delete(
            pecan.request.context['host_name'],
            pecan.request.context['service_description']
        )


class HostServicesSubController(rest.RestController):

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose([service.Service])
    def get_all(self):
        """Returns all services assocaited with this host."""
        handler = service_handler.ServiceHandler(pecan.request)
        services = handler.get_all(
            host_name=pecan.request.context['host_name']
        )
        return services

    @pecan.expose()
    def _lookup(self, service_description, *remainder):
        return HostServiceSubController(service_description), remainder


class HostSubController(rest.RestController):
    services = HostServicesSubController()


class HostController(rest.RestController):

    def __init__(self, host_name):
        pecan.request.context['host_name'] = host_name
        self._id = host_name

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(host.Host)
    def get(self):
        """Returns a specific host."""
        handler = host_handler.HostHandler(pecan.request)
        h = handler.get(self._id)
        return h

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(None, body=host.Host, status_code=204)
    def put(self, data):
        """Modify this host.

        :param data: a host within the request body.
        """
        handler = host_handler.HostHandler(pecan.request)
        handler.update(self._id, data)

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(None, status_code=204)
    def delete(self):
        """Delete this host."""
        handler = host_handler.HostHandler(pecan.request)
        handler.delete(self._id)

    @pecan.expose()
    def _lookup(self, *remainder):
        return HostSubController(), remainder


class HostsController(rest.RestController):

    @pecan.expose()
    def _lookup(self, host_name, *remainder):
        return HostController(host_name), remainder

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose([host.Host])
    def get_all(self):
        """Returns all hosts."""
        handler = host_handler.HostHandler(pecan.request)
        hosts = handler.get_all()
        return hosts

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(host.Host, body=host.Host, status_code=201)
    def post(self, data):
        """Create a new host.

        :param data: a host within the request body.
        """
        handler = host_handler.HostHandler(pecan.request)
        handler.create(data)
