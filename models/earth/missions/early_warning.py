# -----------------------------------------------------------------------------
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# The Orbita Simulator
# The Earth orbit simulation model (v2)
#
# The simulator missions implementation: The Early Warning Missle Detection
# System
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
from decimal import Decimal
import gettext

import data
import constants
from mission import Mission
from logger import debug_log, mission_log

_ = gettext.gettext

class EarlyWarningMission(Mission):
    name = constants.MISSION_EARLY_WARNING

    acceptable_detection_delay = 180.0
    acceptable_intercept_rate = Decimal('0.7')
    boost_phase_duration = 180.0
    boost_acceleration = 10.0

    def __init__(self, global_parameters):
        Mission.__init__(self, global_parameters)
        self.targets = {}
        self.unlaunched_targets = {}
        self.undetected_targets = set([])
        self.current_target_index = None
        self.target_x = None
        self.target_y = None
        self.target_z = None
        self.missiles_intercepted = 0
        self.max_detection_delay = 0.0

    def init(self, probes, initial_tick, lang):
        global _ # pylint: disable=W0603
        _ = lang
        probe = probes.get()[0]

        orient = probe.systems[constants.SUBSYSTEM_ORIENTATION]
        orient.planet_rotation = True

        self.targets = {}
        self.unlaunched_targets = {}

        for missile in probe.xml.flight.mission.missiles.missile:
            self.targets[missile.index] = {'location_angle': float(missile.location_angle),
                                           'launch_time': float(missile.launch_time)}
            self.unlaunched_targets[int(missile.launch_time)] = missile.index

        self.undetected_targets = set(self.targets.keys())

        self.current_target_index = None

        self.target_x = None
        self.target_y = None
        self.target_z = None

        self.missiles_intercepted = 0

        self.max_detection_delay = 0.0

    def step(self, probes, tick):
        probe = probes.get()[0]
        navig = probe.systems[constants.SUBSYSTEM_NAVIGATION]
        orient = probe.systems[constants.SUBSYSTEM_ORIENTATION]
        radio = probe.systems[constants.SUBSYSTEM_RADIO]
        load = probe.systems[constants.SUBSYSTEM_LOAD]

        planet_params = self.params.Planets[probe.planet]

        flight_time = probe.systems[constants.SUBSYSTEM_CPU].flight_time
        angle_offset = 360.0 * flight_time / orient.planet_rotation_period

        if int(flight_time) in self.unlaunched_targets:
            target_index = self.unlaunched_targets[int(flight_time)]
            del self.unlaunched_targets[int(flight_time)]
            self.current_target_index = target_index
            debug_log(probe, _('Rocket launch: %s'), str(target_index))

        if self.current_target_index is not None:
            target = self.targets[self.current_target_index]
            launch_time = target['launch_time']
            if flight_time - launch_time <= self.boost_phase_duration:
                location_angle = target['location_angle']
                location_angle = data.normalize_angle(location_angle + angle_offset)

                height = self.boost_acceleration * ((flight_time - launch_time) ** 2) / 2
                debug_log(probe, _('Rocket height: %s'), str(height))

                radius = height + float(planet_params.radius)

                angle_rad = math.radians(location_angle)
                self.target_x = radius * math.sin(angle_rad)
                self.target_y = radius * math.cos(angle_rad)
                self.target_z = 0

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

                intersect = abs(line_coeff_c) <= target_distance * float(planet_params.radius)
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

                load.visible_target = self.current_target_index if target_visible else None
                load.target_offset_angle = target_offset_angle
                load.target_distance = target_distance if target_visible else None
            else:
                if self.current_target_index is not None:
                    debug_log(probe, _('The end of the active trajectory of the target'))

                self.current_target_index = None

                self.target_x = None
                self.target_y = None
                self.target_z = None

                load.visible_target = None
                load.target_offset_angle = None
                load.target_distance = None

        for gs in radio.sent_packets.keys():
            if len(radio.sent_packets[gs]) != 0:
                for message in radio.sent_packets[gs].values():
                    header = message[3][0]

                    if header == self.name:
                        payload = message[3][1]

                        debug_log(probe, _('Image received from camera: %s'),
                                  str(payload['visible_target']))

                        if (((payload['visible_target'] in self.undetected_targets) and
                             (payload['camera_range'] == 'infrared'))):
                            mission_log(probe, _('Ballistic launch detected!!'))
                            receive_time = flight_time
                            launch_time = self.targets[payload['visible_target']]['launch_time']

                            self.undetected_targets.discard(payload['visible_target'])

                            detection_delay = receive_time - launch_time
                            if detection_delay <= self.acceptable_detection_delay:
                                mission_log(probe, _('Data sent in time.'))

                                if detection_delay > self.max_detection_delay:
                                    self.max_detection_delay = detection_delay

                                self.missiles_intercepted += 1

                                if ((self.missiles_intercepted >=
                                     len(self.targets) * self.acceptable_intercept_rate)):
                                    mission_log(probe, _('MISSION ACCOMPLISHED! More than %d%%%% targets intercepted.') % # pylint: disable=C0301
                                                int(self.acceptable_intercept_rate * 100))
                                    probe.success = True
                                    probe.missiles_unintercepted = (len(self.targets) -
                                                                    self.missiles_intercepted)
                                    probe.detection_delay = self.max_detection_delay
                                    probe.success_score = None
                                    probe.success_timestamp = time.time()
                            else:
                                mission_log(probe, _('Data sent with delay.'))

data.available_missions[EarlyWarningMission.name] = EarlyWarningMission
