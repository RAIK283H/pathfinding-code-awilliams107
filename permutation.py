import perm_test_graph_data

def sjt_perms(n):
    p = list(range(1, n + 1))
    directions = [-1] * n
    yield p[:]
    
    # Find the largest mobile integer
    while True:
        largest_mobile = -1
        for i in range(n):
            if directions[i] == -1 and i > 0 and p[i] > p[i - 1] or directions[i] == 1 and i < n - 1 and p[i] > p[i + 1]:
                if largest_mobile == -1 or p[i] > p[largest_mobile]:
                    largest_mobile = i
        if largest_mobile == -1:
            return
        
        # Swap the mobile integer in its direction
        swap_index = largest_mobile + directions[largest_mobile]
        p[largest_mobile], p[swap_index] = p[swap_index], p[largest_mobile]
        directions[largest_mobile], directions[swap_index] = directions[swap_index], directions[largest_mobile]
        largest_mobile = swap_index
        
        # Reverse direction of all integers larger than the largest mobile integer
        for i in range(n):
            if p[i] > p[largest_mobile]:
                directions[i] = -directions[i]

        yield p[:]

# Determine if a graph has a Valid Hamiltonian Cycle
def has_ham_cycle(graph):
    # Account for 0 and n with a -2
    n = len(graph) - 2
    ham_cycles = []
    
    for perm in sjt_perms(n):
        cycle = [0] + perm + [len(graph) - 1]
        
        # Test to see if cycle is valid
        valid_cycle = all(cycle[i + 1] in graph[cycle[i]][1] for i in range(len(cycle) - 1))
        
        if valid_cycle:
            ham_cycles.append(cycle)
    
    # Print and return all valid Hamiltonian cycles or return -1 if no valid cycles exist
    if ham_cycles:
        for cycle in ham_cycles:
            print("Hamiltonian cycle found:", cycle)
        return ham_cycles
    else:
        print("No Hamiltonian cycle found.")
        return -1

'''
# Tests used for verification before unit tests
print()
(has_ham_cycle(perm_test_graph_data.perm_test_graph_data[0]))
print()
(has_ham_cycle(perm_test_graph_data.perm_test_graph_data[1]))
print()
'''