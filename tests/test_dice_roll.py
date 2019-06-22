# Import built-in modules
import unittest

# Import local modules
from dice_roll import roll_string


class TestDiceRoll(unittest.TestCase):

    def test_multiplication_1(self):
        self.assertTrue(roll_string('2x3') == 6)

    def test_multiplication_2(self):
        self.assertTrue(roll_string('2*2') == 4)

    def test_multiplication_3(self):
        self.assertTrue(roll_string('5(0.5)') == 2)

    def test_brackets_1(self):
        self.assertTrue(
            roll_string('2(((3)))+(2(1+1))') == 10
        )

if __name__ == '__main__':
    unittest.main()