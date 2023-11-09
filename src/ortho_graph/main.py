#!/bin/env python
# License: GNU GPL version 3

import sys
import yaml
from PrettyPrint import PrettyPrintTree

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
        edges_per_node = {}
        discovered_node_names = {*graph}
        edges_per_node = dict.fromkeys( graph.keys(), 0 )

        for node_name in graph:
            node = graph[node_name]

            for target_node_name in node:
                edges.append({node_name: target_node_name})
                edges_per_node[node_name] += 1

                if target_node_name not in discovered_node_names:
                    discovered_node_names.add(target_node_name)
                    edges_per_node[target_node_name] = 1
                else:
                    edges_per_node[target_node_name] += 1
        
        for node_name in discovered_node_names.difference({*graph}):
            graph[node_name] = []


        graphs[graph_name] = {
            'nodes': {*graph},
            'edges': edges,
            'edges per node': dict(sorted(edges_per_node.items(), key = lambda item: item[1], reverse = True))
            } 

    return graphs 

def print_graph(data):
    pt = PrettyPrintTree()
    pt.print_json(data, orientation=PrettyPrintTree.Horizontal)


def obtain_node_placements(graphs):
    
    for graph in graphs:
        unique_node_coordinates = set()
        nodes_with_coordinates = {}
        add_to_coordinates = [(0,3), (3,0), (0,-3), (-3,0)]

        first_node, first_node_number_of_connections = next(iter(graphs[graph]['edges per node'].items()))

        unique_node_coordinates.add((0,0))
        nodes_with_coordinates[first_node] = (0,0)
       
        connected_nodes = [d[first_node] for d in graphs[graph]['edges'] if first_node in d]
        connected_nodes = connected_nodes + [key for d in graphs[graph]['edges'] if any(first_node == v for v in d.values()) for key, value in d.items() if value == first_node]

        if first_node_number_of_connections <= 4:
            for position, node in enumerate(connected_nodes):
                node_coordinates = (nodes_with_coordinates[first_node][0] + add_to_coordinates[position][0],
                nodes_with_coordinates[first_node][1] + add_to_coordinates[position][1])
                unique_node_coordinates.add(node_coordinates)
                nodes_with_coordinates[node] = node_coordinates

        print('Nodes with their assigned coordinates', nodes_with_coordinates )


def main():
    if len(sys.argv) != 2:
        print("Usage: ortho-graph graph_description.yaml")
        exit(2)
    else:
        # Access the command line arguments
        file_path = sys.argv[1]

    graphs = load_graphs(file_path)
    obtain_node_placements(graphs)
    print(graphs)
    #pt = PrettyPrintTree()
    #pt.print_json(graphs, orientation=PrettyPrintTree.Horizontal)

if __name__ == '__main__':
    main()

