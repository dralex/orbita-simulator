# -----------------------------------------------------------------------------
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# The Orbita Simulator
# The Earth orbit simulation model (v2)
#
# The simulator missions implementation: The Molniya Telecom System
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

class MolniyaMission(Mission):
    name = constants.MISSION_MOLNIYA

    acceptable_bandwidth = 1.0 * 1024 * 1024
    acceptable_duration = 8.0 * 60 * 60
    acceptable_count = 2
    max_duration = 24.0 * 60 * 60

    def __init__(self, global_parameters):
        Mission.__init__(self, global_parameters)
        self.session_durations = []
        self.on_air = False
        self.transferred_data = 0.0

    def init(self, probe, initial_tick, lang):
        global _ # pylint: disable=W0603
        _ = lang

        orient = probe.systems[constants.SUBSYSTEM_ORIENTATION]

        orient.planet_rotation = True

        self.session_durations = []
        self.on_air = False
        self.transferred_data = 0.0

    def step(self, probe, tick):
        radio = probe.systems[constants.SUBSYSTEM_RADIO]

        if radio.transmitting and radio.max_bandwidth >= self.acceptable_bandwidth:
            if self.on_air and self.session_durations[-1] < self.max_duration:
                self.session_durations[-1] += tick
            else:
                self.session_durations.append(tick)

            self.on_air = True
            self.transferred_data += radio.max_bandwidth
        else:
            self.on_air = False

        if len(self.session_durations) >= self.acceptable_count:
            acceptable_session_durations = [duration for duration
                                            in self.session_durations
                                            if duration >= self.acceptable_duration]
            if len(acceptable_session_durations) >= self.acceptable_count:
                if not probe.success:
                    mission_log(probe, _('MISSION ACCOMPLISHED! The required telecommunication session completed.')) # pylint: disable=C0301
                    probe.success = True

                probe.session_count = len(acceptable_session_durations)
                probe.session_length = min(acceptable_session_durations) / (60 * 60)
                probe.success_score = None
                probe.success_timestamp = time.time()

data.available_missions[MolniyaMission.name] = MolniyaMission
