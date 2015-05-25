# Copyright 2015 - Savoir-Faire Linux inc.
#
# Licensed under the Apache License, Version 2.0 (the 'License'); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import json

import requests_mock

from surveil.tests.api import functionalTest


class TestLogs(functionalTest.FunctionalTest):

    def setUp(self):
        super(TestLogs, self).setUp()
        self.influxdb_response = json.dumps({
            'results': [
                {
                    'series': [
                        {
                            'name': 'ALERT',
                            'columns': [
                                'time',
                                'notification_type',
                                'event_type',
                                'contact',
                                'host_name',
                                'service_description',
                                'state',
                                'notification_method',
                                'output',
                                'alert_type',
                                'state_type',
                                'attempts',
                                'downtime_type'
                            ],
                            'values': [
                                [
                                    '2015-06-04T18:55:12Z',
                                    'HOST',
                                    'NOTIFICATION',
                                    'Aviau',
                                    'Localhost',
                                    None,
                                    'CRITICAL',
                                    'notify-service-by-email',
                                    'OK - localhost: rta 0.064ms, lost 0%'
                                ],
                                [
                                    '2015-06-07T18:55:18Z',
                                    None,
                                    'ALERT',
                                    None,
                                    'savoirfairelinux.com',
                                    None,
                                    'WARNING',
                                    None,
                                    'Warning: savoirfairelinux.com is not responding'
                                    'SOFT',
                                    ''
                                    '[Errno -2] Name or service not known',
                                    'CRITICAL',
                                    'SOFT',
                                    None
                                ],
                                [
                                    '2015-06-04T18:55:18Z',
                                    None,
                                    None,
                                    'notify via email',
                                    'email',
                                    '[Errno -2] Name or service not known',
                                    'CRITICAL',
                                    'SOFT',
                                    None
                                ],
                                [
                                    '2015-06-04T18:55:12Z',
                                    'HOST',
                                    'NOTIFICATION',
                                    None,
                                    'google.com',
                                    'load',
                                    'CRITICAL',
                                    None,
                                    'Load: high usage 95%'
                                ],
                                [
                                    '2015-06-04T18:55:18Z',
                                    3,
                                    None,
                                    None,
                                    None,
                                    '[Errno -2] Name or service not known',
                                    'CRITICAL',
                                    'SOFT',
                                    'host'
                                ]
                            ]
                        }
                    ]
                }
            ]
        })

        self.expected_values = [
            {
                'time': '2015-06-04T18:55:12Z',
                'attempts': 4,
                'contact': 'Aviau',
                'output': 'OK - localhost: rta 0.064ms, lost 0%',
                'state': 'UP',
                'state_type': 'HARD'
            },
            {
                'time': '2015-06-04T18:55:18Z',
                'notification_method': 'notify via email',
                'notification_type': 'email',
                'output': '[Errno -2] Name or service not known',
                'state': 'CRITICAL',
                'state_type': 'SOFT'
            },
            {
                'time': '2015-06-04T18:55:18Z',
                'attempts': 3,
                'output': '[Errno -2] Name or service not known',
                'state': 'CRITICAL',
                'state_type': 'SOFT',
                'alert_type': 'host'
            }
        ]

    def test_get_alerts(self):
        with requests_mock.Mocker() as m:
            m.register_uri(requests_mock.GET,
                           'http://influxdb:8086/query',
                           text=self.influxdb_response)

            response = self.get('/v2/logs/alerts')

            self.assert_count_equal_backport(
                json.loads(response.body.decode()),
                self.expected_values
            )

    def test_get_alerts_for_host(self):
        with requests_mock.Mocker() as m:
            m.register_uri(requests_mock.GET,
                           'http://influxdb:8086/query',
                           text=self.influxdb_response)

            response = self.get('/v2/logs/alerts/srv-monitoring-01')

            for alert in self.expected_values:
                alert['host_name'] = 'srv-monitoring-01'

            self.assert_count_equal_backport(
                json.loads(response.body.decode()),
                self.expected_values
            )
