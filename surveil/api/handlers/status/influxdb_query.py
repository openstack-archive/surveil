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


def build_influxdb_query(live_query,
                         measurement,
                         group_by=[],
                         order_by=[],
                         limit=None):

    query = ['SELECT * FROM', measurement]

    if live_query:
        filters = json.loads(live_query.filters)
        if filters:
            query.append(_build_where_clause(filters))

    if group_by:
        query.append('GROUP BY')
        query.append(', '.join(group_by))

    if order_by:
        query.append('ORDER BY')
        query.append(', '.join(order_by))

    if limit is not None:
        query.append('LIMIT %d' % limit)

    return ' '.join(query)


def _build_where_clause(filters):
    filters_conversion = {
        'is': '=',
        'isnot': '!='
    }
    clause = []
    first = True

    for filter_name, filter_data in sorted(filters.items()):
        for field, values in sorted(filter_data.items()):
            for value in values:
                if first:
                    clause.append('WHERE')
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
                first = False

    return ' '.join(clause)
