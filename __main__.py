from classes.observador import Observador
from classes.estado import Cliente, Servidor
from classes.nf_handler import NfHandler
from lib.network import HttpService
import os
import logging

NF = {
    'PATH': os.path.abspath('nf'),
    'EXTENSAO': 'XML'
}
PICKLE_PATH = os.path.abspath('quantisync.dat')
DELAY = 5.0


def main():
    logging.basicConfig(level=logging.DEBUG)
    httpService = HttpService('sync/nfs')
    cliente = Cliente(NF['PATH'], NF['EXTENSAO'])
    servidor = Servidor(PICKLE_PATH)
    nfHandler = NfHandler(httpService)
    observador = Observador(nfHandler, cliente, servidor, DELAY)
    observador.observar()


if __name__ == "__main__":
    main()
