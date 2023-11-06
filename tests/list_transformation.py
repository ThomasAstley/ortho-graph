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
                            'edges': [{'A': 'B'}, {'B': 'C'}, {'B': 'D'}, {'C': 'D'}],
                            'edges per node': {'A': 1, 'B': 3, 'C': 2, 'D': 2}
                            }

        self.assertEqual(graph, expected_graph)
        
    def test_two_graphs(self):
        """
        Test list of nodes and edges for each graph 
        """

        file_path = 'tests/list_transformation_graph_description_2'
        
        graphs = parse_graph_descriptions(file_path)

        first_graph = graphs['Graph']

        first_expected_graph = {
                            'nodes': {'A', 'B', 'C', 'D'},
                            'edges': [{'A': 'B'}, {'B': 'C'}, {'B': 'D'}, {'C': 'D'}],
                            'edges per node': {'A': 1, 'B': 3, 'C': 2, 'D': 2}
                            }

        self.assertEqual(first_graph, first_expected_graph)
        
        # ------------------------------------

        second_graph = graphs['A']

        second_expected_graph = {
                            'nodes': {1, 'a', 2, 'b'},
                            'edges': [{1: 'a'}, {2: 'b'}],
                            'edges per node': {1: 1, 2: 1, 'a': 1, 'b': 1}
                            }

        self.assertEqual(second_graph, second_expected_graph)
        
    def test_multiple_same_edges(self):
        """
        Test list of nodes and edges with duplicates 
        """

        file_path = 'tests/AB_BA_BA_AA'
        
        graphs = parse_graph_descriptions(file_path)

        graph = graphs['Graph']

        expected_graph = {
                            'nodes': {'A', 'B', 'C', 'D'},
                            'edges': [{'A': 'A'}, {'A': 'B'}, {'B': 'A'}, {'B': 'A'}, {'B': 'C'}, {'B': 'D'}, {'C': 'D'}],
                            'edges per node': {'A': 5, 'B': 5, 'C': 2, 'D': 2}
                            }

        self.assertEqual(graph, expected_graph)
        
    def test_multiple_same_self_edges(self):
        """
        Test list of nodes and edges with duplicates 
        """

        file_path = 'tests/AB_BA_BA_AA_AA'
        
        graphs = parse_graph_descriptions(file_path)

        graph = graphs['Graph']

        expected_graph = {
                            'nodes': {'A', 'B', 'C', 'D'},
                            'edges': [{'A': 'A'}, {'A': 'A'}, {'A': 'B'}, {'B': 'A'}, {'B': 'A'}, {'B': 'C'}, {'B': 'D'}, {'C': 'D'}],
                            'edges per node': {'A': 7, 'B': 5, 'C': 2, 'D': 2}
                            }

        self.assertEqual(graph, expected_graph)
        
#complicated graphs

if __name__ == '__main__':
    unittest.main()

