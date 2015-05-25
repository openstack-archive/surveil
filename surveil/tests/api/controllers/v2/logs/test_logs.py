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

import json

import requests_mock

from surveil.tests.api import functionalTest


class TestLogs(functionalTest.FunctionalTest):

    def setUp(self):
        super(TestLogs, self).setUp()
        self.influxdb_response = json.dumps({
            "results": [
                {
                    "series": [
                        {
                            "name": "ALERT",
                            "tags": {
                                "event_type": "ALERT",
                                "host_name": "myServiceIsDown",
                                "service_description": "iAmADownService"
                            },
                            "columns": [
                                "time",
                                "attempts",
                                "output",
                                "state",
                                "state_type",
                                "alert_type"
                            ],
                            "values": [
                                [
                                    "2015-06-04T18:55:12Z",
                                    1,
                                    "Connection refused",
                                    "CRITICAL",
                                    "SOFT",
                                    "SERVICE"
                                ],
                                [
                                    '2015-06-04T18:55:12Z',
                                    2,
                                    'Connection refused',
                                    'CRITICAL',
                                    'SOFT',
                                    'SERVICE'
                                ],
                                [
                                    '2015-06-04T18:55:12Z',
                                    3,
                                    'Connection refused',
                                    'CRITICAL',
                                    'SOFT',
                                    'SERVICE'
                                ]
                            ]
                        },
                        {
                            'name': 'ALERT',
                            'tags': {
                                'event_type': 'ALERT',
                                'host_name': 'savoirfairelinux',
                                'service_description': 'CPU'
                            },
                            'columns': [
                                'time',
                                'attempts',
                                'output',
                                'state',
                                'state_type',
                                'alert_type'
                            ],
                            'values': [
                                [
                                    '2015-06-04T18:55:12Z',
                                    1,
                                    'Warning - Connection refused',
                                    'CRITICAL',
                                    'HARD',
                                    'SERVICE'
                                ],
                                [
                                    '2015-06-04T18:55:12Z',
                                    2,
                                    'Warning - Connection refused',
                                    'WARNING',
                                    'HARD',
                                    'HOST'
                                ]
                            ]
                        },
                        {
                            'name': 'ALERT',
                            'tags': {
                                'event_type': 'NOTIFICATION',
                                'host_name': 'savoirfairelinux',
                                'service_description': 'CPU'
                            },
                            'columns': [
                                'time',
                                'notification_type',
                                'contact',
                                'state',
                                'notification_method',
                                'acknowledgement'
                            ],
                            'values': [
                                [
                                    '2015-06-04T18:55:12Z',
                                    'SERVICE',
                                    'admin',
                                    'CRITICAL',
                                    'notify-service-by-email',
                                    None
                                ],
                                [
                                    '2015-06-04T18:55:12Z',
                                    'SERVICE',
                                    'admin',
                                    'CRITICAL',
                                    'notify-service-by-email',
                                    'ACKNOWLEDGEMENT'
                                ]
                            ]
                        },
                        {
                            'name': 'ALERT',
                            'tags': {
                                'event_type': 'NOTIFICATION',
                                'host_name': 'Google',
                                'service_description': 'Load'
                            },
                            'columns': [
                                'time',
                                'notification_type',
                                'contact',
                                'state',
                                'notification_method',
                                'acknowledgement'
                            ],
                            'values': [
                                [
                                    '2015-06-04T18:55:12Z',
                                    'SERVICE',
                                    'admin',
                                    'CRITICAL',
                                    'notify-service-by-email',
                                    None
                                ]
                            ]
                        }
                    ]
                }
            ]
        })

        self.influxdb_google_response = json.dumps({
            "results": [
                {
                    "series": [
                        {
                            'name': 'ALERT',
                            'tags': {
                                'event_type': 'NOTIFICATION',
                                'host_name': 'Google',
                                'service_description': 'Load'
                            },
                            'columns': [
                                'time',
                                'notification_type',
                                'contact',
                                'state',
                                'notification_method',
                                'acknowledgement'
                            ],
                            'values': [
                                [
                                    '2015-06-04T18:55:12Z',
                                    'SERVICE',
                                    'admin',
                                    'CRITICAL',
                                    'notify-service-by-email',
                                    None
                                ]
                            ]
                        }
                    ]
                }
            ]
        })

        self.expected_values = [
            {
                "host_name": "myServiceIsDown",
                "event_type": "ALERT",
                "service_description": "iAmADownService",
                "time": "2015-06-04T18:55:12Z",
                "attempts": 1,
                "output": "Connection refused",
                "state": "CRITICAL",
                "state_type": "SOFT",
                "alert_type": "SERVICE"
            },
            {
                'host_name': 'myServiceIsDown',
                'event_type': 'ALERT',
                'service_description': 'iAmADownService',
                'time': '2015-06-04T18:55:12Z',
                'attempts': 2,
                'output': 'Connection refused',
                'state': 'CRITICAL',
                'state_type': 'SOFT',
                'alert_type': 'SERVICE'
            },
            {
                'host_name': 'myServiceIsDown',
                'event_type': 'ALERT',
                'service_description': 'iAmADownService',
                'time': '2015-06-04T18:55:12Z',
                'attempts': 3,
                'output': 'Connection refused',
                'state': 'CRITICAL',
                'state_type': 'SOFT',
                'alert_type': 'SERVICE'
            },
            {
                'host_name': 'savoirfairelinux',
                'event_type': 'ALERT',
                'service_description': 'CPU',
                'time': '2015-06-04T18:55:12Z',
                'attempts': 1,
                'output': 'Warning - Connection refused',
                'state': 'CRITICAL',
                'state_type': 'HARD',
                'alert_type': 'SERVICE'
            },
            {
                'host_name': 'savoirfairelinux',
                'event_type': 'ALERT',
                'service_description': 'CPU',
                'time': '2015-06-04T18:55:12Z',
                'attempts': 2,
                'output': 'Warning - Connection refused',
                'state': 'WARNING',
                'state_type': 'HARD',
                'alert_type': 'HOST'
            },
            {
                'host_name': 'savoirfairelinux',
                'event_type': 'NOTIFICATION',
                'service_description': 'CPU',
                'time': '2015-06-04T18:55:12Z',
                'notification_type': 'SERVICE',
                'contact': 'admin',
                'state': 'CRITICAL',
                'notification_method': 'notify-service-by-email'
            },
            {
                'host_name': 'savoirfairelinux',
                'event_type': 'NOTIFICATION',
                'service_description': 'CPU',
                'time': '2015-06-04T18:55:12Z',
                'notification_type': 'SERVICE',
                'contact': 'admin',
                'state': 'CRITICAL',
                'notification_method': 'notify-service-by-email',
                'acknowledgement': 'ACKNOWLEDGEMENT'
            },
            {
                'host_name': 'Google',
                'event_type': 'NOTIFICATION',
                'service_description': 'Load',
                'time': '2015-06-04T18:55:12Z',
                'notification_type': 'SERVICE',
                'contact': 'admin',
                'state': 'CRITICAL',
                'notification_method': 'notify-service-by-email'
            }
        ]

    def test_get_all(self):
        with requests_mock.Mocker() as m:
            m.register_uri(requests_mock.GET,
                           'http://influxdb:8086/query',
                           text=self.influxdb_response)

            response = self.get('/v2/logs')

            self.assert_count_equal_backport(
                json.loads(response.body.decode()),
                self.expected_values
            )

    def test_get_logs_for_host(self):
        with requests_mock.Mocker() as m:
            m.register_uri(requests_mock.GET,
                           'http://influxdb:8086/query',
                           text=self.influxdb_google_response)

            query = {
                'filters': json.dumps({
                    "is": {
                        "host_name": ['Google']
                    }
                })
            }

            response = self.post_json('/v2/logs', params=query)

            self.assertEqual(
                m.last_request.qs['q'],
                ["select * from alert where host_name='google'"]
            )

            self.assert_count_equal_backport(
                json.loads(response.body.decode()),
                [{
                    'host_name': 'Google',
                    'event_type': 'NOTIFICATION',
                    'service_description': 'Load',
                    'time': '2015-06-04T18:55:12Z',
                    'notification_type': 'SERVICE',
                    'contact': 'admin',
                    'state': 'CRITICAL',
                    'notification_method': 'notify-service-by-email'
                }]
            )
