import json
import os

from http import HTTPStatus

from quantisync.lib.network import HttpStreamQueue, HttpDeleteQueue
from quantisync.core.file import Properties
from quantisync.core.nf.nf_parser import NfParser, InvalidXml
from quantisync.core.nf.nf import Nf, InvalidNf


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
        self._enqueueInsertedNfs(insertions)
        self._dequeueInsertedNfs()

    def _enqueueInsertedNfs(self, insertions):
        for i in insertions:
            try:
                insertedNf = self._setupInsertedNf(i)
                self._insertedNfsQueue.enqueue(insertedNf.toDict())
            except (InvalidNf, InvalidXml) as e:                
                self._localFolder.addInvalidFile(e.filePath)
            except Exception:
                pass

    def _setupInsertedNf(self, state):                
        try:
            fileProperties = Properties.fromState(state)
            filePath = os.path.join(self._localFolder.getPath(),
                                    '{}.{}'.format(fileProperties.name,
                                                    self._localFolder.getExtension()))
            nfContent = NfParser.parse(filePath)
            nf = Nf(fileProperties, nfContent)
            return nf
        except InvalidNf:
            raise InvalidNf(filePath)
        except InvalidXml:
            raise InvalidXml(filePath)                  

    def _dequeueInsertedNfs(self):
        self._insertedNfsQueue.dequeue(self._postBatchHandler)

    def _streamGenerator(self, nfs):
        for nf in nfs:
            yield json.dumps(nf, ensure_ascii=False).encode()

    def _postBatchHandler(self, response):
        if (response.status_code == HTTPStatus.OK):
            self._cloudFolder.setSnapshot(response.json())


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
