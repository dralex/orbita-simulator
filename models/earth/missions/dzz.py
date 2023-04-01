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
import math
import gettext

import data
import constants
from mission import Mission
from logger import debug_log, mission_log

_ = gettext.gettext

class DzzMission(Mission):
    name = constants.MISSION_DZZ

    perfect_offset_angle = 0.01
    perfect_incidence_angle = 0.01
    target_index = 0

    def __init__(self, global_parameters):
        Mission.__init__(self, global_parameters)
        self.target_angle = None
        self.target_height = None
        self.target_x = None
        self.target_y = None
        self.target_z = None

    def init(self, probe, initial_tick, lang):
        global _ # pylint: disable=W0603
        _ = lang

        planet_params = self.params.Planets[probe.planet]

        self.target_angle = float(probe.xml.flight.mission.target_angle)
        self.target_height = float(planet_params.radius)
        angle_rad = math.radians(self.target_angle)
        self.target_x = self.target_height * math.sin(angle_rad)
        self.target_y = self.target_height * math.cos(angle_rad)
        self.target_z = 0

    def step(self, probe, tick):
        navig = probe.systems[constants.SUBSYSTEM_NAVIGATION]
        orient = probe.systems[constants.SUBSYSTEM_ORIENTATION]
        radio = probe.systems[constants.SUBSYSTEM_RADIO]
        load = probe.systems[constants.SUBSYSTEM_LOAD]

        planet_params = self.params.Planets[probe.planet]

        direction = (self.target_x - navig.x,
                     self.target_y - navig.y,
                     self.target_z - navig.z)
        direction_angle = math.degrees(math.atan2(direction[1], direction[0]))

        target_offset_angle = abs(data.normalize_angle_difference(orient.orient_angle -
                                                                  direction_angle))

        distance2 = data.calculate_distance2(data.Vector([self.target_x,
                                                          self.target_y,
                                                          self.target_z]),
                                             data.Vector([navig.x,
                                                          navig.y,
                                                          navig.z]))
        target_distance = math.sqrt(distance2)

        line_coeff_a = navig.y - self.target_y
        line_coeff_b = self.target_x - navig.x
        line_coeff_c = navig.x * self.target_y - navig.y * self.target_x

        intersect = abs(line_coeff_c) <= (target_distance *
                                          float(planet_params.radius))
        if intersect:
            intersect_x = -line_coeff_a * line_coeff_c / distance2
            intersect_y = line_coeff_b * line_coeff_c / distance2

            if abs(navig.x - self.target_x) > abs(navig.y - self.target_y):
                target_visible = ((intersect_x <= min(navig.x, self.target_x)) or
                                  (intersect_x >= max(navig.x, self.target_x)))
            else:
                target_visible = ((intersect_y <= min(navig.y, self.target_y)) or
                                  (intersect_y >= max(navig.y, self.target_y)))
        else:
            target_visible = True

        load.visible_target = self.target_index if target_visible else None
        load.target_offset_angle = target_offset_angle
        load.target_distance = target_distance if target_visible else None
        load.target_incidence_angle = abs(orient.off_nadir_angle) if target_visible else None

        for gs in radio.sent_packets.keys():
            if len(radio.sent_packets[gs]) != 0:
                for message in radio.sent_packets[gs].values():
                    header = message[3][0]

                    if header == self.name:
                        payload = message[3][1]

                        debug_log(_('Image %s received from camera'),
                                  str(payload['visible_target']))

                        if (((payload['visible_target'] == self.target_index) and
                             (payload['camera_range'] == 'visible'))):
                            mission_log(_('MISSION ACCOMPLISHED! The image of the target received.')) # pylint: disable=C0301
                            probe.success = True
                            offset_angle = payload['target_offset_angle']
                            resolution = payload['target_resolution']
                            incidence_angle = payload['target_incidence_angle']
                            probe.photo_resolution = resolution
                            probe.photo_offset_angle = offset_angle
                            probe.photo_incidence_angle = incidence_angle
                            #perfect_resolution = float(probe.xml.flight.mission.resolution)
                            #success_score = data.BASE_SCORE[self.name]
                            #if resolution > perfect_resolution:
                            #    success_score *= perfect_resolution / resolution
                            #if offset_angle > self.perfect_offset_angle:
                            #    success_score *= self.perfect_offset_angle / offset_angle
                            #if incidence_angle > self.perfect_incidence_angle:
                            #    success_score *= self.perfect_incidence_angle / incidence_angle
                            #if probe.success_score == 0.0 or probe.success_score < success_score:
                            #    probe.success_score = success_score
                            probe.success_score = None
                            probe.success_timestamp = time.time()

data.available_missions[DzzMission.name] = DzzMission
