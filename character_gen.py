"""Generate a character sheet for an npc."""

# Import built-in modules
import random

# Import local modules
from config import get_config

        
def get_roll(num, dice):
    """Roll XdY dice and return the total.
    
    Args:
        dice (int): What die to roll.
        num (int): Number of dice to roll.
        
    Returns:
        int: Total.

    """
    return sum([random.randint(1, dice) for x in range(num)])
        

def get_scores(num):
    """Get values for ability scores.
    
    This works by rolling 4d6 and removing the lowest value.

    Args:
        num: Number of scores to generate.
    
    Yields:
        int: A stat value from 3 to 18.

    """
    scores = []
    for i in range(num):
        values = []
        for j in range(4):
            values.append(random.randint(1, 6))
        scores.append(sum(values) - min(values))
    return scores

    
def gen_ability_scores(ability_priorities):
    """Roll 6 sets of stats and assign them to adilites (str/int/wis/ect).
    
    Works based on the order of the ability_priorities list in character
    config files.
    
    Args: 
        ability_priorities (list of str): Stats to generate.

    Returns:
        dict: Keys are stats, values are scores.
        
    """
    scores = get_scores(len(ability_priorities))
    scores.sort(reverse=True)
    ability_dict = {}
    index = 0
    for priority in ability_priorities:
        ability_dict[priority] = scores[index]
        index += 1         
    return ability_dict


def get_ability_modifier(ability_score, printable=False):
    """Covert an ability score to an ability modifier.
    
    Args:
        ability_score: Ability score.
        printable (bool, optional): If true return a string explisitly
            adding a '+' for nicer printing. 
    
    Returns:
        int: Ability modifier.

    """
    modifier = (ability_score - 10) // 2
    if printable and modifier > 0:
        return "+{}".format(modifier)
    return modifier


def get_max_hp(level, con_modifier, hit_dice):
    """Get max character hp.
    
    Args:
        level (int): Character level.
        con_modifier (int): Constitution ability modifier.
        hit_dice (int): Class hit dice.
    
    Returns:
        int: Max character hp.

    """
    return get_roll(level, hit_dice) + level * con_modifier
    
def gen_character(character_class, level):
    """Get a character sheet for an npc.
    
    Args:
        character_class (str): Class to build a character for.
            Requiers a <character_class>.yaml file to exist
            to pull stats for.
        level (int): Character level.

    """
    # TODO: this will need to be in a class someday.
    #character_config = load_yaml('{}.yaml'.format(character_class))
    character_config = get_config('class', 'fighter')
    
    abilities = gen_ability_scores(character_config['ability_priorities'])
    
    hp = get_max_hp(
        level,
        get_ability_modifier(abilities['con']),
        character_config['hit_dice']
    )
    
    # Debug prints.
    # TODO: Remove this. put it in a class and add logging if it's needed.
    print "HP: {}".format(hp)
    for key, value in abilities.items():
        print key, value, '\t', get_ability_modifier(value, printable=True)
    
if __name__ == '__main__':
    gen_character("fighter", 5)
    