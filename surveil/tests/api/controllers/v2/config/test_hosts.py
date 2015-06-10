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

from surveil.api.datamodel.config import host
from surveil.api.datamodel.config import service
from surveil.tests.api import functionalTest


class TestHostController(functionalTest.FunctionalTest):

    def setUp(self):
        super(TestHostController, self).setUp()
        self.hosts = [
            {
                "host_name": "bogus-router", "address": "192.168.1.254",
                "max_check_attempts": 5, "check_period": "24x7",
                "contacts": "admin,carl", "contact_groups": "router-admins",
                "notification_interval": 30, "notification_period": "24x7",
                "_CRITICAL": "10"
            },
            {
                "host_name": "bogus-router2", "address": "192.168.1.254",
                "max_check_attempts": 5, "check_period": "24x7",
                "contacts": "admin,carl", "contact_groups": "router-admins",
                "notification_interval": 30, "notification_period": "24x7"
            },
            {
                "host_name": "bogus-router333", "address": "192.168.1.254",
                "max_check_attempts": 5, "check_period": "24x7",
                "contacts": "admin,carl", "contact_groups": "router-admins",
                "notification_interval": 30, "notification_period": "24x7",
                'use': 'test'
            },
        ]
        self.mongoconnection.shinken.hosts.insert(
            copy.deepcopy(self.hosts)
        )

        self.services = [
            {
                "host_name": "bogus-router",
                "service_description": "service-example",
                "check_command": "check-disk!/dev/sdb1",
                "max_check_attempts": 5,
                "check_interval": 5,
                "retry_interval": 3,
                "check_period": "24x7",
                "notification_interval": 30,
                "notification_period": "24x7",
                "contacts": "surveil-ptl,surveil-bob",
                "contact_groups": "linux-admins"
            }
        ]
        self.mongoconnection.shinken.services.insert(
            copy.deepcopy(self.services)
        )

    def test_get_all_hosts(self):
        response = self.get('/v2/config/hosts')

        # Adjust self.host content to reflect custom_fields sub-dict
        c_fields = {}
        for h in self.hosts:
            if '_CRITICAL' in h.keys():
                c_fields['_CRITICAL'] = h['_CRITICAL']
                h.pop('_CRITICAL')
                h['custom_fields'] = c_fields

        self.assert_count_equal_backport(
            json.loads(response.body.decode()),
            self.hosts
        )
        self.assertEqual(response.status_int, 200)

    def test_get_all_hosts_no_templates(self):
        self.mongoconnection.shinken.hosts.insert(
            copy.deepcopy(
                {"host_name": "bogus-router", "address": "192.168.1.254",
                 "max_check_attempts": 5, "check_period": "24x7",
                 "contacts": "admin,carl", "contact_groups": "router-admins",
                 "notification_interval": 30, "notification_period": "24x7",
                 "register": "0"}
            )
        )
        response = self.get('/v2/config/hosts')

        # Adjust self.host content to reflect custom_fields sub-dict
        c_fields = {}
        for h in self.hosts:
            if '_CRITICAL' in h.keys():
                c_fields['_CRITICAL'] = h['_CRITICAL']
                h.pop('_CRITICAL')
                h['custom_fields'] = c_fields

        self.assert_count_equal_backport(
            json.loads(response.body.decode()),
            self.hosts
        )
        self.assertEqual(response.status_int, 200)

    def test_get_specific_host(self):
        response = self.get('/v2/config/hosts/bogus-router333')

        self.assert_count_equal_backport(
            json.loads(response.body.decode()),
            self.hosts[2]
        )
        self.assertEqual(response.status_int, 200)

    def test_get_specific_host_custom_field(self):
        response = self.get('/v2/config/hosts/bogus-router')
        my_host = json.loads(response.body.decode())

        self.assertIn("custom_fields", my_host.keys())
        self.assertNotIn("_CRITICAL", my_host.keys())
        self.assertIsNone(my_host.get("_CRITICAL"))

    def test_update_host(self):
        put_host = {
            u'host_name': u'bogus-router333',
            u'contacts': u'newcontacts',
        }
        response = self.put_json(
            "/v2/config/hosts/bogus-router333", params=put_host
        )

        mongo_host = host.Host(
            **self.mongoconnection.shinken.hosts.find_one(
                {'host_name': 'bogus-router333'}, {'_id': 0}
            )
        )

        expected = {
            'address': u'192.168.1.254',
            'check_period': u'24x7',
            'notification_interval': 30,
            'contacts': u'newcontacts',
            'notification_period': u'24x7',
            'contact_groups': u'',
            'host_name': u'bogus-router333',
            'max_check_attempts': 3,
            'use': u'test'
        }

        self.assertEqual(expected, mongo_host.as_dict())
        self.assertEqual(response.status_int, 204)

    def test_delete_host(self):
        response = self.delete('/v2/config/hosts/bogus-router')

        mongo_hosts = [host.Host(**h) for h
                       in self.mongoconnection.shinken.hosts.find()]

        self.assertEqual(2, len(mongo_hosts))
        self.assertEqual(response.status_int, 204)

    def test_add_host(self):
        new_host = {
            "host_name": "testpost",
            "address": "192.168.1.254",
            "max_check_attempts": 5,
            "check_period": "24x7",
            "contacts": "admin,carl",
            "contact_groups": "router-admins",
            "notification_interval": 3,
            "notification_period": "24x7"
        }
        response = self.post_json("/v2/config/hosts", params=new_host)

        hosts = [host.Host(**h).as_dict() for h
                 in self.mongoconnection.shinken.hosts.find(None, {'_id': 0})]

        self.assertTrue(new_host in hosts)
        self.assertEqual(response.status_int, 201)

    def test_add_host_custom_fields(self):
        my_host = {
            "host_name": "custom_field_host", "address": "192.168.1.254",
            "max_check_attempts": 5, "check_period": "24x7",
            "contacts": "admin,carl", "contact_groups": "router-admins",
            "notification_interval": 30, "notification_period": "24x7",
            "_TEST_CUSTOM_FIELD": "10"
        }

        self.mongoconnection.shinken.hosts.insert(my_host)
        mongo_host = self.mongoconnection.shinken.hosts.find_one(
            {"host_name": "custom_field_host"}
        )
        # In-MongoDB representation should hold custom fields similarly to
        # Shinken:
        #
        # define host {
        #       _CUSTOM     value
        # }
        # (no "custom_fields" sub-dict)
        self.assertNotIn("custom_fields", mongo_host.keys())
        self.assertIn("_TEST_CUSTOM_FIELD", mongo_host.keys())
        self.assertIsNotNone(mongo_host["_TEST_CUSTOM_FIELD"])

    def test_post_add_host_custom_fields(self):
        my_host = {
            "host_name": "custom_field_host", "address": "192.168.1.254",
            "max_check_attempts": 5, "check_period": "24x7",
            "contacts": "admin,carl", "contact_groups": "router-admins",
            "notification_interval": 30, "notification_period": "24x7",
            "custom_fields": {
                "_TEST_CUSTOM_FIELD": "10"
            }
        }

        self.post_json('/v2/config/hosts', my_host)
        mongo_host = self.mongoconnection.shinken.hosts.find_one(
            {"host_name": "custom_field_host"}
        )
        # In-MongoDB representation should hold custom fields similarly to
        # Shinken:
        #
        # define host {
        #       _CUSTOM     value
        # }
        # (no "custom_fields" sub-dict)
        self.assertNotIn("custom_fields", mongo_host.keys())
        self.assertIn("_TEST_CUSTOM_FIELD", mongo_host.keys())
        self.assertIsNotNone(mongo_host["_TEST_CUSTOM_FIELD"])

    def test_get_associated_services(self):
        response = self.get('/v2/config/hosts/bogus-router/services')

        self.assertEqual(
            self.services,
            json.loads(response.body.decode())
        )

    def test_get_specific_service(self):
        response = self.get(
            '/v2/config/hosts/bogus-router/services/service-example'
        )

        self.assertEqual(
            self.services[0],
            json.loads(response.body.decode())
        )

    def test_delete_specific_service(self):
        mongo_services = [service.Service(**h) for h
                          in self.mongoconnection.shinken.services.find()]
        self.assertEqual(1, len(mongo_services))

        self.delete(
            '/v2/config/hosts/bogus-router/services/service-example'
        )

        mongo_services = [service.Service(**h) for h
                          in self.mongoconnection.shinken.services.find()]

        self.assertEqual(0, len(mongo_services))
