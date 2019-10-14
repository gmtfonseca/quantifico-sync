import os
from pathlib import Path
from functools import partial

from quantisync.lib.network import HttpService
from quantisync.core.auth import KeyringTokenStorage, AuthService
from quantisync.core.model import SyncDataModel
from quantisync.core.snapshot import LocalFolder, BlacklistedFolder, CloudFolder, Observer
from quantisync.core.nf.nf_handler import NfHandler, NfInsertionStrategy, NfDeletionStrategy
from quantisync.core.sync import Sync, SyncManager, UninitializedSync, InvalidSyncSettings


class InvalidSettings(Exception):
    pass


class App:

    def __init__(self, config):
        self._config = config
        self._syncDataModel = SyncDataModel(jsonPath=self._config['storage']['SYNC_DATA_PATH'])
        self._keyringTokenStorage = KeyringTokenStorage(serviceName=self._config['auth']['SERVICE_NAME'])
        self._authService = AuthService(self.httpService(endpoint='sessao'),
                                        tokenStorageService=self.keyringTokenStorage,
                                        syncDataModel=self.syncDataModel)
        self._cloudFolder = CloudFolder(self._config['storage']['CLOUD_SNAPSHOT_PATH'],
                                        self.httpService(endpoint='nfs/snapshot'))

        self._syncManager = None

    def httpService(self, endpoint):
        return HttpService(endpoint,
                           url=self._config['network']['HTTP_URL'],
                           tokenStorageService=self.keyringTokenStorage)

    def createSyncManager(self, view):
        self._syncManager = SyncManager(partial(self._syncFactory, view))

    def _syncFactory(self, view):

        nfsDir = self.syncDataModel.getSyncData().nfsDir

        if not nfsDir:
            raise InvalidSyncSettings()

        blacklistedFolder = BlacklistedFolder(self._config['storage']['BLACKLISTED_SNAPSHOT_PATH'])
        localFolder = LocalFolder(path=nfsDir,
                                  extension=self._config['sync']['NF_EXTENSION'],
                                  blacklistedFolder=blacklistedFolder)

        observer = Observer(localFolder=localFolder, cloudFolder=self._cloudFolder)

        nfInsertionStrategy = NfInsertionStrategy(httpService=self.httpService(endpoint='sync/nfs'),
                                                  localFolder=localFolder,
                                                  cloudFolder=self._cloudFolder,
                                                  batchSize=self._config['network']['MAX_BATCH_SIZE']['STREAM'])
        nfDeletionStrategy = NfDeletionStrategy(httpService=self.httpService(endpoint='sync/nfs'),
                                                cloudFolder=self._cloudFolder,
                                                batchSize=self._config['network']['MAX_BATCH_SIZE']['DELETE'])

        nfsHandler = NfHandler(nfInsertionStrategy=nfInsertionStrategy,
                               nfDeletionStrategy=nfDeletionStrategy,
                               syncDataModel=self.syncDataModel)
        sync = Sync(view=view,
                    observer=observer,
                    handler=nfsHandler,
                    delay=self._config['sync']['DELAY'])

        return sync

    @property
    def syncDataModel(self):
        return self._syncDataModel

    @property
    def keyringTokenStorage(self):
        return self._keyringTokenStorage

    @property
    def authService(self):
        return self._authService

    @property
    def cloudFolder(self):
        return self._cloudFolder

    @property
    def syncManager(self):
        if not self._syncManager:
            raise UninitializedSync()

        return self._syncManager


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
        'HTTP_URL': 'http://localhost:4000/',
        'MAX_BATCH_SIZE': {
            'STREAM': 40,
            'DELETE': 100
        }
    },
    'sync': {
        'NF_EXTENSION': 'XML',
        'DELAY': 2,
    }
}

app = App(config)
