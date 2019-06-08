from lib.network import HttpService
from models.arquivo import Arquivo
import xmltodict
import os


class NfHandler():
    def __init__(self):
        self.httpService = HttpService('nfs')

    def onInsercao(self, path, insercoes):
        for i in insercoes:
            arquivo = Arquivo.fromEstado(i)
            pathArquivo = os.path.join(path, '{}.XML'.format(arquivo.nome))
            xml = open(pathArquivo, 'r').read()
            arquivo.conteudo = xmltodict.parse(xml)
            response = self.httpService.post(arquivo.toJSON())
            print(response)

    def onDelecao(self, delecoes):
        for d in delecoes:
            arquivo = Arquivo.fromEstado(d)
            del arquivo.conteudo
            response = self.httpService.post(arquivo.toJSON())
            print(response)
