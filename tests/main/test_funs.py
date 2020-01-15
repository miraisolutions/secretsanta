import unittest
from hypothesis import given
from secretsanta.main import funs
from hypothesis.strategies import text, sets, integers, characters


class MakeSantaDict(unittest.TestCase):
    @given(sets(text(alphabet=characters(whitelist_categories=["Lu", "Ll"]), min_size=3, max_size=20), 2, 10),
           integers(min_value=0, max_value=2**32 - 1))
    def test_no_self_assign(self, test_set, seed):
        test_list=list(test_set)
        test_dict = dict(zip(test_list, test_list))
        assignment = funs.make_santa_dict(test_dict, seed)
        for left, right in assignment.items():
            assert (left != right)
