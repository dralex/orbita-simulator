# -----------------------------------------------------------------------------
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# The Orbita Simulator
# The Earth orbit simulation model (v2)
#
# Satellite system-level API
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

import importlib
from google.protobuf.message import EncodeError, DecodeError
import systems_pb2 as proto

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
    def __init__(self, send_to_controller, receive_from_controller):
        self.cpu = CPU(send_to_controller, receive_from_controller)
        self.telemetry = Telemetry(send_to_controller, receive_from_controller)
        self.transmitter = Transmitter(send_to_controller, receive_from_controller)
        self.power = Power(send_to_controller, receive_from_controller)
        self.navigation = Navigation(send_to_controller, receive_from_controller)
        self.orientation = Orientation(send_to_controller, receive_from_controller)
        self.engine = Engine(send_to_controller, receive_from_controller)
        self.heat_control = HeatControl(send_to_controller, receive_from_controller)
        self.camera = Camera(send_to_controller, receive_from_controller)
        self.container = Container(send_to_controller, receive_from_controller)

# -----------------------------------------------------------------------------
# Abstract system class
# -----------------------------------------------------------------------------

class System:
    def __init__(self, kind, send_to_controller, receive_from_controller):
        self._send_to_controller = send_to_controller
        self._receive_from_controller = receive_from_controller
        self._kind = kind

    @classmethod
    def _serialize_request(cls, system, command, *args):
        request = proto.Request()
        request.system = system
        request.command = command

        for i in range(len(args) // 2):
            argument = request.arguments.add()

            arg_type = args[i * 2]
            arg_value = args[i * 2 + 1]

            if arg_type == 'none':
                pass
            elif arg_type == 'boolean':
                argument.boolean = bool(arg_value)
            elif arg_type == 'integer':
                argument.integer = int(arg_value)
            elif arg_type == 'real':
                argument.real = float(arg_value)
            elif arg_type == 'text':
                argument.text = str(arg_value)
            elif arg_type == 'data':
                argument.data = str(arg_value)
            elif arg_type == 'message':
                argument.message.CopyFrom(arg_value)
            else:
                raise BadParametersError

        try:
            data = request.SerializeToString()
        except EncodeError:
            raise GenericError

        return data

    def make_call(self, command, *args): # pylint: disable=R0912,R0911
        request_data = self._serialize_request(self._kind, command, *args)
        self._send_to_controller(request_data)
        response_data = self._receive_from_controller()

        try:
            response = proto.Response()
            response.ParseFromString(response_data)
        except DecodeError:
            raise GenericError

        if response.WhichOneof('Outcomes') == 'result':
            result = response.result
            if result.WhichOneof('Types') == 'boolean':
                return bool(result.boolean)
            if result.WhichOneof('Types') == 'integer':
                return int(result.integer)
            if result.WhichOneof('Types') == 'real':
                return float(result.real)
            if result.WhichOneof('Types') == 'text':
                return str(result.text)
            if result.WhichOneof('Types') == 'data':
                return str(result.data)
            if result.WhichOneof('Types') == 'message':
                msg = proto.Message()
                msg.CopyFrom(result.message)
                return msg
            raise GenericError
        if response.WhichOneof('Outcomes') == 'error':
            error = response.error
            if error == proto.ERROR_SYSTEM_NOT_AVAIL:
                raise SystemNotAvailableError
            if error == proto.ERROR_NOT_SUPPORTED:
                raise NotSupportedError
            if error == proto.ERROR_BAD_PARAMETERS:
                raise BadParametersError
            raise GenericError
        return None

    def get_state(self):
        return self.make_call(proto.CALL_GET_STATE)

    def set_state(self, state):
        if state is None:
            raise BadParametersError
        if not isinstance(state, int):
            raise BadParametersError
        return self.make_call(proto.CALL_SET_STATE, 'integer', state)

    def sleep(self, timeout):
        if timeout is None:
            raise BadParametersError
        if not isinstance(timeout, (int, float)):
            raise BadParametersError
        return self.make_call(proto.CALL_SLEEP, 'real', timeout)

    def dispatch(self, event, name=None, value=None):
        if not isinstance(event, str):
            raise BadParametersError
        if name is None:
            return self.make_call(proto.CALL_DISPATCH, 'text', event)
        if value is None:
            raise BadParametersError
        if not isinstance(name, str) or not isinstance(value, str):
            raise BadParametersError
        return self.make_call(proto.CALL_DISPATCH, 'text',
                              "{}:{}:{}".format(event, name, value))

    def has_event(self):
        ev = self.make_call(proto.CALL_HAS_EVENT)
        if not ev:
            return None
        if ev.find(':') < 0:
            return ev
        return ev.split(':')

# -----------------------------------------------------------------------------
# CPU system class
# -----------------------------------------------------------------------------

class CPU(System):
    def __init__(self, send_to_controller, receive_from_controller):
        System.__init__(self, proto.SYSTEM_CPU, send_to_controller, receive_from_controller)

    def run(self):
        return self.make_call(proto.CALL_CPU_RUN)

    def get_flight_time(self):
        return self.make_call(proto.CALL_CPU_GET_FLIGHT_TIME)

    def mission_completed(self):
        return self.make_call(proto.CALL_CPU_SUCCESS)

    def terminate(self):
        return self.make_call(proto.CALL_CPU_TERMINATE)

# -----------------------------------------------------------------------------
# Telemetry system class
# -----------------------------------------------------------------------------

class Telemetry(System):
    def __init__(self, send_to_controller, receive_from_controller):
        System.__init__(self, proto.SYSTEM_TELEMETRY, send_to_controller, receive_from_controller)

    def set_period(self, period):
        if period is None:
            raise BadParametersError
        if not isinstance(period, int):
            raise BadParametersError
        return self.make_call(proto.CALL_TELEMETRY_SET_PERIOD, 'integer', period)

    def send_message(self, text):
        if text is None:
            raise BadParametersError
        if not isinstance(text, str):
            raise BadParametersError
        return self.make_call(proto.CALL_TELEMETRY_SEND_MESSAGE, 'text', text)

    def debug(self, text):
        if text is None:
            raise BadParametersError
        if not isinstance(text, str):
            raise BadParametersError
        return self.make_call(proto.CALL_TELEMETRY_DEBUG, 'text', text)

# -----------------------------------------------------------------------------
# High-performance radio system class
# -----------------------------------------------------------------------------

class Transmitter(System):
    def __init__(self, send_to_controller, receive_from_controller):
        System.__init__(self, proto.SYSTEM_TRANSMITTER, send_to_controller, receive_from_controller)

    def send_data(self, msg_type, data, receiver=-1, sender=-1, timeout=None):
        if msg_type is None:
            raise BadParametersError
        if not isinstance(msg_type, int):
            raise BadParametersError
        if data is None:
            raise BadParametersError
        if not isinstance(data, bytes):
            raise BadParametersError
        if sender is None:
            raise BadParametersError
        if not isinstance(sender, int):
            raise BadParametersError
        if receiver is None:
            raise BadParametersError
        if not isinstance(receiver, int):
            raise BadParametersError
        if timeout is not None:
            if not isinstance(timeout, (int, float)):
                raise BadParametersError
        msg = proto.Message()
        msg.receiver = receiver
        msg.sender = sender
        msg.type = msg_type
        msg.id = 0
        msg.data = data
        msg.send_time = 0.0
        if timeout is not None:
            msg.timeout = timeout
        return self.make_call(proto.CALL_TRANSMITTER_SEND_DATA, 'message', msg)

    def send_photo(self, slot_num, receiver=None):
        if slot_num is None:
            raise BadParametersError
        if not isinstance(slot_num, int):
            raise BadParametersError
        if receiver is None:
            return self.make_call(proto.CALL_TRANSMITTER_SEND_PHOTO, 'integer', slot_num)
        if not isinstance(receiver, int):
            raise BadParametersError
        return self.make_call(proto.CALL_TRANSMITTER_SEND_PHOTO_TO, 'integer',
                              slot_num, 'integer', receiver)

    def receive(self, sender):
        if sender is None:
            raise BadParametersError
        if not isinstance(sender, int):
            raise BadParametersError
        return self.make_call(proto.CALL_TRANSMITTER_RECEIVE, 'integer', sender)

    def get_progress(self, sender):
        if sender is None:
            raise BadParametersError
        if not isinstance(sender, int):
            raise BadParametersError
        return self.make_call(proto.CALL_TRANSMITTER_GET_PROGRESS, 'integer', sender)

    def get_message(self, sender):
        if sender is None:
            raise BadParametersError
        if not isinstance(sender, int):
            raise BadParametersError
        return self.make_call(proto.CALL_TRANSMITTER_GET_MESSAGE, 'integer', sender)

# -----------------------------------------------------------------------------
# Power system class
# -----------------------------------------------------------------------------

class Power(System):
    def __init__(self, send_to_controller, receive_from_controller):
        System.__init__(self, proto.SYSTEM_POWER, send_to_controller,
                        receive_from_controller)

    def get_battery_capacity(self):
        return self.make_call(proto.CALL_POWER_GET_BATTERY_CAPACITY)

    def get_generation(self):
        return self.make_call(proto.CALL_POWER_GET_GENERATION)

    def get_consumption(self):
        return self.make_call(proto.CALL_POWER_GET_CONSUMPTION)

# -----------------------------------------------------------------------------
# Navigation system class
# -----------------------------------------------------------------------------

class Navigation(System):
    def __init__(self, send_to_controller, receive_from_controller):
        System.__init__(self, proto.SYSTEM_NAVIGATION, send_to_controller,
                        receive_from_controller)

    def get_orbit_height(self):
        return self.make_call(proto.CALL_NAVI_GET_ORBIT_HEIGHT)

    def get_z_axis_angle(self):
        return self.make_call(proto.CALL_NAVI_GET_Z_AXIS_ANGLE)

    def get_x_coord(self):
        return self.make_call(proto.CALL_NAVI_GET_X_COORD)

    def get_y_coord(self):
        return self.make_call(proto.CALL_NAVI_GET_Y_COORD)

    def get_transversal_velocity(self):
        return self.make_call(proto.CALL_NAVI_GET_TRANSVERSAL_VELOCITY)

    def get_radial_velocity(self):
        return self.make_call(proto.CALL_NAVI_GET_RADIAL_VELOCITY)

# -----------------------------------------------------------------------------
# Orientation system class
# -----------------------------------------------------------------------------

class Orientation(System):
    def __init__(self, send_to_controller, receive_from_controller):
        System.__init__(self, proto.SYSTEM_ORIENTATION, send_to_controller,
                        receive_from_controller)

    def get_angle(self, axis):
        if axis is None:
            raise BadParametersError
        if not isinstance(axis, int):
            raise BadParametersError
        return self.make_call(proto.CALL_ORIENT_GET_ANGLE, 'integer', axis)

    def get_angular_velocity(self, axis):
        if axis is None:
            raise BadParametersError
        if not isinstance(axis, int):
            raise BadParametersError
        return self.make_call(proto.CALL_ORIENT_GET_ANGULAR_VELOCITY, 'integer', axis)

    def start_motor(self, axis):
        if axis is None:
            raise BadParametersError
        if not isinstance(axis, int):
            raise BadParametersError
        return self.make_call(proto.CALL_ORIENT_START_MOTOR, 'integer', axis)

    def stop_motor(self, axis):
        if axis is None:
            raise BadParametersError
        if not isinstance(axis, int):
            raise BadParametersError
        return self.make_call(proto.CALL_ORIENT_STOP_MOTOR, 'integer', axis)

    def set_motor_moment(self, axis, torsion):
        if axis is None:
            raise BadParametersError
        if not isinstance(axis, int):
            raise BadParametersError
        if torsion is None:
            raise BadParametersError
        if not isinstance(torsion, (int, float)):
            raise BadParametersError
        return self.make_call(proto.CALL_ORIENT_SET_MOTOR_MOMENT, 'integer', axis, 'real', torsion)

    def start_coil(self, axis):
        if axis is None:
            raise BadParametersError
        if not isinstance(axis, int):
            raise BadParametersError
        return self.make_call(proto.CALL_ORIENT_START_COIL, 'integer', axis)

    def stop_coil(self, axis):
        if axis is None:
            raise BadParametersError
        if not isinstance(axis, int):
            raise BadParametersError
        return self.make_call(proto.CALL_ORIENT_STOP_COIL, 'integer', axis)

# -----------------------------------------------------------------------------
# Engine system class
# -----------------------------------------------------------------------------

class Engine(System):
    def __init__(self, send_to_controller, receive_from_controller):
        System.__init__(self, proto.SYSTEM_ENGINE, send_to_controller,
                        receive_from_controller)

    def get_fuel(self):
        return self.make_call(proto.CALL_ENGINE_GET_FUEL)

    def start_engine(self):
        return self.make_call(proto.CALL_ENGINE_START_ENGINE)

    def stop_engine(self):
        return self.make_call(proto.CALL_ENGINE_STOP_ENGINE)

    def set_traction(self, traction):
        if traction is None:
            raise BadParametersError
        if not isinstance(traction, (int, float)):
            raise BadParametersError
        return self.make_call(proto.CALL_ENGINE_SET_TRACTION, 'real', traction)

# -----------------------------------------------------------------------------
# Heat control class
# -----------------------------------------------------------------------------

class HeatControl(System):
    def __init__(self, send_to_controller, receive_from_controller):
        System.__init__(self, proto.SYSTEM_HEATCONTROL, send_to_controller,
                        receive_from_controller)

    def get_temperature(self):
        return self.make_call(proto.CALL_HC_GET_TEMPERATURE)

    def start_heating(self):
        return self.make_call(proto.CALL_HC_START_HEATING)

    def stop_heating(self):
        return self.make_call(proto.CALL_HC_STOP_HEATING)

    def set_power(self, power):
        if power is None:
            raise BadParametersError
        if not isinstance(power, (int, float)):
            raise BadParametersError
        return self.make_call(proto.CALL_HC_SET_POWER, 'real', power)

# -----------------------------------------------------------------------------
# Camera class
# -----------------------------------------------------------------------------

class Camera(System):
    def __init__(self, send_to_controller, receive_from_controller):
        System.__init__(self, proto.SYSTEM_CAMERA, send_to_controller,
                        receive_from_controller)

    def take_photo(self):
        return self.make_call(proto.CALL_CAMERA_TAKE_PHOTO)

    def start_shooting(self):
        return self.make_call(proto.CALL_CAMERA_START_SHOOTING)

    def stop_shooting(self):
        return self.make_call(proto.CALL_CAMERA_STOP_SHOOTING)

    def get_image_size(self, slot_num):
        if slot_num is None:
            raise BadParametersError
        if not isinstance(slot_num, int):
            raise BadParametersError
        return self.make_call(proto.CALL_CAMERA_GET_IMAGE_SIZE, 'integer', slot_num)

# -----------------------------------------------------------------------------
# Container
# -----------------------------------------------------------------------------

class Container(System):
    def __init__(self, send_to_controller, receive_from_controller):
        System.__init__(self, proto.SYSTEM_CONTAINER, send_to_controller,
                        receive_from_controller)

    def start_experiment(self):
        return self.make_call(proto.CALL_CONTAINER_START_EXPERIMENT)

    def stop_experiment(self):
        return self.make_call(proto.CALL_CONTAINER_STOP_EXPERIMENT)

    def set_parachute_height(self, height):
        if height is None:
            raise BadParametersError
        if not isinstance(height, (int, float)):
            raise BadParametersError
        return self.make_call(proto.CALL_CONTAINER_SET_PARA_HEIGHT, 'real', height)

    def drop(self):
        return self.make_call(proto.CALL_CONTAINER_DROP)

# -----------------------------------------------------------------------------
# Build global namespace for user code
# -----------------------------------------------------------------------------

def build_globals(send_to_controller, receive_from_controller):
    math = importlib.import_module('math')
    pysm = importlib.import_module('pysm')
    sputnik = Sputnik(send_to_controller, receive_from_controller)
    user_globals = {'math' : math,
                    'pysm' : pysm,
                    'sputnik': sputnik,
                    'cpu': sputnik.cpu,
                    'telemetry': sputnik.telemetry,
                    'transmitter': sputnik.transmitter,
                    'power': sputnik.power,
                    'navigation': sputnik.navigation,
                    'orientation': sputnik.orientation,
                    'engine': sputnik.engine,
                    'heat_control': sputnik.heat_control,
                    'camera': sputnik.camera,
                    'container': sputnik.container,
                    'debug': sputnik.telemetry.debug,
                    'STATE_NOT_INITIALIZED': proto.STATE_NOT_INITIALIZED,
                    'STATE_OFF': proto.STATE_OFF,
                    'STATE_ON': proto.STATE_ON,
                    'STATE_SLEEP': proto.STATE_SLEEP,
                    'STATE_DEAD': proto.STATE_DEAD,
                    'STATE_SAFE': proto.STATE_SAFE,
                    'STATE_WAKEUP': proto.STATE_WAKEUP,
                    'GenericError': GenericError,
                    'SystemNotAvailableError': SystemNotAvailableError,
                    'NotSupportedError': NotSupportedError,
                    'BadParametersError': BadParametersError,
                    'MESSAGE_TELEMETRY': proto.MESSAGE_TELEMETRY,
                    'MESSAGE_PHOTO': proto.MESSAGE_PHOTO,
                    'MESSAGE_SMS': proto.MESSAGE_SMS,
                    'AXIS_X': proto.AXIS_X,
                    'AXIS_Y': proto.AXIS_Y,
                    'AXIS_Z': proto.AXIS_Z}

    return user_globals
