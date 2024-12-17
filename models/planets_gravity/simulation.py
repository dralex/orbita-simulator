# -----------------------------------------------------------------------------
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# The Orbita Simulator
# The simple gravity calculation model
#
# Gravity simulator
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
if sys.version_info.minor >= 10:
    import collections
    import collections.abc
    collections.MutableSequence = collections.abc.MutableSequence

import math
import gettext
import time
import pyxb

import gdata as data
from glogger import set_logging, test_log, open_logs, close_logs, short_log_xml
from plotgraph import plot_graph
import venusg.testmodel
from errors import CriticalError

_ = gettext.gettext
DEFAULT_LANGUAGE = 'en'
LANG_ORIGIN = 'orbita'

def set_language(lang):
    global _ # pylint: disable=W0603
    t = gettext.translation(LANG_ORIGIN, '.', languages=[lang])
    _ = t.gettext
    t.install()
    data.load_language(_)

class Probe:
    def __init__(self, the_planet, tick, square, mass, h, x, vy, vx, aerodynamic_coeff):
        self.name = ''
        self.planet = the_planet
        self.tick = tick
        self.total_mass = mass
        self.friction_square = square
        self.x = x
        self.height = float(data.Planets[self.planet].radius) + h
        self.v_x = vx if vx != 0.0 else 0.000001
        self.v_y = vy
        self.aerodynamic_coeff = aerodynamic_coeff
        self.time = 0.0
        self.angle = 180.0 * math.atan(abs(vy / self.v_x)) / math.pi
        self.acceleration = 0.0
        self.max_acceleration = 0.0

    @classmethod
    def fromFile(cls, filename):
        xmldata = data.read_xml_file(filename)
        try:
            testprobe = venusg.testmodel.CreateFromDocument(xmldata)
            if hasattr(testprobe, 'h') and testprobe.h is not None:
                h = float(testprobe.h)
            else:
                h = float(data.Planets[testprobe.planet].atmosphere.height)
            if hasattr(testprobe, 'vx') and testprobe.vx is not None:
                vx = float(testprobe.vx)
            else:
                vx = math.sqrt(float(data.Parameters.G) *
                               float(data.Planets[testprobe.planet].mass) /
                               float(data.Planets[testprobe.planet].radius)) / 2.0
            return Probe(testprobe.planet,
                         float(testprobe.tick),
                         float(testprobe.square),
                         float(testprobe.mass),
                         h,
                         float(testprobe.x) if hasattr(testprobe, 'x') else 0.0,
                         float(testprobe.vy) if hasattr(testprobe, 'vy') else 0.0,
                         vx,
                         float(testprobe.aerodynamic_coeff))
        except pyxb.BadDocumentError:
            return None
        except pyxb.ValidationError:
            return None
        else:
            return testprobe

    def debug(self):
        test_log(_("Test Probe {}:").format(self.name))
        test_log(_("\tPlanet: %s"), self.planet)
        test_log(_("\tTick: %s"), self.tick)
        test_log(_("\tFriction square: %.4f m^2"), self.friction_square)
        test_log(_("\tTotal mass: %.4f kg"), self.total_mass)
        test_log(_("\tStart X: %.4f m"), self.x)
        test_log(_("\tStart height (Y): %.4f m"), self.height -
                 float(data.Planets[self.planet].radius))
        test_log(_("\tStart velocity (X): %.4f m/s"), self.v_x)
        test_log(_("\tStart velocity (Y): %.4f m/s"), self.v_y)

def gravity_simulation(probe, tick_length, print_step, imgtempl):

    start_real_time = time.time()
    simulation_time = 0.0
    prev_seconds = -1
    landed = False

    collector = {}
    collector['Ti'] = []
    collector['X'] = []
    collector['H'] = []
    collector['Vx'] = []
    collector['Vy'] = []
    collector['Ang'] = []
    collector['Ac'] = []
    collector['As'] = []

    while True:
        h = probe.height
        probe_mass = probe.total_mass
        square = probe.friction_square

        v_x = probe.v_x if probe.v_x != 0 else 0.000001
        v_y = probe.v_y
        v_2 = v_x ** 2 + v_y ** 2

        # aerodynamic force acceleration (Stokes)
        a_s = (probe.aerodynamic_coeff *
               data.planet_atmosphere_density(probe.planet, h) * v_2 *
               square / (2.0 * probe_mass))

        # gravity acceleration
        a_g_y = float(data.Parameters.G) * float(data.Planets[probe.planet].mass) / (h ** 2)

        angle_norm = 2.0 * math.atan(abs(v_y / v_x)) / math.pi
        angle = 90.0 * angle_norm
        probe.angle = angle

        # VERTICAL MOVEMENT

        # multiply Stokes by -1 if we're flying up
        if v_y > 0:
            a_s_sign = -1.0
        else:
            a_s_sign = 1.0

        a_y = -a_g_y + (a_s_sign * a_s) * angle_norm

        # HORIZONTAL MOVEMENT

        if v_x > 0:
            a_s_sign = 1.0
        else:
            a_s_sign = -1.0
        a_x = - (a_s_sign * a_s) * (1 - angle_norm)

        a = math.sqrt(a_x ** 2 + a_y ** 2)
        probe.acceleration = a
        probe.acceleration_stokes = a_s
        if probe.max_acceleration < a:
            probe.max_acceleration = a

        # write log every second
        if tick_length > 1 or simulation_time == 0 or (int(simulation_time) -
                                                       prev_seconds >= print_step):
            parameters = []
            collector['Ti'].append(probe.time)
            parameters.append('Ti=%s' % data.time_to_str(probe.time))
            collector['X'].append(probe.x)
            parameters.append('X=%09.1f' % probe.x)
            h = (probe.height - float(data.Planets[probe.planet].radius))
            collector['H'].append(h)
            parameters.append('H=%08.1f' % h)
            collector['Vx'].append(probe.v_x)
            parameters.append('Vx=%06.1f' % probe.v_x)
            collector['Vy'].append(probe.v_y)
            parameters.append('Vy=%07.1f' % probe.v_y)
            collector['Ang'].append(probe.angle)
            parameters.append('Ang=%04.1f' % probe.angle)
            collector['Ac'].append(probe.acceleration)
            parameters.append('Ac=%05.1f' % probe.acceleration)
            collector['As'].append(probe.acceleration_stokes)
            parameters.append('As=%05.1f' % probe.acceleration_stokes)
            test_log(' '.join(parameters))

            prev_seconds = int(simulation_time)

        simulation_time += tick_length
        probe.time += tick_length

        probe.v_x += a_x * tick_length
        probe.v_y += a_y * tick_length
        probe.x += probe.v_x * tick_length
        probe.height += probe.v_y * tick_length

        if probe.height <= data.Planets[probe.planet].radius:
            test_log(_("SURFACE! Ti=%s, V=%.2f m/s, Max.Acc=%.2f m/s^2 (%.2f g)"),
                     data.time_to_str(probe.time),
                     data.probe_velocity(probe),
                     probe.max_acceleration,
                     probe.max_acceleration / 9.81)
            landed = True
            break

        real_time = time.time()
        if real_time - start_real_time > 120:
            raise CriticalError('test model running too long')

    if imgtempl is not None:
        configobj = data.Config.Logging[probe.planet].landing
        for img in configobj.image:
            notfound = False
            for p in img.params.split(' '):
                if p not in collector:
                    # skip images which are not available in test model
                    notfound = True
                    break
            if notfound:
                continue
            imagefile = '%s%s-%s.png' % (imgtempl, probe.name, img.params.replace(' ', '-'))
            ylimits = ['calc', 'calc']
            if hasattr(img, 'ymin') and img.ymin is not None:
                ylimits[0] = float(img.ymin)
            if hasattr(img, 'ymax') and img.ymax is not None:
                ylimits[1] = float(img.ymax)
            if img.params.find(' ') == -1:
                plot_graph(collector['Ti'], collector[img.params],
                           img.label, imagefile, ylimits)
            else:
                values = []
                for p in img.params.split(' '):
                    values.append(collector[p])
                plot_graph(collector['Ti'], values, img.label, imagefile, ylimits, True)

    return landed

def run(testname, testfile, logfile, debugfile, shortfile, imagetempl, htmltmpl, lang='en'): # pylint: disable=W0613

    if lang != DEFAULT_LANGUAGE:
        set_language(lang)
        
    if logfile is not None:
        set_logging('test', logfile)
    if shortfile is not None:
        set_logging('short', shortfile)

    open_logs()
        
    data.parameters_load(lang)
    data.config_load(lang)
    data.planets_load()

    probe = Probe.fromFile(testfile)
    if probe is None:
        raise CriticalError(_('cannot load test file %s') % testfile)

    probe.name = testname
    probe.debug()

    check_probe_limits(probe)

    tick_length = 0.1 # 1/10 sec
    gravity_simulation(probe, tick_length, probe.tick, imagetempl)

    close_logs()
    params = {'name': testname}
    short_log_xml(params)

    return True

def check_probe_limits(p):
    if p.v_y > 0:
        raise CriticalError(_("cannot run test with positive Vy %f") % p.v_y)
    if abs(p.v_y) > 5000:
        raise CriticalError(_("cannot run test with abs(Vy) > 5000: %f") % p.v_y)
    if abs(p.v_x) > 5000:
        raise CriticalError(_("cannot run test with abs(Vy) > 5000: %f") % p.v_x)
    if p.tick <= 0.0:
        raise CriticalError(_('negative tick %f') % p.tick)
    if p.planet not in ['Moon', 'Mars', 'Mars2', 'Mercury', 'Venus', 'Earth']:
        raise CriticalError(_("bad planet %s") % p.planet)
    if p.friction_square <= 0.0:
        raise CriticalError(_("negative friction square %f") % p.friction_square)
    if p.total_mass <= 0.0:
        raise CriticalError(_("negative probe mass %f") % p.total_mass)
    if p.height <= data.Planets[p.planet].radius:
        raise CriticalError(_("bad probe height %f") % p.height)

if __name__ == '__main__':

    if not (2 <= len(sys.argv) <= 13) or len(sys.argv) == 9:
        print('usage: %s <testmodel.xml> | ' % sys.argv[0] +
              '( <planet> <print-tick> <square> <mass> ' +
              '[<h> <x> <Vy> <Vx> <aerodynamic-coeff>] ) ' +
              '[--test-log=<log-file>] [--img-templ=<images>] [--lang=<en|ru>]')
        sys.exit(1)

    testLogFile = None
    testImageTempl = None
    langStr = DEFAULT_LANGUAGE
    addargs = 0
    for arg in sys.argv[-3:]:
        if arg.find('--test-log=') != -1:
            testLogFile = arg[len('--test-log='):]
            addargs += 1
        elif arg.find('--img-templ=') != -1:
            testImageTempl = arg[len('--img-templ='):]
            addargs += 1
        elif langStr == DEFAULT_LANGUAGE and arg.find('--lang=') != -1:
            langStr = arg[len('--lang='):]
            addargs += 1

    if langStr != DEFAULT_LANGUAGE:
        set_language(langStr)

    if testLogFile is not None:
        set_logging('test', testLogFile)

    open_logs()
        
    data.parameters_load(langStr)
    data.config_load(langStr)
    data.planets_load()

    restargs = len(sys.argv) - addargs
    if restargs > 2 and sys.argv[1] not in data.Planets:
        print(_("cannot find planet %s in parameters") % sys.argv[1])
        sys.exit(1)

    if restargs == 2:
        the_probe = Probe.fromFile(sys.argv[1])
        if the_probe is None:
            print(_('cannot load probe %s') % sys.argv[1])
            sys.exit(1)
        the_probe.name = sys.argv[1]
    elif 3 <= len(sys.argv) <= 9:
        planet = sys.argv[1]
        pl_params = data.Planets[planet]
        the_probe = Probe(planet,
                          int(sys.argv[2]),
                          float(sys.argv[3]),
                          float(sys.argv[4]),
                          float(pl_params.atmosphere.height),
                          0.0,
                          0.0,
                          math.sqrt(float(data.Parameters.G) * float(pl_params.mass) /
                                    float(pl_params.radius)) * float(pl_params.start_braking_koeff),
                          0.0)
        the_probe.name = 'cli'
    else:
        the_probe = Probe(sys.argv[1],
                          int(sys.argv[2]), float(sys.argv[3]),
                          float(sys.argv[4]), float(sys.argv[5]),
                          float(sys.argv[6]), float(sys.argv[7]),
                          float(sys.argv[8]), float(sys.argv[9]))
        the_probe.name = 'cli'
    the_probe.debug()

    check_probe_limits(the_probe)

    the_tick_length = 0.1 # 1/10 sec
    gravity_simulation(the_probe, the_tick_length, the_probe.tick, testImageTempl)

    sys.exit(0)
