"""Load config yaml files."""

# Import built-in modules
import os

# Import third-party modules
import yaml


_CONFIG_PATH = os.path.join(os.path.split(__file__)[0], "etc")


def load_yaml(filename):
    """Load the yaml file for a class.
    
    Args:
        filename (str): Name of the yaml to load.
    
    Returns:
        dict: Loaded yaml file contents.

    """
    with open(filename, 'r') as class_yaml:
        return yaml.safe_load(class_yaml)

def get_config(*config):
    """Get a config file.
    
    Args:
        config (list of str): Path from the root of the etc folder
            to a relevent yaml file.
     
    Returns:
        dict: Loaded config file.
    
    """
    # Make sure the last argument is actually a yaml file, and append
    # the .yaml file extension if not.
    final_index = len(config) - 1 
    if not config[final_index].endswith(".yaml"):
        config = list(config)
        config[final_index] = "{}.yaml".format(config[final_index])
    return load_yaml(os.path.join(_CONFIG_PATH, *config))