# -----------------------------------------------------------------------------
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# The Orbita Simulator
# The Earth orbit simulation model (v2)
#
# The simulator missions implementation: the Test mission 3
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

import gettext

import data
import constants
from mission import Mission
from logger import mission_log

_ = gettext.gettext

class TestOrbitMission(Mission):
    name = constants.MISSION_TEST_ORBIT

    def __init__(self, global_parameters):
        Mission.__init__(self, global_parameters)
        self.target_height = None
        self.target_diff = None
        self.worst_target_diff = None
        self.orbit_start_angle = None
        self.orbit_start_time = None

    def init(self, probes, initial_tick, lang):
        global _ # pylint: disable=W0603
        _ = lang
        probe = probes.get()[0]

        navig = probe.systems[constants.SUBSYSTEM_NAVIGATION]

        planet_params = self.params.Planets[probe.planet]

        self.target_height = (float(probe.xml.flight.mission.target_orbit) * 1000.0 +
                              float(planet_params.radius))
        self.target_diff = abs(navig.height - self.target_height)
        self.worst_target_diff = None
        self.orbit_start_angle = None
        self.orbit_start_time = None

    def step(self, probes, tick):
        probe = probes.get()[0]
        navig = probe.systems[constants.SUBSYSTEM_NAVIGATION]
        engine = probe.systems[constants.SUBSYSTEM_ENGINE]

        self.target_diff = abs(navig.height - self.target_height)

        if engine.running or self.target_diff > 5000:
            self.worst_target_diff = None
            self.orbit_start_angle = None
            self.orbit_start_time = None
        else:
            if self.worst_target_diff is None or self.target_diff > self.worst_target_diff:
                self.worst_target_diff = self.target_diff

            if self.orbit_start_angle is None:
                self.orbit_start_angle = navig.angle
                self.orbit_start_time = probe.time()
            elif (((probe.time() - self.orbit_start_time > 600) and
                   abs(navig.angle - self.orbit_start_angle) < 1.0)):
                mission_log(probe, _('MISSION ACCOMPLISHED! The probe completed the revolution on the new orbit.')) # pylint: disable=C0301
                probe.orbit_diff = self.worst_target_diff
                probe.success = True
                probe.completed = True

data.available_missions[TestOrbitMission.name] = TestOrbitMission
