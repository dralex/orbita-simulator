# -----------------------------------------------------------------------------
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# The Orbita Simulator
# The Earth orbit simulation model (v2)
#
# The calculation models: the programmed control model
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

import data
from abstractmodel import AbstractModel
from logger import mission_log
import pycontrol.program
from api.systems_runtime import SputnikRuntime
from language import Language

_ = Language.get_tr()

# -----------------------------------------------------------------------------
# Python (new) model
# -----------------------------------------------------------------------------

class PythonControlModel(AbstractModel):
    def __init__(self, global_parameters):
        AbstractModel.__init__(self, global_parameters)
        self.programs = []

    def init_model(self, probe, initial_tick):
        print("init")
        
        global _ # pylint: disable=W0603
        _ = Language.get_tr()
        for s in probe.systems.values():
            if s and s.program is not None:
                if len(str(s.program).strip()) != 0:
                    try:
                        s.program_text = str(s.program).lstrip().split('\n')
                        runtime = SputnikRuntime(probe)
                        s.program_instance = pycontrol.program.Program(runtime,
                                                                       'systems_api',
                                                                       s.program_text
                                                                       )
                        
                        self.programs.append(s)
                        
                    except pycontrol.program.ProgramError as e:
                        str_e = str(e).replace('%', '%%')
                        data.critical_error(probe,
                                            _('The device %s program error: %s\n\t%s'),
                                            s.device.name, str_e, e.dump)
                    except pycontrol.program.SecurityError as e:
                        str_e = str(e).replace('%', '%%')
                        data.critical_error(probe,
                                            _('Error while running program of the device: %s: %s'),
                                            s.device.name, str_e)
                    except pycontrol.program.WorkerError as e:
                        str_e = str(e).replace('%', '%%')
                        data.critical_error(probe,
                                            _('System error while running program: %s'),
                                            str_e)

    def step(self, probe, tick):
        for s in self.programs:
            try:
                s.run_program()
            except pycontrol.program.ProgramError as e:
                str_e = str(e).replace('%', '%%')
                s = (_('The device %s program error: %s\n\t%s') %
                     (s.device.name, str_e, e.dump))
                mission_log(s)
                probe.program_error = True
                data.terminate(probe, s)
            except pycontrol.program.SecurityError as e:
                str_e = str(e).replace('%', '%%')
                data.critical_error(probe,
                                    _('Error while running program of the device %s: %s'),
                                    s.device.name, str_e)
            except pycontrol.program.FinishError as e:
                str_e = str(e).replace('%', '%%')
                mission_log(_('Program finished.'))
                if probe.success:
                    probe.completed = True
                else:
                    probe.program_error = True
                    data.terminate(probe, str_e)

    def debug_model(self, probe):
        return ('\n'.join(probe.program_instance.print_buffer if
                          probe.program_instance else 'None'))
