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
    
    
def roll_string(roll):
    """Convert a string into a random number.
    
    Works by trying to evaluate XdX statments first, then uses 
    eval statments to do the actual math, starting with brackets
    until none are left and then the whole given string.
    
    This allows for order of operations to be respected. Decimals
    are respected in the actual math but NOT in XdX statments.
    
    Things that will work:
        1d6         Random number from 1 to 6
        1d6 + 4     Random number from 1 to 6, + 4
        (1d6)*0.5   Random number from 0 to 3
        (d6)+(d6) Sum of two random numbers from 1 to 6
        2d6         Also the sum of two random numbers from 1 to 6
        (1d6)2      A random number from 1 to 6, times 2
        
    Things that will not work as expected:
        d6.5        1d6 resolved to a random number, eval appends the .5
                        to the result, then removes it by casting to an int.
        d6.5.5      Syntax error
        ()          Freeze forever TODO FIX THIS
        (           Syntax error
        sys         TypeError: int() argument must be a string or a number,
                        not 'module
        
    Args:
        roll (str): String representing a roll.
    
    Returns:
        int: Random number based on given string. 
        
    """
    # TODO: unit test
    roll = roll.replace(' ', '')
    roll = roll.replace('x', '*')
    
    # Convers XdX statments to numbers.
    for group in re.findall(r'[0-9]*d[1-9][0-9]*', roll):
        i, j = group.split('d')
        if not i:
            i = 1
        roll = roll.replace(group, str(get_roll(int(i), int(j))), 1)
    
    roll = re.sub('([0-9\)])(\()', r'\1*(', roll)
    roll = re.sub('(\))([\(0-9])', r')*\2', roll)
    
    pattern = r'\([0-9+\*\/]*\)'
    try:
        group = re.findall(pattern, roll)[0]
    except IndexError:
        # No brackets? Let's exit early!
        return int(eval(roll))
    
    while group:
        roll = roll.replace(group, "{}".format(eval(group)), 1)
        try:
            group = re.findall(pattern, roll)[0]
        except IndexError:
            break
    return int(eval(roll))


if __name__ == '__main__':
    import sys
    print "Result: {}".format(roll_string(''.join(sys.argv[1:])))
