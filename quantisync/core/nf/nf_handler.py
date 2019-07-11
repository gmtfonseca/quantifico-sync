from lib.network import HttpStreamQueue, HttpDeleteQueue
from core.arquivo import PropriedadesArquivo
from core.nf.nf_parser import NfParser
from core.nf.nf import Nf
from requests.exceptions import HTTPError
from http import HTTPStatus
import json
import os


class NfHandler():
    def __init__(self, httpService):
        self._httpService = httpService

    def onInsercao(self, cliente, servidor, insercoes):
        nfInsercaoStrategy = NfInsercaoStrategy(self._httpService,
                                                cliente,
                                                servidor)
        nfInsercaoStrategy.inserir(insercoes)

    def onRemocao(self, servidor, remocoes):
        nfRemocaoStrategy = NfRemocaoStrategy(self._httpService,
                                              servidor)
        nfRemocaoStrategy.remover(remocoes)


class NfInsercaoStrategy:
    """
    Classe responsável pela lógica de inserção de Nf no Cliente"
    """

    def __init__(self, httpService, cliente, servidor):
        self._cliente = cliente
        self._servidor = servidor
        self._nfsInseridasQueue = HttpStreamQueue(httpService,
                                                  self._streamGenerator)

    def inserir(self, insercoes):
        self._enqueueNfsInseridas(insercoes)
        self._dequeueNfsInseridas()

    def _enqueueNfsInseridas(self, insercoes):
        for i in insercoes:
            nfInserida = self._setupNfInserida(i)
            self._nfsInseridasQueue.enqueue(nfInserida.toDict())

    def _setupNfInserida(self, estado):
        propriedadesArquivo = PropriedadesArquivo.fromEstado(estado)
        pathXml = os.path.join(self._cliente.getPath(),
                               '{}.{}'.format(propriedadesArquivo.nome,
                                              self._cliente.getExtensao()))
        conteudoNf = NfParser.parse(pathXml)
        nf = Nf(propriedadesArquivo, conteudoNf)
        return nf

    def _dequeueNfsInseridas(self):
        self._nfsInseridasQueue.dequeue(self._postBatchHandler)

    def _streamGenerator(self, nfs):
        for nf in nfs:
            yield json.dumps(nf, ensure_ascii=False).encode()

    def _postBatchHandler(self, response):
        if (response.status_code == HTTPStatus.OK):
            self._servidor.setEstado(response.json())


class NfRemocaoStrategy:
    """
    Classe responsável pela lógica de remoção de Nf no Cliente"
    """

    def __init__(self, httpService, servidor):
        self._servidor = servidor
        self._nfsRemovidasQueue = HttpDeleteQueue(httpService)

    def remover(self, remocoes):
        self._enqueueNfsRemovidas(remocoes)
        self._dequeueNfsRemovidas()

    def _enqueueNfsRemovidas(self, remocoes):
        for r in remocoes:
            nomeArquivoNfRemovida = PropriedadesArquivo.fromEstado(r).nome
            self._nfsRemovidasQueue.enqueue(nomeArquivoNfRemovida)

    def _dequeueNfsRemovidas(self):
        try:
            self._nfsRemovidasQueue.dequeue(self._postBatchHandler)
        except HTTPError:
            pass

    def _postBatchHandler(self, response):
        if (response.status_code == HTTPStatus.OK):
            self._servidor.setEstado(response.json())
