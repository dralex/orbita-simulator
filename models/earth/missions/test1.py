# -----------------------------------------------------------------------------
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# The Orbita Simulator
# The Earth orbit simulation model (v2)
#
# The simulator missions implementation: the Test mission 1
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

class TestLookMission(Mission):
    name = constants.MISSION_TEST_LOOK

    normal_precision = 1.0

    def __init__(self, global_parameters):
        Mission.__init__(self, global_parameters)
        self.is_normal = False
        self.normal_start_angle = None
        self.normal_start_time = None

    def init(self, probe, initial_tick, lang):
        global _ # pylint: disable=W0603
        _ = lang
        self.is_normal = False
        self.normal_start_angle = None
        self.normal_start_time = None

    def step(self, probe, tick):
        navig = probe.systems[constants.SUBSYSTEM_NAVIGATION]
        orient = probe.systems[constants.SUBSYSTEM_ORIENTATION]

        is_normal = abs(orient.off_nadir_angle) <= self.normal_precision

        if is_normal and not self.is_normal:
            self.normal_start_time = probe.time()
            self.normal_start_angle = navig.angle

        if not is_normal and self.is_normal:
            self.normal_start_time = None
            self.normal_start_angle = None

        self.is_normal = is_normal

        if self.is_normal:
            if (((probe.time() - self.normal_start_time > 600) and
                 abs(navig.angle - self.normal_start_angle) < 1.0)):
                mission_log(probe, _('MISSION ACCOMPLISHED! The probe completed the orbital revolution with the normal orientation.')) # pylint: disable=C0301
                probe.success = True
                probe.success_timestamp = time.time()
                probe.completed = True

data.available_missions[TestLookMission.name] = TestLookMission
