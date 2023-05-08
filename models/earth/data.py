# pylint: disable=C0302
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# The Orbita Simulator
# The Earth orbit simulation model (v2)
#
# The simulator data storage
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

import os
import time
import math

from constants import * # pylint: disable=W0401,W0614
import calcmodels.planet

from logger import debug_log, error_log, mission_log, time_to_str
from errors import CriticalError, Terminated
from xmlconverters import ProbeLoader, ShortLogLoader
from language import Language
import sm.python_hsm

_ = Language.get_tr()

available_missions = {}
from missions import * # pylint: disable=W0401,C0413

def critical_error(probe, m, *e):
    if probe:
        msg = _('Critical error while running probe %s: %s') % (probe.name, m % e)
    else:
        msg = _('Critical error: {}').format(m % e)
    error_log(msg)
    raise CriticalError(msg, probe)

def terminate(probe, message):
    debug_log(_('Probe terminated'))
    debug_log('t=%s', time_to_str(probe.time()))
    debug_log(message)
    raise Terminated(message)

class Vector:
    def __init__(self, v):
        self.x = float(v[0])
        self.y = float(v[1])
        self.z = float(v[2])

def normalize_angle(angle):
    while angle >= 360.0:
        angle -= 360.0
    while angle < 0.0:
        angle += 360.0
    return angle

def normalize_angle_difference(difference):
    while difference > 180.0:
        difference -= 360.0
    while difference < -180.0:
        difference += 360.0
    return difference

def load_parameters_atmosphere(parameters):
    for planet_params in parameters.Planets.values():
        if not planet_params.Atmosphere:
            if hasattr(planet_params,
                       'atmosphere_table') and planet_params.atmosphere_table is not None:
                planet_params.Atmosphere = calcmodels.planet.TableAtmosphere(parameters,
                                                                             planet_params.name)
            else:
                planet_params.Atmosphere = calcmodels.planet.BasicAtmosphere(parameters,
                                                                             planet_params.name)
class Device:

    DEVICE_CLASS = {}
    MODES = [STATE_DEAD, STATE_OFF]

    def __init__(self, xml, probe, start_mode, program=None, placement=None):
        self.device = xml
        self.probe = probe
        self.program = program
        self.placement = placement
        self.mass = float(self.device.mass)
        self.mode = STATE_OFF
        self.__start_mode = start_mode
        self.min_temperature = float(xml.min_temperature) + 273.0
        self.max_temperature = float(xml.max_temperature) + 273.0
        self.power = 0
        self.heat_production = 0

    def set_initial_mode(self):
        self.set_mode(self.__start_mode)

    def set_mode(self, new_mode):
        if new_mode not in self.MODES:
            critical_error(self.probe, _('Trying to set bad mode %s') % new_mode)
        if new_mode == self.mode:
            return
        if self.mode == STATE_DEAD:
            # cannot change state of dead device
            debug_log(_('Trying to change the state %s for the dead device %s'),
                      new_mode, self.device.name)
            return
        debug_log(_('The device %s now has the state %s'), self.device.name, new_mode)
        self.mode = new_mode
        if self.mode == STATE_OFF or self.mode == STATE_DEAD:
            self.turn_off()

    def turn_off(self):
        self.power = 0
        self.heat_production = 0

    def check_temperature(self, T):
        if self.mode != STATE_DEAD and not self.min_temperature <= T <= self.max_temperature:
            debug_log(_('The device %s has %s'),
                      self.device.name,
                      _('overheated') if T > self.max_temperature else _('overcooled'))
            self.set_mode(STATE_DEAD)

    @classmethod
    def init_device(cls, devices_map, name, probe, start_mode, program, placement=None):
        if name not in devices_map:
            critical_error(probe, _("Cannot create device: %s") % name)
        xml = devices_map[name]
        return cls.DEVICE_CLASS[str(xml.type)](xml, probe, start_mode, program, placement)
    @classmethod
    def get_devices(cls, devices_map, typ):
        devices = []
        for name, dev in devices_map.items():
            if dev.type == typ:
                devices.append(name)
        return devices

    @classmethod
    def default_program(cls):
        return None

    def run_program(self):
        pass

    def available_systems(self): # pylint: disable=R0201
        return {}

class ConstructionDevice(Device):
    def __init__(self, xml, probe, start_mode, program=None, placement=None):
        if start_mode != STATE_OFF:
            critical_error(probe,
                           _('The state %s cannot be set for the probe construction') %
                           start_mode)
        if program is not None:
            critical_error(probe,
                           _('The program cannot be set for the probe construction'))
        Device.__init__(self, xml, probe, start_mode, program, placement)

class LogicDevice(Device):

    MODES = [STATE_ON, STATE_SLEEP] + Device.MODES
    VARIABLES = ['mode']
    CALLABLES = ['set_mode']
    DEFAULT_SLEEP = 3600

    def __init__(self, xml, probe, start_mode, program, placement=None):
        self.timer = None
        Device.__init__(self, xml, probe, start_mode, program, placement)
        self.program_instance = None
        if hasattr(xml, 'memory') and xml.memory is not None:
            self.memory_size = float(xml.memory)  # MB
        else:
            self.memory_size = 0
        self.program_error = False

    def available_systems(self):
        # all the systems has access to the variables - both self and CPU
        system_name = str(self.device.type)
        return {system_name: self.probe.systems[system_name],
                SUBSYSTEM_CPU: self.probe.systems[SUBSYSTEM_CPU]}

    def set_mode(self, new_mode):
        if new_mode == self.mode:
            return
        if self.probe.safe_mode and (self.device.type != SUBSYSTEM_CPU
                                     and new_mode not in (STATE_OFF, STATE_DEAD)):
            debug_log(_('Trying to change the state of the subsystem %s in SAFE MODE'),
                      self.device.name)
            return
        if self.mode == STATE_SLEEP:
            if new_mode != STATE_WAKEUP:
                return
            new_mode = STATE_ON
        Device.set_mode(self, new_mode)
        if self.mode == STATE_ON:
            self.turn_on()
        elif self.mode == STATE_SLEEP:
            self.sleep_mode()
            if self.timer is None:
                self.timer = (time.time(), self.DEFAULT_SLEEP)

    def turn_on(self):
        assert hasattr(self.device, 'power') and self.device.power is not None
        self.power = float(self.device.power)
        self.heat_production = float(self.device.heat_production)

    def sleep_mode(self):
        assert hasattr(self.device, 'power') and self.device.power is not None
        self.power = 0.1
        self.heat_production = 0

    def sleep(self, t):
        self.set_mode(STATE_SLEEP)
        self.timer = (self.probe.time(), t)

    def reset(self):
        if self.program_instance:
            self.program_instance.reset() # pylint: disable=E1103

    def get_variable(self, name):
        if name in self.VARIABLES:
            assert hasattr(self, name)
            return getattr(self, name)
        return None

    def get_callable(self, name):
        if name in self.CALLABLES:
            assert hasattr(self, name)
            return getattr(self, name)
        return None

    def run_program(self):
        if self.timer is not None:
            if self.timer[0] + self.timer[1] <= self.probe.time():
                self.timer = None
                self.set_mode(STATE_WAKEUP)
            else:
                # do not run program in the sleep mode
                return
        if self.mode == STATE_ON:
            if self.program_instance:
                self.program_instance.run()  # pylint: disable=E1103

class CPUDevice(LogicDevice):

    MODES = [STATE_SAFE] + LogicDevice.MODES
    VARIABLES = LogicDevice.VARIABLES + ['flight_time', 'time_left', 'cycle']
    CALLABLES = LogicDevice.CALLABLES + ['set_cycle']
    def __init__(self, xml, probe, start_mode, program, placement=None):
        LogicDevice.__init__(self, xml, probe, start_mode, program, placement)
        self.flight_time = 0
        self.time_left = 0
        self.cycle = 0

    def set_cycle(self, cyc):
        c = int(cyc)
        if self.cycle != c:
            debug_log(_('Cycle number %d'), c)
            tel = self.probe.systems[SUBSYSTEM_TELEMETRY]
            tel.send_log_message(_('Cycle number %d') % c)
            self.cycle = c

    def available_systems(self):
        # CPU has access to all variables and methods
        return self.probe.systems

    def set_mode(self, new_mode):
        oldmode = self.mode
        if new_mode == STATE_SAFE and self.mode == STATE_DEAD:
            if self.probe.mission != MISSION_CRYSTAL:
                terminate(self.probe, _('Cannot start SAFE MODE, CPU is dead'))
        LogicDevice.set_mode(self, new_mode)
        #if self.mode == STATE_DEAD:
        #    if self.probe.mission != MISSION_CRYSTAL:
        #        terminate(self.probe, _("CPU is dead"))
        if self.mode == STATE_OFF:
            if self.probe.mission != MISSION_CRYSTAL:
                terminate(self.probe, _("CPU was turned off: %s. Computer stopped") % new_mode)
        if oldmode == STATE_SAFE and self.mode != STATE_SAFE:
            self.probe.safe_mode_off()

    def update_time(self, tick):
        self.flight_time += tick
        self.time_left -= tick

class RadioDevice(LogicDevice):

    VARIABLES = LogicDevice.VARIABLES + ['message_received', 'message', 'message_sent']
    CALLABLES = LogicDevice.CALLABLES + ['receive_message', 'send_message']

    def __init__(self, xml, probe, start_mode, program, placement=None):
        LogicDevice.__init__(self, xml, probe, start_mode, program, placement)
        self.memory_total = int(self.memory_size * 1024 * 1024)
        self.overflow = False
        self.send_queues = {}
        self.receive_queues = {}
        self.broadcast_queue = None
        self.queues_size = 0
        self.message_id = 1
        self.received_messages = {}
        self.receiving_requests = {}
        self.receiving_progress = {}
        self.message_sent = False
        self.start_angle = None
        self.start_time = None
        self.transmitting = False
        self.radio_type = 'radio'
        if self.device.radio_angle is not None:
            self.radio_angle = float(self.device.radio_angle)
        else:
            self.radio_angle = 90.0
        while self.radio_angle < 0:
            self.radio_angle += 360.0

    def turn_on(self):
        LogicDevice.turn_on(self)
        self.transmitting = True

    def turn_off(self):
        self.transmitting = False
        LogicDevice.turn_off(self)

    def sleep_mode(self):
        self.transmitting = False
        LogicDevice.sleep_mode(self)

    def receive(self, sender):
        source = self.gs_index_to_name(sender)
        if source is None:
            return

        self.receiving_requests[source] = True
        self.receiving_progress[source] = 0.0
        if source in self.received_messages:
            del self.received_messages[source]

    def get_progress(self, sender):
        source = self.gs_index_to_name(sender)
        if source is None:
            return 0.0

        if source in self.receiving_progress:
            return self.receiving_progress[source]

        return 0.0

    def get_message(self, sender):
        source = self.gs_index_to_name(sender)
        if source is None:
            return None

        if source in self.received_messages:
            return self.received_messages[source]

        return None

    def send_photo(self, slot_num, receiver=None):
        if receiver is None:
            target = None
        else:
            target = self.gs_index_to_name(receiver)

        load = self.probe.systems[SUBSYSTEM_LOAD]
        if load is None:
            return

        size = load.get_image_size(slot_num)
        data = load.get_image_data(slot_num)
        if (size is None) or (data is None):
            return

        if target is not None:
            self.put_data(target, size, (self.probe.mission, data))
        else:
            self.put_data_broadcast(size, (self.probe.mission, data))

        load.remove_image(slot_num)

    def send_message(self, mtype, message, receiver, sender, timeout=None): # pylint: disable=W0613
        if mtype != MESSAGE_TYPE_SMS:
            debug_log(_('This type of message is not supported'))
            return

        if receiver is None:
            target = None
        else:
            target = self.gs_index_to_name(receiver)

        if sender is None:
            source = None
        else:
            source = self.gs_index_to_name(sender)

        if self.probe.mission in [MISSION_SMS, MISSION_TEST_SMS]:
            debug_log(_('Sending SMS from %s to %s'), source, target)
        else:
            debug_log(_('This mission do not allow sending messages'))
            return

        size = len(message)
        data = (self.probe.mission, source, message)

        if target is not None:
            self.put_data(target, size, data)
        else:
            self.put_data_broadcast(size, data)

    def gs_index_to_name(self, index):
        if index < 0:
            return None

        orient = self.probe.systems[SUBSYSTEM_ORIENTATION]
        names = orient.ground_stations

        if index >= len(names):
            return None

        return names[index]

    def put_data_broadcast(self, volume, realdata=None):
        self.put_data(None, volume, realdata)

    def put_data(self, gs, volume, realdata=None):
        telemetry = self.probe.systems[SUBSYSTEM_TELEMETRY]
        if self.queues_size + volume > self.memory_total:
            debug_log(_('Dropping message (len %d B) which does not fit the memory %f MB'),
                      volume, self.memory_size)
            if self != telemetry and not self.overflow:
                telemetry.send_log_message(_('Memory of the transmitter %s (%f MB) is overful. The messagy (type %s len %f MB) dropped') % # pylint: disable=C0301
                                           (self.device.full_name,
                                            self.memory_size,
                                            ('N/A' if realdata is None else realdata[0]),
                                            volume / 1048576.0))
            self.overflow = True
        else:
            self.overflow = False
            if gs is None:
                self.broadcast_queue_append([self.message_id,
                                             self.probe.time(),
                                             volume,
                                             0,
                                             realdata])
                self.message_id += 1
            elif gs in self.send_queues:
                self.send_queues_append(gs,
                                        [self.message_id,
                                         self.probe.time(),
                                         volume,
                                         0,
                                         realdata])
                self.message_id += 1
            else:
                telemetry.send_log_message(_('Trying to send the message to an unavailable ground station %s') % # pylint: disable=C0301
                                           str(gs))

    def receive_data(self, gs, size, data):
        telemetry = self.probe.systems[SUBSYSTEM_TELEMETRY]
        if gs in self.receive_queues:
            self.receive_queues_append(gs,
                                       [self.message_id,
                                        None,
                                        size,
                                        0,
                                        data])
            self.message_id += 1
        else:
            telemetry.send_log_message(_('Trying to receive the message form an unavailable ground station %s') % # pylint: disable=C0301
                                       str(gs))

    def send_queues_append(self, gs, data):
        self.send_queues[gs].append(data)
        self.queues_size += data[2]

    def receive_queues_append(self, gs, data):
        self.receive_queues[gs].append(data)
        self.queues_size += data[2]

    def broadcast_queue_append(self, data):
        self.broadcast_queue.append(data)
        self.queues_size += data[2]

    def send_queues_pop(self, gs):
        data = self.send_queues[gs].popleft()
        self.queues_size -= data[2]

    def receive_queues_pop(self, gs):
        data = self.receive_queues[gs].popleft()
        self.queues_size -= data[2]

    def broadcast_queue_pop(self):
        data = self.broadcast_queue.popleft()
        self.queues_size -= data[2]

    def receive_queues_flush(self):
        for gs in self.receive_queues:
            while len(self.receive_queues[gs]) > 0:
                data = self.receive_queues[gs].pop()
                self.queues_size -= data[2]

    def queues_len(self):
        return self.queues_size / 1048576.0 # MB

class PowerDevice(LogicDevice):

    VARIABLES = LogicDevice.VARIABLES + ['power_generation',
                                         'power_consumption',
                                         'accumulator']

    def __init__(self, xml, probe, start_mode, program, placement=None):
        LogicDevice.__init__(self, xml, probe, start_mode, program, placement)
        self.accumulator = 0
        self.power_generation = 0
        self.power_consumption = 0
        self.voltage = 0

    def init_power(self, voltage):
        self.power_generation = 0
        self.power_consumption = 0
        self.voltage = voltage

class NavigationDevice(LogicDevice):

    VARIABLES = LogicDevice.VARIABLES + ['orbit_height',
                                         'angle',
                                         'dark_side',
                                         'velocity']

    def __init__(self, xml, probe, start_mode, program, placement=None):
        LogicDevice.__init__(self, xml, probe, start_mode, program, placement)

        self.orbit_height = None
        self.angle = None
        self.start_angle = None

        self.height = None
        self.x = None
        self.y = None
        self.z = None
        self.velocity = None
        self.v_transversal = None
        self.v_radial = None
        self.acceleration = None
        self.dark_side = None

    def available_systems(self):
        # the navigation system is able to control engines which have no program
        avsys = LogicDevice.available_systems(self)
        avsys[SUBSYSTEM_ENGINE] = self.probe.systems[SUBSYSTEM_ENGINE]
        return avsys

    def initialize_flight(self, start_height, start_angle):
        self.orbit_height = start_height * 1000.0
        self.angle = self.start_angle = start_angle

class OrientationDevice(LogicDevice):

    VARIABLES = LogicDevice.VARIABLES + ['orient_angle', 'angular_velocity']
    CALLABLES = LogicDevice.CALLABLES + ['start_torsion', 'stop_torsion']

    def __init__(self, xml, probe, start_mode, program, placement=None):
        LogicDevice.__init__(self, xml, probe, start_mode, program, placement)
        if self.device.orientation_type == 'wheel':
            self.max_torsion = float(self.device.max_torsion)
        elif self.device.orientation_type == 'none':
            self.max_torsion = 0.0
        else:
            critical_error(probe, _('This version of the simulator supports only orientation systems with wheel or w/o conrtol at all')) # pylint: disable=C0301
        self.moment = 0.0
        self.motor_running = False
        self.orient_angle = 0.0
        self.angular_velocity = self.start_angular_velocity = 0.0

    def initialize_flight(self, start_angular_velocity):
        self.orient_angle = 0.0
        self.angular_velocity = self.start_angular_velocity = start_angular_velocity

    def turn_on(self):
        LogicDevice.turn_on(self)
        self.motor_running = False
        self.set_torsion(0.0)

    def turn_off(self):
        self.stop_motor()
        LogicDevice.turn_off(self)

    def sleep_mode(self):
        self.stop_motor()
        LogicDevice.sleep_mode(self)

    def start_motor(self):
        if self.mode == STATE_ON:
            debug_log(_('Flywheel started'))
            self.motor_running = True
        else:
            debug_log(_('Trying to run flywheel while the navigation system is off'))

    def stop_motor(self):
        if not self.motor_running:
            return
        debug_log(_('Flywheel stopped'))
        self.motor_running = False

    def set_torsion(self, m):
        if self.mode == STATE_ON:
            moment = float(m)
            max_moment = self.max_torsion

            if abs(moment) > max_moment:
                if moment < 0.0:
                    self.moment = -max_moment
                else:
                    self.moment = max_moment
                debug_log(_('Bad moment value %f'), moment)
            else:
                self.moment = moment

            debug_log(_('Moment set %f'), self.moment)
        else:
            debug_log(_('Trying to set moment while the navigation system is off'))

    def start_coil(self):
        pass

    def stop_coil(self):
        pass

class EngineDevice(LogicDevice):

    VARIABLES = LogicDevice.VARIABLES + ['fuel']
    CALLABLES = LogicDevice.CALLABLES + ['set_traction']

    def __init__(self, xml, probe, start_mode, program=None, placement=None):
        if program is not None:
            critical_error(probe, _('Cannot set program to an engine device'))
        LogicDevice.__init__(self, xml, probe, start_mode, program, placement)
        self.fuel = 0.0
        self.running = False
        self.traction = 0.0

    def initialize_fuel(self, fuel):
        self.fuel = fuel
        self.mass += self.fuel

    def turn_on(self):
        LogicDevice.turn_on(self)
        self.running = False
        self.set_traction(float(self.device.max_traction))

    def turn_off(self):
        self.stop_engine()
        LogicDevice.turn_off(self)

    def sleep_mode(self):
        self.stop_engine()
        LogicDevice.sleep_mode(self)

    def start_engine(self):
        if self.mode == STATE_ON:
            debug_log(_('Engine started. Fuel %f kg') % self.fuel)
            self.running = True
        else:
            debug_log(_('Trying to start engine while the engine device is off'))

    def stop_engine(self):
        if not self.running:
            return
        debug_log(_('Engine stopped. Fuel %f kg') % self.fuel)
        self.running = False

    def set_traction(self, t):
        if self.mode == STATE_ON:
            traction = float(t)
            max_traction = float(self.device.max_traction)

            if traction < 0 or traction > max_traction:
                self.traction = max_traction
                debug_log(_('Bad engine traction value %f'), traction)
            else:
                self.traction = traction

            debug_log(_('Set engine traction %f'), self.traction)
        else:
            debug_log(_('Trying to set traction while the engine is off'))

    def check_fuel(self, df):
        return self.fuel >= df

    def decrement_fuel(self, df):
        self.fuel -= df
        self.mass -= df

class TelemetryDevice(RadioDevice):

    VARIABLES = LogicDevice.VARIABLES + ['period']
    CALLABLES = LogicDevice.CALLABLES + ['set_period', 'send_log_message']

    def __init__(self, xml, probe, start_mode, program, placement=None):
        RadioDevice.__init__(self, xml, probe, start_mode, program, placement)
        if hasattr(xml, 'min_period') and xml.min_period is not None:
            self.min_period = int(xml.min_period)
        else:
            self.min_period = 1
        if hasattr(xml, 'max_period') and xml.max_period is not None:
            self.max_period = int(xml.max_period)
        else:
            self.max_period = 3600 * 24
        self.period = self.min_period
        if hasattr(xml, 'data_volume') and xml.data_volume is not None:
            self.data_volume = float(xml.data_volume)
        else:
            self.data_volume = 4
        self.radio_type = 'telemetry'
        if self.device.radio_angle is not None:
            self.radio_angle = float(self.device.radio_angle)
        else:
            self.radio_angle = 360.0
        while self.radio_angle < 0:
            self.radio_angle += 360.0
        self.last_telemetry = 0

    def set_period(self, period):
        period = int(period)

        if not self.min_period <= period <= self.max_period:
            debug_log(_('The priod value %d exceeds the possible limits [%d:%d]') %
                      (period, self.min_period, self.max_period))
            if period < self.min_period:
                period = self.min_period
            else:
                period = self.max_period

        debug_log(_('Set telemetry period %d s'), period)
        self.period = period

    def send_log_message(self, s):
        debug_log(_('Telemetry message: %s'), s)
        self.put_data_broadcast(self.data_volume, ('telemetry', s))

    @classmethod
    def debug(cls, s):
        debug_log(_('Program debug: %s'), s)

class HeatControlDevice(LogicDevice):

    VARIABLES = LogicDevice.VARIABLES + ['temperature', 'heating']
    CALLABLES = LogicDevice.CALLABLES + ['start_heating', 'stop_heating']

    def __init__(self, xml, probe, start_mode, program, placement=None):
        LogicDevice.__init__(self, xml, probe, start_mode, program, placement)
        self.temperature = None
        self.heating = False
        self.heater_power = 0.0

    def turn_on(self):
        LogicDevice.turn_on(self)
        self.heating = False
        self.power = float(self.device.power)
        self.heat_production = float(self.device.power)
        self.set_power(float(self.device.heat_production))

    def turn_off(self):
        self.stop_heating()
        LogicDevice.turn_off(self)

    def sleep_mode(self):
        self.stop_heating()
        LogicDevice.sleep_mode(self)

    def set_power(self, p):
        if self.mode == STATE_ON:
            heater_power = float(p)
            max_heater_power = float(self.device.heat_production)

            if heater_power > max_heater_power:
                self.heater_power = max_heater_power
                debug_log(_('Too high heater power %f'),
                          heater_power)
            else:
                self.heater_power = heater_power

            debug_log(_('Set heater power %f'), self.heater_power)

            if self.heating:
                self.power = float(self.device.power) + self.heater_power
                self.heat_production = float(self.device.power) + self.heater_power
        else:
            debug_log(_('Trying to set heat power while the heat control device is off'))

    def start_heating(self):
        if self.mode == STATE_ON:
            debug_log(_('Start heating'))
            self.heating = True
            self.power = float(self.device.power) + self.heater_power
            self.heat_production = float(self.device.power) + self.heater_power
        else:
            debug_log(_('Tring to start heating while the heat control device is off'))

    def stop_heating(self):
        if not self.heating:
            return
        debug_log(_('Stop heating'))
        self.heating = False
        self.power = float(self.device.power)
        self.heat_production = float(self.device.power)

class LoadDevice(LogicDevice):
    MAX_SLOTS = 256

    def __init__(self, xml, probe, start_mode, program, placement=None):
        LogicDevice.__init__(self, xml, probe, start_mode, program, placement)
        self.photo = self.device.resolution is not None
        self.running = False

        # There are two types of load devices: cameras and scientific experiments containers
        if self.photo:
            self.camera_range = self.device.camera_range
            self.data_stream = int(float(self.device.data_stream) *
                                   1024 * 1024 / 8) # megabit/sec -> bytes/sec
            debug_log(_('Photocamera with the performance of %f Mbps -> %f B/s'),
                      self.device.data_stream, self.data_stream)
            self.memory_total = int(self.memory_size * 1024 * 1024)
            self.memory_used = 0
            self.memory_slots = [None] * self.MAX_SLOTS
            self.photo_data = 0
            self.visible_target = None
            self.target_offset_angle = None
            self.target_distance = None
            self.target_resolution = None
            self.target_incidence_angle = None
            self.best_visible_target = None
            self.best_target_offset_angle = None
            self.best_target_distance = None
            self.best_target_resolution = None
            self.best_target_incidence_angle = None
            self.max_temperature_diff = None
            self.valid_environment = None
        else:
            self.valid_environment = False
            self.start_angle = None
            self.start_time = None
            self.full_circle = False
            self.parachute_ready = False
            self.avg_temperature = (self.min_temperature + self.max_temperature) / 2.0
            self.max_temperature_diff = 0

    # --------------------------------------------------------------------------
    # Cameras
    # --------------------------------------------------------------------------
    def take_photo(self): #pylint: disable=R0912
        if not self.photo:
            debug_log(_('The device is not a camera'))
            return None

        if self.mode != STATE_ON:
            debug_log(_('Trying to take a photo while the camera is off'))
            return None

        if self.running:
            debug_log(_('The shooting is already performing'))
            return None

        if self.visible_target is not None:
            if self.target_offset_angle > float(self.device.camera_angle) / 2:
                self.visible_target = None

        if self.visible_target is not None:
            self.target_resolution = (2.0 *
                                      math.tan(math.radians(float(self.device.camera_angle) / 2)) *
                                      math.cos(math.radians(self.target_offset_angle)) *
                                      self.target_distance /
                                      float(self.device.resolution))
        else:
            self.target_resolution = None

        debug_log(_('Camera shot: %s'), str(self.visible_target))
        if self.target_offset_angle is not None:
            debug_log(_('Target offset angle: %.3f deg'), float(self.target_offset_angle))
        if self.target_distance is not None:
            debug_log(_('Distance to the target: %.3f m'), float(self.target_distance))
        if self.visible_target is not None:
            if self.target_resolution is not None:
                debug_log(_('Resolution: %.3f m/pixel'), float(self.target_resolution))
            if self.target_incidence_angle is not None:
                debug_log(_('Target incidence angle: %.3f deg'), float(self.target_incidence_angle))

        image_size = int(self.data_stream * 0.1) # TODO: make in a proper way

        free_memory = self.memory_total - self.memory_used
        if image_size > free_memory:
            debug_log(_('Insufficient memory to save the image'))
            return None

        slot_found = None
        for slot in range(len(self.memory_slots)):
            if self.memory_slots[slot] is None:
                slot_found = slot

        if slot_found is None:
            debug_log(_('There are no empty slot to save the image'))
            return None

        payload = {'camera_range': self.camera_range,
                   'visible_target': self.visible_target,
                   'target_offset_angle': self.target_offset_angle,
                   'target_distance': self.target_distance,
                   'target_resolution': self.target_resolution,
                   'target_incidence_angle': self.target_incidence_angle}

        self.memory_slots[slot_found] = (image_size, payload)
        self.memory_used += image_size

        return slot_found

    def start_shooting(self):
        if self.photo:
            if self.mode == STATE_ON:
                debug_log(_('Start shooting'))
                self.running = True
                self.photo_data = 0
                self.best_visible_target = None
                self.best_target_offset_angle = None
                self.best_target_distance = None
                self.best_target_incidence_angle = None
            else:
                debug_log(_('Trying to start shooting while the camera is off'))
        else:
            debug_log(_('The device is not a camera'))

    def stop_shooting(self):
        if not self.photo:
            debug_log(_('The device is not a camera'))
            return None

        if not self.running:
            return None

        debug_log(_('Stop shooting'))
        self.running = False

        if self.photo_data == 0:
            debug_log(_('Buffer is empty. Nothing was shooted'))
            return None

        if self.best_visible_target is not None:
            if self.best_target_offset_angle > float(self.device.camera_angle) / 2:
                self.best_visible_target = None

        if self.best_visible_target is not None:
            self.best_target_resolution = (2.0 *
                                           math.tan(math.radians(float(self.device.camera_angle) /
                                                                 2)) *
                                           math.cos(math.radians(self.best_target_offset_angle)) *
                                           self.best_target_distance /
                                           float(self.device.resolution))
        else:
            self.best_target_resolution = None

        debug_log(_('Camera shot: %s'), str(self.best_visible_target))
        if self.best_visible_target is not None:
            if self.best_target_offset_angle is not None:
                debug_log(_('The best target offset angle: %.3f deg'),
                          float(self.best_target_offset_angle))
            if self.best_target_distance is not None:
                debug_log(_('The best distance to target: %.3f m'),
                          float(self.best_target_distance))
            if self.best_target_resolution is not None:
                debug_log(_('The best resolution: %.3f m/pixel'),
                          float(self.best_target_resolution))
            if self.best_target_incidence_angle is not None:
                debug_log(_('The best target incidence angle: %.3f deg'),
                          float(self.best_target_incidence_angle))

        slot_found = None
        for slot in range(len(self.memory_slots)):
            if self.memory_slots[slot] is None:
                slot_found = slot

        if slot_found is None:
            debug_log(_('There are no empty slots to save the shot'))
            return None

        payload = {'camera_range': self.camera_range,
                   'visible_target': self.best_visible_target,
                   'target_offset_angle': self.best_target_offset_angle,
                   'target_distance': self.best_target_distance,
                   'target_resolution': self.best_target_resolution,
                   'target_incidence_angle': self.best_target_incidence_angle}

        self.memory_slots[slot_found] = (self.photo_data, payload)
        self.memory_used += self.photo_data

        return slot_found

    def get_image_size(self, slot):
        if not self.photo:
            debug_log(_('The device is not a camera'))
            return None

        if slot >= self.MAX_SLOTS:
            return None

        if self.memory_slots[slot] is None:
            return None

        return self.memory_slots[slot][0]

    def get_image_data(self, slot):
        if not self.photo:
            debug_log(_('The device is not a camera'))
            return None

        if slot >= self.MAX_SLOTS:
            return None

        if self.memory_slots[slot] is None:
            return None

        return self.memory_slots[slot][1]

    def remove_image(self, slot):
        if not self.photo:
            debug_log(_('The device is not a camera'))
            return

        if slot >= self.MAX_SLOTS:
            return

        if self.memory_slots[slot] is None:
            return

        self.memory_used -= self.memory_slots[slot][0]
        self.memory_slots[slot] = None

    # --------------------------------------------------------------------------
    # Containers for scientific experiments
    # --------------------------------------------------------------------------
    def start_experiment(self):
        if not self.photo:
            if self.mode == STATE_ON:
                if self.start_angle is None:
                    debug_log(_('Starting the experiment'))
                    self.running = True
                    self.valid_environment = True
                else:
                    debug_log(_('The experiment was already started'))
            else:
                debug_log(_('Trying to start experiment while the container is off'))
        else:
            debug_log(_('Cannot start experiment. The device is not a scientific container'))

    def check_temperature(self, T):
        LogicDevice.check_temperature(self, T)
        if not self.photo and self.running:
            dT = abs(T - self.avg_temperature)
            if dT > self.max_temperature_diff:
                self.max_temperature_diff = dT

    def stop_experiment(self):
        if self.photo:
            debug_log(_('Cannot stop experiment. The device is not a scientific container'))
            return

        if not self.running:
            return

        debug_log(_('The experiment finished'))
        self.running = False

    def set_para_height(self, h):
        debug_log(_('Set parachute activation height to %f m'), h)
        self.probe.parachute_height = h

    def drop(self):
        self.stop_experiment()
        self.probe.parachute_square = 0
        self.probe.drop_container()
        self.parachute_ready = True
        debug_log(_('The container was shot off'))

    def parachute_open(self):
        if self.parachute_ready:
            if self.probe.systems[SUBSYSTEM_NAVIGATION].velocity <= self.device.parachute_velocity:
                self.probe.parachute_square = self.device.parachute_square
                self.parachute_ready = False
                debug_log(_('The parachute has opened'))
            else:
                self.parachute_drop()
                debug_log(_('The parachute has dropped because of exceeding the maximum speed'))

    def parachute_drop(self):
        self.probe.parachute_square = 0
        self.probe.mass -= self.device.parachute_mass

    def turn_on(self):
        LogicDevice.turn_on(self)
        self.running = False

    def turn_off(self):
        if self.photo:
            self.stop_shooting()
        else:
            self.stop_experiment()
        LogicDevice.turn_off(self)

    def sleep_mode(self):
        if self.photo:
            self.stop_shooting()
        else:
            self.stop_experiment()
        LogicDevice.sleep_mode(self)

Device.DEVICE_CLASS = {
    SUBSYSTEM_CONSTRUCTION: ConstructionDevice,
    SUBSYSTEM_CPU: CPUDevice,
    SUBSYSTEM_RADIO: RadioDevice,
    SUBSYSTEM_ORIENTATION: OrientationDevice,
    SUBSYSTEM_NAVIGATION: NavigationDevice,
    SUBSYSTEM_ENGINE: EngineDevice,
    SUBSYSTEM_POWER: PowerDevice,
    SUBSYSTEM_TELEMETRY: TelemetryDevice,
    SUBSYSTEM_HEAT_CONTROL: HeatControlDevice,
    SUBSYSTEM_LOAD: LoadDevice
}

class Probe: # pylint: disable=R0902

    def __init__(self, name, probefile, parameters, devices_map): #pylint: disable=R0912
        probe = ProbeLoader.load_probe(Language, probefile)

        global _ # pylint: disable=W0603
        _ = Language.get_tr()

        self.Parameters = parameters
        self.Devices = devices_map
        self.name = probe.name
        self.filename = name
        self.xml = probe
        self.completed = False
        self.success = False
        self.success_score = None
        self.success_timestamp = None
        self.message_number = None
        self.telemetry_received = 0
        self.program_error = False
        self.collector = {}
        self.photo_resolution = None
        self.photo_offset_angle = None
        self.photo_incidence_angle = None
        self.photo_distance = None
        self.landing_error = None
        self.orbit_diff = None
        self.session_count = None
        self.session_length = None
        self.missiles_unintercepted = None
        self.detection_delay = None

        self.tournament = probe.flight.tournament
        self.planet = probe.flight.planet.name
        self.mission = probe.flight.mission.type
        if self.mission not in available_missions:
            critical_error(self, _("Mission %s is not supported") % self.mission)
        self.clear_telemetry = available_missions[self.mission]

        planet_params = self.Parameters.Planets[self.planet]

        if hasattr(probe.flight, 'time') and probe.flight.time is not None:
            self.start_time = probe.flight.time.start
        else:
            self.start_time = ''
        self.safe_mode = False
        self.aerodynamic_coeff = 1.05
        self.parachute_square = 0
        self.parachute_height = None
        self.parachute_aerodynamic_coeff = 0.9
        self.container_mode = False
        self.flight_result = ()
        self.flight_images = []
        self.landed = False
        self.max_telemetry_time = 0
        self.mass = 0.0

        self.systems = dict((d, None) for d in Device.DEVICE_CLASS)

        for d in probe.systems.system:
            if d.name not in self.Devices:
                if hasattr(d, 'type') and d.type is not None:
                    critical_error(self, _("Unknown subsystem type %s: %s") %
                                   (d.type, d.name))
                else:
                    critical_error(self, _("Unknown subsystem %s") % d.name)
            typ = str(self.Devices[d.name].type)
            if self.systems[typ] is not None:
                critical_error(self, _("More than one subsystem of type %s") % typ)
            program = d.program if hasattr(d, 'program') else None
            if ((program is None and
                 hasattr(d, 'hsm_diagram') and d.hsm_diagram is not None)):
                if d.hsm_diagram.type != sm.python_hsm.SUPPORTED_TYPE:
                    critical_error(self,
                                   _("HSM diagram of unsupported type %s in %s subsystem") %
                                   d.hsm_diagram.type, typ)
                try:
                    hsm_path = d.hsm_diagram.path
                    if not os.path.isfile(hsm_path):
                        hsm_path = os.path.join(os.path.dirname(probefile),
                                                hsm_path)
                        if not os.path.isfile(hsm_path):
                            critical_error(self,
                                           _("Cannot file HSM diagram file %s") %
                                           d.hsm_diagram.path)
                    program = sm.python_hsm.convert_graphml(hsm_path)
                except sm.python_hsm.HSMException as e:
                    critical_error(self,
                                   _("Error while converting HSM diagram %s: %s") %
                                   hsm_path, str(e))
            placement = d.placement if hasattr(d, 'placement') else None
            if hasattr(d, 'start_mode') and d.start_mode is not None:
                mode = d.start_mode
            else:
                mode = STATE_OFF
            self.systems[typ] = Device.init_device(self.Devices,
                                                   d.name,
                                                   self,
                                                   mode,
                                                   program,
                                                   placement)

        for sname, s in self.systems.items():
            if s:
                s.set_initial_mode()
            if not s and sname not in (SUBSYSTEM_ENGINE, SUBSYSTEM_RADIO, SUBSYSTEM_LOAD):
                critical_error(self, _("The required system %s should be enabled in the probe") %
                               sname)

        if (self.mission in [MISSION_CRYSTAL] and (self.systems[SUBSYSTEM_LOAD] is None or
                                                   self.systems[SUBSYSTEM_LOAD].photo)):
            critical_error(self, _("There is no required equipment for this mission: a container for scientific experiments")) # pylint: disable=C0301

        if (self.mission in [MISSION_INSPECT,
                             MISSION_DZZ,
                             MISSION_EARLY_WARNING] and (self.systems[SUBSYSTEM_LOAD] is None or
                                                         not self.systems[SUBSYSTEM_LOAD].photo)):
            critical_error(self, _("There is no required equipment for this mission: a camera"))

        if (self.mission in [MISSION_INSPECT,
                             MISSION_DZZ,
                             MISSION_TELECOM,
                             MISSION_SMS,
                             MISSION_TEST_SMS,
                             MISSION_MOLNIYA,
                             MISSION_EARLY_WARNING] and self.systems[SUBSYSTEM_RADIO] is None):
            critical_error(self, _("There is no required equipment for this mission: a high-performance transmitter")) # pylint: disable=C0301

        construction = self.systems[SUBSYSTEM_CONSTRUCTION]
        self.inertia_moment_factor, self.square = self.calculate_construction(construction)
        if hasattr(construction.device,
                   'max_acceleration') and construction.device.max_acceleration is not None:
            self.max_acceleration = float(construction.device.max_acceleration)
        else:
            self.max_acceleration = 9.8 * 15

        self.update_mass()
        debug_log(_('Probe mass: %f kg'), self.mass)

        if self.mass > planet_params.probe.max_mass:
            critical_error(self, _('The probe weight limit %.3f exceeded'), planet_params.max_mass)

        if self.inertia_moment <= 0:
            critical_error(self, _('The moment of inertia for the probe %.1f kg m^2 should be positive'), # pylint: disable=C0301
                           self.inertia_moment)

        cpu = self.systems[SUBSYSTEM_CPU]
        cpu.time_left = float(probe.flight.mission.duration) * 3600

        navigation = self.systems[SUBSYSTEM_NAVIGATION]
        navigation.initialize_flight(float(probe.flight.mission.orbit), 0.0)

        orientation = self.systems[SUBSYSTEM_ORIENTATION]
        orientation.initialize_flight(float(probe.flight.mission.start_angular_velocity))

        heat_control = self.systems[SUBSYSTEM_HEAT_CONTROL]
        heat_control.temperature = float(probe.flight.T_start)
        if hasattr(construction.device,
                   'heat_capacity') and construction.device.heat_capacity is not None:
            self.heat_capacity = float(construction.device.heat_capacity)
        else:
            self.heat_capacity = 800.0
        if hasattr(construction.device,
                   'heat_absorption') and construction.device.heat_absorption is not None:
            self.heat_absorption = float(construction.device.heat_absorption)
        else:
            self.heat_absorption = 10.0

        v = float(probe.construction.voltage)
        if v <= 0.0:
            critical_error(self, _("The voltage of the probe's electric network %.1f V should be positive"), v) # pylint: disable=C0301
        power = self.systems[SUBSYSTEM_POWER]
        power.init_power(v)

        if hasattr(probe.construction,
                   'xz_yz_solar_panel_fraction') and probe.construction.xz_yz_solar_panel_fraction is not None: # pylint: disable=C0301
            self.xz_yz_solar_panel_fraction = float(probe.construction.xz_yz_solar_panel_fraction)
            if self.xz_yz_solar_panel_fraction < 0.0 or self.xz_yz_solar_panel_fraction > 100.0:
                critical_error(self, _('The fraction of solar panels square %.1f%%%% should be between 0 and 100%%%%'), # pylint: disable=C0301
                               self.xz_yz_solar_panel_fraction)
        else:
            self.xz_yz_solar_panel_fraction = 0.0

        if hasattr(probe.construction,
                   'xz_yz_radiator_fraction') and probe.construction.xz_yz_radiator_fraction is not None: # pylint: disable=C0301
            self.xz_yz_radiator_fraction = float(probe.construction.xz_yz_radiator_fraction)
            if self.xz_yz_radiator_fraction < 0.0 or self.xz_yz_radiator_fraction > 100.0:
                critical_error(self, _('The fraction of radiator square (side) %.1f%%%% should be between 0 and 100%%%%'), # pylint: disable=C0301
                               self.xz_yz_radiator_fraction)
        else:
            self.xz_yz_radiator_fraction = 0.0

        if hasattr(probe.construction,
                   'xy_radiator_fraction') and probe.construction.xy_radiator_fraction is not None:
            self.xy_radiator_fraction = float(probe.construction.xy_radiator_fraction)
            if self.xy_radiator_fraction < 0.0 or self.xy_radiator_fraction > 100.0:
                critical_error(self, _('The fraction of radiator square (top-bottom) %.1f%%%% should be between 0%%%% and 100%%%%'), # pylint: disable=C0301
                               self.xy_radiator_fraction)
        else:
            self.xy_radiator_fraction = 0.0

        xz_yz_summary_fraction = self.xz_yz_solar_panel_fraction + self.xz_yz_radiator_fraction
        if xz_yz_summary_fraction > 100.0:
            critical_error(self,
                           _('The total square of side faces %.1f%%%% should not exceed 100%%%%'),
                           xz_yz_summary_fraction)

        self.volume_used = 0.0
        self.max_fuel_volume = 0.0
        for s in self.systems.values():
            if s and s != construction:
                # transfer liters to cubic meters
                self.volume_used += float(s.device.volume) / 1000.0
                if str(s.device.type) == SUBSYSTEM_ENGINE and (hasattr(s.device, 'fuel') and
                                                               s.device.fuel is not None):
                    self.max_fuel_volume += float(s.device.fuel) / 1000.0

        if self.volume_used > float(construction.device.volume) / 1000.0:
            critical_error(self,
                           _('The value of devices %.5f m^3 exceeds the possible value of construction %.5f m^3'), # pylint: disable=C0301
                           self.volume_used,
                           float(construction.device.volume) / 1000.0)

        engine = self.systems[SUBSYSTEM_ENGINE]
        if engine:
            fuel_mass = 0
            if hasattr(probe.construction, 'fuel') and probe.construction.fuel is not None:
                fuel_mass = float(probe.construction.fuel)
                fuel_volume = fuel_mass / float(planet_params.probe.fuel_density)
                if fuel_volume > self.max_fuel_volume:
                    critical_error(self,
                                   _('The value of fuel %f m^3 exceeds the possible value of fuel tanks %f m^3'), # pylint: disable=C0301
                                   fuel_volume, self.max_fuel_volume)
            engine.initialize_fuel(fuel_mass)
        self.update_mass()
        debug_log(_('Total mass (with fuel): %f kg'), self.mass)

    def print_probe(self):
#        self.Parameters.debug_parameters(self.planet, debug_log)
        self.debug_probe(debug_log)
        debug_log('')

#        self.Parameters.debug_parameters(self.planet)
        self.debug_probe()
        mission_log('')
        mission_log(_('The flight log:'))

    @classmethod
    def calculate_construction(cls, construction):
        a = pow(float(construction.device.volume), 1.0 / 3.0) / 10
        debug_log(_("The size of the probe's side: %f"), a)
        square = a ** 2
        return (1/12.0) * 2.0 * square, square

    def update_mass(self):
        self.mass = 0.0
        for s in self.systems.values():
            if s:
                self.mass += s.mass
        self.inertia_moment = self.mass * self.inertia_moment_factor

    def time(self):
        return self.systems[SUBSYSTEM_CPU].flight_time

    def mission_ended(self):
        return self.completed or self.landed or self.systems[SUBSYSTEM_CPU].time_left <= 0

    def safe_mode_on(self):
        if not self.safe_mode:
            debug_log(_('Going to SAFE MODE'))
            for s in self.systems.values():
                if s and s.device.type != SUBSYSTEM_CONSTRUCTION:
                    if s.device.type == SUBSYSTEM_CPU:
                        s.set_mode(STATE_SAFE)
                    elif s.device.type == SUBSYSTEM_POWER or s.device.type == SUBSYSTEM_TELEMETRY:
                        s.set_mode(STATE_ON)
                    else:
                        s.set_mode(STATE_OFF)
            self.safe_mode = True

    def safe_mode_off(self):
        self.safe_mode = False

    def drop_container(self):
        if self.container_mode:
            critical_error(self, _('Trying to drop already dropped container'))
        load = self.systems[SUBSYSTEM_LOAD]
        if load is None or load.photo:
            critical_error(self, _('Trying to drop a container while the probe has no container'))

        self.container_mode = True
        for s in self.systems.values():
            if s and s.device.type != SUBSYSTEM_CONSTRUCTION:
                s.set_mode(STATE_OFF)
        self.aerodynamic_coeff = 0.47
        radius = pow(float(load.device.volume) * 3.0 / (4.0 * math.pi), 1/3.0)
        self.inertia_moment_factor = 2.0 * radius * radius / 5.0
        self.square = math.pi * radius * radius
        self.mass = load.device.mass
        self.update_mass()

    def debug_probe(self, logger=mission_log):
        navig = self.systems[SUBSYSTEM_NAVIGATION]
        orient = self.systems[SUBSYSTEM_ORIENTATION]
        logger(_('Probe %s:'), str(self.name))
        logger(_('\tFlight parameters:'))
        logger(_('\t\tPlanet: %s'), self.planet)
        logger(_('\t\tStart temperature: %.1f К'),
               self.systems[SUBSYSTEM_HEAT_CONTROL].temperature)
        logger(_('\t\tStart time of the autonomous flight: %s'), self.start_time)
        logger(_('\t\tFlight duration: %d h'), self.systems[SUBSYSTEM_CPU].time_left / 3600)
        logger(_('\t\tOrbit height: %.2f m'), navig.orbit_height)
        logger(_('\t\tStart angle: %.2f deg'), navig.angle)
        logger(_('\t\tStart orientation angle: %.2f deg'), orient.orient_angle)
        logger(_('\t\tStart rotation speed of the probe: %.2f deg/s'), orient.angular_velocity)
        # logger(_('\t\tTarget:'))
        # logger(_('\t\t\tX coord: %.1f m'), self.target.x)
        # logger(_('\t\t\tY coord: %.1f m'), self.target.y)
        logger(_('\tSubsystems:'))
        min_T = -1000
        max_T = 1000
        for sysname, system in self.systems.items():
            if system:
                if isinstance(system.program, str):
                    p = '\t' + '\n\t'.join(system.program.split('\n'))
                else:
                    p = _('\tNo')
                logger(_('\t\tSubsystem %s: device %s, m %f v %f st.state %s, program:\n%s\n'),
                       sysname,
                       system.device.full_name,
                       system.device.mass,
                       system.device.volume,
                       system.mode,
                       p)
                if system.device.min_temperature > min_T:
                    min_T = float(system.device.min_temperature)
                if system.device.max_temperature < max_T:
                    max_T = float(system.device.max_temperature)
            else:
                logger(_('\t\tSubsystem %s is absent\n'), sysname)
        logger(_('\tStart mass: %.4f kg'), self.mass)
        logger(_("\tSystems' volume: %.5f m^3"), self.volume_used)
        logger(_('\tMin temperature: %.1f K'), min_T + 273)
        logger(_('\tMax temperature: %.1f K'), max_T + 273)
        logger(_('\tStart power generation: %.2f W'),
               self.systems[SUBSYSTEM_POWER].power_generation)

    def write_short_log(self, filename, data, events, addparams):
        if self.success_score is not None:
            score = self.success_score
        else:
            score = 0.0
        res = ShortLogLoader.generate_short_log(self.tournament,
                                                self.name,
                                                self.planet,
                                                self.mission,
                                                self.time(),
                                                self.flight_result[0],
                                                self.flight_result[1],
                                                score,
                                                self.flight_images,
                                                self.telemetry_received or self.program_error,
                                                data,
                                                events,
                                                addparams)

        f = open(filename, 'w')
        f.truncate()
        f.write(res)
        f.close()

def calculate_distance2(v1, v2):
    return (v1.x - v2.x) ** 2 + (v1.y - v2.y) ** 2  + (v1.z - v2.z) ** 2

def calculate_distance(v1, v2):
    return math.sqrt(calculate_distance2(v1, v2))
