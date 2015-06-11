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


class Plugin(object):

    def run(self):
        print("DISK OK - free space: / 3326 MB (56%); | /=2643MB;5948;5958;0;"
              "5968")
        sys.exit(0)


def main():
    Plugin().run()

if __name__ == "__main__":
    main()
