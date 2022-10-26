import click
import json

from secretsanta.main import funs as secretsanta

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version='0.0.1')
def santa():
    pass


@santa.command()
@click.argument('json', type=click.Path(exists=True))
@click.option('--test_run', is_flag=True, help='do a test run with fixed seed')
def makedict(**kwargs):
    """
    Make a randomized dictionary of secret santa assignments.

    JSON is the path to a json file containing the set of participants with names and email addresses.
    """
    f_participants = kwargs['json']
    with open(f_participants, 'r') as f:
        participants = json.load(f)
    print(participants)
    assignments = secretsanta.make_santa_dict(participants, seed=666 if kwargs['test_run'] else None)
    print(assignments)


@santa.command()
@click.argument('json', type=click.Path(exists=True))
@click.option('--smtp', default='smtp.gmail.com:587', help='smtp server with port')
@click.option('--sender', default='santa.claus@acme-example.com', help='sender email address')
@click.option('--pwd', default='1234', help='password for sender')
@click.option('--test_run', default=True, is_flag=True, help='do a test run without sending emails')
def senddict(**kwargs):
    """
    Send emails for a set of secret santa assignments.

    JSON is the path to a json file containing the set of assignments with names and email addresses.
    """
    f_assignments = kwargs['json']
    with open(f_assignments, 'r') as f:
        assignments = json.load(f)
    check = secretsanta.send_santa_dict(
        kwargs['smtp'],
        kwargs['sender'],
        kwargs['pwd'],
        assignments,
        test=kwargs['test_run']
    )
    print(check)


if __name__ == '__main__':
    santa()
