# -----------------------------------------------------------------------------
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# The Orbita Simulator
# The Earth orbit simulation model (v2)
#
# The simulator missions implementation: the Test mission 2
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

import time
import gettext

import data
import constants
from mission import Mission
from logger import debug_log, mission_log

_ = gettext.gettext

class TestSmsMission(Mission):
    name = constants.MISSION_TEST_SMS

    def __init__(self, global_parameters):
        Mission.__init__(self, global_parameters)
        self.text = ''

    def init(self, probes, initial_tick, lang):
        global _ # pylint: disable=W0603
        _ = lang
        probe = probes.get()[0]
        self.text = _(probe.xml.flight.mission.oneway_message.text)

    def step(self, probes, tick):
        probe = probes.get()[0]
        radio = probe.systems[constants.SUBSYSTEM_RADIO]

        for gs in radio.sent_packets.keys():
            if len(radio.sent_packets[gs]) != 0:
                for message in radio.sent_packets[gs].values():
                    realdata = message[3]

                    if realdata[0] == self.name:
                        text = realdata[2].decode('utf-8')
                        msg = (_('The ground station %s received SMS size %d. ') %
                               (gs, len(text)))
                        error = False
                        errmsg = ''
                        if self.text != text:
                            msg += _('Error: the message was changed while being transferred. ')
                            error = True

                        mission_log(probe, msg + errmsg)
                        debug_log(probe, msg + errmsg)

                        if error:
                            data.terminate(probe,
                                           _('The probe transferred wrong message. {}').format(errmsg)) # pylint: disable=C0301
                        else:
                            mission_log(probe, _('MISSION ACCOMPLISHED! The message was transferred.'))
                            probe.success = True
                            probe.success_timestamp = time.time()
                            probe.completed = True

data.available_missions[TestSmsMission.name] = TestSmsMission
