"""
Test module for mass breakdown functions.
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

import pytest

from ..a_airframe import (
    ComputeTailWeight,
    ComputeTailWeightGD,
    ComputeTailWeightTorenbeekGD,
    ComputeFlightControlsWeight,
    ComputeFlightControlsWeightFLOPS,
    ComputeFuselageWeight,
    ComputeFuselageWeightRaymer,
    ComputeFuselageWeightRoskam,
    ComputeFuselageMassAnalytical,
    ComputeWingWeight,
    ComputeLandingGearWeight,
    ComputeWingMassAnalytical,
    ComputePaintWeight,
)
from ..a_airframe.wing_components import (
    ComputeWebMass,
    ComputeLowerFlange,
    ComputeUpperFlange,
    ComputeSkinMass,
    ComputeMiscMass,
    ComputeRibsMass,
    ComputePrimaryMass,
    ComputeSecondaryMass,
    UpdateWingMass,
)
from ..a_airframe.fuselage_components import (
    ComputeWingFuselageConnection,
    ComputeShell,
    ComputeWindows,
    ComputeFloor,
    ComputeDoors,
    ComputeBulkhead,
    ComputeInsulation,
    ComputeNLGHatch,
    ComputeTailCone,
    ComputeEngineSupport,
    ComputeAddBendingMassVertical,
    ComputeAddBendingMassHorizontal,
)
from ..a_airframe.sum import AirframeWeight
from ..b_propulsion import (
    ComputeOilWeight,
    ComputeFuelLinesWeight,
    ComputeFuelLinesWeightFLOPS,
    ComputeEngineWeight,
    ComputeEngineWeightRaymer,
    ComputeUnusableFuelWeight,
)
from ..b_propulsion.sum import PropulsionWeight
from ..c_systems import (
    ComputeLifeSupportSystemsWeight,
    ComputeLifeSupportSystemsWeightFLOPS,
    ComputeAvionicsSystemsWeight,
    ComputeElectricWeight,
    ComputeHydraulicWeight,
    ComputeAvionicsSystemsWeightFromUninstalled,
    ComputeRecordingSystemsWeight,
)
from ..c_systems.sum import SystemsWeight
from ..d_furniture import ComputePassengerSeatsWeight
from ..d_furniture.sum import FurnitureWeight
from ..mass_breakdown import MassBreakdown, ComputeOperatingWeightEmpty
from ..compute_design_payload import ComputeDesignPayload
from ..compute_maximum_payload import ComputeMaxPayload

from tests.testing_utilities import run_system, get_indep_var_comp, list_inputs

from .dummy_engines import ENGINE_WRAPPER_TBM900 as ENGINE_WRAPPER

XML_FILE = "daher_tbm900.xml"


def test_compute_design_payload():

    # Research independent input value in .xml file
    ivc = get_indep_var_comp(list_inputs(ComputeDesignPayload()), __file__, XML_FILE)

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(ComputeDesignPayload(), ivc)
    assert problem["data:weight:aircraft:payload"] == pytest.approx(612.0, abs=1e-2)


def test_compute_max_payload():

    # Research independent input value in .xml file
    ivc = get_indep_var_comp(list_inputs(ComputeMaxPayload()), __file__, XML_FILE)

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(ComputeMaxPayload(), ivc)
    assert problem["data:weight:aircraft:max_payload"] == pytest.approx(690.0, abs=1e-2)


def test_compute_wing_weight():
    """Tests wing weight computation from sample XML data."""
    # Research independent input value in .xml file
    ivc = get_indep_var_comp(list_inputs(ComputeWingWeight()), __file__, XML_FILE)

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(ComputeWingWeight(), ivc)
    weight_a1 = problem.get_val("data:weight:airframe:wing:mass", units="kg")
    assert weight_a1 == pytest.approx(
        277.95, abs=1e-2
    )  # difference because of integer conversion error


def test_compute_fuselage_weight():
    """Tests fuselage weight computation from sample XML data."""
    # Research independent input value in .xml file
    ivc = get_indep_var_comp(list_inputs(ComputeFuselageWeight()), __file__, XML_FILE)

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(ComputeFuselageWeight(), ivc)
    weight_a2 = problem.get_val("data:weight:airframe:fuselage:mass", units="kg")
    assert weight_a2 == pytest.approx(306.13, abs=1e-2)


def test_compute_fuselage_weight_raymer():
    """Tests fuselage weight computation from sample XML data."""
    # Research independent input value in .xml file
    ivc = get_indep_var_comp(list_inputs(ComputeFuselageWeightRaymer()), __file__, XML_FILE)

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(ComputeFuselageWeightRaymer(), ivc)
    weight_a2 = problem.get_val("data:weight:airframe:fuselage:mass", units="kg")
    assert weight_a2 == pytest.approx(320.60, abs=1e-2)


def test_compute_fuselage_weight_roskam():
    """Tests fuselage weight computation from sample XML data."""
    # Research independent input value in .xml file
    ivc = get_indep_var_comp(list_inputs(ComputeFuselageWeightRoskam()), __file__, XML_FILE)

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(ComputeFuselageWeightRoskam(), ivc)
    weight_a2 = problem.get_val("data:weight:airframe:fuselage:mass", units="kg")
    assert weight_a2 == pytest.approx(133.19, abs=1e-2)

    problem.check_partials(compact_print=True)


def test_compute_shell_mass():
    """Tests fuselage shell weight computation from sample XML data."""
    # Research independent input value in .xml file
    ivc = get_indep_var_comp(list_inputs(ComputeShell()), __file__, XML_FILE)

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(ComputeShell(), ivc)
    assert problem["data:weight:airframe:fuselage:shell:mass"] == pytest.approx(120.07, abs=1e-2)
    assert problem["data:weight:airframe:fuselage:shell:added_weight_ratio"] == pytest.approx(
        1.92, abs=1e-2
    )
    assert problem["data:weight:airframe:fuselage:shell:area_density"] == pytest.approx(
        2.83, abs=1e-2
    )
    assert problem["data:loads:fuselage:inertia"] == pytest.approx(0.00108963, rel=1e-2)
    assert problem["data:loads:fuselage:sigmaMh"] == pytest.approx(1.617e8, rel=1e-2)
    assert problem.get_val("data:geometry:fuselage:skin_thickness", units="mm") == pytest.approx(
        0.5753, abs=1e-4
    )


def test_compute_cone_mass():
    """Tests fuselage cone weight computation from sample XML data."""
    # Research independent input value in .xml file
    ivc = get_indep_var_comp(list_inputs(ComputeTailCone()), __file__, XML_FILE)

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(ComputeTailCone(), ivc)
    assert problem["data:weight:airframe:fuselage:cone:mass"] == pytest.approx(13.95, abs=1e-2)


def test_compute_windows_mass():
    """Tests fuselage windows weight computation from sample XML data."""
    # Research independent input value in .xml file
    ivc = get_indep_var_comp(list_inputs(ComputeWindows()), __file__, XML_FILE)

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(ComputeWindows(), ivc)
    assert problem["data:weight:airframe:fuselage:windows:mass"] == pytest.approx(39.21, abs=1e-2)


def test_compute_insulation_mass():
    """Tests fuselage insulation weight computation from sample XML data."""
    # Research independent input value in .xml file
    ivc = get_indep_var_comp(list_inputs(ComputeInsulation()), __file__, XML_FILE)

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(ComputeInsulation(), ivc)
    assert problem["data:weight:airframe:fuselage:insulation:mass"] == pytest.approx(
        55.00, abs=1e-2
    )


def test_compute_floor_mass():
    """Tests fuselage floor weight computation from sample XML data."""
    # Research independent input value in .xml file
    ivc = get_indep_var_comp(list_inputs(ComputeFloor()), __file__, XML_FILE)

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(ComputeFloor(), ivc)
    assert problem["data:weight:airframe:fuselage:floor:mass"] == pytest.approx(32.09, abs=1e-2)


def test_compute_nlg_hatch_mass():
    """Tests NLG hatch weight computation from sample XML data."""
    # Research independent input value in .xml file
    ivc = get_indep_var_comp(list_inputs(ComputeNLGHatch()), __file__, XML_FILE)

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(ComputeNLGHatch(), ivc)
    assert problem["data:weight:airframe:fuselage:nlg_hatch:mass"] == pytest.approx(11.56, abs=1e-2)


def test_compute_doors_mass():
    """Tests fuselage doors weight computation from sample XML data."""
    # Research independent input value in .xml file
    ivc = get_indep_var_comp(list_inputs(ComputeDoors()), __file__, XML_FILE)

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(ComputeDoors(), ivc)
    assert problem["data:weight:airframe:fuselage:doors:mass"] == pytest.approx(61.97, abs=1e-2)


def test_compute_wing_fuselage_connection_mass():
    """Tests wing/fuselage weight computation from sample XML data."""
    # Research independent input value in .xml file
    ivc = get_indep_var_comp(list_inputs(ComputeWingFuselageConnection()), __file__, XML_FILE)

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(ComputeWingFuselageConnection(), ivc)
    assert problem["data:weight:airframe:fuselage:wing_fuselage_connection:mass"] == pytest.approx(
        38.67, abs=1e-2
    )


def test_compute_engine_support_mass():
    """Tests engine support weight computation from sample XML data."""
    # Research independent input value in .xml file
    ivc = get_indep_var_comp(list_inputs(ComputeEngineSupport()), __file__, XML_FILE)

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(ComputeEngineSupport(), ivc)
    assert problem["data:weight:airframe:fuselage:engine_support:mass"] == pytest.approx(
        8.31, abs=1e-2
    )


def test_compute_bulkhead_mass():
    """Tests fuselage bulkhead weight computation from sample XML data."""
    # Research independent input value in .xml file
    ivc = get_indep_var_comp(list_inputs(ComputeBulkhead()), __file__, XML_FILE)

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(ComputeBulkhead(), ivc)
    assert problem["data:weight:airframe:fuselage:bulkhead:mass"] == pytest.approx(40.43, abs=1e-2)


def test_compute_additional_horizontal_bending_mass():
    """Tests fuselage added horizontal bending material weight computation from sample XML data."""
    # Research independent input value in .xml file
    ivc = get_indep_var_comp(list_inputs(ComputeAddBendingMassHorizontal()), __file__, XML_FILE)

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(ComputeAddBendingMassHorizontal(), ivc)
    assert problem["data:weight:airframe:fuselage:additional_mass:horizontal"] == pytest.approx(
        0.0, abs=1e-2
    )


def test_compute_additional_vertical_bending_mass():
    """Tests fuselage added vertical bending material weight computation from sample XML data."""
    # Research independent input value in .xml file
    ivc = get_indep_var_comp(list_inputs(ComputeAddBendingMassVertical()), __file__, XML_FILE)

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(ComputeAddBendingMassVertical(), ivc)
    assert problem["data:weight:airframe:fuselage:additional_mass:vertical"] == pytest.approx(
        0.0, abs=1e-2
    )


def test_compute_fuselage_mass_analytical():
    """Tests fuselage weight analytical computation from sample XML data."""
    # Research independent input value in .xml file
    ivc = get_indep_var_comp(list_inputs(ComputeFuselageMassAnalytical()), __file__, XML_FILE)

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(ComputeFuselageMassAnalytical(), ivc)
    assert problem["data:weight:airframe:fuselage:mass"] == pytest.approx(421.31, abs=1e-2)


def test_compute_empennage_weight():
    """Tests empennage weight computation from sample XML data."""
    # Research independent input value in .xml file
    ivc = get_indep_var_comp(list_inputs(ComputeTailWeight()), __file__, XML_FILE)

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(ComputeTailWeight(), ivc)
    weight_a31 = problem.get_val("data:weight:airframe:horizontal_tail:mass", units="kg")
    assert weight_a31 == pytest.approx(38.57, abs=1e-2)
    weight_a32 = problem.get_val("data:weight:airframe:vertical_tail:mass", units="kg")
    assert weight_a32 == pytest.approx(22.95, abs=1e-2)


def test_compute_empennage_weight_gd():
    """Tests empennage weight computation from sample XML data."""
    # Research independent input value in .xml file
    ivc = get_indep_var_comp(list_inputs(ComputeTailWeightGD()), __file__, XML_FILE)

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(ComputeTailWeightGD(), ivc)
    weight_a31 = problem.get_val("data:weight:airframe:horizontal_tail:mass", units="kg")
    assert weight_a31 == pytest.approx(25.62, abs=1e-2)
    weight_a32 = problem.get_val("data:weight:airframe:vertical_tail:mass", units="kg")
    assert weight_a32 == pytest.approx(21.58, abs=1e-2)


def test_compute_empennage_weight_torenbeek_gd():
    """Tests empennage weight computation from sample XML data."""
    # Research independent input value in .xml file
    ivc = get_indep_var_comp(list_inputs(ComputeTailWeightTorenbeekGD()), __file__, XML_FILE)

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(ComputeTailWeightTorenbeekGD(), ivc)
    weight_a31 = problem.get_val("data:weight:airframe:horizontal_tail:mass", units="kg")
    assert weight_a31 == pytest.approx(58.25, abs=1e-2)
    weight_a32 = problem.get_val("data:weight:airframe:vertical_tail:mass", units="kg")
    assert weight_a32 == pytest.approx(21.58, abs=1e-2)


def test_compute_flight_controls_weight():
    """Tests flight controls weight computation from sample XML data."""
    # Research independent input value in .xml file
    ivc = get_indep_var_comp(list_inputs(ComputeFlightControlsWeight()), __file__, XML_FILE)

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(ComputeFlightControlsWeight(), ivc)
    weight_a4 = problem.get_val("data:weight:airframe:flight_controls:mass", units="kg")
    assert weight_a4 == pytest.approx(71.08, abs=1e-2)


def test_compute_flight_controls_weight_flops():
    """Tests flight controls weight computation from sample XML data."""
    # Research independent input value in .xml file
    ivc = get_indep_var_comp(list_inputs(ComputeFlightControlsWeightFLOPS()), __file__, XML_FILE)

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(ComputeFlightControlsWeightFLOPS(), ivc)
    weight_a4 = problem.get_val("data:weight:airframe:flight_controls:mass", units="kg")
    assert weight_a4 == pytest.approx(60.99, abs=1e-2)


def test_compute_landing_gear_weight():
    """Tests landing gear weight computation from sample XML data."""
    # Research independent input value in .xml file
    ivc = get_indep_var_comp(list_inputs(ComputeLandingGearWeight()), __file__, XML_FILE)

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(ComputeLandingGearWeight(), ivc)
    weight_a51 = problem.get_val("data:weight:airframe:landing_gear:main:mass", units="kg")
    assert weight_a51 == pytest.approx(114.19, abs=1e-2)
    weight_a52 = problem.get_val("data:weight:airframe:landing_gear:front:mass", units="kg")
    assert weight_a52 == pytest.approx(39.16, abs=1e-2)


def test_compute_paint_weight():
    """Tests landing gear weight computation from sample XML data."""
    # Research independent input value in .xml file
    ivc = get_indep_var_comp(list_inputs(ComputePaintWeight()), __file__, XML_FILE)

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(ComputePaintWeight(), ivc)
    weight_a7 = problem.get_val("data:weight:airframe:paint:mass", units="kg")
    assert weight_a7 == pytest.approx(32.47, abs=1e-2)


def test_compute_airframe_weight():
    """Tests airframe weight computation from sample XML data."""
    # Research independent input value in .xml file
    ivc = get_indep_var_comp(list_inputs(AirframeWeight()), __file__, XML_FILE)

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(AirframeWeight(), ivc)
    weight_a = problem.get_val("data:weight:airframe:mass", units="kg")
    assert weight_a == pytest.approx(870.06, abs=1e-2)


def test_compute_oil_weight():
    """Tests engine weight computation from sample XML data."""
    # Research independent input value in .xml file
    ivc = get_indep_var_comp(
        list_inputs(ComputeOilWeight(propulsion_id=ENGINE_WRAPPER)), __file__, XML_FILE
    )

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(ComputeOilWeight(propulsion_id=ENGINE_WRAPPER), ivc)
    weight_b1_2 = problem.get_val("data:weight:propulsion:engine_oil:mass", units="kg")
    assert weight_b1_2 == pytest.approx(4.85, abs=1e-2)


def test_compute_engine_weight():
    """Tests engine weight computation from sample XML data."""
    # Research independent input value in .xml file
    ivc = get_indep_var_comp(
        list_inputs(ComputeEngineWeight(propulsion_id=ENGINE_WRAPPER)), __file__, XML_FILE
    )

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(ComputeEngineWeight(propulsion_id=ENGINE_WRAPPER), ivc)
    weight_b1 = problem.get_val("data:weight:propulsion:engine:mass", units="kg")
    assert weight_b1 == pytest.approx(289.51, abs=1e-2)


def test_compute_engine_weight_raymer():
    """Tests engine weight computation from sample XML data."""
    # Research independent input value in .xml file
    ivc = get_indep_var_comp(
        list_inputs(ComputeEngineWeightRaymer(propulsion_id=ENGINE_WRAPPER)), __file__, XML_FILE
    )

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(ComputeEngineWeightRaymer(propulsion_id=ENGINE_WRAPPER), ivc)
    weight_b1 = problem.get_val("data:weight:propulsion:engine:mass", units="kg")
    assert weight_b1 == pytest.approx(330.31, abs=1e-2)


def test_compute_fuel_lines_weight():
    """Tests fuel lines weight computation from sample XML data."""
    # Research independent input value in .xml file
    ivc = get_indep_var_comp(list_inputs(ComputeFuelLinesWeight()), __file__, XML_FILE)

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(ComputeFuelLinesWeight(), ivc)
    weight_b2 = problem.get_val("data:weight:propulsion:fuel_lines:mass", units="kg")
    assert weight_b2 == pytest.approx(63.03, abs=1e-2)


def test_compute_fuel_lines_weight_flops():
    """Tests fuel lines weight computation from sample XML data."""
    # Research independent input value in .xml file
    ivc = get_indep_var_comp(list_inputs(ComputeFuelLinesWeightFLOPS()), __file__, XML_FILE)

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(ComputeFuelLinesWeightFLOPS(), ivc)
    weight_b2 = problem.get_val("data:weight:propulsion:fuel_lines:mass", units="kg")
    assert weight_b2 == pytest.approx(38.91, abs=1e-2)


def test_compute_unusable_fuel_weight():
    """Tests engine weight computation from sample XML data."""
    # Research independent input value in .xml file
    ivc = get_indep_var_comp(
        list_inputs(ComputeUnusableFuelWeight(propulsion_id=ENGINE_WRAPPER)), __file__, XML_FILE
    )

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(ComputeUnusableFuelWeight(propulsion_id=ENGINE_WRAPPER), ivc)
    weight_b3 = problem.get_val("data:weight:propulsion:unusable_fuel:mass", units="kg")
    assert weight_b3 == pytest.approx(41.58, abs=1e-2)


def test_compute_propulsion_weight():
    """Tests propulsion weight computation from sample XML data."""
    # Research independent input value in .xml file
    ivc = get_indep_var_comp(
        list_inputs(PropulsionWeight(propulsion_id=ENGINE_WRAPPER)), __file__, XML_FILE
    )

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(PropulsionWeight(propulsion_id=ENGINE_WRAPPER), ivc)
    weight_b = problem.get_val("data:weight:propulsion:mass", units="kg")
    assert weight_b == pytest.approx(352.55, abs=1e-2)


def test_compute_avionics_systems_weight():
    """Tests navigation systems weight computation from sample XML data."""
    # Research independent input value in .xml file
    ivc = get_indep_var_comp(list_inputs(ComputeAvionicsSystemsWeight()), __file__, XML_FILE)

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(ComputeAvionicsSystemsWeight(), ivc)
    weight_c3 = problem.get_val("data:weight:systems:avionics:mass", units="kg")
    assert weight_c3 == pytest.approx(89.81, abs=1e-2)


def test_compute_avionics_systems_weight_from_uninstalled():
    """Tests navigation systems weight computation from sample XML data"""

    # Research independent input value in .xml file
    ivc = get_indep_var_comp(
        list_inputs(ComputeAvionicsSystemsWeightFromUninstalled()), __file__, XML_FILE
    )
    ivc.add_output("data:weight:systems:avionics:mass_uninstalled", val=45.0, units="lbm")

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(ComputeAvionicsSystemsWeightFromUninstalled(), ivc)
    weight_c3 = problem.get_val("data:weight:systems:avionics:mass", units="kg")
    assert weight_c3 == pytest.approx(33.37, abs=1e-2)


def test_compute_electric_power_system_weight():
    """Tests electric power system weight computation from sample XML data."""

    # Research independent input value in .xml file
    ivc = get_indep_var_comp(list_inputs(ComputeElectricWeight()), __file__, XML_FILE)

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(ComputeElectricWeight(), ivc)
    weight_c12 = problem.get_val("data:weight:systems:power:electric_systems:mass", units="kg")
    assert weight_c12 == pytest.approx(101.64, abs=1e-2)


def test_compute_hydraulic_power_system_weight():
    """Tests hydraulic power system weight computation from sample XML data."""

    # Research independent input value in .xml file
    ivc = get_indep_var_comp(list_inputs(ComputeHydraulicWeight()), __file__, XML_FILE)

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(ComputeHydraulicWeight(), ivc)
    weight_c13 = problem.get_val("data:weight:systems:power:hydraulic_systems:mass", units="kg")
    assert weight_c13 == pytest.approx(23.51, abs=1e-2)


def test_compute_life_support_systems_weight():
    """Tests life support systems weight computation from sample XML data."""

    # Research independent input value in .xml file
    ivc = get_indep_var_comp(list_inputs(ComputeLifeSupportSystemsWeight()), __file__, XML_FILE)

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(ComputeLifeSupportSystemsWeight(), ivc)
    weight_c21 = problem.get_val("data:weight:systems:life_support:insulation:mass", units="kg")
    assert weight_c21 == pytest.approx(0.0, abs=1e-2)
    weight_c22 = problem.get_val(
        "data:weight:systems:life_support:air_conditioning:mass", units="kg"
    )
    assert weight_c22 == pytest.approx(97.74, abs=1e-2)
    weight_c23 = problem.get_val("data:weight:systems:life_support:de_icing:mass", units="kg")
    assert weight_c23 == pytest.approx(0.0, abs=1e-2)
    weight_c24 = problem.get_val(
        "data:weight:systems:life_support:internal_lighting:mass", units="kg"
    )
    assert weight_c24 == pytest.approx(0.0, abs=1e-2)
    weight_c25 = problem.get_val(
        "data:weight:systems:life_support:seat_installation:mass", units="kg"
    )
    assert weight_c25 == pytest.approx(0.0, abs=1e-2)
    weight_c26 = problem.get_val("data:weight:systems:life_support:fixed_oxygen:mass", units="kg")
    assert weight_c26 == pytest.approx(11.16, abs=1e-2)
    weight_c27 = problem.get_val("data:weight:systems:life_support:security_kits:mass", units="kg")
    assert weight_c27 == pytest.approx(0.0, abs=1e-2)


def test_compute_life_support_systems_weight_flops():
    """Tests life support systems weight computation from sample XML data."""

    # Research independent input value in .xml file
    ivc = get_indep_var_comp(
        list_inputs(ComputeLifeSupportSystemsWeightFLOPS()), __file__, XML_FILE
    )

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(ComputeLifeSupportSystemsWeightFLOPS(), ivc)
    weight_c21 = problem.get_val("data:weight:systems:life_support:insulation:mass", units="kg")
    assert weight_c21 == pytest.approx(0.0, abs=1e-2)
    weight_c22 = problem.get_val(
        "data:weight:systems:life_support:air_conditioning:mass", units="kg"
    )
    assert weight_c22 == pytest.approx(60.71, abs=1e-2)
    weight_c23 = problem.get_val("data:weight:systems:life_support:de_icing:mass", units="kg")
    assert weight_c23 == pytest.approx(25.06, abs=1e-2)
    weight_c24 = problem.get_val(
        "data:weight:systems:life_support:internal_lighting:mass", units="kg"
    )
    assert weight_c24 == pytest.approx(0.0, abs=1e-2)
    weight_c25 = problem.get_val(
        "data:weight:systems:life_support:seat_installation:mass", units="kg"
    )
    assert weight_c25 == pytest.approx(0.0, abs=1e-2)
    weight_c26 = problem.get_val("data:weight:systems:life_support:fixed_oxygen:mass", units="kg")
    assert weight_c26 == pytest.approx(11.16, abs=1e-2)
    weight_c27 = problem.get_val("data:weight:systems:life_support:security_kits:mass", units="kg")
    assert weight_c27 == pytest.approx(0.0, abs=1e-2)


def test_compute_recording_systems_weight():
    """Tests power systems weight computation from sample XML data"""

    # Research independent input value in .xml file
    ivc = get_indep_var_comp(list_inputs(ComputeRecordingSystemsWeight()), __file__, XML_FILE)

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(ComputeRecordingSystemsWeight(), ivc)
    weight_c12 = problem.get_val("data:weight:systems:recording:mass", units="kg")
    assert weight_c12 == pytest.approx(0.0, abs=1e-2)


def test_compute_systems_weight():
    """Tests propulsion weight computation from sample XML data."""

    # Research independent input value in .xml file
    ivc = get_indep_var_comp(list_inputs(SystemsWeight()), __file__, XML_FILE)

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(SystemsWeight(), ivc)
    weight_b = problem.get_val("data:weight:systems:mass", units="kg")
    assert weight_b == pytest.approx(323.88, abs=1e-2)


def test_compute_passenger_seats_weight():
    """Tests passenger seats weight computation from sample XML data."""

    # Research independent input value in .xml file
    ivc = get_indep_var_comp(list_inputs(ComputePassengerSeatsWeight()), __file__, XML_FILE)

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(ComputePassengerSeatsWeight(), ivc)
    weight_d2 = problem.get_val("data:weight:furniture:passenger_seats:mass", units="kg")
    assert weight_d2 == pytest.approx(
        113.43, abs=1e-2
    )  # additional 2 pilots seats (differs from old version)


def test_compute_furniture_weight():
    """Tests propulsion weight computation from sample XML data."""

    # Research independent input value in .xml file
    ivc = get_indep_var_comp(list_inputs(FurnitureWeight()), __file__, XML_FILE)

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(FurnitureWeight(), ivc)
    weight_b = problem.get_val("data:weight:furniture:mass", units="kg")
    assert weight_b == pytest.approx(113.43, abs=1e-2)


def test_evaluate_owe():
    """Tests a simple evaluation of Operating Weight Empty from sample XML data."""

    ivc = get_indep_var_comp(
        list_inputs(ComputeOperatingWeightEmpty(propulsion_id=ENGINE_WRAPPER)), __file__, XML_FILE
    )

    # noinspection PyTypeChecker
    mass_computation = run_system(ComputeOperatingWeightEmpty(propulsion_id=ENGINE_WRAPPER), ivc)

    print(mass_computation.get_val("data:weight:systems:mass", units="kg"))
    oew = mass_computation.get_val("data:weight:aircraft:OWE", units="kg")
    assert oew == pytest.approx(1669, abs=1)


def test_loop_compute_owe():
    """Tests a weight computation loop matching the max payload criterion."""

    # Payload is computed from NPAX_design
    ivc = get_indep_var_comp(
        list_inputs(MassBreakdown(propulsion_id=ENGINE_WRAPPER, payload_from_npax=True)),
        __file__,
        XML_FILE,
    )

    # noinspection PyTypeChecker
    mass_computation = run_system(
        MassBreakdown(propulsion_id=ENGINE_WRAPPER, payload_from_npax=True),
        ivc,
        check=True,
    )
    oew = mass_computation.get_val("data:weight:aircraft:OWE", units="kg")
    assert oew == pytest.approx(1648, abs=1)


def test_compute_web_mass():
    # Research independent input value in .xml file
    ivc = get_indep_var_comp(list_inputs(ComputeWebMass()), __file__, XML_FILE)

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(ComputeWebMass(), ivc)
    assert problem["data:weight:airframe:wing:web:mass:max_fuel_in_wing"] == pytest.approx(
        5.75, abs=1e-2
    )

    ivc2 = get_indep_var_comp(
        list_inputs(ComputeWebMass(min_fuel_in_wing=True)), __file__, XML_FILE
    )

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(ComputeWebMass(min_fuel_in_wing=True), ivc2)
    assert problem["data:weight:airframe:wing:web:mass:min_fuel_in_wing"] == pytest.approx(
        6.09, abs=1e-2
    )


def test_compute_upper_flange_mass():
    # Research independent input value in .xml file
    ivc = get_indep_var_comp(list_inputs(ComputeUpperFlange()), __file__, XML_FILE)

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(ComputeUpperFlange(), ivc)
    assert problem["data:weight:airframe:wing:upper_flange:mass:max_fuel_in_wing"] == pytest.approx(
        30.79, abs=1e-2
    )

    ivc2 = get_indep_var_comp(
        list_inputs(ComputeUpperFlange(min_fuel_in_wing=True)), __file__, XML_FILE
    )

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(ComputeUpperFlange(min_fuel_in_wing=True), ivc2)
    assert problem["data:weight:airframe:wing:upper_flange:mass:min_fuel_in_wing"] == pytest.approx(
        33.23, abs=1e-2
    )


def test_compute_lower_flange_mass():
    # Research independent input value in .xml file
    ivc = get_indep_var_comp(list_inputs(ComputeLowerFlange()), __file__, XML_FILE)

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(ComputeLowerFlange(), ivc)
    assert problem["data:weight:airframe:wing:lower_flange:mass:max_fuel_in_wing"] == pytest.approx(
        23.05, abs=1e-2
    )

    ivc2 = get_indep_var_comp(
        list_inputs(ComputeLowerFlange(min_fuel_in_wing=True)), __file__, XML_FILE
    )

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(ComputeLowerFlange(min_fuel_in_wing=True), ivc2)
    assert problem["data:weight:airframe:wing:lower_flange:mass:min_fuel_in_wing"] == pytest.approx(
        24.87, abs=1e-2
    )


def test_compute_skin_mass():
    # Research independent input value in .xml file
    ivc = get_indep_var_comp(list_inputs(ComputeSkinMass()), __file__, XML_FILE)

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(ComputeSkinMass(), ivc)
    assert problem["data:weight:airframe:wing:skin:mass"] == pytest.approx(147.88, abs=1e-2)


def test_compute_ribs_mass():
    # Research independent input value in .xml file
    ivc = get_indep_var_comp(list_inputs(ComputeRibsMass()), __file__, XML_FILE)

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(ComputeRibsMass(), ivc)
    assert problem["data:weight:airframe:wing:ribs:mass"] == pytest.approx(19.10, abs=1e-2)


def test_compute_misc_mass():
    # Research independent input value in .xml file
    ivc = get_indep_var_comp(list_inputs(ComputeMiscMass()), __file__, XML_FILE)

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(ComputeMiscMass(), ivc)
    assert problem["data:weight:airframe:wing:misc:mass"] == pytest.approx(40.53, abs=1e-2)


def test_compute_primary_mass():
    # Research independent input value in .xml file
    ivc = get_indep_var_comp(list_inputs(ComputePrimaryMass()), __file__, XML_FILE)

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(ComputePrimaryMass(), ivc)
    assert problem["data:weight:airframe:wing:primary_structure:mass"] == pytest.approx(
        274.32, abs=1e-2
    )


def test_compute_secondary_mass():

    # Research independent input value in .xml file
    ivc = get_indep_var_comp(list_inputs(ComputeSecondaryMass()), __file__, XML_FILE)

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(ComputeSecondaryMass(), ivc)
    assert problem["data:weight:airframe:wing:secondary_structure:mass"] == pytest.approx(
        91.44, abs=1e-2
    )


def test_update_wing_mass():
    # Research independent input value in .xml file
    ivc = get_indep_var_comp(list_inputs(UpdateWingMass()), __file__, XML_FILE)

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(UpdateWingMass(), ivc)
    assert problem["data:weight:airframe:wing:mass"] == pytest.approx(365.77, abs=1e-2)


def test_compute_wing_mass_analytical():
    # Research independent input value in .xml file
    ivc = get_indep_var_comp(list_inputs(ComputeWingMassAnalytical()), __file__, XML_FILE)

    # Run problem and check obtained value(s) is/(are) correct
    problem = run_system(ComputeWingMassAnalytical(), ivc)
    assert problem["data:weight:airframe:wing:mass"] == pytest.approx(362.42, abs=1e-2)
