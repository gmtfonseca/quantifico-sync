import unittest
from unittest.mock import Mock, patch


# from requests.exceptions import HTTPError

from quantisync.core.auth import Auth, EmptyEmail, KeyringTokenStorage  # , InvalidUser
# from tests.shared import MockResponse


class KeyringAuthTest(unittest.TestCase):

    def setUp(self):
        httpService = Mock()
        keyringTokenStorage = KeyringTokenStorage('test')
        self.auth = Auth(httpService, keyringTokenStorage)

    def test_exception_when_empty_email(self):
        """
        Email em branco deve disparar exception
        """
        with self.assertRaises(EmptyEmail):
            self.auth.signin('', '')

    @patch('quantisync.core.auth.Auth._requestSession')
    def test_token_update_when_signin(self, _requestSession):
        """
        Signin deve atualizar token corretamente
        """
        _requestSession.return_value = {'token': 'valid_token'}
        self.auth.signin('gustavo', '1234')
        self.assertEqual(self.auth.getToken(), 'valid_token')

    @patch('quantisync.core.auth.Auth._requestSession')
    def test_token_update_when_signout(self, _requestSession):
        """
        Signout deve remover token corretamente
        """
        self.auth.signin('gustavo', '1234')
        self.auth.signout()
        self.assertIsNone(self.auth.getToken())


if __name__ == '__main__':
    unittest.main()
