"""FAST - Copyright (c) 2021 ONERA ISAE."""

#  This file is part of FAST : A framework for rapid Overall Aircraft Design
#  Copyright (C) 2020  ONERA & ISAE-SUPAERO
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


class ReserveEnergy(om.ExplicitComponent):
    """Computes the fuel consumed during the reserve phase."""

    def setup(self):

        self.add_input("data:mission:sizing:main_route:cruise:fuel", np.nan, units="kg")
        self.add_input("data:mission:sizing:main_route:cruise:energy", np.nan, units="W*h")
        self.add_input("data:mission:sizing:main_route:cruise:duration", np.nan, units="s")
        self.add_input("data:mission:sizing:main_route:reserve:duration", np.nan, units="s")

        self.add_output("data:mission:sizing:main_route:reserve:fuel", units="kg")
        self.add_output("data:mission:sizing:main_route:reserve:energy", units="W*h")

    def setup_partials(self):
        self.declare_partials(
            of="data:mission:sizing:main_route:reserve:fuel",
            wrt=[
                "data:mission:sizing:main_route:cruise:fuel",
                "data:mission:sizing:main_route:cruise:duration",
                "data:mission:sizing:main_route:reserve:duration",
            ],
            method="exact",
        )
        self.declare_partials(
            of="data:mission:sizing:main_route:reserve:energy",
            wrt=[
                "data:mission:sizing:main_route:cruise:energy",
                "data:mission:sizing:main_route:cruise:duration",
                "data:mission:sizing:main_route:reserve:duration",
            ],
            method="exact",
        )

    def compute(self, inputs, outputs, discrete_inputs=None, discrete_outputs=None):

        m_reserve = (
            inputs["data:mission:sizing:main_route:cruise:fuel"]
            * inputs["data:mission:sizing:main_route:reserve:duration"]
            / max(
                1e-6, inputs["data:mission:sizing:main_route:cruise:duration"]
            )  # avoid 0 division
        )
        energy_reserve = (
            inputs["data:mission:sizing:main_route:cruise:energy"]
            * inputs["data:mission:sizing:main_route:reserve:duration"]
            / max(
                1e-6, inputs["data:mission:sizing:main_route:cruise:duration"]
            )  # avoid 0 division
        )
        outputs["data:mission:sizing:main_route:reserve:fuel"] = m_reserve
        outputs["data:mission:sizing:main_route:reserve:energy"] = energy_reserve

    def compute_partials(self, inputs, partials, discrete_inputs=None):

        cruise_time = inputs["data:mission:sizing:main_route:cruise:duration"]
        rsv_time = inputs["data:mission:sizing:main_route:reserve:duration"]
        cruise_fuel = inputs["data:mission:sizing:main_route:cruise:fuel"]
        cruise_energy = inputs["data:mission:sizing:main_route:cruise:energy"]

        partials[
            "data:mission:sizing:main_route:reserve:fuel",
            "data:mission:sizing:main_route:cruise:fuel",
        ] = (
            rsv_time / cruise_time
        )
        partials[
            "data:mission:sizing:main_route:reserve:energy",
            "data:mission:sizing:main_route:cruise:energy",
        ] = (
            rsv_time / cruise_time
        )
        partials[
            "data:mission:sizing:main_route:reserve:fuel",
            "data:mission:sizing:main_route:reserve:duration",
        ] = (
            cruise_fuel / cruise_time
        )
        partials[
            "data:mission:sizing:main_route:reserve:energy",
            "data:mission:sizing:main_route:reserve:duration",
        ] = (
            cruise_energy / cruise_time
        )
        partials[
            "data:mission:sizing:main_route:reserve:fuel",
            "data:mission:sizing:main_route:cruise:duration",
        ] = (
            rsv_time * cruise_fuel / cruise_time ** 2
        )
        partials[
            "data:mission:sizing:main_route:reserve:energy",
            "data:mission:sizing:main_route:cruise:duration",
        ] = (
            rsv_time * cruise_energy / cruise_time ** 2
        )
