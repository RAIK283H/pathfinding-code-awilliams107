import graph_data
import global_game_data
from numpy import random
from collections import deque
import heapq

def set_current_graph_paths():
    global_game_data.graph_paths.clear()
    global_game_data.graph_paths.append(get_test_path())
    global_game_data.graph_paths.append(get_random_path())
    global_game_data.graph_paths.append(get_dfs_path())
    global_game_data.graph_paths.append(get_bfs_path())
    global_game_data.graph_paths.append(get_dijkstra_path())


def get_test_path():
    return graph_data.test_path[global_game_data.current_graph_index]

# Tries 20 or variable amount of times to generate a successful random path
def get_random_path(max_retries = 20):
    # Get data
    graph = graph_data.graph_data[global_game_data.current_graph_index]
    start_node = 0
    exit_node = len(graph) - 1
    target_node = global_game_data.target_node[global_game_data.current_graph_index]
    
    # Precondition: Must have at least 2 nodes
    assert len(graph) > 1, "Graph must have at least 2 nodes"
    
    # Helper function: creates path between two given nodes
    def random_path_two_nodes(current_node, target_node, visited):
        path = []
        while current_node != target_node:
            neighbors = [n for n in graph[current_node][1] if n not in visited]
            if not neighbors:
                return None
            next_node = random.choice(neighbors)
            path.append(int(next_node))
            visited.add(int(next_node))
            current_node = next_node
        return path
    
    # Attempt to create paths multiple times for more successes
    for _ in range(max_retries):
        visited = set()
        visited.add(start_node)
        
        start_to_target_path = random_path_two_nodes(start_node, target_node, visited)
        target_to_exit_path = random_path_two_nodes(target_node, exit_node, visited)

        if start_to_target_path is not None and target_to_exit_path is not None:
            full_path = start_to_target_path + target_to_exit_path

            # Postconditions: start at start node, include target node, exit at exit node
            assert start_node in visited, "Path must start at start node"
            assert target_node in full_path, "Path must include target node"
            assert full_path[-1] == exit_node, "Path must end at exit node"

            return full_path

    # If all retries fail, return empty path and do not close window (fail gracefully)
    print("Random Path Generator failed after multiple attempts")
    return []

# Creates and returns a DFS path from the start to the end while hitting the target along the way
def get_dfs_path():
    graph = graph_data.graph_data[global_game_data.current_graph_index]
    start_node = 0
    exit_node = len(graph) - 1
    target_node = global_game_data.target_node[global_game_data.current_graph_index]
    
    # Helper function gives a DFS search from a starting node to a target node
    def dfs_search(start, target):
        stack = [(start, [start])]
        visited = set()
        
        while stack:
            (current_node, path) = stack.pop()
            if current_node in visited:
                continue
            visited.add(current_node)
            if current_node == target:
                return path
            for neighbor in graph[current_node][1]:
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor]))
        return []
    
    # Gets DFS path from start to target and then target to exit
    start_to_target_path = dfs_search(start_node, target_node)
    target_to_exit_path = dfs_search(target_node, exit_node)
    
    # Combines the two and returns path if it exists or empty array if it does not
    if start_to_target_path and target_to_exit_path:
        full_path = start_to_target_path + target_to_exit_path[1:]
        full_path = full_path[1:]
        
        # Postconditions a, b, c
        assert target_node in full_path, "Path must include the target node"
        assert full_path[-1] == exit_node, "Path must end at the exit node"
        for i in range(len(full_path) - 1):
            assert full_path[i+1] in graph[full_path[i]][1], f"Vertices {full_path[i]} and {full_path[i+1]} must be connected"
        
        return full_path
    else:
        return []

# Creates and returns a BFS path from the start to the end while hitting the target along the way
def get_bfs_path():
    graph = graph_data.graph_data[global_game_data.current_graph_index]
    start_node = 0
    exit_node = len(graph) - 1
    target_node = global_game_data.target_node[global_game_data.current_graph_index]
    
    # Helper function gives a BFS search from a starting node to a target node
    def bfs_search(start, target):
        queue = deque([(start, [start])])
        visited = set()
        
        while queue:
            current_node, path = queue.popleft()
            if current_node in visited:
                continue
            visited.add(current_node)
            if current_node == target:
                return path
            for neighbor in graph[current_node][1]:
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor]))
        return []
    
    # Gets BFS path from start to target and then target to exit
    start_to_target_path = bfs_search(start_node, target_node)
    target_to_exit_path = bfs_search(target_node, exit_node)
    
    # Combines the two and returns path if it exists or empty array if it does not
    if start_to_target_path and target_to_exit_path:
        full_path = start_to_target_path + target_to_exit_path[1:]
        full_path = full_path[1:]
        
        # Postconditions a, b, c
        assert target_node in full_path, "Path must include the target node"
        assert full_path[-1] == exit_node, "Path must end at the exit node"
        for i in range(len(full_path) - 1):
            assert full_path[i+1] in graph[full_path[i]][1], f"Vertices {full_path[i]} and {full_path[i+1]} must be connected"
        
        return full_path
    else:
        return []


def get_dijkstra_path():
    graph = graph_data.graph_data[global_game_data.current_graph_index]
    start_node = 0
    target_node = global_game_data.target_node[global_game_data.current_graph_index]
    exit_node = len(graph) - 1
    
    # Helper function to perform dijkstra from a given start to a given end
    def dijkstra(graph, start, end):
        # Priority Queue
        pq = []
        heapq.heappush(pq, (0, start, [start]))
        visited = set()
        
        while pq:
            dist, current_node, path = heapq.heappop(pq)
            
            # Skip the node if it's already been visited
            if current_node in visited:
                continue
            visited.add(current_node)
            
            # If we reach the last node, return the path
            if current_node == end:
                return path
            
            # Explore neighbors
            for neighbor in graph[current_node][1]:
                if neighbor not in visited:
                    edge_weight = calculate_distance(graph[current_node][0], graph[neighbor][0])
                    heapq.heappush(pq, (dist + edge_weight, neighbor, path + [neighbor]))
        
        # Return empty list if no path is found to not break functionality
        return []
    
    # Get path from start to target
    start_to_target = dijkstra(graph, start_node, target_node)
    if not start_to_target:
        return []
    
    # Get path from target to exit
    target_to_exit = dijkstra(graph, target_node, exit_node)
    if not target_to_exit:
        return []
    
    # Append the two paths and get rid of the overlap
    full_path = start_to_target[:-1] + target_to_exit
    
    # Postconditions
    assert full_path[0] == start_node, "Path must start at the Start node."
    assert full_path[-1] == exit_node, "Path must end at the Exit node."
    for i in range(len(full_path) - 1):
        assert full_path[i + 1] in graph[full_path[i]][1], f"Edge {full_path[i]} -> {full_path[i + 1]} must exist."
    
    full_path = full_path[1:]
    return full_path

# Helper function for Euclidean distance found on Stack Overflow
def calculate_distance(coord1, coord2):
    return ((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2) ** 0.5