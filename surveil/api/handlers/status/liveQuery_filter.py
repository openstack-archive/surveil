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
            fields = json.loads(live_query.fields)
            matching_item = {}
            for field in fields:
                matching_item[field] = item[field]

            matching_items.append(matching_item)

    return matching_items
