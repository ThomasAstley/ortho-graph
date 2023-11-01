#!/bin/env python

import unittest
import pprint

from src.ortho_graph.main import parse_graph_descriptions, print_graph 


class TestTransformInputGraph(unittest.TestCase):

    def test_simple_graph(self):
        """
        Test list of nodes and edges 
        """

        file_path = 'tests/list_transformation_graph_description_1'
        
        graphs = parse_graph_descriptions(file_path)

        graph = graphs['Graph']

        expected_graph = {
                            'nodes': {'A', 'B', 'C', 'D'},
                            'edges': [{'A': 'B'}, {'B': 'C'}, {'B': 'D'}, {'C': 'D'}]
                            }

        self.assertEqual(graph, expected_graph)
        
#new test two graphs

    def test_two_graphs(self):
        """
        Test list of nodes and edges for each graph 
        """

        file_path = 'examples/two_graphs'
        
        graphs = parse_graph_descriptions(file_path)
        # pprint(graphs)

        first_graph = graphs['Graph']
        first_nodes = first_graph['nodes']
        first_edges = first_graph['edges']
        
        first_expected_nodes = {'A', 'B', 'C', 'D'}
        first_expected_edges = [{'A': 'B'}, {'B': 'C'}, {'B': 'D'}, {'C': 'D'}]

        self.assertEqual(first_nodes, first_expected_nodes)
        self.assertEqual(first_edges, first_expected_edges)

        # ------------------------------------

        second_graph = graphs['A']
        second_nodes = second_graph['nodes']
        second_edges = second_graph['edges']
        
        second_expected_nodes = {1, 'a', 2, 'b'}
        second_expected_edges = [{1: 'a'}, {2: 'b'}]

        self.assertEqual(second_nodes, second_expected_nodes)
        self.assertEqual(second_edges, second_expected_edges)

#complicated graphs

if __name__ == '__main__':
    unittest.main()

