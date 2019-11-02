import wx
import time
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
    IDLE = 0
    SYNCING = 1
    NO_CONNECTION = 2
    UNINITIALIZED = 3


class UninitializedSync(Exception):
    pass


class InvalidSyncSettings(Exception):
    pass


class SyncManager(object):
    '''
    Encapsula uma Thread de Sync, sendo responsável por criar e abortar a mesma
    '''

    def __init__(self, syncFactory):
        self._syncFactory = syncFactory
        self._sync = None

    def start(self):
        self._sync = self._syncFactory()
        self._sync.start()

    def restart(self):
        self._stop(postEvent=False)
        self.start()

    def stop(self):
        self._stop(postEvent=True)

    def _stop(self, postEvent):
        '''
        O post event é usado para determinar se é necessário avisar a View que a thread foi abortada.
        No caso de reinicialização, a View não precisa responder a este evento.
        '''
        if self._sync:
            self._sync.abort(postEvent)

    def isRunning(self):
        return self._sync and self._sync.is_alive()

    @property
    def state(self):
        if not self._sync:
            raise UninitializedSync()

        return self._sync.state

    @property
    def localFolder(self):
        if not self._sync:
            raise UninitializedSync()

        return self._sync.localFolder

    @property
    def cloudFolder(self):
        if not self._sync:
            raise UninitializedSync()

        return self._sync.cloudFolder


class Sync(Thread):
    '''
    Thread responsável por realizar sincronização de arquivos
    '''

    def __init__(self, view, observer, handler, delay, logger):
        super().__init__()
        super().setDaemon(True)
        self._view = view
        self._observer = observer
        self._handler = handler
        self._delay = delay
        self._logger = logger
        self._abort = False
        self._state = State.UNINITIALIZED

    def run(self):
        while True:
            if self._abort:
                return

            self._observeChanges()
            time.sleep(self._delay)

    def start(self):
        self._setStateAndPostEvent(State.IDLE)
        super().start()

    def abort(self, postEvent):
        self._abort = True
        self._state = State.UNINITIALIZED
        if postEvent:
            self._postSyncEvent()

    def _observeChanges(self):
        self._observer.observe()
        if self._observer.hasChanged():
            self._handleChanges()

    def _handleChanges(self):
        try:
            self._setStateAndPostEvent(State.SYNCING)
            self._handleSync()
            self._setStateAndPostEvent(State.IDLE)
        except (NewConnectionError, ConnectionError) as error:
            self._logger.exception(error)
            self.abort(False)
            self._setStateAndPostEvent(State.NO_CONNECTION)
        except HTTPError as error:
            self._logger.exception(error)
            if error.response.status_code == HTTPStatus.UNAUTHORIZED:
                self.abort(False)
                self._setStateAndPostEvent(State.UNINITIALIZED)

    def _handleSync(self):
        if self._observer.hasDeletions():
            self._handleDeletions()
        if self._observer.hasInsertions():
            self._handleInsertions()
        if self._observer.hasBlacklistedGhostFiles():
            self._handleBlacklistedGhostFiles()

    def _handleInsertions(self):
        self._logger.debug('Inserindo')
        self._handler.onInsert(self._observer.insertions)

    def _handleDeletions(self):
        self._logger.debug('Removendo')
        self._handler.onDelete(self._observer.deletions)

    def _handleBlacklistedGhostFiles(self):
        '''
        Remove arquivos que estão na blacklist e não existem mais no FileSystem
        Este cenário acontece quando arquivos que não foram importados por alguma
        razão foram removidos pelo usuário
        '''
        self._logger.debug('Ghost Files')
        self._observer.localFolder.removeBlacklistedGhostFiles()

    def _setStateAndPostEvent(self, state):
        self._state = state
        self._postSyncEvent()

    def _postSyncEvent(self):
        evt = SyncEvent(myEVT_SYNC, -1, self._state)
        wx.PostEvent(self._view, evt)

    @property
    def localFolder(self):
        return self._observer.localFolder

    @property
    def cloudFolder(self):
        return self._observer.cloudFolder

    @property
    def state(self):
        return self._state
