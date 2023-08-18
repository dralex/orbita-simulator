# -----------------------------------------------------------------------------
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# The Orbita Simulator
# The Earth orbit simulation model (v2)
#
# The calculation models: the simple ballistics model (constant circular orbit,
# one-axis rotation)
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
from collections import deque

import data
import constants
from abstractmodel import AbstractModel
from logger import debug_log, time_to_str, mission_log
from language import Language

_ = Language.get_tr()

class FlatBallisticModel(AbstractModel):
    def __init__(self, global_parameters):
        AbstractModel.__init__(self, global_parameters)
        self.atmosphere = 0.0

    @classmethod
    def exact_solution(cls, R, t, K):
        v = math.sqrt(K / R)
        T = R / v
        angle = t / T

        return [[R * math.sin(angle), R * math.cos(angle), 0.0],
                [v * math.cos(angle), -v * math.sin(angle), 0.0]]

    @classmethod
    def grav_accel(cls, x, K):
        r = math.sqrt(x[0] * x[0] + x[1] * x[1] + x[2] * x[2])
        a = K / (r * r)
        return [-x[0] * a / r, -x[1] * a / r, -x[2] * a / r]

    @classmethod
    def build_the_past(cls, R, dt, K):
        past = deque()
        for i in range(1, 4):
            x, v = FlatBallisticModel.exact_solution(R, -i * dt, K)
            a = FlatBallisticModel.grav_accel(x, K)
            past.append(v + a)
        return past

    @classmethod
    def rotate_past(cls, past):
        rv = past.popleft()
        past.append(rv)
        return rv

    def init_model(self, probe, initial_tick):
        global _ # pylint: disable=W0603
        _ = Language.get_tr()

        planet_params = self.params.Planets[probe.planet]
        self.atmosphere = planet_params.Atmosphere

        navig = probe.systems[constants.SUBSYSTEM_NAVIGATION]
        navig.planet_radius = float(planet_params.radius)
        navig.height = (navig.planet_radius + navig.orbit_height)
        navig.x = 0
        navig.y = navig.height
        navig.z = 0
        navig.gravity_koeff = (float(planet_params.mass) *
                               float(self.params.G))
        navig.velocity = navig.v_x = math.sqrt(navig.gravity_koeff /
                                               navig.height)
        navig.v_y = 0
        navig.v_z = 0
        navig.v_tan = navig.velocity
        navig.v_norm = 0
        navig.past = FlatBallisticModel.build_the_past(navig.height,
                                                       initial_tick,
                                                       navig.gravity_koeff)
        navig.turns = 0
        navig.last_turn_time = probe.time()

        navig.max_acceleration = navig.acceleration = (navig.gravity_koeff /
                                                       navig.height ** 2)
        navig.atm_border = self.atmosphere.border(float(planet_params.atmosphere.density_border))
        debug_log(probe, _('The atmosphere border: %f m'), navig.atm_border)
        navig.acceleration_limit = probe.max_acceleration
        omega = 2.0 * math.pi / float(planet_params.rotation_period)
        navig.gs_orbit = math.pow(float(planet_params.mass) *
                                  float(self.params.G) / omega ** 2, 1 / 3.0)
        debug_log(probe, _('The geostationary orbit: %f (%f) m'), navig.gs_orbit,
                  navig.gs_orbit - navig.planet_radius)

        navig.angle = navig.start_angle

        navig.dark_side = False

        navig.ground_visibility_angle = math.degrees(math.acos(navig.planet_radius /
                                                               navig.height)) * 2

    def step(self, probe, tick, probes): # pylint: disable=R0912,R0914
        navig = probe.systems[constants.SUBSYSTEM_NAVIGATION]
        orient = probe.systems[constants.SUBSYSTEM_ORIENTATION]
        engine = probe.systems[constants.SUBSYSTEM_ENGINE]

        for probe_a in probes.get():
            if probe_a != probe:
                navig_a = probe_a.systems[constants.SUBSYSTEM_NAVIGATION]
                if data.calculate_distance(navig, navig_a) < 1:
                    data.terminate(probe, "Spacecraft collision")

        if navig.height <= navig.planet_radius:
            if abs(navig.velocity) <= probe.Parameters.Planets[probe.planet].max_landing_velocity:
                debug_log(probe, _('Successful landing %s!'), time_to_str(probe.time()))
                mission_log(probe, _('LANDING Ti=%s, Ang=%.2f V=%.2f, Max.Acc=%.2f'),
                            time_to_str(probe.time()),
                            navig.angle,
                            navig.velocity,
                            navig.max_acceleration)
                probe.landed = True
            else:
                debug_log(_('Falling velocity: %f'), navig.velocity)
                data.terminate(probe, _('The probe has crushed on the ground'))
        elif probe.parachute_height is not None and navig.height <= probe.parachute_height:
            load = probe.systems[data.SUBSYSTEM_LOAD]
            assert load
            load.open_parachute()

        gmr3 = navig.gravity_koeff * probe.mass / (navig.height ** 3)
        F_gravity_x = - navig.x * gmr3
        F_gravity_y = - navig.y * gmr3
        F_gravity_z = 0

        F_engine_x = 0
        F_engine_y = 0
        F_engine_z = 0

        if engine is not None and engine.mode == constants.STATE_ON and engine.running:
            df = engine.traction * tick
            if engine.check_fuel(df):
                phi_rad = math.radians(orient.orient_angle)
                F_engine = engine.traction * float(engine.device.jet_speed)
                F_engine_x = F_engine * math.cos(phi_rad)
                F_engine_y = F_engine * math.sin(phi_rad)
                engine.decrement_fuel(df)
            else:
                debug_log(_('The fuel is exhausted.'))
                engine.stop_engine()

        F_stokes_x = 0
        F_stokes_y = 0
        F_stokes_z = 0

        if navig.height <= navig.atm_border:
            d = self.atmosphere.density(navig.height)
            s = (probe.aerodynamic_coeff * probe.square +
                 probe.parachute_aerodynamic_coeff * probe.parachute_square) * d / 2.0
            F_stokes_x = s * (navig.v_x ** 2)
            F_stokes_y = s * (navig.v_y ** 2)
            if navig.v_x > 0:
                F_stokes_x = -F_stokes_x
            if navig.v_y > 0:
                F_stokes_y = -F_stokes_y

        a_x = (F_gravity_x + F_engine_x + F_stokes_x) / probe.mass
        a_y = (F_gravity_y + F_engine_y + F_stokes_y) / probe.mass
        a_z = (F_gravity_z + F_engine_z + F_stokes_z) / probe.mass
        navig.acceleration = math.sqrt(a_x ** 2 + a_y ** 2 + a_z ** 2)
        if navig.acceleration > navig.max_acceleration:
            navig.max_acceleration = navig.acceleration
        if navig.acceleration > navig.acceleration_limit:
            debug_log(_('Acceleration: %f'), navig.acceleration)
            data.terminate(probe, _('The probe was crushed by overload'))

        delta = [navig.v_x, navig.v_y, navig.v_z, a_x, a_y, a_z]
        navig.past.append(delta)
        delta = [55.0 * d for d in delta]
        delta = [d - 59.0 * p for d, p in zip(delta,
                                              FlatBallisticModel.rotate_past(navig.past))]
        delta = [d + 37.0 * p for d, p in zip(delta,
                                              FlatBallisticModel.rotate_past(navig.past))]
        delta = [d - 9.0 * p for d, p in zip(delta,
                                             navig.past.popleft())]
        delta = [d * tick / 24.0 for d in delta]

        navig.x += delta[0]
        navig.y += delta[1]
        navig.z += delta[2]
        navig.v_x += delta[3]
        navig.v_y += delta[4]
        navig.v_z += delta[5]
        navig.velocity = math.sqrt(navig.v_x ** 2 + navig.v_y ** 2 + navig.v_z ** 2)

        navig.angle = math.degrees(math.atan2(navig.x, navig.y))
        while navig.angle < 0.0:
            navig.angle += 360.0
        if navig.angle <= 0.1 and probe.time() - navig.last_turn_time > 600:
            navig.turns += 1
            navig.last_turn_time = probe.time()
            data.debug_log(probe, _('Orbital revolution: %d'), navig.turns)

        alpha = math.atan2(navig.v_x, navig.v_y) - math.atan2(navig.x, navig.y)
        navig.v_transversal = navig.velocity * math.sin(alpha)
        navig.v_radial = navig.velocity * math.cos(alpha)

        navig.height = math.sqrt(navig.x ** 2 + navig.y ** 2 + navig.z ** 2)
        navig.orbit_height = (navig.height - navig.planet_radius)

        navig.dark_side = navig.x < 0 and abs(navig.y) <= navig.planet_radius

        if navig.orbit_height > 0:
            navig.ground_visibility_angle = math.degrees(math.acos(navig.planet_radius /
                                                                   navig.height)) * 2
        else:
            navig.ground_visibility_angle = 0.0

    def debug_model(self, probe):
        navig = probe.systems[constants.SUBSYSTEM_NAVIGATION]
        return "(%07.1f,%07.1f,%07.1f) A=%03.1f DS=%s" % (navig.x,
                                                          navig.y,
                                                          navig.z,
                                                          navig.angle,
                                                          'T' if navig.dark_side else 'F')
