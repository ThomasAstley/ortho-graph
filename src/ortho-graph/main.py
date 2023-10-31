#!/bin/env python
# License: GNU GPL version 3

import yaml

file_path = '/home/tom-kubuntu/tom/devel/ortho-graph/examples/example'

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
data = read_yaml(file_path)
graph = parse_yaml(data)
print('Graph: ', graph[0], '\nNodes: ', graph[1], '\nEdges: ', graph[2])

