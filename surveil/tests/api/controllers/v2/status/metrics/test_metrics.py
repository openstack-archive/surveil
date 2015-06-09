# Copyright 2015 - Savoir-Faire Linux inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import json

import requests_mock

from surveil.tests.api import functionalTest


class TestMetrics(functionalTest.FunctionalTest):
    def setUp(self):
        super(TestMetrics, self).setUp()
        self.influxdb_response = json.dumps({"results": [{"series": [
            {"name": "ALERT",
             "columns": ["_key", "event_type", "host_name",
                         "service_desc", "service_description"],
             "values": [["ALERT,host_name=srv-monitoring-01", "",
                         "srv-monitoring-01", "", ""],
                        ["ALERT,host_name=test_keystone",
                         "", "test_keystone", "", ""],
                        ["ALERT,host_name=sw-iwebcore-01",
                         "", "sw-iwebcore-01", "", ""],
                        ["ALERT,host_name=ws-arbiter,"
                         "service_description=check-ws-arbiter",
                         "", "ws-arbiter", "", "check-ws-arbiter"],
                        ["ALERT,host_name=openstackceilometer-host",
                         "", "openstackceilometer-host", "", ""],
                        ["ALERT,host_name=srv-ldap-01",
                         "", "srv-ldap-01", "", ""],
                        ["ALERT,host_name=myserviceisdown",
                         "", "myserviceisdown", "", ""],
                        ["ALERT,host_name=srv-apache-01",
                         "", "srv-apache-01", "", ""],
                        ["ALERT,event_type=ALERT,host_name=myserviceisdown,"
                         "service_desc=iamadownservice",
                         "ALERT", "myserviceisdown", "iamadownservice", ""],
                        ["ALERT,host_name=myserviceisdown,"
                         "service_description=iamadownservice",
                         "", "myserviceisdown", "", "iamadownservice"],
                        ["ALERT,host_name=myparentisdown",
                         "", "myparentisdown", "", ""],
                        ["ALERT,host_name=google.com",
                         "", "google.com", "", ""],
                        ["ALERT,event_type=ALERT,host_name=test_keystone,"
                         "service_desc=Check\\ KeyStone\\ service.",
                         "ALERT", "test_keystone",
                         "Check KeyStone service.", ""],
                        ["ALERT,host_name=test_keystone,"
                         "service_description=Check\\ KeyStone\\ service.", "",
                         "test_keystone", "", "Check KeyStone service."],
                        ["ALERT,host_name=localhost",
                         "", "localhost", "", ""],
                        ["ALERT,host_name=ws-arbiter",
                         "", "ws-arbiter", "", ""]]},
            {"name": "HOST_STATE",
             "columns": ["_key", "host_name"],
             "values": [["HOST_STATE,host_name=srv-monitoring-01",
                         "srv-monitoring-01"],
                        ["HOST_STATE,host_name=test_keystone",
                         "test_keystone"],
                        ["HOST_STATE,host_name=sw-iwebcore-01",
                         "sw-iwebcore-01"],
                        ["HOST_STATE,host_name=openstackceilometer-host",
                         "openstackceilometer-host"],
                        ["HOST_STATE,host_name=srv-ldap-01",
                         "srv-ldap-01"],
                        ["HOST_STATE,host_name=myserviceisdown",
                         "myserviceisdown"],
                        ["HOST_STATE,host_name=srv-apache-01",
                         "srv-apache-01"],
                        ["HOST_STATE,host_name=myparentisdown",
                         "myparentisdown"],
                        ["HOST_STATE,host_name=google.com",
                         "google.com"],
                        ["HOST_STATE,host_name=localhost",
                         "localhost"],
                        ["HOST_STATE,host_name=ws-arbiter",
                         "ws-arbiter"]]},
            {"name": "SERVICE_STATE",
             "columns": ["_key", "host_name", "service_description"],
             "values": [
                 ["SERVICE_STATE,host_name=ws-arbiter,"
                  "service_description=check-ws-arbiter",
                  "ws-arbiter", "check-ws-arbiter"],
                 ["SERVICE_STATE,host_name=myserviceisdown,"
                  "service_description=iamadownservice",
                  "myserviceisdown", "iamadownservice"],
                 ["SERVICE_STATE,host_name=test_keystone,"
                  "service_description=Check\\ KeyStone\\ service.",
                  "test_keystone", "Check KeyStone service."]]},
            {"name": "metric_pl",
             "columns": ["_key", "host_name"],
             "values": [["metric_pl,host_name=test_keystone",
                         "test_keystone"],
                        ["metric_pl,host_name=sw-iwebcore-01",
                         "sw-iwebcore-01"],
                        ["metric_pl,host_name=srv-ldap-01",
                         "srv-ldap-01"],
                        ["metric_pl,host_name=myserviceisdown",
                         "myserviceisdown"],
                        ["metric_pl,host_name=localhost",
                         "localhost"],
                        ["metric_pl,host_name=ws-arbiter",
                         "ws-arbiter"]]},
            {"name": "metric_rta",
             "columns": ["_key", "host_name"],
             "values": [["metric_rta,host_name=test_keystone",
                         "test_keystone"],
                        ["metric_rta,host_name=sw-iwebcore-01",
                         "sw-iwebcore-01"],
                        ["metric_rta,host_name=srv-ldap-01",
                         "srv-ldap-01"],
                        ["metric_rta,host_name=myserviceisdown",
                         "myserviceisdown"],
                        ["metric_rta,host_name=localhost",
                         "localhost"],
                        ["metric_rta,host_name=ws-arbiter",
                         "ws-arbiter"]]},
            {"name": "metric_rtmax",
             "columns": ["_key", "host_name"],
             "values": [["metric_rtmax,host_name=test_keystone",
                         "test_keystone"],
                        ["metric_rtmax,host_name=sw-iwebcore-01",
                         "sw-iwebcore-01"],
                        ["metric_rtmax,host_name=srv-ldap-01",
                         "srv-ldap-01"],
                        ["metric_rtmax,host_name=myserviceisdown",
                         "myserviceisdown"],
                        ["metric_rtmax,host_name=localhost",
                         "localhost"],
                        ["metric_rtmax,host_name=ws-arbiter",
                         "ws-arbiter"]]},
            {"name": "metric_rtmin",
             "columns": ["_key", "host_name"],
             "values": [["metric_rtmin,host_name=test_keystone",
                         "test_keystone"],
                        ["metric_rtmin,host_name=sw-iwebcore-01",
                         "sw-iwebcore-01"],
                        ["metric_rtmin,host_name=srv-ldap-01",
                         "srv-ldap-01"],
                        ["metric_rtmin,host_name=myserviceisdown",
                         "myserviceisdown"],
                        ["metric_rtmin,host_name=localhost",
                         "localhost"],
                        ["metric_rtmin,host_name=ws-arbiter",
                         "ws-arbiter"]]},
            {"name": "metric_time",
             "columns": ["_key", "host_name", "service_description"],
             "values": [
                 ["metric_time,host_name=ws-arbiter,"
                  "service_description=check-ws-arbiter",
                  "ws-arbiter", "check-ws-arbiter"]]}]}]})

    def test_get_metric_hosts(self):
        with requests_mock.Mocker() as m:
            m.register_uri(requests_mock.GET,
                           "http://influxdb:8086/query",
                           text=self.influxdb_response)
            response = self.get("/v2/status/metrics")
            print(json.loads(response.body.decode()))
            self.assert_count_equal_backport(
                json.loads(response.body.decode()),
                [{'metric_name': 'pl'}, {'metric_name': 'rta'},
                 {'metric_name': 'rtmax'}, {'metric_name': 'rtmin'},
                 {'metric_name': 'time'}])