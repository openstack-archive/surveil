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

"""Starter script for the Surveil API service."""

import os
import subprocess
import sys

from surveil import api


def main():
    filename = os.path.join(os.path.dirname(api.__file__), "config.py")
    subprocess.Popen(['pecan', 'serve', '--reload', filename],
                     stdin=sys.stdout, stdout=sys.stdout)
