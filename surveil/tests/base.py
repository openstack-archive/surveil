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

import sys
import time
import unittest


class BaseTestCase(unittest.TestCase):
    maxDiff = None

    def assert_count_equal_backport(self, item1, item2):
        if sys.version_info[0] >= 3:
            result = self.assertCountEqual(
                item1,
                item2
            )
        else:
            result = self.assertItemsEqual(
                sorted(item1),
                sorted(item2)
            )

        return result

    def try_for_x_seconds(self,
                          function,
                          time_to_wait=108,
                          message="Function did not succeed",
                          cooldown=10,
                          exception=Exception):
        """Returns True if the functions raises no exception."""

        now = time.time()
        while True:
            if time.time() < (now + time_to_wait):
                try:
                    function()
                    return True
                except exception:
                    pass
                time.sleep(cooldown)
            else:
                raise Exception(message)
