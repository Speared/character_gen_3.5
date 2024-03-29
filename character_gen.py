"""Generate a character sheet for an npc."""

# Import built-in modules
import math
import random

# Import third-part modules
from six import string_types

# Import local modules
from config import get_config
from item_gen import get_item_by_name

        
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
    """Roll 6 sets of stats and assign them to abilities (str/int/wis/ect).
    
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
    for index, priority in enumerate(ability_priorities):
        ability_dict[priority] = scores[index]
        index += 1         
    return ability_dict


def get_ability_modifier(ability_score, printable=False):
    """Covert an ability score to an ability modifier.
    
    Args:
        ability_score: Ability score.
        printable (bool, optional): If true return a string, adding a '+'
            for nicer printing.
    
    Returns:
        int|str: Ability modifier.

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


class Character(object):
    """An npc.
    
    Holds hp, ac, ability modifiers, skills, size, race, ect, everything
    you need for a fully flushed-out character.

    Globals:
        _BASE_AC (int): The armor class all characters have by default.
    
    Attributes:
        ability_scores (dict): Keys are the 6 dnd abilities (con, str, dex
            int, wis, cha), values are the scores for said abilities.
        hp (int): Max hit points.
        items (dict): Keys are various 'slots' characters have, for held
            weapons, jewelery, armor and whatnot. Values are lists of items.

    """
    
    _BASE_AC = 10
    
    def __init__(self, character_class, level, race="Human", gold=2000,
                 items=None):
        """Initialize a character.
        
        Args:
            character_class (str): Character class.
            level (int): Level.
            race (str, optional): Character race, defaults to Human.
            gold (int, optional): Rough total value of the npc's
                equiptment. Defaults to 2000, to cover plate armor
                and a weapon.
            items (dict, optional): Keys are item types
                (weapon/armor/whatever), values are item names or dicts
                describing the item.

        """
        self.character_class = character_class
        self.level = level
        self.race = race
        self.gold = gold
        
        self.class_config = get_config('class', character_class)
        self.ability_scores = gen_ability_scores(
            self.class_config['ability_priorities']
        )
        self.hp = get_max_hp(
            level,
            get_ability_modifier(self.ability_scores['con']),
            self.class_config['hit_dice']
        )
        
        # Many item slots really only make sense having one of them.
        # These are all being made lists though, to cover things like
        # multiple weapons from dual-welding, multiple amulets from
        # having multiple necks, wearing 3 pairs of pants at once, ect.
        # Enforcing logical limits on item usage will need to come from
        # item generation code.
        self.held_items = {
            'weapon': [],
            'quivered': [],
            'rings': [],
            'amulet': [],
            'armor': [],
            'held': []
        }
        
        # TODO: armor generation needs to be part of a more flushed out
        # item generation, using starting gold to make purchases at random.
        if not items:
            return
        for item_type in self.held_items:
            try:
                for item in items[item_type]:
                    if isinstance(item, string_types):
                        item = get_item_by_name(item)
                self.held_items[item_type].append(item)
            except KeyError:
                continue

        #self.held_items['armor'].append(item_gen.get_armor('medium', 'heavy'))
    
    @property
    def ability_modifiers(self):
        """dict: Ability scores converted to modifiers"""
        return_me = {}
        for key in self.ability_scores:
            return_me[key] = get_ability_modifier(self.ability_scores[key])
        return return_me
    
    @property
    def max_dex_bonus(self):
        """int: Max bonus dex can apply to ac. Affected by armor.
        
        If the npc is wearing multiple pieces of armor use the lowest
        available max dex bonus.
        
        """
        max_dex_bonus = 999
        for armor in self.held_items['armor']:
            if armor['max_dex'] == '~':
                continue
            if max_dex_bonus > armor['max_dex']:
                max_dex_bonus = armor['max_dex']
        return max_dex_bonus
    
    @property
    def item_ac(self):
        """int: Total bonus to ac from items.
        
        Unfortunately has to check every item category, in case someone with
        a sword of +1 ac comes along to mess up this character gen.

        """
        total_ac = 0
        for key, value in self.held_items.items():
            for item in value:
                total_ac += item.get('ac', 0)
        return total_ac
    
    @property
    def ac(self):
        """int: Armor class of the character.
        
        This is their armor in normal situations. Ie: not touch, or flat
        footed.
        
        """
        if not min(self.ability_modifiers['dex'], self.max_dex_bonus):
            print "here"

        return (
            self._BASE_AC
            + min(self.ability_modifiers['dex'], self.max_dex_bonus)
            + self.item_ac
        )
    
    @property
    def touch_ac(self):
        """int: Armor class against touch attacks."""
        return (
            self._BASE_AC
            + min(self.ability_modifiers['dex'], self.max_dex_bonus)
        )
        
    @property
    def flatfooted_ac(self):
        """int: Armor class when surprised"""
        return (
            self._BASE_AC
            + self.item_ac
        )
    
    @property
    def bab(self):
        """int: Base attack bonus"""
        return int(
            (
                self.class_config['start_bab'] +
                math.ceil(
                    self.class_config['bab_per_level'] * (self.level - 1)
                )
            )
        )
    
    @property
    def total_skill_points(self):
        """int: Total skill points for this class/level/intelligence"""
        return (
            self.class_config['skill_points'] * 4 +
            (
                self.class_config['skill_points'] +
                self.ability_modifiers["int"]
            ) * self.level - 1
        ) 
    
    def print_character_sheet(self):
        print "Class: {}".format(self.character_class)
        print "HP: {}".format(self.hp)
        print "level: {}".format(self.level)
        print "Base attack bonus: {}".format(self.bab) 
        print "Ability scores:"
        for key, value in self.ability_scores.items():
            print "\t", key, value, '\t', get_ability_modifier(
                value, printable=True) 
        print "ac: {} ({} flatfooted, {} touch)".format(
            self.ac, self.flatfooted_ac, self.touch_ac)
        print "Total skill points: {}".format(self.total_skill_points)
        print "items:"
        for key, value in self.held_items.items():
            print "\t", "{}: ".format(
                key), " ".join(item['name'] for item in value)

    
if __name__ == '__main__':
    gen_me = get_config('templates', 'gen_me')
    for name, character in gen_me.items():
        print name
        my_character = Character(
            character['class'],
            character['level'],
            items=character.get('items')
        )
        my_character.print_character_sheet()
        print ""
