from lib.network import HttpService
from models.arquivo import Arquivo
from models.arquivo_queue import ArquivoQueue
import json
import xmltodict
import os


class NfHandler():
    def __init__(self, batchSize=10):
        self.httpService = HttpService('nfs')
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

        self.processaArquivosInseridos(servidor)

    def processaArquivosInseridos(self, servidor):
        while not self.arquivosInseridosQueue.empty():
            batchArquivos = self.arquivosInseridosQueue.nextBatch()
            response = self.httpService.stream(
                batchArquivos, self.streamGenerator)
            self.atualizaEstadoServidor(response, servidor)

    def onRemocao(self, servidor, remocoes):
        for r in remocoes:
            arquivo = Arquivo.fromEstado(r)
            del arquivo.conteudo
            self.arquivosRemovidosQueue.enqueue(arquivo.toDict())

        self.processaArquivosRemovidos(servidor)

    def processaArquivosRemovidos(self, servidor):
        while not self.arquivosRemovidosQueue.empty():
            batchArquivos = self.arquivosRemovidosQueue.nextBatch()
            response = self.httpService.put({'arquivos': batchArquivos})
            self.atualizaEstadoServidor(response, servidor)

    def atualizaEstadoServidor(self, response, servidor):
        print(response)
        servidor.setEstado(response['estadoServidor'])

    def streamGenerator(self, arquivos):
        for arquivo in arquivos:
            yield json.dumps(arquivo, ensure_ascii=False).encode()
