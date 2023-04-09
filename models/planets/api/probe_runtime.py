# -----------------------------------------------------------------------------
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# The Orbita Simulator
# The planet landing model
#
# Simple probe API runtime
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

from google.protobuf.message import DecodeError
import data
import api.probe_pb2 as proto

# -----------------------------------------------------------------------------
# High-level runtime class
# -----------------------------------------------------------------------------

class ProbeRuntime:
    def __init__(self, probe):
        self.probe = probe
        self.state_map = {
            'ON': proto.STATE_ON,
            'OFF': proto.STATE_OFF,
            'DEAD': proto.STATE_DEAD
        }
        self.command_args = {
            proto.CALL_GET_DEVICE_STATE: ['text'],
            proto.CALL_SET_DEVICE_STATE: ['text', 'integer'],
            proto.CALL_GET_DEVICE_PERIOD: ['text'],
            proto.CALL_SET_DEVICE_PERIOD: ['text', 'real'],
            proto.CALL_CPU_GET_FLIGHT_TIME: [],
            proto.CALL_CPU_DROP_STAGE: [],
            proto.CALL_TELEMETRY_SEND_MESSAGE: ['text'],
            proto.CALL_NAVI_GET_ACCEL: [],
            proto.CALL_NAVI_HAS_LANDED: [],
            proto.CALL_POWER_GET_BATTERY_CAPACITY: [],
            proto.CALL_POWER_GET_GENERATION: [],
            proto.CALL_POWER_GET_CONSUMPTION: [],
            proto.CALL_TRANSMITTER_GET_BANDWIDTH: [],
            proto.CALL_TRANSMITTER_GET_TRAFFIC: [],
            proto.CALL_HC_GET_EXT_TEMPERATURE: [],
            proto.CALL_HC_GET_TEMPERATURE: [],
            proto.CALL_ENGINE_GET_FUEL: [],
            proto.CALL_ENGINE_SET_ANGLE: ['text', 'real'],
        }
        self.device_commands = set((proto.CALL_GET_DEVICE_STATE,
                                    proto.CALL_SET_DEVICE_STATE,
                                    proto.CALL_GET_DEVICE_PERIOD,
                                    proto.CALL_SET_DEVICE_PERIOD,
                                    proto.CALL_ENGINE_SET_ANGLE))
    @classmethod
    def deserialize_request(cls, d):
        try:
            request = proto.Request()
            request.ParseFromString(d)
        except DecodeError:
            request = None
        return request

    @classmethod
    def serialize_response(cls, response):
        return response.SerializeToString()

    def process_call(self, d): # pylint: disable=R0912
        request = self.deserialize_request(d)
        response, next_step = self.__process_command(request)
        return self.serialize_response(response), next_step

    def __process_command(self, request): # pylint: disable=R0911
        response = proto.Response()

        if request is None:
            response.error = proto.ERROR_UNKNOWN
            return response, False

        cmd = request.command
        args = request.arguments

        if cmd == proto.CALL_RUN:
            response.result.boolean = True
            return response, True

        if cmd not in self.command_args:
            response.error = proto.ERROR_NOT_SUPPORTED
            return response, False

        req_arg_types = self.command_args[cmd]
        parsed_args = []

        if len(args) != len(req_arg_types):
            response.error = proto.ERROR_BAD_PARAMETERS
            return response, False

        if len(args) > 0:
            for i, arg in enumerate(args):
                req_type = req_arg_types[i]
                if arg.WhichOneof('Types') == req_type:
                    parsed_args.append(getattr(arg, req_type))
                else:
                    response.error = proto.ERROR_BAD_PARAMETERS
                    return response, False

        if cmd in self.device_commands:
            device_id = parsed_args[0]
            d = data.probe_device_by_identifier(self.probe, device_id)
            if d is None:
                response.error = proto.ERROR_SYSTEM_NOT_AVAIL
                return response, False
            if cmd == proto.CALL_GET_DEVICE_STATE:
                response.result.integer = self.state_map[d.state]
            elif cmd == proto.CALL_SET_DEVICE_STATE:
                pstate = parsed_args[1]
                if pstate == proto.STATE_ON:
                    command = 'TURNON'
                elif pstate == proto.STATE_OFF:
                    command = 'TURNOFF'
                else:
                    response.error = proto.ERROR_BAD_PARAMETERS
                    return response, False
                data.probe_do_command(self.probe, d, command, None)
            elif cmd == proto.CALL_GET_DEVICE_PERIOD:
                response.result.real = d.period
            elif cmd == proto.CALL_SET_DEVICE_PERIOD:
                period = parsed_args[1]
                if period <= 0:
                    response.error = proto.ERROR_BAD_PARAMETERS
                    return response, False
                data.probe_do_command(self.probe, d, 'PERIOD', period)
            elif cmd == proto.CALL_ENGINE_SET_ANGLE:
                if not data.device_is_engine(d.name):
                    response.error = proto.ERROR_NOT_SUPPORTED
                    return response, False
                angle = float(parsed_args[1])
                if abs(angle) > data.MAX_ENGINE_ANGLE:
                    response.error = proto.ERROR_BAD_PARAMETERS
                    return response, False
                data.probe_do_command(self.probe, d, 'ANGLE', angle)
        elif cmd == proto.CALL_CPU_GET_FLIGHT_TIME:
            response.result.real = self.probe.time
        elif cmd == proto.CALL_CPU_DROP_STAGE:
            d = data.probe_device_by_identifier(self.probe, 'CPU1')
            if d is None:
                response.error = proto.ERROR_SYSTEM_NOT_AVAIL
                return response, False
            data.probe_do_command(self.probe, d, 'DROP STAGE', None)
        elif cmd == proto.CALL_TELEMETRY_SEND_MESSAGE:
            data.probe_send_message(self.probe, parsed_args[0])
        elif cmd == proto.CALL_NAVI_GET_ACCEL:
            response.result.real = self.probe.acceleration
        elif cmd == proto.CALL_NAVI_HAS_LANDED:
            response.result.boolean = data.probe_landed(self.probe)
        elif cmd == proto.CALL_POWER_GET_BATTERY_CAPACITY:
            response.result.real = self.probe.energy_reserve
        elif cmd == proto.CALL_POWER_GET_GENERATION:
            response.result.real = self.probe.power_generation
        elif cmd == proto.CALL_POWER_GET_CONSUMPTION:
            response.result.real = self.probe.power_generation - self.probe.power_balance
        elif cmd == proto.CALL_TRANSMITTER_GET_BANDWIDTH:
            response.result.real = self.probe.total_bandwidth / self.probe.tick_length
        elif cmd == proto.CALL_TRANSMITTER_GET_TRAFFIC:
            response.result.real = self.probe.bandwidth / self.probe.tick_length
        elif cmd == proto.CALL_HC_GET_EXT_TEMPERATURE:
            response.result.real = self.probe.T_gas
        elif cmd == proto.CALL_HC_GET_TEMPERATURE:
            response.result.real = self.probe.T
        elif cmd == proto.CALL_ENGINE_GET_FUEL:
            response.result.real = data.probe_available_fuel(self.probe,
                                                             self.probe.minimal_fuel_threshold *
                                                             self.probe.tick_length)
        return response, False
