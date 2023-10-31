#!/bin/env python
# License: GNU GPL version 3

import sys
import yaml
from PrettyPrint import PrettyPrintTree

def parse_graph_description(file_path):
    with open(file_path) as stream:
        try:
            data = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    
    pt = PrettyPrintTree()
    pt.print_json(data, orientation=PrettyPrintTree.Horizontal)

    g = {}

    for graph in data:
        n = []
        e = []

        for node in data[graph]:
            n.append(node)

            for target_node in data[graph][node]:
                e.append({node: target_node})

        g[graph] = {'nodes': n,'edges': e} 
        
    return g 

def main():
    if len(sys.argv) != 2:
        print("Usage: ortho-graph graph_description.yaml")
        exit(2)
    else:
        # Access the command line arguments
        file_path = sys.argv[1]

    graph = parse_graph_description(file_path)
    #print('Graphs: ', graph)
    pt = PrettyPrintTree()
    pt.print_json(graph, orientation=PrettyPrintTree.Horizontal)

main()
