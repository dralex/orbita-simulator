# -----------------------------------------------------------------------------
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# The Orbita Simulator
# The Earth orbit simulation model (v2)
#
# The simulator missions implementation: Growing Crystal on Orbit
#
# Copyright (C) 2015-2023 Alexey Fedoseev <aleksey@fedoseev.net>
# Copyright (C) 2016-2023 Ilya Tagunov <tagunil@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see https://www.gnu.org/licenses/
# -----------------------------------------------------------------------------

import time
import gettext

import data
import constants
from mission import Mission
from logger import mission_log

_ = gettext.gettext

class CrystalMission(Mission):
    name = constants.MISSION_CRYSTAL

    def __init__(self, global_parameters):
        Mission.__init__(self, global_parameters)
        self.landing_angle = None
        self.target_height = None
        self.target_diff = None
        self.full_orbit = None
        self.orbit_start_angle = None
        self.orbit_start_time = None

    def init(self, probe, initial_tick, lang):
        global _ # pylint: disable=W0603
        _ = lang

        navig = probe.systems[constants.SUBSYSTEM_NAVIGATION]

        planet_params = self.params.Planets[probe.planet]

        self.landing_angle = float(probe.xml.flight.mission.target_angle)
        self.target_height = (float(probe.xml.flight.mission.target_orbit) * 1000.0 +
                              float(planet_params.radius))
        self.target_diff = abs(navig.height - self.target_height)
        self.full_orbit = False
        self.orbit_start_angle = None
        self.orbit_start_time = None

    def step(self, probe, tick):
        navig = probe.systems[constants.SUBSYSTEM_NAVIGATION]
        load = probe.systems[constants.SUBSYSTEM_LOAD]

        self.target_diff = abs(navig.height - self.target_height)

        if not self.full_orbit:
            if load.running:
                if load.valid_environment:
                    load.valid_environment = (self.target_diff <= 1000.0)
                    load.valid_environment = (load.valid_environment and
                                              load.mode == constants.STATE_ON)

                    for s in probe.systems.values():
                        if s and (s.device.type not in (constants.SUBSYSTEM_CPU,
                                                        constants.SUBSYSTEM_LOAD,
                                                        constants.SUBSYSTEM_POWER,
                                                        constants.SUBSYSTEM_HEAT_CONTROL)):
                            load.valid_environment = (load.valid_environment and
                                                      (s.mode != constants.STATE_ON))

                if self.orbit_start_angle is None:
                    self.orbit_start_angle = navig.angle
                    self.orbit_start_time = probe.time()
                elif (((probe.time() - self.orbit_start_time > 600) and
                       (abs(navig.angle - self.orbit_start_angle) < 1.0))):
                    self.full_orbit = True

        if probe.landed:
            probe.success = self.full_orbit and load.valid_environment
            if probe.success:
                mission_log(probe, _('MISSION ACCOMPLISHED! The crystal has landed earth successfully.'))
                landing_error = abs(data.normalize_angle_difference(navig.angle -
                                                                    self.landing_angle))
                probe.landing_error = landing_error
#                perfect_landing_error = float(probe.xml.flight.mission.precision)
#                probe.success_score = constants.BASE_SCORE[constants.MISSION_CRYSTAL]
#                if landing_error > perfect_landing_error:
#                    probe.success_score *= math.sqrt(perfect_landing_error / landing_error)
                probe.success_timestamp = time.time()
                probe.completed = True

data.available_missions[CrystalMission.name] = CrystalMission
