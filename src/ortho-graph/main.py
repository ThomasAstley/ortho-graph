#!/bin/env python
# License: GNU GPL version 3

import yaml
import sys

def read_yaml(file_path):
    with open(file_path) as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

def parse_yaml(data):
    g = []
    n = []
    e = []
    for graph in data:
        g.append(graph)
        for node in data[graph]:
            n.append(node)
            for edge in data[graph][node]:
                e.append(node + edge)
            
    return g, n, e

def main():
    if len(sys.argv) != 2:
        print("Usage: ortho-graph graph_description.yaml")
        exit(2)
    else:
        # Access the command line arguments
        file_path = sys.argv[1]

    data = read_yaml(file_path)
    graph = parse_yaml(data)
    print('Graph: ', graph[0], '\nNodes: ', graph[1], '\nEdges: ', graph[2])

main()
