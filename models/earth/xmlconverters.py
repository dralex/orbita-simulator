# -----------------------------------------------------------------------------
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# The Orbita Simulator
# The Earth orbit simulation model (v2)
#
# XML data file parsers and generators
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

import random
from os.path import isfile
from collections import deque
from xml.sax.saxutils import escape

import pyxb
import venus.probe
import venus.devices
import venus.global_parameters
import venus.global_config
import venus.missions
import venus.shortlog

from logger import logging
from errors import CriticalError
from language import Language
from utils import generate_bytes

_ = Language.get_tr()

def read_xml_file(f):
    return open(f).read()

xml_escape_table = {'"': "&quot;", "'": "&apos;"}

def xml_escape(text):
    return escape(text, xml_escape_table)

class XMLLoader:

    ORIGIN = None
    XML_FILE = None

    @classmethod
    def load(cls, lang, xml_file=None):
        try:
            _ = lang.get_tr()
            if xml_file is None:
                xml_file = cls.XML_FILE
            xmldata = read_xml_file(xml_file)
        except IOError:
            raise CriticalError(_("XML Error. Cannot load %s: cannot open file %s") %
                                (cls.ORIGIN, xml_file))
        try:
            return cls.decode(xmldata)
        except pyxb.BadDocumentError as e:
            raise CriticalError(_("XML Error. Cannot load %s: bad xml-document %s: %s") %
                                (cls.ORIGIN, xml_file, str(e)))
        except pyxb.ValidationError as e:
            raise CriticalError(_("XML Error. Cannot load %s: bad xml-документ %s: error in %s") %
                                (cls.ORIGIN, xml_file, str(e.location)))
        except pyxb.PyXBException:
            raise CriticalError(_("XML Error. Cannot load %s: bad xml document %s") %
                                (cls.ORIGIN, xml_file))

    @classmethod
    def decode(cls, xmldata): # pylint: disable=W0613
        return None

class GlobalParameters(XMLLoader):

    ORIGIN = _('parameters')
    XML_FILE = "parameters.xml"

    def __init__(self):
        self.Planets = {}
        self.G = None
        self.Orbasic = None

    @classmethod
    def decode(cls, xmldata):
        xml = venus.global_parameters.CreateFromDocument(xmldata)
        params = GlobalParameters()
        params.G = xml.G
        params.Orbasic = xml.orbasic
        for p in xml.planets.planet:
            if p.name in params.Planets:
                raise CriticalError(_("XML Error. Cannot load %s: there are two planets with the same name %s") % # pylint: disable=C0301
                                    (cls.ORIGIN, p.name))
            p.Models = {}
            for m in p.models.model:
                p.Models[m.order] = (m.kind, m.modelclass)
            p.Models = [p.Models[order] for order in sorted(p.Models.keys())]
            params.Planets[p.name] = p
            p.Atmosphere = None
        return params

    def debug_parameters(self, planet, logger):
        logger(_('Global Parameters:'))
        logger(_('\tG: %.4e kg m^3 / sec^2'), self.G)
        p = self.Planets[planet]
        logger(_('\tPlanet: %s'), planet)
        logger(_('\t\tRadius: %.4f км,'), p.radius / 1000.0)
        logger(_('\t\tMass: %.4e кг'), p.mass)
        logger(_('\tConstruction limits:'))
        logger(_('\t\tMax mass: %.2f кг'), p.probe.max_mass)

class GlobalConfig(XMLLoader):

    ORIGIN = _('config')
    XML_FILE = "config.xml"

    def __init__(self):
        self.BallisticsParams = {}

    @classmethod
    def decode(cls, xmldata):
        xml = venus.global_config.CreateFromDocument(xmldata)
        config = GlobalConfig()
        for p in xml.ballistics_model.config_parameter:
            if p.name in config.BallisticsParams:
                raise CriticalError(_("XML Error. Cannot load %s: there are two parameters with the same name %s") % # pylint: disable=C0301
                                    (cls.ORIGIN, p.name))
            config.BallisticsParams[p.name] = {'full_name': p.full_name,
                                               'unit': p.unit,
                                               'required': p.required}
        return config

    @classmethod
    def generate_testmodel_xml(cls, name, planet, params):
        """
        Function to generate the testmodel xml document. Arguments:

        NAME		TYPE		DESCRIPTION
	name		str		name of the modeling calculation
        planet		str		planet ('Earth')
        params		dict		calculation parameters
		params['param name'] = param value
        """
        result = '<?xml version="1.0" encoding="utf-8"?>\n'
        result += '<v:testmodel name="%s" planet="%s" xmlns:v="venus">\n' % (name, planet)
        for pname in sorted(params.keys()):
            pvalue = params[pname]
            result += '\t<%s>%f</%s>\n' % (pname, float(pvalue), pname)
        result += '</v:testmodel>\n'
        return result

class Missions(XMLLoader):

    ORIGIN = _('missions')
    XML_FILE = "missions.xml"

    def __init__(self):
        self.Miss = {}
        self.parameters = {}

    @classmethod
    def decode(cls, xmldata):
        xml = venus.missions.CreateFromDocument(xmldata)
        missions = Missions()
        for m in xml.mission_list.mission:
            if m.name in missions.Miss:
                raise CriticalError(_("XML Error. Cannot load %s: there are two missions with the same name %s") % # pylint: disable=C0301
                                    (cls.ORIGIN, m.name))
            if hasattr(m, 'test') and m.test is not None and m.test:
                m.is_test = True
            else:
                m.is_test = False
            if hasattr(m, 'default') and m.default is not None:
                m.has_default = True
            else:
                m.has_default = False
            missions.Miss[m.name] = m
        for p in xml.generation.parameter:
            missions.parameters[p.name] = {'full_name': _(p.full_name),
                                           'unit': _(p.unit)}
        return missions

    def generate_mission(self, name):
        g = self.Miss[name].generator
        result = {}
        csnames = []
        csvalues = {}
        for cs in g.control_stations.control_station:
            csnames.append(cs.name)
            csvalues[cs.name] = {}
            frm = float(cs.location_angle.frm)
            to = float(cs.location_angle.to)
            if to < frm:
                to += 360.0
            location_angle = int(random.uniform(frm, to)) % 360
            csvalues[cs.name]['location_angle'] = location_angle
        result['duration'] = float(self.Miss[name].duration)
        result['start_angular_velocity'] = 1.0
        for gen in g.parameters.split(','):
            if gen == 'orbit':
                result['orbit'] = int(random.uniform(float(g.orbit.frm),
                                                     float(g.orbit.to)))
            elif gen == 'control_stations':
                result['control_stations'] = csvalues
            elif gen == 'oneway_message':
                length = int(random.uniform(float(g.oneway_message.length.frm),
                                            float(g.oneway_message.length.to)))
                result['oneway_message'] = generate_bytes(length)
            elif gen == 'messages':
                result['messages'] = {}
                locations = [0.0, 0.0, 0.0]
                for i in range(g.messages.number):
                    m = {}
                    m['data'] = int(random.uniform(float(g.messages.data.frm),
                                                   float(g.messages.data.to)))
                    m['timeout'] = int(random.uniform(float(g.messages.timeout.frm),
                                                      float(g.messages.timeout.to)))
                    while ((locations[2] - locations[0]) > 240.0 or
                           (locations[2] - locations[1]) < 60.0 or
                           (locations[1] - locations[0]) < 60.0):
                        m['msgfrom'] = random.choice(csnames)
                        locations[1] = float(csvalues[m['msgfrom']]['location_angle'])
                        if locations[1] < locations[0]:
                            locations[1] += 360.0
                        m['msgto'] = random.choice(csnames)
                        locations[2] = float(csvalues[m['msgto']]['location_angle'])
                        if locations[2] < locations[1]:
                            locations[2] += 360.0
                    while locations[2] > 360.0:
                        locations[2] -= 360.0
                    locations[1] = locations[2]
                    locations[0] = locations[2]
                    result['messages'][i + 1] = m
            elif gen == 'target_angle':
                result['target_angle'] = int(random.uniform(float(g.target.location_angle.frm),
                                                            float(g.target.location_angle.to)))
            elif gen == 'target_orbit':
                result['target_orbit'] = int(random.uniform(float(g.target.orbit.frm),
                                                            float(g.target.orbit.to)))
            elif gen == 'channel':
                result['channel'] = int(random.uniform(float(g.channel.frm),
                                                       float(g.channel.to)))
            elif gen == 'precision':
                result['precision'] = round(random.uniform(float(g.precision.frm),
                                                           float(g.precision.to)),
                                            3)
            elif gen == 'resolution':
                result['resolution'] = round(random.uniform(float(g.resolution.frm),
                                                            float(g.resolution.to)),
                                             3)
            elif gen == 'missiles':
                result['missiles'] = {}
                for i in range(g.missiles.number):
                    m = {}
                    frm = float(g.missiles.location_angle.frm)
                    to = float(g.missiles.location_angle.to)
                    if to < frm:
                        to += 360.0
                    location_angle = int(random.uniform(frm, to)) % 360
                    m['location_angle'] = location_angle
                    frm = float(g.missiles.launch_time.frm)
                    to = float(g.missiles.launch_time.to)
                    while True:
                        launch_time = int(random.uniform(frm, to))
                        collision = False
                        for j in result['missiles']:
                            if abs(result['missiles'][j]['launch_time'] -
                                   launch_time) < g.missiles.cooldown:
                                collision = True
                                break
                        if not collision:
                            break
                    m['launch_time'] = launch_time
                    result['missiles'][i + 1] = m

        return result

    @classmethod
    def generate_xml(cls, mission_type, mission_data):
        result = '<mission type="%s">\n' % mission_type
        for key in sorted(mission_data.keys()):
            value = mission_data[key]
            if key == 'control_stations':
                result += '<control_stations>\n'
                for csname, csvalue in value.items():
                    result += '\t<control_station name="%s">\n' % csname
                    result += ('\t\t<location_angle>%f</location_angle>\n' %
                               float(csvalue['location_angle']))
                    result += '\t</control_station>\n'
                result += '</control_stations>\n'
            elif key == 'messages':
                if value is not None and len(value) > 0:
                    result += '<messages>\n'
                    for index, msg in value.items():
                        result += ('<message order="%d" msgfrom="%s" msgto="%s" data="%f" duration="%f"/>\n' % # pylint: disable=C0301
                                   (int(index), msg['msgfrom'], msg['msgto'],
                                    float(msg['data']), float(msg['timeout'])))
                    result += '</messages>\n'
            elif key == 'oneway_message':
                if value is not None and len(value) > 0:
                    result += ('<oneway_message text="%s"/>\n' % value)
            elif key == 'missiles':
                if value is not None and len(value) > 0:
                    result += '<missiles>\n'
                    for index, missile in value.items():
                        result += '\t<missile index="%d">\n' % int(index)
                        result += ('\t\t<location_angle>%f</location_angle>\n' %
                                   float(missile['location_angle']))
                        result += ('\t\t<launch_time>%f</launch_time>\n' %
                                   float(missile['launch_time']))
                        result += '\t</missile>\n'
                    result += '</missiles>\n'
            else:
                result += '<%s>%f</%s>\n' % (key, float(value), key)
        result += '</mission>\n'
        return result

    def table(self):
        result = ''
        for mission in self.Miss.values():
            result += ('  \\multicolumn{3}{|c|}{\\textbf{%s}}\\\\\n' %
                       mission.full_name)
            result += '  \\hline\n'
            for a in mission.achievements.achievement:
                if a.type != 'spec':
                    for s in a.score:
                        d = s.description if hasattr(s, 'description') else ''
                        result += '  %s & %s & %s\\\\\n' % (s.full_name,
                                                            d,
                                                            s.score_value)
                        result += '  \\hline\n'
                else:
                    result += '  %s & %s & %s\\\\\n' % (a.full_name,
                                                        '',
                                                        a.score[0].score_value)
                    result += '  \\hline\n'
        return result

class Devices(XMLLoader):

    ORIGIN = _('devices')
    XML_FILE = "devices.xml"

    @classmethod
    def decode(cls, xmldata):
        return venus.devices.CreateFromDocument(xmldata)

    @classmethod
    def load_devices_map(cls, lang, devices_file=XML_FILE):
        devices = cls.load(lang, devices_file)
        devices_map = {}
        for d in devices.choices.device:
            if d.name in devices_map:
                raise CriticalError(_("XML Error. Cannot load %s: there are two devices with the same nameд %s") % # pylint: disable=C0301
                                    (cls.ORIGIN, d.name))
            devices_map[d.name] = d
        return devices_map

class ProbeLoader(XMLLoader):

    ORIGIN = 'probe'

    @classmethod
    def load_probe(cls, lang, probefile):
        return cls.load(lang, probefile)

    @classmethod
    def decode(cls, xmldata):
        return venus.probe.CreateFromDocument(xmldata)

    @classmethod
    def generate_xml(cls, parameters,
                     tournament, probename, planet, starttime,
                     mission_type, mission_data,
                     constr_params, systems):
        """
        Gerenation of the probe XML file. Arguments:

        NAME		TYPE		DESCRIPTION
	tournament	str		the tournament name
	probename	str		the probe name
        planet		str		the planet (Земля = 'Earth')
        starttime	str,utc		the probe start time
        mission_type	str		the mission code (dzz, inspect, ...)
	mission_data	dict		the results of Missions.generate_mission call
        constr_params	dict		the probe constuction parameters
		constr_params['param name'] = param value
        systems		dict		the dictionary of the probe subsystems:
        	systems['subsystem name'] = {
                	'start_mode': str with the start state (ON / OFF), OFF is default
                        'program': str with the program for the subsystem, the default is empty
                }
        """
        result = '<?xml version="1.0" encoding="utf-8"?>\n'
        probename = probename.replace('"', '') # remove quote from the probe name
        result += '<v:probe name="%s" xmlns:v="venus">\n' % probename
        result += '<flight>\n'
        result += '<tournament>%s</tournament>\n' % tournament
        result += '<planet name="%s"/>\n' % planet
        result += '<time start="%s"/>\n' % starttime
        result += '<T_start>%f</T_start>\n' % parameters.Planets[planet].probe.T_start
        result += Missions.generate_xml(mission_type, mission_data)
        result += '</flight>\n'
        result += '<construction>'
        if 'fuel' in constr_params:
            result += '<fuel>%f</fuel>\n' % float(constr_params['fuel'])
        result += '<voltage>%f</voltage>\n' % float(constr_params['voltage'])
        if 'xz_yz_solar_panel_fraction' in constr_params:
            result += ('<xz_yz_solar_panel_fraction>%f</xz_yz_solar_panel_fraction>\n' %
                       float(constr_params['xz_yz_solar_panel_fraction']))
        if 'xz_yz_radiator_fraction' in constr_params:
            result += ('<xz_yz_radiator_fraction>%f</xz_yz_radiator_fraction>\n' %
                       float(constr_params['xz_yz_radiator_fraction']))
        if 'xy_radiator_fraction' in constr_params:
            result += ('<xy_radiator_fraction>%f</xy_radiator_fraction>\n' %
                       float(constr_params['xy_radiator_fraction']))
        result += '</construction>\n'
        result += '<systems>'
        for sname, svalue in systems.items():
            result += '<system name="%s"' % sname
            if 'start_mode' in svalue:
                result += ' start_mode="%s"' % svalue['start_mode']
            if 'program' in svalue:
                result += ('>\n<program>\n<![CDATA[\n%s\n]]></program>\n</system>\n' %
                           svalue['program'])
            else:
                result += '/>\n'
        result += '</systems>\n'
        result += '</v:probe>\n'
        return result

class ShortLogLoader(XMLLoader):

    ORIGIN = 'short log'

    @classmethod
    def decode(cls, xmldata):
        result = {}
        try:
            xml = venus.shortlog.CreateFromDocument(xmldata)
            result['code'] = xml.status
            result['result_message'] = xml.result_message
            possible_tags = ('result_score', 'result_detectiondelay', 'result_resolution',
                             'result_sessioncount',
                             'result_sessionlength', 'result_targetangle', 'result_targetdest',
                             'result_targetdiff', 'result_targetnormal', 'result_tempdelta',
                             'result_turns', 'result_unintercepted',
                             'tournament', 'planet', 'probe', 'mission',
                             'flight_time', 'mission_log')
            for t in possible_tags:
                if hasattr(xml, t):
                    tagvalue = getattr(xml, t)
                    if tagvalue is not None:
                        result[t] = tagvalue
            if hasattr(xml, 'images') and xml.images is not None:
                result['images'] = []
                for img in xml.images.image:
                    result['images'].append((img.file, img.title))
            # ignore data and events
        except pyxb.ValidationError as e:
            result = {'code': 'error',
                      'result_message': _('Error while reading short log: %s') % str(e)}
        return result

    @classmethod
    def generate_short_log(cls, tournament, name, planet, mission,
                           time, status, message, score, images,
                           telemetry, data, events, addparams):
        result = deque()
        result.append('<?xml version="1.0" encoding="utf-8"?>\n')
        result.append('<v:shortlog xmlns:v="venus">\n')
        result.append('<tournament>%s</tournament>\n' % tournament)
        result.append('<probe>%s</probe>\n' % name)
        result.append('<planet>%s</planet>\n' % planet)
        result.append('<mission>%s</mission>\n' % mission)
        result.append('<flight_time>%d</flight_time>\n' % time)
        result.append('<status>%s</status>\n' % status)
        result.append('<result_message>' + str(xml_escape(message)) +
                      '</result_message>\n')
        result.append('<result_score>' + str(score) + '</result_score>\n')
        for k in sorted(addparams.keys()):
            result.append('<' + k + '>' + str(addparams[k]) + '</' + k + '>\n')
        if len(images) > 0:
            result.append('<images>\n')
            for img in images:
                result.append('<image file="%s" title="%s"/>\n' % img)
            result.append('</images>\n')
        logfile = logging['mission']
        if telemetry and logfile and isfile(logfile):
            result.append('<mission_log>%s</mission_log>\n' % logfile)
        if len(data) > 0:
            result.append('<data>\n')
            for d in data:
                result.append('%s\n' % d)
            result.append('</data>\n')
        if len(events) > 0:
            result.append('<events>\n')
            for e in events:
                result.append('%s\n' % e)
            result.append('</events>\n')
        result.append('</v:shortlog>\n')
        return ''.join(result)
