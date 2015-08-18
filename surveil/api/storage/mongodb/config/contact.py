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


class Contact(mongoengine.Document):
    meta = {'collection': 'contacts'}
    contact_name = mongoengine.StringField(unique=True)
    host_notifications_enabled = mongoengine.IntField()
    service_notifications_enabled = mongoengine.IntField()
    host_notification_period = mongoengine.StringField()
    service_notification_period = mongoengine.StringField()
    host_notification_options = mongoengine.ListField()
    service_notification_options = mongoengine.ListField()
    host_notification_commands = mongoengine.ListField()
    service_notification_commands = mongoengine.ListField()
    email = mongoengine.StringField()
    pager = mongoengine.StringField()
    can_submit_commands = mongoengine.IntField()
    is_admin = mongoengine.IntField()
    retain_status_information = mongoengine.IntField()
    retain_nonstatus_information = mongoengine.IntField()
    min_business_impact = mongoengine.IntField()

