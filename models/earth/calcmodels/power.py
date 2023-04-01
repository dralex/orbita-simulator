# -----------------------------------------------------------------------------
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# The Orbita Simulator
# The Earth orbit simulation model (v2)
#
# The calculation models: the simple power model
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
import constants
from abstractmodel import AbstractModel
from logger import debug_log
from language import Language

_ = Language.get_tr()

class SimplePowerModel(AbstractModel):
    def __init__(self, global_parameters):
        AbstractModel.__init__(self, global_parameters)

    def init_model(self, probe, initial_tick):
        global _ # pylint: disable=W0603
        _ = Language.get_tr()
        power = probe.systems[data.SUBSYSTEM_POWER]
        power.sun_generation = ((float(power.device.solar_efficiency) / 100) *
                                (float(probe.xz_yz_solar_panel_fraction) / 100) *
                                float(probe.square) *
                                float(self.params.Planets[probe.planet].sun_radiation))
        if hasattr(power.device, 'capacity') and power.device.capacity is not None:
            power.max_capacity = float(power.device.capacity) * 3600.0
        else:
            power.max_capacity = 0
        power.accumulator = power.max_capacity

    def step(self, probe, tick): # pylint: disable=R0912
        power = probe.systems[data.SUBSYSTEM_POWER]

        if power.mode == constants.STATE_OFF or power.mode == constants.STATE_DEAD:
            if not probe.safe_mode:
                debug_log(_('Power subsystem is not working'))
                probe.safe_mode_on()
            elif probe.mission != constants.MISSION_CRYSTAL:
                data.terminate(probe, _('Entering SAFE MODE twice'))

        power.power_consumption = 0.0
        for s in probe.systems.values():
            if s:
                power.power_consumption += s.power

        if probe.systems[data.SUBSYSTEM_NAVIGATION].dark_side:
            power.power_generation = 0.0
        else:
            power.power_generation = power.sun_generation

        if power.mode == constants.STATE_SLEEP:
            power.power_generation = 0.0

        dw = power.power_generation - power.power_consumption
        if dw < 0 or power.accumulator < power.max_capacity:
            charge_current = dw / power.voltage
            if charge_current < -float(power.device.max_recharge):
                debug_log(_('Power consumption %.4f A exceeds maximum recharge current of the accumulator %.4f A'), # pylint: disable=C0301
                          abs(charge_current), float(power.device.max_recharge))
                probe.safe_mode_on()
            elif charge_current > power.device.max_charge:
                charge_current = float(power.device.max_charge)
            power.accumulator += dw * tick

            if power.accumulator < 0:
                debug_log(_('The battery is low'))
                probe.safe_mode_on()
            elif power.accumulator > power.max_capacity:
                power.accumulator = power.max_capacity
                debug_log(_('The battery is charged'))
