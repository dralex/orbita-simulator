import time
import gettext

import data
import constants
from mission import Mission
from logger import debug_log, mission_log

_ = gettext.gettext

class SatelliteInternetMission(Mission):
    name = constants.MISSION_SATELLITE_INTERNET

    def __init__(self, global_parameters):
        Mission.__init__(self, global_parameters)
        self.sms_messages = None

    def init(self, probe, initial_tick, lang):
        global _ # pylint: disable=W0603
        _ = lang
        radio = probe.systems[constants.SUBSYSTEM_RADIO]

        sms = {}
        for message in probe.xml.flight.mission.messages.message:
            sms[message.order] = [message.msgfrom,
                                  message.msgto,
                                  generate_bytes(int(message.data * 16)).encode('utf-8'),
                                  float(message.duration),
                                  None]

        self.sms_messages = []
        for order in sorted(sms.keys()):
            self.sms_messages.append(sms[order])
            debug_log(probe, _('Message %d: %s->%s'),
                      order, sms[order][0], sms[order][1])

        if len(self.sms_messages) == 0:
            data.critical_error(probe,
                                _('The Probe definition did not contain any SMS message'))

        msgfrom, msgto, text, duration = self.sms_messages[0][0:4]
        radio.receive_data(msgfrom, len(text), (probe.mission, msgto, text, duration))
