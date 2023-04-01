# pylint: disable=C0302
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# The Orbita Simulator
# The planet landing model
#
# Simulator data storage
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

import os
import re
import datetime
from math import pi, sqrt, exp, log
import gettext
import pyxb

import venus.probe
import venus.devices
import venus.global_parameters
import venus.global_config
import venus.planets

from logger import load_log_language, debug_log, error_log, mission_log, short_log_xml, get_image_template, html_log
from errors import CriticalError, Terminated
from plotgraph import plot_graph

LOCAL_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_LANG = 'en'
PARAMETERS_FILE = os.path.join(LOCAL_DIR, 'parameters{}.xml')
DEVICES_FILE = os.path.join(LOCAL_DIR, 'devices{}.xml')
CONFIG_FILE = os.path.join(LOCAL_DIR, 'config{}.xml')
PLANETS_FILE = os.path.join(LOCAL_DIR, 'planets.xml')

_ = gettext.gettext
Devices = None
Parameters = None
Config = None
Planets = None
last_debug_diagn = 0.0
AD_messages = []
Collector = {}

MAX_ENGINE_ANGLE = 90.0

#Device types
DT_TRANMITTER = 1
DT_FUELTANK = 2
DT_PARACHUTE = 3
DT_DAMPER = 4
DT_ENGINE = 5
DT_SCIENTIFIC = 6
DT_BASE_DIAGNOSTIC = 7
DT_ACCUMULATOR = 8
DT_SOLARPANEL = 9
DT_ADV_DIAGNOSTIC = 10

def load_language(tr):
    global _ # pylint: disable=W0603
    _ = tr
    load_log_language(tr)

def xmlfiles(dirpath):
    result = []
    for f in os.listdir(dirpath):
        regexp = re.compile(r'^(.*)\.xml$')
        m = regexp.match(f)
        if not m:
            continue
        name = m.group(1)
        result.append((name, dirpath + '/' + f))
    return result

def cleanup_collector():
    global Collector #pylint: disable=W0603
    Collector = {}
    global AD_messages #pylint: disable=W0603
    AD_messages = []

def read_xml_file(f):
    return open(f).read()
#    encfile = codecs.open(f, 'r', encoding='utf-8')
#    return encfile.read()

def mission_adv_log(s, *args):
    msg = s % args
    debug_log(msg)
    AD_messages.append(msg)

def parameters_load(lang):
    global Parameters #pylint: disable=W0603
    Parameters = None
    lang_postfix = "-{}".format(lang) if lang != DEFAULT_LANG else ''
    xmldata = read_xml_file(PARAMETERS_FILE.format(lang_postfix))
    try:
        Parameters = venus.global_parameters.CreateFromDocument(xmldata)
        Parameters.Missions = {}
        for p in Parameters.missions.mission:
            if p.name in Parameters.Missions:
                critical_error(None,
                               _("Cannot decode parameters. Similar missions names: {}").format(p.name)) # pylint: disable=C0301
            p.Models = p.models.split(',')
            tmp = p.devices.replace('\n', '').replace(' ', '').replace('\t', '')
            p.Devices = tmp.split(',')
            Parameters.Missions[p.name] = p
            p.result_criteria = p.result.split(',')
            if p.max_length is None:
                p.max_length = p.max_radius #no stages allowed
    except pyxb.BadDocumentError as e:
        critical_error(None, _("Cannot load parameters: bad xml document"))
    except pyxb.ValidationError as e:
        critical_error(None, _("Cannot load parameters: error in %s") % e.location)
    else:
        debug_log(_("Parameters loaded successfully."))

def planets_load():
    global Planets #pylint: disable=W0603
    Planets = None
    xmldata = read_xml_file(PLANETS_FILE)
    try:
        Pl = venus.global_parameters.CreateFromDocument(xmldata)
        Planets = {}
        for p in Pl.planet:
            if p.name in Planets:
                critical_error(None, _("Cannot decode planets. Similar planets names: {}").format(p.name)) # pylint: disable=C0301
            Planets[p.name] = p
            if p.rotation is not None:
                p.period = (p.rotation.hours * 60 + p.rotation.minutes)*60 + p.rotation.seconds
            else:
                p.period = 99999999.0 # TODO cast error here
    except pyxb.BadDocumentError as e:
        critical_error(None, _("Cannot load planets: bad xml document"))
    except pyxb.ValidationError as e:
        critical_error(None, _("Cannot load planets: error in %s") % e.location)
    else:
        debug_log(_("Planets loaded successfully."))

def is_model_on(probe, model):
    return model in Parameters.Missions[probe.mission].Models

def is_device_allowed(probe, device):
    return device in Parameters.Missions[probe.mission].Devices

def config_load(lang):
    global Config #pylint: disable=W0603
    Config = None
    lang_postfix = "-{}".format(lang) if lang != DEFAULT_LANG else ''
    xmldata = read_xml_file(CONFIG_FILE.format(lang_postfix))
    try:
        Config = venus.global_config.CreateFromDocument(xmldata)
        Config.Logging = {}
        for m in Config.logging.mission:
            if m.name in Config.Logging:
                critical_error(None, _("Cannot decode config. Similar mission names: %s") % m.name) # pylint: disable=C0301
            Config.Logging[m.name] = m
        Config.debug_diagn_period = float(Config.logging.debug_diagn_period)
    except pyxb.BadDocumentError as e:
        critical_error(None, _("Cannot load config: bad xml document"))
    except pyxb.ValidationError as e:
        critical_error(None, _("Cannot load config: error in %s") % e.location)
    else:
        debug_log(_("Config loaded successfully."))

def devices_load(lang):
    global Devices #pylint: disable=W0603
    Devices = {}
    lang_postfix = "-{}".format(lang) if lang != DEFAULT_LANG else ''
    xmldata = read_xml_file(DEVICES_FILE.format(lang_postfix))
    try:
        devices = venus.devices.CreateFromDocument(xmldata)
        for d in devices.device:
            if d.name in Devices:
                critical_error(None, _("Cannot decode devices. Similar device names: %s") % d.name) # pylint: disable=C0301
            Devices[d.name] = d
            device_set_type(d.name)
    except pyxb.BadDocumentError as e:
        critical_error(None, _("Cannot load devices: bad xml document") % DEVICES_FILE)
    except pyxb.ValidationError as e:
        critical_error(None, _("Cannot load devices: error %s in %s") % (str(e), e.location))

def device_get(name):
    return Devices[name]

def device_set_type(name):
    d = Devices[name]
    if d.type == 'Transmitters':
        d.ntype = DT_TRANMITTER
    elif d.type == 'Fuel tanks':
        d.ntype = DT_FUELTANK
    elif d.type == 'Parachutes':
        d.ntype = DT_PARACHUTE
    elif d.type == 'Dampers':
        d.ntype = DT_DAMPER
    elif d.type == 'Engines':
        d.ntype = DT_ENGINE
    elif d.type == 'Scientific equipment':
        d.ntype = DT_SCIENTIFIC
    elif d.type == 'Base diagnostics':
        d.ntype = DT_BASE_DIAGNOSTIC
    elif d.type == 'Advanced diagnostics':
        d.ntype = DT_ADV_DIAGNOSTIC
    elif d.type == 'Accumulators':
        d.ntype = DT_ACCUMULATOR
    elif d.type == 'Solar panels':
        d.ntype = DT_SOLARPANEL
    else:
        d.ntype = 0

def device_is_transmitter(name):
    return Devices[name].ntype == DT_TRANMITTER

def device_is_fueltank(name):
    return Devices[name].ntype == DT_FUELTANK

def device_is_parachute(name):
    return Devices[name].ntype == DT_PARACHUTE

def device_is_damper(name):
    return Devices[name].ntype == DT_DAMPER

def device_is_engine(name):
    return Devices[name].ntype == DT_ENGINE

def device_is_scientific(name):
    return Devices[name].ntype == DT_SCIENTIFIC

def device_is_diagnostics(name):
    return (Devices[name].ntype == DT_BASE_DIAGNOSTIC) or (Devices[name].ntype == DT_ADV_DIAGNOSTIC)

def device_is_base_diagnostics(name):
    return Devices[name].ntype == DT_BASE_DIAGNOSTIC

def device_is_adv_diagnostics(name):
    return Devices[name].ntype == DT_ADV_DIAGNOSTIC

def device_is_accumulator(name):
    return Devices[name].ntype == DT_ACCUMULATOR

def device_is_solar_panel(name):
    return Devices[name].ntype == DT_SOLARPANEL

def probe_update_total_mass(p):
    p.device_mass = 0.0
    for d in p.devices.device:
        p.device_mass += d.actual_mass
    p.total_mass = p.construction_mass + p.isolator_mass + p.absorber_mass + p.device_mass

def probe_stage_load(s, mission_params):
    if s.geometry == "cylinder":
        s.internal_volume = (pi * s.radius ** 2) * s.length
    elif s.geometry == "sphere":
        s.internal_volume = (4.0 * pi / 3.0) * (s.radius ** 3)
        s.length = s.radius
    s.construction_mass = s.internal_volume * float(mission_params.construction.density)
    s.device_volume = 0

def probe_update_friction_square(p):
    r = p.parameters.radius_external
    if p.contruction is not None:
        for s in p.contruction.stage:
            if s.radius > r:
                r = s.radius
    friction_s = pi * (float(r) ** 2)
    return friction_s

def solar_generation(probe, power):
    if not probe.landed:
        return 0
    return power * planet_sunlight(probe.planet, probe.time, probe.flight.cycle_time)

def probe_update_power_balance(p, tick_len):
    pb = 0
    pg = 0
    for d in p.devices.device:
        if probe_device_is_turnedon(d):
            if d.device.power_generation > 0:
                pg += d.device.power_generation
            if device_is_solar_panel(d.name):
                solar = solar_generation(p, d.device.solar_power)
                pg += solar
                pb += solar
            pb += d.device.power_generation

    p.power_generation = pg
    p.power_balance = pb
    r = probe_update_energy(p, p.power_balance, tick_len)
    #p.energy_reserve = probe_energy_reserve(p)
    if r < 0:
        mission_adv_log(_('negative power balance %d, going to safe mode'), int(p.power_balance))
        probe_safe_mode(p)
        probe_update_power_balance(p, tick_len)

def probe_update_bandwidth(p, tick_length): # pylint: disable=R0912
    bandwidth = 0.0
    p.base_diag = False
    p.adv_diag = False

    for d in p.devices.device:
        if (d.transmitter_type and probe_device_is_turnedon(d)):
            bandwidth -= d.device.traffic_generation * tick_length
            d.transmitting = True
        else: d.transmitting = False
    p.total_bandwidth = abs(bandwidth)

    for d in p.devices.device:
        if probe_device_is_turnedon(d) and d.device.traffic_generation < 0:
            devbw = abs(d.device.traffic_generation * tick_length / d.period)
            if bandwidth + devbw <= 0:
                d.transmitting = True
                if (d.prev_transmitting != d.transmitting and (device_is_scientific(d.name) or
                                                               device_is_diagnostics(d.name))):
                    mission_adv_log(_("device %s started transmission"), d.identifier)
                if (p.landed and (device_is_scientific(d.name)
                                  and p.scientific_devices[d.name] > 0.0)):
                    if devbw < p.scientific_devices[d.name]:
                        si = devbw
                        p.scientific_devices[d.name] -= si
                    else:
                        si = p.scientific_devices[d.name]
                        p.scientific_devices[d.name] = 0.0
                    p.scientific_information += si
                if device_is_base_diagnostics(d.name):
                    p.base_diag = d
                elif device_is_adv_diagnostics(d.name):
                    p.adv_diag = d
                bandwidth += devbw
            else:
                if (d.prev_transmitting != d.transmitting and (device_is_scientific(d.name) or
                                                               device_is_diagnostics(d.name))):
                    mission_adv_log(_("device {} stopped transmitting due to bandwidth limit").format(d.identifier)) # pylint: disable=C0301
        elif (d.prev_transmitting != d.transmitting and
              (device_is_scientific(d.name) or device_is_diagnostics(d.name))):
            mission_adv_log(_("device {} stopped transmitting").format(d.identifier))
        d.prev_transmitting = d.transmitting

    p.bandwidth = p.total_bandwidth - abs(bandwidth)

def probe_landed(probe):
    return probe.landed

def probe_available_fuel(p, threshold):
    available = 0.0
    for d in p.devices.device:
        if (device_is_fueltank(d.name) and d.state == 'ON'):
            if d.available_fuel > threshold:
                available += d.available_fuel
    return available

def probe_decrement_fuel(p, dm, tick_len):
    for d in p.devices.device:
        if (device_is_fueltank(d.name) and d.state == 'ON'):
            if d.available_fuel >= dm:
                d.available_fuel -= dm
                d.actual_mass -= dm
                if d.available_fuel < p.minimal_fuel_threshold * tick_len:
                    # empry tank won't be available
                    mission_adv_log(_("fuel tank {} is empty, fuel left: {:05}").format(d.identifier, d.available_fuel)) # pylint: disable=C0301
                    d.state = 'DEAD'
                break

def probe_fuel_total(p):
    fuel = 0.0
    for d in p.devices.device:
        if device_is_fueltank(d.name):
            fuel += d.available_fuel
    return fuel

def probe_fuel_used(p):
    fuel_remains = probe_available_fuel(p, 0)
    return p.start_fuel - fuel_remains

def probe_update_energy(p, de, tick_len):
    #if tick_len == 0: return 0
    reserve = 0
    energy = de * tick_len / 3600.0 # to Watt * hours
    for d in p.devices.device:
        if d.accumulator_type and probe_device_is_turnedon(d):
            if energy < 0: # using the accumulator
                if d.available_energy > 0: # the accumulator not empty
                    if d.available_energy >= (- energy):
                        d.available_energy += energy
                        energy = 0
                    else:
                        energy += d.available_energy
                        d.available_energy = 0
                        mission_adv_log(_('Accumulator %s is empty') % d.identifier)
            elif energy > 0: # charging the accumulator
                need = d.device.capacity - d.available_energy
                if need > 0:  # accumulator not full
                    if energy >= need:
                        d.available_energy = d.device.capacity
                        energy -= need
                    else:
                        d.available_energy += energy
                        energy = 0
            reserve += d.available_energy
    p.energy_reserve = reserve
    return energy

# removed for optimisation
#def probe_energy_reserve (p):
#    reserve = 0
#    for d in p.devices.device:
#        if d.accumulator_type and probe_device_is_turnedon(d):
#            reserve += d.available_energy
#    return reserve
#

def probe_get_available_parachure(p):
    for d in p.devices.device:
        if (device_is_parachute(d.name) and probe_device_is_turnedon(d)):
            return float(d.device.parachute_square)
    return None

def probe_has_available_damper(p):
    velocity = probe_velocity(p)
    E = p.total_mass * (p.v_x ** 2 + p.v_y ** 2)/2.0
    for d in p.devices.device:
        if (device_is_damper(d.name) and probe_device_is_turnedon(d)):
#            if d.device.max_speed >= velocity: # TODO: improve dumper model later
#                debug_log(_("Damper %s used successfully! Velocity %3.2f, max velocity %3.2f") %
#                          (d.identifier, velocity, float(d.device.max_speed)))
#                return True
            if d.device.energy_compensation >= E:
                debug_log(_("Damper %s used successfully! Velocity %3.2f") %
                          (d.identifier, velocity))
                return True
            if d.device.custom:
                dL = velocity * sqrt(p.total_mass /d.kHook)
                #print "velocity, dL", velocity, dL
                if dL > d.springs_length/2:
                    debug_log(_("Damper %s collapsed! Compression %f > 1/2 of springs length") %
                              (d.identifier, dL))
                    return False
                return True
    return False

def probe_work_engine_devices(p):
    result = []
    for d in p.devices.device:
        if device_is_engine(d.name) and probe_device_is_turnedon(d):
            result.append(d)
    return result

def probe_check_critical(p):
    cpu_found = False
    for d in p.cpus:
        cpu_found = True
        if d.state != 'ON':
            terminate(p, 'cpuoff', _("CPU is dead"))
        else:
            return # cpu ok
    if not cpu_found:
        terminate(p, 'nocpu', _("No working CPU device found"))

def probe_check_device_temp(p):
    for d in p.devices.device:
        if d.state != 'DEAD' and d.device.critical_temperature < p.T:
            if d.name != 'cpu' and d.name != 'diagnadv':
                mission_adv_log(_("device %s has burn"), d.identifier)
            probe_break_device(p, d, "burn")
            d.state = 'DEAD'

def probe_check_parachute(p):
    for d in p.devices.device:
        if (device_is_parachute(d.name) and probe_device_is_turnedon(d)):
            velocity = probe_velocity(p)
            max_speed = float(d.device.max_speed)
            if velocity > max_speed:
                mission_adv_log(_("dropping parachute %s because of speed limit: V = %f, maxV = %f") % # pylint: disable=C0301
                                (d.identifier, velocity, max_speed))
                probe_turnoff_device(p, d)
                add_event(p, 'parachute drop s')

def probe_device_code_is_turnedon(p, name):
    for d in p.devices.device:
        if (d.name == name and probe_device_is_turnedon(d)):
            return d
    return None

def probe_device_type_is_turnedon(p, typ):
    for d in p.devices.device:
        if (d.device.type == typ and probe_device_is_turnedon(d)):
            return d
    return None

def probe_device_is_turnedon(d):
    return d.state == 'ON'

def probe_velocity(p):
    return sqrt(p.v_x ** 2 + p.v_y ** 2)

def probe_thermal_protection(p):
    if p.landed:
        return 0.0
    para = probe_device_type_is_turnedon(p, 'Parachutes')
    if para is None:
        return 0.0
    return min(float(para.device.thermal_protection), 1.0)

def probe_turnon_device(p, dev):
    if not probe_device_is_turnedon(dev):
        if device_is_engine(dev.name) and not probe_device_type_is_turnedon(p, 'Engines'):
            add_event(p, 'engines on')
        dev.state = 'ON'
        mission_adv_log(_("device %s is turned on") % dev.identifier)
        if device_is_parachute(dev.name):
            # checking max speed for the parachute and the availability of another parachutes
            parachute_crash = False
            velocity = probe_velocity(p)
            max_speed = dev.device.max_speed
            if velocity > max_speed:
                mission_adv_log(_("dropping parachute %s because of speed limit: V = %f, maxV = %f") % # pylint: disable=C0301
                                (dev.identifier, velocity, max_speed))
                parachute_crash = True
                add_event(p, 'parachute drop s')
            for d in p.devices.device:
                if (d.identifier != dev.identifier and (device_is_parachute(d.name) and
                                                        probe_device_is_turnedon(d))):
                    # if the parachute was already opened drop the both
                    mission_adv_log(_("dropping entangled parachutes: %s and %s") %
                                    (d.identifier, dev.identifier))
                    probe_turnoff_device(p, d)
                    parachute_crash = True
                    add_event(p, 'parachute drop e')
            if parachute_crash:
                probe_turnoff_device(p, dev)
            else:
                if probe_thermal_protection(p) > 0:
                    add_event(p, 'parachute on hs')
                else:
                    add_event(p, 'parachute on')

def probe_break_device(p, d, event): # pylint: disable=W0613
    debug_log(_("device %s has %s") % (d.identifier, event))
    d.state = 'DEAD'

def probe_remove_device(p, d, event): # pylint: disable=W0613
    # TODO: what is happening here?
    debug_log(_("device %s dropped %s") % (d.identifier, event))

def probe_drop_stage(p):
    mission_adv_log(_("dropping stage %s ") % p.current_stage)
    success = False
    for d in p.devices.device:
        if d.stage == p.current_stage:
            probe_remove_device(p, d, "(stage %d separation)" % p.current_stage)
            success = True
    if not success:
        mission_adv_log(_("dropping stage %s failed: stage not found") % p.current_stage)
    p.devices.device[:] = [d for d in p.devices.device if not d.stage == p.current_stage]
    p.cpus[:] = [d for d in p.cpus if not d.stage == p.current_stage]
    p.current_stage += 1

def probe_check_turnedon_parachutes(p):
    parachutes = {}
    for d in p.devices.device:
        if (device_is_parachute(d.name) and probe_device_is_turnedon(d)):
            parachutes[d.identifier] = d
    if len(parachutes) > 1:
        mission_adv_log(_("dropping entangled parachutes: %s") %
                        ', '.join(parachutes.keys()))
        for d in parachutes.values():
            probe_turnoff_device(p, d)
            add_event(p, 'parachute drop e')

def probe_turnoff_device(p, d):
    if probe_device_is_turnedon(d):
        d.state = 'OFF'
        # drop parachute when it is disabled
        if device_is_parachute(d.name):
            mission_adv_log(_("parachute %s has dropped"), d.identifier)
            d.state = 'DEAD'
            d.actual_mass = 0
            add_event(p, 'parachute off')
        else:
            mission_adv_log(_("device %s is turned off") % d.identifier)
            if device_is_engine(d.name) and not probe_device_type_is_turnedon(p, 'Engines'):
                add_event(p, 'engines off')

def probe_safe_mode(p):
    if p.safe_mode:
        terminate(p, 'noenergy', _("double safe mode!"))
    else:
        p.safe_mode = True
        for d in p.devices.device:
            if d.in_safe_mode == 'OFF':
                probe_turnoff_device(p, d)
            elif d.in_safe_mode == 'ON':
                probe_turnon_device(p, d)
            else:
                # do nothing!
                pass

def probe_process_commands(p, tick_length):
    stage = p.stage
    if p.python_program or not p.program:
        return
    for s in p.program.stage:
        if s.id == stage:
            stage_time = int(p.time - p.start_stage_time)
            turnoff_commands = []
            rest_commands = []
            for c in s.command:
                if 0 <= c.time - stage_time < tick_length:
                    if c.action == 'TURNOFF':
                        turnoff_commands.append(c)
                    else:
                        rest_commands.append(c)
            for c in turnoff_commands + rest_commands:
                device = probe_device_by_identifier(p, c.device)
                if device is None:
                    critical_error(p, _("cannot find device %s (stage %s, time %d, command %s)") %
                                   (c.device, stage, c.time, c.action))
                probe_do_command(p,
                                 device,
                                 c.action,
                                 c.argument)
            break

def probe_device_by_identifier(p, ident):
    for d in p.devices.device:
        if d.identifier == ident:
            return d
    return None

def probe_do_command(p, d, cmd, *other):
    mission_adv_log(_("%s: command %s with device %s%s") % (time_to_str(p.time - p.start_stage_time), # pylint: disable=C0301
                                                              cmd,
                                                              d.identifier,
                                                              (_(" param ") + str(other[0])) if cmd in ['PERIOD', 'ANGLE'] else '')) # pylint: disable=C0301
    if d.state == 'DEAD':
        mission_adv_log(_("command error: trying to activate dead device"))
    elif cmd == 'TURNON':
        probe_turnon_device(p, d)
    elif cmd == 'TURNOFF':
        probe_turnoff_device(p, d)
    elif cmd == 'PERIOD':
        period = int(other[0])
        if d.device.period_min <= period <= d.device.period_max:
            mission_adv_log(_("setting period to %d"), period)
            d.period = period
        else:
            mission_adv_log(_("error: period %d does not fit the device period limits [%d:%d]"),
                            period, d.device.period_min, d.device.period_max)
    elif cmd == 'ANGLE':
        if device_is_engine(d.name):
            angle = float(other[0])
            if abs(angle) <= MAX_ENGINE_ANGLE:
                d.angle = angle
            else:
                mission_adv_log(_("error: engine %s angle too large: %0.1f; max %0.1f allowed"),
                                d.identifier, angle, MAX_ENGINE_ANGLE)
        else:
            mission_adv_log(_("command error: trying to set angle for non-engine device %s"), d.identifier) # pylint: disable=C0301
    elif cmd == 'DROP STAGE':
        probe_drop_stage(p)
    else:
        critical_error(p, 'unknown command %s' % cmd)

def probe_landing(p):
    for d in p.devices.device:
        if (probe_device_is_turnedon(d) and (device_is_engine(d.name) or
                                             device_is_parachute(d.name))):
            mission_adv_log(_("turning off engine/parachute %s on landing") % d.identifier)
            probe_turnoff_device(p, d)
    add_event(p, 'landing')
    p.v_x = 0
    p.v_y = 0
    p.acceleration = p.acceleration_engine = p.acceleration_stokes = 0
    p.height = float(Planets[p.planet].radius)
    p.landed = True

def probe_orbit_reached(p):
    add_event(p, 'orbit reached')

def time_to_str(time):
    t = int(time) # round to sec
    hours = t / 3600
    minutes = (t % 3600) / 60
    seconds = (t % 3600) % 60
    return '%02d:%02d:%02d' % (hours, minutes, seconds)

def probe_send_message(p, msg):
    tel = probe_device_type_is_turnedon(p, 'Advanced diagnostics')
    # send telemetry to Earht no more than once per period
    if tel is None or p.time - p.last_user_log < tel.period:
        return
    trans = probe_device_type_is_turnedon(p, 'Transmitters')
    if trans and trans.transmitting and tel and tel.transmitting:
        mission_log(str(msg))
        p.last_user_log = p.time

def setup_diagnostics(p):
    stage = p.stage
    if stage == 'Landing':
        configobj = Config.Logging[p.mission].landing
    elif stage == 'Surface activity':
        configobj = Config.Logging[p.mission].surface_activity
    elif stage == 'Launch':
        configobj = Config.Logging[p.mission].launch
    else:
        critical_error(None, _("Cannot setup logs. Unknown stage %s") % stage)
    return configobj

def probe_diagnostics(p, tick_length): # pylint: disable=R0912
    global AD_messages #pylint: disable=W0603

    stage = p.stage

    def add_param(par, la, collector, value, logformat, logvalue=None):
        if la is not None:
            la.append(('%s=%s' % (par,
                                  logformat)) % (logvalue if logvalue else value)) # pylint: disable=W0631
        if collector is not None:
            collector[stage][par].append(value) # pylint: disable=W0631

    def append_parameters(param_string, logarr, needtime, col=None):  # pylint: disable=R0912
        for param in param_string.split(' '):
            if param == 'Ti' and needtime:
                add_param(param, logarr, col, p.time, '%s', time_to_str(p.time -
                                                                        p.start_stage_time))
            elif param == 'X':
                add_param(param, logarr, col, p.x, '%09.1f')
            elif param == 'Y':
                add_param(param, logarr, col, p.y, '%09.1f')
            elif param == 'H':
                add_param(param, logarr, col, p.height - float(Planets[p.planet].radius), '%08.1f')
            elif param == 'D':
                add_param(param, logarr, col, p.land_distance, '%08.1f')
            elif param == 'Vx':
                add_param(param, logarr, col, p.v_x, '%06.1f')
            elif param == 'Vy':
                add_param(param, logarr, col, p.v_y, '%07.1f')
            elif param == 'V':
                add_param(param, logarr, col, probe_velocity(p), '%07.1f')
            elif param == 'Vr':
                add_param(param, logarr, col, p.v_r, '%06.1f')
            elif param == 'Vt':
                add_param(param, logarr, col, p.v_t, '%07.1f')
            elif param == 'Ang':
                add_param(param, logarr, col, p.angle, '%04.1f')
            elif param == 'Ac':
                add_param(param, logarr, col, p.acceleration, '%05.1f')
            elif param == 'Ae':
                add_param(param, logarr, col, p.acceleration_engine, '%05.1f')
            elif param == 'As':
                add_param(param, logarr, col, p.acceleration_stokes, '%05.1f')
            elif param == 'Tg':
                add_param(param, logarr, col, p.T_gas, '%05.1f')
            elif param == 'PB':
                add_param(param, logarr, col, p.power_balance, '%03d')
            elif param == 'PG':
                add_param(param, logarr, col, p.power_generation, '%03d')
            elif param == 'PC':
                add_param(param, logarr, col, p.power_generation - p.power_balance, '%03d')
            elif param == 'ERs':
                add_param(param, logarr, col, p.energy_reserve, '%03.5f')
            elif param == 'BW':
                add_param(param, logarr, col, p.bandwidth / tick_length, '%02.1f/%02.1f',
                          (p.bandwidth / tick_length, p.total_bandwidth / tick_length))
            elif param == 'BWG':
                add_param(param, logarr, col, p.total_bandwidth / tick_length, '%02.1f')
            elif param == 'BWC':
                add_param(param, logarr, col, p.bandwidth / tick_length, '%02.1f')
            elif param == 'Te':
                add_param(param, logarr, col, p.T, '%05.1f')
            elif param == 'F':
                add_param(param, logarr, col,
                          probe_available_fuel(p, p.minimal_fuel_threshold * tick_length), '%05.1f')
            elif param == 'SI':
                add_param(param, logarr, col, p.scientific_information, '%05.1f')
            elif param == 'Datm':
                add_param(param, logarr, col,
                          planet_atmosphere_density(p.planet, float(p.height)), '%04.1f')
            elif param == 'Devs':
                devices = []
                for d in p.devices.device:
                    if d.state == 'ON':
                        state = '+'
                    elif d.state == 'OFF':
                        state = '-'
                    elif d.state == 'DEAD':
                        state = 'D'
                    else:
                        state = '?'
                    devices.append('{}{}'.format(d.identifier, state))
                logarr.append('Devs={}'.format(';'.join(devices)))

    if not stage in Collector:
        Collector[stage] = {}

    configobj = p.logconfig

    mission_base_log_string = configobj.mission_log.diagnostics
    mission_ext_log_string = configobj.mission_log.adv_diagnostics
    debug_log_string = configobj.debug_log
    short_log_string = configobj.short_log
    for s in short_log_string.split(' '):
        if s not in Collector[stage]:
            Collector[stage][s] = []

    parameters = []

        # trans = probe_device_type_is_turnedon(p, 'Transmitters')
        # if trans and trans.transmitting:
        #     tel = probe_device_type_is_turnedon(p, 'Base diagnostics')
        #     if tel:
        #         period = int(max(tick_length, tel.period))
        #         if tel.transmitting and (int(p.time) - p.last_transmit) >= period:
        #             append_parameters(mission_base_log_string, parameters, True)
        #             p.last_transmit = int(p.time)
        #     tel = probe_device_type_is_turnedon(p, 'Advanced diagnostics')
        #     if tel:
        #         period = int(max(tick_length, tel.period))
        #         if tel.transmitting and (int(p.time) - p.last_transmit_adv) >= period:
        #             need_time = len(parameters) == 0
        #             if not need_time:
        #                 parameters.append('AD:')
        #             append_parameters(mission_ext_log_string, parameters, need_time)
        #             p.last_transmit_adv = int(p.time)
        #             for ad in AD_messages:
        #                 mission_log('AD: ' + ad)
        #             AD_messages = []

    tel = p.base_diag
    if tel:
        period = int(max(tick_length, tel.period))
        if tel.transmitting and (int(p.time) - p.last_transmit) >= period:
            append_parameters(mission_base_log_string, parameters, True)
            p.last_transmit = int(p.time)
    tel = p.adv_diag
    if tel:
        period = int(max(tick_length, tel.period))
        if tel.transmitting and (int(p.time) - p.last_transmit_adv) >= period:
            need_time = len(parameters) == 0
            if not need_time:
                parameters.append('AD:')
            append_parameters(mission_ext_log_string, parameters, need_time)
            p.last_transmit_adv = int(p.time)
            for ad in AD_messages:
                mission_log('AD: ' + ad)
            AD_messages = []

    if len(parameters) > 0:
        mission_log(' '.join(parameters))

    parameters = []
    global last_debug_diagn #pylint: disable=W0603
    if int(p.time) - int(last_debug_diagn) >= Config.debug_diagn_period:
        last_debug_diagn = p.time
        append_parameters(debug_log_string, parameters, True)
        debug_log(' '.join(parameters))
        parameters = []
        append_parameters(short_log_string, parameters, True, Collector)

def custom_device(probe, d):
    if device_is_damper(d.name):
        if d.springs > d.device.max_springs:
            critical_error(probe, _("incorrect springs number in device %s, max %i allowed "),
                           d.identifier, d.device.max_springs)
        if d.springs_length > d.device.max_springs_length or d.springs_length <= 0:
            critical_error(probe, _("incorrect springs length in device %s, max %d allowed "),
                           d.identifier, d.device.max_springs_length)
        d.kHook = d.device.k_spring * d.springs
        d.actual_mass = d.springs * d.springs_length * d.device.m_spring
        #print "d.actual_mass", d.actual_mass, "d.kHook", d.kHook
        d.device.energy_compensation = 0 # TODO: make model working!!!
    else:
        critical_error(probe, _("incorrect custom device %s "), d.name)

def probe_load(name, probefile):  # pylint: disable=R0912
    global last_debug_diagn #pylint: disable=W0603
    last_debug_diagn = 0.0
    xmldata = read_xml_file(probefile)
    probe = None
    try:
        probe = venus.probe.CreateFromDocument(xmldata)
        probe.mission = probe.flight.mission.name
        mission_params = Parameters.Missions[probe.mission]
        planet_params = Planets[mission_params.planet]
        probe.stage = 'Landing'
        probe.filename = name
        probe.planet = planet_params.name

        if hasattr(probe.flight, 'time') and probe.flight.time is not None:
            probe.start_time = probe.flight.time.start
        else:
            probe.start_time = ''
        if not hasattr(probe.flight, 'cycle_time') or probe.flight.cycle_time is None:
            probe.flight.cycle_time = 0
        probe.scientific_information = 0.0
        probe.landing_velocity = 0.0
        probe.time = 0.0
        probe.events = []
        probe.landed = False
        #external flight parameters
        probe.height = float(planet_params.radius) + float(probe.flight.start_height)
        probe.start_height = float(probe.flight.start_height)
        if (hasattr(mission_params, 'launch') and hasattr(mission_params.launch,
                                                          'target_distance')):
            if getattr(probe.flight, 'target_distance', None) is not None:
                mission_params.launch.target_distance = probe.flight.target_distance
            if mission_params.launch.target_distance > (pi * Planets[probe.planet].radius / 2): # pylint: disable=C0301
                critical_error(probe, _("error decoding probe %s. target distance %d is too large") % (probefile, # pylint: disable=C0301
                                                                                                         mission_params.launch.target_distance)) # pylint: disable=C0301
        probe.device_volume = 0.0
        probe.minimal_fuel_threshold = 999999.0
        probe.scientific_devices = {}
        probe.cpus = []
        probe.has_absorber = probe.parameters.absorber == 'ON'
        probe.has_isolator = probe.parameters.absorber == 'ON'
        probe.current_stage = 1
        if not hasattr(probe.parameters, 'radius_internal'):
            probe.parameters.radius_internal = probe.parameters.radius_external# - 0.001
        probe.total_length = probe.parameters.radius_external
        if hasattr(probe.contruction, 'stage'):
            i = 0
            for s in probe.contruction.stage:
                i += 1
                if int(s.number) != i:
                    critical_error(probe, _("error decoding probe %s. wrong stage order of %s") % (probefile, s.name)) # pylint: disable=C0301
                probe_stage_load(s, mission_params)
                probe.total_length += s.length

        for d in probe.devices.device:
            if d.name not in Devices:
                critical_error(probe, _("error decoding probe %s. unknown device %s") % (probefile, d.name)) # pylint: disable=C0301
            d.device = Devices[d.name]
            if not is_device_allowed(probe, d.name):
                critical_error(probe, _("device %s is not available in mission %s"),
                               d.name, probe.mission)
            d.identifier = d.device.code + str(d.number)
            if getattr(d.device, "custom"):
                custom_device(probe, d)
            else: # normal device params
                d.actual_mass = float(d.device.mass)
            if d.stage is not None:
                try:
                    s = probe.contruction.stage[int(d.stage) - 1]
                    s.device_volume += float(d.device.volume)
                except Exception: # pylint: disable=W0703
                    critical_error(probe, _("error decoding probe %s. wrong stage of device %s %s; stage %s does not exist") % (probefile, d.name, d.number, d.stage)) # pylint: disable=C0301
            else:
                # payload device
                probe.device_volume += float(d.device.volume)
            d.state = d.start_state
            if device_is_fueltank(d.name):
                d.available_fuel = float(d.device.mass)
            if device_is_engine(d.name):
                if probe.minimal_fuel_threshold > d.device.traction:
                    probe.minimal_fuel_threshold = float(d.device.traction)
            if device_is_accumulator(d.name):
                d.available_energy = d.device.capacity
                d.accumulator_type = True # optimisation
            else:
                d.accumulator_type = False
            if device_is_transmitter(d.name): #optimisation
                d.transmitter_type = True
            else:
                d.transmitter_type = False
            d.period = d.device.period_min
            d.transmitting = d.prev_transmitting = False
            if device_is_scientific(d.name) and d.name not in probe.scientific_devices:
                probe.scientific_devices[d.name] = float(d.device.scientific_limit)
            if d.name == "cpu":
                probe.cpus.append(d)
        probe.start_fuel = probe_fuel_total(probe)
        # do checks
        has_hs = False
        for d in probe.devices.device:
            if device_is_engine(d.name):
                d.angle = 0
                if probe.minimal_fuel_threshold > d.device.traction:
                    probe.minimal_fuel_threshold = float(d.device.traction)
                if d.state == 'ON' and probe_device_type_is_turnedon(probe, 'Engines') == d:
                    add_event(probe, 'engines on')
            if device_is_parachute(d.name):
                if d.state == 'ON':
                    parachutes = []
                    for dev in probe.devices.device:
                        if (device_is_parachute(dev.name) and probe_device_is_turnedon(dev)):
                            parachutes.append(dev.identifier)
                    if len(parachutes) > 1:
                        critical_error(probe, _("more than one parachutes (%s) turned on from the beginning"), # pylint: disable=C0301
                                       ', '.join(parachutes))
                if float(d.device.thermal_protection) > 0:
                    if not has_hs:
                        has_hs = True
                        if d.state == 'ON':
                            add_event(probe, 'parachute on hs')
                        else:
                            critical_error(probe, _("the heatshield %s should be turned on from the beginning"), # pylint: disable=C0301
                                           d.name)
                    else:
                        critical_error(probe, _("there are more than one heatshield %s installed"),  # pylint: disable=C0301
                                       d.name)
                else:
                    if d.state == 'ON':
                        add_event(probe, 'parachute on')
        probe.heat_transmission_surface = 4.0 * pi * (float(probe.parameters.radius_external) ** 2)
        external_volume = (4.0 * pi / 3.0) * (float(probe.parameters.radius_external) ** 3)
        probe.internal_volume = (4.0 * pi / 3.0) * (float(probe.parameters.radius_internal) ** 3)
        probe.construction_mass = probe.internal_volume * float(mission_params.construction.density)
        if probe.has_isolator:
            probe.isolator_volume = external_volume - probe.internal_volume
            probe.isolator_mass = probe.isolator_volume * float(mission_params.isolator.density)
        else:
            probe.isolator_volume = 0
            probe.isolator_mass = 0
        if probe.has_absorber:
            probe.absorber_volume = probe.internal_volume - probe.device_volume
            probe.absorber_mass = probe.absorber_volume * float(mission_params.absorber.density)
            probe.hard_absorber_mass = probe.absorber_mass
            probe.absorber_state = mission_params.absorber.state
        else:
            probe.absorber_volume = 0
            probe.absorber_mass = 0
            probe.hard_absorber_mass = 0
            probe.absorber_state = 'none'
        probe_update_total_mass(probe)
        probe.x = 0.0
        if not hasattr(probe.flight, 'start_height'):
            critical_error(probe, _("probe %s has no start_height flight parameter") % probefile) # pylint: disable=C0301
        probe.v_x = (sqrt(float(Parameters.G) * float(planet_params.mass) /
                          float(planet_params.radius)) *
                     float(mission_params.start_braking_koeff))
        probe.v_y = 0.0
        probe.friction_square = probe_update_friction_square(probe)
        probe.safe_mode = False
        probe_update_power_balance(probe, 0)
        probe.last_transmit = 0.0
        probe.last_transmit_adv = 0.0
        probe.angle = 0.0
        probe.T = float(mission_params.T_start)
        probe.T_gas = 0.0
        probe.bandwidth = 0.0
        probe.total_bandwidth = 0.0
        probe.start_stage_time = 0.0
        probe.acceleration = 0.0
        probe.acceleration_engine = 0.0
        probe.acceleration_stokes = 0.0
        probe.max_acceleration = 0.0
        probe.safe_mode = False
        probe.start_total_mass = probe.total_mass
        probe.last_user_log = 0.0
        probe.tick_length = 0
        probe.base_diag = False
        probe.adv_diag = False
        if probe.python_code is not None:
            probe.python_program = str(probe.python_code).split('\n')
        else:
            probe.python_program = None
    except pyxb.BadDocumentError as e:
        critical_error(None, _("Cannot load probe %s: bad xml-document") % name)
    except pyxb.ValidationError as e:
        critical_error(None, _("Cannot load probe %s: error %s in %s") % (name,
                                                                            str(e),
                                                                            e.location))
    else:
        debug_log('')
        debug_parameters(probe.mission, probe.planet)
        debug_config(probe.mission)
        debug_log('')
        debug_log(_("Probe %s was loaded successfully."), name)
        debug_probe(probe, mission_log)
        debug_probe(probe, debug_log)
        debug_log('')

        # check correctness of the probe and the mission limits
        cpu_found = False
        for d in probe.devices.device:
            if d.name == 'cpu':
                cpu_found = True
                break
        if not cpu_found:
            probe.started = False
            critical_error(probe, _("No CPU device found"))
        if probe.parameters.radius_internal > probe.parameters.radius_external:
            probe.started = False
            critical_error(probe, _("probe error: probe internal radius %.3f m should not be more than external radius %.3f m"),  # pylint: disable=C0301
                           probe.parameters.radius_internal, probe.parameters.radius_external)
        if probe.parameters.radius_external > mission_params.max_radius:
            probe.started = False
            critical_error(probe, _("probe error: probe radius %.3f m is greater than size limit %.3f m"),  # pylint: disable=C0301
                           probe.parameters.radius_external, mission_params.max_radius)
        if probe.total_length > mission_params.max_length:
            probe.started = False
            critical_error(probe, _("probe error: probe length %.3f m is greater than size limit %.3f m"),  # pylint: disable=C0301
                           probe.total_length, mission_params.max_length)
        if probe.device_volume > probe.internal_volume:
            probe.started = False
            critical_error(probe, _("probe error: total devices volume %.3f m^3 is greater than internal volume %.3f m^3"),  # pylint: disable=C0301
                           probe.device_volume, probe.internal_volume)
        if probe.contruction is not None:
            for s in probe.contruction.stage:
                if s.internal_volume < s.device_volume:
                    probe.started = False
                    critical_error(probe, _('probe error: stage "%s" devices volume %.3f m^3 is greater than internal volume %.3f m^3'),  # pylint: disable=C0301
                                   s.name, s.device_volume, s.internal_volume)
                if s.radius > mission_params.max_radius:
                    probe.started = False
                    critical_error(probe, _('probe error: probe stage "%s" radius %.3f m is greater than size limit %.3f m'),  # pylint: disable=C0301
                                   s.name, s.radius, mission_params.max_radius)
        if probe.total_mass > mission_params.max_mass:
            probe.started = False
            critical_error(probe, _("probe error: probe total mass %.3f kg is greater than mass limit %.3f kg"),  # pylint: disable=C0301
                           probe.total_mass, mission_params.max_mass)
        probe.started = True
    return probe

def debug_device(name):
    d = Devices[name]
    debug_log(_("Device name %s, code %s"),
              str(d.name), str(d.code))

def debug_parameters(mission, planet):
    debug_log(_("Global parameters:"))
    debug_log(_("\tG: %.4e kg m^3 / (c^2)"), Parameters.G)
    p = Planets[planet]
    m = Parameters.Missions[mission]
    debug_log(_("\tMission: %s"), mission)
    debug_log(_("\tPlanet: %s"), planet)
    debug_log(_("\t\tRadius: %.4f m,"), p.radius)
    debug_log(_("\t\tMass: %.4e kg"), p.mass)
    debug_log(_("\t\tAtmosphere height: %.2f m"), p.atmosphere.height)
    debug_log(_("\t\tAtmosphere border: %.2f m"),
              planet_atmosphere_border(planet, float(p.atmosphere.density_border)) -
              float(p.radius))
    debug_log(_("\t\tGround temperature: %.2f K"), p.atmosphere.T_ground)
    debug_log(_("\t\tGround pressure: %.2f Pa"), p.atmosphere.P_ground)
    debug_log(_("\t\tStart braking koeff: %.2f"), m.start_braking_koeff)
    debug_log(_("\t\tMax acceleration: %.2f"), m.max_acceleration)

def debug_config(mission):
    debug_log(_("Global config:"))
    debug_log(_("\tLogging"))
    debug_log(_("\t\tMission: %s"), mission)
    if getattr(Config.Logging[mission], "landing", None) is not None:
        debug_log(_("\t\t\tLanding:"))
        debug_log(_("\t\t\t\tMission log:"))
        debug_log(_("\t\t\t\t\tDiagnostics: %s"),
                  Config.Logging[mission].landing.mission_log.diagnostics)
        debug_log(_("\t\t\t\t\tAdv. Diagnostics: %s"),
                  Config.Logging[mission].landing.mission_log.adv_diagnostics)
        debug_log(_("\t\t\t\tDebug log: %s"),
                  Config.Logging[mission].landing.debug_log)
    else:
        debug_log(_("\t\t\tLanding log undefined"))
    if getattr(Config.Logging[mission], "surface_activity", None) is not None:
        debug_log(_("\t\t\tSurface activity:"))
        debug_log(_("\t\t\t\tMission log:"))
        debug_log(_("\t\t\t\t\tDiagnostics: %s"),
                  Config.Logging[mission].surface_activity.mission_log.diagnostics)
        debug_log(_("\t\t\t\t\tAdv. Diagnostics: %s"),
                  Config.Logging[mission].surface_activity.mission_log.adv_diagnostics)
        debug_log(_("\t\t\t\tDebug log: %s"),
                  Config.Logging[mission].surface_activity.debug_log)
    else:
        debug_log(_("\t\t\tSurface activity log undefined"))

def debug_probe(probe, logger=mission_log):
    mission_params = Parameters.Missions[probe.mission]
    planet_params = Planets[mission_params.planet]
    logger(_("Probe %s:"), str(probe.name))
    logger(_("\tTeam: %s"), str(probe.team))
    logger(_("\tTournament: %s"), str(probe.tournament))
    if getattr(Config.Logging[probe.mission], "debug_constants", "") != "NO":
        logger(_("\tConstant parameters:"))
        logger(_("\t\tConstruction density: %.4f kg / m^3"),
               mission_params.construction.density)
        if probe.has_isolator:
            logger(_("\t\tIsolator:"))
            logger(_("\t\t\tK: %.4f W / (m K)"), mission_params.isolator.k)
        if probe.has_absorber:
            logger(_("\t\tAbsorber:"))
            logger(_("\t\t\tState: %s"), str(mission_params.absorber.state))
            logger(_("\t\t\tDensity: %s kg / m^3"), str(mission_params.absorber.density))
            logger(_("\t\t\tMelting temperature: %s К"), str(mission_params.absorber.T_melting))
            logger(_("\t\t\tL: %s J / kg"), str(mission_params.absorber.L))
            logger(_("\t\t\tC (hard): %s J / (kg K)"), str(mission_params.absorber.C_hard))
            logger(_("\t\t\tC (liquid): %s J / (kg K)"), str(mission_params.absorber.C_liquid))
        logger(_("\t\tStart temperature: %.1f K"), mission_params.T_start)
        if is_model_on(probe, 'stokes'):
            logger(_("\t\tAerodynamic factor: %.3f"), mission_params.aerodynamic_coeff)
        logger(_("\tBase parameters:"))
        logger(_("\t\tExternal radius: %.3f m"), probe.parameters.radius_external)
        logger(_("\t\tInternal radius: %.3f m"), probe.parameters.radius_internal)
        logger(_("\tFlight parameters:"))
        logger(_("\t\tPlanet: %s"), probe.planet)
        logger(_("\t\tStart time: %s"), probe.start_time)
        logger(_("\t\tStart X: %.4f m"), probe.x)
        logger(_("\t\tStart height (Y): %.4f m"), probe.height - float(planet_params.radius))
        logger(_("\tDevices:"))
        for d in probe.devices.device:
            # debug_device(d.code, '\t\t')
            logger(_("\t\tDevice %s, identifier %s, start state %s") %
                   (str(d.device.name), str(d.identifier), str(d.start_state)))
    if probe.python_program:
        logger(_("\tProgram (python):"))
        logger(('\t\t' + '\n\t\t'.join(probe.python_program)).replace('%', '%%'))
    elif probe.program:
        logger(_("\tProgram:"))
        for s in probe.program.stage:
            logger(_("\t\tStage %s:"), s.id)
            for c in s.command:
                logger(_("\t\t\tTime %03d device %s command %s"), c.time, c.device, c.action)
    else:
        logger(_("\tNo program"))
    if getattr(Config.Logging[probe.mission], "debug_probe", "") != "NO":
        logger(_("\tDerived parameters:"))
        if probe.has_isolator:
            logger(_("\t\tIsolator mass: %.4f kg"), probe.isolator_mass)
            logger(_("\t\tIsolator volume: %.4f m^3"), probe.isolator_volume)
        logger(_("\t\tConstruction mass: %.4f kg"), probe.construction_mass)
        logger(_("\t\tDevice mass: %.4f kg"), probe.device_mass)
        logger(_("\t\tDevice volume: %.4f m^3"), probe.device_volume)
        logger(_("\t\tFuel: %.1f kg"), probe.start_fuel)
        logger(_("\t\tHeat transmission surface: %.4f m^2"), probe.heat_transmission_surface)
        logger(_("\t\tFriction square: %.4f m^2"), probe.friction_square)
        logger(_("\t\tInternal volume: %.4f m^3"), probe.internal_volume)
        if probe.has_absorber:
            logger(_("\t\tAbsorber volume: %.4f m^3"), probe.absorber_volume)
            logger(_("\t\tAbsorber mass: %.4f kg"), probe.absorber_mass)
        logger(_("\t\tTotal mass: %.4f kg"), probe.total_mass)
        logger(_("\t\tStart velocity (X): %.4f m/s"), probe.v_x)
        logger(_("\t\tStart velocity (Y): %.4f m/s"), probe.v_y)
        logger(_("\t\tPower balance: %.4f * 10W"), probe.power_balance)
        logger(_("\t\tScientific information: %.4f kbit"), probe.scientific_information)
    logger('\n'+_("Flight telemetry:"))

def add_event(probe, msg):
    probe.events.append((probe.time, msg, probe.landed))

def critical_error(probe, *e):
    error_log(*e)
    msg = e[0] % e[1:] if len(e) > 0 else ''
    if probe:
        if hasattr(probe, 'started') and not probe.started:
            write_short_log(probe, 'notstarted', msg)
        else:
            write_short_log(probe, 'error', msg)
    raise CriticalError(msg)

def terminate(probe, reason, message):
    debug_log(_("PROBE TERMINATED"))
    debug_log("Ti=%s", time_to_str(probe.time))
    debug_log(message)
    mission_log(_("Total scientific information: %.4f kbit"), probe.scientific_information)
    debug_log(_("Total scientific information: %.4f kbit"), probe.scientific_information)
    debug_log(_("Unused scientific limits:"))
    for d, si in probe.scientific_devices.items():
        debug_log("\t%s\t%.1f", d, si)
    add_event(probe, 'terminated')
    write_short_log(probe, 'terminated', reason)
    imagetmpl = get_image_template()
    if imagetmpl:
        draw_images(probe, probe.stage, imagetmpl)
    raise Terminated(message)

def write_short_log(probe, result, reason='unknown'):  # pylint: disable=R0912
    mission_params = Parameters.Missions[probe.mission]
    planet_params = Planets[mission_params.planet]

    parameters = {}
    parameters['name'] = probe.name
    parameters['planet'] = probe.planet
    if len(probe.start_time) > 0:
        parameters['starttime'] = probe.start_time
    parameters['realtime'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    parameters['missiontime'] = str(probe.time)
    parameters['startmass'] = '%.1f' % getattr(probe, 'start_total_mass', -1)
    parameters['startheight'] = '%.1f' % probe.start_height
    parameters['events'] = {}
    parameters['events']['Landing'] = []
    parameters['landingvelocity'] = '%1.f' % probe.landing_velocity
    parameters['surfacetime'] = 0
    parameters['result'] = result
    if probe.stage == 'Surface activity':
        parameters['result'] = 'termonsurface'
        parameters['surfacetime'] = str(probe.time - probe.start_stage_time)
        if hasattr(mission_params, 'score') and (mission_params.score and
                                                 mission_params.score != 'si'):
            assert mission_params.score == 'si_per_m'
            parameters['score'] = '%.1f' % (1000.0 * probe.scientific_information /
                                            probe.start_total_mass)
        else:
            parameters['score'] = '%.1f' % probe.scientific_information
        parameters['scientificinformation'] = '%.1f' % probe.scientific_information
        parameters['events']['Surface activity'] = []
        for e in probe.events:
            if not e[2]:
                parameters['events']['Landing'].append((str(e[0]), e[1]))
            else:
                parameters['events']['Surface activity'].append((str(e[0]), e[1]))
    elif probe.stage == 'Landing':
        for e in probe.events:
            parameters['events']['Landing'].append((str(e[0]), e[1]))
    elif probe.stage == 'Launch':
        if "reach_height" in mission_params.result_criteria:
            if reason == "height limit":
                parameters['result'] = "height reached"
        if "fuel_used" in mission_params.result_criteria:
            parameters['fuel_used'] = probe_fuel_used(probe)
        if "hit_target" in mission_params.result_criteria:
            accuracy = abs(probe.land_distance - mission_params.launch.target_distance)
            r_accuracy = accuracy/mission_params.launch.target_distance
            if reason == "crashed":
                if mission_params.launch.accuracy is None:
                    mission_params.launch.accuracy = 0.5 #default 50%
                if r_accuracy <= mission_params.launch.accuracy:
                    reason = "hit target"
                else: reason = "miss target"
            parameters['hit_accuracy'] = accuracy
            parameters['relative_accuracy'] = '%.3f' % r_accuracy
        parameters['events']['Launch'] = []
        for e in probe.events:
            parameters['events']['Launch'].append((str(e[0]), e[1]))
    parameters['reason'] = reason
    parameters['image'] = []
    parameters['data'] = []
    if probe.team is not None:
        parameters['team'] = probe.team
    else:
        parameters['team'] = ''
    if probe.tournament is not None:
        parameters['torunament'] = probe.tournament
    else:
        parameters['tournament'] = ''

    hlimit = float(planet_params.atmosphere.height) + 10000.0
    parameters['limits'] = {}
    parameters['limits']['h'] = hlimit

    g = sqrt(float(Parameters.G) * float(planet_params.mass) /
             (float(planet_params.radius) + hlimit) ** 2)
    t = sqrt(2 * hlimit / g)
    v_x = (sqrt(float(Parameters.G) * float(planet_params.mass) / float(planet_params.radius)) *
           float(mission_params.start_braking_koeff))
    x = v_x * t
    parameters['limits']['x'] = x

    def print_stage(parameters, stage):
        if stage == 'Landing':
            configobj = Config.Logging[probe.mission].landing
        elif stage == 'Surface activity':
            configobj = Config.Logging[probe.mission].surface_activity
        elif stage == 'Launch':
            configobj = Config.Logging[probe.mission].launch

        imgtmpl = get_image_template()
        if imgtmpl is not None:
            for img in configobj.image:
                if stage not in Collector or (len(Collector[stage]) == 0 or
                                              'Ti' not in Collector[stage] or
                                              len(Collector[stage]['Ti']) < 2):
                    parameters['image'].append((stage, img.params, Config.logging.empty_image))
                else:
                    imagefile = '%s%s-%s-%s.png' % (imgtmpl, probe.filename, stage,
                                                    img.params.replace(' ', '-'))
                    found = False
                    for i in range(len(parameters['image'])):
                        if parameters['image'][i][1] == img.params:
                            parameters['image'][i] = (stage, img.params, imagefile)
                            found = True
                            break
                    if not found:
                        parameters['image'].append((stage, img.params, imagefile))
        if stage not in Collector or (len(Collector[stage]) == 0 or
                                      'Ti' not in Collector[stage] or
                                      len(Collector[stage]['Ti']) < 2):
            return
        string = (':'.join(configobj.short_log.split(' '))) + "\n"
        maxt = len(Collector[stage]['Ti']) - 1
        for i in range(Config.logging.short_log_len + 1):
            tindex = int(float(i) * float(maxt) / Config.logging.short_log_len)
            assert 0 <= tindex <= maxt
            line = []
            for s in configobj.short_log.split(' '):
                line.append('%010.3f' % Collector[stage][s][tindex])
            string += ':'.join(line) + "\n"
        parameters['data'].append((stage, string))

    if result not in ('error', 'notstarted'):
        print_stage(parameters, probe.stage)

    #if probe.stage != 'Landing': print_stage(parameters, probe.stage)

    short_log_xml(parameters)
    html_log(parameters)

def draw_images(probe, stage, imgtmpl):
    if stage not in Collector or (len(Collector[stage]) == 0 or
                                  'Ti' not in Collector[stage] or
                                  len(Collector[stage]['Ti']) < 2):
        return
    if stage == 'Landing':
        configobj = Config.Logging[probe.mission].landing
    elif stage == 'Launch':
        configobj = Config.Logging[probe.mission].launch
    else:
        assert stage == 'Surface activity'
        configobj = Config.Logging[probe.mission].surface_activity
    for img in configobj.image:
        imagefile = '%s%s-%s-%s.png' % (imgtmpl, probe.filename, stage,
                                        img.params.replace(' ', '-'))
        ylimits = ['calc', 'calc']
        if hasattr(img, 'ymin') and img.ymin is not None:
            ylimits[0] = float(img.ymin)
        if hasattr(img, 'ymax') and img.ymax is not None:
            ylimits[1] = float(img.ymax)
        if img.params.find(' ') == -1:
            if img.params == 'Te' and stage == 'Surface activity':
                plot_graph(Collector['Landing']['Ti'] + Collector['Surface activity']['Ti'],
                           Collector['Landing']['Te'] + Collector['Surface activity']['Te'],
                           img.label, imagefile, ylimits)
            else:
                plot_graph(Collector[stage]['Ti'], Collector[stage][img.params], img.label,
                           imagefile, ylimits)
        else:
            values = []
            for p in img.params.split(' '):
                values.append(Collector[stage][p])
            plot_graph(Collector[stage]['Ti'], values, img.label, imagefile, ylimits, True)

def planet_atmosphere_temperature(planet, h):
    planet_params = Planets[planet]
    h2 = h - float(planet_params.radius)
    if h2 <= 0:
        return float(planet_params.atmosphere.T_ground) + 273.03
    t = (float(planet_params.atmosphere.T_ground) -
         float(planet_params.atmosphere.T_grad) * (h2 / 1000.0))
    if t < -270:
        t = -270
    return t + 273

def planet_atmosphere_density(planet, h):
    #    return 67.0 * (venus_radius + atmosphere_height - h) / atmosphere_height
    #    return 67.0 / 2
    planet_params = Planets[planet]
    if h < planet_params.radius:
        return float(planet_params.atmosphere.P_ground)
    return float(planet_params.atmosphere.P_ground) * exp((float(planet_params.radius) - h) /
                                                          float(planet_params.atmosphere.P_coeff))

def planet_atmosphere_border(planet, density):
    if density == 0:
        density = 0.00000000000001
    planet_params = Planets[planet]
    if planet_params.atmosphere.P_ground == 0:
        return 0
    return (float(planet_params.radius) -
            float(planet_params.atmosphere.P_coeff) * log(density /
                                                          float(planet_params.atmosphere.P_ground)))

def planet_sunlight(planet, time, start_time):
    planet_params = Planets[planet]
    day = planet_params.period / 2.0
    t = time + start_time
    pr = t // day
    return int((pr % 2) == 0)
