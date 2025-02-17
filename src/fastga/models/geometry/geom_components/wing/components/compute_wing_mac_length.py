"""Estimation of wing mean aerodynamic chord length."""
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

from ..constants import SUBMODEL_WING_MAC_LENGTH


@oad.RegisterSubmodel(SUBMODEL_WING_MAC_LENGTH, "fastga.submodel.geometry.wing.mac.length.legacy")
class ComputeWingMacLength(om.ExplicitComponent):
    """
    Compute MAC length of the wing.
    """

    def setup(self):

        self.add_input("data:geometry:wing:area", val=np.nan, units="m**2")
        self.add_input("data:geometry:wing:root:y", val=np.nan, units="m")
        self.add_input("data:geometry:wing:tip:y", val=np.nan, units="m")
        self.add_input("data:geometry:wing:root:chord", val=np.nan, units="m")
        self.add_input("data:geometry:wing:tip:chord", val=np.nan, units="m")

        self.add_output("data:geometry:wing:MAC:length", units="m")

        self.declare_partials(of="*", wrt="*", method="exact")

    def compute(self, inputs, outputs, discrete_inputs=None, discrete_outputs=None):

        wing_area = inputs["data:geometry:wing:area"]
        y2_wing = inputs["data:geometry:wing:root:y"]
        y4_wing = inputs["data:geometry:wing:tip:y"]
        l2_wing = inputs["data:geometry:wing:root:chord"]
        l4_wing = inputs["data:geometry:wing:tip:chord"]

        l0_wing = (
            3.0 * y2_wing * l2_wing ** 2.0
            + (y4_wing - y2_wing) * (l2_wing ** 2.0 + l4_wing ** 2.0 + l2_wing * l4_wing)
        ) * (2.0 / (3.0 * wing_area))

        outputs["data:geometry:wing:MAC:length"] = l0_wing

    def compute_partials(self, inputs, partials, discrete_inputs=None):

        wing_area = inputs["data:geometry:wing:area"]
        y2_wing = inputs["data:geometry:wing:root:y"]
        y4_wing = inputs["data:geometry:wing:tip:y"]
        l2_wing = inputs["data:geometry:wing:root:chord"]
        l4_wing = inputs["data:geometry:wing:tip:chord"]

        partials["data:geometry:wing:MAC:length", "data:geometry:wing:area"] = (
            2.0
            * (
                (y2_wing - y4_wing) * (l2_wing ** 2.0 + l2_wing * l4_wing + l4_wing ** 2.0)
                - 3.0 * l2_wing ** 2.0 * y2_wing
            )
        ) / (3.0 * wing_area ** 2.0)
        partials["data:geometry:wing:MAC:length", "data:geometry:wing:root:y"] = -(
            2.0 * (-2.0 * l2_wing ** 2.0 + l2_wing * l4_wing + l4_wing ** 2.0)
        ) / (3.0 * wing_area)
        partials["data:geometry:wing:MAC:length", "data:geometry:wing:tip:y"] = (
            2.0 * (l2_wing ** 2.0 + l2_wing * l4_wing + l4_wing ** 2.0)
        ) / (3 * wing_area)
        partials["data:geometry:wing:MAC:length", "data:geometry:wing:root:chord"] = (
            2.0 * (6.0 * l2_wing * y2_wing - (2.0 * l2_wing + l4_wing) * (y2_wing - y4_wing))
        ) / (3.0 * wing_area)
        partials["data:geometry:wing:MAC:length", "data:geometry:wing:tip:chord"] = -(
            2.0 * (l2_wing + 2.0 * l4_wing) * (y2_wing - y4_wing)
        ) / (3.0 * wing_area)
