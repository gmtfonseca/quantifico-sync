from lib.network import HttpService
from classes.arquivo import Arquivo
from classes.arquivo_queue import ArquivoQueue
import json
import xmltodict
import os


class NfHandler():
    def __init__(self, batchSize=10):
        self._httpService = HttpService('sync/nfs')
        self.arquivosRemovidosQueue = ArquivoQueue(batchSize)
        self.arquivosInseridosQueue = ArquivoQueue(batchSize)

    def onInsercao(self, cliente, servidor, insercoes):
        for i in insercoes:
            arquivo = Arquivo.fromEstado(i)
            pathArquivo = os.path.join(cliente.getPath(),
                                       '{}.XML'.format(arquivo.nome))
            xml = open(pathArquivo, 'r').read()
            arquivo.conteudo = xmltodict.parse(xml)
            self.arquivosInseridosQueue.enqueue(arquivo.toDict())

        self._processaArquivosInseridos(servidor)

    def _processaArquivosInseridos(self, servidor):
        while not self.arquivosInseridosQueue.empty():
            batchArquivos = self.arquivosInseridosQueue.nextBatch()
            estadoServidor = self._httpService.stream(
                batchArquivos, self._streamGenerator)
            print(estadoServidor)
            servidor.setEstado(estadoServidor)

    def onRemocao(self, servidor, remocoes):
        for r in remocoes:
            arquivo = Arquivo.fromEstado(r)
            self.arquivosRemovidosQueue.enqueue(arquivo.nome)

        self._processaArquivosRemovidos(servidor)

    def _processaArquivosRemovidos(self, servidor):
        while not self.arquivosRemovidosQueue.empty():
            batchArquivos = self.arquivosRemovidosQueue.nextBatch()
            estadoServidor = self._httpService.delete(
                {'arquivos': batchArquivos})
            print(estadoServidor)
            servidor.setEstado(estadoServidor)

    def _streamGenerator(self, arquivos):
        for arquivo in arquivos:
            yield json.dumps(arquivo, ensure_ascii=False).encode()
