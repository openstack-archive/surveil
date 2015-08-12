# Copyright 2015 - Savoir-Faire Linux inc.
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


def build_mongodb_query(live_query):
    query = []
    kwargs = {}

    #  Build the filters
    filters = {}
    for filter_name, filter_data in live_query.get('filters', {}).items():
        for field, values in filter_data.items():
            filters[field] = {
                _get_mongo_filter(filter_name): values
            }

    search = live_query.get('search', None)
    if search:
        filters["$text"] = {"$search": search}

    if filters:
        query.append(filters)

    #  Build the required fields
    fields = {}
    for field in live_query.get("fields", []):
        fields[field] = 1

    if fields:
        query.append(fields)

    # Paging
    paging = live_query.get('paging', None)
    if paging is not None:
        kwargs['limit'] = paging.size
        kwargs['skip'] = paging.size * paging.page

    return query, kwargs


def _get_mongo_filter(livequery_filter):
    filters = {
        "is": "$in",
        "isnot": "$nin"
    }
    return filters[livequery_filter]


def translate_live_query(live_query, mappings):
    """Translate field names in a live query so that they match mongodb."""

    #  Load the fields
    fields = live_query.get("fields", [])

    #  Translate the fields
    translated_fields = []
    for field in fields:
        translated_fields.append(mappings.get(field, field))
    live_query["fields"] = translated_fields

    #  Load the filters
    filters = json.loads(live_query.get("filters", '{}'))

    #  Translate the filters
    for filter in filters.values():
        for field in filter.keys():
            value = filter.pop(field)
            filter[mappings.get(field, field)] = value
    live_query["filters"] = filters

    return live_query