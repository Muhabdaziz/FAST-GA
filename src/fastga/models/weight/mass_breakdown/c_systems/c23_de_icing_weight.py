"""
Estimation of anti icing systems weight.
"""
#  This file is part of FAST-OAD_CS23 : A framework for rapid Overall Aircraft Design
#  Copyright (C) 2022  ONERA & ISAE-SUPAERO
#  FAST is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import numpy as np
import openmdao.api as om


class ComputeAntiIcingSystemsWeight(om.ExplicitComponent):
    """
    Anti-icing is bundled up with the air-conditioning weight, thus the following component returns zero value.

    Based on a statistical analysis. See :cite:`raymer:2012` but can also be found in
    :cite:`gudmundsson:2013` for the air conditioning and de-icing.
    """

    def setup(self):

        self.add_input("data:weight:aircraft:MTOW", val=np.nan, units="lb")

        self.add_output("data:weight:systems:life_support:de_icing:mass", units="lb")

        self.declare_partials(of="*", wrt="*", val=0.0)

    def compute(self, inputs, outputs, discrete_inputs=None, discrete_outputs=None):

        c23 = 0.0 * inputs["data:weight:aircraft:MTOW"]

        outputs["data:weight:systems:life_support:de_icing:mass"] = c23
