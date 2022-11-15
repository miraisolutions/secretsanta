from unittest import TestCase
from unittest.mock import patch

from secretsanta.main.core import SecretSanta


class TestSecretSanta(TestCase):
    def test_secret_santa_init___result_has_helper_rudolph(self):
        res = SecretSanta('me@gmail.com', 'you')
        self.assertEqual('rudolph', res.helper)

    def test_secret_santa_init___email_attribute_is_string(self):
        res = SecretSanta('me@gmail.com', 'you')
        self.assertTrue(isinstance(res.email, str))

    @patch('smtplib.SMTP')
    def test_secret_santa_send(self, mock_smtp):
        """
        Test that the send implementation sends a message containing the specified variable content and metadata
        """
        santa_email = 'me@gmail.com'
        res = SecretSanta(santa_email, 'you')
        from_address = "i@gmail.com"
        subject = "Santa Unit Test"
        message = "It's a unit test"
        res.send(subject, from_address, message, mock_smtp, test=True)
        # use a custom validator (we only care that the message sent to SMTP contains our parameters)
        mock_smtp.sendmail.assert_called_with(from_address, santa_email,
                                              SantaMockMessageValidator("Santa", subject,
                                                                        santa_email, message))


class SantaMockMessageValidator(object):
    """
    Mock object validator: overrides equality operator to control match conditions inside `assert_called_with`,
    using the provided parameters to check that the produced string (`other`) contains the expected values.
    """
    def __init__(self, sender: str, subject: str, santa_email: str, message: str):
        self.sender = sender
        self.subject = subject
        self.santa_email = santa_email
        self.message = message

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, str):
            return NotImplemented
        needed_elements = [self.sender, self.subject, self.santa_email, self.message]
        test = all(fragment in other for fragment in needed_elements)
        if not test:
            print("one of %s is missing in the produced SMTP message!" % needed_elements)
        return test
