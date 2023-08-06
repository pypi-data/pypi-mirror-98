"""Classes for climb/descent segments."""
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

import logging
from copy import copy
from dataclasses import dataclass
from typing import Tuple, List

import pandas as pd
from scipy.constants import g, foot

from fastoad.base.flight_point import FlightPoint
from fastoad.utils.physics import AtmosphereSI
from .base import ManualThrustSegment
from ..exceptions import FastFlightSegmentIncompleteFlightPoint
from ..util import get_closest_flight_level

_LOGGER = logging.getLogger(__name__)  # Logger for this module


@dataclass
class AltitudeChangeSegment(ManualThrustSegment):
    """
    Computes a flight path segment where altitude is modified with constant speed.

    .. note:: **Setting speed**

        Constant speed may be:

        - constant true airspeed (TAS)
        - constant equivalent airspeed (EAS)
        - constant Mach number

        Target should have :code:`"constant"` as definition for one parameter among
        :code:`true_airspeed`, :code:`equivalent_airspeed` or :code:`mach`.
        All computed flight points will use the corresponding **start** value.
        The two other speed values will be computed accordingly.

        If not "constant" parameter is set, constant TAS is assumed.

    .. note:: **Setting target**

        Target can be an altitude, or a speed:

        - Target altitude can be a float value (in **meters**), or can be set to:

            - :attr:`OPTIMAL_ALTITUDE`: in that case, the target altitude will be the altitude
              where maximum lift/drag ratio is achieved for target speed, depending on current mass.
            - :attr:`OPTIMAL_FLIGHT_LEVEL`: same as above, except that altitude will be rounded to
              the nearest flight level (multiple of 100 feet).

        - For a speed target, as explained above, one value  TAS, EAS or Mach must be
          :code:`"constant"`. One of the two other ones can be set as target.

        In any case, the achieved value will be capped so it respects
        :attr:`maximum_flight_level`.

    """

    time_step: float = 2.0

    #: The maximum allowed flight level (i.e. multiple of 100 feet).
    maximum_flight_level: float = 500.0

    #: Using this value will tell to target the altitude with max lift/drag ratio.
    OPTIMAL_ALTITUDE = "optimal_altitude"  # pylint: disable=invalid-name # used as constant

    #: Using this value will tell to target the nearest flight level to altitude
    #: with max lift/drag ratio.
    OPTIMAL_FLIGHT_LEVEL = "optimal_flight_level"  # pylint: disable=invalid-name # used as constant

    def compute_from(self, start: FlightPoint) -> pd.DataFrame:
        self.complete_flight_point(start)  # needed to ensure all speed values are computed.

        if self.target.altitude is not None:
            if isinstance(self.target.altitude, str):
                # Target altitude will be modified along the process, so we keep track
                # of the original order in target CL, that is not used otherwise.
                self.target.CL = self.target.altitude  # pylint: disable=invalid-name
                # let's put a numerical, negative value in self.target.altitude to
                # ensure there will be no problem in self._get_distance_to_target()
                self.target.altitude = -1000.0
                self.interrupt_if_getting_further_from_target = False
            else:
                # Target altitude is fixed, back to original settings (in case
                # this instance is used more than once)
                self.target.CL = None
                self.interrupt_if_getting_further_from_target = True

        atm = AtmosphereSI(start.altitude)
        if self.target.equivalent_airspeed == self.CONSTANT_VALUE:
            start.true_airspeed = atm.get_true_airspeed(start.equivalent_airspeed)
        elif self.target.mach == self.CONSTANT_VALUE:
            start.true_airspeed = start.mach * atm.speed_of_sound

        return super().compute_from(start)

    def _get_distance_to_target(self, flight_points: List[FlightPoint]) -> float:
        current = flight_points[-1]

        # Max flight level is first priority
        max_authorized_altitude = self.maximum_flight_level * 100.0 * foot
        if current.altitude >= max_authorized_altitude:
            return max_authorized_altitude - current.altitude

        if self.target.CL:
            # Optimal altitude is based on a target Mach number, though target speed
            # may be specified as TAS or EAS. If so, Mach number has to be computed
            # for target altitude and speed.

            # First, as target speed is expected to be set to self.CONSTANT_VALUE for one
            # parameter. Let's get the real value from start point.
            target_speed = copy(self.target)
            for speed_param in ["true_airspeed", "equivalent_airspeed", "mach"]:
                if isinstance(getattr(target_speed, speed_param), str):
                    setattr(target_speed, speed_param, getattr(flight_points[0], speed_param))

            # Now, let's compute target Mach number
            atm = AtmosphereSI(max(self.target.altitude, current.altitude))
            if target_speed.equivalent_airspeed:
                target_speed.true_airspeed = atm.get_true_airspeed(target_speed.equivalent_airspeed)
            if target_speed.true_airspeed:
                target_speed.mach = target_speed.true_airspeed / atm.speed_of_sound

            # Now we compute optimal altitude
            optimal_altitude = self._get_optimal_altitude(
                current.mass, target_speed.mach, current.altitude
            )
            if self.target.CL == self.OPTIMAL_ALTITUDE:
                self.target.altitude = optimal_altitude
            else:  # self.target.CL == self.OPTIMAL_FLIGHT_LEVEL:
                self.target.altitude = get_closest_flight_level(
                    optimal_altitude, up_direction=False
                )

        if self.target.altitude is not None:
            return self.target.altitude - current.altitude
        if self.target.true_airspeed and self.target.true_airspeed != self.CONSTANT_VALUE:
            return self.target.true_airspeed - current.true_airspeed
        if (
            self.target.equivalent_airspeed
            and self.target.equivalent_airspeed != self.CONSTANT_VALUE
        ):
            return self.target.equivalent_airspeed - current.equivalent_airspeed
        if self.target.mach is not None and self.target.mach != self.CONSTANT_VALUE:
            return self.target.mach - current.mach

        raise FastFlightSegmentIncompleteFlightPoint(
            "No valid target definition for altitude change."
        )

    def _get_gamma_and_acceleration(self, mass, drag, thrust) -> Tuple[float, float]:
        gamma = (thrust - drag) / mass / g
        return gamma, 0.0
