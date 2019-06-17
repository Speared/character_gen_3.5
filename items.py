"""Functions to handle equiptment generation."""

# Import built-in modules
from random import randint

# Import local modules
from config import get_config


def get_armor(*desired_categorys):
    """Get a random peice of armor.
    
    Args:
        catergory (list of str): Select armor catagories (light/medium/heavy)
            you want a suit from/
    
    Returns:
        dict: Stats for a random suit of armor, pulled from
            etc/items/armor.yaml
    
    """
    armors = get_config("items", "armor")
    valid_armors = []
    for catergory, armor_set in armors.items():
        if catergory in desired_categorys:
            valid_armors.extend(armor_set)
    return(valid_armors[randint(0, len(valid_armors) - 1)])
        

if __name__ == "__main__":
    print get_armor("heavy")
        