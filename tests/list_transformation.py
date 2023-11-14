#!/bin/env python

import unittest
import pprint
import subprocess

from src.ortho_graph.main import parse_graph_descriptions, print_graph, place_nodes  


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
                            'edges': [{'A': 'B'}, {'B': 'C'}, {'B': 'D'}, {'C': 'D'}],
                            'nodes': {'A': ['B'], 'B': ['A', 'C', 'D'], 'C': ['B', 'D'], 'D': ['B', 'C']},
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
            'edges': [{'A': 'B'}, {'B': 'C'}, {'B': 'D'}, {'C': 'D'}],
            'nodes': {'A': ['B'], 'B': ['A', 'C', 'D'], 'C': ['B', 'D'], 'D': ['B', 'C']},
            })

        # ------------------------------------

        self.assertEqual(
            graphs['A'],
            {
            'edges': [{1: 'a'}, {2: 'b'}],
            'nodes': {1: ['a'], 'a': [1], 2: ['b'], 'b': [2]},
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
                'edges': [{'A': 'A'}, {'A': 'B'}, {'B': 'A'}, {'B': 'A'}, {'B': 'C'}, {'B': 'D'}, {'C': 'D'}],
                'nodes': {'A': ['A', 'A', 'B', 'B', 'B'], 'B': ['A', 'A', 'A', 'C', 'D'], 'C':['B', 'D'], 'D':['B', 'C']}
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
                'edges': [{'A': 'A'}, {'A': 'A'}, {'A': 'B'}, {'B': 'A'}, {'B': 'A'}, {'B': 'C'}, {'B': 'D'}, {'C': 'D'}],
                'nodes': {'A': ['A', 'A', 'A', 'A', 'B', 'B', 'B'], 'B': ['A', 'A', 'A', 'C', 'D'], 'C':['B', 'D'], 'D':['B', 'C']}
                })

    def test_node_placement(self):
        """
        Test node placement for simple graph
        """
        
        graphs = parse_graph_descriptions({
                                            'Graph': 
                                              { 
                                              'A': [ 'B' ],
                                              'B': [ 'C', 'D' ],
                                              'C': [ 'D' ]
                                              }
                                            })
        
        place_nodes(graphs)

        self.assertEqual(
                graphs['Graph'],
                {
                'edges': [{'A': 'B'}, {'B': 'C'}, {'B': 'D'}, {'C': 'D'}],
                'nodes': {'A': ['B'], 'B': ['A', 'C', 'D'], 'C':['B', 'D'], 'D':['B', 'C']},
                'placed nodes':{'A': (0, 0), 'B': (0, 3), 'C': (0, 6), 'D': (3, 3)}
                })

    def test_node_placement_many_edges(self):
        """
        Test node placement for a node with many edges
        """

        graphs = parse_graph_descriptions({
                                            'Graph':
                                                {
                                                'A': [1, 2, 3, 4, 5, 6, 7, 8, 9]
                                                }
                                            })

        place_nodes(graphs)

        self.assertEqual(
            graphs['Graph'],
            {
            'edges': [   {'A': 1}, {'A': 2}, {'A': 3}, {'A': 4}, {'A': 5}, {'A': 6}, {'A': 7}, {'A': 8}, {'A': 9}],
            'nodes': {   1: ['A'], 2: ['A'], 3: ['A'], 4: ['A'], 5: ['A'], 6: ['A'], 7: ['A'], 8: ['A'], 9: ['A'], 'A': [1, 2, 3, 4, 5, 6, 7, 8, 9]},
            'placed nodes': {   1: (0, 3), 2: (3, 0), 3: (0, -3), 4: (-3, 0), 5: (0, 6), 6: (6, 0), 7: (0, -6), 8: (-6, 0), 9: (0, 9), 'A': (0, 0)}
            })



if __name__ == '__main__':
    unittest.main()

