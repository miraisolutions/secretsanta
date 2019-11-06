from unittest import TestCase

from secretsanta.main.core import SecretSanta


class InitializeSecretSanta(TestCase):
    def test_secret_santa_init___result_has_helper_rudolph(self):
        res = SecretSanta('me@gmail.com', 'you')
        self.assertEqual('rudolph', res.helper)

    def test_secret_santa_init___email_attribute_is_string(self):
        res = SecretSanta('me@gmail.com', 'you')
        self.assertTrue(isinstance(res.email, str))
