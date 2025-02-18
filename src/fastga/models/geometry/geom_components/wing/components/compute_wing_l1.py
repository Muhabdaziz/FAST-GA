"""Estimation of wing L1 chords."""
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
import fastoad.api as oad

from ..constants import SUBMODEL_WING_L1


@oad.RegisterSubmodel(SUBMODEL_WING_L1, "fastga.submodel.geometry.wing.l1.legacy")
class ComputeWingL1(om.ExplicitComponent):
    """Estimate l1 wing chord."""

    def setup(self):

        self.add_input("data:geometry:wing:area", val=np.nan, units="m**2")
        self.add_input("data:geometry:wing:root:y", val=np.nan, units="m")
        self.add_input("data:geometry:wing:tip:y", val=np.nan, units="m")
        self.add_input("data:geometry:wing:taper_ratio", val=np.nan)

        self.add_output("data:geometry:wing:root:virtual_chord", units="m")

        self.declare_partials(of="*", wrt="*", method="exact")

    def compute(self, inputs, outputs, discrete_inputs=None, discrete_outputs=None):

        wing_area = inputs["data:geometry:wing:area"]
        y2_wing = inputs["data:geometry:wing:root:y"]
        y4_wing = inputs["data:geometry:wing:tip:y"]
        taper_ratio = inputs["data:geometry:wing:taper_ratio"]

        l1_wing = wing_area / (2.0 * y2_wing + (y4_wing - y2_wing) * (1.0 + taper_ratio))

        outputs["data:geometry:wing:root:virtual_chord"] = l1_wing

    def compute_partials(self, inputs, partials, discrete_inputs=None):

        wing_area = inputs["data:geometry:wing:area"]
        y2_wing = inputs["data:geometry:wing:root:y"]
        y4_wing = inputs["data:geometry:wing:tip:y"]
        taper_ratio = inputs["data:geometry:wing:taper_ratio"]

        partials["data:geometry:wing:root:virtual_chord", "data:geometry:wing:area"] = 1.0 / (
            2.0 * y2_wing - (y2_wing - y4_wing) * (taper_ratio + 1.0)
        )
        partials["data:geometry:wing:root:virtual_chord", "data:geometry:wing:root:y"] = (
            wing_area * (taper_ratio - 1.0)
        ) / (2.0 * y2_wing - (y2_wing - y4_wing) * (taper_ratio + 1.0)) ** 2.0
        partials["data:geometry:wing:root:virtual_chord", "data:geometry:wing:tip:y"] = (
            -(wing_area * (taper_ratio + 1.0))
            / (2.0 * y2_wing - (y2_wing - y4_wing) * (taper_ratio + 1.0)) ** 2.0
        )
        partials["data:geometry:wing:root:virtual_chord", "data:geometry:wing:taper_ratio"] = (
            wing_area * (y2_wing - y4_wing)
        ) / (2.0 * y2_wing - (y2_wing - y4_wing) * (taper_ratio + 1.0)) ** 2.0
