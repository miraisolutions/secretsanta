import unittest
from hypothesis import given
from secretsanta.main import funs
from hypothesis.strategies import text, lists, integers, characters


class MakeSantaDict(unittest.TestCase):
    @given(lists(text(alphabet=characters(whitelist_categories=["Lu", "Ll", "Nd", "Pc", "Pd"],
                                          whitelist_characters=["@"]), min_size=3, max_size=20), 2, 10, unique=True),
           integers(min_value=0, max_value=2**32 - 1))
    def test_all_different_assign(self, test_list, seed):
        """
        Test that a generated list of unique names, turned into a dictionary, are all assigned to one another, without
        self-assignment.
        :param test_list: list of names
        :param seed: seed for random choice picking
        """
        test_dict = dict(zip(test_list, test_list))
        assignment = funs.make_santa_dict(test_dict, seed)
        assert len(assignment) == len(test_list)
        for left, right in assignment.items():
            assert (left != right)
