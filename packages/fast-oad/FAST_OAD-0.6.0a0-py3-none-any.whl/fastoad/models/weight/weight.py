"""
Weight computation (mass and CG)
"""
#  This file is part of FAST-OAD : A framework for rapid Overall Aircraft Design
#  Copyright (C) 2021 ONERA & ISAE-SUPAERO
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

from fastoad.model_base.options import PAYLOAD_FROM_NPAX
from fastoad.models.weight.cg.cg import CG
from fastoad.models.weight.mass_breakdown import MassBreakdown


class Weight(om.Group):
    """
    Computes masses and Centers of Gravity for each part of the empty operating aircraft, among
    these 5 categories:
    airframe, propulsion, systems, furniture, crew

    This model uses MTOW as an input, as it allows to size some elements, but resulting OWE do
    not aim at being consistent with MTOW.

    Consistency between OWE and MTOW can be achieved by cycling with a model that computes MTOW
    from OWE, which should come from a mission computation that will assess needed block fuel.

    Options:
    - payload_from_npax: If True (default), payload masses will be computed from NPAX.
                         If False, design payload mass and maximum payload mass must be provided.

    """

    def initialize(self):
        self.options.declare(PAYLOAD_FROM_NPAX, types=bool, default=True)

    def setup(self):
        self.add_subsystem("cg", CG(), promotes=["*"])
        self.add_subsystem(
            "mass_breakdown",
            MassBreakdown(**{PAYLOAD_FROM_NPAX: self.options[PAYLOAD_FROM_NPAX]}),
            promotes=["*"],
        )
