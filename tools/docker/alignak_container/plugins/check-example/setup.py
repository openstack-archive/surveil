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

from __future__ import with_statement

import setuptools


description = 'An Alignak plugin'
long_description = (''' .. ''')


setuptools.setup(
    name='check_example',
    version="1.0",
    packages=setuptools.find_packages(),
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
