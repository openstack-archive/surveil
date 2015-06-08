#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Copyright (C) 2014, Savoir-faire Linux, Inc.
#
# Authors:
#   Vincent Fournier <vincent.fournier@savoirfairelinux.com>
#
#############################################################################

from __future__ import with_statement

from setuptools import setup, find_packages

#############################################################################

description = 'An Alignak plugin'
long_description = (''' .. ''')


setup(
    name='check_example',
    version="1.0",
    packages=find_packages(),
    author="Vincent Fournier",
    author_email="vincent.fournier@savoirfairelinux.com",
    long_description=long_description,
    description=description,
    platforms=['any'],
    install_requires=[],
    entry_points="""
    [console_scripts]
    check_example = check_example.check_example:main
    """,
)
