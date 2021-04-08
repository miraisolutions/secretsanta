import datetime
import logging
import smtplib
from secretsanta.main.core import SecretSanta
from secretsanta.main.utils import setup_logging
from typing import Optional, Dict, Tuple, List, Union

import numpy as np

# PyCharm: ctrl-p inside parentheses shows function args!


# mypy is missing a library stub file for module 'numpy' and will complain about it
# workaround: append --ignore-missing-imports to the mypy call (see https://github.com/python/mypy/issues/3905)
def make_santa_dict(
    dictionary: Dict[str, str],
    seed: Optional[int] = None,
    verbose: bool = False,
    level: str = "ERROR",
) -> Dict[str, str]:
    # type triple-quotes and press enter to generate empty docstring stub
    """Creates a random secret santa assignment as a dictionary from an initial dictionary of the participants' names
    and associated email addresses.

    Args:
        dictionary: mapping names to email addresses
        seed: seed for numpy random number generator
        verbose: boolean to control print output
    Returns:
        Shuffled (randomized) dictionary, guaranteed not to map any name to its original email in `dictionary`
    """
    ######
    # Implementation note: the main challenge we have beyond simply shuffling a list is to ensure no one gets assigned
    # as their own secret santa. This means we need to exclude the participant from the secret santa choices as we go
    # through the list of participants.
    # in order to obtain this property, we rotate sub-sections of the list of participants, instead of shuffling it.
    ######

    setup_logging(level)
    logger = logging.getLogger(__name__)
    # print(__name__): secretsanta.main.funs

    # We need to map each person to some e-mail address, so we start by getting a list of all names
    # unpack dict_keys object into list literal (no control over order!)
    # https://stackoverflow.com/questions/16819222/how-to-return-dictionary-keys-as-a-list-in-python
    names: List[str] = [*dictionary.keys()]

    np.random.seed(seed)

    if len(dictionary) == 1:
        # Despite this often being perceived as an anti-pattern, we want the exception to be shown in log files also.
        logger.error("Only one person listed")
        raise ValueError("Only one person listed")
    if len(dictionary) <= 3:
        logger.warning("Too few people, assignment will be deterministic")

    shuffled_names = shuffle_move_all(names)

    return dict(zip(shuffled_names, dictionary.values()))


def shuffle_move_all(lst):
    """
    randomly shuffle a list such that none of the elements remains in its previous index.
    :param lst: the list to shuffle
    :return: the shuffled list
    """
    # We start by creating pivots delimiting segments of length at least 2
    pvts = pivots(lst)
    for i in range(0, len(pvts) - 1):
        start = pvts[i]
        stop = pvts[i + 1]
        sublen = stop - start - 1
        # each segment of the list gets rotated by at least one, up to (not including) its length; this guarantees that
        # no element will remain in its original position.
        rotate_steps = 1 if sublen <= 1 else np.random.randint(1, sublen)
        lst[start:stop] = rotate(rotate_steps, lst[start:stop])
    return lst


def pivots(lst):
    """
    Randomly generate an ordered list of unique valid indices, \
    defining segments of length two or greater over the input list.
    :param lst: the list to split
    :return: random, ordered indices of the list, including 0 and the length.
    """
    pivot = 0
    end = len(lst)
    result = []
    # the last pivot must allow for a segment of length >=2 up to the end
    while pivot <= end - 2:
        result = result + [pivot]
        # computing the next pivot fails if the pivot is = end-2, as the min and max args of randint are the same;
        # so we check and stop if the next pivot would be thrown away by the next iteration (pivot + 2 > end-2)
        if pivot <= end - 4:
            pivot = np.random.randint(pivot + 2, end)
        else:
            break
    return result + [end]


def rotate(n, lst):
    """
    rotate the list by a given number of steps.
    :param n: steps to rotate the list by
    :param lst: list to rotate
    :return: the rotated list
    """
    return lst[n:] + lst[:n]


def send_santa_dict(smtpserverwithport: str, sender: str, pwd: str,
                    senddict: Dict[str, str], test: bool = False) -> Dict[str, Tuple[int, bytes]]:
    def santa_builder(email: Union[str, List[str]], person: str):
        return SecretSanta(email, person)
    return internal_send_santa_dict(smtpserverwithport, sender, pwd, senddict, santa_builder, test)


def internal_send_santa_dict(smtpserverwithport: str, sender: str, pwd: str, senddict: Dict[str, str], santabuilder,
                             test: bool = False) -> Dict[str, Tuple[int, bytes]]:
    # "\" is used in the docstring to escape the line ending in sphinx output
    """Loops over a 'santa' dictionary and sends respective emails

    Args:
        smtpserverwithport: SMTP server including port (colon-separated)
        sender: email address from which to send emails
        pwd: password for sender's email account
        senddict: mapping of names to email addresses
        test: boolean to allow test-run
    Returns:
        All failed email sending attempts as returned by :func:`smtplib.sendmail()`, empty if all were successful
    """
    # create SMTP server object and connect
    server = smtplib.SMTP(smtpserverwithport)

    # start TLS, following SMTP commands will be encrypted
    server.starttls()

    server.login(sender, pwd)

    subj = 'Secret Santa %d' % datetime.datetime.now().year

    def parameterized_send(santa: SecretSanta) -> Dict[str, Tuple[int, bytes]]:
        return santa.send(subj, sender, 'Lucky you! You got the lovely', server, test)

    # Dictionary comprehension: https://www.python.org/dev/peps/pep-0274/#semantics
    checks = {email: error
              # For each entry (name and email address to send to) ...
              for (name, mail) in senddict.items()
              # ... we initialize a SecretSanta instance, and call send.
              # We capture the results as individual variables from each call's result Dict,
              # so we can construct a single Dict containing all failed attempts.
              for (email, error) in parameterized_send(santabuilder(mail, name)).items()
              }

    server.quit()
    return checks
