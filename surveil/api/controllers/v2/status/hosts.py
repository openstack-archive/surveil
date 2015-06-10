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

from surveil.api.controllers.v2 import logs
from surveil.api.datamodel import checkresult
from surveil.api.datamodel.status import live_host
from surveil.api.datamodel.status import live_query
from surveil.api.datamodel.status import live_service
from surveil.api.datamodel.status.metrics import live_metric
from surveil.api.datamodel.status.metrics import time_delta
from surveil.api.handlers.status import live_host_handler
from surveil.api.handlers.status import live_service_handler
from surveil.api.handlers.status.metrics import live_metric_handler
from surveil.common import util


class HostsController(rest.RestController):

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose([live_host.LiveHost])
    def get_all(self):
        """Returns all hosts."""
        handler = live_host_handler.HostHandler(pecan.request)
        hosts = handler.get_all()
        return hosts

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose([live_host.LiveHost], body=live_query.LiveQuery)
    def post(self, query):
        """Given a LiveQuery, returns all matching hosts."""
        handler = live_host_handler.HostHandler(pecan.request)
        hosts = handler.get_all(live_query=query)
        return hosts

    @pecan.expose()
    def _lookup(self, host_name, *remainder):
        return HostController(host_name), remainder


class ConfigController(rest.RestController):

    @util.policy_enforce(['authenticated'])
    @pecan.expose()
    def get_all(self):
        """Returns config from a specific host."""
        return "Dump CONFIG"


class HostServicesController(rest.RestController):

    @pecan.expose()
    def _lookup(self, service_name, *remainder):
        return HostServiceController(service_name), remainder


class HostServiceMetricsController(rest.RestController):

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose([live_metric.LiveMetric])
    def get(self):
        """Returns all metrics name for a host with a service."""
        handler = live_metric_handler.MetricHandler(pecan.request)
        metrics_name = handler.get_metric(
            pecan.request.context['host_name'],
            pecan.request.context['service_name']
        )
        return metrics_name

    @pecan.expose()
    def _lookup(self, metric_name, *remainder):
        return HostServiceMetricController(metric_name), remainder


class HostMetricsController(rest.RestController):

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose([live_metric.LiveMetric])
    def get(self):
        """Returns all metrics name for a host."""
        handler = live_metric_handler.MetricHandler(pecan.request)
        metrics_name = handler.get_metric(pecan.request.context['host_name'])
        return metrics_name

    @pecan.expose()
    def _lookup(self, metric_name, *remainder):
        return HostMetricController(metric_name), remainder


class HostCheckResultsSubController(rest.RestController):

    @util.policy_enforce(['authenticated'])
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


class ServiceCheckResultsSubController(rest.RestController):

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(body=checkresult.CheckResult, status_code=204)
    def post(self, data):
        """Submit a new check result.

        :param data: a check result within the request body.
        """
        result = data.as_dict()
        result['host_name'] = pecan.request.context['host_name']

        result['service_description'] = pecan.request.context[
            'service_name'
        ]

        requests.post(
            pecan.request.ws_arbiter_url + "/push_check_result",
            data=result
        )


class HostServiceController(rest.RestController):

    metrics = HostServiceMetricsController()
    results = ServiceCheckResultsSubController()

    def __init__(self, service_name):
        pecan.request.context['service_name'] = service_name
        self.service_name = service_name

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(live_service.LiveService)
    def get(self):
        """Returns a specific host service."""
        handler = live_service_handler.ServiceHandler(pecan.request)
        service = handler.get(
            pecan.request.context['host_name'],
            self.service_name
        )
        return service


class HostServiceMetricController(rest.RestController):

    def __init__(self, metric_name):
        pecan.request.context['metric_name'] = metric_name
        self.metric_name = metric_name

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(live_metric.LiveMetric)
    def get(self):
        """Return the last measure for the metric name

            of the service name on the host name.
            """
        handler = live_metric_handler.MetricHandler(pecan.request)
        metric = handler.get(
            self.metric_name,
            pecan.request.context['host_name'],
            pecan.request.context['service_name']
        )
        return metric

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose([live_metric.LiveMetric], body=time_delta.TimeDelta)
    def post(self, time):
        """Given a LiveQuery, returns all matching s."""
        handler = live_metric_handler.MetricHandler(pecan.request)
        metrics = handler.get_all(time_delta=time,
                                  metric_name=self.metric_name,
                                  host_name=pecan.request.context['host_name'],
                                  service_description=pecan.request.
                                  context['service_name'])
        return metrics


class HostMetricController(rest.RestController):

    def __init__(self, metric_name):
        pecan.request.context['metric_name'] = metric_name
        self.metric_name = metric_name

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(live_metric.LiveMetric)
    def get(self):
        """Return the last measure for the metric name

        of the service name on the host name
        """
        handler = live_metric_handler.MetricHandler(pecan.request)
        metric = handler.get(
            self.metric_name,
            pecan.request.context['host_name']
        )
        return metric

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose([live_metric.LiveMetric], body=time_delta.TimeDelta)
    def post(self, time):
        """Given a LiveQuery, returns all matching s."""
        handler = live_metric_handler.MetricHandler(pecan.request)
        metrics = handler.get_all(time_delta=time,
                                  metric_name=self.metric_name,
                                  host_name=pecan.request.context['host_name']
                                  )
        return metrics


class HostController(rest.RestController):

    services = HostServicesController()
    # See init for controller creation. We need host_name to instanciate it
    # externalcommands = ExternalCommandsController()
    # config = config.ConfigController()
    events = logs.LogsController()
    metrics = HostMetricsController()
    results = HostCheckResultsSubController()

    def __init__(self, host_name):
        pecan.request.context['host_name'] = host_name
        self.host_name = host_name

    @util.policy_enforce(['authenticated'])
    @wsme_pecan.wsexpose(live_host.LiveHost)
    def get(self):
        """Returns a specific host."""
        handler = live_host_handler.HostHandler(pecan.request)
        host = handler.get(self.host_name)
        return host
