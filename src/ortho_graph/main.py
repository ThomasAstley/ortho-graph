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
        edges_per_node = {}
        discovered_node_names = {*graph}
        edges_per_node = dict.fromkeys( graph.keys(), 0 )
        connected_nodes = dict()        

        for node_name in graph:
            node = graph[node_name]

            if connected_nodes.get(node_name) == None:
                connected_nodes[node_name] = []

            for target_node_name in node:
                edges.append({node_name: target_node_name})
                edges_per_node[node_name] += 1

                if connected_nodes.get(target_node_name) == None:
                    connected_nodes[target_node_name] = []

                connected_nodes[node_name].append(target_node_name)

                if target_node_name not in discovered_node_names:
                    discovered_node_names.add(target_node_name)
                    edges_per_node[target_node_name] = 1
                    connected_nodes[target_node_name].append(node_name)

                else:
                    edges_per_node[target_node_name] += 1
                    connected_nodes[target_node_name].append(node_name)
        
        for node_name in discovered_node_names.difference({*graph}):
            graph[node_name] = []


        graphs[graph_name] = {
            'nodes': {*graph},
            'edges': edges,
            'edges per node': dict(sorted(edges_per_node.items(), key = lambda item: item[1], reverse = True)),
            'connected nodes': connected_nodes
            } 

    return graphs 

def print_graph(data):
    pt = PrettyPrintTree()
    pt.print_json(data, orientation=PrettyPrintTree.Horizontal)


def place_nodes(graphs):
    
    pp = pprint.PrettyPrinter(indent=4)

    for graph in graphs.values():
    
        used_coordinates = set()
        placed_nodes = {}
        offsets = [(0,3), (3,0), (0,-3), (-3,0)]

        for node_name, connections in graph['edges per node'].items():
                
            used_coordinates.add((0,0))
            placed_nodes[node_name] = (0,0)
            node_edges = []

            for edge in graph['edges']:
                print('edge: ', end='')
                pp.pprint(edge)

                for src_node, dst_node in edge.items():

                    if src_node == node_name:
                        node_edges.append(src_node) 

                    if dst_node == node_name:
                        node_edges.append(dst_node)

            if connections <= 4:
                for position, dst_node in enumerate(node_edges):

                    dst_node_coordinate = (
                                            placed_nodes[node_name][0] + offsets[position][0],
                                            placed_nodes[node_name][1] + offsets[position][1]
                                            )

                    used_coordinates.add(dst_node_coordinate)
                   
                    placed_nodes[dst_node] = dst_node_coordinate

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

