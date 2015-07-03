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


class TestHostMetric(functionalTest.FunctionalTest):

    def setUp(self):
        super(TestHostMetric, self).setUp()
        self.influxdb_response = json.dumps({
            "results": [
                {
                    "series": [
                        {"name": "metric_load1",
                         "tags": {"host_name": "srv-monitoring-01",
                                  "service_description": "load",
                                  },
                         "columns": [
                             "time",
                             "critical",
                             "min",
                             "value",
                             "warning"
                         ],
                         "values": [
                             ["2015-04-19T01:09:24Z",
                              "30",
                              "0",
                              "0.60",
                              "15"]
                         ]},
                        {"name": "metric_load1",
                         "tags": {"host_name": "test_keystone",
                                  "service_description": "unload"},
                         "columns": [
                             "time",
                             "critical",
                             "min",
                             "value",
                             "warning"
                         ],
                         "values": [
                             ["2015-04-19T01:09:23Z",
                              "60",
                              "0",
                              "1.5",
                              "20"]
                         ]},
                        {"name": "metric_load1",
                         "tags": {"host_name": "ws-arbiter",
                                  },
                         "columns": [
                             "time",
                             "critical",
                             "min",
                             "value",
                             "warning"
                         ],
                         "values": [
                             ["2015-04-19T01:09:24Z",
                              "20",
                              "0",
                              "6",
                              "10"],
                         ]}
                    ]
                }
            ]
        })

    def test_get(self):
        """Test get all metric names for a service."""
        influxdb_response = json.dumps({
            "results": [
                {
                    "series": [
                        {
                            "name": "measurements",
                            "columns": ["name"],
                            "values": [
                                    ["metric_rtmin"],
                                    ["ALERT"]
                            ]
                        }
                    ]
                }
            ]
        })
        with requests_mock.Mocker() as m:
            m.register_uri(requests_mock.GET,
                           "http://influxdb:8086/query",
                           text=influxdb_response)

            response = self.get(
                "/v2/status/hosts/localhost/services/load/metrics"
            )

            expected = [{"metric_name": "rtmin"}, ]

            self.assert_count_equal_backport(
                json.loads(response.body.decode()),
                expected)
            self.assertEqual(
                m.last_request.qs['q'],
                ["show measurements where host_name='localhost' "
                 "and service_description='load'"]
            )

    def test_get_metric_name(self):
        """Test get the last measure for a metric within a service."""
        self.influxdb_response = json.dumps({
            "results": [
                {
                    "series": [
                        {
                            "name": "measurements",
                            "columns": ["name"],
                            "values": [
                                ["metric_rtmin"],
                                ["ALERT"]
                            ]
                        }
                    ]
                }
            ]
        })
        with requests_mock.Mocker() as m:
            m.register_uri(requests_mock.GET,
                           "http://influxdb:8086/query",
                           text=self.influxdb_response)

            response = self.get(
                "/v2/status/hosts/ws-arbiter/services/load/metrics"
            )

            expected = [{"metric_name": "rtmin"}, ]

            self.assert_count_equal_backport(
                json.loads(response.body.decode()),
                expected)
            self.assertEqual(
                m.last_request.qs['q'],
                ["show measurements where host_name='ws-arbiter' "
                 "and service_description='load'"]
            )

    def test_post_live_query(self):
        """Test posting a live query."""
        self.influxdb_response = json.dumps({
            "results": [
                {
                    "series": [
                        {"name": "metric_load1",
                         "tags": {"host_name": "srv-monitoring-01",
                                  "service_description": "load"},
                         "columns": ["time",
                                     "critical",
                                     "min",
                                     "value",
                                     "warning",
                                     ],
                         "values": [["2015-04-19T01:09:24Z",
                                     "30",
                                     "0",
                                     "0.6",
                                     "15"],
                                    ["2015-04-19T01:09:25Z",
                                     "40",
                                     "4",
                                     "10",
                                     "10"]]}]}]

        })

        with requests_mock.Mocker() as m:
            m.register_uri(requests_mock.GET,
                           "http://influxdb:8086/query",
                           text=self.influxdb_response)

            query = {
                'fields': [],
                'time_interval': {
                    'start_time': '2015-04-19T00:09:24Z',
                    'end_time': '2015-04-19T02:09:25Z'
                }
            }

            response = self.post_json("/v2/status/hosts/srv-monitoring-01/"
                                      "services/load/metrics/load1",
                                      params=query)

            expected = [{"metric_name": 'load1',
                         "min": "0",
                         "critical": "30",
                         "warning": "15",
                         "value": "0.6"
                         },
                        {"metric_name": 'load1',
                         "min": "4",
                         "critical": "40",
                         "warning": "10",
                         "value": "10"
                         }]

            self.assertEqual(
                m.last_request.qs['q'],
                ["select * from metric_load1 "
                 "where time >= '2015-04-19t00:09:24z' "
                 "and time <= '2015-04-19t02:09:25z' "
                 "and host_name='srv-monitoring-01' "
                 "and service_description='load' "
                 "order by time desc"
                 ]
            )
            self.assert_count_equal_backport(
                json.loads(response.body.decode()),
                expected)
