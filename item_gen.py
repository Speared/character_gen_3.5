"""Functions to handle equiptment generation."""

# Import built-in modules
from random import randint

# Import local modules
import config


def get_armor(*desired_category):
    """Get a random piece of armor.
    
    Args:
        desired_category (list of str): Select armor categories
            (light/medium/heavy) you want a suit from.
    
    Returns:
        dict: Stats for a random suit of armor, pulled from
            etc/items/armor.yaml
    
    """
    armors = config.get_config("items", "armor")
    valid_armors = []
    for category in armors:
        if category in desired_category:
            for key, value in armors[category].items():
                armor = value
                armor['name'] = key
                valid_armors.append(armor)

    return valid_armors[randint(0, len(valid_armors) - 1)]


def _search_items(search_dict, find_me):
    """Search for a key occurring anywhere in a dict of dicts
    
    This aims to be a breadth-first search, since it will mostly/only
    be used to grab items by name, which will usually be within the
    first couple tiers of item stats
    
    """
    values_list = []
    for key in search_dict:
        try:
            # Append item name before returning it so we still
            # know what item this is
            key[find_me]['name'] = find_me
            return key[find_me]
        except KeyError:
            values_list.extend(key.values())
        except TypeError:
            # key is not a collection and does not contain more configs.
            continue
        values_list.extend(key)

    if values_list:
        return _search_items(values_list, find_me)
    return None
            

def get_item_by_name(name):
    """Get an item by name.
    
    Which currently could mean a key in a dictionary, or an -items
    field, in anything in items.yaml. This may be poorly planned.
    
    Args:
        name (str): Item name to find.
    
    Returns:
        dict: Stats for an item.
    
    """
    configs = config.get_configs_in_dir("items")
    return _search_items(configs, name)


if __name__ == "__main__":
    print get_item_by_name('heavy_mace')
