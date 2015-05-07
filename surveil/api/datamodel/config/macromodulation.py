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

import wsme
import wsme.types as wtypes

from surveil.api.datamodel import types


class MacroModulation(types.Base):
    macromodulation_name = wsme.wsattr(wtypes.text, mandatory=True)
    modulation_period = wsme.wsattr(wtypes.text, mandatory=True)
    # _CRITICAL = wsme.wsattr(int, mandatory=True)
    # _WARNING = wsme.wsattr(int, mandatory=True)

    macros = wsme.wsattr(
        wtypes.DictType(wtypes.text, int),
        mandatory=False
    )

    def __init__(self, **kwargs):
        super(MacroModulation, self).__init__(**kwargs)

        # Custom fields start with '_'. Detect them and assign them.
        macros = [i for i in kwargs.items()
                  if isinstance(i[0], str) and i[0].startswith('_')]
        if len(macros) > 0:
            self.macros = {}
            for item in macros:
                self.macros[item[0]] = item[1]

    def as_dict(self):
        mod_dict = super(MacroModulation, self).as_dict()
        macros = mod_dict.pop("macros", None)
        if macros:
            for item in macros.items():
                mod_dict[item[0]] = item[1]
        return mod_dict

    @classmethod
    def sample(cls):
        return cls(
            macromodulation_name='HighDuringNight',
            modulation_period='night',
            macros={"_CRITICAL": 20, "_WARNING": 10}
        )
