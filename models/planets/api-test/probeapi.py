# -----------------------------------------------------------------------------
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# The Orbita Simulator
# The planet landing model
#
# Probe API test implementation
#
# Copyright (C) 2016-2023 Alexey Fedoseev <aleksey@fedoseev.net>
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

STATE_OFF		= 0
STATE_ON 		= 1
STATE_DEAD		= 2

class GenericError(Exception):
    pass

class SystemNotAvailableError(GenericError):
    pass

class NotSupportedError(GenericError):
    pass

class BadParametersError(GenericError):
    pass

# -----------------------------------------------------------------------------
# High-level API class
# -----------------------------------------------------------------------------

class Probe(object):
    def __init__(self):
        pass

    def run(self):
        return True

    def get_device_state(self, device_id):
        return STATE_OFF

    def set_device_state(self, device_id, state):
        return None

    def get_device_period(self, device_id):
        return 1

    def set_device_period(self, device_id, period):
        return None

    def cpu_get_flight_time(self):
        return 0.0

    def telemetry_send_message(self, text):
        print('telemetry: ', text)
        return None

    def transmitter_get_bandwidth(self):
        return 1.0

    def transmitter_get_traffic(self):
        return 0.5

    def power_get_battery_capacity(self):
        return 1000

    def power_get_generation(self):
        return 20

    def power_get_consumption(self):
        return 10

    def navigation_get_accel(self):
        return 4.3

    def navigation_has_landed(self):
        return False

    def engine_get_fuel(self):
        return 0.2

    def engine_set_angle(self, device_id, angle):
        return None

    def heat_control_get_ext_temperature(self):
        return 100

# -----------------------------------------------------------------------------
# Build global namespace for user code
# -----------------------------------------------------------------------------

probe = Probe()
