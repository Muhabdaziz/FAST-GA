"""
Estimation of tail weight.
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

from stdatm import Atmosphere
import fastoad.api as oad

from .constants import SUBMODEL_HORIZONTAL_TAIL_MASS

oad.RegisterSubmodel.active_models[
    SUBMODEL_HORIZONTAL_TAIL_MASS
] = "fastga.submodel.weight.mass.airframe.horizontal_tail.legacy"


@oad.RegisterSubmodel(
    SUBMODEL_HORIZONTAL_TAIL_MASS, "fastga.submodel.weight.mass.airframe.horizontal_tail.legacy"
)
class ComputeHorizontalTailWeight(om.ExplicitComponent):
    """
    Weight estimation for tail weight

    Based on a statistical analysis. See :cite:`raymer:2012` but can also be found in
    :cite:`gudmundsson:2013`
    """

    def setup(self):

        self.add_input("data:mission:sizing:cs23:sizing_factor:ultimate_aircraft", val=np.nan)
        self.add_input("data:weight:aircraft:MTOW", val=np.nan, units="lb")
        self.add_input("data:weight:airframe:horizontal_tail:k_factor", val=1.0)
        self.add_input("data:TLAR:v_cruise", val=np.nan, units="m/s")
        self.add_input("data:mission:sizing:main_route:cruise:altitude", val=np.nan, units="ft")

        self.add_input("data:geometry:horizontal_tail:area", val=np.nan, units="ft**2")
        self.add_input("data:geometry:horizontal_tail:thickness_ratio", val=np.nan)
        self.add_input("data:geometry:horizontal_tail:sweep_25", val=np.nan, units="deg")
        self.add_input("data:geometry:horizontal_tail:aspect_ratio", val=np.nan)
        self.add_input("data:geometry:horizontal_tail:taper_ratio", val=np.nan)

        self.add_output("data:weight:airframe:horizontal_tail:mass", units="lb")

        self.declare_partials("*", "*", method="exact")

    def compute(self, inputs, outputs, discrete_inputs=None, discrete_outputs=None):

        sizing_factor_ultimate = inputs["data:mission:sizing:cs23:sizing_factor:ultimate_aircraft"]
        mtow = inputs["data:weight:aircraft:MTOW"]
        v_cruise_ktas = inputs["data:TLAR:v_cruise"]
        cruise_alt = inputs["data:mission:sizing:main_route:cruise:altitude"]

        area_ht = inputs["data:geometry:horizontal_tail:area"]
        t_c_ht = inputs["data:geometry:horizontal_tail:thickness_ratio"]
        sweep_25_ht = inputs["data:geometry:horizontal_tail:sweep_25"]
        ar_ht = inputs["data:geometry:horizontal_tail:aspect_ratio"]
        taper_ht = inputs["data:geometry:horizontal_tail:taper_ratio"]

        rho_cruise = Atmosphere(cruise_alt, altitude_in_feet=True).density
        dynamic_pressure = 1.0 / 2.0 * rho_cruise * v_cruise_ktas ** 2.0 * 0.0208854
        # In lb/ft2

        a31 = 0.016 * (
            (sizing_factor_ultimate * mtow) ** 0.414
            * dynamic_pressure ** 0.168
            * area_ht ** 0.896
            * (100.0 * t_c_ht / np.cos(sweep_25_ht * np.pi / 180.0)) ** -0.12
            * (ar_ht / (np.cos(sweep_25_ht * np.pi / 180.0)) ** 2.0) ** 0.043
            * taper_ht ** -0.02
        )
        # Mass formula in lb

        outputs["data:weight:airframe:horizontal_tail:mass"] = (
            a31 * inputs["data:weight:airframe:horizontal_tail:k_factor"]
        )

    def compute_partials(self, inputs, partials, discrete_inputs=None):

        sizing_factor_ultimate = inputs["data:mission:sizing:cs23:sizing_factor:ultimate_aircraft"]
        mtow = inputs["data:weight:aircraft:MTOW"]
        v_cruise_ktas = inputs["data:TLAR:v_cruise"]
        cruise_alt = inputs["data:mission:sizing:main_route:cruise:altitude"]

        area_ht = inputs["data:geometry:horizontal_tail:area"]
        t_c_ht = inputs["data:geometry:horizontal_tail:thickness_ratio"]
        sweep_25_ht = inputs["data:geometry:horizontal_tail:sweep_25"]
        ar_ht = inputs["data:geometry:horizontal_tail:aspect_ratio"]
        taper_ht = inputs["data:geometry:horizontal_tail:taper_ratio"]

        k_factor = inputs["data:weight:airframe:horizontal_tail:k_factor"]

        rho_cruise = Atmosphere(cruise_alt, altitude_in_feet=True).density
        dynamic_pressure = 1.0 / 2.0 * rho_cruise * v_cruise_ktas ** 2.0 * 0.0208854
        # In lb/ft2

        a31 = 0.016 * (
            (sizing_factor_ultimate * mtow) ** 0.414
            * dynamic_pressure ** 0.168
            * area_ht ** 0.896
            * (100.0 * t_c_ht / np.cos(sweep_25_ht * np.pi / 180.0)) ** -0.12
            * (ar_ht / (np.cos(sweep_25_ht * np.pi / 180.0)) ** 2.0) ** 0.043
            * taper_ht ** -0.02
        )
        # Mass formula in lb

        partials[
            "data:weight:airframe:horizontal_tail:mass",
            "data:mission:sizing:cs23:sizing_factor:ultimate_aircraft",
        ] = k_factor * (
            (
                0.006624
                * area_ht ** (0.8960)
                * mtow
                * (ar_ht / np.cos(0.017453 * sweep_25_ht) ** 2) ** (0.0430)
                * (0.010443 * rho_cruise * v_cruise_ktas ** 2) ** (0.1680)
            )
            / (
                taper_ht ** (0.0200)
                * (mtow * sizing_factor_ultimate) ** (0.5860)
                * ((100.0 * t_c_ht) / np.cos(0.017453 * sweep_25_ht)) ** (0.1200)
            )
        )
        partials[
            "data:weight:airframe:horizontal_tail:mass", "data:weight:aircraft:MTOW"
        ] = k_factor * (
            (
                0.006624
                * area_ht ** (0.8960)
                * sizing_factor_ultimate
                * (ar_ht / np.cos(0.017453 * sweep_25_ht) ** 2) ** (0.0430)
                * (0.010443 * rho_cruise * v_cruise_ktas ** 2) ** (0.1680)
            )
            / (
                taper_ht ** (0.0200)
                * (mtow * sizing_factor_ultimate) ** (0.5860)
                * ((100.0 * t_c_ht) / np.cos(0.017453 * sweep_25_ht)) ** (0.1200)
            )
        )
        partials["data:weight:airframe:horizontal_tail:mass", "data:TLAR:v_cruise"] = k_factor * (
            (
                0.00005614
                * area_ht ** (0.8960)
                * rho_cruise
                * v_cruise_ktas
                * (mtow * sizing_factor_ultimate) ** (0.4140)
                * (ar_ht / np.cos(0.017453 * sweep_25_ht) ** 2) ** (0.0430)
            )
            / (
                taper_ht ** (0.0200)
                * ((100.0 * t_c_ht) / np.cos(0.017453 * sweep_25_ht)) ** (0.1200)
                * (0.010443 * rho_cruise * v_cruise_ktas ** 2) ** (0.8320)
            )
        )
        d_a31_d_rho_cruise = (
            0.00002807
            * area_ht ** (0.8960)
            * v_cruise_ktas ** 2
            * (mtow * sizing_factor_ultimate) ** (0.4140)
            * (ar_ht / np.cos(0.017453 * sweep_25_ht) ** 2) ** (0.0430)
        ) / (
            taper_ht ** (0.0200)
            * ((100.0 * t_c_ht) / np.cos(0.017453 * sweep_25_ht)) ** (0.1200)
            * (0.010443 * rho_cruise * v_cruise_ktas ** 2) ** (0.8320)
        )
        d_rho_cruise_d_cruise_alt = 2.3e-6  # lb/ft^4
        partials[
            "data:weight:airframe:horizontal_tail:mass",
            "data:mission:sizing:main_route:cruise:altitude",
        ] = k_factor * (d_a31_d_rho_cruise * d_rho_cruise_d_cruise_alt)
        partials[
            "data:weight:airframe:horizontal_tail:mass", "data:geometry:horizontal_tail:area"
        ] = k_factor * (
            (
                0.014336
                * (mtow * sizing_factor_ultimate) ** (0.4140)
                * (ar_ht / np.cos(0.017453 * sweep_25_ht) ** 2) ** (0.0430)
                * (0.010443 * rho_cruise * v_cruise_ktas ** 2) ** (0.1680)
            )
            / (
                area_ht ** (13 / 125)
                * taper_ht ** (0.0200)
                * ((100.0 * t_c_ht) / np.cos(0.017453 * sweep_25_ht)) ** (0.1200)
            )
        )
        partials[
            "data:weight:airframe:horizontal_tail:mass",
            "data:geometry:horizontal_tail:thickness_ratio",
        ] = k_factor * (
            -(
                0.192
                * area_ht ** (0.8960)
                * (mtow * sizing_factor_ultimate) ** (0.4140)
                * (ar_ht / np.cos(0.017453 * sweep_25_ht) ** 2) ** (0.0430)
                * (0.010443 * rho_cruise * v_cruise_ktas ** 2) ** (0.1680)
            )
            / (
                taper_ht ** (0.0200)
                * np.cos(0.017453 * sweep_25_ht)
                * ((100.0 * t_c_ht) / np.cos(0.017453 * sweep_25_ht)) ** (1.1200)
            )
        )
        partials[
            "data:weight:airframe:horizontal_tail:mass", "data:geometry:horizontal_tail:sweep_25"
        ] = k_factor * (
            (
                0.000024016
                * ar_ht
                * area_ht ** (0.8960)
                * np.sin(0.017453 * sweep_25_ht)
                * (mtow * sizing_factor_ultimate) ** (0.4140)
                * (0.010443 * rho_cruise * v_cruise_ktas ** 2) ** (0.1680)
            )
            / (
                taper_ht ** (0.0200)
                * np.cos(0.017453 * sweep_25_ht) ** 3
                * (ar_ht / np.cos(0.017453 * sweep_25_ht) ** 2) ** (0.9570)
                * ((100.0 * t_c_ht) / np.cos(0.017453 * sweep_25_ht)) ** (0.1200)
            )
            - (
                0.003351
                * area_ht ** (0.8960)
                * t_c_ht
                * np.sin(0.017453 * sweep_25_ht)
                * (mtow * sizing_factor_ultimate) ** (0.4140)
                * (ar_ht / np.cos(0.017453 * sweep_25_ht) ** 2) ** (0.0430)
                * (0.010443 * rho_cruise * v_cruise_ktas ** 2) ** (0.1680)
            )
            / (
                taper_ht ** (0.0200)
                * np.cos(0.017453 * sweep_25_ht) ** 2
                * ((100.0 * t_c_ht) / np.cos(0.017453 * sweep_25_ht)) ** (1.1200)
            )
        )
        partials[
            "data:weight:airframe:horizontal_tail:mass",
            "data:geometry:horizontal_tail:aspect_ratio",
        ] = k_factor * (
            (
                0.000688
                * area_ht ** (0.8960)
                * (mtow * sizing_factor_ultimate) ** (0.4140)
                * (0.010443 * rho_cruise * v_cruise_ktas ** 2) ** (0.1680)
            )
            / (
                taper_ht ** (0.0200)
                * np.cos(0.017453 * sweep_25_ht) ** 2
                * (ar_ht / np.cos(0.017453 * sweep_25_ht) ** 2) ** (0.9570)
                * ((100.0 * t_c_ht) / np.cos(0.017453 * sweep_25_ht)) ** (0.1200)
            )
        )
        partials[
            "data:weight:airframe:horizontal_tail:mass", "data:geometry:horizontal_tail:taper_ratio"
        ] = k_factor * (
            -(
                0.00032
                * area_ht ** (0.8960)
                * (mtow * sizing_factor_ultimate) ** (0.4140)
                * (ar_ht / np.cos(0.017453 * sweep_25_ht) ** 2) ** (0.0430)
                * (0.010443 * rho_cruise * v_cruise_ktas ** 2) ** (0.1680)
            )
            / (
                taper_ht ** (1.0200)
                * ((100.0 * t_c_ht) / np.cos(0.017453 * sweep_25_ht)) ** (0.1200)
            )
        )
        partials[
            "data:weight:airframe:horizontal_tail:mass",
            "data:weight:airframe:horizontal_tail:k_factor",
        ] = a31
