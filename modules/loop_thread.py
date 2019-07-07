from ui.events.task_bar_icon import UIEvent, myEVT_UI
from threading import Thread
from enum import Enum
import time
import wx
import logging


class Estado(Enum):
    NORMAL = 0
    SYNCING = 1
    ERROR = 2,
    ABORT = 3


class LoopThread(Thread):

    def __init__(self, observador, handler, delay, parent):
        super().__init__()
        self._observador = observador
        self._handler = handler
        self._delay = delay
        self._parent = parent
        self._estado = Estado.NORMAL

    def run(self):
        while True:
            if self._estado == Estado.ABORT:
                return

            self._observaMudancas()
            time.sleep(self._delay)

    def _observaMudancas(self):
        self._observador.observar()
        if self._observador.possuiMudancas():
            self._handleMudancas()

    def _handleMudancas(self):
        try:
            self._atualizaEstadoPropagaEvento(Estado.SYNCING)
            self._handleInsercoesRemocoes()
            self._atualizaEstadoPropagaEvento(Estado.NORMAL)
        except Exception as err:
            self._atualizaEstadoPropagaEvento(Estado.ERROR)
            logging.debug('Erro ao syncar')
            logging.debug(err)

    def _handleInsercoesRemocoes(self):
        if self._observador.possuiInsercoes():
            logging.debug('Inserindo')
            self._handler.onInsercao(self._observador.cliente,
                                     self._observador.servidor,
                                     self._observador.getInsercoes())
        elif self._observador.possuiRemocoes():
            logging.debug('Removendo')
            self._handler.onRemocao(self._observador.servidor,
                                    self._observador.getRemocoes())

    def _atualizaEstadoPropagaEvento(self, estado):
        self._estado = estado
        evt = UIEvent(myEVT_UI, -1, self._estado)
        wx.PostEvent(self._parent, evt)

    def abort(self):
        self._estado = Estado.ABORT
