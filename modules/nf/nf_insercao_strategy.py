from lib.network import HttpStreamQueue
from modules.arquivo import PropriedadesArquivo
import json
import os


class NfInsercaoStrategy:
    """
    Classe responsável pela lógica de inserção de Nf no Cliente"
    """

    def __init__(self, httpService, batchSize=10):
        self.nfsInseridasQueue = HttpStreamQueue(httpService, batchSize, self._streamGenerator)

    def onInsercao(self, cliente, servidor, insercoes):
        self._enqueueInsercoes(cliente, servidor, insercoes)

    def _enqueueInsercoes(self, cliente, insercoes):
        for i in insercoes:
            self._setupNfAndEnqueue(cliente, i)

    def _setupNfAndEnqueue(self, cliente, estado):
        try:
            nfInserida = self._setupNfInserida(
                estado, cliente.getPath())
            self.nfsInseridasQueue.enqueue(nfInserida.toDict())
        except FileNotFoundError:
            print('Arquivo não encontrado')
        except XmlInvalido:
            print('XML Inválido')
        except NfInvalida:
            print('Nf Invalida')

    def _setupNfInserida(self, estado, clientePath):
        propriedadesArquivo = PropriedadesArquivo.fromEstado(estado)
        pathXml = os.path.join(clientePath, '{}.XML'.format(propriedadesArquivo.nome))
        conteudoNf = NfParser.parse(pathXml)
        nf = Nf(propriedadesArquivo, conteudoNf)
        return nf

    def _streamGenerator(self, nfs):
        for nf in nfs:
            yield json.dumps(nf, ensure_ascii=False).encode()
