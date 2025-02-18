"""Estimation of wing geometry."""
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

import fastoad.api as oad

from .constants import (
    SUBMODEL_WING_THICKNESS_RATIO,
    SUBMODEL_WING_SPAN,
    SUBMODEL_WING_ROOT_HEIGHT,
    SUBMODEL_WING_TIP_HEIGHT,
    SUBMODEL_WING_L1,
    SUBMODEL_WING_L2,
    SUBMODEL_WING_L3,
    SUBMODEL_WING_L4,
    SUBMODEL_WING_X_LOCAL_KINK,
    SUBMODEL_WING_X_LOCAL_TIP,
    SUBMODEL_WING_X_ABSOLUTE_MAC,
    SUBMODEL_WING_X_ABSOLUTE_TIP,
    SUBMODEL_WING_Y_KINK,
    SUBMODEL_WING_Y_ROOT,
    SUBMODEL_WING_Y_TIP,
    SUBMODEL_WING_B50,
    SUBMODEL_WING_MAC_LENGTH,
    SUBMODEL_WING_MAC_X,
    SUBMODEL_WING_MAC_Y,
    SUBMODEL_WING_SWEEP_0,
    SUBMODEL_WING_SWEEP_50,
    SUBMODEL_WING_SWEEP_100_INNER,
    SUBMODEL_WING_SWEEP_100_OUTER,
    SUBMODEL_WING_WET_AREA,
    SUBMODEL_WING_OUTER_AREA,
)
from ...constants import SUBMODEL_WING_GEOMETRY


@oad.RegisterSubmodel(SUBMODEL_WING_GEOMETRY, "fastga.submodel.geometry.wing.legacy")
class ComputeWingGeometry(om.Group):
    # TODO: Document equations. Cite sources
    """Wing geometry estimation."""

    def setup(self):
        self.add_subsystem(
            "wing_toc",
            oad.RegisterSubmodel.get_submodel(SUBMODEL_WING_THICKNESS_RATIO),
            promotes=["*"],
        )
        self.add_subsystem(
            "wing_span", oad.RegisterSubmodel.get_submodel(SUBMODEL_WING_SPAN), promotes=["*"]
        )
        self.add_subsystem(
            "wing_y_kink", oad.RegisterSubmodel.get_submodel(SUBMODEL_WING_Y_KINK), promotes=["*"]
        )
        self.add_subsystem(
            "wing_y_root", oad.RegisterSubmodel.get_submodel(SUBMODEL_WING_Y_ROOT), promotes=["*"]
        )
        self.add_subsystem(
            "wing_y_tip", oad.RegisterSubmodel.get_submodel(SUBMODEL_WING_Y_TIP), promotes=["*"]
        )
        self.add_subsystem(
            "wing_l1", oad.RegisterSubmodel.get_submodel(SUBMODEL_WING_L1), promotes=["*"]
        )
        self.add_subsystem(
            "wing_l2", oad.RegisterSubmodel.get_submodel(SUBMODEL_WING_L2), promotes=["*"]
        )
        self.add_subsystem(
            "wing_l3", oad.RegisterSubmodel.get_submodel(SUBMODEL_WING_L3), promotes=["*"]
        )
        self.add_subsystem(
            "wing_l4", oad.RegisterSubmodel.get_submodel(SUBMODEL_WING_L4), promotes=["*"]
        )
        self.add_subsystem(
            "wing_z_root",
            oad.RegisterSubmodel.get_submodel(SUBMODEL_WING_ROOT_HEIGHT),
            promotes=["*"],
        )
        self.add_subsystem(
            "wing_z_tip",
            oad.RegisterSubmodel.get_submodel(SUBMODEL_WING_TIP_HEIGHT),
            promotes=["*"],
        )
        self.add_subsystem(
            "wing_x_kink",
            oad.RegisterSubmodel.get_submodel(SUBMODEL_WING_X_LOCAL_KINK),
            promotes=["*"],
        )
        self.add_subsystem(
            "wing_x_tip",
            oad.RegisterSubmodel.get_submodel(SUBMODEL_WING_X_LOCAL_TIP),
            promotes=["*"],
        )
        self.add_subsystem(
            "wing_b50", oad.RegisterSubmodel.get_submodel(SUBMODEL_WING_B50), promotes=["*"]
        )
        self.add_subsystem(
            "wing_mac_length",
            oad.RegisterSubmodel.get_submodel(SUBMODEL_WING_MAC_LENGTH),
            promotes=["*"],
        )
        self.add_subsystem(
            "wing_mac_x", oad.RegisterSubmodel.get_submodel(SUBMODEL_WING_MAC_X), promotes=["*"]
        )
        self.add_subsystem(
            "wing_mac_y", oad.RegisterSubmodel.get_submodel(SUBMODEL_WING_MAC_Y), promotes=["*"]
        )
        self.add_subsystem(
            "wing_xabsolute_mac",
            oad.RegisterSubmodel.get_submodel(SUBMODEL_WING_X_ABSOLUTE_MAC),
            promotes=["*"],
        )
        self.add_subsystem(
            "wing_xabsolute_tip",
            oad.RegisterSubmodel.get_submodel(SUBMODEL_WING_X_ABSOLUTE_TIP),
            promotes=["*"],
        )
        self.add_subsystem(
            "wing_sweep_0", oad.RegisterSubmodel.get_submodel(SUBMODEL_WING_SWEEP_0), promotes=["*"]
        )
        self.add_subsystem(
            "wing_sweep_50",
            oad.RegisterSubmodel.get_submodel(SUBMODEL_WING_SWEEP_50),
            promotes=["*"],
        )
        self.add_subsystem(
            "wing_sweep_100_inner",
            oad.RegisterSubmodel.get_submodel(SUBMODEL_WING_SWEEP_100_INNER),
            promotes=["*"],
        )
        self.add_subsystem(
            "wing_sweep_100_outer",
            oad.RegisterSubmodel.get_submodel(SUBMODEL_WING_SWEEP_100_OUTER),
            promotes=["*"],
        )
        self.add_subsystem(
            "wing_wet_area",
            oad.RegisterSubmodel.get_submodel(SUBMODEL_WING_WET_AREA),
            promotes=["*"],
        )
        self.add_subsystem(
            "wing_outer_area",
            oad.RegisterSubmodel.get_submodel(SUBMODEL_WING_OUTER_AREA),
            promotes=["*"],
        )
