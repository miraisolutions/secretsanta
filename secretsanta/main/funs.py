import smtplib
import numpy as np
import datetime
from contextlib import suppress
from secretsanta.main.core import SecretSanta

# PyCharm: ctrl-p inside parentheses shows function args!


def make_santa_dict(dictionary, seed=None, verbose=False):
    # type triple-quotes and press enter to generate empty docstring stub
    """
    creates a randomized 'santa' dictionary from an initial dictionary of names with associated email addresses

    :param dictionary: mapping names to email addresses
    :param seed: seed for numpy RNG
    :param verbose: boolean to control print output
    :return: shuffled (randomized) dictionary
    """
    # unpack dict_keys object into list literal (no control over order!)
    # https://stackoverflow.com/questions/16819222/how-to-return-dictionary-keys-as-a-list-in-python
    names = [*dictionary.keys()]

    # initialize sending dictionary
    senddict = {}
    swap = False
    swapname2 = swapname1 = ''

    np.random.seed(seed)

    # "dict"s are always unordered, therefore iterating through them has unpredictable order
    for name in dictionary:
        # print(dictionary.get(name))
        if verbose:
            print(name)
        pick = names.copy()
        if len(pick) == 2:
            swapname1 = name
        if len(pick) == 1:
            picked = pick[0]
            if picked == name:
                swap = True
                swapname2 = picked
        else:
            # try:
            #     pick.remove(name)
            # except ValueError:
            #     pass
            with suppress(ValueError):
                pick.remove(name)
            picked = np.random.choice(pick, 1)[0]
        if verbose:
            print(picked)
        senddict[name] = dictionary.get(picked)
        names.remove(picked)

    # if swap is necessary ...
    if swap:
        tmp = senddict[swapname1]
        senddict[swapname1] = senddict[swapname2]
        senddict[swapname2] = tmp

    return senddict


def send_santa_dict(smtpserverwithport, sender, pwd, senddict, test=False):
    """
    loops over a 'santa' dictionary and sends respective emails

    :param smtpserverwithport: SMTP server including port (colon-separated)
    :param sender: email address from which to send emails
    :param pwd: password for sender's email account
    :param senddict: mapping of names to email addresses
    :param test: boolean to allow test-run
    :return: send-status of last email
    """
    # create SMTP server object and connect
    server = smtplib.SMTP(smtpserverwithport)

    # start TLS, following SMTP commands will be encrypted
    server.starttls()

    server.login(sender, pwd)

    subj = 'Secret Santa %d' % datetime.datetime.now().year
    check = 0

    for name in senddict:
        obj = SecretSanta(senddict.get(name), name)
        check = obj.send(subj, sender, 'You picked', server, test)

    server.quit()
    return check
