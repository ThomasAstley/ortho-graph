#!/bin/env python
# License: GNU GPL version 3

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
import graph
import algorithm.annealing
import asciio


def main():
    parser = OptionParser()

    parser.add_option("-f", "--file", dest="file_path", metavar="graph_description.yaml")
    parser.add_option("--json",       dest="json", help="Output json to stdout")

    (options, args) = parser.parse_args()

    if options.file_path is None:
        print("Usage: ortho-graph graph_description.yaml")
        exit(2)

    graphs = graph.load_graphs(options.file_path)

    algorithm.annealing.place_nodes(graphs)

    if options.json:
        generate_json(graphs)
    

if __name__ == '__main__':
    main()
