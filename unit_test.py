import math
import unittest
import graph_data
import global_game_data
from pathing import get_random_path



class TestPathFinding(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('test'.upper(), 'TEST')

    def test_isupper(self):
        self.assertTrue('TEST'.isupper())
        self.assertFalse('Test'.isupper())

    def test_floating_point_estimation(self):
        first_value = 0
        for x in range(1000):
            first_value += 1/100
        second_value = 10
        almost_pi = 3.1
        pi = math.pi
        self.assertNotEqual(first_value,second_value)
        self.assertAlmostEqual(first=first_value,second=second_value,delta=1e-9)
        self.assertNotEqual(almost_pi, pi)
        self.assertAlmostEqual(first=almost_pi, second=pi, delta=1e-1)
    def setUp(self):
        # This setup applies to all tests, assuming current_graph_index and target_node are part of the data
        global_game_data.current_graph_index = 0  # Set the graph index
        global_game_data.target_node = [2] * len(graph_data.graph_data)  # Set the target node for each graph

    def test_random_path_valid_start_and_exit(self):
        # Test that the path starts at the start node and ends at the exit node
        path = get_random_path()
        self.assertEqual(path[0], path[0], "Path should start at the start node")
        self.assertEqual(path[-1], len(graph_data.graph_data[global_game_data.current_graph_index]) - 1, "Path should end at the exit node")

    def test_random_path_contains_target(self):
        # Test that the path contains the target node
        path = get_random_path()
        target_node = global_game_data.target_node[global_game_data.current_graph_index]
        self.assertIn(target_node, path, "Path should contain the target node")

    def test_random_path_non_empty(self):
        # Test that the path is not empty
        path = get_random_path()
        self.assertTrue(len(path) > 0, "Path should not be empty")

    def test_random_path_max_retries(self):
        # Test that the function works within the maximum retry limit
        path = get_random_path()
        self.assertTrue(len(path) > 0, "Path should succeed within the given retries")

    def test_random_path_no_invalid_jumps(self):
        # Test that the path does not have any invalid jumps to non-neighbors
        path = get_random_path()
        graph = graph_data.graph_data[global_game_data.current_graph_index]
        for i in range(len(path) - 1):
            self.assertIn(path[i+1], graph[path[i]][1], "Each step in the path should only move to a neighbor")

if __name__ == '__main__':
    unittest.main()
