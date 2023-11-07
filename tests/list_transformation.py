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



    def test_valid_graph_description(self):
        """
        Test valid graph description, exits with code 0
        """

        file_path = 'tests/AB_BC_BD_CD'
        
        ortho_graph_process = subprocess.run(['python', 'src/ortho_graph/main.py', file_path], capture_output = True)
        
        self.assertEqual(ortho_graph_process.returncode, 0)



    def test_parse_simple_graph(self):
        """
        Test simple list of nodes and edges 
        """

        graph_descriptions = {
                                'Graph': 
                                  { 
                                  'A': [ 'B' ],
                                  'B': [ 'C', 'D' ],
                                  'C': [ 'D' ]
                                  }
                                }

        graphs = parse_graph_descriptions(graph_descriptions)

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

        graph_descriptions = {
                                'Graph': 
                                  { 
                                  'A': [ 'B' ],
                                  'B': [ 'C', 'D' ],
                                  'C': [ 'D' ]
                                  },

                                'A': 
                                  { 
                                  1: [ 'a' ],
                                  2: [ 'b' ], 
                                  }
                                }

        graphs = parse_graph_descriptions(graph_descriptions)

        # ------------------------------------

        self.assertEqual(
            graphs['Graph'],
            {
            'nodes': {'A', 'B', 'C', 'D'},
            'edges': [{'A': 'B'}, {'B': 'C'}, {'B': 'D'}, {'C': 'D'}],
            'edges per node': {'A': 1, 'B': 3, 'C': 2, 'D': 2}
            })

        # ------------------------------------

        self.assertEqual(
            graphs['A'],
            {
            'nodes': {1, 'a', 2, 'b'},
            'edges': [{1: 'a'}, {2: 'b'}],
            'edges per node': {1: 1, 2: 1, 'a': 1, 'b': 1}
            })

        
    def test_multiple_same_edges(self):
        """
        Test list of nodes and edges with duplicates 
        """

        graph_descriptions = {
                            'Graph': 
                              { 
                              'A': [ 'A', 'B' ],
                              'B': [ 'A', 'A', 'C', 'D' ],
                              'C': [ 'D' ]
                              }
                            }

        graphs = parse_graph_descriptions(graph_descriptions)

        self.assertEqual(
                graphs['Graph'],
                {
                'nodes': {'A', 'B', 'C', 'D'},
                'edges': [{'A': 'A'}, {'A': 'B'}, {'B': 'A'}, {'B': 'A'}, {'B': 'C'}, {'B': 'D'}, {'C': 'D'}],
                'edges per node': {'A': 5, 'B': 5, 'C': 2, 'D': 2}
                })

        
    def test_multiple_same_self_edges(self):
        """
        Test list of nodes and edges with duplicates 
        """

        graph_descriptions = {
                                'Graph': 
                                  { 
                                  'A': [ 'A', 'A', 'B' ],
                                  'B': [ 'A', 'A', 'C', 'D' ],
                                  'C': [ 'D' ]
                                  }
                                }

        graphs = parse_graph_descriptions(graph_descriptions)

        self.assertEqual(
                graphs['Graph'],
                {
                'nodes': {'A', 'B', 'C', 'D'},
                'edges': [{'A': 'A'}, {'A': 'A'}, {'A': 'B'}, {'B': 'A'}, {'B': 'A'}, {'B': 'C'}, {'B': 'D'}, {'C': 'D'}],
                'edges per node': {'A': 7, 'B': 5, 'C': 2, 'D': 2}
                })

        

if __name__ == '__main__':
    unittest.main()

