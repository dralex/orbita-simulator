# -----------------------------------------------------------------------------
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# The Orbita Simulator
# The Earth orbit simulation model (v2)
#
# Main simulation procedure
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
if sys.version_info.minor >= 10:
    import collections
    import collections.abc
    collections.MutableSequence = collections.abc.MutableSequence

import os
import os.path
import gettext
import importlib

import xmlconverters
import data
import constants
import logger
from logger import set_logging, debug_log, mission_log, sync_logs
from errors import CriticalError, Terminated
from language import Language

_ = gettext.gettext

DEFAULT_LANG = 'en'
LOCAL_DIR = os.path.dirname(os.path.abspath(__file__))
PARAMETERS_FILE = os.path.join(LOCAL_DIR, 'parameters.xml')
DEVICES_FILE = os.path.join(LOCAL_DIR, 'devices{}.xml')
SYNC_LOGS_PERIOD = 1000

def usage():
    print('usage: %s <probe-file> ' % sys.argv[0] +
          '[--mission-log=<mission-log-file] ' +
          '[--debug-log=<debug-log-file>] ' +
          '[--image=<image-name-template>]' +
          '[--short-log=<short-log-file>]' +
          '[--lang=<en|ru>]')
    sys.exit(1)

def run(probename, probefile, missionfile, debugfile, shortfile, #pylint: disable=R0912,R0914
        imagedir, htmldir, lang): 				    #pylint: disable=W0613
    """ This is main entry point for server
    All logic, except command-line parsing should be inside this call
    """

    Language.set_lang(lang)
    global _ # pylint: disable=W0603
    _ = Language.get_tr()

    if missionfile:
        set_logging('mission', missionfile)
    if debugfile:
        set_logging('debug', debugfile)
    if imagedir:
        if os.path.isdir(imagedir):
            imagetmpl = imagedir + "/"
        else:
            imagetmpl = imagedir
        set_logging('image', imagetmpl)
    else:
        imagetmpl = None

    probe = None
    try:

        parameters = xmlconverters.GlobalParameters.load(Language, PARAMETERS_FILE)
        data.load_parameters_atmosphere(parameters)

        lang_postfix = "-{}".format(lang) if lang != DEFAULT_LANG else ''
        devices_map = xmlconverters.Devices.load_devices_map(Language,
                                                             DEVICES_FILE.format(lang_postfix))

        probe = data.Probe(probename,
                           probefile,
                           parameters,
                           devices_map)

        planet_params = parameters.Planets[probe.planet]
        tick_length = float(planet_params.tick)
        probe.print_probe()

        models = []
        telemetry = None
        for kind, modelclass in planet_params.Models:
            try:
                pkg = 'calcmodels.{}'.format(kind)
                module = importlib.import_module(pkg, pkg)
                if not hasattr(module, modelclass):
                    raise CriticalError(_('Module load error: cannot find class %s in module %s') %
                                        (modelclass, kind))
                cls = getattr(module, modelclass)
                model = cls(parameters)
                models.append(model)
                if kind == 'telemetry':
                    telemetry = model
            except ImportError as e:
                raise CriticalError(_('Module load error: module %s cannot be loaded: %s') %
                                    (kind, str(e)))

        cls = data.available_missions[probe.mission]
        mission = cls(parameters)

        try:
            probe.systems[constants.SUBSYSTEM_CPU].flight_time = 0.0

            for m in models:
                m.init_model(probe, tick_length)

            mission.init(probe, tick_length, Language.get_tr())

            simulation_time = 0.0
            iteration = 0

            while True:
                for m in models:
                    m.step(probe, tick_length)

                mission.step(probe, tick_length)

                probe.update_mass()

                probe.systems[constants.SUBSYSTEM_CPU].update_time(tick_length)

                if probe.mission_ended():
                    debug_log(_('MISSION ENDED. Duration = %s'),
                              data.time_to_str(simulation_time + tick_length))
                    break

                simulation_time += tick_length
                logger.simulation_time += tick_length

                if iteration % SYNC_LOGS_PERIOD == 0:
                    sync_logs()
                iteration += 1

        except Terminated as e:
            debug_log(_('Terminated: ') + str(e))

        if probe.success:
            code = 'completed'
            if probe.success_score is not None:
                res = _('Mission accomplished with the score %f') % probe.success_score
            else:
                res = _('Mission accomplished')
        elif probe.telemetry_received > 0 or probe.program_error:
            code = 'failed'
            res = _('Mission failed')
        else:
            code = 'notelemetry'
            res = _('No telemetry from the probe')

        mission_log(_('%s. Duration: %s'),
                    res, data.time_to_str(probe.time()))
        probe.flight_result = (code, res)

        if code != 'completed':
            telemetry.clear_extra_telemetry(probe)

        if imagetmpl:
            telemetry.draw_images(probe, imagetmpl)

        if shortfile:
            d = telemetry.get_short_results(probe)
            events = telemetry.get_events(probe)

            addparams = {}

            if ((probe.mission == constants.MISSION_TEST_LOOK or
                 probe.mission == constants.MISSION_TEST_SMS)):
                addparams['result_turns'] = probe.systems[constants.SUBSYSTEM_NAVIGATION].turns
            elif probe.mission == constants.MISSION_TEST_ORBIT:
                if probe.orbit_diff is not None:
                    addparams['result_targetdiff'] = probe.orbit_diff
            elif probe.mission == constants.MISSION_SMS:
                if probe.message_number is not None:
                    addparams['result_msgnum'] = probe.message_number
            elif probe.mission == constants.MISSION_INSPECT:
                if probe.photo_resolution is not None:
                    addparams['result_resolution'] = probe.photo_resolution
                if probe.photo_distance is not None:
                    addparams['result_targetdest'] = probe.photo_distance
            elif probe.mission == constants.MISSION_DZZ:
                if probe.photo_resolution is not None:
                    addparams['result_resolution'] = probe.photo_resolution
                if probe.photo_offset_angle is not None:
                    addparams['result_targetangle'] = probe.photo_offset_angle
                if probe.photo_incidence_angle is not None:
                    addparams['result_targetnormal'] = probe.photo_incidence_angle
            elif probe.mission == constants.MISSION_CRYSTAL:
                load = probe.systems[constants.SUBSYSTEM_LOAD]
                if load.valid_environment:
                    if probe.landing_error is not None:
                        addparams['result_targetdiff'] = probe.landing_error
                    if load.max_temperature_diff is not None:
                        addparams['result_tempdelta'] = load.max_temperature_diff
            elif probe.mission == constants.MISSION_MOLNIYA:
                if probe.session_count is not None:
                    addparams['result_sessioncount'] = probe.session_count
                if probe.session_length is not None:
                    addparams['result_sessionlength'] = probe.session_length
            elif probe.mission == constants.MISSION_EARLY_WARNING:
                if probe.detection_delay is not None:
                    addparams['result_detectiondelay'] = probe.detection_delay
                if probe.missiles_unintercepted is not None:
                    addparams['result_unintercepted'] = probe.missiles_unintercepted

            probe.write_short_log(shortfile, d, events, addparams)

    except CriticalError as e:
        debug_log(_('CriticalError: {}').format(str(e)))
        if shortfile:
            f = open(shortfile, 'w')
            f.truncate()
            f.write('<?xml version="1.0" encoding="utf-8"?>\n')
            f.write('<v:shortlog xmlns:v="venus">\n')
            if e.tournament:
                f.write('<tournament>%s</tournament>\n' % e.tournament)
            if e.probe:
                f.write('<probe>%s</probe>\n' % e.probe)
            if e.planet:
                f.write('<planet>%s</planet>\n' % e.planet)
            if e.mission:
                f.write('<mission>%s</mission>\n' % e.mission)
            f.write('<status>error</status>\n')
            f.write('<result_message>%s</result_message>\n' % xmlconverters.xml_escape(str(e)))
            f.write('</v:shortlog>\n')
            f.close()

    return True

if __name__ == '__main__':

    if len(sys.argv) < 2 or len(sys.argv) > 7:
        usage()

    missionLogFile = None
    debugLogFile = None
    shortLogFile = None
    imageTemplate = None
    langArg = DEFAULT_LANG

    probe_file = sys.argv[1]

    for arg in sys.argv[2:]:
        if not missionLogFile and arg.find('--mission-log=') != -1:
            missionLogFile = arg[len('--mission-log='):]
        elif not debugLogFile and arg.find('--debug-log=') != -1:
            debugLogFile = arg[len('--debug-log='):]
        elif not imageTemplate and arg.find('--image=') != -1:
            imageTemplate = arg[len('--image='):]
        elif not shortLogFile and arg.find('--short-log=') != -1:
            shortLogFile = arg[len('--short-log='):]
        elif langArg == DEFAULT_LANG and arg.find('--lang=') != -1:
            langArg = arg[len('--lang='):]
        else:
            usage()

    try:
        probe_name = os.path.basename(probe_file)
        probe_name = probe_name[0:probe_name.find('.xml')]
        run(probe_name, probe_file, missionLogFile,
            debugLogFile, shortLogFile, imageTemplate,
            None, langArg)
    except CriticalError as e:
        print(_('Critical error: {}').format(str(e)))
        sys.exit(2)

    sys.exit(0)
