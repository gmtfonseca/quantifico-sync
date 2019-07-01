from requests.exceptions import HTTPError
from modules.lib.network import HttpDeleteQueue
from modules.arquivo import PropriedadesArquivo


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
        self._servidor.setEstado(response)
