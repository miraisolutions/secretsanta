import unittest
import os
from hypothesis import given
from secretsanta.main.funs import make_santa_dict
from hypothesis.strategies import text, lists, integers, characters, sampled_from

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
        # check if directory exists, if not then create it
        check_dir = os.path.exists('log_files')
        if not check_dir:
            directory = "log_files"
            path = os.path.join('.', directory)
            os.makedirs(path)
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
        #convert list to dict
        participants_dict = {i: i for i in test_list}
        # check if directory exists, if not then create it
        check_dir = os.path.exists('log_files')
        if not check_dir:
            directory = "log_files"
            path = os.path.join('.', directory)
            os.makedirs(path)
        os.environ["level"] = "DEBUG"
        log_level = os.environ.get('log_level', os.getenv("level")).upper()
        if log_level == "INFO":
            with self.assertLogs('secretsanta.main.funs', level='INFO') as cm:
                make_santa_dict(participants_dict, seed=1, verbose=True, level=log_level)
            self.assertEqual(cm.output[0], log_level + ':secretsanta.main.funs:' + test_list[0])