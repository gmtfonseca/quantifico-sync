import unittest
from unittest.mock import patch

# from quantisync.core.model import SyncDataModel
# from quantisync.core.auth import AuthService, EmptyUser, KeyringTokenStorage
from tests.config import FIXTURE_PATH

SYNC_DATA_PATH = FIXTURE_PATH / 'sync_data_auth.json'


class KeyringAuthTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_exception_when_empty_user(self):
        pass

    @patch('quantisync.core.auth.AuthService._requestSession')
    def test_token_update_when_signin(self, _requestSession):
        pass

    @patch('quantisync.core.auth.AuthService._requestSession')
    def test_token_update_when_signout(self, _requestSession):
        pass


if __name__ == '__main__':
    unittest.main()
