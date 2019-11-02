from functools import partial

from quantisync.lib.network import HttpService
from quantisync.core.auth import KeyringTokenStorage, AuthService
from quantisync.core.model import SyncDataModel
from quantisync.core.logger import LoggerFactory
from quantisync.core.snapshot import LocalFolder, BlacklistedFolder, CloudFolder, Observer
from quantisync.core.nf.nf_handler import NfHandler, NfInsertionStrategy, NfDeletionStrategy
from quantisync.core.sync import Sync, SyncManager, UninitializedSync, InvalidSyncSettings


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
        self._logger = self._getLogger()
        self._syncManager = None

    def _getLogger(self):
        env = self._config['env']
        logger = LoggerFactory.getRootLogger()
        if env == 'dev':
            logger = LoggerFactory.getDevLogger()
        elif env == 'prod':
            logger = LoggerFactory.getProdLogger(self._config['storage']['LOG_PATH'])
        return logger

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
                    delay=self._config['sync']['DELAY'],
                    logger=self._logger)

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

    @property
    def logger(self):
        return self._logger
