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

import copy
import json

from surveil.api.datamodel.config import service
from surveil.tests.api import functionalTest


class TestServiceController(functionalTest.FunctionalTest):

    def setUp(self):
        super(TestServiceController, self).setUp()
        self.services = [
            {
                "host_name": ["sample-server1"],
                "service_description": "check-",
                "check_command": "check-disk!/dev/sdb1",
                "max_check_attempts": 5,
                "check_interval": 5,
                "retry_interval": 3,
                "check_period": "24x7",
                "notification_interval": 30,
                "notification_period": "24x7",
                "contacts": ["surveil-ptl", "surveil-bob"],
                "contact_groups": ["linux-admins"],
                "use": []
            },
            {
                "host_name": ["sample-server2"],
                "service_description": "check-disk-sdb2",
                "check_command": "check-disk!/dev/sdb1",
                "max_check_attempts": 5,
                "check_interval": 5,
                "retry_interval": 3,
                "check_period": "24x7",
                "notification_interval": 30,
                "notification_period": "24x7",
                "contacts": ["surveil-ptl", "surveil-bob"],
                "contact_groups": ["linux-admins"],
                "use": []
            },
            {
                "host_name": ["sample-server3"],
                "service_description": "check-disk-sdb3",
                "check_command": "check-disk!/dev/sdb1",
                "max_check_attempts": 5,
                "check_interval": 5,
                "retry_interval": 3,
                "check_period": "24x7",
                "notification_interval": 30,
                "notification_period": "24x7",
                "contacts": ["surveil-ptl", "surveil-bob"],
                "contact_groups": ["linux-admins"],
                "use": []
            },
        ]
        self.mongoconnection.shinken.services.insert(
            copy.deepcopy(self.services)
        )

        self.hosts = [
            {"host_name": "sample-server1"}
        ]
        self.mongoconnection.shinken.hosts.insert(
            copy.deepcopy(self.services)
        )

    def test_get_all_services(self):
        response = self.post_json('/v2/config/services', params={})

        self.assert_count_equal_backport(
            json.loads(response.body.decode()),
            self.services
        )
        self.assertEqual(response.status_int, 200)

    def test_get_all_services_templates(self):
        self.mongoconnection.shinken.services.insert(
            copy.deepcopy(
                {"host_name": ["sample-server444"],
                 "service_description": "check-disk-sdb2",
                 "check_command": "check-disk!/dev/sdb1",
                 "max_check_attempts": 5,
                 "check_interval": 5,
                 "retry_interval": 3,
                 "check_period": "24x7",
                 "notification_interval": 30,
                 "notification_period": "24x7",
                 "contacts": ["surveil-ptl", "surveil-bob"],
                 "name": "Template",
                 "register": "0",
                 "contact_groups": ["linux-admins"],
                 "use": []}
            )
        )

        post_lq = {"filters": '{"is":{"register": "0"},'
                              '"defined":{"name": "True"}}'}
        response = self.post_json('/v2/config/services', params=post_lq)

        self.assert_count_equal_backport(
            json.loads(response.body.decode()),
            [{"host_name": ["sample-server444"],
              "service_description": "check-disk-sdb2",
              "check_command": "check-disk!/dev/sdb1",
              "max_check_attempts": 5,
              "check_interval": 5,
              "retry_interval": 3,
              "check_period": "24x7",
              "notification_interval": 30,
              "notification_period": "24x7",
              "contacts": ["surveil-ptl", "surveil-bob"],
              "name": "Template",
              "register": "0",
              "contact_groups": ["linux-admins"],
              "use":[]}]
        )

        response = self.post_json('/v2/config/services', params=post_lq)

        self.assertEqual(
            len(json.loads(response.body.decode())),
            1
        )

        self.assertEqual(response.status_int, 200)

    def test_add_service(self):
        new_service = {
            "host_name": ["sample-server1"],
            "service_description": "check-new-thing",
            "check_command": "check-disk!/dev/sdb1",
            "max_check_attempts": 5,
            "check_interval": 5,
            "retry_interval": 3,
            "check_period": "24x7",
            "notification_interval": 30,
            "notification_period": "24x7",
            "contacts": ["surveil-ptl", "surveil-bob"],
            "contact_groups": ["linux-admins"],
            "use": []
        }
        response = self.put_json(
            "/v2/config/services",
            params=new_service
        )

        services = [service.Service(**s).as_dict() for s in
                    self.mongoconnection.shinken.services.find()]

        self.assertTrue(new_service in services)
        self.assertEqual(response.status_int, 201)
