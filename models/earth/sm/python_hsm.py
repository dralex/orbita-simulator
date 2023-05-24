# -----------------------------------------------------------------------------
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# The GraphML HSM converter
# Based on the implementation of the State Machine diagram to C++ generator
# from: https://github.com/notiel/fullgraphmlparser
#
# Copyright (C) 2023      Alexey Fedoseev <aleksey@fedoseev.net>
# Copyright (C) 2018-2021 Julia Notiel Salnikova
# Copyright (C) 2018-2021 Artem Sergeev
# Copyright (C) 2021      Alexey Ereminn
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
from typing import List
import xmltodict

import sm.qm as qm
import sm.graphml as gr
from sm.pycontrol_generator import PyControlGenerator

SUPPORTED_TYPE = 'yEd'
INIT_SCRIPTS_NOTE = 'Init scripts:'

class HSMException(Exception):
    def __init__(self, msg):
        Exception.__init__(self)
        self.msg = msg
    def __str__(self):
        return self.msg

def load_python_modules(xmlfile, filenames: List[str]):
    xmlpath = os.path.dirname(os.path.abspath(xmlfile))
    modules = {}
    result = '\n\n#Init script code:\n'
    for name in filenames:
        index = name.find('.py')
        if index < 0:
            continue
        filename = os.path.join(xmlpath, name)
        if not os.path.isfile(filename):
            raise HSMException('Cannot open impotred Python file {}'.format(filename))
        result += '\n# code imported from {}\n'.format(name)
        result += open(filename).read()
    return result

def convert_graphml(filename: str):

    player_signal = list()
    try:
        data = xmltodict.parse(open(filename).read())
        modelname = os.path.basename(filename)
        modelname = modelname.split('.')[0]
        modelname = modelname[0].lower() + modelname[1:]
    except FileNotFoundError:
        raise HSMException('Cannot open hsm file {}'.format(filename))

    # get nodes from file
    flat_nodes = gr.get_flat_nodes(data)
    state_nodes = [node for node in flat_nodes if (gr.is_node_a_state(node) or
                                                   gr.is_node_a_choice(node) or
                                                   gr.is_node_a_group(node))]
    state_nodes.sort(key=lambda st: len(st['id']))
    gr.update_qroup_nodes(state_nodes)
    state_nodes.sort(key=gr.coord_sort)

    # get min and max coord and height and width of the diagram
    coords = gr.get_minmax_coord(state_nodes)
    # create states from nodes and add internal triggers
    # to list the signals and all functions to function list
    functions: List[str] = list()
    qm_states, player_signal = qm.create_states_from_nodes(state_nodes, coords,
                                                           player_signal, functions)
    # get edges for external triggers
    flat_edges = gr.get_flat_edges(data)
    try:
        start_nodes = gr.get_start_nodes_data(flat_nodes, flat_edges)
    except ValueError:
        raise HSMException('UML-diagram %s does not have start node' % filename)
    try:
        finish_nodes = gr.get_finish_nodes_data(flat_nodes, flat_edges)
    except ValueError:
        finish_nodes = []
        # allow diagrams w/o finish nodes
    # add external trigger and update list of signals with them
    player_signal = qm.update_states_with_edges(qm_states, flat_edges,
                                                start_nodes[0][0],
                                                player_signal,
                                                coords[0],
                                                coords[1])
    # get notes
    notes = [node for node in flat_nodes if gr.is_node_a_note(node)]

    # load addional modules
    init_modules_code = ''
    for note in notes:
        note_text = note['y:UMLNoteNode']['y:NodeLabel']['#text']
        if note_text.startswith(INIT_SCRIPTS_NOTE):
            modules = filter(lambda t: len(t) > 0,
                             map(lambda t: t.strip(),
                                 note_text.split('\n')[1:]))
            init_modules_code = load_python_modules(filename, modules)
            break

    code = PyControlGenerator(modelname, start_nodes, finish_nodes, qm_states,
                              notes, init_modules_code).generate_code()
    code = ("# Python program generated from %s HSM diagram located in %s\n\n" %
            (SUPPORTED_TYPE, filename)) + code
    return code

if __name__ == '__main__':
    print(sys.argv[1])
