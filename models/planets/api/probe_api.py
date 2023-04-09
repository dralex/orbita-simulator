# -----------------------------------------------------------------------------
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# The Orbita Simulator
# The planet landing model
#
# Simple probe API
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

import importlib
from google.protobuf.message import EncodeError, DecodeError
import probe_pb2 as proto

class GenericError(Exception):
    pass

class SystemNotAvailableError(GenericError):
    pass

class NotSupportedError(GenericError):
    pass

class BadParametersError(GenericError):
    pass

# -----------------------------------------------------------------------------
# Abstract system class
# -----------------------------------------------------------------------------

class ProbeBase:
    def __init__(self, send_to_controller, receive_from_controller):
        self._send_to_controller = send_to_controller
        self._receive_from_controller = receive_from_controller

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
            else:
                raise BadParametersError

        try:
            data = request.SerializeToString()
        except EncodeError:
            raise GenericError

        return data

    def make_call(self, command, *args): # pylint: disable=R0912
        request_data = self._serialize_request(0, command, *args)
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


# -----------------------------------------------------------------------------
# High-level API class
# -----------------------------------------------------------------------------

class Probe(ProbeBase):
    def __init__(self, send_to_controller, receive_from_controller):
        ProbeBase.__init__(self, send_to_controller, receive_from_controller)

    def run(self):
        return self.make_call(proto.CALL_RUN)

    def get_device_state(self, device_id):
        if device_id is None:
            raise BadParametersError
        if not isinstance(device_id, str):
            raise BadParametersError
        if len(device_id) == 0:
            raise BadParametersError
        return self.make_call(proto.CALL_GET_DEVICE_STATE, 'text', device_id)

    def set_device_state(self, device_id, state):
        if device_id is None:
            raise BadParametersError
        if not isinstance(device_id, str):
            raise BadParametersError
        if len(device_id) == 0:
            raise BadParametersError
        if state not in (proto.STATE_OFF, proto.STATE_ON):
            raise BadParametersError
        return self.make_call(proto.CALL_SET_DEVICE_STATE, 'text', device_id, 'integer', int(state))

    def get_device_period(self, device_id):
        if device_id is None:
            raise BadParametersError
        if not isinstance(device_id, str):
            raise BadParametersError
        if len(device_id) == 0:
            raise BadParametersError
        return self.make_call(proto.CALL_GET_DEVICE_PERIOD, 'text', device_id)

    def set_device_period(self, device_id, period):
        if device_id is None:
            raise BadParametersError
        if not isinstance(device_id, str):
            raise BadParametersError
        if len(device_id) == 0:
            raise BadParametersError
        if not isinstance(period, int) and not isinstance(period, float):
            raise BadParametersError
        return self.make_call(proto.CALL_SET_DEVICE_PERIOD, 'text', device_id,
                              'real', float(period))

    def cpu_get_flight_time(self):
        return self.make_call(proto.CALL_CPU_GET_FLIGHT_TIME)

    def cpu_drop_stage(self):
        return self.make_call(proto.CALL_CPU_DROP_STAGE)

    def telemetry_send_message(self, text):
        if text is None:
            raise BadParametersError
        if not isinstance(text, str):
            raise BadParametersError
        return self.make_call(proto.CALL_TELEMETRY_SEND_MESSAGE, 'text', text)

    def transmitter_get_bandwidth(self):
        return self.make_call(proto.CALL_TRANSMITTER_GET_BANDWIDTH)

    def transmitter_get_traffic(self):
        return self.make_call(proto.CALL_TRANSMITTER_GET_TRAFFIC)

    def power_get_battery_capacity(self):
        return self.make_call(proto.CALL_POWER_GET_BATTERY_CAPACITY)

    def power_get_generation(self):
        return self.make_call(proto.CALL_POWER_GET_GENERATION)

    def power_get_consumption(self):
        return self.make_call(proto.CALL_POWER_GET_CONSUMPTION)

    def navigation_get_accel(self):
        return self.make_call(proto.CALL_NAVI_GET_ACCEL)

    def navigation_has_landed(self):
        return self.make_call(proto.CALL_NAVI_HAS_LANDED)

    def engine_get_fuel(self):
        return self.make_call(proto.CALL_ENGINE_GET_FUEL)

    def engine_set_angle(self, device_id, angle):
        if device_id is None:
            raise BadParametersError
        if not isinstance(device_id, str):
            raise BadParametersError
        if len(device_id) == 0:
            raise BadParametersError
        if not isinstance(angle, int) and not isinstance(angle, float):
            raise BadParametersError
        return self.make_call(proto.CALL_ENGINE_SET_ANGLE, 'text', device_id, 'real', float(angle))

    def heat_control_get_temperature(self):
        return self.make_call(proto.CALL_HC_GET_TEMPERATURE)

    def heat_control_get_ext_temperature(self):
        return self.make_call(proto.CALL_HC_GET_EXT_TEMPERATURE)

# -----------------------------------------------------------------------------
# Build global namespace for user code
# -----------------------------------------------------------------------------

def build_globals(send_to_controller, receive_from_controller):
    math = importlib.import_module('math')
    probe = Probe(send_to_controller, receive_from_controller)
    user_globals = {'math' : math,
                    'probe': probe,
                    'STATE_OFF': proto.STATE_OFF,
                    'STATE_ON': proto.STATE_ON,
                    'STATE_DEAD': proto.STATE_DEAD,
                    'GenericError': GenericError,
                    'SystemNotAvailableError': SystemNotAvailableError,
                    'NotSupportedError': NotSupportedError,
                    'BadParametersError': BadParametersError}
    return user_globals
