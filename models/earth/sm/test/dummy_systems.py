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
import time
import select

class CPU:
    def __init__(self):
        self.events = []        

    def run(self):
        self.__getchar()
        return True

    def has_event(self):
        if self.events:
            ev = self.events.pop(0)
            if ev[1] is None:
                return ev[0]
            else:
                return ev
        else:
            return ''

    def dispatch(self, event, value=None):
        self.events.append((event, value))

    def terminate(self):
        sys.exit(0)

    def get_flight_time(self):
        return time.time()

    def __getchar(self):
        # This line is working on Linux. TODO: write portable code
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            c = sys.stdin.read(1)
            if c:
                self.dispatch('GETCHAR', c)

cpu = CPU()
debug = print
