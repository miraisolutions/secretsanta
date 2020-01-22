import datetime
import smtplib
from contextlib import suppress
from typing import Optional, Dict, Tuple, List, Union, Any

import numpy as np

from secretsanta.main.core import SecretSanta


# PyCharm: ctrl-p inside parentheses shows function args!


# mypy is missing a library stub file for module 'numpy' and will complain about it
# workaround: append --ignore-missing-imports to the mypy call (see https://github.com/python/mypy/issues/3905)
def make_santa_dict(dictionary: Dict[str, str], seed: Optional[int] = None, verbose: bool = False) -> Dict[str, str]:
    # type triple-quotes and press enter to generate empty docstring stub
    """
    creates a random secret santa assignment as a dictionary from an initial dictionary of the participants' names and\
    associated email addresses.

    :param dictionary: mapping names to email addresses
    :param seed: seed for numpy random number generator
    :param verbose: boolean to control print output
    :return: shuffled (randomized) dictionary, guaranteed not to map any name to its original email in `dictionary`
    """
    ######
    # Implementation note: the main challenge we have beyond simply shuffling a list is to ensure no one gets assigned
    # as their own secret santa. This means we need to exclude the participant from the secret santa choices as we go
    # through the list of participants.
    # However the last e-mail left to be assigned may be precisely the last participant's.
    # To see this, consider:
    # 1. we start with participants [a,b,c] and their e-mails [a@acme.com, b@acme.com, c@acme.com]
    # 2. random assignment of a to b@acme.com; a@acme.com and c@acme.com are left
    # 3. random assignment of b to a@acme.com; only c@acme.com is left
    # 4. only c is left, and only c's e-mail is left! We can only assign c to him/herself
    # If this situation occurs, we simply swap the last two entries, so e.g. c's assignment would be changed to
    # a@acme.com and b's to c@acme.com.
    ######

    # We need to map each person to some e-mail address, so we start by getting a list of all names
    # unpack dict_keys object into list literal (no control over order!)
    # https://stackoverflow.com/questions/16819222/how-to-return-dictionary-keys-as-a-list-in-python
    names = [*dictionary.keys()]

    # To store the shuffled dictionary, we initialize a new variable
    senddict: Dict[Union[str, Any], Union[str, Any]] = {}
    # To avoid the last assignee be one's own secret santa, we may need to swap the two last entries; therefore we need
    # to keep track of the second to last one. This variable must be defined here to avoid warnings about undefined
    # names.
    swapname1 = ''

    np.random.seed(seed)

    # "dict"s are always unordered, therefore iterating through them has unpredictable order
    for name in dictionary:
        # print(dictionary.get(name))
        if verbose:
            print(name)
        # PyCharm: Alt+Enter (on variable definition) -> Add type hint - automatically generates type given variable
        # assignment
        # `name` is the person getting a present, we want to pick their secret santa from the available participants
        pick = names.copy()
        if len(pick) == 1:
            # if this is the last person in the list, we only have one choice left
            picked = pick[0]
            # we check if the last person was the last available choice and if so, swap the last 2 entries
            if picked == name:
                swapname2 = picked
                tmp = senddict[swapname1]
                senddict[swapname1] = dictionary[picked]
                senddict[swapname2] = tmp
            else:
                senddict[name] = dictionary[picked]
        else:
            # if only 2 choices are left we keep track of the name, in case the last e-mail left is the last
            # participant's
            if len(pick) == 2:
                swapname1 = name
            # try:
            #     pick.remove(name)
            # except ValueError:
            #     pass
            # the above try-except is equivalent to:
            with suppress(ValueError):
                # A person shouldn't be their own secret santa, so we remove them as a possible pick
                pick.remove(name)
            # randomly pick a participant
            picked = np.random.choice(pick, 1)[0]
            if verbose:
                print(picked)
            # set `name`'s value in the result to the picked participant's e-mail.
            senddict[name] = dictionary[picked]
            names.remove(picked)

    return senddict


def send_santa_dict(smtpserverwithport: str, sender: str, pwd: str,
                    senddict: Dict[str, str], test: bool = False) -> Dict[str, Tuple[int, bytes]]:
    def santa_builder(email: Union[str, List[str]], person: str):
        return SecretSanta(email, person)
    return internal_send_santa_dict(smtpserverwithport, sender, pwd, senddict, santa_builder, test)


def internal_send_santa_dict(smtpserverwithport: str, sender: str, pwd: str, senddict: Dict[str, str], santabuilder,
                             test: bool = False) -> Dict[str, Tuple[int, bytes]]:
    # "\" is used in the docstring to escape the line ending in sphinx output
    """
    loops over a 'santa' dictionary and sends respective emails

    :param smtpserverwithport: SMTP server including port (colon-separated)
    :param sender: email address from which to send emails
    :param pwd: password for sender's email account
    :param senddict: mapping of names to email addresses
    :param test: boolean to allow test-run
    :return: all failed email sending attempts as returned by :func:`smtplib.sendmail()`, empty if all\
    were successful
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
