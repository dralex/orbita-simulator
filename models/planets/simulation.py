# -----------------------------------------------------------------------------
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# The Orbita Simulator
# The planet landing model
#
# Main simulation procedure
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
import os
import os.path
import math
import gettext

import data
from logger import debug_log, mission_log, set_logging, open_logs, close_logs
from errors import CriticalError, Terminated

_ = gettext.gettext

DEFAULT_LANG = 'en'
USE_PYCONTROL = True

if USE_PYCONTROL:
    try:
        import pycontrol.program
        import api.probe_runtime
    except ImportError:
        data.critical_error(None, _('Cannot import pycontrol'))

def angle_R(x, y):
    if x != 0:
        aR = math.atan(y / x)
    else:
        signy = 1 if y > 0 else -1
        aR = signy * math.pi / 2.0
    return aR

def simulation_heating(probe, ext_temp, tick_length, planet_params): # pylint: disable=W0613

    mission_params = data.Parameters.Missions[probe.mission]

    T = probe.T
    if ext_temp <= T:
        return

    if probe.has_isolator:
        k = float(mission_params.isolator.k)
    else:
        k = 1.0
    k *= (1.0 - data.probe_thermal_protection(probe))
    Q = (k *
         (ext_temp - T) *
         probe.heat_transmission_surface /
         (float(probe.parameters.radius_external) -
          float(probe.parameters.radius_internal))) * tick_length

    if probe.has_absorber:
        if T < mission_params.absorber.T_melting:
            probe.T += Q / (float(mission_params.absorber.C_hard) * probe.absorber_mass)
            if probe.T >= float(mission_params.absorber.T_melting):
                probe.absorber_state = 'melting'
                probe.T = float(mission_params.absorber.T_melting)
        else:
            if probe.absorber_state == 'melting':
                dM = Q / float(mission_params.absorber.L)
                probe.hard_absorber_mass -= dM
                if probe.hard_absorber_mass <= 0:
                    probe.absorber_state = 'liquid'
            elif probe.absorber_state == 'liquid':
                probe.T += Q / (float(mission_params.absorber.C_liquid) * probe.absorber_mass)
    else:
        probe.T = ext_temp

    data.probe_check_device_temp(probe)

def simulation_program(probe, program):
    if program is not None:
        try:
            program.run()
        except pycontrol.program.FinishError:
            message = _('Flying program completed.')
            data.mission_log(message)
            data.terminate(probe, 'program', message)
        except pycontrol.program.ProgramError as e:
            str_e = str(e).replace('%', '%%')
            message = _('Program error: %s\n%s') % (str_e, e.dump)
            data.mission_log(message)
            data.terminate(probe, 'program', message)
        except pycontrol.program.SecurityError as e:
            str_e = str(e).replace('%', '%%')
            message = _('Security error while running the program:\n%s') % str_e
            data.mission_log(message)
            data.terminate(probe, 'program', message)
        except pycontrol.program.ControlError as e:
            str_e = str(e).replace('%', '%%')
            program.print_stderr()
            data.critical_error(probe, _('Program runtime error:\n%s'), str_e)

def simulation_flight_heating(probe, h, tick_length, v_2, planet_params):
    gas_density = data.planet_atmosphere_density(probe.planet, h)
    gas_temp = (data.planet_atmosphere_temperature(probe.planet, h) +
                (gas_density ** 0.5) * v_2 / (2.0 * planet_params.atmosphere.C * 10.0))
    probe.T_gas = gas_temp
    simulation_heating(probe, gas_temp, tick_length, planet_params)

def simulation_launch(probe, program, tick_length): # pylint: disable=R0912

    mission_params = data.Parameters.Missions[probe.mission]
    planet_params = data.Planets[mission_params.planet]

    probe.stage = 'Launch'
    probe.start_stage_time = 0.0
    simulation_time = 0.0
    prev_seconds = -1
    probe.tick_length = tick_length
    probe.logconfig = data.setup_diagnostics(probe)
    probe.takeOff = False
 
    # caсhing
    GM = data.Parameters.G * planet_params.mass
    MaxLaunchTime = data.Parameters.MaxLaunchTime
    max_wait_time = mission_params.launch.max_wait_time
    max_height = mission_params.launch.max_height + planet_params.radius
    planetRadius = data.Planets[probe.planet].radius

    probe.y = probe.height

    probe.land_distance = 0.0

    probe.orbit_cycle = 0
    cc = False

    while True:
        simulation_program(probe, program)

        h = probe.height
        probe_mass = probe.total_mass
        x = probe.x
        y = probe.y
        v_x = probe.v_x
        v_y = probe.v_y

        # alpha - the angle between radius vector and x axis
        sin_alpha = y/h
        cos_alpha = x/h
        alphaR = angle_R(x, y)

        v_2 = v_x ** 2 + v_y ** 2
        v = math.sqrt(v_2)

        # beta - the angle between velocity vector and x axis
        #sin_beta = v_y/v
        #cos_beta = v_x/v
        betaR = angle_R(v_x, v_y)

        gammaR = alphaR - betaR
        probe.v_r = v * math.cos(gammaR) # rad velocity
        probe.v_t = v * math.sin(gammaR) # tan velocity

        # DYNAMICS (the forces applied to the probe)

        # the Stokes force
        # if data.is_model_on(probe, 'stokes'):
        #    a_s = (float(mission_params.aerodynamic_coeff) *
        #           data.planet_atmosphere_density(probe.planet, h) * v_2 *
        #           square / (2.0 * probe_mass))
        #    probe.acceleration_stokes = a_s
        # else:
        #    probe.acceleration_stokes = a_s = 0

        # gravity acceleration
        a_g = - GM / (h ** 2)
        #a_g = 0
        a_gy = a_g * sin_alpha
        a_gx = a_g * cos_alpha

        # engines
        a_e = 0.0
        a_ex = a_ey = 0
        for engine in probe.devices.device:
            if data.device_is_engine(engine.name) and data.probe_device_is_turnedon(engine):
                if data.probe_available_fuel(probe, engine.device.traction * tick_length):
                    a_e += engine.device.fuel_speed * engine.device.traction / probe_mass
                    # engine angle
                    e_angR = alphaR - engine.angle * math.pi/180.0
                    a_ex += a_e * math.cos(e_angR)
                    a_ey += a_e * math.sin(e_angR)
                    data.probe_decrement_fuel(probe, engine.device.traction * tick_length,
                                              tick_length)
                else:
                    data.probe_turnoff_device(probe, engine)
        probe.acceleration_engine = a_e

        # y axis acceleration
        a_y = a_gy + a_ey #+ stokes

        # x axis acceleration
        a_x = a_gx + a_ex #+ stokes

        # probe parameters update
        data.probe_update_total_mass(probe)

        a = math.sqrt(a_x ** 2 + a_y ** 2)
        probe.acceleration = a
        # check wether the probe was crushed by the acceleration
        if probe.acceleration > mission_params.max_acceleration:
            data.terminate(probe, 'acceleration',
                           _("Acceleration %3.2f. Max acceleration %3.2f was exceeded!") %
                           (a, mission_params.max_acceleration))
        if probe.max_acceleration < a:
            probe.max_acceleration = a

        # heating from friction
        if data.is_model_on(probe, 'termodynamics'):
            simulation_flight_heating(probe, h, tick_length, v_2, planet_params)

        simulation_time += tick_length
        probe.time += tick_length

        probe.v_x += a_x * tick_length
        probe.v_y += a_y * tick_length
        probe.x += probe.v_x * tick_length
        probe.y += probe.v_y * tick_length
        probe.height = math.sqrt(probe.x * probe.x + probe.y * probe.y)
        probe.land_distance = planetRadius * math.asin(probe.x / planetRadius)

        if probe.height <= planetRadius:
            if probe.takeOff:
                data.terminate(probe, 'crashed', _("Probe was crashed by the surface"))
            else:
                probe.y = probe.height = planetRadius
                probe.v_x = probe.v_y = 0 # no velocity on sufrace!
                if probe.time > max_wait_time:
                    data.terminate(probe, 'launch failed',
                                   _("Time limit for takeoff exceeded!"))
        elif not probe.takeOff:
            probe.takeOff = True
            debug_log(_("Take off at %s!"), data.time_to_str(simulation_time))
            mission_log(_("Take off Ti=%s"), data.time_to_str(probe.time))

        if -2000 < probe.x < 0 < probe.y and not cc:
            probe.orbit_cycle += 1
            cc = True
            debug_log(_("Orbit cycle at %s!"), data.time_to_str(simulation_time))
            if probe.orbit_cycle == mission_params.launch.cycles:
                debug_log(_("%s Success! %s has entered %s orbit. %d orbital cycles completed"),
                          data.time_to_str(simulation_time), probe.name,
                          planet_params.name, probe.orbit_cycle)
                mission_log(_("%s Success! %s has entered %s orbit. %d orbital cycles completed"),
                            data.time_to_str(simulation_time), probe.name,
                            planet_params.name, probe.orbit_cycle)
                data.probe_orbit_reached(probe)
                if "reach_orbit" in mission_params.result_criteria:
                    data.terminate(probe, 'orbit reached', _('orbit reached'))
                return True
        if cc and probe.x > 0:
            cc = False

        # critical checks
        data.probe_check_critical(probe)

        # electricity
        data.probe_update_power_balance(probe, tick_length)

        # telecommunication
        data.probe_update_bandwidth(probe, tick_length)

        # send telemetry no often that 1 sec
        if tick_length > 1.0 or int(simulation_time) > prev_seconds:
            data.probe_process_commands(probe, tick_length)
            data.probe_diagnostics(probe, tick_length)
            if probe.time > MaxLaunchTime:
                data.terminate(probe, 'Max launch time', _("Max launch time exceeded!"))
            if h >= max_height:
                data.terminate(probe, 'height limit', _('height limit'))
        prev_seconds = int(simulation_time)
    return False

def simulation_stage1(probe, program, tick_length): # pylint: disable=R0912

    mission_params = data.Parameters.Missions[probe.mission]
    planet_params = data.Planets[mission_params.planet]

    probe.stage = 'Landing'
    probe.start_stage_time = 0.0
    simulation_time = 0.0
    prev_seconds = -1
    probe.tick_length = tick_length
    probe.logconfig = data.setup_diagnostics(probe)

    data.probe_check_turnedon_parachutes(probe)

    while True:
        simulation_program(probe, program)

        h = probe.height
        probe_mass = probe.total_mass

        data.probe_check_parachute(probe)
        parachute_square = data.probe_get_available_parachure(probe)
        if parachute_square is None:
            square = probe.friction_square
        else:
            square = probe.friction_square + parachute_square

        v_x = probe.v_x if probe.v_x > 0 else 0.000001
        v_y = probe.v_y
        v_2 = v_x ** 2 + v_y ** 2

        if data.is_model_on(probe, 'stokes'):
            # the aerodyamic force
            a_s = (float(mission_params.aerodynamic_coeff) *
                   data.planet_atmosphere_density(probe.planet, h) * v_2 *
                   square / (2.0 * probe_mass))
            probe.acceleration_stokes = a_s
        else:
            probe.acceleration_stokes = a_s = 0

        # gravity
        a_g_y = data.Parameters.G * data.Planets[probe.planet].mass / (h ** 2)

        # engines
        a_e = 0.0
        for engine in data.probe_work_engine_devices(probe):
            if data.probe_available_fuel(probe, engine.device.traction * tick_length):
                a_e += engine.device.fuel_speed * engine.device.traction / probe_mass
                data.probe_decrement_fuel(probe, engine.device.traction * tick_length, tick_length)
            else:
                data.probe_turnoff_device(probe, engine)
        probe.acceleration_engine = a_e

        angle_norm = 2.0 * math.atan(abs(v_y / v_x)) / math.pi
        angle = 90.0 * angle_norm
        probe.angle = angle

        # vertical movement

        # multiply stokes by -1 if we're flying up
        if v_y > 0:
            a_s_sign = -1.0
        else:
            a_s_sign = 1.0

        a_y = -a_g_y + (a_s_sign * a_s + a_e) * angle_norm

        # horizontal movement

        if v_x > 0:
            a_s_sign = 1.0
        else:
            a_s_sign = -1.0
        a_x = - (a_s_sign * a_s + a_e) * (1 - angle_norm)

        # updating probe

        data.probe_update_total_mass(probe)

        a = math.sqrt(a_x ** 2 + a_y ** 2)
        probe.acceleration = a
        if probe.acceleration > mission_params.max_acceleration:
            data.terminate(probe, 'acceleration',
                           _("Acceleration %3.2f. Max acceleration %3.2f was exceeded!") %
                           (a, mission_params.max_acceleration))
        if probe.max_acceleration < a:
            probe.max_acceleration = a

        if data.is_model_on(probe, 'termodynamics'):
            simulation_flight_heating(probe, h, tick_length, v_2, planet_params)

        simulation_time += tick_length
        probe.time += tick_length

        probe.v_x += a_x * tick_length
        probe.v_y += a_y * tick_length
        probe.x += probe.v_x * tick_length
        probe.height += probe.v_y * tick_length

        if probe.height <= data.Planets[probe.planet].radius:
            probe.landing_velocity = data.probe_velocity(probe)
            if abs(probe.v_y) <= 0.1 or data.probe_has_available_damper(probe):
                if abs(probe.v_y) > 0.1:
                    data.add_event(probe, 'dumper')
                debug_log(_("Successfull landing %s!"), data.time_to_str(simulation_time))
                mission_log(_("LANDING Ti=%s, V=%.2f, Max.Acc=%.2f, Te=%.1f"),
                            data.time_to_str(probe.time),
                            probe.landing_velocity,
                            probe.max_acceleration,
                            probe.T)
                data.probe_landing(probe)
                return True
            data.terminate(probe, 'crashed', _("Probe was crashed by the surface"))

        # critical checks

        data.probe_check_critical(probe)

        # electricity

        data.probe_update_power_balance(probe, tick_length)

        # telecommunication

        data.probe_update_bandwidth(probe, tick_length)

        # send telemetry no often that 1 sec
        if tick_length > 1.0 or int(simulation_time) > prev_seconds:
            data.probe_process_commands(probe, tick_length)
            data.probe_diagnostics(probe, tick_length)

        prev_seconds = int(simulation_time)

    return False

def simulation_stage2(probe, program, tick_length):

    mission_params = data.Parameters.Missions[probe.mission]
    planet_params = data.Planets[mission_params.planet]
    probe.start_stage_time = probe.time
    simulation_time = 0.0
    prev_seconds = -1
    tick_period = 3600
    tick_factor = 1.01
    prev_tick_period = 3600
    prev_tick_time = 0.0
    probe.stage = 'Surface activity'
    probe.logconfig = data.setup_diagnostics(probe)
    probe.T_gas = data.planet_atmosphere_temperature(probe.planet,
                                                     float(data.Planets[probe.planet].radius))
    while True:
        simulation_program(probe, program)

        if data.is_model_on(probe, 'termodynamics'):
            simulation_heating(probe,
                               probe.T_gas,
                               tick_length, planet_params)

        # critical checks

        data.probe_check_critical(probe)

        # electricity

        data.probe_update_power_balance(probe, tick_length)

        # telecommunication

        data.probe_update_bandwidth(probe, tick_length)

        # telemetry

        # send telemetry no often than 1 sec
        if tick_length > 1.0 or int(simulation_time) > prev_seconds:
            data.probe_process_commands(probe, tick_length)
            data.probe_diagnostics(probe, tick_length)

            prev_seconds = int(simulation_time)

        simulation_time += tick_length
        probe.time += tick_length

#        if (start_period <= simulation_time <= start_period + start_tick_length):
#            tick_length = start_period

        if ((simulation_time >= 3600 * 24 and simulation_time >= tick_period and
             (int(prev_tick_time) / prev_tick_period < int(simulation_time) / tick_period))):

            data.Config.debug_diagn_period *= tick_factor
            tick_length *= tick_factor
            prev_tick_period = tick_period
            tick_period = int(tick_period * tick_factor)
            prev_tick_time = simulation_time
            debug_log(_("%s: set tick length to %f s, tick period to %f s"),
                      data.time_to_str(simulation_time), tick_length, tick_period)
            probe.tick_length = tick_length

        if data.is_model_on(probe, 'surfacelimited'):
            if ((probe.time - probe.start_stage_time >
                 data.Parameters.Missions[probe.mission].surface_max_time)):
                data.terminate(probe, 'limit', _('Time limit'))
    return False

def usage():
    print('usage: {} <probe-file> '.format(sys.argv[0]) +
          '[--mission-log=<mission-log-file] ' +
          '[--debug-log=<debug-log-file>] ' +
          '[--short-log=<short-log-file>] ' +
          '[--image=<image-name-template>] ' +
          '[--html-log=<html-log-file>] ' +
          '[--lang=<en|ru>]')
    sys.exit(1)

def run(probename, probefile, missionfile, debugfile, shortfile, imagedir, htmltmpl, lang='en'): # pylint: disable=R0912
    """ This is main entry point for simulation
    All logic, except command-line parsing should be inside this call
    """

    if lang != 'en':
        global _ # pylint: disable=W0603
        t = gettext.translation('orbita',
                                os.path.dirname(os.path.abspath(__file__)),
                                languages=[lang])
        _ = t.gettext
        t.install()
        data.load_language(_)

    if missionfile:
        set_logging('mission', missionfile)
    if debugfile:
        set_logging('debug', debugfile)
    if shortfile:
        set_logging('short', shortfile)
    if imagedir:
        imagetmpl = imagedir + '/'
        set_logging('image', imagetmpl)
    else:
        imagetmpl = None
    if htmltmpl:
        set_logging('html', htmltmpl)

    open_logs()

    if imagedir and not os.path.isdir(imagedir):
        data.critical_error(None, _("Bad image directory {}").format(imagedir))
        sys.exit(1)

    try:
        data.cleanup_collector()
        data.parameters_load()
        data.planets_load()
        data.config_load()
        data.devices_load()

        the_probe = data.probe_load(probename, probefile)

        if the_probe is None:
            data.critical_error(None, _("Cannot decode probe {}").format(probename))
            sys.exit(1)

        program = None

        if USE_PYCONTROL:
            if the_probe.python_program:
                try:
                    debug_log(_('python program available, running the runtime'))
                    runtime = api.probe_runtime.ProbeRuntime(the_probe)
                    program = pycontrol.program.Program(runtime, 'probe_api',
                                                        the_probe.python_program, _)
                except pycontrol.program.ControlError as e:
                    str_e = str(e).replace('%', '%%')
                    data.critical_error(the_probe, _('Probe program error:\n\t%s'), str_e)

        tick_length_1 = 0.1 # 1/10 sec
        if data.is_model_on(the_probe, 'launch'):
            simulation_launch(the_probe, program, tick_length_1)
            if imagetmpl:
                data.draw_images(the_probe, 'Launch', imagetmpl)
        if data.is_model_on(the_probe, 'landing'):
            simulation_stage1(the_probe, program, tick_length_1)
            if imagetmpl:
                data.draw_images(the_probe, 'Landing', imagetmpl)
        else:
            data.probe_landing(the_probe)
        if data.is_model_on(the_probe, 'surface') or data.is_model_on(the_probe, 'surfacelimited'):
            tick_length_2 = 10.0 # 10 sec
            simulation_stage2(the_probe, program, tick_length_2)
        else:
            data.write_short_log(the_probe, 'landing')
    finally:
        close_logs()
    return True

if __name__ == '__main__':

    if len(sys.argv) < 2 or len(sys.argv) > 8:
        usage()

    missionLogFile = None
    debugLogFile = None
    shortLogFile = None
    imageTemplate = None
    htmlLogFile = None
    langStr = None

    probe_file = sys.argv[1]

    for arg in sys.argv[2:]:
        if not missionLogFile and arg.find('--mission-log=') != -1:
            missionLogFile = arg[len('--mission-log='):]
        elif not debugLogFile and arg.find('--debug-log=') != -1:
            debugLogFile = arg[len('--debug-log='):]
        elif not shortLogFile and arg.find('--short-log=') != -1:
            shortLogFile = arg[len('--short-log='):]
        elif not imageTemplate and arg.find('--image=') != -1:
            imageTemplate = arg[len('--image='):]
        elif not htmlLogFile and arg.find('--html-log=') != -1:
            htmlLogFile = arg[len('--html-log='):]
        elif not langStr and arg.find('--lang=') != -1:
            langStr = arg[len('--lang='):]
        else:
            usage()

    if not langStr:
        langStr = DEFAULT_LANG

    try:
        probe_name = os.path.basename(probe_file)
        probe_name = probe_name[0:probe_name.find('.xml')]
        run(probe_name, probe_file, missionLogFile, debugLogFile,
            shortLogFile, imageTemplate, htmlLogFile, langStr)
    except Terminated as e:
        print(_("Termination error: {}").format(e))
        sys.exit(1)
    except CriticalError as e:
        print(_("Critical error: {}").format(e))
        sys.exit(2)
    sys.exit(0)
