# -----------------------------------------------------------------------------
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# The Orbita Simulator
# The Earth orbit simulation model (v2)
#
# Dummy calls for the universal HSM interpreter
#
# Copyright (C) 2015-2023 Alexey Fedoseev <aleksey@fedoseev.net>
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

class CPU:
    def __init__(self):
        self.events = []        
    
    def run(self):
        return True

    def has_event(self):
        if self.events:
            return self.events.pop(0)
        else:
            return ''

    def dispatch(self, event):
        self.events.append(event)

    def terminate(self):
        sys.exit(0)

cpu = CPU()
debug = print