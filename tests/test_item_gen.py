# Import built-in modules
import unittest

# Import local modules
from item_gen import _search_items


class TestDiceRoll(unittest.TestCase):

    def test_search_items_in_list(self):
        test_dict = [
            {
                "find_me": {"yay!": "found me!"}
            }
        ]
        assert(_search_items(test_dict, "find_me"))

    def test_search_items_in_dict(self):
        test_dict = {
            "find_me": {
                "yay!": "found me!"
            }
        }
        assert(_search_items(test_dict, "find_me"))

    def test_search_item_by_name_field(self):
        test_dict = [
            {
                "name": "find_me"
            },
        ]
        assert(_search_items(test_dict, "find_me"))

    def test_search_word(self):
        test_dict = ["find_me"]
        assert(_search_items(test_dict, "find_me"))

    def test_nonexistent_value(self):
        test_dict = {
            'nope': {},
            'not in here': {}
        }
        assert(not _search_items(test_dict, "find_me"))


if __name__ == '__main__':
    unittest.main()