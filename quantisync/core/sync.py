import wx
import time
import logging
from threading import Thread
from enum import Enum
from http import HTTPStatus

from requests.exceptions import ConnectionError, HTTPError
from urllib3.connection import NewConnectionError

from ui.events import SyncEvent, myEVT_SYNC


class State(Enum):
    '''
    Representa o estado de um objeto Sync (Thread)
    '''
    NORMAL = 0
    SYNCING = 1
    NO_CONNECTION = 2
    UNAUTHORIZED = 3


class SyncManager:
    '''
    Encapsula uma Thread de Sync, sendo responsável por criar e abortar a mesma
    '''

    def __init__(self, syncFactory, view):
        self._syncFactory = syncFactory
        self._view = view
        self._sync = None

    def startSync(self):
        self._sync = self._syncFactory(self._view)
        self._sync.start()

    def stopSync(self):
        if self._sync:
            self._sync.abort()


class Sync(Thread):
    '''
    Thread responsável por realizar sincronização de arquivos
    '''

    def __init__(self, view, observer, handler, delay):
        super().__init__()
        self._view = view
        self._observer = observer
        self._handler = handler
        self._delay = delay
        self._abort = False

    def run(self):
        while True:
            if self._abort:
                return

            self._observeChanges()
            time.sleep(self._delay)

    def abort(self):
        self._abort = True

    def _observeChanges(self):
        self._observer.observe()
        if self._observer.hasChanged():
            self._handleChanges()

    def _handleChanges(self):
        try:
            self._postSyncEvent(State.SYNCING)
            self._handleSync()
            self._postSyncEvent(State.NORMAL)
        except (NewConnectionError, ConnectionError):
            self.abort()
            self._postSyncEvent(State.NO_CONNECTION, True)
        except HTTPError as error:
            if error.response.status_code == HTTPStatus.UNAUTHORIZED:
                self.abort()
                self._postSyncEvent(State.UNAUTHORIZED, True)

    def _handleSync(self):
        if self._observer.hasDeletions():
            self._handleDeletions()
        if self._observer.hasInsertions():
            self._handleInsertions()
        if self._observer.hasBlacklistedGhostFiles():
            self._handleBlacklistedGhostFiles()

    def _handleInsertions(self):
        logging.debug('Inserindo')
        self._handler.onInsert(self._observer.getInsertions())

    def _handleDeletions(self):
        logging.debug('Removendo')
        self._handler.onDelete(self._observer.getDeletions())

    def _handleBlacklistedGhostFiles(self):
        '''
        Remove arquivos que estão na blacklist e não existem mais no FileSystem
        Este cenário acontece quando arquivos que não foram importados por alguma
        razão foram removidos pelo usuário
        '''
        logging.debug('Ghost files')
        self._observer.getLocalFolder().removeBlacklistedGhostFiles()

    def _postSyncEvent(self, state, isFatal=False):
        evt = SyncEvent(myEVT_SYNC, -1, state, isFatal)
        wx.PostEvent(self._view, evt)
