from modules.observador import Observador
from modules.estado import Cliente, Servidor
from modules.nf.nf_handler import NfHandler
from modules.lib.network import HttpService


class NfsFactory:
    @classmethod
    def getObservador(cls, nfsPath, picklePath):
        cliente = Cliente(nfsPath, 'XML')
        servidor = Servidor(picklePath)
        return Observador(cliente, servidor)

    @classmethod
    def getHandler(cls):
        httpService = HttpService('sync/nfs')
        return NfHandler(httpService)
