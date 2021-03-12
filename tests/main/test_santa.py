import unittest
import os
from hypothesis import given
from secretsanta.main.funs import make_santa_dict
from hypothesis.strategies import lists, integers, sampled_from

class TestLogging(unittest.TestCase):
    # test error
    def test_error(self):
        participants_dict = {'Stephanie': 'Stephanie'}
        os.environ["level"] = "ERROR"
        log_level = os.environ.get('log_level', os.getenv("level")).upper()
        with self.assertRaises(ValueError):
            make_santa_dict(participants_dict, seed=None, verbose=True, level=log_level)

    # test warning
    ls = ['Stephanie', 'Simon', 'Gustavo']
    @given(lists(sampled_from(ls), min_size=2, max_size=2, unique=True),
           integers(min_value=1, max_value=1))
    def test_warning(self, participants, seed):
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
            make_santa_dict(participants_dict, seed=seed, verbose=True, level=log_level)
        self.assertEqual(cm.output[0], 'WARNING:secretsanta.main.funs:WARNING: Too few people, assignment will be deterministic')

    # test info
    ls = ['Stephanie', 'Simon', 'Gustavo', 'Nicola', 'Guido', 'Francesca',
          'Gabriel', 'Roland', 'Nikki', 'Peter', 'Martin', 'Riccardo']
    @given(lists(sampled_from(ls), min_size=4, max_size=4, unique=True),
           integers(min_value=1, max_value=1))
    def test_info(self, participants, seed):
        #convert list to dict
        participants_dict = {i: i for i in participants}
        # check if directory exists, if not then create it
        check_dir = os.path.exists('log_files')
        if not check_dir:
            directory = "log_files"
            path = os.path.join('.', directory)
            os.makedirs(path)
        os.environ["level"] = "DEBUG"
        log_level = os.environ.get('log_level', os.getenv("level")).upper()
        with self.assertLogs('secretsanta.main.funs', level='INFO') as cm:
            make_santa_dict(participants_dict, seed = seed, verbose = True, level = log_level)
        self.assertEqual(cm.output[0], 'INFO:secretsanta.main.funs:INFO:' + participants[0])