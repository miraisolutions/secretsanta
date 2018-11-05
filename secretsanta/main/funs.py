import smtplib
import numpy as np
from contextlib import suppress
from secretsanta.main.core import SecretSanta

# PyCharm: ctrl-p inside parentheses shows function args!


def make_santa_dict(dictionary, i):
    # type triple-quotes and press enter to generate empty docstring stub
    """
    creates a randomized 'santa' dictionary from an initial dictionary of names with associated email addresses

    :param dictionary:
    :param i:
    :return:
    """
    # unpack dict_keys object into list literal (no control over order!)
    # https://stackoverflow.com/questions/16819222/how-to-return-dictionary-keys-as-a-list-in-python
    names = [*dictionary.keys()]

    # initialize sending dictionary
    senddict = {}
    swap = False
    swapname2 = swapname1 = ''

    np.random.seed(i)

    # "dict"s are always unordered, therefore iterating through them has unpredictable order
    for name in dictionary:
        # print(dictionary.get(name))
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
        print(picked)
        senddict[name] = dictionary.get(picked)
        names.remove(picked)

    # if swap is necessary ...
    if swap:
        tmp = senddict[swapname1]
        senddict[swapname1] = senddict[swapname2]
        senddict[swapname2] = tmp

    return senddict


def send_santa_dict(smtpserverwithport, sender, pwd, senddict, i):
    """
    loops over a 'santa' dictionary and sends respective emails

    :param smtpserverwithport:
    :param sender:
    :param pwd:
    :param senddict:
    :param i:
    :return:
    """
    # create SMTP server object and connect
    server = smtplib.SMTP(smtpserverwithport)

    # start TLS, following SMTP commands will be encrypted
    server.starttls()

    from_addr = sender
    server.login(from_addr, pwd)

    subj = 'Secret Santa Test %i' % i
    check = 0

    for name in senddict:
        obj = SecretSanta(senddict.get(name), name)
        check = obj.send(subj, from_addr, 'you picked', server)

    server.quit()
    return check
