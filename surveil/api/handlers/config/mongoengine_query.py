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

import mongoengine

from surveil.api.storage.mongodb import foreign_key_field


def build_mongoengine_query(live_query, resource_storage):

    query = mongoengine.Q()

    # Filters
    if live_query.filters and json.loads(live_query.filters).items():
        for filter_name, filter_data in json.loads(live_query.filters).items():
            for field, value in filter_data.items():
                qobj = mongoengine.Q(
                    **_get_mongoengine_filter(field,
                                              filter_name,
                                              value)
                )
                query = query & qobj

    # search
    if live_query.search:
        search_q = None

        string_fields = [
            field for field in resource_storage._fields
            if isinstance(
                getattr(resource_storage, field),
                (
                    mongoengine.StringField,
                    mongoengine.ListField,
                    foreign_key_field.ForeignKeyListField,
                    foreign_key_field.ForeignKeyListField
                )
            )
        ]

        for field in string_fields:
            field_q = mongoengine.Q(
                __raw__={
                    field: {"$regex": ".*%s.*" % live_query.search,
                            "$options": "-i"}
                }
            )

            if search_q is None:
                search_q = field_q
            else:
                search_q = search_q | field_q

        query = query & search_q

    # Fields
    fields = []
    if live_query.fields:
        for field in live_query.fields:
            fields.append(field)

    # Paging
    skip = None
    limit = None
    if live_query.paging:
        skip = live_query.paging.size * live_query.paging.page
        limit = skip + live_query.paging.size

    return fields, query, skip, limit


def _get_mongoengine_filter(field_name, filter_name, value):
    filters = {
        "is": field_name + "__in",
        "isnot": field_name + "__nin",
        "defined": field_name + "__exists"
    }
    return {filters[filter_name]: value}