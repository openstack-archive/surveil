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
                "host_name": "bogus-router",
                "address": "192.168.1.254",
                "max_check_attempts": 5,
                "check_period": "24x7",
                "contacts": ["admin", "carl"],
                "contact_groups": ["router-admins"],
                "notification_interval": 30,
                "notification_period": "24x7",
                "custom_fields": {},
                "use": []
            },
            {
                "host_name": "bogus-router2",
                "address": "192.168.1.254",
                "max_check_attempts": 5,
                "check_period": "24x7",
                "contacts": ["admin", "carl"],
                "contact_groups": ["router-admins"],
                "notification_interval": 30,
                "notification_period": "24x7",
                "custom_fields": {},
                "use": []
            },
            {
                "host_name": "bogus-router333",
                "address": "192.168.1.254",
                "max_check_attempts": 5,
                "check_period": "24x7",
                "contacts": ["admin", "carl"],
                "contact_groups": ["router-admins"],
                "notification_interval": 30,
                "notification_period": "24x7",
                'use': ['test'],
                "custom_fields": {},
                "use": []
            },
        ]
        self.mongoconnection.shinken.hosts.insert(
            copy.deepcopy(self.hosts)
        )

        self.services = [
            {
                "host_name": ["bogus-router"],
                "service_description": "service-example",
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
        ]
        self.mongoconnection.shinken.services.insert(
            copy.deepcopy(self.services)
        )

    def test_get_all_hosts(self):
        response = self.post_json('/v2/config/hosts', params={})

        self.assert_count_equal_backport(
            json.loads(response.body.decode()),
            self.hosts
        )
        self.assertEqual(response.status_int, 200)

    def test_get_all_hosts_paging(self):
        response = self.post_json(
            '/v2/config/hosts',
            params={"paging": {"page": 2, "size": 1}}
        )

        hosts = json.loads(response.body.decode())

        self.assertEqual(
            hosts,
            [self.hosts[2]]
        )

    def test_get_all_hosts_templates(self):
        self.mongoconnection.shinken.hosts.insert(
            copy.deepcopy(
                {"host_name": "bogus-router345345",
                 "address": "192.168.1.254",
                 "max_check_attempts": 5,
                 "check_period": "24x7",
                 "contacts": ["admin", "carl"],
                 "contact_groups": ["router-admins"],
                 "notification_interval": 30,
                 "notification_period": "24x7",
                 "name": "Template",
                 "register": "0",
                 "custom_fields": {},
                 "use": []}
            )
        )
        post_lq = {"filters": '{"is":{"register": "0"},'
                              '"defined":{"name": "True"}}'}
        response = self.post_json('/v2/config/hosts', params=post_lq)

        self.assert_count_equal_backport(
            json.loads(response.body.decode()),
            [{"host_name": "bogus-router345345",
              "address": "192.168.1.254",
              "max_check_attempts": 5,
              "check_period": "24x7",
              "contacts": ["admin", "carl"],
              "contact_groups": ["router-admins"],
              "notification_interval": 30,
              "notification_period": "24x7",
              "name": "Template",
              "register": "0",
              "custom_fields": {},
              "use": []}]
        )

        response = self.post_json('/v2/config/hosts',  params=post_lq)
        self.assertEqual(
            len(json.loads(response.body.decode())),
            1
        )

        self.assertEqual(response.status_int, 200)

    def test_get_specific_host(self):
        response = self.get('/v2/config/hosts/bogus-router333')

        self.assert_count_equal_backport(
            json.loads(response.body.decode()),
            self.hosts[2]
        )
        self.assertEqual(response.status_int, 200)

    def test_update_host(self):
        put_host = {
            u'host_name': u'bogus-router333',
            u'contacts': [u'newcontacts'],
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
            'contacts': [u'newcontacts'],
            'notification_period': u'24x7',
            'contact_groups': [u'router-admins'],
            'host_name': u'bogus-router333',
            'max_check_attempts': 5,
            'use': [],
            'custom_fields': {},
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
            "contacts": ["admin", "carl"],
            "contact_groups": ["router-admins"],
            "notification_interval": 3,
            "notification_period": "24x7",
            "custom_fields": {},
            "use": []
        }
        response = self.put_json("/v2/config/hosts", params=new_host)

        hosts = [host.Host(**h).as_dict() for h
                 in self.mongoconnection.shinken.hosts.find(None, {'_id': 0})]

        self.assertTrue(new_host in hosts)
        self.assertEqual(response.status_int, 201)

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
