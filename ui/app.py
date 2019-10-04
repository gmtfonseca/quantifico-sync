import os
from pathlib import Path

from quantisync.lib.network import HttpService
from quantisync.core.auth import KeyringTokenStorage, AuthService
from quantisync.core.model import SyncDataModel
from quantisync.core.snapshot import LocalFolder, BlacklistedFolder, CloudFolder, Observer
from quantisync.core.nf.nf_handler import NfHandler, NfInsertionStrategy, NfDeletionStrategy
from quantisync.core.sync import Sync


class NotInitializedSync(Exception):
    pass


class InvalidSettings(Exception):
    pass


class App:

    def __init__(self, config):
        self.config = config
        self.syncDataModel = SyncDataModel(jsonPath=self.config['storage']['SYNC_DATA_PATH'])
        self.keyringTokenStorage = KeyringTokenStorage(serviceName=self.config['auth']['SERVICE_NAME'])
        self.authService = AuthService(self.httpService(endpoint='sessao'),
                                       tokenStorageService=self.keyringTokenStorage,
                                       syncDataModel=self.syncDataModel)

        self._sync = None
        self._localFolder = None
        self._cloudFolder = None

    def httpService(self, endpoint):
        return HttpService(endpoint,
                           url=self.config['network']['HTTP_URL'],
                           tokenStorageService=self.keyringTokenStorage)

    def createSync(self, view):
        nfsDir = self.syncDataModel.getSyncData().nfsDir

        if not nfsDir:
            raise InvalidSettings()

        blacklistedFolder = BlacklistedFolder(self.config['storage']['BLACKLISTED_SNAPSHOT_PATH'])
        self._localFolder = LocalFolder(path=nfsDir,
                                        extension=self.config['sync']['NF_EXTENSION'],
                                        blacklistedFolder=blacklistedFolder)
        self._cloudFolder = CloudFolder(self.config['storage']['CLOUD_SNAPSHOT_PATH'])
        observer = Observer(localFolder=self._localFolder, cloudFolder=self._cloudFolder)

        nfInsertionStrategy = NfInsertionStrategy(httpService=self.httpService(endpoint='sync/nfs'),
                                                  localFolder=self._localFolder,
                                                  cloudFolder=self._cloudFolder,
                                                  batchSize=self.config['network']['MAX_BATCH_SIZE']['STREAM'])
        nfDeletionStrategy = NfDeletionStrategy(httpService=self.httpService(endpoint='sync/nfs'),
                                                cloudFolder=self._cloudFolder,
                                                batchSize=self.config['network']['MAX_BATCH_SIZE']['DELETE'])

        nfsHandler = NfHandler(nfInsertionStrategy=nfInsertionStrategy,
                               nfDeletionStrategy=nfDeletionStrategy,
                               syncDataModel=self.syncDataModel)
        sync = Sync(view=view,
                    observer=observer,
                    handler=nfsHandler,
                    delay=self.config['sync']['DELAY'])

        self._sync = sync

    def sync(self):
        if not self.sync:
            raise NotInitializedSync()

        return self._sync

    def localFolder(self):
        if not self._localFolder:
            raise NotInitializedSync()

        return self._localFolder

    def cloudFolder(self):
        if not self._cloudFolder:
            raise NotInitializedSync()

        return self._cloudFolder


APPDATA_PATH = Path(os.getenv('LOCALAPPDATA')) / 'Quantifico'

config = {
    'storage': {
        'SYNC_DATA_PATH': APPDATA_PATH / 'sync_data.json',
        'CLOUD_SNAPSHOT_PATH': APPDATA_PATH / 'cloud.dat',
        'BLACKLISTED_SNAPSHOT_PATH': APPDATA_PATH / 'blacklisted.dat'
    },
    'auth': {
        'SERVICE_NAME': 'quantisync',

    },
    'network': {
        'HTTP_URL': 'http://localhost:3000/',
        'MAX_BATCH_SIZE': {
            'STREAM': 40,
            'DELETE': 100
        }
    },
    'sync': {
        'NF_EXTENSION': 'XML',
        'DELAY': 5,
    }
}

app = App(config)
