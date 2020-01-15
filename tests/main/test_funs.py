import unittest
from typing import Union, List
from unittest.mock import patch
from hypothesis import given
from secretsanta.main import funs
from hypothesis.strategies import text, lists, integers, characters


class MakeSantaDict(unittest.TestCase):
    @given(lists(text(alphabet=characters(whitelist_categories=["Lu", "Ll", "Nd", "Pc", "Pd"],
                                          whitelist_characters=["@"]), min_size=2, max_size=20), 2, 10, unique=True),
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

    @patch('secretsanta.main.core.SecretSanta')
    @patch('smtplib.SMTP')
    def test_send_santa_dict(self, MockSMTP, MockSanta):
        """
        Test that the function calls our sending logic with the expected parameters, the expected number of times
        :return:
        """
        test_dict = dict(zip(["a", "b", "c"], ["a@m.com", "b@m.com", "c@m.com"]))

        smtpserverwithport = "lalaland:1337"

        def mocksantabuilder(email: Union[str, List[str]], person: str):
            return MockSanta(email, person)

        funs.internal_send_santa_dict(smtpserverwithport, "mr.jack", "NoOneCanGuess1234", test_dict, mocksantabuilder)
        MockSMTP.assert_called_with(smtpserverwithport)
        MockSanta.assert_called_with("c@m.com", "c")
        assert MockSanta.call_count == 3
