# -----------------------------------------------------------------------------
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# The Orbita Simulator
# The Earth orbit simulation model (v2)
#
# The calculation models: the simple radio connectivity model
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

import math
from collections import deque

import data
import constants
from abstractmodel import AbstractModel
from logger import debug_log, mission_log
from language import Language

_ = Language.get_tr()

class SimpleRadioModel(AbstractModel):
    def __init__(self, global_parameters):
        AbstractModel.__init__(self, global_parameters)

    def init_model(self, probe, initial_tick):
        global _ # pylint: disable=W0603
        _ = Language.get_tr()
        if probe.systems[constants.SUBSYSTEM_RADIO]:
            self.__init_model_device(probe, probe.systems[constants.SUBSYSTEM_RADIO])
        self.__init_model_device(probe, probe.systems[constants.SUBSYSTEM_TELEMETRY])

    def __init_model_device(self, probe, radio):
        orient = probe.systems[constants.SUBSYSTEM_ORIENTATION]

        planet = self.params.Planets[probe.planet]

        phase_manipulations = 4
        noise_temperature = 1000
        if hasattr(radio.device, 'circuit_loss') and radio.device.circuit_loss is not None:
            circuit_loss = float(radio.device.circuit_loss)
        else:
            circuit_loss = 1
        wave_length = 3.0 * 1e8 / (float(radio.device.freq) * 1e6)
        radio.base_calculation = ((float(radio.device.ground_amplification) *
                                   float(radio.device.amplification) *
                                   float(planet.ground.control_stations.targeting_loss) *
                                   1.0 *
                                   float(radio.device.radio_power) *
                                   math.log(phase_manipulations)) /
                                  (100.0 *
                                   (4 * math.pi / wave_length) ** 2 *
                                   float(planet.ground.control_stations.environment_loss) *
                                   float(planet.ground.control_stations.circuit_loss) *
                                   circuit_loss *
                                   1.2 *
                                   1.38 * 1e-23 *
                                   noise_temperature *
                                   math.log(2)))

        debug_log(_('The basic radio model for %s is: %f (%f MHz; %f W)'),
                  radio.device.name,
                  radio.base_calculation,
                  radio.device.freq,
                  radio.device.radio_power)

        radio.max_bandwidth = 0.0

        radio.send_queues = {}
        radio.receive_queues = {}
        radio.broadcast_queue = deque()
        radio.queues_size = 0
        radio.sent_packets = {}
        radio.received_packets = {}

        for gs in orient.ground_stations:
            radio.send_queues[gs] = deque()
            radio.receive_queues[gs] = deque()
            radio.received_packets[gs] = {}

    def step(self, probe, tick, probes):
        if probe.systems[constants.SUBSYSTEM_RADIO]:
            self.__step_device(probe, probe.systems[constants.SUBSYSTEM_RADIO], tick)
        self.__step_device(probe, probe.systems[constants.SUBSYSTEM_TELEMETRY], tick)

    def __step_device(self, probe, radio, tick): # pylint: disable=R0912,R0914,R0201
        orient = probe.systems[constants.SUBSYSTEM_ORIENTATION]
        navig = probe.systems[constants.SUBSYSTEM_NAVIGATION]
        is_telemetry = radio == probe.systems[constants.SUBSYSTEM_TELEMETRY]

        if not radio.transmitting:
            return

        radio.received_packets.clear()
        radio.sent_packets.clear()

        radio.max_bandwidth = 0.0

        for gs, gsvector in orient.ground_stations_coords.items():
            if orient.ground_stations_visible[gs] and orient.ground_stations_arc[gs][constants.SUBSYSTEM_TELEMETRY if is_telemetry else constants.SUBSYSTEM_RADIO]: # pylint: disable=C0301
                distance2 = data.calculate_distance2(navig, data.Vector(gsvector))
                bandwidth = (radio.base_calculation / distance2) / 8.0
                if bandwidth > radio.max_bandwidth:
                    radio.max_bandwidth = bandwidth

                channel = bandwidth * tick

                received = 0
                received_data = 0
                senttoprobe = 0
                senttoprobe_data = 0

                radio.received_packets[gs] = {}
                radio.sent_packets[gs] = {}

                while channel > 0 and (len(radio.receive_queues[gs]) > 0 or
                                       len(radio.send_queues[gs]) > 0 or
                                       len(radio.broadcast_queue) > 0):
                    if len(radio.receive_queues[gs]) > 0:
                        # trying to receive data first
                        message_id, message_time, volume, received, realdata = radio.receive_queues[gs][0] # pylint: disable=C0301
                        received += channel
                        if received >= volume:
                            channel = received - volume
                            received = volume
                            now = probe.time()
                            radio.received_packets[gs][message_id] = (message_time,
                                                                      now,
                                                                      volume,
                                                                      realdata)
                            if realdata is not None:
                                senttoprobe += 1
                                senttoprobe_data += volume
                                msg = (_('The probe received (channel %s) from %s the data type %s, size %d bytes') % # pylint: disable=C0301
                                       (radio.radio_type, gs, realdata[0], volume))
                                debug_log(msg)
                                #mission_log(msg)

                                if gs in radio.receiving_requests:
                                    debug_log(_('The message received'))
                                    radio.receiving_progress[gs] = 100.0
                                    radio.received_messages[gs] = (message_id,
                                                                   realdata[0],
                                                                   realdata[2],
                                                                   realdata[1],
                                                                   gs, now, realdata[3])
                                    del radio.receiving_requests[gs]
                            else:
                                debug_log(_('Error: the unexpected message received'))
                            radio.receive_queues_pop(gs)
                        else:
                            radio.receive_queues[gs][0][3] = received
                            channel = 0
                            if gs in radio.receiving_requests:
                                radio.receiving_progress[gs] = received / volume

                    elif len(radio.send_queues[gs]) > 0:
                        message_id, message_time, volume, sent, realdata = radio.send_queues[gs][0]
                        sent += channel
                        if sent >= volume:
                            channel = sent - volume
                            sent = volume
                            now = probe.time()
                            radio.sent_packets[gs][message_id] = (message_time,
                                                                  now,
                                                                  volume,
                                                                  realdata)
                            if realdata is not None:
                                received += 1
                                received_data += volume
                                msg = (_('The ground station %s received (channel %s) the data %d type %s, size %d bytes') % # pylint: disable=C0301
                                       (gs, radio.radio_type, message_id, realdata[0], volume))
                                debug_log(msg)
                                #if realdata[0] in data.available_missions or realdata[1] is None:
                                #    mission_log(msg)
                                #else:
                                #    mission_log(msg + ': %s' % realdata[1])
                            radio.send_queues_pop(gs)
                            radio.message_sent = True
                        else:
                            radio.send_queues[gs][0][3] = sent
                            channel = 0

                    elif len(radio.broadcast_queue) > 0:
                        message_id, message_time, volume, sent, realdata = radio.broadcast_queue[0]
                        sent += channel
                        if sent >= volume:
                            channel = sent - volume
                            sent = volume
                            now = probe.time()
                            radio.sent_packets[gs][message_id] = (message_time,
                                                                  now,
                                                                  volume,
                                                                  realdata)
                            if realdata is not None:
                                received += 1
                                received_data += volume
                                msg = ('The ground station %s received (channel %s) the data %d type %s, size %d bytes' % # pylint: disable=C0301
                                       (gs, radio.radio_type, message_id, realdata[0], volume))
                                if realdata[0] != 'telemetry':
                                    debug_log(msg)
                                    #if ((realdata[0] in data.available_missions or
                                    #     realdata[1] is None):
                                    #    mission_log(msg)
                                    #else:
                                    #    mission_log(msg + ': %s' % realdata[1])
                                else:
                                    if probe.telemetry_received < message_id:
                                        mission_log(str(realdata[1]))
                                        probe.telemetry_received = message_id
                                        probe.max_telemetry_time = message_time
                            radio.broadcast_queue_pop()
                            radio.message_sent = True
                        else:
                            radio.broadcast_queue[0][3] = sent
                            channel = 0

                if senttoprobe > 0:
                    debug_log(_('%d data packets sent to Earth by channel %s: total value %.1f bytes') % # pylint: disable=C0301
                              (senttoprobe, radio.radio_type, senttoprobe_data))
                if received_data > 0:
                    debug_log(_('%d data packets received to Earth by channel %s: total value  %.1f bytes') % # pylint: disable=C0301
                              (received, radio.radio_type, received_data))
