#!/bin/env python
# License: GNU GPL version 3

import sys
import yaml
# from PrettyPrint import PrettyPrintTree
import pprint

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
        graph = graph_descriptions[graph_name]

        edges = []
        discovered_node_names = {*graph}
        connected_nodes = dict()        

        for node_name in graph:
            node = graph[node_name]

            if connected_nodes.get(node_name) == None:
                connected_nodes[node_name] = []

            for target_node_name in node:
                edges.append({node_name: target_node_name})

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


        graphs[graph_name] = {
            'edges': edges,
            'nodes': connected_nodes
            } 

    return graphs 

def print_graph(data):
    pt = PrettyPrintTree()
    pt.print_json(data, orientation=PrettyPrintTree.Horizontal)

def new_coordinate(src_coordinate, node_name, used_coordinates):
    
    offsets = [(0,3), (3,0), (0,-3), (-3,0)]

    new_coordinate = src_coordinate
    offset_index = 0

    while new_coordinate in used_coordinates:
        new_coordinate = ( src_coordinate[0] + offsets[offset_index][0], src_coordinate[1] + offsets[offset_index][1])
        offset_index += 1
        
        if offset_index > 3:
            for position, offset in enumerate(offsets):
                if offset[0] > 0:
                    offset_x = offset[0] + 3
                elif offset[0] < 0:
                    offset_x = offset[0] - 3
                else:
                    offset_x = 0

                if offset[1] > 0:
                    offset_y = offset[1] + 3
                elif offset[1] < 0:
                    offset_y = offset[1] - 3
                else:
                    offset_y = 0

                offsets[position] = (offset_x, offset_y)

            offset_index = 0

    return new_coordinate

def place_nodes(graphs):
    
    pp = pprint.PrettyPrinter(indent=4)

    for graph in graphs.values():
    
        used_coordinates = set()
        placed_nodes = {}
        offsets = [(0,3), (3,0), (0,-3), (-3,0)]

        for node_name, connected_nodes in graph['nodes'].items():
            if placed_nodes.get(node_name) == None:
                node_coordinate = new_coordinate((0, 0), node_name, used_coordinates)

                placed_nodes[node_name] = node_coordinate
                used_coordinates.add(node_coordinate)
            
            for connected_node in connected_nodes:
                if placed_nodes.get(connected_node) == None:
                    connected_node_coordinates = new_coordinate(placed_nodes[node_name], connected_node, used_coordinates)

                    placed_nodes[connected_node] = connected_node_coordinates
                    used_coordinates.add(connected_node_coordinates)
                   

        graph['placed nodes'] = placed_nodes


def main():
    if len(sys.argv) != 2:
        print("Usage: ortho-graph graph_description.yaml")
        exit(2)
    else:
        # Access the command line arguments
        file_path = sys.argv[1]

    pp = pprint.PrettyPrinter(indent=4)

    graphs = load_graphs(file_path)

    place_nodes(graphs)
    
    pp.pprint(graphs)
    #pt = PrettyPrintTree()
    #pt.print_json(graphs, orientation=PrettyPrintTree.Horizontal)

if __name__ == '__main__':
    main()

