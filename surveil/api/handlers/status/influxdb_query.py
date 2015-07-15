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

import functools
import json
import time

from surveil.api.datamodel.status import event


def build_influxdb_query(live_query,
                         measurement,
                         group_by=[],
                         order_by=[],
                         additional_filters={},
                         limit=None):
    query = ['SELECT * FROM', measurement]

    filters = {}
    time = None
    if live_query:
        if live_query.filters:
            filters.update(json.loads(live_query.filters))
        if live_query.time_interval:
            time = live_query.time_interval
        if live_query.paging:
            limit = live_query.paging.size

    filters.update(additional_filters)
    query += _build_where_clause(filters, time)

    if group_by:
        query.append('GROUP BY')
        query.append(', '.join(group_by))

    if order_by:
        query.append('ORDER BY')
        query.append(', '.join(order_by))

    if limit is not None:
        query.append('LIMIT %d' % limit)

    return ' '.join(query)


def _build_where_clause(filters, time=None):
    filters_conversion = {
        'is': '=',
        'isnot': '!='
    }
    clause = []
    is_where_append = False

    if time:
        clause.append('WHERE')
        clause.append("time >= '%s' AND time <= '%s'" %
                      (time.start_time, time.end_time))
        is_where_append = True

    for filter_name, filter_data in sorted(filters.items()):
        for field, values in sorted(filter_data.items()):
            for value in values:
                if not is_where_append:
                    clause.append('WHERE')
                    is_where_append = True
                else:
                    clause.append('AND')

                if type(value) == int:
                    clause.append("%s%s%d" % (field,
                                              filters_conversion[filter_name],
                                              value))
                else:
                    clause.append("%s%s'%s'" %
                                  (field,
                                   filters_conversion[filter_name],
                                   value))

    return clause


def paging(response, live_query=None):

    if live_query and live_query.paging:
        paging = live_query.paging.size
        tag_list = enumerate(response.keys())

        def sort_by_time(init, serie):

            tag = next(tag_list)
            host_name = tag[1][1]['host_name']
            service_description = tag[1][1]['service_description']
            event_type = tag[1][1]['event_type']

            for point in serie:
                event_dict = _event_dict_from_influx_item(point)
                ts = time.strptime(event_dict['time'][:-1],
                                   '%Y-%m-%dT%H:%M:%S')
                event_dict['timestamp'] = time.mktime(ts)

                if host_name is not '':
                    event_dict['host_name'] = host_name

                if service_description is not '':
                    event_dict['service_description'] = service_description

                if event_type is not '':
                    event_dict['event_type'] = event_type

                init.append(event_dict)

            init = sorted(init, key=lambda event: event.get('timestamp'),
                          reverse=True)
            return init[:paging]

        resp_list = functools.reduce(sort_by_time, response, [])

        event_list = []

        for resp in resp_list:
            del resp['timestamp']
            event_list.append(event.Event(**resp))

        return event_list

    else:
        events = []

        for item in response.items():
            tags = item[0][1]
            for point in response.get_points(tags=tags):
                point.update(tags)
                event_dict = _event_dict_from_influx_item(point)
                events.append(event.Event(**event_dict))

        return events


def _event_dict_from_influx_item(item):
    mappings = [
        'time',
        'event_type',
        'host_name',
        'service_description',
        'state',
        'state_type',
        'attempts',
        'downtime_type',
        'notification_type',
        'notification_method',
        'contact',
        'alert_type',
        'output',
        'acknowledgement'
    ]

    event_dict = {}

    for field in mappings:
        value = item.get(field, None)
        if value is not None and value != "null":
            event_dict[field] = value

    return event_dict