#!/usr/bin/python3
# -----------------------------------------------------------------------------
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# The Orbita Simulator
# The Earth orbit simulation model (v2)
#
# The GraphML HSM universal interpreter
#
# Copyright (C) 2023      Alexey Fedoseev <aleksey@fedoseev.net>
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
import os
import subprocess

PROGRAM_PREAMBLE = """import sys
import pysm
sys.path.append('..')
from dummy_systems import *
"""

sys.path.append('../..')
import sm.python_hsm

def run_script(filename):
    idx = filename.index('.graphml')
    if idx < 0:
        print('Bad graph file name {}'.format(filename))
        sys.exit(1)
    if not os.path.isfile(filename):
        print('Cannot find file {}'.format(filename))
        sys.exit(1)
    code = None
    try:
        code = sm.python_hsm.convert_graphml(filename)
        code = PROGRAM_PREAMBLE + code
        result = subprocess.run(['python3', '-c', code],
                                capture_output=True,
                                text=True,
                                check=True)
        print(result.stdout)
    except sm.python_hsm.HSMException as s:
        print('Script failed: {}\n\n Program code:{}\n'.format(str(s), code))
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print('Script failed: {}\n\n Program code:{}\n'.format(str(e), code))
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python3 {} <graphml-file>'.format(sys.argv[0]))
        sys.exit(1)
    run_script(sys.argv[1])
