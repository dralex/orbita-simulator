# -----------------------------------------------------------------------------
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# The Orbita Simulator
# The Earth orbit simulation model (v2)
#
# Orbita 2.0 test API
#
# Copyright (C) 2015-2023 Alexey Fedoseev <aleksey@fedoseev.net>
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
import time

STATE_NOT_INITIALIZED = int(0)
STATE_OFF = int(1)
STATE_ON = int(2)
STATE_SLEEP = int(3)
STATE_DEAD = int(4)
STATE_SAFE = int(5)
STATE_WAKEUP = int(6)

AXIS_X = int(0)
AXIS_Y = int(1)
AXIS_Z = int(2)

SYSTEM_CPU = int(10)
SYSTEM_TELEMETRY = int(20)
SYSTEM_TRANSMITTER = int(30)
SYSTEM_POWER = int(40)
SYSTEM_NAVIGATION = int(50)
SYSTEM_ORIENTATION = int(60)
SYSTEM_ENGINE = int(70)
SYSTEM_HEATCONTROL = int(80)
SYSTEM_CAMERA = int(90)
SYSTEM_CONTAINER = int(100)

MESSAGE_TELEMETRY = int(1)
MESSAGE_PHOTO = int(2)
MESSAGE_SMS = int(3)

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

class Sputnik:
    def __init__(self):
        self.cpu = CPU()
        self.telemetry = Telemetry()
        self.transmitter = Transmitter()
        self.power = Power()
        self.navigation = Navigation()
        self.orientation = Orientation()
        self.engine = Engine()
        self.heat_control = HeatControl()
        self.camera = Camera()
        self.container = Container()

# -----------------------------------------------------------------------------
# Abstract system class
# -----------------------------------------------------------------------------

class System:
    def __init__(self, kind):
        self._kind = kind
        self.events = []

    def get_state(self):
        return STATE_ON

    def set_state(self, state):
        if state not in [STATE_NOT_INITIALIZED,
                         STATE_OFF,
                         STATE_ON,
                         STATE_SLEEP,
                         STATE_DEAD,
                         STATE_SAFE,
                         STATE_WAKEUP]:
            raise BadParametersError
        if state == STATE_WAKEUP and self._kind != SYSTEM_CPU:
            raise BadParametersError
        return None

    def sleep(self, timeout):
        return None

    def has_event(self):
        if self.events:
            ev = self.events.pop(0)
            if ev[1] is None:
                return ev[0]
            else:
                return ev
        else:
            return None

    def dispatch(self, event, value=None):
        self.events.append((event, value))

# -----------------------------------------------------------------------------
# CPU system class
# -----------------------------------------------------------------------------

class CPU(System):
    def __init__(self):
        System.__init__(self, SYSTEM_CPU)

    def run(self):
        return True

    def get_flight_time(self):
        return time.time()

    def mission_completed(self):
        return False

    def terminate(self):
        from sys import exit
        exit(0)

# -----------------------------------------------------------------------------
# Telemetry system class
# -----------------------------------------------------------------------------

class Telemetry(System):
    def __init__(self):
        System.__init__(self, SYSTEM_TELEMETRY)

    def set_period(self, period):
        return None

    def send_message(self, text):
        return None

    @classmethod
    def debug(cls, text):
        print(text)

debug = Telemetry.debug

# -----------------------------------------------------------------------------
# High-performance radio system class
# -----------------------------------------------------------------------------

class Transmitter(System):
    def __init__(self):
        System.__init__(self, SYSTEM_TRANSMITTER)

    def send_data(self, msg_type, data, receiver=-1, sender=-1, timeout=None):
        if msg_type not in [MESSAGE_TELEMETRY,
                            MESSAGE_PHOTO,
                            MESSAGE_SMS]:
            raise BadParametersError
        return None

    def send_photo(self, slot_num, receiver=None):
        return None

    def receive(self, sender):
        return None

    def get_progress(self, sender):
        return 0.0

    def get_message(self, sender):
        return None

# -----------------------------------------------------------------------------
# Power system class
# -----------------------------------------------------------------------------

class Power(System):
    def __init__(self):
        System.__init__(self, SYSTEM_POWER)

    def get_battery_capacity(self):
        return 500.0

    def get_generation(self):
        return 0.0

    def get_consumption(self):
        return 0.0

# -----------------------------------------------------------------------------
# Navigation system class
# -----------------------------------------------------------------------------

class Navigation(System):
    def __init__(self):
        System.__init__(self, SYSTEM_NAVIGATION)

    def get_orbit_height(self):
        return 0.0

    def get_z_axis_angle(self):
        return 0.0

    def get_x_coord(self):
        return 0.0

    def get_y_coord(self):
        return 0.0

    def get_transversal_velocity(self):
        return 0.0

    def get_radial_velocity(self):
        return 0.0

# -----------------------------------------------------------------------------
# Orientation system class
# -----------------------------------------------------------------------------

class Orientation(System):
    def __init__(self):
        System.__init__(self, SYSTEM_ORIENTATION)

    def get_angle(self, axis):
        if axis != AXIS_Z:
            return None
        return 0.0

    def get_angular_velocity(self, axis):
        if axis != AXIS_Z:
            return None
        return 0.0

    def start_motor(self, axis):
        if axis != AXIS_Z:
            raise NotSupportedError
        return None

    def stop_motor(self, axis):
        if axis != AXIS_Z:
            raise NotSupportedError
        return None

    def set_motor_moment(self, axis, torsion):
        if axis != AXIS_Z:
            raise NotSupportedError
        return None

    def start_coil(self, axis):
        raise NotSupportedError

    def stop_coil(self, axis):
        raise NotSupportedError

# -----------------------------------------------------------------------------
# Engine system class
# -----------------------------------------------------------------------------

class Engine(System):
    def __init__(self):
        System.__init__(self, SYSTEM_ENGINE)

    def get_fuel(self):
        return 5.0

    def start_engine(self):
        return None

    def stop_engine(self):
        return None

    def set_traction(self, t):
        return None

# -----------------------------------------------------------------------------
# Heat control class
# -----------------------------------------------------------------------------

class HeatControl(System):
    def __init__(self):
        System.__init__(self, SYSTEM_HEATCONTROL)

    def get_temperature(self):
        return 290.0

    def start_heating(self):
        return None

    def stop_heating(self):
        return None

    def set_power(self, p):
        return None

# -----------------------------------------------------------------------------
# Camera class
# -----------------------------------------------------------------------------

class Camera(System):
    def __init__(self):
        System.__init__(self, SYSTEM_CAMERA)

    def take_photo(self):
        return 0

    def start_shooting(self):
        return None

    def stop_shooting(self):
        return 0

    def get_image_size(self, slot_num):
        if slot_num == 0:
            return 5 * 1024 * 1024
        else:
            return None

# -----------------------------------------------------------------------------
# Container
# -----------------------------------------------------------------------------

class Container(System):
    def __init__(self):
        System.__init__(self, SYSTEM_CONTAINER)

    def start_experiment(self):
        return None

    def stop_experiment(self):
        return None

    def set_parachute_height(self, h):
        return None

    def drop(self):
        return None

# -----------------------------------------------------------------------------
# Build global namespace for user code
# -----------------------------------------------------------------------------

sputnik = Sputnik()

cpu = sputnik.cpu
telemetry = sputnik.telemetry
transmitter = sputnik.transmitter
power = sputnik.power
navigation = sputnik.navigation
orientation = sputnik.orientation
engine = sputnik.engine
heat_control = sputnik.heat_control
camera = sputnik.camera
container = sputnik.container

debug = sputnik.telemetry.debug
