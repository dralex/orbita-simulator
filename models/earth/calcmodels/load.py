# -----------------------------------------------------------------------------
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# The Orbita Simulator
# The Earth orbit simulation model (v2)
#
# The calculation models: the probe load models
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

import constants
from abstractmodel import AbstractModel
from logger import debug_log
from language import Language

_ = Language.get_tr()

class SimpleLoadModel(AbstractModel):
    def __init__(self, global_parameters):
        AbstractModel.__init__(self, global_parameters)

    def init_model(self, probe, initial_tick):
        global _ # pylint: disable=W0603
        _ = Language.get_tr()
        load = probe.systems[constants.SUBSYSTEM_LOAD]
        if not load:
            return
        if load.photo:
            probe.photo_resolution = None
            probe.photo_offset_angle = None
            probe.photo_incidence_angle = None
            probe.photo_distance = None

    def step(self, probe, tick, probes): # pylint: disable=R0912
        load = probe.systems[constants.SUBSYSTEM_LOAD]
        if not load:
            return

        if (load.mode == constants.STATE_ON) and load.running:
            if load.photo:
                if load.visible_target is not None:
                    if load.best_visible_target is not None:
                        if load.best_visible_target != load.visible_target:
                            load.best_target_offset_angle = None
                    load.best_visible_target = load.visible_target
                    if (((load.best_target_offset_angle is None) or
                         (load.target_offset_angle <= load.best_target_offset_angle))):
                        load.best_target_offset_angle = load.target_offset_angle
                        load.best_target_distance = load.target_distance
                        load.best_target_incidence_angle = load.target_incidence_angle
                load.photo_data += int(load.data_stream * tick)
                free_memory = load.memory_total - load.memory_used
                if load.photo_data > free_memory:
                    telemetry = probe.systems[constants.SUBSYSTEM_TELEMETRY]
                    telemetry.send_log_message(_('The camera memory %s (%f bytes) overloaded. The memory buffer was dropped') % # pylint: disable=C0301
                                               (load.device.full_name, load.memory_total))
                    debug_log(_('The camera memory (%f bytes) overloaded, the data was lost (%f bytes)'), # pylint: disable=C0301
                              load.memory_total, load.photo_data)
                    load.photo_data = 0
                    load.best_visible_target = None
                    load.best_target_offset_angle = None
                    load.best_target_distance = None
                    load.best_target_incidence_angle = None
