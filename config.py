"""Load config yaml files.

Globals:
    _CONFIG_PATH (str): Absolute path to the root of the etc folder in this
        project.

"""

# Import built-in modules
import os

# Import third-party modules
import yaml


_CONFIG_PATH = os.path.join(os.path.split(__file__)[0], "etc")


def load_yaml(filename):
    """Load a yaml file.
    
    Args:
        filename (str): Absolute path of a .yaml file to load.
    
    Returns:
        dict: Loaded yaml file contents.

    """
    with open(filename, 'r') as class_yaml:
        return yaml.safe_load(class_yaml)
        

def get_config(*config):
    """Get configuration data.
    
    Args:
        config (list of str): Path from the root of the etc folder
            to a relevent yaml file. So, for example, calling
            get_config("test", "config", "file") would return the
            file ".\etc\test\config\file.yaml".
     
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
