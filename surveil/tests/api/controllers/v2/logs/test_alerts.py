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

import copy
import json
import httpretty

from surveil.tests.api import functionalTest


class TestAlertsController(functionalTest.FunctionalTest):

    def setUp(self):
        super(TestAlertsController, self).setUp()
        self.alerts_request = json.dumps({
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

    @httpretty.activate
    def test_get_all_alerts(self):
        httpretty.register_uri(httpretty.GET,
                               "http://influxdb:8086/query",
                               body=self.alerts_request)

        response = self.get('/v2/logs/alerts')
        resp_data = json.loads(response.body)

        self.assertEquals(len(resp_data), 2)