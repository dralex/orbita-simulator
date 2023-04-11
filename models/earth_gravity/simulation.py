# -----------------------------------------------------------------------------
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# The Orbita Simulator
# The Earth orbit simulation model (v2)
#
# The gravity simulation
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
import math
import time
from os.path import basename
import gettext
import pyxb

import venus.testmodel
import calcmodels.planet
import xmlconverters
from logger import set_logging, test_log, time_to_str
from plotgraph import plot_graph, plot_parametric
from errors import CriticalError
from language import Language

_ = gettext.gettext
DEFAULT_LANG = 'en'
LANG_ORIGIN = 'sputnik'
LOCAL_DIR = os.path.dirname(os.path.abspath(__file__))
PARAMETERS_FILE = os.path.join(LOCAL_DIR, 'parameters.xml')

def load_parameters_atmosphere(parameters):
    for planet_params in parameters.Planets.values():
        if not planet_params.Atmosphere:
            if hasattr(planet_params,
                       'atmosphere_table') and planet_params.atmosphere_table is not None:
                planet_params.Atmosphere = calcmodels.planet.TableAtmosphere(parameters,
                                                                             planet_params.name)
            else:
                planet_params.Atmosphere = calcmodels.planet.BasicAtmosphere(parameters,
                                                                             planet_params.name)

class Probe: # pylint: disable=R0902
    def __init__(self, testname, filename, params, name, planet, tick, mass, duration, # pylint: disable=R0913
                 x, y, vx, vy, ispeed, itime, itraction, iduration,
                 oa, av, edge, moment):
        self.filename = filename
        self.name = testname
        self.Parameters = params

        self.planet = planet
        self.tick = tick
        self.mass = mass
        self.time = 0.0
        self.duration = duration

        if ((x is None or y is None or vx is None or vy is None or oa is None or # pylint: disable=R0916
             av is None or not edge or moment is None)):
            raise CriticalError(_('Error in model parameters'))

        self.x = x
        self.y = y
        self.height = math.sqrt(self.x ** 2 + self.y ** 2)
        self.v_x = vx
        self.v_y = vy
        self.velocity = None
        self.angle = None
        self.acceleration = None
        self.max_acceleration = None
        self.acceleration_stokes = None
        self.ispeed = ispeed
        self.itime = itime
        self.itraction = itraction
        self.iduration = iduration
        if ((self.ispeed is not None and
             (self.itime is None or self.itraction is None or self.iduration is None))):
            raise CriticalError(_('Not enought model parameters'))

        self.orient_angle = oa
        self.angular_velocity = av
        self.edge = edge
        self.square = self.edge ** 2
        self.moment = moment

        self.flight_status = None
        self.flight_message = None

        self.inertia_moment = None

    def check_limits(self): # pylint: disable=R0912
        planet_params = self.Parameters.Planets[self.planet]
        R = float(planet_params.radius)
        if not R < self.height <= 100000000:
            raise CriticalError(_('Bad parameters: the probe height %f should be in [%d; 100000000] m') # pylint: disable=C0301
                                % (self.height, R))
        if abs(self.v_y) > 20000:
            raise CriticalError('Bad parameters: the absolute velocity Vy exceeds 20000 m/sec: %f' %
                                self.v_y)
        if abs(self.v_x) > 20000:
            raise CriticalError('Bad parameters: the absolute velocity Vx exceeds 20000 m/sec: %f' %
                                self.v_x)
        if self.tick < 0.1 or self.tick > 3600:
            raise CriticalError('Bad parameters: the print period %f should be in [0.1; 3600]' %
                                self.tick)
        if self.planet != 'Earth':
            raise CriticalError('Bad parameters: only planet Earth is supported')
        if self.mass <= 0.0:
            raise CriticalError('Bad parameters: the probe mass %f should be positive' %
                                self.mass)
        if not 0 < self.duration <= 24 * 3600:
            raise CriticalError('Bad parameters: the modelling time %f should be in (0; %f]' %
                                (self.duration, 24 * 3600))
        if self.ispeed is not None and not 0 < self.ispeed <= 10000.0:
            raise CriticalError('Bad parameters: the impulse speed %f should be in (0; 10000]' %
                                self.ispeed)
        if self.itime is not None:
            if self.itime < 0.0:
                raise CriticalError('Bad parameters: the engine start time %f should not be negative' % # pylint: disable=C0301
                                    self.itime)
            if self.itime > self.duration:
                raise CriticalError('Bad parameters: the engine start time %f should not exceed the modelling time %f' % # pylint: disable=C0301
                                    (self.itime, self.duration))
        if self.itraction is not None and (self.itraction <= 0 or self.itraction > 1000.0):
            raise CriticalError('Bad parameters: traction %f should be in (0; 1000]' %
                                self.itraction)
        if self.iduration is not None and self.iduration < 0.0:
            raise CriticalError('Bad parameters: the engine duration %f should not be negative' %
                                self.iduration)
        if not 0 <= self.orient_angle < 360.0:
            raise CriticalError('Bad parameters: the orientation angle %f should be in [0; 360)' %
                                self.orient_angle)
        if abs(self.angular_velocity) > 360:
            raise CriticalError('Bad parameters: the angular velocity %f exceeds 360' %
                                self.angular_velocity)
        if not 0 < self.edge <= 10:
            raise CriticalError('Bad parameters: the probe cube size %f exceeds 10 m' %
                                self.edge)
        if abs(self.moment) > 1000:
            raise CriticalError('Bad parameters: the absolute moment %f exceeds 1000' %
                                self.moment)
        if abs(self.tick) < 1:
            raise CriticalError('Bad parameters: the print period %f should not be less than 1 sec' % # pylint: disable=C0301
                                self.tick)

    @classmethod
    def fromFile(cls, testname, filename, params):
        xmldata = xmlconverters.read_xml_file(filename)
        try:
            p = venus.testmodel.CreateFromDocument(xmldata)
            if not hasattr(p, 'impulse_speed'):
                p.impulse_speed = None
            if not hasattr(p, 'impulse_time'):
                p.impulse_time = None
            if not hasattr(p, 'impulse_traction'):
                p.impulse_traction = None
            if not hasattr(p, 'impulse_duration'):
                p.impulse_duration = None
            return Probe(testname,
                         filename,
                         params,
                         p.name,
                         p.planet,
                         float(p.tick),
                         float(p.mass),
                         float(p.duration),
                         float(p.x),
                         float(p.y),
                         float(p.vx),
                         float(p.vy),
                         float(p.impulse_speed) if p.impulse_speed is not None else None,
                         float(p.impulse_time) if p.impulse_time is not None else None,
                         float(p.impulse_traction) if p.impulse_traction is not None else None,
                         float(p.impulse_duration) if p.impulse_duration is not None else None,
                         float(p.orient_angle),
                         float(p.angular_velocity),
                         float(p.constr_edge),
                         float(p.moment))
        except pyxb.BadDocumentError as e:
            test_log(_('Bad XML document: %s'), str(e))
            return None
        except pyxb.ValidationError as e:
            test_log(_('XML error: %s'), str(e))
            return None

    def gravity_simulation(self, tick_length, print_step, imgtmpl): # pylint: disable=R0914,R0912,R0915
        start_real_time = time.time()
        prev_seconds = -1

        collector = {}
        collector['Ti'] = []
        collector['X'] = []
        collector['Y'] = []
        collector['H'] = []
        collector['Vx'] = []
        collector['Vy'] = []
        collector['m'] = []
        collector['Acc'] = []
        collector['As'] = []
        collector['A'] = []
        collector['OA'] = []
        collector['w'] = []

        planet_params = self.Parameters.Planets[self.planet]
        G = float(self.Parameters.G)
        M = float(planet_params.mass)
        R = float(planet_params.radius)

        self.height = math.sqrt(self.x ** 2 + self.y ** 2)
        self.max_acceleration = self.acceleration = G * M / self.height ** 2
        self.velocity = math.sqrt(self.v_x ** 2 + self.v_y ** 2)
        atm_border = planet_params.Atmosphere.border(float(planet_params.atmosphere.density_border))
        aerodynamic_coeff = 1.05
        self.inertia_moment = (1 / 12.0) * self.mass * (2 * self.edge ** 2)

        while self.time < self.duration:

            if self.y == 0.0:
                if self.x > 0.0:
                    self.angle = 0
                else:
                    self.angle = 180.0
            else:
                self.angle = math.degrees(math.atan(self.x / self.y))
                if self.x >= 0.0:
                    if self.y < 0.0:
                        self.angle -= 180.0
                else:
                    if self.y < 0.0:
                        self.angle += 180.0
                    else:
                        self.angle += 360.0

            if self.angle > 360.0:
                self.angle -= 360.0
            if self.angle < 0.0:
                self.angle += 360.0

            radius = self.x ** 2 + self.y ** 2
            self.height = math.sqrt(radius)

            if self.height <= R:
                if abs(self.velocity) <= 100:
                    msg = _('LANDING')
                    self.flight_status = 'completed'
                    self.flight_message = _('The probe has landed')
                else:
                    msg = _('CRUSHED')
                    self.flight_status = 'failed'
                    self.flight_message = _('The probe crushed on the surface')
                test_log('%s Ti=%s, Ang=%.2f V=%.2f, Max.Acc=%.2f',
                         msg,
                         time_to_str(self.time),
                         self.angle,
                         self.velocity,
                         self.max_acceleration)
                break

            gmr32 = G * M * self.mass / math.pow(radius, 1.5)
            F_gravity_x = - self.x * gmr32
            F_gravity_y = - self.y * gmr32

            F_engine_x = 0
            F_engine_y = 0

            if self.ispeed is not None and self.itime <= self.time < self.itime + self.iduration:
                df = self.itraction * tick_length
                if df >= self.mass:
                    test_log(_('ERROR Ti=%s: the fuel is out') % time_to_str(self.time))
                    self.flight_status = 'failed'
                    self.flight_message = _('The fuel is out')
                    break
                phi_rad = math.radians(self.orient_angle)
                F_engine = self.itraction * self.ispeed
                F_engine_x = F_engine * math.cos(phi_rad)
                F_engine_y = F_engine * math.sin(phi_rad)
                self.mass -= df

            F_stokes_x = 0
            F_stokes_y = 0

            if self.height <= atm_border:
                d = planet_params.Atmosphere.density(self.height)
                F_stokes_x = aerodynamic_coeff * d * (self.v_x ** 2) * self.square / 2.0
                F_stokes_y = aerodynamic_coeff * d * (self.v_y ** 2) * self.square / 2.0
                if self.v_x > 0:
                    F_stokes_x = -F_stokes_x
                if self.v_y > 0:
                    F_stokes_y = -F_stokes_y
                self.acceleration_stokes = math.sqrt(F_stokes_x ** 2 + F_stokes_y ** 2) / self.mass
            else:
                self.acceleration_stokes = 0

            a_x = (F_gravity_x + F_engine_x + F_stokes_x) / self.mass
            a_y = (F_gravity_y + F_engine_y + F_stokes_y) / self.mass

            self.acceleration = math.sqrt(a_x ** 2 + a_y ** 2)
            if self.acceleration > self.max_acceleration:
                self.max_acceleration = self.acceleration

            self.v_x += a_x * tick_length
            self.v_y += a_y * tick_length
            self.velocity = math.sqrt(self.v_x ** 2 + self.v_y ** 2)

            self.x += self.v_x * tick_length
            self.y += self.v_y * tick_length

            if self.moment != 0 or self.angular_velocity != 0:
                self.angular_velocity += (self.moment / self.inertia_moment) * tick_length
                self.orient_angle += self.angular_velocity * tick_length

            if self.orient_angle >= 360.0:
                self.orient_angle -= 360.0
            if self.orient_angle <= 0.0:
                self.orient_angle += 360.0

            # запускаем не чаще, чем раз в секунду
            if self.time == 0 or int(self.time) - prev_seconds >= print_step:
                parameters = []
                collector['Ti'].append(self.time)
                parameters.append('Ti=%s' % time_to_str(self.time))
                collector['X'].append(self.x)
                parameters.append('X=%010.1f' % self.x)
                collector['Y'].append(self.y)
                parameters.append('Y=%010.1f' % self.y)
                h = (self.height - R) / 1000.0
                collector['H'].append(h)
                parameters.append('H=%08.1f' % h)
                collector['Vx'].append(self.v_x)
                parameters.append('Vx=%06.1f' % self.v_x)
                collector['Vy'].append(self.v_y)
                parameters.append('Vy=%07.1f' % self.v_y)
                collector['A'].append(self.angle)
                parameters.append('A=%05.1f' % self.angle)
                collector['Acc'].append(self.acceleration)
                parameters.append('Acc=%05.1f' % self.acceleration)
                collector['As'].append(self.acceleration_stokes)
                parameters.append('As=%05.1f' % self.acceleration_stokes)
                collector['m'].append(self.mass)
                parameters.append('m=%07.2f' % self.mass)
                collector['OA'].append(self.orient_angle)
                parameters.append('OA=%05.1f' % self.orient_angle)
                collector['w'].append(self.angular_velocity)
                parameters.append('w=%04.1f' % self.angular_velocity)
                test_log(' '.join(parameters))
                prev_seconds = int(self.time)

            real_time = time.time()
            if real_time - start_real_time > 120:
                raise CriticalError(_('test model running too long'))
            self.time += tick_length

        test_log(_('The calculation completed. Ti=%s'), time_to_str(self.time))

        self.flight_status = 'completed'
        self.flight_message = _('Calulation completed')

        if imgtmpl is not None:
            label = 'Ballistics'
            imagefile = '%s%s-%s.png' % (imgtmpl, self.name, label)
            plot_parametric((collector['X'], collector['Y']),
                            _("Probe position (km)"), imagefile,
                            R,
                            atm_border,
                            _)

            label = 'Ballistics-Mechanics'
            imagefile = '%s%s-%s.png' % (imgtmpl, self.name, label)
            plot_graph(collector['Ti'], self.duration,
                       (collector['A'], collector['OA']),
                       (_("Navigation"), _("Orientation")),
                       _("Angle (degree)"), imagefile, [0, 360], _, True)

            label = 'Angular-Velocity'
            imagefile = '%s%s-%s.png' % (imgtmpl, self.name, label)
            plot_graph(collector['Ti'], self.duration,
                       collector['w'], None,
                       _("Angular Velocity (degree/s)"), imagefile,
                       ['calc', 'calc'], _)

            label = 'Mass'
            imagefile = '%s%s-%s.png' % (imgtmpl, self.name, label)
            plot_graph(collector['Ti'], self.duration,
                       collector['m'], None,
                       _("Mass (kg)"), imagefile, ['calc', 'calc'], _)

            label = 'Acceleration'
            imagefile = '%s%s-%s.png' % (imgtmpl, self.name, label)
            plot_graph(collector['Ti'], self.duration,
                       collector['Acc'], None,
                       _("Acceleration (m/s2)"), imagefile, ['calc', 'calc'], _)

def run(testname, testfile, logfile, debugfile, shortfile, imagetempl, htmlteml, lang=DEFAULT_LANG): #pylint: disable=R0912,W0613

    if lang != DEFAULT_LANG:
        Language.set_lang(lang)
        global _ # pylint: disable=W0603
        _ = Language.get_tr()

    if logfile:
        set_logging('test', logfile)
    if imagetempl:
        set_logging('image', imagetempl)

    probe = None
    try:
        parameters = xmlconverters.GlobalParameters.load(Language,
                                                         PARAMETERS_FILE)
        load_parameters_atmosphere(parameters)

        probe = Probe.fromFile(testname, testfile, parameters)
        if probe is None:
            raise CriticalError(_('The probe calculation file %s is not available') %
                                testfile)
        probe.check_limits()

        test_log(_('The probe model:'))
        test_log(_('\tPlanet: %s'), probe.planet)
        test_log(_('\tPrint period: %s s'), probe.tick)
        test_log(_('\tProbe mass: %.3f kg'), probe.mass)
        test_log(_('\tModelling duration: %.1f s'), probe.duration)
        test_log(_('\tStart X: %.2f m'), probe.x)
        test_log(_('\tStart Y: %.2f m'), probe.y)
        test_log(_('\tStart horizontal velocity Vx: %.2f m'), probe.v_x)
        test_log(_('\tStart vertical velocity Vy: %.2f m'), probe.v_y)

        if probe.ispeed is not None:
            test_log(_('\tThe engine impulse speed: %.2f m/sec'), probe.ispeed)
            test_log(_('\tThe engine traction: %.2f kg/sec'), probe.itraction)
            test_log(_('\tThe engine start time: %.2f sec'), probe.itime)
            test_log(_('\tThe engine duration: %.2f с'), probe.iduration)

        test_log(_('\tThe start orientation angle: %.2f deg'), probe.orient_angle)
        test_log(_('\tThe start angular velocity: %.4f deg/sec'), probe.angular_velocity)
        test_log(_('\tThe probe size: %f x %f x %f m'), probe.edge, probe.edge, probe.edge)
        test_log(_('\tThe moment: %f'), probe.moment)

        tick_length = float(parameters.Planets[probe.planet].tick)
        probe.gravity_simulation(tick_length, probe.tick, imagetempl)

    except CriticalError as e:
        test_log(_('CriticalError: %s') % str(e))
        return False

    return True

if __name__ == '__main__':

    if not 2 <= len(sys.argv) <= 5:
        print('usage: %s <testmodel.xml>'  % sys.argv[0] +
              ' [--test-log=<log-file>]' +
              ' [--imgages=<images>] [--lang=<en|ru>]')
        sys.exit(1)

    testLogFile = None
    testImageTempl = None
    langStr = DEFAULT_LANG
    for arg in sys.argv[2:]:
        if arg.find('--test-log=') != -1:
            testLogFile = arg[len('--test-log='):]
        if arg.find('--images=') != -1:
            testImageTempl = arg[len('--images='):]
        if langStr == DEFAULT_LANG and arg.find('--lang=') != -1:
            langStr = arg[len('--lang='):]

    task = basename(sys.argv[1]).split(".")[0]

    if run(task, sys.argv[1], testLogFile, None, None, testImageTempl, None, langStr):
        sys.exit(0)
    else:
        sys.exit(1)
