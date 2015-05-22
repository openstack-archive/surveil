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


from surveil.api.datamodel.status.metrics import time_delta
from surveil.api.handlers.status.metrics import influxdb_time_query
from surveil.tests import base


class InfluxdbTimeQueryTest(base.BaseTestCase):
    def test_build_query_basic(self):
        query_time = time_delta.TimeDelta(begin='2015-01-29T21:50:44Z',
                                          end='2015-01-29T22:50:44Z', )
        query_metric_name = 'pl'

        result = influxdb_time_query.build_influxdb_query(query_metric_name,
                                                          query_time
                                                          )
        expected = ("SELECT * "
                    "FROM metric_pl "
                    "WHERE time >= '2015-01-29T21:50:44Z' "
                    "AND time <= '2015-01-29T22:50:44Z' "
                    "GROUP BY host_name, "
                    "service_description ORDER BY time DESC")

        self.assert_count_equal_backport(result, expected)

    def test_build_query_host_name(self):
        query_time = time_delta.TimeDelta(begin='2015-01-29T21:50:44Z',
                                          end='2015-01-29T22:50:44Z', )
        query_metric_name = 'pl'
        query_host_name = 'localhost'

        result = influxdb_time_query.build_influxdb_query(query_metric_name,
                                                          query_time,
                                                          query_host_name
                                                          )
        expected = ("SELECT * "
                    "FROM metric_pl "
                    "WHERE time >= '2015-01-29T21:50:44Z' "
                    "AND time <= '2015-01-29T22:50:44Z' "
                    "AND host_name ='localhost' "
                    "GROUP BY service_description "
                    "ORDER BY time DESC")

        self.assert_count_equal_backport(result, expected)

    def test_build_query_complete(self):
        query_time = time_delta.TimeDelta(begin='2015-01-29T21:50:44Z',
                                          end='2015-01-29T22:50:44Z', )
        query_metric_name = 'pl'
        query_host_name = 'localhost'
        query_service_description = 'mySQL'

        result = influxdb_time_query.build_influxdb_query(
            query_metric_name,
            query_time,
            query_host_name,
            query_service_description
        )
        expected = ("SELECT * "
                    "FROM metric_pl "
                    "WHERE time >= '2015-01-29T21:50:44Z' "
                    "AND time <= '2015-01-29T22:50:44Z' "
                    "AND host_name ='localhost' "
                    "AND service_description ='mySQL' "
                    "ORDER BY time DESC")

        self.assert_count_equal_backport(result, expected)