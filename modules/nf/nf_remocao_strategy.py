from lib.network import HttpDeleteQueue
from modules.arquivo import PropriedadesArquivo


class NfRemocaoStrategy:
    """
    Classe responsável pela lógica de remoção de Nf no Cliente"
    """

    def __init__(self, httpService, batchSize, servidor):
        self._servidor = servidor
        self.nfsRemovidasQueue = HttpDeleteQueue(httpService, batchSize)

    def onRemocao(self, remocoes):
        self._enqueueNfsRemovidas(remocoes)
        self.nfsRemovidasQueue.dequeue(self._postBatchHandler)

    def _enqueueNfsRemovidas(self, remocoes):
        for r in remocoes:
            nomeArquivoNfRemovida = PropriedadesArquivo.fromEstado(r).nome
            self.nfsRemovidasQueue.enqueue(nomeArquivoNfRemovida)

    def _postBatchHandler(self, response):
        self._servidor.setEstado(response)
