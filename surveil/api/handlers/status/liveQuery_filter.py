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

import wsme


def filter_dict_list_with_live_query(item_list, live_query):
    filters = json.loads(live_query.filters)

    matching_items = []

    for item in item_list:
        matches = True

        # Filters are, for example, 'isnot' or 'is'
        for filter in filters.items():

            # Fields are, for example, 'STATE'
            for field in filter[1].items():

                # Values are, for example, 0, 1, UP, Down...
                for value in field[1]:

                    if filter[0] == "isnot":
                        if item[field[0]] == value:
                            matches = False
                            break
                    elif filter[0] == "is":
                        if item[field[0]] != value:
                            matches = False
                            break

        if matches:
            matching_item = {}
            if live_query.fields != wsme.Unset:
                fields = json.loads(live_query.fields)
                for field in fields:
                    matching_item[field] = item[field]
            else:
                matching_item = item
            matching_items.append(matching_item)

    return matching_items


def build_influxdb_query(live_query, measurement, group_by=[], limit=None):

    query = ['SELECT * FROM', measurement]

    if group_by:
        query.append('GROUP BY')
        query.append(', '.join(group_by))

    if limit is not None:
        query.append('LIMIT %d' % limit)

    if live_query:
        filters = json.loads(live_query.filters)
        if filters:
            query.append(_build_where_clause(filters))

    return ' '.join(query)


def _build_where_clause(filters):
    """
    {
        "is": {
            "state": [0],
            "description": ["test_keystone"]
        }
    }
    """
    filters_conversion = {
        'is': '=',
        'isnot': '!='
    }
    clause = []
    first = True

    for filter_name, filter_data in filters.items():
        for field, values in filter_data.items():
            for value in values:
                if first:
                    clause.append('WHERE')
                else:
                    clause.append('AND')

                if type(value) == int:
                    clause.append("%s%s%d" % (field, filters_conversion[filter_name], value))
                else:
                    clause.append("%s%s'%s'" % (field, filters_conversion[filter_name], value))
                first = False

    return ' '.join(clause)
