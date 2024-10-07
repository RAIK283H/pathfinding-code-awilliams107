import graph_data
import global_game_data
from numpy import random
from collections import deque

def set_current_graph_paths():
    global_game_data.graph_paths.clear()
    global_game_data.graph_paths.append(get_test_path())
    global_game_data.graph_paths.append(get_random_path())
    global_game_data.graph_paths.append(get_dfs_path())
    global_game_data.graph_paths.append(get_bfs_path())
    global_game_data.graph_paths.append(get_dijkstra_path())


def get_test_path():
    return graph_data.test_path[global_game_data.current_graph_index]

# Tries 5 or variable amount of times to generate a successful random path
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


# DFS and BFS algorithms found online, implemented to figure out how this stuff works so I can do get_random_path()
def get_dfs_path():
    graph = graph_data.graph_data[global_game_data.current_graph_index]
    start = 0
    exit_node = len(graph) - 1
    visited = set()
    
    def dfs(node, path):
        visited.add(node)
        path.append(node)

        if node == exit_node:
            return path

        for neighbor in graph[node][1]:
            if neighbor not in visited:
                result = dfs(neighbor, path)
                if result: 
                    return result
        path.pop()
        return None
    path = []
    dfs_path = dfs(start, path)
    return dfs_path if dfs_path else []


def get_bfs_path():
    graph = graph_data.graph_data[global_game_data.current_graph_index]
    
    start_node = 0
    exit_node = len(graph) - 1
    
    queue = deque([[start_node]])
    visited = set()

    
    while queue:
        path = queue.popleft()
        current_node = path[-1]

        if current_node == exit_node:
            return path

        if current_node not in visited:
            visited.add(current_node)
            
            for neighbor in graph[current_node][1]:
                if neighbor not in visited:
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)
    return []


def get_dijkstra_path():
    return [1,2]
