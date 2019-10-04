import json
from pathlib import Path
from http import HTTPStatus
from datetime import datetime

from quantisync.lib.network import HttpStreamQueue, HttpDeleteQueue
from quantisync.lib.shell import ShellIcon
from quantisync.core.file import Properties
from quantisync.core.nf.nf_parser import NfParser, InvalidNf
from quantisync.core.nf.nf import Nf


class NfHandler():
    '''
    Responsável em realizar ações em cima de mudanças de estado entre Cliente e Servidor
    '''

    def __init__(self, nfInsertionStrategy, nfDeletionStrategy, syncDataModel):
        self._nfInsertionStrategy = nfInsertionStrategy
        self._nfDeletionStrategy = nfDeletionStrategy
        self._syncDataModel = syncDataModel

    def onInsert(self, insertions):
        self._nfInsertionStrategy.insert(insertions)
        self._updateLastSyncDate()

    def onDelete(self, deletions):
        self._nfDeletionStrategy.delete(deletions)
        self._updateLastSyncDate()

    def _updateLastSyncDate(self):
        self._syncDataModel.setLastSync(datetime.now())


class NfInsertionStrategy:

    def __init__(self, httpService, localFolder, cloudFolder, batchSize):
        self._localFolder = localFolder
        self._cloudFolder = cloudFolder
        self._insertedNfsQueue = HttpStreamQueue(httpService,
                                                 self._streamGenerator,
                                                 batchSize)

    def insert(self, insertions):
        self._updateOverlayIcons()
        self._enqueueInsertedNfs(insertions)
        self._dequeueInsertedNfs()

    def _enqueueInsertedNfs(self, insertions):
        for i in insertions:
            try:
                insertedNf = self._initNfFromState(i)
                self._insertedNfsQueue.enqueue(insertedNf.toDict())
                self._localFolder.removeFromBlacklistIfExists(insertedNf.fileProperties.name)
            except InvalidNf as e:
                self._localFolder.addToBlacklistFromPath(e.filePath, 'Nota Fiscal inválida')
                self._updateOverlayIcons()
            except FileNotFoundError:
                pass

    def _initNfFromState(self, state):
        fileProperties = Properties.fromState(state)
        filePath = Path(self._localFolder.getPath()) / fileProperties.name
        fileContent = NfParser.parse(str(filePath))
        nf = Nf(fileProperties, fileContent)
        return nf

    def _dequeueInsertedNfs(self):
        self._insertedNfsQueue.dequeue(self._postBatchHandler)

    def _streamGenerator(self, nfs):
        for nf in nfs:
            yield json.dumps(nf, ensure_ascii=False).encode()

    def _postBatchHandler(self, response):
        if (response.status_code == HTTPStatus.OK):
            self._cloudFolder.setSnapshot(response.json()['estadoServidor'])
            self._handleBlacklistedFiles(response.json()['arquivosInvalidos'])
            self._updateOverlayIcons()

    def _handleBlacklistedFiles(self, invalidFiles):
        if invalidFiles:
            for file in invalidFiles:
                self._localFolder.addToBlacklistFromState(file['state'], file['error'])

    def _updateOverlayIcons(self):
        ShellIcon.updateDir(self._localFolder.getPath())


class NfDeletionStrategy:

    def __init__(self, httpService, cloudFolder, batchSize):
        self._cloudFolder = cloudFolder
        self._deletedNfsQueue = HttpDeleteQueue(httpService, batchSize)

    def delete(self, deletions):
        self._enqueueDeletedNfs(deletions)
        self._dequeueDeletedNfs()

    def _enqueueDeletedNfs(self, deletions):
        for d in deletions:
            deletedNf = Properties.fromState(d)
            self._deletedNfsQueue.enqueue(deletedNf.name)

    def _dequeueDeletedNfs(self):
        self._deletedNfsQueue.dequeue(self._postBatchHandler)

    def _postBatchHandler(self, response):
        if (response.status_code == HTTPStatus.OK):
            self._cloudFolder.setSnapshot(response.json())
