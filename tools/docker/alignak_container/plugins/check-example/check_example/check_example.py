#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Check example
#
# Copyright (C) 2015 Savoir-faire Linux Inc.
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

import sys


class Plugin(object):

    def run(self):
        print("DISK OK - free space: / 3326 MB (56%); | /=2643MB;5948;5958;0;5968")
        sys.exit(0)


def main():
    Plugin().run()

if __name__ == "__main__":
    main()
