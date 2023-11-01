# -----------------------------------------------------------------------------
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# The Orbita Simulator
# The Earth orbit simulation model (v2)
#
# The simulator logger interface
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

import sys
import os
from collections import deque
from language import Language

_ = Language.get_tr()

logging = {
    'mission': None,
    'debug': None,
    'short': None,
    'image': None,
    'html': None,
    'test': None
}

mission_log_buffer = deque()
simulation_time = 0.0

the_only_probe = False

def time_to_str(tim):
    t = int(tim) # round to sec
    hours = t / 3600
    minutes = (t % 3600) / 60
    seconds = (t % 3600) % 60
    return '%02d:%02d:%02d' % (hours, minutes, seconds)

def set_logging(target, do_logging, probes):
    global the_only_probe
    if target in logging:
        logging[target] = do_logging
        if do_logging and target != 'image':
            if len(probes) > 1:
                for probe in probes:
                    f = open(f'{probe.name}_{do_logging}', 'w')
                    f.truncate()
                    f.close()
            else:
                the_only_probe = True
                f = open(do_logging, 'w')
                f.truncate()
                f.close()
            if target == 'mission':
                mission_log_buffer.clear()
    else:
        error_log(_('Bad logging target "%s"\n'), target)
        sys.exit(1)

def sync_logs(probes):
    if not the_only_probe:
        for probe in probes:
            if logging['debug']:
                f = open(f"{probe.name}_{logging['debug']}", 'a')
                f.flush()
                os.fsync(f.fileno())
                f.close()
            if logging['mission']:
                f = open(f"{probe.name}_{logging['mission']}", 'a')
                f.flush()
                os.fsync(f.fileno())
                f.close()
            if logging['test']:
                f = open(f"{probe.name}_{logging['test']}", 'a')
                f.flush()
                os.fsync(f.fileno())
                f.close()
    else:
        if logging['debug']:
            f = open(logging['debug'], 'a')
            f.flush()
            os.fsync(f.fileno())
            f.close()
        if logging['mission']:
            f = open(logging['mission'], 'a')
            f.flush()
            os.fsync(f.fileno())
            f.close()
        if logging['test']:
            f = open(logging['test'], 'a')
            f.flush()
            os.fsync(f.fileno())
            f.close()    

def debug_log(probe, s, *args):
    if logging['debug']:
        if the_only_probe:
            f = open(logging['debug'], 'a')
        else:
            f = open(f"{probe.name}_{logging['debug']}", 'a')
        f.write('DEBUG [%s]: %s\n' % (time_to_str(simulation_time),
                                      s % args))
        f.close()

def error_log(probe, s, *args):
    debug_log(probe, s, *args)
    mission_log(probe, s, *args)
    sys.stderr.write('ERROR: ' + (s % args) + '\n')

def test_log(probe, s, *args):
    outs = (s % args) + '\n'
    if logging['test']:
        if the_only_probe:
            f = open(logging['test'], 'a')
        else:
            f = open(f"{probe.name}_{logging['test']}", 'a')
        f.write(outs)
        f.close()

def mission_log(probe, s, *args):
    if simulation_time > 0:
        outs = ('%s: ' % time_to_str(simulation_time)) + (s % args) + '\n'
    else:
        outs = (s % args) + '\n'
    mission_log_buffer.append(outs)
    if logging['mission']:
        if the_only_probe:
            f = open(logging['mission'], 'a')
        else:
            f = open(f"{probe.name}_{logging['mission']}", 'a')
        f.write(outs)
        f.close()

def stdout_log(s, *args):
    sys.stdout.write((s % args) + '\n')

def get_mission_logs():
    return ''.join(mission_log_buffer)

def short_log(probe, s, *args):
    if logging['short']:
        if the_only_probe:
            f = open(logging['short'], 'a')
        else:
            f = open(f"{probe.name}_{logging['short']}", 'a')
        f.write((s % args) + '\n')
        f.close()

def short_log_xml(parameters):
    if logging['short']:
        f = open(logging['short'], 'a')
        f.write('<?xml version="1.0" encoding="utf-8"?>\n')
        f.write('<result name="%s">\n' % parameters['name'])
        f.write('<name>%s</name>\n' % parameters['name'])
        for p in parameters:
            if p == 'name':
                continue
            if p == 'data':
                for d in parameters[p]:
                    f.write('<data stage="%s">\n%s</data>\n' % (d[0], d[1]))
            elif p == 'image':
                for img in parameters[p]:
                    f.write('<image stage="%s" params="%s">%s</image>\n' % img)
            else:
                f.write('<%s>%s</%s>\n' % (p, parameters[p], p))
        f.write('</result>\n')
        f.close()

def get_image_template():
    return logging['image']
