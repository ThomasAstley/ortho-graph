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
from   constants              import X_AXIS, Y_AXIS


def load_graphs(file_path):
    with open(file_path) as stream:
        try:
            graph_descriptions = yaml.safe_load(stream)
        except yaml.YAMLError as exception:
            print(exception)
            exit(10)
    
    return parse_graph_descriptions(graph_descriptions)


def parse_graph_descriptions(graph_descriptions):
    graphs = {}

    for graph_name in graph_descriptions:
        graphs[graph_name]    = {} 

        graph                 = graph_descriptions[graph_name]

        discovered_node_names = {*graph}
        connected_nodes       = dict()

        for node_name in graph:
            node = graph[node_name]

            if connected_nodes.get(node_name) == None:
                connected_nodes[node_name] = []

            for target_node_name in node:
                if connected_nodes.get(target_node_name) == None:
                    connected_nodes[target_node_name] = []

                connected_nodes[node_name].append(target_node_name)

                if target_node_name not in discovered_node_names:
                    discovered_node_names.add(target_node_name)
                    connected_nodes[target_node_name].append(node_name)
                else:
                    connected_nodes[target_node_name].append(node_name)
        
        for node_name in discovered_node_names.difference({*graph}):
            graph[node_name] = []

        for node_name in discovered_node_names:
            node = {'name': node_name, 
                    'edges': list(graph[node_name]),
                    'neighbours': connected_nodes[node_name]}

            graphs[graph_name][node_name] = node 

    return graphs 


def print_graph(data):
    pt = PrettyPrintTree()
    pt.print_json(data, orientation=PrettyPrintTree.Horizontal)


def canonize_node_positions(graph):
    min_x = 0
    min_y = 0
    
    for node_name in graph:
        if graph[node_name]['position'][X_AXIS] < min_x: min_x = graph[node_name]['position'][X_AXIS]
        if graph[node_name]['position'][Y_AXIS] < min_y: min_y = graph[node_name]['position'][Y_AXIS]

    for node_name in graph:
        graph[node_name]['position'][X_AXIS] -= min_x
        graph[node_name]['position'][Y_AXIS] -= min_y

