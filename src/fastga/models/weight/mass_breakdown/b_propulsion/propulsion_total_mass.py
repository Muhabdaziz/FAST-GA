"""Computation of the propulsion system mass."""
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

import openmdao.api as om

import numpy as np


class ComputePropulsionMass(om.ExplicitComponent):
    """
    Computes the aircraft's propulsion system total mass.
    """

    def setup(self):

        self.add_input("data:weight:propulsion:engine:mass", val=np.nan, units="kg")
        self.add_input("data:weight:propulsion:fuel_lines:mass", val=np.nan, units="kg")

        self.add_output(
            "data:weight:propulsion:mass", units="kg", desc="Mass of aircraft propulsions"
        )

        self.declare_partials(of="*", wrt="*", val=1.0)

    def compute(self, inputs, outputs, discrete_inputs=None, discrete_outputs=None):

        m_engine = inputs["data:weight:propulsion:engine:mass"]
        m_fuel_lines = inputs["data:weight:propulsion:fuel_lines:mass"]

        outputs["data:weight:propulsion:mass"] = m_engine + m_fuel_lines
