import json
import os
from PIL import Image, ImageDraw
from validation import load_breeding_data, load_breeding_graph
from bfs_search import bfs

def get_image_file_name(pal, breeding_data):
    """
    Get the correct image file name for a given Pal.

    :param pal: Name of the Pal
    :param breeding_data: Dictionary containing the breeding data
    :return: Image file name corresponding to the Pal
    """
    parents = breeding_data['parents']
    for key, value in parents.items():
        if value == pal:
            if "_1" in key:  # Handle variant cases
                return f"{int(key.split('_')[0]):03d}B.png"
            else:
                return f"{int(key):03d}.png"
    return None

def build_binary_tree(path):
    """
    Convert the BFS path to a binary tree data structure, with cycle detection.

    :param path: List of tuples representing the breeding path
    :return: Root of the binary tree
    """
    if not path:
        return None

    # Create nodes from the path
    nodes = {}
    for pal1, pal2, result in path:
        nodes[result] = (pal1, pal2)

    def build_tree(current_pal, visited=set()):
        if current_pal not in nodes:
            return current_pal, None, None
        if current_pal in visited:
            return current_pal, None, None  # Stop recursion if a cycle is detected

        visited.add(current_pal)
        left, right = nodes[current_pal]
        return current_pal, build_tree(left, visited), build_tree(right, visited)

    # The target pal is the last result in the path
    target_pal = path[-1][-1]
    return build_tree(target_pal)

def calculate_dynamic_scale(tree_root, breeding_data, path_length, max_width, max_height):
    """
    Calculate the appropriate scaling factor based on the tree depth, path length, and the available space.

    :param tree_root: Root of the binary tree
    :param breeding_data: Dictionary containing the breeding data
    :param path_length: Length of the path
    :param max_width: Maximum width of the canvas
    :param max_height: Maximum height of the canvas
    :return: Calculated scale factor
    """
    def get_tree_depth(node):
        if not node:
            return 0
        _, left, right = node
        return 1 + max(get_tree_depth(left), get_tree_depth(right))

    depth = get_tree_depth(tree_root)
    max_images_per_row = 2 ** (depth - 1)

    # Load an example image to calculate scaling
    example_image = Image.open(os.path.join("images", "001.png"))
    img_width, img_height = example_image.size

    # Start with the image at 1/2 size
    initial_scale = 0.5
    # Adjust scaling based on path length
    scale = initial_scale * (65/100) ** (path_length - 1)  # Change: Start at half size and reduce by 3/4 for each additional path length
    
    return scale

def visualize_binary_tree(tree_root, breeding_data, path_length, output_path="breeding_tree.png"):
    """
    Visualize the binary tree and save it as an image.

    :param tree_root: Root of the binary tree
    :param breeding_data: Dictionary containing the breeding data
    :param path_length: Length of the breeding path
    :param output_path: Path to save the visualization image
    """
    max_width, max_height = 1200, 800
    scale = calculate_dynamic_scale(tree_root, breeding_data, path_length, max_width, max_height)

    def draw_tree(node, x, y, dx, draw, img_map, scale):
        if not node:
            return
        pal, left, right = node

        # Load and scale the image for the current Pal
        image_file = get_image_file_name(pal, breeding_data)
        if image_file:
            pal_img = Image.open(os.path.join("images", image_file))
            pal_img = pal_img.resize((int(pal_img.width * scale), int(pal_img.height * scale)))
            img_map.paste(pal_img, (x - pal_img.width // 2, y))

            img_width, img_height = pal_img.size

            if left:
                draw.line((x, y + img_height, x - dx, y + img_height + 100), fill="black")
                draw_tree(left, x - dx, y + img_height + 100, dx // 2, draw, img_map, scale)

            if right:
                draw.line((x, y + img_height, x + dx, y + img_height + 100), fill="black")
                draw_tree(right, x + dx, y + img_height + 100, dx // 2, draw, img_map, scale)

    # Create a blank canvas for the tree visualization
    tree_image = Image.new("RGBA", (max_width, max_height), (255, 255, 255, 255))
    draw = ImageDraw.Draw(tree_image)
    draw_tree(tree_root, max_width // 2, 20, max_width // 4, draw, tree_image, scale)

    # Save the visualization as an image file
    tree_image.save(output_path)

def print_tree_structure(node, level=0):
    """
    Recursively prints the tree structure for debugging.
    
    :param node: Current node of the tree
    :param level: Current level in the tree (used for indentation)
    """
    if not node:
        return
    pal, left, right = node
    print(' ' * (level * 4) + f"{pal}")
    print_tree_structure(left, level + 1)
    print_tree_structure(right, level + 1)

# Example usage:
# if __name__ == "__main__":
#     breeding_data = load_breeding_data('breeding_data.json')
#     graph = load_breeding_graph('breeding_graph.json')

#     # Example lists of pets the player currently has
#     initial_pals = ["Lamball", "Lifmunk", "Chikipi", "Kitsun"]

#     # Example target Pal
#     target = "Lifmunk"

#     # Perform BFS to find the breeding path
#     path = bfs(graph, initial_pals, target)

#     if path:
#         tree_root = build_binary_tree(path)
        
#         # Print the tree structure for debugging
#         print("Tree Structure:")
#         print_tree_structure(tree_root)

#         # Generate and save the tree visualization
#         visualize_binary_tree(tree_root, breeding_data, len(path))
#     else:
#         print(f"No path found to breed {target} with the current Pals")
