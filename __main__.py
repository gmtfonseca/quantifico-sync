from classes.observador import Observador
from classes.estado import Cliente, Servidor
from classes.nf_handler import NfHandler
from lib.network import HttpService
import os
import logging

NF = {
    'path': os.path.abspath('nf'),
    'extensao': 'XML'
}
PICKLE_PATH = os.path.abspath('quantisync.dat')
DELAY = 5.0


def main():
    logging.basicConfig(level=logging.DEBUG)
    httpService = HttpService('sync/nfs')
    cliente = Cliente(NF['path'], NF['extensao'])
    servidor = Servidor(PICKLE_PATH)
    observador = Observador(NfHandler(httpService), cliente, servidor, DELAY)
    observador.observar()


if __name__ == "__main__":
    main()
