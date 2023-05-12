#!/usr/bin/python3
# -----------------------------------------------------------------------------
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# The Orbita Simulator
# The Earth orbit simulation model (v2)
#
# The GraphML HSM converter testing infrastructure
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
import re

TESTS_DIR = 'graphs'
PROGRAM_PREAMBLE = """import sys
import pysm
sys.path.append('..')
sys.path.append('../../api-test')
from systems import *
"""
TEST_PATTERN = re.compile(r'(?P<filebase>[^-]+)(-(?P<number>\d+))?.graphml$')

sys.path.append('../..')
import sm.python_hsm

tests = {}

for filename in os.listdir(TESTS_DIR):
    m = TEST_PATTERN.match(filename)
    if not m:
        continue
    fields = m.groupdict()
    filebase = fields['filebase']
    if filebase not in tests:
        tests[filebase] = []
    n = fields['number']
    if n:
        tests[filebase].append(n)

for filebase, numbers in tests.items():
    if numbers:
        # multiple diagrams are not supported yet
        continue
    filename = filebase + '.graphml'
    graphfile = os.path.join(TESTS_DIR, filename)
    outputfile = os.path.join(TESTS_DIR, filebase + '.txt')
    if not os.path.isfile(graphfile) or not os.path.isfile(outputfile):
        continue
    print('Test {}: '.format(filebase), end='')
    output = open(outputfile).read()
    code = None
    try:
        code = sm.python_hsm.convert_graphml(graphfile)
        code = PROGRAM_PREAMBLE + code
        sys.stdout.flush()
        result = subprocess.run(['python3', '-c', code],
                                capture_output=True,
                                text=True,
                                check=True)
        if result.stdout != output:
            raise Exception('failed: output mismatch, output={}'.format(result.stdout))
        print('OK')
    except sm.python_hsm.HSMException as s:
        if output == 'HSMException\n':
            print('OK')
            continue
        print('failed: {}\n\n Program code:{}\n'.format(s, code))
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print('Script failed: {}\n\n Program code:{}\n'.format(str(e), code))
        sys.exit(1)
sys.exit(0)
