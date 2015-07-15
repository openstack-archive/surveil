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

import functools
import json


def build_influxdb_query(live_query,
                         measurement,
                         group_by=[],
                         order_by=[],
                         additional_filters={},
                         limit=None,
                         multiple_series=False):
    query = ['SELECT * FROM', measurement]

    filters = {}
    time = None
    offset = None
    if live_query:
        if live_query.filters:
            filters.update(json.loads(live_query.filters))
        if live_query.time_interval:
            time = live_query.time_interval
        if live_query.paging:
            if multiple_series:
                limit = live_query.paging.size * (live_query.paging.page + 1)
            else:
                limit = live_query.paging.size
                offset = (live_query.paging.page + 1) * live_query.paging.size

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

    if offset is not None:
        query.append('OFFSET %d' % offset)

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


def paging(response, datamodel, live_query=None):
    """Paging function

    :param response: a python-influxdb resulset
    :param datamodel: an Surveil API datamodel class
    :param live_query: an influxdb_query
    :return: a dict of datamodel object. If the live query contain paging,
    the dict is sorted by datamodel time attribute and contain
    live_query.paging.size object for the live_query.paging.page page
    """
    if live_query and live_query.paging:
        limit_paging = live_query.paging.size * (live_query.paging.page + 1)
        limit = live_query.paging.size + live_query.paging.page
        offset_paging = live_query.paging.page * live_query.paging.size

        def sort_by_time(init, point_tag):
            event = {}
            event.update(point_tag[0])
            event.update(point_tag[1])
            init.append(datamodel(**event))
            init.sort(key=lambda event: event.time,
                      reverse=True)
            return init[:limit_paging]

        response = [(tag[1], _dict_from_influx_item(datamodel, point))
                    for tag, points in response.items()
                    for point in points]

        event_list = functools.reduce(sort_by_time, response, [])

        return event_list[offset_paging:limit+1]

    else:
        events = []

        for item in response.items():
            tags = item[0][1]
            for point in response.get_points(tags=tags):
                point.update(tags)
                event_dict = _dict_from_influx_item(datamodel, point)
                events.append(datamodel(**event_dict))

        return events


def _dict_from_influx_item(datamodel, item):
    """Create a dict representing a python-influxdb item

    :param item: an python influxdb item object
    :param datamodel: an Surveil API datamodel class
    :return: a dict (datamodel_attribute:item_value)

    >>> _event_dict_from_influx_item(Event, {"time": 4})
    {'time': 4}
    >>> _event_dict_from_influx_item(Event, {"time": "null"})
    {}
    """

    fields = [attr.name for attr in getattr(datamodel, "_wsme_attributes")]
    return dict([(field, item.get(field, None)) for field in fields
                 if item.get(field, None) is not None])
