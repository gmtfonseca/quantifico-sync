from modules.lib.network import HttpStreamQueue
from modules.arquivo import PropriedadesArquivo
from .nf_parser import NfParser
from .nf import Nf
from http import HTTPStatus
import json
import os


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
