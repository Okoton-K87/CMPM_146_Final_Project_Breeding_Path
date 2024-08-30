import json
import time
from collections import deque

def bfs(graph, initial_pals, target_pal, time_limit=3):
    """
    Performs BFS to find the shortest path to breed the target_pal, allowing for multiple instances of the same Pal.
    Terminates if the search exceeds the specified time limit.
    
    :param graph: The graph representing breeding paths
    :param initial_pals: The list of Pals the player currently has
    :param target_pal: The target Pal we want to reach
    :param time_limit: The time limit in seconds for the BFS search
    :return: A list of tuples representing the breeding path, or None if no path is found or if the search exceeds the time limit
    """
    start_time = time.time()  # Record the start time
    queue = deque([(initial_pals, [])])  # Queue stores (current_pals, path)
    visited = set()  # Track all visited states
    
    while queue:
        # Check if the time limit has been exceeded
        if time.time() - start_time > time_limit:
            return None
        
        current_pals, path = queue.popleft()
        current_state = tuple(sorted(current_pals))
        
        # Check if we've already visited this exact state
        if current_state in visited:
            continue
        
        visited.add(current_state)  # Mark this state as visited

        # Explore all possible breeding combinations within the current Pals
        for i, pal in enumerate(current_pals):
            for j, other_pal in enumerate(current_pals):
                if i != j:  # Ensure we're not breeding a Pal with itself
                    for other_parent, result in graph.get(pal, []):
                        if other_parent == other_pal:
                            new_path = path + [(pal, other_parent, result)]
                            new_pals = current_pals + [result]

                            if result == target_pal:
                                return new_path

                            queue.append((new_pals, new_path))
    
    return None  # No path found

def possible(initial_pals, graph):
    """
    Performs search to find all possible breedable children from the initial_pals.
    Returns a list of all possible children.
    """
    queue = deque([initial_pals])
    visited = set(tuple(initial_pals))
    possible_children = set()
    
    while queue:
        current_pals = queue.popleft()
        
        for i in range(len(current_pals)):
            for j in range(i + 1, len(current_pals)):
                pal1 = current_pals[i]
                pal2 = current_pals[j]
                
                if pal1 in graph:
                    for offspring in graph[pal1]:
                        if offspring == pal2 or offspring not in graph[pal1]:
                            continue
                        if pal2 == offspring[0]:
                            new_offspring = offspring[1]
                            
                            if new_offspring not in possible_children:
                                possible_children.add(new_offspring)
                                new_combination = current_pals + [new_offspring]
                                new_combination_tuple = tuple(sorted(new_combination))
                                
                                if new_combination_tuple not in visited:
                                    visited.add(new_combination_tuple)
                                    queue.append(new_combination)
    
    return list(possible_children)
