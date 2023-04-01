# -----------------------------------------------------------------------------
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# The Orbita Simulator
# The Earth orbit simulation model (v2)
#
# The calculation models: the probe telemetry model
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

from constants import STATE_ON, STATE_OFF, STATE_SAFE, STATE_DEAD, STATE_SLEEP
import data
from logger import debug_log
from abstractmodel import AbstractModel
from plotgraph import plot_graph, plot_parametric
from language import Language

_ = Language.get_tr()

class BasicTelemetryModel(AbstractModel):
    def __init__(self, global_parameters):
        AbstractModel.__init__(self, global_parameters)
        self.collector = {}
        self.last_sec = 0

    def init_model(self, probe, initial_tick):
        global _ # pylint: disable=W0603
        _ = Language.get_tr()

        # the initialization of programs is being done in the subsystems code
        probe.systems[data.SUBSYSTEM_TELEMETRY].last_telemetry = 0

        probe.collector['Time'] = []
        probe.collector['X'] = []
        probe.collector['Y'] = []
        probe.collector['Generation'] = []
        probe.collector['Consumption'] = []
        probe.collector['Accumulator'] = []
        probe.collector['Angle'] = []
        probe.collector['Orient.Angle'] = []
        probe.collector['Ang.Velocity'] = []
        probe.collector['Temperature'] = []
        probe.collector['Radio Queues Len'] = []
        probe.collector['Radio Max.Bandwidth'] = []
        probe.collector['Telemetry'] = []
        probe.collector['Fuel'] = []
        #probe.collector['Target Angle'] = []
        probe.collector['Cyclegram'] = []

        self.last_sec = 0

    def step(self, probe, tick):
        tel = probe.systems[data.SUBSYSTEM_TELEMETRY]
        nowtime = probe.systems[data.SUBSYSTEM_CPU].flight_time
        if tel.mode == STATE_ON and (tel.last_telemetry + tel.period) < (nowtime + 0.001):
            d, c = self.collect_data(probe)
            tel.put_data_broadcast(tel.data_volume, ('telemetry', d))
            tel.last_telemetry = nowtime
            self.add_graphs_step(probe, c)
        # else:
        #     if abs(nowtime - self.last_sec - 1) < tick:
        #         self.last_sec = nowtime
        #         self.add_empty_step(probe)

    def debug_model(self, probe):
        print(self.collect_data(probe))

    SYSTEM_CODES = {
        data.SUBSYSTEM_CPU: 'C',
        data.SUBSYSTEM_POWER: 'P',
        data.SUBSYSTEM_RADIO: 'R',
        data.SUBSYSTEM_ORIENTATION: 'O',
        data.SUBSYSTEM_NAVIGATION: 'N',
        data.SUBSYSTEM_ENGINE: 'E',
        data.SUBSYSTEM_TELEMETRY: 'T',
        data.SUBSYSTEM_HEAT_CONTROL: 'H',
        data.SUBSYSTEM_LOAD: 'L'
    }
    MODE_CODES = {
        STATE_ON: '+',
        STATE_OFF: '-',
        STATE_SLEEP: 's',
        STATE_DEAD: 'x',
        STATE_SAFE: 'S',
    }

    def collect_data(self, probe): #pylint: disable=R0912
        NaN = float('nan')
        parts = []
        collector = {}

        order = (data.SUBSYSTEM_CPU, data.SUBSYSTEM_POWER, data.SUBSYSTEM_RADIO,
                 data.SUBSYSTEM_NAVIGATION, data.SUBSYSTEM_ENGINE,
                 data.SUBSYSTEM_ORIENTATION, data.SUBSYSTEM_TELEMETRY,
                 data.SUBSYSTEM_HEAT_CONTROL, data.SUBSYSTEM_LOAD)
        for kind in order:
            if kind == data.SUBSYSTEM_CONSTRUCTION:
                continue
            system = probe.systems[kind]
            values = []
            if system is None:
                values.append(self.SYSTEM_CODES[kind])
                values.append('0')
            else:
                values.append(self.SYSTEM_CODES[kind])
                values.append(self.MODE_CODES[system.mode])
            if kind == data.SUBSYSTEM_CPU:
                if system.mode == STATE_ON:
                    values.append('t=%07d' % int(round(system.flight_time)))
                    collector['Cyclegram'] = system.cycle
                else:
                    collector['Cyclegram'] = NaN
                collector['Time'] = system.flight_time
            elif kind == data.SUBSYSTEM_POWER:
                if system.mode == STATE_ON:
                    if ((system.power_generation > system.power_consumption and
                         system.accumulator < system.max_capacity)):
                        accum_status = '+'
                    elif system.power_generation < system.power_consumption:
                        accum_status = '-'
                    else:
                        accum_status = ''
                    values.append('G=%05.1f' % system.power_generation)
                    values.append('C=%05.1f' % system.power_consumption)
                    values.append('A=%06.1f%s' % (system.accumulator, accum_status))
                    collector['Generation'] = system.power_generation
                    collector['Consumption'] = system.power_consumption
                    collector['Accumulator'] = system.accumulator
                else:
                    collector['Generation'] = NaN
                    collector['Consumption'] = NaN
                    collector['Accumulator'] = NaN
            elif kind == data.SUBSYSTEM_NAVIGATION:
                if system.mode == STATE_ON:
                    values.append('X=%010.1f' % system.x)
                    values.append('Y=%010.1f' % system.y)
                    values.append('H=%05.2f' % ((system.height - system.planet_radius) / 1000.0))
                    values.append('V=%05.2f' % system.velocity)
                    values.append('Acc=%05.3f' % system.acceleration)
                    values.append('A=%05.2f' % system.angle)
                    values.append('DS=%s' % ('+' if system.dark_side else '-'))
                    collector['X'] = system.x / 1000.0
                    collector['Y'] = system.y / 1000.0
                    collector['Angle'] = system.angle
#                    if probe.mission == data.MISSION_INSPECT:
#                        collector['Target Angle'] = system.target_angle
                else:
                    collector['X'] = NaN
                    collector['Y'] = NaN
                    collector['Angle'] = NaN
#                    if probe.mission == data.MISSION_INSPECT:
#                        collector['Target Angle'] = system.target_angle
            elif kind == data.SUBSYSTEM_ENGINE:
                if system:
                    if system.mode == STATE_ON:
                        values.append('F=%4.3f' % system.fuel)
                        collector['Fuel'] = system.fuel
                    else:
                        collector['Fuel'] = NaN
                else:
                    collector['Fuel'] = 0
            elif kind == data.SUBSYSTEM_ORIENTATION:
                if system.mode == STATE_ON:
#                    gsvisible = 0
#                    for gsv in system.ground_stations_visible.values():
#                        if gsv: gsvisible += 1
                    values.append('OA=%06.2f' % system.orient_angle)
                    values.append('w=%07.3f' % system.angular_velocity)
#                    values.append('N=%s' % ('+' if system.is_normal else '-'))
#                    values.append('GS=%d' % gsvisible)
#                    if probe.mission == data.MISSION_DZZ:
#                        values.append('N=%s' % ('+' if system.is_normal else '-'))
#                        values.append('Hi=%s' % ('+' if system.hit_target else '-'))
#                    elif probe.mission == data.MISSION_INSPECT:
#                        values.append('Hi=%d' % system.hit_target)
                    collector['Orient.Angle'] = system.orient_angle
                    collector['Ang.Velocity'] = system.angular_velocity
                else:
                    collector['Orient.Angle'] = NaN
                    collector['Ang.Velocity'] = NaN
            elif kind == data.SUBSYSTEM_HEAT_CONTROL:
                if system.mode == STATE_ON:
                    values.append('T=%05.1f' % system.temperature)
#                    values.append('H=%05.1f' % system.heat)
#                    values.append('FH=%05.1f' % system.friction_heat)
#                    values.append('S=%05.1f' % system.sun_flow)
#                    values.append('R=%05.1f' % system.radiation)
                    collector['Temperature'] = system.temperature
                else:
                    collector['Temperature'] = NaN
            elif kind == data.SUBSYSTEM_RADIO:
                if system:
                    if system.mode == STATE_ON:
                        qlen = system.queues_len()
                        b = system.max_bandwidth / 1048576.0
                        values.append('B=%07.4f' % b)
                        values.append('Q=%07.4f' % qlen)
                        collector['Radio Queues Len'] = qlen
                        if b > 0:
                            collector['Radio Max.Bandwidth'] = b
                        else:
                            collector['Radio Max.Bandwidth'] = NaN
                    else:
                        collector['Radio Queues Len'] = NaN
                        collector['Radio Max.Bandwidth'] = NaN
                else:
                    collector['Radio Queues Len'] = 0
                    collector['Radio Max.Bandwidth'] = 0
            elif kind == data.SUBSYSTEM_TELEMETRY:
                if system.mode == STATE_ON:
                    b = system.max_bandwidth / 1024.0
                    qlen = math.ceil(system.queues_len())
#                    values.append('P=%05d' % system.period)
                    values.append('B=%07.2f' % b)
                    values.append('Q=%06d' % qlen)
                    if b > 0:
                        collector['Telemetry'] = b
                    else:
                        collector['Telemetry'] = NaN
                else:
                    collector['Telemetry'] = NaN
            else:
                assert kind == data.SUBSYSTEM_LOAD
            parts.append('[' + ':'.join(values) + ']')
        result = ''.join(parts)
        debug_log(_('Telemetry: ') + result)
        #debug_log(_('Radio: ') + self.print_gs_status(probe))

        return result, collector

    @classmethod
    def add_graphs_step(cls, probe, d):
        for k, v in d.items():
            probe.collector[k].append(v)

    @classmethod
    def add_empty_step(cls, probe):
        t = probe.systems[data.SUBSYSTEM_CPU].flight_time
        for k, c in probe.collector.items():
            if k == 'Time':
                c.append(t)
            else:
                c.append(float('nan'))

    @classmethod
    def clear_extra_telemetry(cls, probe):
        if len(probe.collector['Time']) < 2:
            return
        if probe.max_telemetry_time < probe.time():
            i = 0
            for i, t in enumerate(probe.collector['Time']):
                if t >= probe.max_telemetry_time:
                    break
            for key in probe.collector.keys():
                probe.collector[key] = probe.collector[key][:i]

    @classmethod
    def get_short_results(cls, probe):

        if len(probe.collector['Time']) < 2:
            return []
        if not probe.telemetry_received:
            return []

        result = []

        result.append('Ti:X:Y:OA')
        for i, t in enumerate(probe.collector['Time']):
            result.append('%d:%f:%f:%f' % (t,
                                           probe.collector['X'][i],
                                           probe.collector['Y'][i],
                                           probe.collector['Orient.Angle'][i]))
        return result

    @classmethod
    def get_events(cls, probe): # pylint: disable=W0613
        return []

    @classmethod
    def draw_images(cls, probe, imgtmpl):

        if len(probe.collector['Time']) < 2:
            return
        if not probe.telemetry_received:
            return

        # label = ('Cyclegram')
        # imagefile = '%s%s-%s.png' % (imgtmpl, probe.filename, label)
        # plot_cycle_graph(probe.collector['Time'], probe.time(),
        #                  probe.collector['Cyclegram'],
        #                  _("Cycle"), imagefile)

        p = probe.Parameters.Planets[probe.planet]

        if probe.mission in (data.MISSION_INSPECT, data.MISSION_CRYSTAL):
            ext_radius = float(p.radius) / 1000.0 + float(probe.xml.flight.mission.target_orbit)
        elif probe.mission == data.MISSION_TELECOM:
            ext_radius = probe.systems[data.SUBSYSTEM_NAVIGATION].gs_orbit / 1000.0
        else:
            ext_radius = None

        stations = []
        orient = probe.systems[data.SUBSYSTEM_ORIENTATION]
        for name, coord in orient.ground_stations_coords.items():
            s = [name, coord[0] / 1000.0, coord[1] / 1000.0]
            stations.append(s)

        label = 'Ballistics'
        imagefile = '%s%s-%s.png' % (imgtmpl, probe.filename, label)
        plot_parametric((probe.collector['X'], probe.collector['Y']),
                        _("Probe position (km)"), imagefile,
                        float(p.radius) / 1000.0,
                        p.Atmosphere.border(float(p.atmosphere.density_border)) / 1000.0,
                        _,
                        ext_radius,
                        stations)

#        if probe.mission == data.MISSION_INSPECT:
#            graphs = (probe.collector['Angle'], probe.collector['Orient.Angle'],
#                      probe.collector['Target Angle'])
#            labels = ("Navigation", "Orientation", "Target")
#        else:
#            graphs = (probe.collector['Angle'], probe.collector['Orient.Angle'])
#            labels = ("Navigation", "Orientation")
        graphs = (probe.collector['Angle'], probe.collector['Orient.Angle'])
        labels = (_("Navigation"), _("Orientation"))

        label = 'Ballistics-Mechanics'
        imagefile = '%s%s-%s.png' % (imgtmpl, probe.filename, label)
        plot_graph(probe.collector['Time'], probe.time(),
                   graphs, labels,
                   _("Angle (degree)"), imagefile, [0, 360], _, True)

        label = 'Angular-Velocity'
        imagefile = '%s%s-%s.png' % (imgtmpl, probe.filename, label)
        plot_graph(probe.collector['Time'], probe.time(),
                   probe.collector['Ang.Velocity'], None,
                   _("Angular Velocity (degree/s)"), imagefile, ['calc', 'calc'], _)

        if probe.systems[data.SUBSYSTEM_ENGINE]:
            label = 'Fuel'
            imagefile = '%s%s-%s.png' % (imgtmpl, probe.filename, label)
            plot_graph(probe.collector['Time'], probe.time(),
                       probe.collector['Fuel'], None,
                       _("Fuel Left (kg)"), imagefile, ['calc', 'calc'], _)

        label = 'Power'
        imagefile = '%s%s-%s.png' % (imgtmpl, probe.filename, label)
        plot_graph(probe.collector['Time'], probe.time(),
                   (probe.collector['Generation'], probe.collector['Consumption']),
                   (_("Generation"), _("Consumption")),
                   _("Power (W)"), imagefile, ['calc', 'calc'], _, True)

        label = 'Power-Accumulator'
        imagefile = '%s%s-%s.png' % (imgtmpl, probe.filename, label)
        plot_graph(probe.collector['Time'], probe.time(),
                   probe.collector['Accumulator'], None,
                   _("Accumulator Capacity (J)"), imagefile, [0, 'calc'], _)

        label = 'Temperature'
        imagefile = '%s%s-%s.png' % (imgtmpl, probe.filename, label)
        plot_graph(probe.collector['Time'], probe.time(),
                   probe.collector['Temperature'], None,
                   _("Temperature (K)"), imagefile, ['calc', 'calc'], _)

        if probe.systems[data.SUBSYSTEM_RADIO]:
            label = 'Radio-Queue'
            imagefile = '%s%s-%s.png' % (imgtmpl, probe.filename, label)
            plot_graph(probe.collector['Time'], probe.time(),
                       probe.collector['Radio Queues Len'], None,
                       _("Radio Queues Len (MB)"), imagefile, [0, 'calc'], _)

            label = 'Radio-Transmitting-Bandwidth'
            imagefile = '%s%s-%s.png' % (imgtmpl, probe.filename, label)
            plot_graph(probe.collector['Time'], probe.time(),
                       (probe.collector['Telemetry'],
                        probe.collector['Radio Max.Bandwidth']),
                       (_("Telemetry"), _("Radio")),
                       _("Bandwidth (MB/s)"), imagefile, [0, 'calc'], _, True)
        else:
            label = 'Telemetry'
            imagefile = '%s%s-%s.png' % (imgtmpl, probe.filename, label)
            plot_graph(probe.collector['Time'], probe.time(),
                       probe.collector['Telemetry'],
                       _("Telemetry"),
                       _("Bandwidth (KB/s)"), imagefile, [0, 'calc'], _)

    def print_gs_status(self, probe):
        result = ''
        if probe.systems[data.SUBSYSTEM_RADIO]:
            result += self.__print_gs_status(probe, probe.systems[data.SUBSYSTEM_RADIO])
        result += self.__print_gs_status(probe, probe.systems[data.SUBSYSTEM_TELEMETRY])
        return result

    @classmethod
    def __print_gs_status(cls, probe, radio):
        orient = probe.systems[data.SUBSYSTEM_ORIENTATION]
        navig = probe.systems[data.SUBSYSTEM_NAVIGATION]
        if radio == probe.systems[data.SUBSYSTEM_TELEMETRY]:
            arc_const = data.SUBSYSTEM_TELEMETRY
            result = '[T'
        else:
            arc_const = data.SUBSYSTEM_RADIO
            result = '[R'
        if radio.transmitting:
            result += '+'
            for gs, gsvector in orient.ground_stations_coords.items():
                vis = orient.ground_stations_visible[gs]
                if vis:
                    result += 'v'
                arc = orient.ground_stations_arc[gs][arc_const]
                if arc:
                    result += 'a'
                if vis and arc:
                    distance2 = data.calculate_distance2(navig, data.Vector(gsvector))
                    result += 'd{:.1f}:'.format(math.sqrt(distance2) / 1000.0)
                    bandwidth = (radio.base_calculation / distance2) / 8.0
                    result += 'bw{:.1f}'.format(bandwidth)
        else:
            result += '-'
        return result + ']'
