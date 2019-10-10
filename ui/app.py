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
        self.config = config
        self.syncDataModel = SyncDataModel(jsonPath=self.config['storage']['SYNC_DATA_PATH'])
        self.keyringTokenStorage = KeyringTokenStorage(serviceName=self.config['auth']['SERVICE_NAME'])
        self.authService = AuthService(self.httpService(endpoint='sessao'),
                                       tokenStorageService=self.keyringTokenStorage,
                                       syncDataModel=self.syncDataModel)

        self._syncManager = None

    def httpService(self, endpoint):
        return HttpService(endpoint,
                           url=self.config['network']['HTTP_URL'],
                           tokenStorageService=self.keyringTokenStorage)

    def createSyncManager(self, view):
        self._syncManager = SyncManager(partial(self._syncFactory, view))

    def _syncFactory(self, view):

        nfsDir = self.syncDataModel.getSyncData().nfsDir

        if not nfsDir:
            raise InvalidSyncSettings()

        blacklistedFolder = BlacklistedFolder(self.config['storage']['BLACKLISTED_SNAPSHOT_PATH'])
        localFolder = LocalFolder(path=nfsDir,
                                  extension=self.config['sync']['NF_EXTENSION'],
                                  blacklistedFolder=blacklistedFolder)
        cloudFolder = CloudFolder(self.config['storage']['CLOUD_SNAPSHOT_PATH'],
                                  self.httpService(endpoint='nfs/snapshot'))
        observer = Observer(localFolder=localFolder, cloudFolder=cloudFolder)

        nfInsertionStrategy = NfInsertionStrategy(httpService=self.httpService(endpoint='sync/nfs'),
                                                  localFolder=localFolder,
                                                  cloudFolder=cloudFolder,
                                                  batchSize=self.config['network']['MAX_BATCH_SIZE']['STREAM'])
        nfDeletionStrategy = NfDeletionStrategy(httpService=self.httpService(endpoint='sync/nfs'),
                                                cloudFolder=cloudFolder,
                                                batchSize=self.config['network']['MAX_BATCH_SIZE']['DELETE'])

        nfsHandler = NfHandler(nfInsertionStrategy=nfInsertionStrategy,
                               nfDeletionStrategy=nfDeletionStrategy,
                               syncDataModel=self.syncDataModel)
        sync = Sync(view=view,
                    observer=observer,
                    handler=nfsHandler,
                    delay=self.config['sync']['DELAY'])

        return sync

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
        'HTTP_URL': 'http://localhost:3000/',
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
