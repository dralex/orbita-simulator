# -----------------------------------------------------------------------------
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# The Orbita Simulator
# The simple gravity calculation model
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
import gettext
from math import exp, sqrt
import pyxb

import venus.global_parameters
import venus.global_config
import venus.planets

from logger import debug_log, error_log, load_log_language
from errors import CriticalError

LOCAL_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_LANG = 'en'
PARAMETERS_FILE = os.path.join(LOCAL_DIR, 'parameters{}.xml')
CONFIG_FILE = os.path.join(LOCAL_DIR, 'config{}.xml')
PLANETS_FILE = os.path.join(LOCAL_DIR, 'planets.xml')

_ = gettext.gettext
Parameters = None
Config = None
Planets = None

def critical_error(*e):
    error_log(*e)
    msg = e[0] % e[1:] if len(e) > 0 else ''
    raise CriticalError(msg)

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

def read_xml_file(f):
    return open(f).read()

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
                critical_error(_("Cannot decode parameters. Similar missions names: {}").format(p.name)) # pylint: disable=C0301
            p.Models = p.models.split(',')
            tmp = p.devices.replace('\n', '').replace(' ', '').replace('\t', '')
            p.Devices = tmp.split(',')
            Parameters.Missions[p.name] = p
            p.result_criteria = p.result.split(',')
            if p.max_length is None:
                p.max_length = p.max_radius #no stages allowed
    except pyxb.BadDocumentError as e:
        critical_error(_("Cannot load parameters: bad xml document"))
    except pyxb.ValidationError as e:
        critical_error(_("Cannot load parameters: error in %s") % e.location)
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
                critical_error(_("Cannot decode planets. Similar planets names: {}").format(p.name)) # pylint: disable=C0301
            Planets[p.name] = p
            if p.rotation is not None:
                p.period = (p.rotation.hours * 60 + p.rotation.minutes)*60 + p.rotation.seconds
            else:
                p.period = 99999999.0 # TODO cast error here
    except pyxb.BadDocumentError as e:
        critical_error(_("Cannot load planets: bad xml document"))
    except pyxb.ValidationError as e:
        critical_error(_("Cannot load planets: error in %s") % e.location)
    else:
        debug_log(_("Planets loaded successfully."))

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
                critical_error(_("Cannot decode config. Similar mission names: %s") % m.name) # pylint: disable=C0301
            Config.Logging[m.name] = m
        Config.debug_diagn_period = float(Config.logging.debug_diagn_period)
    except pyxb.BadDocumentError as e:
        critical_error(_("Cannot load config: bad xml document"))
    except pyxb.ValidationError as e:
        critical_error(_("Cannot load config: error in %s") % e.location)
    else:
        debug_log(_("Config loaded successfully."))

def planet_atmosphere_density(planet, h):
    #    return 67.0 * (venus_radius + atmosphere_height - h) / atmosphere_height
    #    return 67.0 / 2
    planet_params = Planets[planet]
    if h < planet_params.radius:
        return float(planet_params.atmosphere.P_ground)
    return float(planet_params.atmosphere.P_ground) * exp((float(planet_params.radius) - h) /
                                                          float(planet_params.atmosphere.P_coeff))

def time_to_str(time):
    t = int(time) # round to sec
    hours = t / 3600
    minutes = (t % 3600) / 60
    seconds = (t % 3600) % 60
    return '%02d:%02d:%02d' % (hours, minutes, seconds)

def probe_velocity(p):
    return sqrt(p.v_x ** 2 + p.v_y ** 2)
