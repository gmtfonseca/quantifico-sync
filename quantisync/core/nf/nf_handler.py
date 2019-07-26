import json
from pathlib import Path
from http import HTTPStatus

from requests.exceptions import HTTPError

from quantisync.lib.network import HttpStreamQueue, HttpDeleteQueue
from quantisync.lib.shell import ShellIcon
from quantisync.core.file import Properties
from quantisync.core.nf.nf_parser import NfParser, InvalidNf
from quantisync.core.nf.nf import Nf


class NfHandler():
    '''
    Responsável em realizar ações em cima de mudanças de estado entre Cliente e Servidor
    '''

    def __init__(self, httpService):
        self._httpService = httpService

    def onInsert(self, localFolder, cloudFolder, insertions):
        nfInsertionStrategy = NfInsertionStrategy(self._httpService,
                                                  localFolder,
                                                  cloudFolder)
        nfInsertionStrategy.insert(insertions)

    def onDelete(self, cloudFolder, deletions):
        nfDeletionStrategy = NfDeletionStrategy(self._httpService,
                                                cloudFolder)
        nfDeletionStrategy.delete(deletions)


class NfInsertionStrategy:

    def __init__(self, httpService, localFolder, cloudFolder):
        self._localFolder = localFolder
        self._cloudFolder = cloudFolder
        self._insertedNfsQueue = HttpStreamQueue(httpService,
                                                 self._streamGenerator)

    def insert(self, insertions):
        self._updateOverlayIcons()
        self._enqueueInsertedNfs(insertions)
        self._dequeueInsertedNfs()

    def _enqueueInsertedNfs(self, insertions):
        for i in insertions:
            try:
                insertedNf = self._setupInsertedNf(i)
                self._insertedNfsQueue.enqueue(insertedNf.toDict())
                self._localFolder.removeFromBlacklist(insertedNf.fileProperties.name)
            except InvalidNf as e:
                self._localFolder.addToBlacklist(e.filePath)
                self._updateOverlayIcons()
            except FileNotFoundError:
                pass

    def _setupInsertedNf(self, state):
        fileProperties = Properties.fromState(state)
        filePath = Path(self._localFolder.getPath()) / fileProperties.name
        fileContent = NfParser.parse(str(filePath))
        nf = Nf(fileProperties, fileContent)
        return nf

    def _dequeueInsertedNfs(self):
        try:
            self._insertedNfsQueue.dequeue(self._postBatchHandler)
        except HTTPError as e:
            print(e)
            # TODO - Add blacklist
            raise

    def _streamGenerator(self, nfs):
        for nf in nfs:
            yield json.dumps(nf, ensure_ascii=False).encode()

    def _postBatchHandler(self, response):
        if (response.status_code == HTTPStatus.OK):
            self._cloudFolder.setSnapshot(response.json())
            self._updateOverlayIcons()
            # TODO - Update blacklist folder

    def _updateOverlayIcons(self):
        ShellIcon.updateDir(self._localFolder.getPath())


class NfDeletionStrategy:

    def __init__(self, httpService, cloudFolder):
        self._cloudFolder = cloudFolder
        self._deletedNfsQueue = HttpDeleteQueue(httpService)

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
