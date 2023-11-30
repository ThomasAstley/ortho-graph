
import sys
import yaml
import pprint
import json
import statistics
import numpy as np
import random
import copy
import subprocess

from   optparse               import OptionParser
import constants

import time
import requests


def display_graph(graph, grid_upper_boundary, current_node, median_x, median_y):
    script = bytes("select_all_elements ; delete_selected_elements ;", 'utf-8')

    info = {}
    info['node']     = current_node
    info['median_x'] = median_x
    info['median_y'] = median_y

    pp = pprint.PrettyPrinter(indent=1, width=20, sort_dicts=False)
    script += bytes(
                ("add 'info', new_text(TEXT_ONLY =>\"%s\"), 30, 0 ;\n") % (pp.pformat(info))
                , 'utf-8')

    script += graph_to_asciio_script(graph, grid_upper_boundary, 0)

    median_node = {}
    median_node['x'] = {'name': 'x', 'position': [median_x, median_y]}

    script += graph_to_asciio_script(median_node, grid_upper_boundary, 0)
    script += bytes("select_by_name 'x' ;", 'utf-8')
    script += bytes("change_selected_elements_color 0, [1, 0, 0] ;", 'utf-8')
    script += bytes("deselect_all_elements 'x' ;", 'utf-8')
    
    # subprocess.run(["xh", "-f", "POST", "http://localhost:4444/script",  bytes("script=", 'utf-8') + script])

    answer = requests.post('http://localhost:4444/script', data = {'script': script, 'show_script': 0})
    time.sleep(0.002)


def graph_to_asciio_script(graph, boundary, box):
    object_type = 'new_box' if box else 'new_text'

    script = bytes(
                "create_undo_snapshot ;\n" +
                "delete_all_ruler_lines ;\n" +
                "add_ruler_line 'vertical',"   + str(boundary)     + ";\n" +
                "add_ruler_line 'horizontal'," + str(boundary + 1) + ";\n", 'utf-8') 

    for node in graph.values():
        position  = node['position']
        node_name = node['name']

        script += bytes(
                    ("add '%s', " + object_type + "(TEXT_ONLY =>'%s'), %d, %d ;\n") % 
                        (node_name, node_name, position[0] + boundary, -position[1] + boundary ), 
                    'utf-8')

    return script



def canonize_graphs_placed_nodes(graphs):
    for graph in graphs.values():
        canonize_node_positions(graph)


def map_node_positions(graph, grid_upper_boundary):
    for node_name in graph:
        graph[node_name]['position'][X_AXIS] += grid_upper_boundary
        graph[node_name]['position'][Y_AXIS] += grid_upper_boundary


