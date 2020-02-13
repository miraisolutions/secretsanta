from unittest import TestCase
from unittest.mock import patch, ANY

from secretsanta.main.core import SecretSanta


class InitializeSecretSanta(TestCase):
    def test_secret_santa_init___result_has_helper_rudolph(self):
        res = SecretSanta('me@gmail.com', 'you')
        self.assertEqual('rudolph', res.helper)

    def test_secret_santa_init___email_attribute_is_string(self):
        res = SecretSanta('me@gmail.com', 'you')
        self.assertTrue(isinstance(res.email, str))

    # @patch('email.mime.multipart.MIMEMultipart')

    @patch('smtplib.SMTP')
    def test_secret_santa_send(self, mock_smtp):
        santa_email = 'me@gmail.com'
        res = SecretSanta(santa_email, 'you')
        from_address = "i@gmail.com"
        subject = "Santa Unit Test"
        message = "It's a unit test"
        res.send(subject, from_address, message, mock_smtp, test=True)
        mock_smtp.sendmail.assert_called_with(from_address, santa_email,
                                              SantaMessageValidator("Santa", subject,
                                                                    santa_email, message))


class SantaMessageValidator(object):
    def __init__(self, sender: str, subject: str, santa_email: str, message: str):
        self.sender = sender
        self.subject = subject
        self.santa_email = santa_email
        self.message = message

    def __eq__(self, other: str):
        needed_elements = [self.sender, self.subject, self.santa_email, self.message]
        test = all(fragment in other for fragment in needed_elements)
        if not test:
            print("one of %s is missing " % needed_elements)
        return test
