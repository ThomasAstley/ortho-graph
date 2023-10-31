#!/bin/env python

import unittest

from src.ortho_graph.main import parse_graph_descriptions, print_graph 


class TestTransformInputGraph(unittest.TestCase):

    def test_simple_graph(self):
        """
        Test list of nodes and edges 
        """

        file_path = '/home/tom-kubuntu/tom/devel/ortho-graph/examples/simple_graph'
        
        graphs = parse_graph_descriptions(file_path)
        print_graph(graphs)

        graph = graphs['Graph']
        nodes = graph['nodes']
        edges = graph['edges']

        expected_nodes = ['A', 'B', 'C', 'D']
        expected_edges = [{'A': 'B'}, {'B': 'C'}, {'B': 'D'}, {'C': 'D'}]

        self.assertEqual(nodes, expected_nodes)
        self.assertEqual(edges, expected_edges)
        
#new test two graphs

#complicated graphs

if __name__ == '__main__':
    unittest.main()

