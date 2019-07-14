class NfsFactory:
    @classmethod
    def getObservador(cls, nfsPath, picklePath):
        from quantisync.core.estado import Cliente, Servidor, Observador

        cliente = Cliente(nfsPath, 'XML')
        servidor = Servidor(picklePath)
        return Observador(cliente, servidor)

    @classmethod
    def getHandler(cls):
        from quantisync.lib.network import HttpService
        from quantisync.core.nf.nf_handler import NfHandler

        httpService = HttpService('sync/nfs')
        return NfHandler(httpService)


class AuthFactory:

    @classmethod
    def getKeyringTokenStorage(cls):
        from quantisync.lib.auth import KeyringTokenStorage
        from quantisync.config import auth
        return KeyringTokenStorage(auth.SERVICE_NAME)

    @classmethod
    def getKeyringAuth(cls):
        from quantisync.lib.auth import Auth
        from quantisync.lib.network import HttpService

        httpService = HttpService('sessao')
        keyringAuthStorge = cls.getKeyringStorage()
        return Auth(httpService, keyringAuthStorge)
