# -----------------------------------------------------------------------------
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# The Orbita Simulator
# The Earth orbit simulation model (v2)
#
# The calculation models: the simple thermodynamics model
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

import data
from abstractmodel import AbstractModel

class SimpleThermodynamicsModel(AbstractModel):
    def __init__(self, global_parameters):
        AbstractModel.__init__(self, global_parameters)
        self.atmosphere = 0.0

    def init_model(self, probe, initial_tick):
        planet_params = self.params.Planets[probe.planet]
        self.atmosphere = planet_params.Atmosphere

        hc = probe.systems[data.SUBSYSTEM_HEAT_CONTROL]
        power = probe.systems[data.SUBSYSTEM_POWER]

        hc.sun_heat = (float(planet_params.sun_radiation) *
                       float(probe.square) *
                       ((float(probe.xz_yz_radiator_fraction) / 100) *
                        float(hc.device.absorption_factor) +
                        (float(probe.xz_yz_solar_panel_fraction) / 100) *
                        float(power.device.absorption_factor)))
        hc.radiation_koeff = (5.67 * 1e-8 * float(probe.square) *
                              ((2 * float(probe.xy_radiator_fraction) / 100 +
                                4 * float(probe.xz_yz_radiator_fraction) / 100) *
                               float(hc.device.radiation_blackness) +
                               (4 * float(probe.xz_yz_solar_panel_fraction) / 100) *
                               float(power.device.radiation_blackness)))

        hc.friction_heat = 0
        hc.heat = 0
        hc.sun_flow = 0
        hc.radiation = 0

    def step(self, probe, tick, probes):
        hc = probe.systems[data.SUBSYSTEM_HEAT_CONTROL]
        navig = probe.systems[data.SUBSYSTEM_NAVIGATION]

        Q_int = 0.0
        for s in probe.systems.values():
            if s:
                Q_int += s.heat_production

        if navig.dark_side:
            sun_flow = 0
        else:
            sun_flow = hc.sun_heat

        hc.friction_heat = 0
        if navig.height < navig.atm_border:
            # calculating the heat from the air friction
            T_ext = self.atmosphere.temperature(navig.height)
            a = self.atmosphere.temperature(navig.height)
            T0 = T_ext * (1 + ((1.401 - 1) / 2.0) * (navig.velocity / a) ** 2)
            if T0 > 6000:
                T0 = 6000
            if T0 > hc.temperature:
                hc.friction_heat = (probe.heat_absorption * (T0 - hc.temperature) * probe.square)

        hc.heat = Q_int
        hc.sun_flow = sun_flow
        hc.radiation = hc.radiation_koeff * (hc.temperature ** 4)

        Q_ext = hc.friction_heat + hc.sun_flow - hc.radiation

        hc.temperature += (Q_int + Q_ext) * tick / (probe.heat_capacity * probe.mass)

        for s in probe.systems.values():
            if s:
                s.check_temperature(hc.temperature)

    def debug_model(self, probe):
        hc = probe.systems[data.SUBSYSTEM_HEAT_CONTROL]
        return "T=%03.1f" % hc.temperature
