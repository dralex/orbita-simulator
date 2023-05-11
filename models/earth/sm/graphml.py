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
graphml.py is a technical module for .graphml->.qm transator
it contains functions for analyze and transform data in .graphml file
-flatten(mixed data, key) -                                            flattens mixed_data list using key
-flatten_with_key(mixed_data: list, key: str, newkeys: dict) -> list   flattens data nodes using key
                                                                       adding new dict keys from newkeys
-get_flat_nodes(data: dict)->[dict]:                                   gets list of flattened nodes from data dict
-get_flat_edges(data: dict)->[dict]:                                   gets list of flattened edges from data dict
-get_sub_nodes(nodes: list) -> list:                                   gets all sub-nodes from groupnodes
-get_start_nodes_data(nodes: [dict]) -> int                            get data for all available start node
-get_finish_nodes_data(nodes: [dict]) -> int                           get data for all available finish nodes
-is_node_a_choice(node: dict) -> bool                                  detects if node in graphml file is a choice
-is_node_a_state(node: dict) -> bool                                   detects if node in graphml file is a state
-get_coordinates(node: dict) -> tuple                                  gets x, y, width and height of a node
-get_minmax_coord(nodes: [node]) -> tuple                              function gets the smallest/biggest x and y coord
-get_state_actions(data: dict) -> str                                  gets actions for state as a single string
-def get_group_actions(data: dict) -> str:                             get label with actions from group node data
-get_state_label(data: dict) -> str                                    gets state label from state node
-get_group_label(data: dict)-> str:                                    gets group node label from node data
-is_edge_correct(edge: dict, edge_type: str) -> bool                   checks if edge is correct
-def get_edge_coordinates(edge: dict) -> tuple                         function get edge coordinates (start as a shift
                                                                       from source state center, enf as a shift from
                                                                       source state center)
-def get_edge_label_coordinates(edge: dict) -> tuple:                  gets coordinates for edge label
"""
from typing import List, Dict, Any, Union, Tuple
edge_types = ['y:PolyLineEdge', 'y:GenericEdge']

def flatten(mixed_data: list, key: str) -> List:
    """
    function separates data nodes using key
    Example:
        flatten([{data:[info1, info2]}], data)
        [info1, info2]
    :param mixed_data: list of nodes with data
    :param key: dictionary key to get list with data
    :return: list with data items
    """
    flat_data = list()
    for node in mixed_data:
        if isinstance(node, dict) and key in node.keys():
            node_data = node[key]
            if isinstance(node_data, dict):
                flat_data.append(node_data)
            else:
                for e in node_data:
                    flat_data.append(e)
    return flat_data


def flatten_with_key(mixed_data: List[Any], key: str, newkeys: Dict[str, Any]) -> List[Any]:
    """
    function separates data nodes using key adding new dict keys from newkeys
    Example:
        flatten_with_key([{'data' : [info1, info2]}, 'id':1, 'test':'value'], 'data', {'id':'number', 'test':'data'})
        [{info1, 'number':1, 'data':'value'}, {info2, 'number':1, 'data':'value'}]
    :param mixed_data: list of nodes with data
    :param key: dictionary key to get list with data
    :param newkeys: key for additional data to extract
    :return: list with data items
    """
    flat_data: List[Any] = list()
    for node in mixed_data:
        if isinstance(node, dict) and key in node.keys():
            node_data = node[key]
            if isinstance(node_data, dict):
                for k in newkeys.keys():
                    node_data.update([(newkeys[k], node[k])])
                flat_data.append(node_data)
            else:
                for e in node_data:
                    for k in newkeys.keys():
                        e.update([(newkeys[k], node[k])])
                    flat_data.append(e)
    return flat_data


def get_sub_nodes(nodes: List[Any]) -> List[Any]:
    """
    gets all sub-nodes from groupnodes (
    detects in node has subnodes (has "graph' key) and gets all nodes in node['graph']
    item, flattened by node and by data fields
    :param nodes: list of nodes
    :return: list of nodes
    """
    group_nodes: List[Any] = [node for node in nodes if '@yfiles.foldertype' in node.keys()]
    res: List[Any] = list()
    while group_nodes:
        new: List[Any] = [node['graph'] for node in group_nodes]
        new = flatten(new, 'node')
        res.extend(new)
        group_nodes = [node for node in new if '@yfiles.foldertype' in node.keys()]
    return res


def get_flat_nodes(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    gets list of flattened nodes from data dictg
    :param data: dict with data
    :return: list of nodes
    """
    nodes: Union[List[Dict[str, Any], Dict[str, Any]]] = data['graphml']['graph']['node']
    if isinstance(nodes, dict):
        nodes = [nodes]
    nodes.extend(get_sub_nodes(nodes))
    nodes = flatten_with_key(nodes, 'data', {'@id': 'id'})
    return nodes


def update_qroup_nodes(data: List[Dict[str, Any]]):
    """
    flattens group nodes
    :param data: data with nodes
    :return:
    """
    correct = dict()
    for node in data:
        if is_node_a_group(node):
            group_nodes = node['y:ProxyAutoBoundsNode']['y:Realizers']['y:GroupNode']
            if isinstance(group_nodes, list):
                for group_node in group_nodes:
                    if group_node['y:State']['@closed'] == 'false':
                        correct = group_node
                node['y:ProxyAutoBoundsNode']['y:Realizers']['y:GroupNode'] = correct


def get_flat_edges(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    gets list of transitions from data dict
    :param data: dict with data
    :return: list of transitions
    """
    edges: List[Dict[str, Any]] = data['graphml']['graph']['edge']
    flattened_edges: List[Dict[str, Any]] = flatten_with_key(edges, 'data', {'@source': 'source', '@target': 'target'})
    return flattened_edges

def is_inside_the_node(x: int, y: int, w: int, h: int, target_node: Dict[str, Any]):
    """functions checks if the target (x, y, w, h) is inside the  node
    :param x, y, w, h: object geometry
    :param node: the node
    :return: True if the object is fully inside the node
    """
    tx, ty, tw, th = get_coordinates(target_node)
    return x >= tx and y >= ty and x + w <= tx + tw and y + h <= ty + th

def get_start_nodes_data(nodes: List[Dict[str, Any]], edges) -> List[Tuple[str, str, List[str], str]]:
    """functions gets start nodes (including the target of start edge) and raises exception if no start node found
    :param nodes: list of nodes
    :param edges: list of edges
    :return: id of start node, target of initial trigger, initial trigger action
    """
    node_ids = {}
    start_nodes = []
    for node in nodes:
        if 'y:GenericNode' in node.keys() and '@configuration' in node['y:GenericNode'].keys():
            if (node['y:GenericNode']['@configuration'] == 'com.yworks.bpmn.Event.withShadow' or
                node['y:GenericNode']['@configuration'] == 'com.yworks.bpmn.Event'):
                found_start = False
                for prop in node['y:GenericNode']['y:StyleProperties']['y:Property']:
                    if (prop['@name'] == 'com.yworks.bpmn.type' and
                        prop['@value'] == 'EVENT_TYPE_PLAIN'):
                        found_start = True
                if not found_start:
                    continue
                nid = node['id']
                x, y, w, h = get_coordinates(node)
                found = []
                for target_node in nodes:
                    if nid == target_node['id']:
                        continue
                    if is_inside_the_node(x, y, w, h, target_node):
                        found.append(target_node['id'])
                node_ids[nid] = found
    for edge in edges:
        for edge_type in edge_types:
            try:
                if edge['source'] in node_ids and len(edge.keys()) > 3:
                    if is_edge_correct(edge, edge_type) and "#text" in edge[edge_type]['y:EdgeLabel'].keys():
                        action: str = edge[edge_type]['y:EdgeLabel']["#text"]
                    else:
                        action = ""
                    start_nodes.append((edge['source'], edge['target'],
                                        node_ids[edge['source']], action))
            except KeyError:
                continue
    if start_nodes:
        return start_nodes
    raise ValueError                   # raise exception of no start node found

def get_finish_nodes_data(nodes: List[Dict[str, Any]], edges) -> List[Tuple[str, str]]:
    """functions gets start nodes (including the target of start edge) and raises exception if no start node found
    :param nodes: list of nodes
    :param edges: list of edges
    :return: id of the finish trigger, id of the finish node, finish trigger action
    """
    node_ids = {}
    finish_nodes = []
    for node in nodes:
        if 'y:GenericNode' in node.keys() and '@configuration' in node['y:GenericNode'].keys():
            if (node['y:GenericNode']['@configuration'] == 'com.yworks.bpmn.Event.withShadow' or
                node['y:GenericNode']['@configuration'] == 'com.yworks.bpmn.Event'):
                found_finish = False
                for prop in node['y:GenericNode']['y:StyleProperties']['y:Property']:
                    if (prop['@name'] == 'com.yworks.bpmn.type' and
                        prop['@value'] == 'EVENT_TYPE_TERMINATE'):
                        found_finish = True
                if not found_finish:
                    continue
                nid = node['id']
                node_ids[nid] = True
    for edge in edges:
        for edge_type in edge_types:
            try:
                if edge['target'] in node_ids and len(edge.keys()) > 3:
                    if is_edge_correct(edge, edge_type) and "#text" in edge[edge_type]['y:EdgeLabel'].keys():
                        action: str = edge[edge_type]['y:EdgeLabel']["#text"]
                    else:
                        action = ""
                    finish_nodes.append((edge['source'], edge['target']))
            except KeyError:
                continue
    if finish_nodes:
        return finish_nodes
    raise ValueError                   # raise exception of no start node found

def is_node_a_choice(node: Dict[str, Any]) -> bool:
    """
    detects if node is a choice (using @configuration key)
    :param node: dict with node
    :return: true if state otherwise false
    """
    if 'y:GenericNode' in node.keys() and '@configuration' in node['y:GenericNode'].keys():
        if node['y:GenericNode']['@configuration'] == "com.yworks.bpmn.Gateway.withShadow":
            return True
    return False


def is_node_a_state(node: Dict[str, Any]) -> bool:
    """
    detects if node is a state (using @configuration key)
    :param node: dict with node
    :return: true if state otherwise false
    """
    if 'y:GenericNode' in node.keys() and '@configuration' in node['y:GenericNode'].keys():
        if node['y:GenericNode']['@configuration'] == "com.yworks.entityRelationship.big_entity":
            return True
    return False


def is_node_a_note(node: Dict[str, Any]) -> bool:
    """
    detects is node contains start variables
    :param node: dict with node
    :return: true if start variables else false
    """
    if 'y:UMLNoteNode' in node.keys() and 'y:NodeLabel' in node['y:UMLNoteNode'].keys():
        if "#text" in node['y:UMLNoteNode']['y:NodeLabel'].keys():
            return True
    return False


def is_node_a_group(node: Dict[str, Any]) -> bool:
    """
    detects if node if group node
    :param node: dict with node
    :return: true if group else false
    """
    if 'y:ProxyAutoBoundsNode' in node.keys():
        return True
    return False


def get_note_label(node: Dict[str, Any]) -> str:
    """
    gets note_label data
    :param node:
    :return:
    """
    return node['y:UMLNoteNode']['y:NodeLabel']["#text"]


def get_coordinates(node: Dict[str, Any]) -> Tuple[int, int, int, int]:
    """
    function to get node coordinates
    :param node: node with data
    :return: (x, y, width, height)
    """
    if 'y:GenericNode' not in node.keys() and 'y:ProxyAutoBoundsNode' not in node.keys():
        return 0, 0, 0, 0
    node = node['y:GenericNode'] if 'y:GenericNode' in node.keys() else node['y:ProxyAutoBoundsNode']['y:Realizers'][
        'y:GroupNode']
    if 'y:Geometry' not in node.keys():
        return 0, 0, 0, 0
    node: Dict[str, Any] = node['y:Geometry']
    x: int = int(float(node['@x']))
    y: int = int(float(node['@y']))
    width: int = int(float(node['@width']))
    height: int = int(float(node['@height']))
    return x, y, width, height


def coord_sort(node: Dict[str, Any]) -> float:
    """
    function for sorting nodes by x
    :param node: dict with node data
    :return: x coordinates
    """
    x, _, _, _ = get_coordinates(node)
    return x


def get_minmax_coord(nodes: [dict]) -> tuple:
    """
    function gets the smallest x and y coordinate for nodes to make shift or coordinate system
    :param nodes: list of nodes
    :return: (min x, min y)
    """
    min_x, min_y, max_x, max_y = 0, 0, 0, 0
    for node in nodes:
        if 'y:GenericNode' in node.keys() or \
                ('y:ProxyAutoBoundsNode' in node.keys() and 'y:Realizers' in node['y:ProxyAutoBoundsNode'].keys()
                 and 'y:GroupNode' in node['y:ProxyAutoBoundsNode']['y:Realizers'].keys()):
            temp_node = node['y:GenericNode'] if 'y:GenericNode' in node.keys() \
                else node['y:ProxyAutoBoundsNode']['y:Realizers']['y:GroupNode']
            temp_node = temp_node['y:Geometry']
            x: int = int(float(temp_node['@x']))
            y: int = int(float(temp_node['@y']))
            w: int = int(float(temp_node['@width']))
            h: int = int(float(temp_node['@height']))
            min_x: int = min([min_x, x])
            min_y: int = min([min_y, y])
            max_x: int = max([max_x, x + w])
            max_y: int = max([max_y, y + h])
    return min_x - 1, min_y - 1, max_x + 1, max_y + 1


def get_state_actions(data: Dict[str, Any]) -> str:
    """
    get label with actions from node data
    :param data: node with data
    :return: str with actions
    """
    if 'y:GenericNode' not in data.keys() or 'y:NodeLabel' not in data['y:GenericNode'].keys():
        return ""
    data = data['y:GenericNode']
    data = flatten([data], 'y:NodeLabel')
    for label in data:
        if "#text" in label.keys() and '@configuration' in label.keys():
            if label['@configuration'] == 'com.yworks.entityRelationship.label.attributes':
                return label['#text']
    return ""


def get_group_actions(data: Dict[str, Any]) -> str:
    """
    get label with actions from group node data
    :param data: node with data
    :return: str with actions
    """
    if 'y:ProxyAutoBoundsNode' not in data.keys():
        return ""
    data = data['y:ProxyAutoBoundsNode']
    if 'y:Realizers' not in data.keys():
        return ""
    data = data['y:Realizers']
    if 'y:GroupNode' not in data.keys():
        return ""
    data = data['y:GroupNode']
    data = flatten([data], 'y:NodeLabel')
    for label in data:
        if "#text" in label.keys() and '@modelName' in label.keys():
            if label['@modelName'] == 'custom':
                return label['#text']
            if label['@alignment'] == 'left':
                return label['#text']
    return ""


def get_state_label(data: Dict[str, Any]) -> str:
    """
    gets state label from node data
    :param data: dict with data
    :return: string with label
    """
    if 'y:GenericNode' not in data.keys() or 'y:NodeLabel' not in data['y:GenericNode'].keys():
        return ""
    data = data['y:GenericNode']
    data = flatten([data], 'y:NodeLabel')
    for label in data:
        if "#text" in label.keys() and '@configuration' in label.keys():
            if label['@configuration'] == 'com.yworks.entityRelationship.label.name':
                return label['#text']
    return ""


def get_group_label(data: Dict[str, Any]) -> str:
    """
    gets group node label from node data
    :param data: dict with data
    :return: string with label
    """
    if 'y:ProxyAutoBoundsNode' not in data.keys():
        return ""
    data = data['y:ProxyAutoBoundsNode']
    if 'y:Realizers' not in data.keys():
        return ""
    data = data['y:Realizers']
    if 'y:GroupNode' not in data.keys():
        return ""
    data = data['y:GroupNode']
    data = flatten([data], 'y:NodeLabel')
    for label in data:
        if "#text" in label.keys() and '@modelName' in label.keys():
            if label['@modelName'] == 'internal':
                return label['#text']
    return ""


def is_edge_correct(edge: Dict[str, Any], edge_type: str) -> bool:
    """
    checks if edge contains all necessary data to be a correct edge with label
    :param edge: dict with edge data
    :param edge_type: type of edge:generic or curve
    :return: true if edge is generic false otherwise
    """
    if len([edge_type for edge_type in edge_types if edge_type in edge.keys()]) == 0:
        return False
    if 'y:EdgeLabel' not in edge[edge_type].keys():
        return False
    if not isinstance(edge[edge_type]['y:EdgeLabel'], dict):
        return False
    return True


def get_edge_coordinates(edge: Dict[str, Any]) -> Tuple[int, int, int, int, List[Tuple[int, int]]]:
    """
    function get edge coordinates (start as a shift from source state center, enf as a shift from source state center,
    points coordinates between them (as int)
    :param edge: dict with edge data
    :return: (first_x, first_y, last_dx, last_dy, points)
    """
    for edgetype in edge_types:
        try:
            coordinates = edge[edgetype]['y:Path']
        except KeyError:
            continue
    x: int = int(float(coordinates['@sx']))
    y: int = int(float(coordinates['@sy']))
    last_dx: int = int(float(coordinates['@tx']))
    last_dy: int = int(float(coordinates['@ty']))
    points: List[Tuple[int, int]] = list()
    if 'y:Point' in coordinates.keys():
        coordinates = [coordinates['y:Point']] if isinstance(coordinates['y:Point'], dict) else coordinates['y:Point']
        points = [(int(float(point['@x'])), int(float(point['@y']))) for point in coordinates]
    return x, y, last_dx, last_dy, points


def get_edge_label_coordinates(edge: Dict[str, Any]) -> Tuple[int, int, int]:
    """
    gets coordinates for edge label
    :param edge: dict with edge data
    :return: x, y, width of edge coordinates
    """
    for edge_type in edge_types:
        try:
            if is_edge_correct(edge, edge_type):
                label = edge[edge_type]['y:EdgeLabel']
                return int(float(label['@x'])), int(float(label['@y'])), int(float(label['@width']))
            else:
                return 0, 0, 0
        except KeyError:
            continue
