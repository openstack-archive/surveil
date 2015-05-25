# Copyright 2015 - Savoir-Faire Linux inc.
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

import requests_mock

from surveil.tests.api import functionalTest


class TestAlerts(functionalTest.FunctionalTest):

    def setUp(self):
        super(TestAlerts, self).setUp()
        self.influxdb_response = json.dumps({
            u'results': [
                {
                    u'series': [
                        {
                            u'columns': [
                                u'time',
                                u'attempts',
                                u'contact',
                                u'notification_method',
                                u'notification_type',
                                u'output',
                                u'state',
                                u'state_type',
                                u'alert_type'
                            ],
                            u'name': u'ALERT',
                            u'values': [
                                [u'2015-05-14T14:17:15Z',
                                 None,
                                 None,
                                 None,
                                 None,
                                 u'OK - localhost: rta 0.042ms, lost 0%',
                                 u'UP',
                                 u'HARD',
                                 None],
                                [u'2015-05-14T14:17:56Z',
                                 None,
                                 None,
                                 None,
                                 None,
                                 u'OK - load average: 0.79, 0.50, 0.39',
                                 u'OK',
                                 u'HARD',
                                 None]
                            ]
                        }
                    ]
                }
            ]
        })

    def test_get_alerts(self):
        with requests_mock.Mocker() as m:
            m.register_uri(requests_mock.GET,
                           "http://influxdb:8086/query",
                           text=self.influxdb_response)


            response = self.get('/v2/logs/alerts')

            expected_nb_values = len(json.loads(response.body.decode()))
            self.assertEquals(expected_nb_values, 2)

    def test_get_alert_host(self):
        with requests_mock.Mocker() as m:
            m.register_uri(requests_mock.GET,
                           "http://influxdb:8086/query",
                           text= "")