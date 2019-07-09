from .events import UIEvent, myEVT_UI
from requests.exceptions import ConnectionError, HTTPError
from urllib3.connection import NewConnectionError
from threading import Thread
from enum import Enum
from http import HTTPStatus
import time
import wx
import logging


class Estado(Enum):
    NORMAL = 0
    SYNCING = 1
    NO_CONNECTION = 2
    UNAUTHORIZED = 3


class BackgroundThread(Thread):

    def __init__(self, observador, handler, delay, parent):
        super().__init__()
        self._observador = observador
        self._handler = handler
        self._delay = delay
        self._parent = parent
        self._abort = False

    def run(self):
        while True:
            if self._abort:
                return

            self._observaMudancas()
            time.sleep(self._delay)

    def _observaMudancas(self):
        self._observador.observar()
        if self._observador.possuiMudancas():
            self._handleMudancas()

    def _handleMudancas(self):
        try:
            self._propagaEstadoUI(Estado.SYNCING)
            self._handleInsercoesRemocoes()
            self._propagaEstadoUI(Estado.NORMAL)
        except (NewConnectionError, ConnectionError):
            self._propagaEstadoUI(Estado.NO_CONNECTION, True)
        except HTTPError as error:
            if error.response.status_code == HTTPStatus.UNAUTHORIZED:
                self._propagaEstadoUI(Estado.UNAUTHORIZED, True)

    def _handleInsercoesRemocoes(self):
        if self._observador.possuiInsercoes():
            self._handleInsercoes()
        if self._observador.possuiRemocoes():
            self._handleRemocoes()

    def _handleInsercoes(self):
        logging.debug('Inserindo')
        self._handler.onInsercao(self._observador.cliente,
                                 self._observador.servidor,
                                 self._observador.getInsercoes())

    def _handleRemocoes(self):
        logging.debug('Removendo')
        self._handler.onRemocao(self._observador.servidor,
                                self._observador.getRemocoes())

    def _propagaEstadoUI(self, estado, isFatal=False):
        evt = UIEvent(myEVT_UI, -1, estado, isFatal)
        wx.PostEvent(self._parent, evt)

    def abortar(self):
        self._abort = True
