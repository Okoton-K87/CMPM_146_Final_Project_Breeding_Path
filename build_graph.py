import json
from collections import defaultdict

# Step 1: Load the JSON data from a file
def load_data(file_path):
    """
    Loads JSON data from the specified file path.
    
    :param file_path: Path to the JSON file
    :return: Parsed JSON data as a Python dictionary
    """
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

# Step 2: Build the graph representation
def build_graph(data):
    """
    Constructs a graph where each Pal is a node, and each breeding possibility 
    is an edge leading to a resulting Pal.
    
    :param data: Dictionary containing the 'parents' and 'results' from the JSON
    :return: A graph represented as a dictionary of lists
    """
    graph = defaultdict(list)
    
    # Extract 'parents' and 'results' from the loaded data
    parents = data['parents']
    results = data['results']

    print("Parents dictionary contents:")
    for key, value in parents.items():
        print(f"Key: '{key}', Value: '{value}'")
    
    # Iterate over each Pal and its breeding options in 'results'
    for pal, breed_options in results.items():
        for key, result in breed_options.items():
            # Check if the key exists in the parents dictionary
            if key in parents:
                # Get the other parent from the 'parents' dictionary using the key
                other_parent = parents[key]
                # Add an edge from the current pal to the resulting pal
                graph[pal].append((other_parent, result))

                # print(f"Key '{key}'")
                # print(f"pal: '{pal}', other parent: '{other_parent}, result: '{result}'")
            else:
                other_parent = "NOT IN PARENTS"
                # If the key doesn't exist, skip this entry
                # print(f"[DEBUG] Warning: Key '{key}' not found in parents. Skipping...")
                # print(f"pal: '{pal}', other parent: '{other_parent}, result: '{result}'")
    
    return graph

# Step 3: Save the graph to a file (optional)
def save_graph(graph, output_path):
    """
    Saves the constructed graph to a JSON file.
    
    :param graph: The graph dictionary to be saved
    :param output_path: Path where the graph JSON will be saved
    """
    with open(output_path, 'w') as f:
        json.dump(graph, f, indent=4)

# Step 4: Main execution block to load data, build graph, and save it
if __name__ == "__main__":
    # Load the breeding data from the JSON file
    data = load_data('breeding_data.json')
    
    # Build the graph from the breeding data
    graph = build_graph(data)
    
    # Save the graph to a new JSON file for later use
    save_graph(graph, 'breeding_graph.json')
