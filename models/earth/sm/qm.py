# -----------------------------------------------------------------------------
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# The GraphML HSM library
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

"""
this is special module for creating objects for qm file. Module contains description of class State (namedtiple)
for states and  class Trigger for trigsitions between states and functions for theis analyze and creation

-State                                                                       namedtuple with State data
-Trigger                                                                     namedtuple with trigger data
-get_state_by_id(states: [State], id:int, type:str) -> State                 gets state by its id
-def create_actions(raw_triggers: str, source: int) -> [Trigger]             creates trigger list from actions string
-create_state_from_node(id: int, node: dict) -> State:                       creates single qm state
-create_choice_from_node(node: dict, new_id: int, min_x: int, min_y: int) -> State:
                                                                             creates choice state from node
-create_states_from_nodes(nodes: [dict], min_x: int, min_y: int) -> [State]: function gets node data from node dict
                                                                             and returns State object with all  data
-update_states_with_edges(states: [State], flattened_edges: [dict]):         updates states with external transitions
-is_state_a_child(child: State, parent: State) -> bool:                      detects if one node is a parent to other
-is_state_a_child_by_coord(x, y, width, height, parent: State) -> bool:      detects if one node is a parent to other
                                                                             (using coordinates)
-get_parent(child: State, states: [State]) -> State:                         gets id of parent of a child
-get_parent_by_coord(x, y, w, h, states: [State]) -> State:                  gets id of parent of a child
-def get_childs(parent: State, states: [State]) ->[str]:                     gets list of childs
"""

import re
from typing import List, Optional, Tuple

from sm.graphml import *
from sm.stateclasses import State, Trigger

divider = 10  # we divide graphml coordinates by that value
action_delta = 5  # addition to action box
internal_trigger_height = 5  # height of space for internal trigger
internal_trigger_delta = 10  # addition to trigger name length
global_h_delta = 10  # addition to global height
global_w_delta = 10  # addition to global width
terminal_w = 10
terminal_h = 10


def get_state_by_id(states: [State], state_id: str, id_type: str) -> State:
    """
    gets state by its id
    :param id_type: for "old" we search for state with id = id, for "new" we search state with new_id = id
    :param states: list of states
    :param state_id: id for search
    :return: state with searched id
    """
    if id_type == 'new':
        for state in states:
            if state.new_id == state_id:
                return state
    if id_type == 'old':
        for state in states:
            if state.id == state_id:
                return state
    return states[0]


def get_functions(actions: str, functions: List[str]):
    """
    gets functions from code
    :param actions: text of node
    :param functions: list of sunctions to add new
    :return:
    """
    f_regexp = r'([A-Z]\w+)\([^\)]*\)'
    new_functions = re.findall(f_regexp, actions)
    for func in new_functions:
        if func not in functions:
            functions.append(func)
    return


def create_actions(raw_triggers: str, source: str, player_signal: List[str], functions: List[str]) -> List[Trigger]:
    """
    parses raw label text with events and their actions to get a list of Triggers ("exit" and "entry" events ignored)
    we use regexp to split raw data string
    regexp is some non-space symbols, then some space symbols, than "/" symbol
    Example:
        >>>create_actions("entry/
                           BUTTON2_PRESSED/
                             flash(get_color(rgb_table));
                             play_sound(get_random_sound(BLASTER));
                           BUTTON2_PRESSED_FOR_THREE_SECOND/
                             play_sound(get_random_sound(FORCE);
                           BOTH_BUTTONS_PRESSED/
                             change_color(get_color(rgb_table));
                             play_sound(get_sound(BOOT), 5);")

        [Trigger(name="BUTTON2_PRESSED", action="flash(get_color(rgb_table));
                                                play_sound(get_random_sound(BLASTER));", source=5)
         Trigger(name="BUTTON2_PRESSED_FOR_THREE_SECOND"), action="play_sound(get_random_sound(FORCE);", source=5),
         Trigger(name="BOTH_BUTTONS_PRESSED"), action="change_color(get_color(rgb_table));
                                                     play_sound(get_sound(BOOT));", source=5)]
    :param functions: list of fucntions
    :param raw_triggers: string with events and reactions
    :param source: id of source node
    :param player_signal - list of all sygnals
    :return: list of Triggers, list of sygnals
    """
    # regexp takes beginnig of string, than some a-zA-Z0-9_ symbols tnan spaces, than [guard] then /
    trigger_regexp: str = r"^ *\w+ *(?:\[.+?\])?\/"
    trigger_list = re.findall(trigger_regexp, raw_triggers, re.MULTILINE)
    trigger_data = re.split(trigger_regexp, raw_triggers, flags=re.MULTILINE)
    triggers: Dict[str, str] = dict(list(zip(trigger_list, trigger_data[1:])))
    actions: List[Trigger] = list()
    for (trigger_id, (trigger, action)) in enumerate(triggers.items(), start=1):
        guard: str = ""
        i = trigger.index(r'/')
        trigger_name: str = trigger[:i].strip()
        if '[' in trigger_name:
            guard_regexp: str = r"\[.*\]"
            res = re.search(guard_regexp, trigger_name)
            guard = res.group(0)[1:-1]
            trigger_name = re.split(guard_regexp, trigger_name)[0].strip()
            # if guard != 'else':
            #    logging.warning("Internal trigger %s[%s] can't contain guard" % (trigger_name, guard))

        if trigger_name not in player_signal and trigger_name and trigger_name != "entry" and trigger_name != 'exit':
            player_signal.append(trigger_name)
        # Un-indent each line in the (potentially multiline) action by the indent of the first line.
        lines = action.split('\n')[1:]  # discard 0, as 0-th line is the whitespace after 'SOME_SIG/'
        if lines:
            indent = len(lines[0]) - len(lines[0].lstrip())
            action = '\n'.join(line[indent:] for line in lines)
            action = action.rstrip()
        actions.append(Trigger(name=trigger_name, action=action, source=source, type="internal", guard=guard,
                               target="", id=trigger_id, x=0, y=internal_trigger_height * trigger_id,
                               dx=len(trigger_name) + internal_trigger_delta, dy=0, points=[], action_x=0,
                               action_y=5 * trigger_id - 2,
                               action_width=len(trigger_name) + action_delta))
    # add functions to function list
    get_functions(raw_triggers, functions)
    return actions, player_signal


def create_state_from_node(node: dict, node_type: str, min_x: int, min_y: int, states: [State],
                           player_signal: List[str], functions: List[str]) -> Tuple[State, List[str]]:
    """
    creates state from mode with node_type type (state or group)
    :param functions: list with functions
    :param node: dict with node data
    :param node_type: state or group
    :param min_x - min x coordinate to add to state coordinate to excluse negative coordinates
    :param min_y - min y coordinate to add to state coordinate to excluse negative coordinates
    :param states - list of created states
    :param player_signal - list of triggers
    :return State
    """
    name: str = get_state_label(node) if node_type == 'state' else get_group_label(node)
    actions: str = get_state_actions(node) if node_type == 'state' else get_group_actions(node)
    node_id = node['id']
    (triggers, player_signal) = create_actions(actions, node_id, player_signal, functions)
    state_entry: List[str] = [trig.action for trig in triggers if trig.name == 'entry']
    state_exit: List[str] = [trig.action for trig in triggers if trig.name == 'exit']
    state_entry_str = state_entry[0] if state_entry else ""
    state_exit_str = state_exit[0] if state_exit else ""
    triggers: List[Trigger] = [trig for trig in triggers if trig.name != 'entry' and trig.name != 'exit']
    x, y, width, height = get_coordinates(node)
    x = x // divider - min_x // divider + 2
    y = y // divider - min_y // divider + 2
    width: int = width // divider
    height: int = height // divider
    parent: State = get_parent_by_label(node_id, states)
    new_id: List[str] = [(parent.new_id[0] + "/" + str(len(parent.childs) + len(parent.trigs)))]
    state: State = State(name=name, type=node_type, id=node_id, new_id=new_id, actions=actions,
                         entry=state_entry_str, exit=state_exit_str, trigs=triggers, x=x,
                         y=y, width=width, height=height, parent=parent, childs=list())
    return state, player_signal


def create_choice_from_node(node: dict, min_x: int, min_y: int, states: [State]) -> State:
    """
    creates choice state from node
    :param node: dict with node data
    :param min_x - min x coordinate to add to state coordinate to excluse negative coordinates
    :param min_y - min y coordinate to add to state coordinate to excluse negative coordinates
    :param states - list of already creates states
    :return State
    """
    node_id = node['id']
    x, y, width, height = get_coordinates(node)
    x: int = x // divider - min_x // divider + 1
    y: int = y // divider - min_y // divider + 1
    width: int = width // divider
    height: int = height // divider
    parent: State = get_parent_by_label(node_id, states)
    new_id: List[str] = [parent.new_id[0] + "/" + str(len(parent.childs) + len(parent.trigs))]
    state: State = State(name=get_state_label(node), type="choice", id=node_id, new_id=new_id, actions="",
                         entry="", exit="", trigs=[], x=x, y=y,
                         width=width, height=height, parent=parent, childs=list())
    return state


def create_global_state(w: int, h: int) -> State:
    """
    creates global parent state of all states
    :param w: width between states
    :param h: height of all states
    :return: global parent state
    """
    state = State(name="global", type="group", id="", new_id=["1"], actions="",
                  entry="", exit="", trigs=[],
                  x=1, y=1, width=w // divider + global_w_delta, height=h // divider + global_h_delta, parent=None,
                  childs=[])
    return state


def create_states_from_nodes(nodes: [dict], coords: tuple, player_signal, functions: List[str]) -> List[State]:
    """
    function gets node data from node dict and returns State object with all necessary data
    :param functions: list of functions
    :param player_signal: list of signals
    :param coords: min x coordinate to calibrate others, min y coordinate to calibrate others,
    global wigth for global state, global height global state
    :param nodes: list of dicts with data
    :return: State list
    """
    min_x, min_y, w, h = coords[0], coords[1], coords[2] - coords[0], coords[3] - coords[1]
    states: List[State] = [create_global_state(w, h)]
    #states.append(create_terminate_state(states))
    #add_terminal_trigger(states)
    for node in nodes:
        if is_node_a_group(node):
            state, player_signal = create_state_from_node(node, "group", min_x, min_y, states, player_signal, functions)
            states.append(state)
    for node in nodes:
        if is_node_a_state(node):
            state, player_signal = create_state_from_node(node, "state", min_x, min_y, states, player_signal, functions)
            states.append(state)
    for node in nodes:
        if is_node_a_choice(node):
            state = create_choice_from_node(node, min_x, min_y, states)
            states.append(state)
    return states, player_signal


def update_states_with_edges(states: [State], flat_edges: [dict], start_state: str, player_signal: [str], min_x: int,
                             min_y: int):
    """
    function parses events on edges and adds them as external triggers to corresponding state (excluding start_edge)
    and recognizes and adds special labels to a choice edgea
    :param min_x: minimum value of x
    :param min_y: minimum value of y
    :param states: list of states
    :param flat_edges: list with edges
    :param start_state - id for start state for exclude start edge
    :param player_signal - list of already created signals
    :return:
    """
    for edge in flat_edges:
        for edge_type in edge_types:
            try:
                old_source: str = edge['source']
                if old_source != start_state and len(edge.keys()) > 3:
                    old_target: str = edge['target']
                    source_state: State = get_state_by_id(states, old_source, "old")
                    target_state: State = get_state_by_id(states, old_target, "old")
                    if is_edge_correct(edge, edge_type) and "#text" in edge[edge_type]['y:EdgeLabel'].keys():
                        action: str = edge[edge_type]['y:EdgeLabel']["#text"].split('/')
                        trigger_name: str = action[0].strip()
                        guard: str = ""
                        if '[' in trigger_name and ']' in trigger_name:
                            guard_regexp: str = r"\[.*\]"
                            res = re.search(guard_regexp, trigger_name)
                            guard: str = res.group(0)[1:-1]
                            trigger_name: str = re.split(guard_regexp, trigger_name)[0].strip()
                            # if guard == 'else':
                            #    logging.warning("External trigger %s[%s] can't contain 'else'" % (trigger_name, guard))
                        trigger_action: str = action[1].strip() if len(action) > 1 else ""
                    else:
                        trigger_name = ""
                        trigger_action = ""
                        guard = ""
                    x, y, dx, dy, points = get_edge_coordinates(edge)
                    new_points = []
                    for point in points:
                        new_points.append(((point[0] - min_x) // divider, (point[1] - min_y) // divider))
                    action_x, action_y, action_width = get_edge_label_coordinates(edge)
                    trig_type = "external"
                    if source_state.type == "choice":
                        trig_type = "choice_result"
                    if target_state.type == "choice":
                        trig_type = "choice_start"
                    trigger = Trigger(name=trigger_name, type=trig_type, guard=guard, source=old_source,
                                      target=old_target, action=trigger_action,
                                      id=0,
                                      x=x // divider, y=y // divider, dx=dx // divider, dy=dy // divider,
                                      points=new_points, action_x=action_x // divider, action_y=action_y // divider,
                                      action_width=action_width // divider + 2)
                    source_state.trigs.append(trigger)
                    if trigger_name and trigger_name not in player_signal:
                        player_signal.append(trigger_name)
            except KeyError:
                continue
    update_state_ids(states)
    return player_signal


def create_terminate_state(states: [State]) -> State:
    """
    creates state for terminate state machine on desktop
    :param states: list of states
    :return: global parent state
    """
    global_state: State = get_state_by_id(states, '', 'old')
    state: State = State(name="final?def DESKTOP", type="state", id="last", new_id=["2"], actions="",
                         entry="""printf("\nBye! Bye!\n"); exit(0);""", exit="", trigs=[],
                         x=global_state.x + global_state.width // 2 - terminal_w // 2,
                         y=states[0].y + states[0].height + 5, width=terminal_w, height=terminal_h, parent=None,
                         childs=[])
    return state


def add_terminal_trigger(states):
    terminate: State = get_state_by_id(states, "last", "old")
    first: State = get_state_by_id(states, "", "old")
    trigger: Trigger = Trigger(name="TERMINATE?def DESKTOP", type="external", guard="", source=first.id,
                               target=terminate.id, action="", id=0, x=0, y=first.height // 2,
                               dx=0, dy=-terminal_h // 2, points=[], action_x=-5, action_y=2, action_width=10)
    first.trigs.append(trigger)


def update_state_ids(states: [State]):
    """
    updates state ids to get path in ids
    :param states: list of states
    :return:
    """
    states.sort(key=lambda st: st.x)
    for i in range(0, len(states)):
        if states[i].new_id[0] == '1':
            states[i].new_id.append("1")
        else:
            if states[i].new_id[0] == '2':
                states[i].new_id.append("2")
            else:
                len_brothers: int = len(states[i].parent.childs)
                trigs = states[i].parent.trigs
                len_trigs = len(set([trig.name for trig in trigs]))
                states[i].new_id.append(states[i].parent.new_id[1] + "/" + str(len_brothers + len_trigs))
                if states[i].type != 'choice':
                    states[i].parent.childs.append(states[i])


def get_start_state_data(start_state: int, states: [State]) -> tuple:
    """
    function finds start state and gets it's id and coordinates
    :param start_state: id of start state
    :param states: list of states
    :return: id, x and y of start state
    """
    first_node = 0
    for state in states:
        if state.trigs:
            for trig in state.trigs:
                if trig.source == start_state:
                    first_node = trig.target
    return (get_state_by_id(states, first_node, "new").new_id, get_state_by_id(states, first_node, "old").y,
            (get_state_by_id(states, first_node, "new").x - 2))


def is_state_a_child(child: State, parent: State) -> bool:
    """
    detects if one node is a parent to other (using coordinates)
    :param child: child?
    :param parent: parent?
    :return: True if is a child else false
    """
    if parent.x <= child.x <= parent.x + parent.width and parent.y <= child.y <= parent.y + parent.height:
        return True
    return False


def is_state_a_child_by_coord(x, y, width, height, parent: State) -> bool:
    """
    detects if one node is a parent to other (using coordinates)
    :param x: x coord of a child
    :param y:  y coord of a child
    :param width: width of a child
    :param height: height of a child
    :param parent: parent?
    :return: true if child else false
    """
    if x + 1 >= parent.x and y + 1 >= parent.y and x + width - 1 <= parent.x + parent.width:
        if y + height - 1 <= parent.y + parent.height:
            return True
    return False


def is_state_a_child_by_label(parent: State, label: str)-> bool:
    """
    ckecks if parent state is really parent for child state
    :param parent: is a parent state?
    :param label: child label
    :return: is a  child?
    """
    pass
    return label.startswith(parent.id)


def get_parent_by_label(label: str, states: List[State]) -> Optional[State]:
    """
    gets nearest parent using node id
    :param label: child label
    :param states: list of States
    :return:
    """
    parents: List[State] = [state for state in states if is_state_a_child_by_label(state, label)]
    if not parents:
        return None
    parents.sort(key=lambda st: len(st.id))
    return parents[-1]


def get_parent(child: State, states: [State]) -> Optional[State]:
    """
    gets id of parent of a child
    :param child: state to get parent
    :param states: all states
    :return: parent
    """
    parents = [state for state in states if is_state_a_child(child, state)]
    if not parents:
        return None
    parents.sort(key=lambda st: st.x, reverse=True)
    return parents[0]


def get_parent_by_coord(x, y, w, h, states: [State]) -> Optional[State]:
    """
    gets id of parent of a child
    :param x: x coord of a child
    :param y:  y coord of a child
    :param w: width of a child
    :param h: height of a child

    :param states: all states
    :return: parent
    """
    parents: List[State] = [state for state in states if is_state_a_child_by_coord(x, y, w, h, state)]
    if not parents:
        return None
    parents.sort(key=lambda st: st.x, reverse=True)
    return parents[0]


def get_parent_list(state: State) -> List[State]:
    """
    get list of parent states
    :param state: current state
    :return: list of parent states
    """
    curr_state: State = state.parent
    parents: List[State] = list()
    while curr_state:
        parents.append(curr_state)
        curr_state = curr_state.parent
    return parents


def get_path(state1: str, state2: str, states) -> str:
    """
    gets path from state1 to state2 as for folders:
    EXAMPLE: "../../1/2"
    :param state1: first state
    :param state2: second state
    :param states: list of states
    :return:
    """
    state1 = get_state_by_id(states, state1, "old")
    state2 = get_state_by_id(states, state2, "old")
    if state1.id == "" and state2.id == "last":
        return "../../2"
    if state1 == state2:
        return ".."
    parents1 = get_parent_list(state1)
    parents2 = get_parent_list(state2)
    for parent in parents1:
        if parent in parents2:
            level = parents1.index(parent) + 2
            path = "../" * level
            path2 = list(reversed(state2.new_id[1].split('/')))
            path2 = path2[:parents2.index(parent) + 1]
            path += "/".join(list(reversed(path2)))
            return path


def get_graphml_coords_by_state_name(states: List[State], name: str, minx: float, miny: float) -> \
        Tuple[float, float, float, float]:
    """
    gets coords for graphml by name
    :param states: list of states
    :param name: name of needed state
    :param minx: min x
    :param miny: min y
    :return: x, y, width, height
    """
    for state in states:
        if state.name == name:
            return (state.x - 2) * divider + minx, (state.y - 2) * divider + miny, \
                   state.width * divider, state.height * divider
    return 0, 0, 0, 0


def get_edge_coords_by_state_and_name(states: List[State], name_state: str, name_edge: str, minx: int, miny: int) -> \
        Tuple[int, int, int, int, List[Tuple[int, int]]]:
    """
    get coords of edge by edge name and source name
    :param miny: min y of scheme
    :param minx:  min x of scheme
    :param states: list of states
    :param name_state: name of state
    :param name_edge: name of edge
    :return:
    """
    for state in states:
        if state.name == name_state:
            for trig in state.trigs:
                if trig.name == name_edge:
                    sx = trig.x * divider
                    sy = trig.y * divider
                    tx = trig.dx * divider
                    ty = trig.dy * divider
                    points = list()
                    for point in trig.points:
                        points.append((point[0]*divider + minx, point[1]*divider + miny))
                    return sx, sy, tx, ty, points
    return 0, 0, 0, 0, []
