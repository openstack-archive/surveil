# Copyright 2014 - Savoir-Faire Linux inc.
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


def build_influxdb_query(metric_name,
                         time_delta,
                         host_name=None,
                         service_description=None
                         ):
    group_by = []
    query = ['SELECT * FROM metric_%s'
             % metric_name]
    begin = time_delta.begin
    end = time_delta.end
    query.append("WHERE time >= '%s' AND time <= '%s'" % (begin, end))

    if host_name is None:
        group_by.append('host_name')
    else:
        query.append("AND host_name ='%s'" % host_name)

    if service_description is None:
        group_by.append('service_description')
    else:
        query.append("AND service_description ='%s'" % service_description)

    if len(group_by) != 0:
        query.append('GROUP BY')
        query.append(', '.join(group_by))

    query.append('ORDER BY time DESC')
    return ' '.join(query)