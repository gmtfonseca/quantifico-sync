from lib.network import HttpService
from models.arquivo import Arquivo
from models.estado_queue import EstadoQueue
import json
import xmltodict
import os


class NfHandler():
    def __init__(self):
        self.httpService = HttpService('nfs')
        self.estadoQueue = EstadoQueue(3)

    def onInsercao(self, cliente, servidor, insercoes):
        arquivos = []
        for i in insercoes:
            arquivo = Arquivo.fromEstado(i)
            pathArquivo = os.path.join(cliente.getPath(),
                                       '{}.XML'.format(arquivo.nome))
            xml = open(pathArquivo, 'r').read()
            arquivo.conteudo = xmltodict.parse(xml)
            arquivos.append(arquivo.toDict())

        response = self.httpService.stream(arquivos, self.streamGen)
        print(response)
        servidor.setEstado(response['estadoServidor'])

    def onDelecao(self, servidor, delecoes):
        arquivos = []
        for d in delecoes:
            arquivo = Arquivo.fromEstado(d)
            print(arquivo.nome)
            del arquivo.conteudo
            arquivos.append(arquivo.toDict())

        response = self.httpService.put({'arquivos': arquivos})
        print(response)
        servidor.setEstado(response['estadoServidor'])

    def streamGen(self, arquivos):
        for arquivo in arquivos:
            print(arquivo['nome'])
            yield json.dumps(arquivo, ensure_ascii=False).encode()
