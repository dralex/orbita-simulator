# -----------------------------------------------------------------------------
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# The Orbita Simulator
# The planet landing model
#
# interface for plotting 2-d graphs of fucuntions
#
# Copyright (C) 2013-2023 Alexey Fedoseev <aleksey@fedoseev.net>
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

import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('Agg')

global_counter = 0

def plot_graph(times, values, value_label, imagefile, ylimits, multi=False):
    global global_counter #pylint: disable=W0603
    plt.figure(global_counter)
    global_counter += 1
    if multi:
        maxlist = []
        minlist = []
        for v in values:
            maxlist.append(max(v))
            minlist.append(min(v))
    else:
        maxlist = values
        minlist = values
    if ylimits[0] == 'calc':
        ylimits[0] = min(minlist) - 1
    if ylimits[1] == 'calc':
        ylimits[1] = max(maxlist) + 1
    maxtime = (int(times[-1] / 60) + 1) * 60
    plt.axis([0, maxtime] + ylimits)
    plt.xlabel('time')
    plt.ylabel(value_label)
    plt.grid(True)
    if multi:
        for v in values:
            plt.plot(times, v)
    else:
        plt.plot(times, values)
    plt.savefig(imagefile, transparent=True)
