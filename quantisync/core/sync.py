import wx
import time
import logging
from threading import Thread
from enum import Enum
from http import HTTPStatus

from requests.exceptions import ConnectionError, HTTPError
from urllib3.connection import NewConnectionError

from ui.events import EVT_SYNC, myEVT_SYNC


class InvalidSettings(Exception):
    pass


class Estado(Enum):
    """
    Representa o estado de um objeto Sync (Thread)
    """
    NORMAL = 0
    SYNCING = 1
    NO_CONNECTION = 2
    UNAUTHORIZED = 3


class SyncManager:
    """
    Classe que encapsula o gerenciamento de um Sync
    """

    def __init__(self, syncFactory):
        self._syncFactory = syncFactory
        self._sync = None

    def startSync(self):
        self._sync = self._syncFactory.getDefaultSync()
        self._sync.start()

    def abortSync(self):
        if self._sync:
            self._sync.abort()

    def restartSync(self):
        self.abortSync()
        self.startSync()


class Sync(Thread):
    """
    Thread responsável por realizar sincronização de arquivos
    """

    def __init__(self, view, observador, handler, delay):
        super().__init__()
        self._view = view
        self._observador = observador
        self._handler = handler
        self._delay = delay
        self._abort = False

    def run(self):
        while True:
            if self._abort:
                return

            self._observaMudancas()
            time.sleep(self._delay)

    def abort(self):
        self._abort = True

    def _observaMudancas(self):
        self._observador.observe()
        if self._observador.hasChanged():
            self._handleMudancas()

    def _handleMudancas(self):
        try:
            self._propagaEstadoView(Estado.SYNCING)
            self._handleInsercoesRemocoes()
            self._propagaEstadoView(Estado.NORMAL)
        except (NewConnectionError, ConnectionError):
            self._propagaEstadoView(Estado.NO_CONNECTION, True)
        except HTTPError as error:
            if error.response.status_code == HTTPStatus.UNAUTHORIZED:
                self._propagaEstadoView(Estado.UNAUTHORIZED, True)

    def _handleInsercoesRemocoes(self):
        if self._observador.hasInsertions():
            self._handleInsercoes()
        if self._observador.hasDeletions():
            self._handleRemocoes()

    def _handleInsercoes(self):
        logging.debug('Inserindo')
        self._handler.onInsercao(self._observador.client,
                                 self._observador.server,
                                 self._observador.getInsertions())

    def _handleRemocoes(self):
        logging.debug('Removendo')
        self._handler.onRemocao(self._observador.server,
                                self._observador.getDeletions())

    def _propagaEstadoView(self, estado, isFatal=False):
        evt = EVT_SYNC(myEVT_SYNC, -1, estado, isFatal)
        wx.PostEvent(self._view, evt)
