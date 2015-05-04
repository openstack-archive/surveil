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

from surveil.tests.api import functionalTest


class TestHelloController(functionalTest.FunctionalTest):

    def test_get(self):
        response = self.get('/v2/hello')
        self.assertEqual(response.body, b"Hello World!")
        assert response.status_int == 200

    def test_post_policy_forbidden(self):
        with self.assertRaisesRegexp(Exception, '403 Forbidden'):
            self.get('/v2/hello/denied')
