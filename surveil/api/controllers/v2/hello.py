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

from surveil.common import util


class HelloController(rest.RestController):

    @pecan.expose()
    @util.policy_enforce(['pass'])
    def get(self):
        """Says hello."""
        return "Hello World!"

    @pecan.expose()
    def _lookup(self, *remainder):
        return HelloSubController(), remainder


class AdminController(rest.RestController):

    @pecan.expose()
    @util.policy_enforce(['admin'])
    def get(self):
        """Says hello to the admin."""
        return "Hello, dear admin!"


class DeniedController(rest.RestController):

    @pecan.expose()
    @util.policy_enforce(['break'])
    def get(self):
        """This should be denied."""
        return "Looks like policies are not working."


class HelloSubController(rest.RestController):
    admin = AdminController()
    denied = DeniedController()
