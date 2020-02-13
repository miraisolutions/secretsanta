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
        res.send("Santa Unit Test", from_address, "It's a unit test", mock_smtp, test=True)
        mock_smtp.sendmail.assert_called_with(from_address, santa_email, ANY)
