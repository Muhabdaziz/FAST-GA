"""Estimation of wing sweep at l/c=100% inner."""
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

from ..constants import SUBMODEL_WING_SWEEP_100_INNER


@oad.RegisterSubmodel(
    SUBMODEL_WING_SWEEP_100_INNER, "fastga.submodel.geometry.wing.sweep.100_inner.legacy"
)
class ComputeWingSweep100Inner(om.ExplicitComponent):
    """Estimation of inner wing sweep at l/c=100%"""

    def setup(self):

        self.add_input("data:geometry:wing:tip:leading_edge:x:local", val=np.nan, units="m")
        self.add_input("data:geometry:wing:root:y", val=np.nan, units="m")
        self.add_input("data:geometry:wing:tip:y", val=np.nan, units="m")
        self.add_input("data:geometry:wing:root:chord", val=np.nan, units="m")
        self.add_input("data:geometry:wing:tip:chord", val=np.nan, units="m")

        self.add_output("data:geometry:wing:sweep_100_inner", units="rad")

        self.declare_partials(of="*", wrt="*", method="exact")

    def compute(self, inputs, outputs, discrete_inputs=None, discrete_outputs=None):

        x4_wing = inputs["data:geometry:wing:tip:leading_edge:x:local"]
        y2_wing = inputs["data:geometry:wing:root:y"]
        y4_wing = inputs["data:geometry:wing:tip:y"]
        l2_wing = inputs["data:geometry:wing:root:chord"]
        l4_wing = inputs["data:geometry:wing:tip:chord"]

        outputs["data:geometry:wing:sweep_100_inner"] = np.arctan2(
            (x4_wing + l4_wing - l2_wing), (y4_wing - y2_wing)
        )

    def compute_partials(self, inputs, partials, discrete_inputs=None):

        x4_wing = inputs["data:geometry:wing:tip:leading_edge:x:local"]
        y2_wing = inputs["data:geometry:wing:root:y"]
        y4_wing = inputs["data:geometry:wing:tip:y"]
        l2_wing = inputs["data:geometry:wing:root:chord"]
        l4_wing = inputs["data:geometry:wing:tip:chord"]

        tmp = (l4_wing - l2_wing + x4_wing) ** 2.0 / (y2_wing - y4_wing) ** 2.0 + 1.0

        partials[
            "data:geometry:wing:sweep_100_inner", "data:geometry:wing:tip:leading_edge:x:local"
        ] = -1.0 / (tmp * (y2_wing - y4_wing))
        partials["data:geometry:wing:sweep_100_inner", "data:geometry:wing:root:y"] = (
            l4_wing - l2_wing + x4_wing
        ) / (tmp * (y2_wing - y4_wing) ** 2.0)
        partials["data:geometry:wing:sweep_100_inner", "data:geometry:wing:tip:y"] = -(
            l4_wing - l2_wing + x4_wing
        ) / (tmp * (y2_wing - y4_wing) ** 2.0)
        partials["data:geometry:wing:sweep_100_inner", "data:geometry:wing:root:chord"] = 1.0 / (
            tmp * (y2_wing - y4_wing)
        )
        partials["data:geometry:wing:sweep_100_inner", "data:geometry:wing:tip:chord"] = -1.0 / (
            tmp * (y2_wing - y4_wing)
        )
