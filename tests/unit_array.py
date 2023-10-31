#!/bin/env python

import unittest

from src.ortho-graph.main import process_array 


class TestProcessArray(unittest.TestCase):
    def _test_setup(self, argument):
        print('Doing setup with argument "', argument,'"')

    def test_process_array(self):
        """
        Test that process array removal of command line arguments
        """
        self._test_setup(1)
        self.assertEqual(process_array([]), [], 'empty array')
        self.assertEqual(process_array(['to be removed', 1, 2, 3]), [1, 2, 3], 'remove first element')
        self.assertEqual(process_array(['to be removed', 1, 2, 3, '--', 'to be removed']), [1, 2, 3], 'remove elements from --')


if __name__ == '__main__':
    unittest.main()

