"""Estimation of nacelle and pylon geometry."""
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

import fastoad.api as oad
import openmdao.api as om

from .constants import (
    SUBMODEL_NACELLE_X_POSITION,
    SUBMODEL_NACELLE_Y_POSITION,
    SUBMODEL_NACELLE_DIMENSION,
)

from ...constants import SUBMODEL_NACELLE_GEOMETRY


@oad.RegisterSubmodel(SUBMODEL_NACELLE_GEOMETRY, "fastga.submodel.geometry.nacelle.legacy")
class ComputeNacelleGeometry(om.Group):
    # TODO: Document equations. Cite sources
    """Nacelle and pylon geometry estimation."""

    def initialize(self):
        self.options.declare("propulsion_id", default="", types=str)

    def setup(self):

        propulsion_option = {"propulsion_id": self.options["propulsion_id"]}
        self.add_subsystem(
            "comp_nacelle_y_pos",
            oad.RegisterSubmodel.get_submodel(SUBMODEL_NACELLE_X_POSITION),
            promotes=["*"],
        )
        self.add_subsystem(
            "comp_nacelle_x_pos",
            oad.RegisterSubmodel.get_submodel(SUBMODEL_NACELLE_Y_POSITION),
            promotes=["*"],
        )
        self.add_subsystem(
            "comp_nacelle_dimension",
            oad.RegisterSubmodel.get_submodel(
                SUBMODEL_NACELLE_DIMENSION, options=propulsion_option
            ),
            promotes=["*"],
        )
