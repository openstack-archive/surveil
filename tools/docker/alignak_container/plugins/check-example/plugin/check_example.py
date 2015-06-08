#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Check example
#
# Copyright (C) 2015 Savoir-faire Linux Inc.
# Copyright © 2012 eNovance <licensing@enovance.com>
#
# Author: Vincent Fournier <vincent.fournier@savoirfairelinux.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import random

from shinkenplugins.old import BasePlugin
from shinkenplugins.perfdata import PerfData
from shinkenplugins.states import STATES

class Plugin(BasePlugin):
    NAME = 'check-example'
    VERSION = '0.1'
    DESCRIPTION = 'check example'
    AUTHOR = 'Vincent Fournier'
    EMAIL = 'vincent.fournier@savoirfairelinux.com'

    ARGS = [
        # Can't touch this:
        ('h', 'help', 'display plugin help', False),
        ('v', 'version', 'display plugin version number', False),
    ]

    def check_args(self, args):
        # You can do your various arguments check here.
        # If you don't need to check things, you can safely remove the method.
        return True, None

    def run(self, args):
        # Here is the core of the plugin.
        # After doing your verifications, escape by doing:
        # self.exit(return_code, 'return_message', *performance_data)

        perfdata = PerfData('check_example', random.randint(0, 10), max_=10)
        state = random.choice(STATES)
        self.exit(state,
                  "Random state " + str(state),
                  perfdata
            )


def main(argv=None):
    Plugin(argv)

if __name__ == "__main__":
    main()