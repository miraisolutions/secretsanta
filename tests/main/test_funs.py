import unittest
from typing import Union, List
from unittest.mock import patch
from hypothesis import given
from secretsanta.main import funs
from hypothesis.strategies import text, lists, integers, characters


class MakeSantaDict(unittest.TestCase):
    # we specify some character classes to avoid unprintable characters that cause issues when used as dictionary keys.
    # the min / max parameters passed to integers match the accepted range for seeds.

    @given(lists(text(alphabet=characters(whitelist_categories=["Lu", "Ll", "Nd", "Pc", "Pd"],
                                          whitelist_characters=["@"]), min_size=2, max_size=20),  min_size=2, max_size=10, unique=True),
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

    # We don't want to actually send e-mail, and we are testing the send_santa_dict functionality (not the SecretSanta
    # class internals)
    @patch('secretsanta.main.core.SecretSanta')
    @patch('smtplib.SMTP')
    def test_send_santa_dict(self, mock_smtp, mock_santa):
        """
        Test that the function calls our email sending logic with the expected parameters, the expected number of times
        """
        test_dict = dict(zip(["a", "b", "c"], ["a@m.com", "b@m.com", "c@m.com"]))

        smtpserverwithport = "lalaland:1337"

        def mocksantabuilder(email: Union[str, List[str]], person: str):
            return mock_santa(email, person)

        funs.internal_send_santa_dict(smtpserverwithport, "mr.jack", "NoOneCanGuess1234", test_dict, mocksantabuilder)
        mock_smtp.assert_called_with(smtpserverwithport)
        mock_santa.assert_called_with("c@m.com", "c")
        assert mock_santa.call_count == 3
