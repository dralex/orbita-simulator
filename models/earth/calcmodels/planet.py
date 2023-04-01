# -----------------------------------------------------------------------------
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# The Orbita Simulator
# The Earth orbit simulation model (v2)
#
# The calculation models: the planetar models
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

from math import log, exp
from numpy import interp # pylint: disable=E0611

class BasicAtmosphere:
    def __init__(self, parameters, planet):
        self.params = parameters.Planets[planet]

    def sound_speed(self, h): # pylint: disable=W0613,R0201
        return 331

    def temperature(self, h):
        h2 = h - self.params.radius
        if h2 <= 0:
            return float(self.params.atmosphere.T_ground) + 273
        t = (float(self.params.atmosphere.T_ground) -
             float(self.params.atmosphere.T_grad) * (h2 / 1000.0))
        if t < -270:
            t = -270
        return t + 273

    def density(self, h):
        #    return 67.0 * (venus_radius + atmosphere_height - h) / atmosphere_height
        #    return 67.0 / 2
        if h < self.params.radius:
            return float(self.params.atmosphere.density_ground)
        return (float(self.params.atmosphere.density_ground) *
                exp((float(self.params.radius) - h) /
                    float(self.params.atmosphere.density_coeff)))

    def border(self, density):
        if density == 0:
            density = 0.00000000000001
        if self.params.atmosphere.density_ground == 0:
            return 0
        return (float(self.params.radius) -
                (float(self.params.atmosphere.density_coeff) *
                 log(density / float(self.params.atmosphere.density_ground))))

class TableAtmosphere:
    def __init__(self, parameters, planet):
        p = parameters.Planets[planet]
        self.radius = float(p.radius)
        self.height_table = [float(x) for x in p.atmosphere_table.height.split(' ')]
        self.temp_table = [float(x) for x in p.atmosphere_table.temperature.split(' ')]
        self.density_table = [float(x) for x in p.atmosphere_table.density.split(' ')]
        self.sound_speed_table = [float(x) for x in p.atmosphere_table.sound_speed.split(' ')]

    def sound_speed(self, h):
        return interp(h - self.radius, self.height_table, self.sound_speed_table)

    def temperature(self, h):
        return interp(h - self.radius, self.height_table, self.temp_table)

    def density(self, h):
        return interp(h - self.radius, self.height_table, self.density_table)

    def border(self, density): # pylint: disable=W0613
        return self.height_table[-1] + self.radius
