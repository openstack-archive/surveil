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

import wsme


def filter_fields(item_list, live_query):
    """Takes unwanted keys out of a dict depending on a live_query."""
    filtered_items = []

    if live_query.fields != wsme.Unset:
        fields = live_query.fields
        for item in item_list:
            filtered_item = {}
            for field in fields:
                filtered_item[field] = item.get(field, None)
            filtered_items.append(filtered_item)
    else:
        filtered_items = item_list

    return filtered_items
