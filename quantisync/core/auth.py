from http import HTTPStatus

from requests.exceptions import HTTPError
import keyring.backends.Windows
import keyring


class InvalidUser(Exception):
    pass


class EmptyUser(Exception):
    pass


class KeyringTokenStorage():

    def __init__(self, serviceName):
        self._serviceName = serviceName
        keyring.set_keyring(keyring.backends.Windows.WinVaultKeyring())

    def setToken(self, token):
        keyring.set_password(self._serviceName, 'token', token)

    def deleteToken(self):
        try:
            keyring.delete_password(self._serviceName, 'token')
        except keyring.errors.PasswordDeleteError:
            pass

    def hasToken(self):
        return bool(self.getToken())

    def getToken(self):
        credential = keyring.get_credential(self._serviceName, 'token')
        if credential:
            return credential.password
        else:
            return None


class AuthService:
    """
    Classe responsável pela autenticação do usuário
    """

    def __init__(self, httpService, tokenStorageService, syncDataModel):
        self._httpService = httpService
        self._tokenStorageService = tokenStorageService
        self._syncDataModel = syncDataModel

    def signin(self, email, password):
        if not email or not password:
            raise EmptyUser()

        session = self._requestSession(email, password)
        self._tokenStorageService.setToken(session['token'])
        userEmail = session['usuario']['email']
        # TODO -Trocar para nome fantasia
        userOrg = session['organizacao']['razaoSocial']
        self._syncDataModel.setUser(userEmail, userOrg)
        return session

    def signout(self):
        self._tokenStorageService.deleteToken()
        self._syncDataModel.setUser('', '')

    def _requestSession(self, email, senha):
        try:
            response = self._httpService.post({
                'email': email,
                'senha': senha
            })
            return response.json()
        except HTTPError as error:
            if error.response.status_code == HTTPStatus.UNAUTHORIZED or \
                    error.response.status_code == HTTPStatus.BAD_REQUEST:
                raise InvalidUser()
            else:
                raise

    def getToken(self):
        return self._tokenStorageService.getToken()

    def isAuthenticated(self):
        return self._tokenStorageService.hasToken()
