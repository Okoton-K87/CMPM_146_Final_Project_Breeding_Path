import json

def load_breeding_data(file_path):
    """
    Load breeding data from a JSON file.

    :param file_path: Path to the JSON file
    :return: Dictionary containing the breeding data
    """
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def load_breeding_graph(file_path):
    """
    Load the breeding graph from a JSON file.

    :param file_path: Path to the JSON file
    :return: Dictionary containing the breeding graph
    """
    with open(file_path, 'r') as f:
        graph = json.load(f)
    return graph

def validate_pals(pals, breeding_data):
    """
    Validate that all given Pals are present in the breeding data.

    :param pals: List of Pals to validate
    :param breeding_data: Dictionary containing the breeding data
    :return: Tuple (is_valid, invalid_pals)
             - is_valid: True if all Pals are valid, False otherwise
             - invalid_pals: List of Pals that are not found in the breeding data
    """
    parents = breeding_data.get('parents', {})
    invalid_pals = [pal for pal in pals if pal not in parents.values()]

    return len(invalid_pals) == 0, invalid_pals
