class NfsFactory:
    @classmethod
    def getObservador(cls, nfsPath, cloudSnapshotPath):
        from quantisync.core.estado import Cliente, Servidor, Observador

        cliente = Cliente(nfsPath, 'XML')
        servidor = Servidor(cloudSnapshotPath)
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
        from quantisync.core.auth import KeyringTokenStorage
        from quantisync.config import auth
        return KeyringTokenStorage(auth.SERVICE_NAME)

    @classmethod
    def getKeyringAuth(cls):
        from quantisync.core.auth import Auth
        from quantisync.lib.network import HttpService

        httpService = HttpService('sessao')
        keyringTokenStorage = cls.getKeyringTokenStorage()
        return Auth(httpService, keyringTokenStorage)


class SyncFactory:

    def __init__(self, view):
        self._view = view

    def getDefaultSync(self):
        from quantisync.config.storage import CLOUD_SNAPSHOT_PATH
        from quantisync.core.settings import SettingsSerializer
        from quantisync.core.sync import Sync, InvalidSettings

        DELAY = 5
        settingsSerializer = SettingsSerializer()
        settings = settingsSerializer.load()

        if not settings.nfsDir:
            raise InvalidSettings()

        nfsObservador = NfsFactory.getObservador(settings.nfsDir, CLOUD_SNAPSHOT_PATH)
        nfsHandler = NfsFactory.getHandler()
        return Sync(self._view, nfsObservador, nfsHandler, DELAY)
