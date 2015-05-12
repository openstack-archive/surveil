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

import copy
import json


from surveil.tests.api import functionalTest


class TestNotificationWayController(functionalTest.FunctionalTest):

    def setUp(self):
        super(TestNotificationWayController, self).setUp()
        self.notificationway = [
            {
                'notificationway_name': 'email_in_day',
                'host_notification_period': '24x7',
                'service_notification_period': '24x7',
                'host_notification_options': 'd,u',
                'service_notification_options': 'w,c,r',
                'host_notification_commands': 'notify-service',
                'service_notification_commands': 'notify-host'
            },
            {
                'notificationway_name': 'email_all_time',
                'host_notification_period': '24x7',
                'service_notification_period': '24x7',
                'host_notification_options': 'd,r,f,u',
                'service_notification_options': 'w,f,c,r',
                'host_notification_commands': 'notify-service',
                'service_notification_commands': 'notify-host',
                'min_business_impact': 5
            }
        ]
        self.mongoconnection.shinken.notificationways.insert(
            copy.deepcopy(self.notificationway)
        )

    def test_get_all_notificationways(self):
        response = self.get('/v2/config/notificationways')

        self.assert_count_equal_backport(
            json.loads(response.body.decode()),
            [
                {
                    'notificationway_name': 'email_in_day',
                    'host_notification_period': '24x7',
                    'service_notification_period': '24x7',
                    'host_notification_options': 'd,u',
                    'service_notification_options': 'w,c,r',
                    'host_notification_commands': 'notify-service',
                    'service_notification_commands': 'notify-host'
                },
                {
                    'notificationway_name': 'email_all_time',
                    'host_notification_period': '24x7',
                    'service_notification_period': '24x7',
                    'host_notification_options': 'd,r,f,u',
                    'service_notification_options': 'w,f,c,r',
                    'host_notification_commands': 'notify-service',
                    'service_notification_commands': 'notify-host',
                    'min_business_impact': 5
                }
            ]
        )
        self.assertEqual(response.status_int, 200)

    def test_get_one_notificationway(self):
        response = self.get('/v2/config/notificationways/email_all_time')

        self.assertEqual(
            json.loads(response.body.decode()),
            {
                'notificationway_name': 'email_all_time',
                'host_notification_period': '24x7',
                'service_notification_period': '24x7',
                'host_notification_options': 'd,r,f,u',
                'service_notification_options': 'w,f,c,r',
                'host_notification_commands': 'notify-service',
                'service_notification_commands': 'notify-host',
                'min_business_impact': 5
            }
        )

    def test_create_notificationway(self):
        notificationway = {
            'notificationway_name': 'test_create_notification',
            'host_notification_period': '24x7',
            'service_notification_period': '24x7',
            'host_notification_options': 'd,r,f,u',
            'service_notification_options': 'w,f,c,r',
            'host_notification_commands': 'notify-service',
            'service_notification_commands': 'notify-host',
            'min_business_impact': 5
        }

        self.post_json('/v2/config/notificationways', notificationway)

        self.assertIsNotNone(
            self.mongoconnection.
            shinken.notificationways.find_one(notificationway)
        )

    def test_delete_notificationway(self):
        notificationway = {
            'notificationway_name': 'email_all_time',
        }

        self.assertIsNotNone(
            self.mongoconnection.shinken.notificationways.find_one(
                notificationway
            )
        )

        self.delete('/v2/config/notificationways/email_all_time')

        self.assertIsNone(
            self.mongoconnection.shinken.notificationways.find_one(
                notificationway
            )
        )

    def test_put_notificationway(self):
        self.assertEqual(
            self.mongoconnection.shinken.notificationways.find_one(
                {'notificationway_name': 'email_all_time'}
            )['min_business_impact'],
            5
        )

        self.put_json(
            '/v2/config/notificationways/email_all_time',
            {
                'notificationway_name': 'email_all_time',
                'host_notification_period': '24x7',
                'service_notification_period': '24x7',
                'host_notification_options': 'd,r,f,u',
                'service_notification_options': 'w,f,c,r',
                'host_notification_commands': 'notify-service',
                'service_notification_commands': 'notify-host',
                'min_business_impact': 3
            }
        )

        self.assertEqual(
            self.mongoconnection.shinken.notificationways.find_one(
                {'notificationway_name': 'email_all_time'}
                )['min_business_impact'],
            3
        )
