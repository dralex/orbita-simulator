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

from dataclasses import dataclass
from typing import List, Tuple, Optional

"""
   Class Trigger describes Triggers of uml-diagrams
        name: name of trigger
        type: internal or external
        guard: text of trigger guard if any
        source: source state of trigger (actual for external triggers)
        target: target state of trigger (actual for external triggers)
        action: action for this trigger if any
        id: order number of internal trigger for better coordinates
        x, y: start of trigger visual path
        dx, dy: first relative movement of trigger visual path
        points: other relative movements of trigger visual path
        action_x, action_y, action_width: coordinates of trigger label
"""


@dataclass
class Trigger:
    name: str
    source: str
    target: str
    action: str
    id: int
    x: int
    y: int
    dx: int
    dy: int
    points: List[Tuple[int, int]]
    action_x: int
    action_y: int
    action_width: int
    type: str = "internal"
    guard: str = ""


"""
   class State describes state of uml-diagram and trigslates to qm format.
   Fields:
        name: name of state
        type: state or choice
        trigs: list of trigsitions from this state both external and internal
        entry: action on entry event
        exit: action on exit event
        id: number of state
        actions: raw_data for external actions
        old_id: id of state in graphml
        x, y: graphical coordinates
        height, width: height and with of node
"""


@dataclass
class State:
    name: str
    type: str
    actions: str
    trigs: List[Trigger]
    entry: str
    exit: str
    id: str
    new_id: List[str]
    x: int
    y: int
    width: int
    height: int
    parent: Optional['State']
    childs: List['State']
