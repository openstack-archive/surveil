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


class MetricsController(rest.RestController):

    @util.policy_enforce(['authenticated'])
    @pecan.expose()
    def get_all(self):
        """Returns all metrics."""
        host_name = pecan.request.context.get("host_name")
        if host_name is not None:
            return '{"host_name": "%s",  "metrics" : "22"}' % host_name

        return '{"host_name": "NOHOSTNAME",  "metrics" : "22"}'

    @util.policy_enforce(['authenticated'])
    @pecan.expose()
    def _lookup(self, *args):
        props = {}
        leftovers = list(args)
        # print leftovers
        for attr in ["host_name", "service_description", "metric"]:
            value = pecan.request.context.get(attr)
            if value is not None:
                props[attr] = value
            else:
                if len(leftovers) > 0:
                    props[attr] = leftovers[0]
                    leftovers.pop(0)
                else:
                    props[attr] = None

        return MetricController(**props), leftovers


class MetricController(rest.RestController):

    def __init__(self, host_name, service_description=None, metric=None):
        self._id = host_name
        self.sd = service_description
        self.metric = metric

    @util.policy_enforce(['authenticated'])
    @pecan.expose()
    def get(self):
        """Returns (specific) metrics."""

        output = '{"hn": %s, "sd": %s, "metric":%s}' % (
                 self._id, self.sd, self.metric)

        return output