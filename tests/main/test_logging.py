import unittest
import os

from pathlib import Path
from hypothesis import given
from secretsanta.main.funs import make_santa_dict
from hypothesis.strategies import text, lists, characters, sampled_from


def create_log_files_dir_if_missing(log_dir='log_files'):
    # check if directory exists, if not then create it
    check_dir = Path(log_dir).exists()
    if not check_dir:
        path = Path('.') / log_dir
        path.mkdir()


class TestLogging(unittest.TestCase):
    # test error
    def test_error_single_participant(self):
        participants_dict = {'Stephanie': 'Stephanie'}
        os.environ["level"] = "ERROR"
        log_level = os.environ.get('log_level', os.getenv("level")).upper()
        with self.assertRaises(ValueError):
            make_santa_dict(participants_dict, seed=None, verbose=True, level=log_level)

    # test warning
    ls = ['Stephanie', 'Simon', 'Gustavo']

    @given(lists(sampled_from(ls), min_size=2, max_size=2, unique=True))
    def test_warning(self, participants):
        # convert list to dict
        participants_dict = {i: i for i in participants}
        create_log_files_dir_if_missing()
        os.environ["level"] = "DEBUG"
        log_level = os.environ.get('log_level', os.getenv("level")).upper()
        with self.assertLogs('secretsanta.main.funs', level='WARNING') as cm:
            make_santa_dict(participants_dict, seed=1, verbose=True, level=log_level)
        self.assertEqual(cm.output[0], 'WARNING:secretsanta.main.funs:Too few people, assignment will be deterministic')

    # test info
    @given(lists(text(alphabet=characters(whitelist_categories=["Lu", "Ll", "Nd", "Pc", "Pd"],
                                          whitelist_characters=["@"]), min_size=2, max_size=20),
                 min_size=2, max_size=10, unique=True))
    def test_info(self, test_list):
        # convert list to dict
        participants_dict = {i: i for i in test_list}
        create_log_files_dir_if_missing()
        os.environ["level"] = "DEBUG"
        log_level = os.environ.get('log_level', os.getenv("level")).upper()
        if log_level == "INFO":
            with self.assertLogs('secretsanta.main.funs', level='INFO') as cm:
                make_santa_dict(participants_dict, seed=1, verbose=True, level=log_level)
            self.assertEqual(cm.output[0], log_level + ':secretsanta.main.funs:' + test_list[0])
