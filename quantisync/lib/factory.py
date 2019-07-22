class NfsFactory:
    @classmethod
    def getObserver(cls, nfsPath, serverSnapshotPath, invalidSnapshotPath):
        from quantisync.core.snapshot import Client, Server, Invalid, Observer

        invalid = Invalid(invalidSnapshotPath)
        client = Client(nfsPath, 'XML', invalid)
        server = Server(serverSnapshotPath)
        return Observer(client, server)

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
        from quantisync.config.storage import SERVER_SNAPSHOT_PATH, INVALID_SNAPSHOT_PATH
        from quantisync.core.settings import SettingsSerializer
        from quantisync.core.sync import Sync, InvalidSettings

        DELAY = 5
        settingsSerializer = SettingsSerializer()
        settings = settingsSerializer.load()

        if not settings.nfsDir:
            raise InvalidSettings()

        nfsObservador = NfsFactory.getObserver(settings.nfsDir, SERVER_SNAPSHOT_PATH, INVALID_SNAPSHOT_PATH)
        nfsHandler = NfsFactory.getHandler()
        return Sync(self._view, nfsObservador, nfsHandler, DELAY)
