from core.observador import Observador
from core.estado import Cliente, Servidor
from core.nf.nf_handler import NfHandler
from lib.network import HttpService


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
