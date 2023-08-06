"""
Aero computation for landing phase
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

import numpy as np
import openmdao.api as om

from fastoad.model_base.options import OpenMdaoOptionDispatcherGroup
from fastoad.utils.physics import Atmosphere
from .components.compute_max_cl_landing import ComputeMaxClLanding
from .components.high_lift_aero import ComputeDeltaHighLift
from .external.xfoil import XfoilPolar
from .external.xfoil.xfoil_polar import OPTION_XFOIL_EXE_PATH


class AerodynamicsLanding(OpenMdaoOptionDispatcherGroup):
    """
    Computes aerodynamic characteristics at landing.

    - Computes CL and CD increments due to high-lift devices at landing.
    - Computes maximum CL of the aircraft in landing conditions.

    Maximum 2D CL without high-lift is computed using XFoil (or provided as input if option
    use_xfoil is set to False). 3D CL is deduced using sweep angle.

    Contribution of high-lift devices is modelled according to their geometry (span and chord ratio)
    and their deflection angles.

    Options:
      - use_xfoil:
         - if True, maximum 2D CL without high-lift aerodynamics:aircraft:landing:CL_max_clean_2D
           is computed using XFOIL
         - if False, aerodynamics:aircraft:landing:CL_max_clean_2D must be provided as input (but
           process is faster)
      - alpha_min, alpha_max:
         - used if use_xfoil is True. Sets the alpha range that is explored to find maximum 2D CL
           without high-lift
      - xfoil_exe_path:
         - the path to the XFOIL executable. Needed for non-Windows OS.
    """

    def initialize(self):
        self.options.declare("use_xfoil", default=True, types=bool)
        self.options.declare("xfoil_alpha_min", default=0.0, types=float)
        self.options.declare("xfoil_alpha_max", default=30.0, types=float)
        self.options.declare("xfoil_iter_limit", default=500, types=int)
        self.options.declare(OPTION_XFOIL_EXE_PATH, default="", types=str, allow_none=True)

    def setup(self):
        self.add_subsystem("mach_reynolds", ComputeMachReynolds(), promotes=["*"])
        if self.options["use_xfoil"]:
            start = self.options["xfoil_alpha_min"]
            end = self.options["xfoil_alpha_max"]
            iter_limit = self.options["xfoil_iter_limit"]
            self.add_subsystem(
                "xfoil_run",
                XfoilPolar(alpha_start=start, alpha_end=end, iter_limit=iter_limit),
                promotes=["data:geometry:wing:thickness_ratio"],
            )
        self.add_subsystem("CL_2D_to_3D", Compute3DMaxCL(), promotes=["*"])
        self.add_subsystem(
            "delta_cl_landing", ComputeDeltaHighLift(landing_flag=True), promotes=["*"]
        )
        self.add_subsystem("compute_max_cl_landing", ComputeMaxClLanding(), promotes=["*"])

        if self.options["use_xfoil"]:
            self.connect("data:aerodynamics:aircraft:landing:mach", "xfoil_run.xfoil:mach")
            self.connect("data:aerodynamics:aircraft:landing:reynolds", "xfoil_run.xfoil:reynolds")
            self.connect(
                "xfoil_run.xfoil:CL_max_2D", "data:aerodynamics:aircraft:landing:CL_max_clean_2D"
            )


class ComputeMachReynolds(om.ExplicitComponent):
    """
    Mach and Reynolds computation
    """

    def setup(self):
        self.add_input("data:geometry:wing:MAC:length", val=np.nan, units="m")
        self.add_input("data:TLAR:approach_speed", val=np.nan, units="m/s")
        self.add_output("data:aerodynamics:aircraft:landing:mach")
        self.add_output("data:aerodynamics:aircraft:landing:reynolds")

        self.declare_partials("*", "*", method="fd")

    def compute(self, inputs, outputs, discrete_inputs=None, discrete_outputs=None):
        l0_wing = inputs["data:geometry:wing:MAC:length"]
        speed = inputs["data:TLAR:approach_speed"]

        atm = Atmosphere(0.0, 15.0)
        mach = speed / atm.speed_of_sound
        reynolds = atm.get_unitary_reynolds(mach) * l0_wing

        outputs["data:aerodynamics:aircraft:landing:mach"] = mach
        outputs["data:aerodynamics:aircraft:landing:reynolds"] = reynolds


class Compute3DMaxCL(om.ExplicitComponent):
    """
    Computes 3D max CL from 2D CL (XFOIL-computed) and sweep angle
    """

    def setup(self):
        self.add_input("data:geometry:wing:sweep_25", val=np.nan, units="rad")
        self.add_input("data:aerodynamics:aircraft:landing:CL_max_clean_2D", val=np.nan)

        self.add_output("data:aerodynamics:aircraft:landing:CL_max_clean")

        self.declare_partials("*", "*", method="fd")

    def compute(self, inputs, outputs, discrete_inputs=None, discrete_outputs=None):
        sweep_25 = inputs["data:geometry:wing:sweep_25"]
        cl_max_2d = inputs["data:aerodynamics:aircraft:landing:CL_max_clean_2D"]
        outputs["data:aerodynamics:aircraft:landing:CL_max_clean"] = (
            cl_max_2d * 0.9 * np.cos(sweep_25)
        )
