from http import HTTPStatus

from requests.exceptions import HTTPError
import keyring.backends.Windows
import keyring


class InvalidUser(Exception):
    pass


class EmptyEmail(Exception):
    pass


class KeyringTokenStorage():

    def __init__(self, serviceName):
        self._serviceName = serviceName
        keyring.set_keyring(keyring.backends.Windows.WinVaultKeyring())

    def setToken(self, token):
        keyring.set_password(self._serviceName, '', token)

    def deleteToken(self):
        try:
            keyring.delete_password(self._serviceName, '')
        except Exception:
            raise

    def hasToken(self):
        return bool(self.getToken())

    def getToken(self):
        credential = keyring.get_credential(self._serviceName, '')
        if credential:
            return credential.password
        else:
            return None


class Auth:
    """
    Classe responsável pela autenticação do usuário
    """

    def __init__(self, httpService, tokenStorageService):
        self._httpService = httpService
        self._tokenStorageService = tokenStorageService

    def signin(self, email, password):
        if not email:
            raise EmptyEmail()

        token = self._requestToken(email, password)
        self._tokenStorageService.setToken(token)
        return token

    def signout(self):
        self._tokenStorageService.deleteToken()

    def _requestToken(self, email, senha):
        try:
            response = self._httpService.post({
                'email': email,
                'senha': senha
            })
            return response.json()['token']
        except HTTPError as error:
            if error.response.status_code == HTTPStatus.UNAUTHORIZED:
                raise InvalidUser()
            else:
                raise

    def getToken(self):
        return self._tokenStorageService.getToken()

    def hasToken(self):
        return self._tokenStorageService.hasToken()
