# -----------------------------------------------------------------------------
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# The Orbita Simulator
# The Earth orbit simulation model (v2)
#
# Satellite API runtime
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

from google.protobuf.message import DecodeError
import constants as const
import api.systems_pb2 as proto

# -----------------------------------------------------------------------------
# High-level runtime class
# -----------------------------------------------------------------------------

class SputnikRuntime:
    def __init__(self, probe):
        self._probe = probe
        self.systems_map = {
            proto.SYSTEM_CPU: const.SUBSYSTEM_CPU,
            proto.SYSTEM_NAVIGATION: const.SUBSYSTEM_NAVIGATION,
            proto.SYSTEM_ORIENTATION: const.SUBSYSTEM_ORIENTATION,
            proto.SYSTEM_ENGINE: const.SUBSYSTEM_ENGINE,
            proto.SYSTEM_POWER: const.SUBSYSTEM_POWER,
            proto.SYSTEM_TELEMETRY: const.SUBSYSTEM_TELEMETRY,
            proto.SYSTEM_HEATCONTROL: const.SUBSYSTEM_HEAT_CONTROL,
            proto.SYSTEM_TRANSMITTER: const.SUBSYSTEM_RADIO
        }
        self.possible_axes = (proto.AXIS_X, proto.AXIS_Y, proto.AXIS_Z)
        self.state_map = {
            const.STATE_ON: proto.STATE_ON,
            const.STATE_OFF: proto.STATE_OFF,
            const.STATE_SLEEP: proto.STATE_SLEEP,
            const.STATE_DEAD: proto.STATE_DEAD,
            const.STATE_SAFE: proto.STATE_SAFE,
            const.STATE_WAKEUP: proto.STATE_WAKEUP
        }
        self.state_back_map = {
            proto.STATE_ON: const.STATE_ON,
            proto.STATE_OFF: const.STATE_OFF,
            proto.STATE_WAKEUP: const.STATE_WAKEUP
        }
        self.msg_type_map = {
            const.MESSAGE_TYPE_SMS: proto.MESSAGE_SMS,
            const.MESSAGE_TYPE_PHOTO: proto.MESSAGE_PHOTO,
            const.MESSAGE_TYPE_TELEMETRY: proto.MESSAGE_TELEMETRY
        }
        self.msg_type_back_map = {
            proto.MESSAGE_SMS: const.MESSAGE_TYPE_SMS,
            proto.MESSAGE_PHOTO: const.MESSAGE_TYPE_PHOTO,
            proto.MESSAGE_TELEMETRY: const.MESSAGE_TYPE_TELEMETRY
        }
        self.command_args = {
            proto.CALL_GET_STATE: [],
            proto.CALL_SET_STATE: ['integer'],
            proto.CALL_SLEEP: ['real'],
            proto.CALL_DISPATCH: ['text'],
            proto.CALL_HAS_EVENT: [],
            proto.CALL_CPU_RUN: [],
            proto.CALL_CPU_GET_FLIGHT_TIME: [],
            proto.CALL_CPU_SUCCESS: [],
            proto.CALL_CPU_TERMINATE: [],
            proto.CALL_TELEMETRY_SET_PERIOD: ['integer'],
            proto.CALL_TELEMETRY_SEND_MESSAGE: ['text'],
            proto.CALL_TELEMETRY_DEBUG: ['text'],
            proto.CALL_TRANSMITTER_SEND_DATA: ['message'],
            proto.CALL_TRANSMITTER_SEND_PHOTO: ['integer'],
            proto.CALL_TRANSMITTER_SEND_PHOTO_TO: ['integer', 'integer'],
            proto.CALL_TRANSMITTER_RECEIVE: ['integer'],
            proto.CALL_TRANSMITTER_GET_PROGRESS: ['integer'],
            proto.CALL_TRANSMITTER_GET_MESSAGE: ['integer'],
            proto.CALL_POWER_GET_BATTERY_CAPACITY: [],
            proto.CALL_POWER_GET_GENERATION: [],
            proto.CALL_POWER_GET_CONSUMPTION: [],
            proto.CALL_NAVI_GET_ORBIT_HEIGHT: [],
            proto.CALL_NAVI_GET_Z_AXIS_ANGLE: [],
            proto.CALL_NAVI_GET_X_COORD: [],
            proto.CALL_NAVI_GET_Y_COORD: [],
            proto.CALL_NAVI_GET_TRANSVERSAL_VELOCITY: [],
            proto.CALL_NAVI_GET_RADIAL_VELOCITY: [],
            proto.CALL_ORIENT_GET_ANGLE: ['integer'],
            proto.CALL_ORIENT_GET_ANGULAR_VELOCITY: ['integer'],
            proto.CALL_ORIENT_START_MOTOR: ['integer'],
            proto.CALL_ORIENT_STOP_MOTOR: ['integer'],
            proto.CALL_ORIENT_SET_MOTOR_MOMENT: ['integer', 'real'],
            proto.CALL_ORIENT_START_COIL: ['integer'],
            proto.CALL_ORIENT_STOP_COIL: ['integer'],
            proto.CALL_ENGINE_GET_FUEL: [],
            proto.CALL_ENGINE_START_ENGINE: [],
            proto.CALL_ENGINE_STOP_ENGINE: [],
            proto.CALL_ENGINE_SET_TRACTION: ['real'],
            proto.CALL_HC_GET_TEMPERATURE: [],
            proto.CALL_HC_START_HEATING: [],
            proto.CALL_HC_STOP_HEATING: [],
            proto.CALL_HC_SET_POWER: ['real'],
            proto.CALL_CAMERA_TAKE_PHOTO: [],
            proto.CALL_CAMERA_START_SHOOTING: [],
            proto.CALL_CAMERA_STOP_SHOOTING: [],
            proto.CALL_CAMERA_GET_IMAGE_SIZE: ['integer'],
            proto.CALL_CONTAINER_START_EXPERIMENT: [],
            proto.CALL_CONTAINER_STOP_EXPERIMENT: [],
            proto.CALL_CONTAINER_SET_PARA_HEIGHT: ['real'],
            proto.CALL_CONTAINER_DROP: [],
        }

    @classmethod
    def deserialize_request(cls, data):
        try:
            request = proto.Request()
            request.ParseFromString(data)
        except DecodeError:
            request = None
        return request

    @classmethod
    def serialize_response(cls, response):
        return response.SerializeToString()

    def process_call(self, data): # pylint: disable=R0912
        request = self.deserialize_request(data)
        response, next_step = self.__process_command(request)
        return self.serialize_response(response), next_step

    def __process_command(self, request): # pylint: disable=R0911
        response = proto.Response()

        if request is None:
            response.error = proto.ERROR_UNKNOWN
            return response, False

        system = request.system
        cmd = request.command
        args = request.arguments

        obj = None

        if system == proto.SYSTEM_CPU and cmd == proto.CALL_CPU_RUN:
            response.result.boolean = True
            return response, True

        if system in self.systems_map:
            obj = self._probe.systems[self.systems_map[system]]
        elif system == proto.SYSTEM_CAMERA:
            if self._probe.mission not in [const.MISSION_INSPECT,
                                           const.MISSION_DZZ,
                                           const.MISSION_EARLY_WARNING]:
                obj = None
            else:
                obj = self._probe.systems[const.SUBSYSTEM_LOAD]
        elif system == proto.SYSTEM_CONTAINER:
            if self._probe.mission != const.MISSION_CRYSTAL:
                obj = None
            else:
                obj = self._probe.systems[const.SUBSYSTEM_LOAD]
        if not obj:
            response.error = proto.ERROR_SYSTEM_NOT_AVAIL
            return response, False

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

        if cmd == proto.CALL_GET_STATE:
            response.result.integer = self.state_map[obj.mode]
        elif cmd == proto.CALL_SET_STATE:
            pstate = parsed_args[0]
            if pstate not in self.state_back_map:
                response.error = proto.ERROR_BAD_PARAMETERS
                return response, False
            if pstate == proto.STATE_WAKEUP and system != proto.SYSTEM_CPU:
                response.error = proto.ERROR_BAD_PARAMETERS
                return response, False
            state = self.state_back_map[pstate]
            obj.set_mode(state)
        elif cmd == proto.CALL_SLEEP:
            timeout = parsed_args[0]
            if timeout <= 0:
                response.error = proto.ERROR_BAD_PARAMETERS
                return response, False
            obj.sleep(timeout)
        elif cmd == proto.CALL_DISPATCH:
            obj.dispatch_event(parsed_args[0])
        elif cmd == proto.CALL_HAS_EVENT:
            ev = obj.get_event()
            if ev is not None:
                response.result.text = ev
            else:
                response.result.text = ''                
        elif system == proto.SYSTEM_CPU:
            if cmd == proto.CALL_CPU_GET_FLIGHT_TIME:
                response.result.real = obj.flight_time
            elif cmd == proto.CALL_CPU_SUCCESS:
                response.result.boolean = self._probe.success
            elif cmd == proto.CALL_CPU_TERMINATE:
                obj.turn_off()
        elif system == proto.SYSTEM_TELEMETRY:
            if cmd == proto.CALL_TELEMETRY_SEND_MESSAGE:
                obj.send_log_message(parsed_args[0])
            elif cmd == proto.CALL_TELEMETRY_SET_PERIOD:
                obj.set_period(parsed_args[0])
            elif cmd == proto.CALL_TELEMETRY_DEBUG:
                obj.debug(parsed_args[0])
        elif system == proto.SYSTEM_TRANSMITTER:
            if cmd == proto.CALL_TRANSMITTER_RECEIVE:
                obj.receive(parsed_args[0])
            elif cmd == proto.CALL_TRANSMITTER_GET_PROGRESS:
                response.result.real = obj.get_progress(parsed_args[0])
            elif cmd == proto.CALL_TRANSMITTER_GET_MESSAGE:
                message = obj.get_message(parsed_args[0])
                if message is not None:
                    msg_id, msg_type, data, receiver, sender, send_time, timeout = message
                    msg = proto.Message()
                    msg.receiver = int(receiver)
                    msg.sender = int(sender)
                    msg.type = self.msg_type_map[msg_type]
                    msg.id = msg_id
                    msg.data = data
                    msg.send_time = send_time
                    if timeout is not None:
                        msg.timeout = timeout
                    response.result.message.CopyFrom(msg)
            elif cmd == proto.CALL_TRANSMITTER_SEND_PHOTO:
                obj.send_photo(parsed_args[0])
            elif cmd == proto.CALL_TRANSMITTER_SEND_PHOTO_TO:
                obj.send_photo(parsed_args[0], parsed_args[1])
            elif cmd == proto.CALL_TRANSMITTER_SEND_DATA:
                msg = parsed_args[0]
                if msg.type not in self.msg_type_back_map:
                    response.error = proto.ERROR_BAD_PARAMETERS
                    return response, False
                obj.send_message(self.msg_type_back_map[msg.type],
                                 msg.data,
                                 msg.receiver,
                                 msg.sender,
                                 msg.timeout)
        elif system == proto.SYSTEM_POWER:
            if cmd == proto.CALL_POWER_GET_BATTERY_CAPACITY:
                response.result.real = obj.accumulator
            elif cmd == proto.CALL_POWER_GET_CONSUMPTION:
                response.result.real = obj.power_consumption
            elif cmd == proto.CALL_POWER_GET_GENERATION:
                response.result.real = obj.power_generation
        elif system == proto.SYSTEM_NAVIGATION:
            if cmd == proto.CALL_NAVI_GET_ORBIT_HEIGHT:
                response.result.real = obj.orbit_height
            elif cmd == proto.CALL_NAVI_GET_Z_AXIS_ANGLE:
                response.result.real = obj.angle
            elif cmd == proto.CALL_NAVI_GET_X_COORD:
                response.result.real = obj.x
            elif cmd == proto.CALL_NAVI_GET_Y_COORD:
                response.result.real = obj.y
            elif cmd == proto.CALL_NAVI_GET_TRANSVERSAL_VELOCITY:
                response.result.real = obj.v_transversal
            elif cmd == proto.CALL_NAVI_GET_RADIAL_VELOCITY:
                response.result.real = obj.v_radial
        elif system == proto.SYSTEM_ORIENTATION:
            axis = parsed_args[0]
            if cmd == proto.CALL_ORIENT_GET_ANGLE:
                if axis == proto.AXIS_Z:
                    response.result.real = obj.orient_angle
            elif cmd == proto.CALL_ORIENT_GET_ANGULAR_VELOCITY:
                if axis == proto.AXIS_Z:
                    response.result.real = obj.angular_velocity
            elif cmd == proto.CALL_ORIENT_START_MOTOR:
                if axis != proto.AXIS_Z:
                    response.error = proto.ERROR_NOT_SUPPORTED
                    return response, False
                obj.start_motor()
            elif cmd == proto.CALL_ORIENT_STOP_MOTOR:
                if axis != proto.AXIS_Z:
                    response.error = proto.ERROR_NOT_SUPPORTED
                    return response, False
                obj.stop_motor()
            elif cmd == proto.CALL_ORIENT_SET_MOTOR_MOMENT:
                if axis != proto.AXIS_Z:
                    response.error = proto.ERROR_NOT_SUPPORTED
                    return response, False
                obj.set_torsion(parsed_args[1])
            elif cmd == proto.CALL_ORIENT_START_COIL:
                response.error = proto.ERROR_NOT_SUPPORTED
                return response, False
            elif cmd == proto.CALL_ORIENT_STOP_COIL:
                response.error = proto.ERROR_NOT_SUPPORTED
                return response, False
        elif system == proto.SYSTEM_ENGINE:
            if cmd == proto.CALL_ENGINE_GET_FUEL:
                response.result.real = obj.fuel
            elif cmd == proto.CALL_ENGINE_START_ENGINE:
                obj.start_engine()
            elif cmd == proto.CALL_ENGINE_STOP_ENGINE:
                obj.stop_engine()
            elif cmd == proto.CALL_ENGINE_SET_TRACTION:
                obj.set_traction(parsed_args[0])
        elif system == proto.SYSTEM_HEATCONTROL:
            if cmd == proto.CALL_HC_GET_TEMPERATURE:
                response.result.real = obj.temperature
            elif cmd == proto.CALL_HC_START_HEATING:
                obj.start_heating()
            elif cmd == proto.CALL_HC_STOP_HEATING:
                obj.stop_heating()
            elif cmd == proto.CALL_HC_SET_POWER:
                obj.set_power(parsed_args[0])
        elif system == proto.SYSTEM_CAMERA:
            if cmd == proto.CALL_CAMERA_TAKE_PHOTO:
                res = obj.take_photo()
                if res is not None:
                    response.result.integer = res
            elif cmd == proto.CALL_CAMERA_START_SHOOTING:
                obj.start_shooting()
            elif cmd == proto.CALL_CAMERA_STOP_SHOOTING:
                res = obj.stop_shooting()
                if res is not None:
                    response.result.integer = res
            elif cmd == proto.CALL_CAMERA_GET_IMAGE_SIZE:
                res = obj.get_image_size(parsed_args[0])
                if res is None:
                    response.error = proto.ERROR_BAD_PARAMETERS
                    return response, False
                response.result.integer = res
        elif system == proto.SYSTEM_CONTAINER:
            if cmd == proto.CALL_CONTAINER_START_EXPERIMENT:
                obj.start_experiment()
            elif cmd == proto.CALL_CONTAINER_STOP_EXPERIMENT:
                obj.stop_experiment()
            elif cmd == proto.CALL_CONTAINER_SET_PARA_HEIGHT:
                h = parsed_args[0]
                if h < 0:
                    response.error = proto.ERROR_BAD_PARAMETERS
                    return response, False
                obj.set_para_height(h)
            elif cmd == proto.CALL_CONTAINER_DROP:
                obj.drop()
        else:
            response.error = proto.ERROR_SYSTEM_NOT_AVAIL
            return response, False

        return response, False
