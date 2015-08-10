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


def build_mongoengine_query(live_query):

    #  Build the filters
    query = {}
    kwargs = None
    fields = []

    if live_query.fields:
        for field in live_query.fields:
            fields.append(field)

    if live_query.filters and json.loads(live_query.filters).items():
        for filter_name, filter_data in json.loads(live_query.filters).items():
            for field, value in filter_data.items():
                query.update(_get_mongoengine_filter(field,
                                                     filter_name,
                                                     value))

    live_query.paging
    if live_query.paging:
        paging = live_query.paging
        skip = paging.size * paging.page
        limit = skip + paging.size
        kwargs = slice(skip, limit)
    else:
        kwargs = slice(None, None)
    return fields, query, kwargs


def _get_mongoengine_filter(field_name, filter_name, value):
    filters = {
        "is": field_name + "__in",
        "isnot": field_name + "__nin",
        "defined": field_name + "__exists"
    }
    return {filters[filter_name]: value}