from .arquivo_queue import ArquivoQueue
from .arquivo import PropriedadesArquivo, Nf
from .nf_parser import NfParser, NfInvalida, XmlInvalido
import json
import os


class NfHandler():
    def __init__(self, httpService, batchSize=10):
        self._httpService = httpService
        self.nfsRemovidasQueue = ArquivoQueue(batchSize)
        self.nfsInseridasQueue = ArquivoQueue(batchSize)

    def onInsercao(self, cliente, servidor, insercoes):
        for i in insercoes:
            try:
                nfInserida = self._setupNfInserida(
                    i, cliente.getPath())
                self.nfsInseridasQueue.enqueue(nfInserida.toDict())
            except FileNotFoundError:
                print('Arquivo não encontrado')
            except XmlInvalido:
                print('XML Inválido')
            except NfInvalida:
                print('Nf Invalida')

        self._processaNfsInseridas(servidor)

    def _setupNfInserida(self, estado, clientePath):
        propriedadesArquivo = PropriedadesArquivo.fromEstado(estado)
        pathXml = os.path.join(clientePath, '{}.XML'.format(propriedadesArquivo.nome))
        conteudoNf = NfParser.parse(pathXml)
        nf = Nf(propriedadesArquivo, conteudoNf)
        return nf

    def _processaNfsInseridas(self, servidor):
        while not self.nfsInseridasQueue.empty():
            nfsBatch = self.nfsInseridasQueue.nextBatch()
            estadoServidor = self._httpService.stream(
                nfsBatch, self._streamGenerator)
            print(estadoServidor)
            servidor.setEstado(estadoServidor)

    def onRemocao(self, servidor, remocoes):
        for r in remocoes:
            nomeArquivoNfRemovida = PropriedadesArquivo.fromEstado(r).nome
            self.nfsRemovidasQueue.enqueue(nomeArquivoNfRemovida)

        self._processaNfsRemovidas(servidor)

    def _processaNfsRemovidas(self, servidor):
        while not self.nfsRemovidasQueue.empty():
            nfsBatch = self.nfsRemovidasQueue.nextBatch()
            estadoServidor = self._httpService.delete(
                {'nfs': nfsBatch})
            print(estadoServidor)
            servidor.setEstado(estadoServidor)

    def _streamGenerator(self, nfs):
        for nf in nfs:
            yield json.dumps(nf, ensure_ascii=False).encode()
