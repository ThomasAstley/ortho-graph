#!/bin/env python

import unittest
import pprint
import subprocess

from src.ortho_graph.main import parse_graph_descriptions, print_graph 


class TestTransformInputGraph(unittest.TestCase):
    def test_invalid_graph_description(self):
        """
        Test invalid graph description, exits with code 10
        """
        
        file_path = 'tests/list_transformation_invalid_graph_description'
        
        ortho_graph_process = subprocess.run(['python', 'src/ortho_graph/main.py', file_path], capture_output = True)
        
        self.assertEqual(ortho_graph_process.returncode, 10)

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

        file_path = 'tests/list_transformation_graph_description_2'
        
        graphs = parse_graph_descriptions(file_path)

        first_graph = graphs['Graph']

        first_expected_graph = {
                            'nodes': {'A', 'B', 'C', 'D'},
                            'edges': [{'A': 'B'}, {'B': 'C'}, {'B': 'D'}, {'C': 'D'}]
                            }

        self.assertEqual(first_graph, first_expected_graph)
        
        # ------------------------------------

        second_graph = graphs['A']

        second_expected_graph = {
                            'nodes': {1, 'a', 2, 'b'},
                            'edges': [{1: 'a'}, {2: 'b'}]
                            }

        self.assertEqual(second_graph, second_expected_graph)
        
#complicated graphs

if __name__ == '__main__':
    unittest.main()

