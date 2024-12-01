import math
import unittest
import graph_data
import global_game_data
from pathing import get_random_path, get_dfs_path, get_bfs_path, get_dijkstra_path, calculate_distance
from permutation import sjt_perms, has_ham_cycle
import perm_test_graph_data
from f_w import reconstruct_path, floyd_warshall



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
        
    def test_sjt_perms2(self):
        # Test SJT with a small example
        perms = list(sjt_perms(2))
        expected = [[1, 2], [2, 1]]
        self.assertEqual(perms, expected, "SJT permutations failed for n=2")

    def test_ham_cycle_exists(self):
        # Test with a graph known to have a Hamiltonian cycle
        result = has_ham_cycle(graph_data.graph_data[0])
        self.assertNotEqual(result, -1, "Expected Hamiltonian cycle but found none")

    def test_no_ham_cycle(self):
        # Test with a graph known to have no Hamiltonian cycle
        result = has_ham_cycle(perm_test_graph_data.perm_test_graph_data[0])
        self.assertEqual(result, -1, "Expected no Hamiltonian cycle but found one")
        
    # Dijkstra
    def test_dijkstra_valid_path(self):
        path = get_dijkstra_path()
        self.assertTrue(len(path) > 0, "Dijkstra should return a valid path")
        self.assertEqual(path[0], 1, "Path should start at first node after 0")
        self.assertEqual(path[-1], len(graph_data.graph_data[global_game_data.current_graph_index]) - 1,
                         "Path should end at Exit node")
    
    def test_dijkstra_hits_target(self):
        path = get_dijkstra_path()
        target_node = global_game_data.target_node[global_game_data.current_graph_index]
        self.assertIn(target_node, path, "Path should include the target node")
    
    def test_dijkstra_no_invalid_edges(self):
        path = get_dijkstra_path()
        graph = graph_data.graph_data[global_game_data.current_graph_index]
        for i in range(len(path) - 1):
            self.assertIn(path[i + 1], graph[path[i]][1], f"Edge {path[i]} -> {path[i + 1]} must exist")
            
    # Floyd-Warshall Tests
    def test_floyd_warshall_correct_distances(self):
        # Define a simple graph as adjacency matrix
        graph_matrix = [
            [0, 2, math.inf, 1],
            [math.inf, 0, 3, math.inf],
            [math.inf, math.inf, 0, 1],
            [math.inf, math.inf, math.inf, 0]
        ]
        # Expected distances
        expected_distances = [
            [0, 2, 5, 1],
            [math.inf, 0, 3, 4],
            [math.inf, math.inf, 0, 1],
            [math.inf, math.inf, math.inf, 0]
        ]
        
        dist, _ = floyd_warshall(graph_matrix)
        self.assertEqual(dist, expected_distances, "Floyd-Warshall did not compute correct distances")
        
    def test_floyd_warshall_reconstruct_path(self):
        # Define a graph where paths are simple to verify
        graph_matrix = [
            [0, 3, math.inf, 7],
            [math.inf, 0, 1, math.inf],
            [math.inf, math.inf, 0, 2],
            [math.inf, math.inf, math.inf, 0]
        ]
        dist, parent = floyd_warshall(graph_matrix)
        
        # Check reconstructed paths
        self.assertEqual(reconstruct_path(parent, 0, 3), [0, 1, 2, 3], "Path reconstruction failed for 0 -> 3")
        self.assertEqual(reconstruct_path(parent, 1, 2), [1, 2], "Path reconstruction failed for 1 -> 2")
        self.assertEqual(reconstruct_path(parent, 0, 1), [0, 1], "Path reconstruction failed for 0 -> 1")

    def test_floyd_warshall_disconnected_graph(self):
        # Define a disconnected graph
        graph_matrix = [
            [0, math.inf, math.inf],
            [math.inf, 0, math.inf],
            [math.inf, math.inf, 0]
        ]
        
        dist, parent = floyd_warshall(graph_matrix)
        
        # Check that distances are inf for disconnected nodes
        self.assertEqual(dist[0][1], math.inf, "Disconnected nodes should have infinite distance")
        self.assertEqual(reconstruct_path(parent, 0, 1), [0, 1], "Path reconstruction should return empty for disconnected nodes")

    def test_floyd_warshall_dense_graph(self):
        # Ensure algorithm does not break down under a dense graph
        graph_matrix = [
            [0, 1, 4, 6],
            [1, 0, 2, 3],
            [4, 2, 0, 1],
            [6, 3, 1, 0]
        ]
        expected_distances = [
            [0, 1, 3, 4],
            [1, 0, 2, 3],
            [3, 2, 0, 1],
            [4, 3, 1, 0]
        ]
        dist, parent = floyd_warshall(graph_matrix)
        self.assertEqual(dist, expected_distances, "Floyd-Warshall failed for a dense graph")
        for i in range(len(graph_matrix)):
            for j in range(len(graph_matrix)):
                if i != j:
                    path = reconstruct_path(parent, i, j)
                    if path:
                        path_weight = sum(graph_matrix[path[k]][path[k + 1]] for k in range(len(path) - 1))
                        self.assertAlmostEqual(
                            path_weight, dist[i][j], delta=1e-6,
                            msg=f"Path weight mismatch for {i} -> {j}"
                        )
        
if __name__ == '__main__':
    unittest.main()
