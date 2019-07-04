from modules.observador import Observador
from modules.estado import Cliente, Servidor
from modules.nf.nf_handler import NfHandler
from modules.lib.network import HttpService


class ObservadorFactory:
    @staticmethod
    def getObservadorNfs(nfsPath, picklePath):
        cliente = Cliente(nfsPath, 'XML')
        servidor = Servidor(picklePath)
        httpService = HttpService('sync/nfs')
        nfHandler = NfHandler(httpService)
        return Observador(nfHandler, cliente, servidor)
