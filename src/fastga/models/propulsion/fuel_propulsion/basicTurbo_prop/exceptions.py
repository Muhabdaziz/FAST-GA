"""Exceptions for basicIC_engine package."""


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


class FastBasicICEngineInconsistentInputParametersError(Exception):
    """
    Raised when provided parameter combination is incorrect.
    """


class FastBasicTPEngineImpossibleTurbopropGeometry(Exception):
    """
    Raised when the geometry of the turboprop can't be computed
    """


class FastBasicTPEngineUnknownLimit(Exception):
    """
    Raised when an unknown limit given to the turboprop
    """
