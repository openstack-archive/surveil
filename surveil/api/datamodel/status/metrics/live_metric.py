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

import wsme
import wsme.types as wtypes

from surveil.api.datamodel import types


class LiveMetric(types.Base):

    metric_name = wsme.wsattr(wtypes.text, mandatory=True)
    """Name of the metric"""

    max = wsme.wsattr(wtypes.text, mandatory=False)
    """Maximum value for the metric"""

    min = wsme.wsattr(wtypes.text, mandatory=False)
    """Minimal value for the metric"""

    critical = wsme.wsattr(wtypes.text, mandatory=False)
    """Critical value for the metric"""

    warning = wsme.wsattr(wtypes.text, mandatory=False)
    """Warning value for the metric"""

    value = wsme.wsattr(wtypes.text, mandatory=False)
    """Current value of the metric"""

    unit = wsme.wsattr(wtypes.text, mandatory=False)
    """Unit of the metric"""

    @classmethod
    def sample(cls):
        return cls(
            metric_name='pl',
            max='100',
            min='0',
            critical='100',
            warning='100',
            value='0',
            unit='s'
        )
