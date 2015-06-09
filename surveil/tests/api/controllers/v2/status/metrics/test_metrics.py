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
        self.influxdb_response = json.dumps({"results":[{"series":[{"name":"ALERT","columns":["_id","event_type","host_name","service_desc","service_description"],"values":[[1,"ALERT","srv-apache-01","memory",""],[2,"","srv-apache-01","","memory"],[3,"ALERT","srv-monitoring-01","cpu",""],[4,"","srv-monitoring-01","","cpu"],[5,"","srv-monitoring-01","","users"],[6,"ALERT","srv-apache-01","swap",""],[7,"","srv-apache-01","","swap"],[8,"ALERT","srv-monitoring-01","disk",""],[9,"","srv-monitoring-01","","disk"],[16,"ALERT","srv-apache-01","_self_",""],[17,"","srv-apache-01","",""],[18,"","srv-monitoring-01","",""],[29,"","myserviceisdown","",""],[35,"","test_keystone","",""],[41,"","srv-ldap-01","",""],[43,"ALERT","openstackceilometer-host","_self_",""],[44,"","openstackceilometer-host","",""],[50,"","localhost","",""],[52,"ALERT","test_keystone","Check KeyStone service.",""],[53,"","test_keystone","","Check KeyStone service."]]},{"name":"HOST_STATE","columns":["_id","host_name"],"values":[[19,"srv-apache-01"],[20,"srv-monitoring-01"],[30,"myserviceisdown"],[36,"test_keystone"],[42,"srv-ldap-01"],[45,"openstackceilometer-host"],[51,"localhost"]]},{"name":"SERVICE_STATE","columns":["_id","host_name","service_description"],"values":[[10,"srv-apache-01","memory"],[11,"srv-monitoring-01","cpu"],[12,"srv-monitoring-01","users"],[13,"srv-apache-01","swap"],[14,"srv-monitoring-01","disk"],[54,"test_keystone","Check KeyStone service."]]},{"name":"metric_pl","columns":["_id","host_name"],"values":[[24,"srv-monitoring-01"],[28,"myserviceisdown"],[34,"test_keystone"],[40,"srv-ldap-01"],[49,"localhost"]]},{"name":"metric_rta","columns":["_id","host_name"],"values":[[22,"srv-monitoring-01"],[26,"myserviceisdown"],[32,"test_keystone"],[38,"srv-ldap-01"],[47,"localhost"]]},{"name":"metric_rtmax","columns":["_id","host_name"],"values":[[23,"srv-monitoring-01"],[27,"myserviceisdown"],[33,"test_keystone"],[39,"srv-ldap-01"],[48,"localhost"]]},{"name":"metric_rtmin","columns":["_id","host_name"],"values":[[21,"srv-monitoring-01"],[25,"myserviceisdown"],[31,"test_keystone"],[37,"srv-ldap-01"],[46,"localhost"]]},{"name":"metric_users","columns":["_id","host_name","service_description"],"values":[[15,"srv-monitoring-01","users"]]}]}]})

    def test_get_metric_hosts(self):
        with requests_mock.Mocker() as m:
            m.register_uri(requests_mock.GET,
                           "http://influxdb:8086/query",
                           text=self.influxdb_response)
        response = self.get("/v2/status/metrics/")
        print(response)