class NfsFactory:
    @classmethod
    def getObserver(cls, dirNfs, cloudFolderPath, invalidFolderPath):
        from quantisync.core.snapshot import LocalFolder, CloudFolder, InvalidFolder, Observer

        invalidFolder = InvalidFolder(invalidFolderPath)
        localFolder = LocalFolder(dirNfs, 'XML', invalidFolder)
        cloudFolder = CloudFolder(cloudFolderPath)
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

    def __init__(self, view):
        self._view = view

    def getDefaultSync(self):
        from quantisync.config.storage import CLOUD_FOLDER_PATH, INVALID_FOLDER_PATH
        from quantisync.core.settings import SettingsSerializer
        from quantisync.core.sync import Sync, InvalidSettings

        DELAY = 5
        settingsSerializer = SettingsSerializer()
        settings = settingsSerializer.load()

        if not settings.nfsDir:
            raise InvalidSettings()

        nfsObserver = NfsFactory.getObserver(settings.nfsDir, CLOUD_FOLDER_PATH, INVALID_FOLDER_PATH)
        nfsHandler = NfsFactory.getHandler()
        return Sync(self._view, nfsObserver, nfsHandler, DELAY)
