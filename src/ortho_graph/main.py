#!/bin/env python
# License: GNU GPL version 3

import sys
import yaml
from PrettyPrint import PrettyPrintTree

def parse_graph_descriptions(file_path):
    with open(file_path) as stream:
        try:
            graph_descriptions = yaml.safe_load(stream)
        except yaml.YAMLError as exception:
            print(exception)
            exit(10)

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

        graphs[graph_name] = {'nodes': {*graph},'edges': edges, 'edges per node': edges_per_node} 

    return graphs 

def print_graph(data):
    pt = PrettyPrintTree()
    pt.print_json(data, orientation=PrettyPrintTree.Horizontal)

def obtain_node_placement_orders(graphs):
    placement_orders = {}

    for graph in graphs:
        placement_order = []
        placement_order = sorted(graphs[graph]['edges per node'], key = lambda x: graphs[graph]['edges per node'][x], reverse = True)
        placement_orders[graph] = placement_order

    return placement_orders

#def obtain_node_placements(graphs):
#    node_placements = {}
#
#    for graph in graphs:
#        number_of_nodes = len(graphs[graph]['nodes'])














def main():
    if len(sys.argv) != 2:
        print("Usage: ortho-graph graph_description.yaml")
        exit(2)
    else:
        # Access the command line arguments
        file_path = sys.argv[1]

    graphs = parse_graph_descriptions(file_path)
    print('Graphs: ', graphs)
    placement_orders = obtain_node_placement_orders(graphs)
    print('placement orders: ', placement_orders)
    #pt = PrettyPrintTree()
    #pt.print_json(graphs, orientation=PrettyPrintTree.Horizontal)

if __name__ == '__main__':
    main()

