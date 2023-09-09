# -----------------------------------------------------------------------------
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# The Orbita Simulator
# The Earth orbit simulation model (v2)
#
# The calculation models: the simple mechanical model
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

import math
import re

import numpy
import constants
import data
from abstractmodel import AbstractModel
from language import Language

_ = Language.get_tr()

def angle_is_between(angle, first, second):
    if second < first:
        second += 360.0
    if angle < first:
        angle += 360.0
    return second >= angle

def natural_sort_key(s, _nsre=re.compile('([0-9]+)')):
    return [int(text) if text.isdigit() else text.lower()
            for text in re.split(_nsre, s)]

class SimpleMechanicalModel(AbstractModel):
    def __init__(self, global_parameters):
        AbstractModel.__init__(self, global_parameters)

    def init_model(self, probe, initial_tick, probes):
        global _ # pylint: disable=W0603
        _ = Language.get_tr()
        planet_params = self.params.Planets[probe.planet]
        orient = probe.systems[constants.SUBSYSTEM_ORIENTATION]

        orient.planet_rotation_period = float(planet_params.rotation_period)
        orient.planet_rotation = False

        orient.orient_angle = 0.0
#        orient.orient_angle = 270.0
        orient.angular_velocity = orient.start_angular_velocity

        orient.off_nadir_angle = None

        orient.moment = 0
        orient.ground_stations = []
        orient.ground_stations_coords = {}
        orient.ground_stations_visible = {}
        orient.ground_stations_arc = {}
        orient.ground_stations_initial_angles = {}
        orient.ground_stations_angles = {}
        for cs in probe.xml.flight.mission.control_stations.control_station:
            name = str(cs.name)
            location_angle = float(cs.location_angle)
            orient.ground_stations.append(name)
            orient.ground_stations_visible[name] = False
            orient.ground_stations_arc[name] = {}
            orient.ground_stations_arc[name][constants.SUBSYSTEM_RADIO] = False
            orient.ground_stations_arc[name][constants.SUBSYSTEM_TELEMETRY] = False
            orient.ground_stations_initial_angles[name] = location_angle
            orient.ground_stations_angles[name] = location_angle
            orient.ground_stations_coords[name] = self.angle_to_coord(probe,
                                                                      location_angle)
        orient.ground_stations.sort(key=natural_sort_key)

        orient.other_probes = []
        orient.other_probes_visible = {}
        orient.other_probes_arc = {}

        for other_probe in probes.get():
            if other_probe == probe:
                continue
            orient.other_probes.append(other_probe)
            orient.other_probes_visible[other_probe.name] = False
            orient.other_probes_arc[other_probe.name] = False

    @classmethod
    def angle_to_coord(cls, probe, angle):
        angle_rad = math.radians(angle)

        navig = probe.systems[constants.SUBSYSTEM_NAVIGATION]

        x = navig.planet_radius * math.sin(angle_rad)
        y = navig.planet_radius * math.cos(angle_rad)
        z = 0

        return (x, y, z)

    def step(self, probe, tick, probes):
        orient = probe.systems[constants.SUBSYSTEM_ORIENTATION]
        navig = probe.systems[constants.SUBSYSTEM_NAVIGATION]
        radio = probe.systems[constants.SUBSYSTEM_RADIO]
        telemetry = probe.systems[constants.SUBSYSTEM_TELEMETRY]

        if orient.motor_running:
            orient.angular_velocity += (orient.moment / probe.inertia_moment) * tick

        if orient.angular_velocity != 0:
            orient.orient_angle += orient.angular_velocity * tick
            orient.orient_angle = data.normalize_angle(orient.orient_angle)

        orient.off_nadir_angle = data.normalize_angle_difference(navig.angle +
                                                                 orient.orient_angle - 270.0)

        position = (navig.x, navig.y, navig.z)

        first_visible_angle = data.normalize_angle(navig.angle -
                                                   navig.ground_visibility_angle / 2)

        last_visible_angle = data.normalize_angle(navig.angle +
                                                  navig.ground_visibility_angle / 2)

        if orient.planet_rotation:
            flight_time = probe.systems[constants.SUBSYSTEM_CPU].flight_time
            angle_offset = 360.0 * flight_time / orient.planet_rotation_period

        for other_probe in orient.other_probes:
            other_navig = other_probe.systems[constants.SUBSYSTEM_NAVIGATION]
            other_orient = other_probe.systems[constants.SUBSYSTEM_ORIENTATION]
            other_radio = other_probe.systems[constants.SUBSYSTEM_RADIO]

            first_visible_coords = self.angle_to_coord(probe, first_visible_angle)
            last_visible_coords = self.angle_to_coord(probe, last_visible_angle)

            matric_first = numpy.array([[first_visible_coords[0], 1.], [navig.x, 1.]])
            vector_first = numpy.array([first_visible_coords[1], navig.y])
            k_first, b_first = numpy.linalg.solve(matric_first, vector_first)

            matric_last = numpy.array([[last_visible_coords[0], 1.], [navig.x, 1.]])
            vector_last = numpy.array([last_visible_coords[1], navig.y])
            k_last, b_last = numpy.linalg.solve(matric_last, vector_last)

            if first_visible_coords[1] > 0:
                is_outside_first = other_navig.y > k_first * other_navig.x + b_first
            elif first_visible_coords[1] < 0:
                is_outside_first = other_navig.y < k_first * other_navig.x + b_first
            else:
                is_outside_first = (other_navig.x > first_visible_coords[0] if first_visible_coords[0] > 0 else
                                    other_navig.x < first_visible_coords[0])

            if last_visible_coords[1] > 0:
                is_outside_last = other_navig.y > k_last * other_navig.x + b_last
            elif last_visible_coords[1] < 0:
                is_outside_last = other_navig.y < k_last * other_navig.x + b_last
            else:
                is_outside_last = (other_navig.x > last_visible_coords[0] if last_visible_coords[0] > 0 else
                                    other_navig.x < last_visible_coords[0])

            orient.other_probes_visible[other_probe.name] = (angle_is_between(other_navig.angle,
                                                                             first_visible_angle,
                                                                             last_visible_angle) or
                                                             is_outside_first or is_outside_last)

            other_probe_position = (other_navig.x, other_navig.y, other_navig.z)

            direction = (other_probe_position[0] - position[0], other_probe_position[1] - position[1],
                         other_probe_position[2] - position[2])
            direction_angle = math.degrees(math.atan2(direction[1], direction[0]))
            off_direction_angle = abs(data.normalize_angle_difference(orient.orient_angle -
                                                                      direction_angle))

            other_direction = (position[0] - other_probe_position[0], position[1] - other_probe_position[1],
                               position[2] - other_probe_position[2])
            other_direction_angle = math.degrees(math.atan2(other_direction[1], other_direction[0]))
            other_off_direction_angle = abs(data.normalize_angle_difference(other_orient.orient_angle -
                                                                            other_direction_angle))

            if radio and other_radio:
                orient.other_probes_arc[other_probe.name] = (orient.other_probes_visible[other_probe.name] and
                                                             off_direction_angle <= radio.radio_angle / 2 and
                                                             other_off_direction_angle <= other_radio.radio_angle / 2)

        for gsname, gs in orient.ground_stations_coords.items():
            location_angle = orient.ground_stations_initial_angles[gsname]

            if orient.planet_rotation:
                location_angle = data.normalize_angle(location_angle + angle_offset)
                orient.ground_stations_angles[gsname] = location_angle
                orient.ground_stations_coords[gsname] = self.angle_to_coord(probe,
                                                                            location_angle)

            orient.ground_stations_visible[gsname] = angle_is_between(location_angle,
                                                                      first_visible_angle,
                                                                      last_visible_angle)

            direction = (gs[0] - position[0], gs[1] - position[1], gs[2] - position[2])
            direction_angle = math.degrees(math.atan2(direction[1], direction[0]))
            off_direction_angle = abs(data.normalize_angle_difference(orient.orient_angle -
                                                                      direction_angle))

            if radio:
                orient.ground_stations_arc[gsname][constants.SUBSYSTEM_RADIO] = (orient.ground_stations_visible[gsname] and # pylint: disable=C0301
                                                                                 off_direction_angle <= radio.radio_angle / 2)  # pylint: disable=C0301
            if telemetry:
                orient.ground_stations_arc[gsname][constants.SUBSYSTEM_TELEMETRY] = (orient.ground_stations_visible[gsname] and  # pylint: disable=C0301
                                                                                     off_direction_angle <= telemetry.radio_angle / 2)  # pylint: disable=C0301


    def debug_model(self, probe):
        orient = probe.systems[constants.SUBSYSTEM_ORIENTATION]
        stations = orient.ground_station_visible.items()
        visible_stations = [gs for (gs, visible) in stations if visible]
        return "Phi=%03.1f w=%03.1f M=%03.1f GSV=%s" % (orient.orient_angle,
                                                        orient.angular_velocity,
                                                        orient.moment,
                                                        len(visible_stations))
