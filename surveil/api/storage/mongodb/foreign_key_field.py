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

import mongoengine


def validate_refering_object_exists(referring_object, field_name, value):
    if referring_object.objects(**{field_name: value}).count() < 1:
            return False
    return True


class ForeignKeyStringField(mongoengine.StringField):

    def __init__(self, referring_object,
                 referring_object_field_name,
                 *args,
                 **kwargs):
        super(ForeignKeyStringField, self).__init__(*args, **kwargs)
        self.refering_object = referring_object
        self.refering_object_field_name = referring_object_field_name

    def validate(self, value):
        mongoengine.StringField.validate(self, value)

        if validate_refering_object_exists(self.refering_object,
                                           self.refering_object_field_name,
                                           value) is False:
            self.error(
                "Could not find matching %s" % value
            )


class ForeignKeyListField(mongoengine.ListField):
    def __init__(self, referring_object,
                 referring_object_field_name,
                 *args,
                 **kwargs):
        super(ForeignKeyListField, self).__init__(*args, **kwargs)
        self.refering_object = referring_object
        self.refering_object_field_name = referring_object_field_name

    def validate(self, value):
        mongoengine.ListField.validate(self, value)

        for key in value:
            if validate_refering_object_exists(self.refering_object,
                                               self.refering_object_field_name,
                                               key) is False:
                self.error(
                "Could not find matching %s" % key
                )