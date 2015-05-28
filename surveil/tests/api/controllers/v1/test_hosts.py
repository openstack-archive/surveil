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

import requests_mock
from six.moves import urllib_parse

from surveil.api.controllers.v1.datamodel import host
from surveil.tests.api import functionalTest


class TestHostController(functionalTest.FunctionalTest):

    def setUp(self):
        super(TestHostController, self).setUp()
        self.hosts = [
            {
                "host_name": "bogus-router", "address": "192.168.1.254",
                "max_check_attempts": 5, "check_period": "24x7",
                "contacts": "admin,carl", "contact_groups": "router-admins",
                "notification_interval": 30, "notification_period": "24x7"
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
                "notification_interval": 30, "notification_period": "24x7"
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
        response = self.app.get('/v1/hosts')

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
        response = self.app.get('/v1/hosts')

        self.assert_count_equal_backport(
            json.loads(response.body.decode()),
            self.hosts
        )
        self.assertEqual(response.status_int, 200)

    def test_get_specific_host(self):
        response = self.app.get('/v1/hosts/bogus-router333')

        self.assert_count_equal_backport(
            json.loads(response.body.decode()),
            self.hosts[2]
        )
        self.assertEqual(response.status_int, 200)

    def test_update_host(self):
        put_host = {
            u"host_name": u"bogus-router333",
            u"address": u"newputaddress",
            u"max_check_attempts": 222225,
            u"check_period": u"newtimeperiod",
            u"contacts": u"aaa,bbb",
            u"contact_groups": u"newgroup",
            u"notification_interval": 333,
            u"notification_period": u"newnotificationperiod"
        }
        response = self.app.put_json(
            "/v1/hosts/bogus-router333", params=put_host
        )

        mongo_host = host.Host(
            **self.mongoconnection.shinken.hosts.find_one(
                {'host_name': 'bogus-router333'}, {'_id': 0}
            )
        )

        self.assertEqual(put_host, mongo_host.as_dict())
        self.assertEqual(response.status_int, 204)

    def test_delete_host(self):
        response = self.app.delete('/v1/hosts/bogus-router')

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
        response = self.app.post_json("/v1/hosts", params=new_host)

        hosts = [host.Host(**h).as_dict() for h
                 in self.mongoconnection.shinken.hosts.find(None, {'_id': 0})]

        self.assertTrue(new_host in hosts)
        self.assertEqual(response.status_int, 201)

    def test_get_associated_services(self):
        response = self.app.get('/v1/hosts/bogus-router/services')

        self.assertEqual(
            self.services,
            json.loads(response.body.decode())
        )

    def test_get_specific_service(self):
        response = self.app.get(
            '/v1/hosts/bogus-router/services/service-example'
        )

        self.assertEqual(
            self.services[0],
            json.loads(response.body.decode())
        )

    def test_submit_service_result(self):
        with requests_mock.Mocker() as m:
            m.register_uri(requests_mock.POST,
                           self.ws_arbiter_url + "/push_check_result")

            check_result = {
                "return_code": "0",
                "output": "TEST OUTPUT",
                "time_stamp": "1409149234"
            }

            response = self.app.post_json(
                "/v1/hosts/bogus-router/services/service-example/results",
                params=check_result
            )

            self.assertEqual(response.status_int, 204)
            self.assertEqual(
                urllib_parse.parse_qs(m.last_request.body),
                {
                    u'output': [u'TEST OUTPUT'],
                    u'return_code': [u'0'],
                    u'service_description': [u'service-example'],
                    u'host_name': [u'bogus-router'],
                    u'time_stamp': [u'1409149234']
                }
            )

    def test_submit_host_result(self):
        with requests_mock.Mocker() as m:
            m.register_uri(requests_mock.POST,
                           self.ws_arbiter_url + "/push_check_result")

            check_result = {
                "return_code": "0",
                "output": "TEST OUTPUT",
                "time_stamp": "1409149234"
            }

            response = self.app.post_json("/v1/hosts/bogus-router/results",
                                          params=check_result)

            self.assertEqual(response.status_int, 204)
            self.assertEqual(
                urllib_parse.parse_qs(m.last_request.body),
                {
                    u'output': [u'TEST OUTPUT'],
                    u'return_code': [u'0'],
                    u'host_name': [u'bogus-router'],
                    u'time_stamp': [u'1409149234']
                }
            )
