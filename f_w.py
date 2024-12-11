# Class for implementation of Floyd_Warshall algorithm, no Extra Credit (just unit testing, no visualization)

import math

def floyd_warshall(graph_matrix):
    n = len(graph_matrix)
    dist = [[math.inf] * n for _ in range(n)]
    parent = [[None] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            if i == j:
                dist[i][j] = 0
            elif graph_matrix[i][j] != 0:  # Assuming 0 means no edge
                dist[i][j] = graph_matrix[i][j]
                parent[i][j] = i
                
    # Floyd-Warshall algorithm
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    parent[i][j] = parent[k][j]

    return dist, parent

def reconstruct_path(parent_matrix, start, end):
    if parent_matrix[start][end] is None:
        return []  # No path
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = parent_matrix[start][current]
        if current == start:
            path.append(start)
            break
    return path[::-1]

def convert_to_matrix(adjacency_list):
    n = len(adjacency_list)
    matrix = [[0 if i != j else 0 for j in range(n)] for i in range(n)]
    for i, edges in enumerate(adjacency_list):
        for neighbor, weight in edges:
            matrix[i][neighbor] = weight
    return matrix

def main():
    adjacency_list = [
        [(1, 4), (2, 1)],
        [(2, 2), (3, 5)],
        [(3, 1)],
        []
    ]
    
    graph_matrix = convert_to_matrix(adjacency_list)
    dist, parent = floyd_warshall(graph_matrix)
    
    start_node = 0
    end_node = 3
    
    shortest_path = reconstruct_path(parent, start_node, end_node)
    if shortest_path:
        print(f"Shortest path from node {start_node} to node {end_node}: {' -> '.join(map(str, shortest_path))}")
        print(f"Distance: {dist[start_node][end_node]}")
    else:
        print(f"No path exists from node {start_node} to node {end_node}")
        
if __name__ == "__main__":
    main()