import tkinter as tk
from tkinter import messagebox
from bfs_search import bfs, possible
from validation import load_breeding_data, validate_pals, load_breeding_graph
from visualize import build_binary_tree, visualize_binary_tree
import os

# Load the breeding data and graph for validation and pathfinding
breeding_data = load_breeding_data('breeding_data.json')
graph = load_breeding_graph('breeding_graph.json')

# Function to start breeding based on user input from the GUI
def start_breeding():
    initial_pals = initial_pals_var.get().split(", ")
    target_pal = target_pal_var.get()
    
    # Validate the entered Pals
    is_valid, invalid_pals = validate_pals(initial_pals + [target_pal], breeding_data)
    
    if not is_valid:
        result = f"Invalid Pals found: {', '.join(invalid_pals)}"
        result_label.config(text=result)
        visualize_button.config(state=tk.DISABLED)  # Disable the visualize button
        return
    
    path = bfs(graph, initial_pals, target_pal)
    if path:
        result = "BFS Path: " + " -> ".join([f"{p[0]} + {p[1]} = {p[2]}" for p in path])
        visualize_button.config(state=tk.NORMAL)  # Enable the visualize button
        visualize_button.path = path  # Store the path in the button for later use
    else:
        result = f"No path found to breed {target_pal} with the current Pals"
        visualize_button.config(state=tk.DISABLED)  # Disable the visualize button
    
    result_label.config(text=result)

# Function to visualize the breeding tree and open the PNG file
def visualize_breeding_tree():
    path = visualize_button.path
    tree_root = build_binary_tree(path)
    visualize_binary_tree(tree_root, breeding_data, path_length=len(path), output_path="breeding_tree.png")
    
    # Open the generated PNG file
    if os.path.exists("breeding_tree.png"):
        os.system("open breeding_tree.png")  # This works on macOS. Use "xdg-open" on Linux or "start" on Windows.
    else:
        messagebox.showerror("Error", "Failed to generate the breeding tree image.")

# Function to find all possible children from the initial Pals
def find_possible_children():
    initial_pals = initial_pals_var.get().split(", ")
    
    # Validate the entered Pals
    is_valid, invalid_pals = validate_pals(initial_pals, breeding_data)
    
    if not is_valid:
        result = f"Invalid Pals found: {', '.join(invalid_pals)}"
        result_label.config(text=result)
        return
    
    children = possible(initial_pals, graph)
    result = f"Possible Children: {', '.join(children)}"
    result_label.config(text=result)

# Set up the main GUI window
root = tk.Tk()
root.title("Pal Breeding Path Finder")

# Initial Pals input
tk.Label(root, text="Enter Your Current Pals (comma-separated):").pack()
initial_pals_var = tk.StringVar(value="Lamball, Lifmunk, Chikipi, Kitsun")
initial_pals_entry = tk.Entry(root, textvariable=initial_pals_var, width=50)
initial_pals_entry.pack()

# Target Pal input
tk.Label(root, text="Enter Your Target Pal:").pack()
target_pal_var = tk.StringVar(value="Leezpunk")
target_pal_entry = tk.Entry(root, textvariable=target_pal_var, width=50)
target_pal_entry.pack()

# Button to find possible children
tk.Button(root, text="Find Possible Children", command=find_possible_children).pack()

# Button to start the breeding path search
tk.Button(root, text="Find Breeding Path", command=start_breeding).pack()

# Label to display the result
result_label = tk.Label(root, text="", wraplength=500)
result_label.pack()

# Button to visualize the breeding tree (initially disabled)
visualize_button = tk.Button(root, text="Visualize Breeding Tree", command=visualize_breeding_tree, state=tk.DISABLED)
visualize_button.pack()

# Start the GUI loop
root.mainloop()
