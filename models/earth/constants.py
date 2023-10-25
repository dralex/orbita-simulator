# -----------------------------------------------------------------------------
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# The Orbita Simulator
# The Earth orbit simulation model (v2)
#
# The simulator constants
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

SUBSYSTEM_CONSTRUCTION = 'construction'
SUBSYSTEM_CPU = 'cpu'
SUBSYSTEM_NAVIGATION = 'navigation'
SUBSYSTEM_ORIENTATION = 'orientation'
SUBSYSTEM_ENGINE = 'engine'
SUBSYSTEM_POWER = 'power'
SUBSYSTEM_TELEMETRY = 'telemetry'
SUBSYSTEM_HEAT_CONTROL = 'heat_control'
SUBSYSTEM_RADIO = 'radio'
SUBSYSTEM_LOAD = 'load'

MISSION_NONE = 'none'
MISSION_TEST_LOOK = 'test1'
MISSION_TEST_SMS = 'test2'
MISSION_TEST_ORBIT = 'test3'
MISSION_SMS = 'sms'
MISSION_TELECOM = 'telecom'
MISSION_INSPECT = 'inspect'
MISSION_DZZ = 'dzz'
MISSION_CRYSTAL = 'crystal'
MISSION_MOLNIYA = 'molniya'
MISSION_EARLY_WARNING = 'early_warning'
MISSION_SATELLITE_INTERNET = 'satellite_internet'

MESSAGE_TYPE_SMS = 'sms'
MESSAGE_TYPE_PHOTO = 'photo'
MESSAGE_TYPE_TELEMETRY = 'telemetry'

BASE_SCORE = {
    MISSION_SMS: 10.0,
    MISSION_INSPECT: 10000000.0,
    MISSION_DZZ: 10000000.0,
    MISSION_CRYSTAL: 10000000.0,
}

STATE_ON = 'ON'
STATE_OFF = 'OFF'
STATE_SLEEP = 'SLEEP'
STATE_DEAD = 'DEAD'
STATE_SAFE = 'SAFE'
STATE_WAKEUP = 'WAKEUP'
