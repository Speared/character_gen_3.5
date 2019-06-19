"""Get random numbers.

Games of chance are strictly forbidden by deuteronomy 7.

"""

# Import built-in modules
import random
import re


def get_roll(num, dice):
    """Roll XdY dice and return the total.
    
    Args:
        dice (int): What die to roll.
        num (int): Number of dice to roll.
        
    Returns:
        int: Total.

    """
    return sum([random.randint(1, dice) for x in range(num)])


def _solve_brackets(roll):
    """todo"""
    # TODO: continue here
    while re.search(r'\([0-9+\*\/()])', roll)
        for group in re.findall(r'\([0-9+\*\/]\)'):
            roll.replace(group, "{}".replace(eval(group)), 1)
    
    
def roll_string(roll):
    """Convert a string into a random number.
    
    Args:
        roll (str): String representing a roll.
    
    Returns:
        int: Random number based on given string.
    
    Examples:
        roll='1d6': Return a random number from 1 to 6.
        roll='d6': Return a random number from 1 to 6.
        roll='1': Return 1.
        roll='2d6': Return the sum of two random numbers from  1 to 6.
            number from 1 to 6.
        roll='1d6+1' Return a random number from 1 to 6, plus 1.
        roll='3+2d6/1d38(1d6+6d6): Return 3 plus the sum of two random
            numbers from 1 to 6 divided by a random number between 1 and 38
            times the sum of one random number from 1 to 6 and the sum of
            six random numbers from 1 to 6. This will pretty much never be
            needed.
        roll-'   1     d 6  ': Return a random number from 1 to 6.

    """
    # TODO: unit test
    roll = roll.replace(' ', '')
    roll = roll.replace('x', '*')
    
    # Convers XdX statments to numbers.
    for group in re.findall(r'[0-9]*d[1-9][0-9]*', roll):
        print "group: ", group
        i, j = group.split('d')
        print i, j
        if not i:
            i = 1
        roll = roll.replace(group, str(get_roll(int(i), int(j))), 1)
        print roll
    
    print "returning:", roll
    return eval(roll)
    
if __name__ == '__main__':
    print roll_string('1d6+2(d4(3)) + 1')
