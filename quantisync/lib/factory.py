class NfsFactory:
    @classmethod
    def getObserver(cls, dirNfs, cloudFolder, blacklistedFolder):
        from quantisync.core.snapshot import LocalFolder, Observer

        localFolder = LocalFolder(dirNfs, 'XML', blacklistedFolder)
        return Observer(localFolder, cloudFolder)

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

    def __init__(self, view, cloudFolder, blacklistedFolder):
        self._view = view
        self._cloudFolder = cloudFolder
        self._blacklistedFolder = blacklistedFolder

    def getDefaultSync(self):
        from quantisync.core.model import syncDataModel
        from quantisync.core.sync import Sync, InvalidSettings

        DELAY = 2
        syncData = syncDataModel.getSyncData()

        if not syncData.nfsDir:
            raise InvalidSettings()

        nfsObserver = NfsFactory.getObserver(syncData.nfsDir, self._cloudFolder, self._blacklistedFolder)
        nfsHandler = NfsFactory.getHandler()
        return Sync(self._view, nfsObserver, nfsHandler, DELAY)
