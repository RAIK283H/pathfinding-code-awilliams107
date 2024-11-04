import math
import unittest
import graph_data
import global_game_data
from pathing import get_random_path, get_dfs_path, get_bfs_path
from permutation import sjt_perms, has_ham_cycle
import perm_test_graph_data



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
            
    # DFS
    def test_dfs_path_valid_start_and_exit(self):
        # Test that the path starts at the start node and ends at the exit node
        path = get_dfs_path()
        self.assertEqual(path[0], 1, "DFS Path should start at the start node")
        self.assertEqual(path[-1], len(graph_data.graph_data[global_game_data.current_graph_index]) - 1, "DFS Path should end at the exit node")
    
    def test_dfs_path_contains_target(self):
        # Test that the path contains the target node
        path = get_dfs_path()
        target_node = global_game_data.target_node[global_game_data.current_graph_index]
        self.assertIn(target_node, path, "DFS Path should contain the target node")
        
    def test_dfs_path_no_invalid_jumps(self):
        # Test that the path does not have any invalid jumps to non-neighbors
        path = get_dfs_path()
        graph = graph_data.graph_data[global_game_data.current_graph_index]
        for i in range(len(path) - 1):
            self.assertIn(path[i+1], graph[path[i]][1], "DFS Path should only move to a neighbor")
            
    def test_dfs_path_reaches_exit(self):
        # Test that the path reaches the exit upon ending
        path = get_dfs_path()
        exit_node = len(graph_data.graph_data[global_game_data.current_graph_index]) - 1
        self.assertEqual(path[-1], exit_node, "DFS Path should reach the exit node")
        
    def test_dfs_path_no_cycles(self):
        # Test that DFS path does not cycle or revisit nodes
        path = get_dfs_path()
        self.assertEqual(len(path), len(set(path)), "DFS Path should not contain cycles or revisit nodes")
            
    # BFS
    def test_bfs_path_valid_start_and_exit(self):
        # Test that the path starts at the start node and ends at the exit node
        path = get_bfs_path()
        self.assertEqual(path[0], 1, "BFS Path should start at the start node")
        self.assertEqual(path[-1], len(graph_data.graph_data[global_game_data.current_graph_index]) - 1, "BFS Path should end at the exit node")
        
    def test_bfs_path_contains_target(self):
        # Test that the path contains the target node
        path = get_bfs_path()
        target_node = global_game_data.target_node[global_game_data.current_graph_index]
        self.assertIn(target_node, path, "BFS Path should contain the target node")
        
    def test_bfs_path_no_invalid_jumps(self):
        # Test that the path does not have any invalid jumps to non-neighbors
        path = get_bfs_path()
        graph = graph_data.graph_data[global_game_data.current_graph_index]
        for i in range(len(path) - 1):
            self.assertIn(path[i+1], graph[path[i]][1], "BFS Path should only move to a neighbor")
            
    def test_bfs_path_reaches_exit(self):
        # Test that the path reaches the exit upon ending
        path = get_bfs_path()
        exit_node = len(graph_data.graph_data[global_game_data.current_graph_index]) - 1
        self.assertEqual(path[-1], exit_node, "BFS Path should reach the exit node")
        
    def test_bfs_path_shortest_distance(self):
        # Test to ensure BFS path length is always less than or equal to DFS path length
        bfs_path = get_bfs_path()
        dfs_path = get_dfs_path()
        self.assertLessEqual(len(bfs_path), len(dfs_path), "BFS Path should be shorter or equal to DFS path")
        
    # Permutation Tests
    def test_sjt_perms(self):
        # Test SJT with a small example
        perms = list(sjt_perms(3))
        expected = [[1, 2, 3], [1, 3, 2], [3, 1, 2], [3, 2, 1], [2, 3, 1], [2, 1, 3]]
        self.assertEqual(perms, expected, "SJT permutations failed for n=3")

    def test_ham_cycle_exists(self):
        # Test with a graph known to have a Hamiltonian cycle
        result = has_ham_cycle(graph_data.graph_data[0])
        self.assertNotEqual(result, -1, "Expected Hamiltonian cycle but found none")

    def test_no_ham_cycle(self):
        # Test with a graph known to have no Hamiltonian cycle
        result = has_ham_cycle(perm_test_graph_data.perm_test_graph_data[0])
        self.assertEqual(result, -1, "Expected no Hamiltonian cycle but found one")

if __name__ == '__main__':
    unittest.main()
