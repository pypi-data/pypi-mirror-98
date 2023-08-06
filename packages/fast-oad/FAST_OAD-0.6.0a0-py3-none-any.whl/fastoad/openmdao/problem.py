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

from fastoad.io import VariableIO
from fastoad.openmdao.validity_checker import ValidityDomainChecker
from fastoad.openmdao.variables import VariableList

INPUT_SYSTEM_NAME = "inputs"


class FASTOADProblem(om.Problem):
    """Vanilla OpenMDAO Problem except that it can write its outputs to a file.

    It also runs :class:`~fastoad.openmdao.validity_checker.ValidityDomainChecker`
    after each :meth:`run_model` or :meth:`run_driver`
    (but it does nothing if no check has been registered).

    A classical usage of this class would be::

        problem = FASTOADProblem()  # instantiation
        [... configuration as for any OpenMDAO problem ...]

        problem.input_file_path = "inputs.xml"
        problem.output_file_path = "outputs.xml"
        problem.write_needed_inputs()  # writes the input file (defined above) with
                                       # needed variables so user can fill it with proper values
        # or
        problem.write_needed_inputs('previous.xml')  # writes the input file with needed variables
                                                     # and values taken from provided file when
                                                     # available
        problem.read_inputs()    # reads the input file
        problem.run_driver()     # runs the OpenMDAO problem
        problem.write_outputs()  # writes the output file
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.input_file_path = None
        self.output_file_path = None

    def run_model(self, case_prefix=None, reset_iter_counts=True):
        status = super().run_model(case_prefix, reset_iter_counts)
        ValidityDomainChecker.check_problem_variables(self)
        return status

    def run_driver(self, case_prefix=None, reset_iter_counts=True):
        status = super().run_driver(case_prefix, reset_iter_counts)
        ValidityDomainChecker.check_problem_variables(self)
        return status

    def write_outputs(self):
        """
        Writes all outputs in the configured output file.
        """
        if self.output_file_path:
            writer = VariableIO(self.output_file_path)
            variables = VariableList.from_problem(self, promoted_only=True)
            writer.write(variables)
