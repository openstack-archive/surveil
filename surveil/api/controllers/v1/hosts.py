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
import requests
import wsmeext.pecan as wsme_pecan

from surveil.api.controllers.v1.datamodel import checkresult
from surveil.api.controllers.v1.datamodel import host
from surveil.api.controllers.v1.datamodel import service


class ServiceCheckResultsSubController(rest.RestController):

    @wsme_pecan.wsexpose(body=checkresult.CheckResult, status_code=204)
    def post(self, data):
        """Submit a new check result.

        :param data: a check result within the request body.
        """
        result = data.as_dict()
        result['host_name'] = pecan.request.context['host_name']

        result['service_description'] = pecan.request.context[
            'service_description'
        ]

        requests.post(
            pecan.request.ws_arbiter_url + "/push_check_result",
            data=result
        )


class HostServiceSubController(rest.RestController):
    results = ServiceCheckResultsSubController()

    def __init__(self, service_description):
        pecan.request.context['service_description'] = service_description
        self._id = service_description

    @wsme_pecan.wsexpose(service.Service)
    def get(self):
        """Returns a specific service."""
        mongo_s = pecan.request.mongo_connection.shinken.services.find_one(
            {
                "host_name": pecan.request.context['host_name'],
                "service_description": pecan.request.context[
                    'service_description'
                ]
            }
        )

        return service.Service(**mongo_s)


class HostServicesSubController(rest.RestController):

    @wsme_pecan.wsexpose([service.Service])
    def get_all(self):
        """Returns all services assocaited with this host."""
        mongo_s = [
            s for s
            in pecan.request.mongo_connection.shinken.services.find(
                {"host_name": pecan.request.context['host_name']}
            )
        ]

        services = [service.Service(**s) for s in mongo_s]

        return services

    @pecan.expose()
    def _lookup(self, service_description, *remainder):
        return HostServiceSubController(service_description), remainder


class HostCheckResultsSubController(rest.RestController):

    @wsme_pecan.wsexpose(body=checkresult.CheckResult, status_code=204)
    def post(self, data):
        """Submit a new check result.

        :param data: a check result within the request body.
        """
        result = data.as_dict()
        result['host_name'] = pecan.request.context['host_name']

        requests.post(
            pecan.request.ws_arbiter_url + "/push_check_result",
            data=result
        )


class HostSubController(rest.RestController):
    services = HostServicesSubController()
    results = HostCheckResultsSubController()


class HostController(rest.RestController):

    def __init__(self, host_name):
        pecan.request.context['host_name'] = host_name
        self._id = host_name

    @wsme_pecan.wsexpose(host.Host)
    def get(self):
        """Returns a specific host."""
        h = pecan.request.mongo_connection.shinken.hosts.find_one(
            {"host_name": self._id}, {'_id': 0}
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

    @pecan.expose()
    def _lookup(self, *remainder):
        return HostSubController(), remainder


class HostsController(rest.RestController):

    @pecan.expose()
    def _lookup(self, host_name, *remainder):
        return HostController(host_name), remainder

    @wsme_pecan.wsexpose([host.Host])
    def get_all(self):
        """Returns all hosts."""
        hosts = [h for h
                 in pecan.request.mongo_connection.
                 shinken.hosts.find(
                     {"register": {"$ne": "0"}},  # Don't return templates
                     {'_id': 0}
                 )]

        return [host.Host(**h) for h in hosts]

    @wsme_pecan.wsexpose(host.Host, body=host.Host, status_code=201)
    def post(self, data):
        """Create a new host.

        :param data: a host within the request body.
        """
        pecan.request.mongo_connection.shinken.hosts.insert(
            data.as_dict()
        )
