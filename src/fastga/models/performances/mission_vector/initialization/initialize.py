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

from fastga.models.performances.mission.mission import (
    POINTS_NB_CLIMB,
    POINTS_NB_CRUISE,
    POINTS_NB_DESCENT,
)

from ..initialization.initialize_altitude import InitializeAltitude
from ..initialization.initialize_airspeed import InitializeAirspeed
from ..initialization.initialize_gamma import InitializeGamma
from ..initialization.initialize_horizontal_speed import InitializeHorizontalSpeed
from ..initialization.initialize_time_and_distance import InitializeTimeAndDistance
from ..initialization.initialize_airspeed_derivatives import InitializeAirspeedDerivatives
from ..initialization.initialize_CoG import InitializeCoG


class Initialize(om.Group):
    """Find the conditions necessary for the aircraft equilibrium."""

    def initialize(self):

        self.options.declare(
            "number_of_points", default=1, desc="number of equilibrium to be treated"
        )

    def setup(self):

        n = self.options["number_of_points"]
        engine_setting = np.concatenate(
            (
                np.full(POINTS_NB_CLIMB, 2),
                np.full(POINTS_NB_CRUISE, 3),
                np.full(POINTS_NB_DESCENT, 2),
            )
        )
        ivc_engine_setting = om.IndepVarComp()
        ivc_engine_setting.add_output("engine_setting", val=engine_setting, units=None, shape=n)

        self.add_subsystem("initialize_engine_setting", subsys=ivc_engine_setting, promotes=[])
        self.add_subsystem(
            "initialize_altitude",
            InitializeAltitude(number_of_points=n),
            promotes_inputs=["data:*"],
            promotes_outputs=[],
        )
        self.add_subsystem(
            "initialize_airspeed",
            InitializeAirspeed(number_of_points=n),
            promotes_inputs=["data:*"],
            promotes_outputs=[],
        )
        self.add_subsystem(
            "initialize_gamma",
            InitializeGamma(number_of_points=n),
            promotes_inputs=["data:*"],
            promotes_outputs=[],
        )
        self.add_subsystem(
            "initialize_horizontal_speed",
            InitializeHorizontalSpeed(number_of_points=n),
            promotes_inputs=[],
            promotes_outputs=[],
        )
        self.add_subsystem(
            "initialize_time_and_distance",
            InitializeTimeAndDistance(number_of_points=n),
            promotes_inputs=["data:*"],
            promotes_outputs=[],
        )
        self.add_subsystem(
            "initialize_airspeed_time_derivatives",
            InitializeAirspeedDerivatives(number_of_points=n),
            promotes_inputs=[],
            promotes_outputs=[],
        )
        self.add_subsystem(
            "initialize_center_of_gravity",
            InitializeCoG(number_of_points=n),
            promotes_inputs=["data:*"],
            promotes_outputs=[],
        )

        self.connect(
            "initialize_horizontal_speed.horizontal_speed",
            "initialize_time_and_distance.horizontal_speed",
        )

        self.connect(
            "initialize_airspeed.true_airspeed",
            [
                "initialize_gamma.true_airspeed",
                "initialize_horizontal_speed.true_airspeed",
                "initialize_time_and_distance.true_airspeed",
                "initialize_airspeed_time_derivatives.true_airspeed",
            ],
        )

        self.connect(
            "initialize_airspeed.equivalent_airspeed",
            "initialize_airspeed_time_derivatives.equivalent_airspeed",
        )

        self.connect(
            "initialize_gamma.gamma",
            ["initialize_airspeed_time_derivatives.gamma", "initialize_horizontal_speed.gamma"],
        )

        self.connect(
            "initialize_altitude.altitude",
            [
                "initialize_airspeed.altitude",
                "initialize_gamma.altitude",
                "initialize_time_and_distance.altitude",
                "initialize_airspeed_time_derivatives.altitude",
            ],
        )
