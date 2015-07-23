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

import mongoengine


class Service(mongoengine.Document):
    meta = {
        'collection': 'services',
        'strict': False
    }
    host_name = mongoengine.StringField()
    service_description = mongoengine.StringField()
    contacts = mongoengine.StringField()
    check_command = mongoengine.StringField()
    max_check_attempts = mongoengine.IntField()
    check_interval = mongoengine.IntField()
    retry_interval = mongoengine.IntField()
    check_period = mongoengine.StringField()
    notification_interval = mongoengine.IntField()
    notification_period = mongoengine.StringField()
    contact_groups = mongoengine.StringField()
    passive_checks_enabled = mongoengine.StringField()
    use = mongoengine.StringField()
    name = mongoengine.StringField()
    register = mongoengine.StringField()