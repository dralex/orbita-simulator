# -----------------------------------------------------------------------------
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# The Orbita Simulator
# The Earth orbit simulation model (v2)
#
# The converter from a GraphML HSM to a pysm-based Flight Program
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

import os.path
import re
from collections import defaultdict
from typing import List, Tuple, Any, Dict

from sm.stateclasses import State, Trigger

# -----------------------------------------------------------------------------
# Generator Constants
# -----------------------------------------------------------------------------

TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             'templates')
HEADER_TEMPLATE = os.path.join(TEMPLATES_DIR, 'header.templ')
FOOTER_TEMPLATE = os.path.join(TEMPLATES_DIR, 'footer.templ')

# -----------------------------------------------------------------------------
# GraphML-PyControl Constants
# -----------------------------------------------------------------------------

INIT_CODE_HEADER = 'Initialization'
TICK_EVENTS_HEADER = 'Tick events'

TIMER_EVENTS = ['TIMER_1S', 'TIMER_1M', 'TIMER_1H']

# -----------------------------------------------------------------------------
# The Generator Code
# -----------------------------------------------------------------------------

class PyControlGenerator:
    def __init__(self, sm_name: str, start_nodes: List[Tuple[str, str, List[str], str]],
                 finish_nodes: List[Tuple[str, str, str]],
                 states: List[State], notes: List[Dict[str, Any]],
                 player_signal: List[str]):

        self.id_to_name = {}
        self.notes_dict = {}
        self.all_signals = []

        self.sm_name = sm_name
        self.player_signal = player_signal
        self.has_timers = False
        self.has_ifelse_timers = False

        notes_mapping = [(INIT_CODE_HEADER, 'init'),
                         (TICK_EVENTS_HEADER, 'tick_events')]
        self.notes_dict = {key: '' for _, key in notes_mapping}

        for note in notes:
            for prefix, key in notes_mapping:
                if note['y:UMLNoteNode']['y:NodeLabel']['#text'].startswith(prefix):
                    text = note['y:UMLNoteNode']['y:NodeLabel']['#text']
                    if key == 'tick_events':
                        value = list(filter(lambda s: s != '', map(lambda v: v.strip(),
                                                                   text.split('\n'))))
                    else:
                        value = text
                    self.notes_dict[key] = value

        self.states = states
        self.choices = []
        for state in states:
            self.id_to_name[state.id] = state.name
            for trigger in state.trigs:
                if trigger.guard:
                    trigger.guard = trigger.guard.strip()
            if state.type == 'choice':
                self.choices.append(state.id)

        self.start_node = ''
        self.parents_with_start_node = {}
        for s in start_nodes:
            _, target_id, parents, _ = s
            target_name = self.id_to_name[target_id] # init edge actions still not supported
            if not parents:
                self.start_node = target_name
            else:
                the_parent = sorted(parents)[-1]
                parent_name = self.id_to_name[the_parent]
                assert parent_name not in self.parents_with_start_node
                self.parents_with_start_node[parent_name] = target_name
        assert self.start_node

        self.finish_nodes = {}
        for f in finish_nodes:
            source_id, target_id = f
            self.finish_nodes[source_id] = target_id

    def generate_code(self):
        handlers = {}
        transitions = {}
        result = ''
        result += self._insert_file_template(HEADER_TEMPLATE)
        result += self._write_choices(transitions)
        result += self._write_triggers(self.states[0], handlers)
        result += self._write_guards(self.states[0], transitions)
        result += self._write_states(self.sm_name, self.states[0], handlers)
        result += self._write_transitions(transitions)
        if self.has_ifelse_timers or self.has_timers:
            result += '\nHas_timers = True\n'
            if self.has_ifelse_timers:
                result += '\nHas_ifelse_timers = True\n\n'
        if self.notes_dict['init']:
            result += self._insert_string('\n# User Initializations:\n')
            result += self._insert_string('\n'.join(self.notes_dict['init'].split('\n')[1:]) + '\n')
        result += self._insert_file_template(FOOTER_TEMPLATE)
        return result

    def write_to_file(self, filename):
        with open(filename, 'w') as f:
            f.write(self.generate_code())

    @classmethod
    def _write_guard_handler(cls, from_state: str, to_state: str,
                             transition_name: str, condition: str):
        result = ""
        handler_name = "is_{}_TO_{}_{}".format(from_state, to_state,
                                               transition_name)
        result += "def {}(state, event):\n".format(handler_name)
        result += '    return ({})\n\n'.format(condition)
        return result

    @classmethod
    def _write_trigger_action(cls, from_state: str, to_state: str,
                              event_name: str, action: str):
        result = ""
        handler_name = "on_{}_TO_{}_{}".format(from_state, to_state,
                                               event_name)
        result += "def {}(state, event):\n".format(handler_name)
        result += '\n'.join(['    ' + line for line in action.split('\n')]) + "\n\n"
        return result

    def _write_choice_guards(self, source_state: State,
                             source_trigger: Trigger,
                             trigger_if: Trigger,
                             trigger_else: Trigger,
                             transitions: Dict[Tuple[str, str], Any]):
        result = ""
        source_name = source_state.name
        parent = source_state.parent.name
        base_name = source_trigger.name
        if len(base_name) == 0:
            base_name = source_name + "_CHOICE"
        trig_from = self.id_to_name[source_trigger.source]
        condition = trigger_if.guard
        assert condition and condition != 'else'

        for trigger in (trigger_if, trigger_else):
            if ((trigger.source in self.finish_nodes and
                 self.finish_nodes[trigger.source] == trigger.target)):
                # terminate edge
                trig_to = 'TERMINATE'
            else:
                trig_to = self.id_to_name[trigger.target]
            trigger_name = base_name + ("_IF" if trigger == trigger_if else "_ELSE")
            if not self.has_ifelse_timers and base_name in TIMER_EVENTS:
                self.has_ifelse_timers = True
            if base_name in self.notes_dict['tick_events']:
                self.notes_dict['tick_events'].append(trigger_name)
            key = (trig_from, trig_to)
            transitions[key] = (trigger_name,
                                True,
                                len(trigger.action) > 0,
                                parent)
            if trigger == trigger_if:
                trigger_guard = condition
            else:
                trigger_guard = "not ({})".format(condition)
            if trigger.action:
                result += self._write_trigger_action(trig_from, trig_to,
                                                     trigger_name,
                                                     trigger.action)
            result += self._write_guard_handler(trig_from, trig_to,
                                                trigger_name,
                                                trigger_guard)
        return result

    def _write_choices(self, transitions: Dict[Tuple[str, str], Any]):
        result = "\n# Choice guard hanlders & actions:\n\n"
        for c in self.choices:
            source_state = None
            source = None
            target_if = None
            target_else = None
            for s in self.states:
                for trigger in s.trigs:
                    if trigger.target == c:
                        assert trigger.type == 'choice_start'
                        source = trigger
                        source_state = s
                    elif trigger.source == c:
                        assert trigger.type == 'choice_result'
                        if trigger.guard == 'else':
                            target_else = trigger
                        else:
                            target_if = trigger
            assert source_state
            assert source
            assert target_if
            assert target_else
            result += self._write_choice_guards(source_state,
                                                source, target_if, target_else,
                                                transitions)
        return result

    def _write_triggers(self, state: State, handlers: Dict[str, Any]):
        result = "\n# Entry & Exit Handlers:\n\n"
        result += "def TERMINATE(state, event):\n"
        result += "    cpu.terminate()\n\n"
        result += self._write_triggers_recursively(state, handlers)
        return result

    @classmethod
    def _write_entry_handler(cls, state_name: str, entry_name: str, entry_code: str,
                             handlers: Dict[str, Any]):
        result = ""
        handler_name = "on_st_{}_{}".format(state_name,
                                            entry_name)
        if state_name not in handlers:
            handlers[state_name] = {}
        if entry_name not in handlers[state_name]:
            handlers[state_name][entry_name] = handler_name
        result += "def {}(state, event):\n".format(handler_name)
        result += '\n'.join(['    ' + line for line in entry_code.split('\n')])
        result += '\n\n'
        return result

    def _write_triggers_recursively(self, state: State, handlers: Dict[str, Any]):
        result = ""
        if state.entry:
            result += self._write_entry_handler(state.name, 'enter', state.entry, handlers)
        if state.exit:
            result += self._write_entry_handler(state.name, 'exit', state.exit, handlers)
        for child_state in state.childs:
            result += self._write_triggers_recursively(child_state, handlers)
        return result

    def _write_guards(self, state: State, transitions: Dict[Tuple[str, str], Any]):
        result = "\n# Transition Conditions and Actions:\n\n"
        for child_state in state.childs:
            result += self._write_guards_recursively(child_state, '', transitions)
        return result

    def _write_guards_recursively(self, state: State, parent: str,
                                  transitions: Dict[Tuple[str, str], Any]):
        result = ""

        name_to_triggers = defaultdict(list)
        name_to_position = {}

        for i, trigger in enumerate(state.trigs):

            name_to_triggers[trigger.name].append(trigger)
            name_to_position[trigger.name] = i

            trig_from = self.id_to_name[trigger.source]

            if trigger.type == 'choice_start' or trigger.type == 'choice_result':
                continue

            if trigger.type == 'external':
                if ((trigger.source in self.finish_nodes and
                     self.finish_nodes[trigger.source] == trigger.target)):
                    # terminate edge
                    trig_to = 'TERMINATE'
                else:
                    trig_to = self.id_to_name[trigger.target]
            else:
                assert trigger.type == 'internal'
                trig_to = 'None'
            key = (trig_from, trig_to)
            if not self.has_timers and trigger.name in TIMER_EVENTS:
                self.has_timers = True
            transitions[key] = (trigger.name,
                                len(trigger.guard) > 0,
                                len(trigger.action) > 0,
                                parent)

            if trigger.name:
                name = trigger.name
            elif trigger.type == 'internal':
                name = state.name + '_INT'
            else:
                name = trig_from + '_TO_' + trig_to

            if trigger.action:
                result += self._write_trigger_action(trig_from, trig_to, name, trigger.action)

            if trigger.guard:
                result += self._write_guard_handler(trig_from, trig_to, name, trigger.guard)

        for child_state in state.childs:
            result += self._write_guards_recursively(child_state, state.name, transitions)
        return result

    @classmethod
    def _write_handlers(cls, state_name: str, handlers: Dict[str, Any]):
        result = ""
        handlers_str = []
        if state_name in handlers:
            for entry, handler in handlers[state_name].items():
                handlers_str.append("'{}': {}".format(entry, handler))
            result += ("st_{}.handlers = ".format(state_name) +
                       "{" + ", ".join(handlers_str) + "}\n")
        return result

    def _write_states(self, smname: str, state: State, handlers: Dict[str, Any]):
        result = "\n\n# Hierarchical States:\n\n"
        result += "sm = pysm.StateMachine('{}')\n".format(smname)
        result += "st_initial = pysm.State('initial')\n"
        result += "sm.add_state(st_initial, initial=True)\n"
        if self.finish_nodes:
            result += "st_TERMINATE = pysm.State('TERMINATE')\n"
            result += "sm.add_state(st_TERMINATE)\n"
            result += "st_TERMINATE.handlers = {'enter': TERMINATE}\n"
        result += self._write_handlers(state.name, handlers)
        return result + self._write_states_recursively(state, "sm", False, handlers)

    @classmethod
    def _write_check_event(cls, state_name):
        result = '\n# Check incoming event function:\n\n'
        result += 'def check_event():\n'
        result += '    return {}.has_event()\n\n'.format(state_name)
        return result

    def _write_states_recursively(self, state: State, parent: str,
                                  initial: bool,
                                  handlers: Dict[str, Any]):
        result = ""
        state_name = state.name
        if state.name == 'global':
            state_name = parent
        else:
            if parent == "sm":
                result += self._write_check_event(state.name)
            state_name = "st_{}".format(state.name)
            if state.childs:
                sm_class = "StateMachine"
            else:
                sm_class = "State"
            result += "{} = pysm.{}('{}')\n".format(state_name,
                                                    sm_class,
                                                    state.name)
            result += "{}.add_state({}{})\n".format(parent,
                                                    state_name,
                                                    ", initial=True" if initial else "")
            result += self._write_handlers(state.name, handlers)
        has_initial_child = state.name in self.parents_with_start_node
        for i, child_state in enumerate(state.childs):
            if has_initial_child:
                child_is_initial = child_state.name == self.parents_with_start_node[state.name]
            else:
                child_is_initial = state.name != 'global' and i == 0
            result += self._write_states_recursively(child_state,
                                                     state_name,
                                                     child_is_initial,
                                                     handlers)
        return result

    def _write_transitions(self, transitions):
        result = "\n# On-tick Transitions:\n\n"
        result += "sm.add_transition(st_initial, st_{}, events=[Init])\n".format(self.start_node)
        for pair, value in transitions.items():
            from_state, to_state = pair
            event_name, has_guard, has_action, parent = value
            if not event_name and not has_guard and not has_action:
                continue
            if not event_name:
                if to_state != 'None':
                    event_name = from_state + '_TO_' + to_state
                else:
                    event_name = from_state + '_INT'
                event = 'Tick'
            else:
                if event_name not in self.notes_dict['tick_events']:
                    event = "'{}'".format(event_name)
                else:
                    event = 'Tick'
            parts = ["st_{}".format(from_state),
                     "st_{}".format(to_state),
                     "events=[{}]".format(event)]
            if has_guard:
                parts.append("condition=is_{}_TO_{}_{}".format(from_state,
                                                               to_state,
                                                               event_name))
            if has_action:
                parts.append("action=on_{}_TO_{}_{}".format(from_state,
                                                            to_state,
                                                            event_name))
            if to_state != 'None':
                owner = parent
            else:
                owner = from_state
            result += "st_{}.add_transition({})\n".format(owner, ', '.join(parts))
        return result

    @classmethod
    def _insert_string(cls, s: str):
        return re.sub('[ ]*\n', '\n', s)

    def _insert_file_template(self, filename: str):
        result = ''
        with open(filename) as input_file:
            for line in input_file.readlines():
                result += self._insert_string(line)
        return result
