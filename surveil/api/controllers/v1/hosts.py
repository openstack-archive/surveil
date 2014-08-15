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


class HostController(rest.RestController):

    def __init__(self, host_id):
        pecan.request.context['host_id'] = host_id
        self._id = host_id

    @pecan.expose()
    def get(self):
        """Returns a specific host """
        return "Returns a specific host: " + self._id


class HostsController(rest.RestController):

    @pecan.expose()
    def _lookup(self, host_id, *remainder):
        return HostController(host_id), remainder

    @pecan.expose()
    def get_all(self):
        """ Returns all host """
        return "Returns all hosts"
