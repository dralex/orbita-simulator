import time
import gettext

import data
import constants
from utils import generate_bytes
from mission import Mission
from logger import debug_log, mission_log

_ = gettext.gettext

class SatelliteInternetMission(Mission):
    name = constants.MISSION_SATELLITE_INTERNET

    def __init__(self, global_parameters):
        Mission.__init__(self, global_parameters)
        self.sms_messages = None
        self.is_start = False
        self.count_ticks = 0
        self.is_end = False
        self.gs_id = None
        self.probe_id = None

    def init(self, probes, initial_tick, lang):
        global _  # pylint: disable=W0603
        _ = lang
        probe = probes.get()[0]

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

    def step(self, probes, tick):
        probe = probes.get()[0]
        radio = probe.systems[constants.SUBSYSTEM_RADIO]

        self.count_ticks += 1 if self.is_start else 0

        for gs in radio.received_packets.keys():
            if len(radio.received_packets[gs]) != 0:
                for message in radio.received_packets[gs].values():
                    realdata = message[3]

                    if realdata[0] == self.name:
                        msg = _('SMS received form %s, time interval %f sec') % (realdata[1],
                                                                                 realdata[3])
                        debug_log(probe, msg)
                        mission_log(probe, msg)
                        self.sms_messages[0][4] = probe.time()
                        if self.is_start:
                            try:
                                int(gs)
                                if gs != self.gs_id:
                                    self.is_end = True
                            except:
                                self.probe_id = gs

        for gs in radio.sent_packets.keys():
            if len(radio.sent_packets[gs]) != 0:
                for message in radio.sent_packets[gs].values():
                    realdata = message[3]

                    if realdata[0] == self.name:
                        source = realdata[1]
                        text = realdata[2]
                        msg = (_('Ground station %s received the SMS-message from %s size %d. ') %
                               (gs, source, len(text)))
                        error = False
                        errmsg = ''

                        if len(self.sms_messages) > 0:
                            sms = self.sms_messages[0]
                            if sms[0] != source:
                                errmsg += (
                                            _('Error: the message was received from the wrong source - %s instead of %s. ') %  # pylint: disable=C0301
                                            (source, sms[0]))
                                error = True
                            if sms[1] != gs:
                                errmsg += (
                                            _('Error: the message was sent to the wrong destination - %s instead of %s. ') %  # pylint: disable=C0301
                                            (gs, sms[1]))
                                error = True
                            if sms[2] != text:
                                errmsg += _('Error: the message was changed while transfered. ')
                                error = True
                            if sms[4] is not None:
                                dt = probe.time() - sms[4]
                                if sms[3] < dt:
                                    errmsg += (
                                                _('Error: the transfer time %f sec exceeded the valid interval %f sec.') %  # pylint: disable=C0301
                                                (dt, sms[3]))
                                    error = True
                            else:
                                errmsg += _(
                                    'Error: the probe tried to send message before receiving it. ')  # pylint: disable=C0301
                                error = True
                        else:
                            errmsg += _('Error: all the messages were sent. ')
                            error = True

                        mission_log(probe, msg + errmsg)
                        debug_log(probe, msg + errmsg)

                        if error and not self.is_start:
                            mission_log(probe, _('Problems while sending SMS-message. ') + errmsg)
                        else:
                            self.is_start = True
                            self.gs_id = gs

                        if len(self.sms_messages) > 0:
                            self.sms_messages.pop(0)

                        if len(self.sms_messages) > 0:
                            msgfrom, msgto, text, duration = self.sms_messages[0][0:4]
                            debug_log(probe, _('New SMS-message %s->%s'), msgfrom, msgto)
                            radio.receive_queues_flush()
                            radio.receive_data(msgfrom, len(text),
                                               (constants.MISSION_SMS, msgto, text, duration))
                        else:
                            probe.completed = True
        if self.is_end:
            mission_log(probe,
                        _('MISSION ACCOMPLISHED! SMS-message was transferred correctly.'))
            probe.success = True


data.available_missions[SatelliteInternetMission.name] = SatelliteInternetMission