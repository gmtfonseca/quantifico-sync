from lib.network import HttpDeleteQueue
from modules.arquivo import PropriedadesArquivo


class NfRemocaoStrategy:
    """
    Classe responsável pela lógica de remoção de Nf no Cliente"
    """

    def __init__(self, httpService, batchSize=10):
        self.nfsRemovidasQueue = HttpDeleteQueue(httpService, batchSize)

    def onRemocao(self, servidor, remocoes):
        for r in remocoes:
            nomeArquivoNfRemovida = PropriedadesArquivo.fromEstado(r).nome
            self.nfsRemovidasQueue.enqueue(nomeArquivoNfRemovida)

        def postBatchHandler(r): servidor.setEstado(r)
        self.nfsRemovidasQueue.dequeue(postBatchHandler)
