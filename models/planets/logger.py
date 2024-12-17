# -----------------------------------------------------------------------------
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# The Orbita Simulator
# The planet landing model
#
# Logger interface
#
# Copyright (C) 2013      Nikolay Safronov <bfishh@gmail.com>
# Copyright (C) 2013-2023 Alexey Fedoseev <aleksey@fedoseev.net>
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
import gettext

_ = gettext.gettext

logging = {
    'mission': None,
    'debug': None,
    'short': None,
    'image': None,
    'html': None,
    'test': None
}

#mission_log_buffer = ''
class LogFiles:
    df = None
    tf = None
    mf = None

def load_log_language(tr):
    global _ # pylint: disable=W0603
    _ = tr

def set_logging(target, do_logging):
    if target in logging:
        logging[target] = do_logging
        if do_logging and target != 'image' and target != 'short':
            f = open(do_logging, 'w')
            f.truncate()
            f.close()
#            if target == 'mission':
#                global mission_log_buffer # pylint: disable=W0603
#                mission_log_buffer = ''
    else:
        error_log('Bad logging target "%s"\n', target)
        sys.exit(1)

def open_logs():
    if logging['debug']:
        LogFiles.df = open(logging['debug'], 'a')
    else:
        LogFiles.df = None
    if logging['test']:
        LogFiles.tf = open(logging['test'], 'a')
    else:
        LogFiles.tf = None
    if logging['mission']:
        LogFiles.mf = open(logging['mission'], 'a')
    else:
        LogFiles.mf = None

def close_logs():
    if LogFiles.df is not None:
        LogFiles.df.close()
        LogFiles.df = None
    if LogFiles.tf is not None:
        LogFiles.tf.close()
        LogFiles.tf = None
    if LogFiles.mf is not None:
        LogFiles.mf.close()
        LogFiles.mf = None

def debug_log(s, *args):
    if logging['debug']:
        LogFiles.df.write('DEBUG: {}\n'.format(s % args))

def error_log(s, *args):
    debug_log(s, *args)
    mission_log(s, *args)
    sys.stderr.write('ERROR: {}\n'.format(s % args))

def test_log(s, *args):
    outs = (s % args) + '\n'
    if logging['test']:
        LogFiles.tf.write(outs)

def mission_log(s, *args):
    outs = (s % args) + '\n'
    #global mission_log_buffer  # pylint: disable=W0603
    #mission_log_buffer += outs
    if logging['mission']:
        LogFiles.mf.write(outs)

def get_mission_logs():
    res = ""
    if logging['mission']:
        LogFiles.mf = open(logging['mission'], 'r')
        res = LogFiles.mf.read()
        LogFiles.mf.close()
    return res
    #return mission_log_buffer

def short_log(s, *args):
    if logging['short']:
        f = open(logging['short'], 'a')
        f.write((s % args) + '\n')
        f.close()

def short_log_xml(parameters):
    if logging['short']:
        f = open(logging['short'], 'a')
        f.write('<?xml version="1.0" encoding="utf-8"?>\n')
        f.write('<result name="{}">\n'.format(parameters['name']))
        for p in parameters:
            if p == 'data':
                for d in parameters[p]:
                    f.write('<data stage="{}">\n{}</data>\n'.format(d[0], d[1]))
            elif p == 'image':
                for img in parameters[p]:
                    f.write('<image stage="%s" params="%s">{}</image>\n'.format(img))
            elif p == 'events':
                for stage in parameters[p]:
                    f.write('<events stage="{}">\n'.format(stage))
                    f.write('Ti:E\n')
                    for e in parameters[p][stage]:
                        f.write('{}:{}\n'.format(e[0], e[1]))
                    f.write('</events>\n')
            elif p == 'limits':
                f.write('<limits><x>{:01}</x><h>{:01}</h></limits>\n'.format(parameters[p]['x'],
                                                                             parameters[p]['h']))
            else:
                f.write('<{0}>{1}</{0}>\n'.format(p, parameters[p]))
        f.write('</result>\n')
        f.close()

def html_log(parameters):
    if logging['html']:
        f = open(logging['html'], 'a')
        f.write('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"' +
                '"http://www.w3.org/TR/html4/strict.dtd">\n')
        f.write('<html>\n')
        f.write('<head>\n')
        f.write(_('<title>Probe {}: Flight Results</title>\n').format(parameters['name']))
        f.write('<meta charset="UTF-8">\n')
        f.write('</head>\n')
        f.write('<body>\n')
        f.write(_('<h3>Probe {}: Flight Results</h3>\n').format(parameters['name']))
        f.write('<ul>\n')
        for p in parameters:
            if p not in ('name', 'data', 'realtime', 'image'):
                value = parameters[p]
                if p == 'planet':
                    # for future translation
                    if value == 'Moon':
                        value = _('Moon')
                    elif value == 'Mars':
                        value = _('Mars')
                    elif value == 'Mercury':
                        value = _('Mercury')
                    elif value == 'Venus':
                        value = _('Venus')
                    name = _('Mission')
                elif p == 'starttime':
                    name = _('Start time')
                elif p == 'missiontime':
                    name = _('Mission duration (sec)')
                elif p == 'startmass':
                    name = _('Start mass (kg)')
                elif p == 'result':
                    name = _('Flight results')
                    if value == 'landing':
                        value = _('Landed successfully')
                    elif value == 'crashed':
                        value = _('Crashed on the surface')
                    elif value == 'notstarted':
                        value = _('Not started (bad parameters)')
                    elif value == 'error':
                        value = _('Calculation error')
                    elif value == 'terminated':
                        value = _('Terminated in flight')
                    elif value == 'termonsurface':
                        value = _('Terminated on surface')
                    elif value == 'acceleration':
                        value = _('Crushed by overload')
                elif p == 'reason':
                    name = _('Last system state')
                    if value == 'unknown':
                        value = _('Not available')
                    elif value == 'cpuoff':
                        value = _('CPU off (prob. overheat)')
                    elif value == 'nocpu':
                        value = _('No CPU on board')
                    elif value == 'noenergy':
                        value = _('Not enough energy (double SAFE MODE)')
                    elif value == 'limit':
                        value = _('Mission time limit')
                elif p == 'surfacetime':
                    name = _('Time on surface (sec)')
                elif p == 'score':
                    name = _('Score')
                elif p == 'scientificinformation':
                    name = _('Scientifical information achieved (kB)')
                else:
                    name = None
                if name is not None:
                    f.write('<li><strong>%s</strong>: %s\n' % (name, value))
        if 'image' in parameters:
            f.write(_('<li><strong>Parameters history:</strong><br/>\n'))
            i = 0
            for img in parameters['image']:
                url = img[2]
                f.write('<a href="%s"><img width="300px" src="%s" align="left"/></a>&nbsp;' %
                        (url, url))
                i += 1
                if i % 2 == 0:
                    f.write('<br clear="left"/>\n')
            f.write('<br clear="left"/>\n')
        f.write(_('<li><strong>Telemetry:</strong>\n'))
        f.write('<pre>\n')
        f.write(get_mission_logs())
        f.write('</pre>\n')
        f.write('</ul>\n')
        f.write('</body>\n')
        f.write('</html>\n')
        f.close()

def get_image_template():
    return logging['image']
