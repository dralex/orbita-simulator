# -----------------------------------------------------------------------------
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# The Orbita Simulator
# The Earth orbit simulation model (v2)
#
# The interface for plotting 2-d graphs of fucuntions
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

import numpy
from numpy import nanmin, nanmax, isnan
import matplotlib
import matplotlib.pyplot as plt
from logger import debug_log

matplotlib.use('Agg')
matplotlib.rcParams['agg.path.chunksize'] = 20000

global_counter = 0

def plot_cycle_graph(times, maxtime, values, y_label, imagefile, tr):

    max_cycle = nanmax(values)

    if str(max_cycle) == 'nan' or max_cycle == 0:
        plot_graph(times, maxtime, values, None, y_label, imagefile, [-0.1, 0.1], tr)
    else:
        max_cycle = int(max_cycle)
        N = max_cycle + 1
        M = len(times)
        cycles = [None] * N
        for j in range(N):
            cycles[j] = [0] * M
            for i in range(M):
                if j == values[i]:
                    cycles[j][i] = values[i]
                else:
                    cycles[j][i] = float('nan')
        plot_graph(times, maxtime, cycles, None, y_label, imagefile, [-0.1, max_cycle + 0.1], True)

def plot_graph(probe, times, maxtime, values, labels, y_label, imagefile, ylimits, tr, multi=False):
    global global_counter #pylint: disable=W0603
    plt.figure(global_counter, figsize=(8.0, 8.0))
    global_counter += 1
    _ = tr
    if multi:
        maxlist = []
        minlist = []
        for v in values:
            maxlist.append(nanmax(v))
            minlist.append(nanmin(v))
    else:
        maxlist = values
        minlist = values
    if isnan(minlist).all() or isnan(maxlist).all():
        debug_log(probe, 'Disable graph {}: all nan min/max array'.format(imagefile))
        return
    if ylimits[0] == 'calc':
        ylimits[0] = nanmin(minlist) * 0.99
    if ylimits[1] == 'calc':
        ylimits[1] = nanmax(maxlist) * 1.01
    plt.axis([0, maxtime] + ylimits)
    plt.xlabel(_('time'))
    plt.ylabel(y_label)
    plt.grid(True)
    style = 'o-' if len(times) <= 25 else '-'
    if multi:
        for i, v in enumerate(values):
            if labels is not None:
                plt.plot(times, v, style, label=labels[i])
            else:
                plt.plot(times, v, style)

    else:
        if labels is not None:
            plt.plot(times, values, style, label=labels)
        else:
            plt.plot(times, values, style)
    if labels is not None:
        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
                   ncol=2, mode="expand", borderaxespad=0.0)
    plt.savefig(imagefile, transparent=True)
    plt.close()

def plot_parametric(values, x_label, imagefile, r1, r2, tr, r3=None, stations=None):

    _ = tr

    global global_counter #pylint: disable=W0603
    plt.figure(global_counter, figsize=(8.0, 8.0))
    global_counter += 1

    limit = max(abs(nanmin(values)), abs(nanmax(values))) * 1.1
    if r3 is not None and r3 > limit:
        limit = r3 * 1.1

    plt.axis([-limit, limit, -limit, limit])
    plt.xlabel(x_label)
    ax = plt.subplots(figsize=(8.0, 8.0))[1]
    ax.grid(True)
    ax.set_aspect('equal')

    t = numpy.arange(0, 2 * numpy.pi, 0.01)
    x = r1 * numpy.cos(t)
    y = r1 * numpy.sin(t)
    ax.plot(x, y, 'black', label=_("Surface"))

    t = numpy.arange(0, 2 * numpy.pi, 0.01)
    x = r2 * numpy.cos(t)
    y = r2 * numpy.sin(t)
    ax.plot(x, y, '--', color='lightskyblue', label=_("Atmosphere"))

    if r3:
        t = numpy.arange(0, 2 * numpy.pi, 0.01)
        x = r3 * numpy.cos(t)
        y = r3 * numpy.sin(t)
        ax.plot(x, y, '--', color='red', linewidth=3,
                label=_("Trajectory of the target"))

    if stations:
        xs = []
        ys = []
        for s in stations:
            x, y = s[1:]
            xs.append(x)
            ys.append(y)
        ax.scatter(xs, ys, marker='o', color='green', label=_("GS"))

    style = 'o-' if len(values[0]) <= 25 else '-'
    ax.plot(values[0], values[1], style, label=_("Trajectory"))

    plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
               ncol=2, mode="expand", borderaxespad=0.0)
    plt.savefig(imagefile, transparent=True)
    plt.close()
