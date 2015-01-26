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


from surveil.api.controllers.v1.datamodel import host
from surveil.tests import base


class TestHostDataModel(base.BaseTestCase):

    def test_host_as_and_from_dict(self):
        h = host.Host(
            host_name="bogus-router",
            address="192.168.1.254",
            max_check_attempts=5,
            check_period="24x7",
            contacts="admin,carl",
            contact_groups="router-admins",
            notification_interval=30,
            notification_period="24x7",
            custom_fields={"_OS_AUTH_URL": "http://localhost:8080/v2"}
        )

        h_dict = {'check_period': u'24x7', 'notification_interval': 30,
                  'contacts': u'admin,carl', 'notification_period': u'24x7',
                  'contact_groups': u'router-admins',
                  'host_name': u'bogus-router', 'address': u'192.168.1.254',
                  'max_check_attempts': 5,
                  '_OS_AUTH_URL': 'http://localhost:8080/v2'}

        self.assertEqual(h.as_dict(), h_dict)
        self.assertEqual(h_dict, host.Host(**h_dict).as_dict())
