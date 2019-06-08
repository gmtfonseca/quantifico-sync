from models.observador import Observador
from models.estado import Cliente, Servidor
from models.nf_handler import NfHandler
import os

NF_PATH = os.path.abspath('nf')
PICKLE_PATH = os.path.abspath('serverstate.file')
DELAY = 15.0


def init():
    estadoCliente = Cliente(NF_PATH)
    estadoServidor = Servidor(PICKLE_PATH)
    observador = Observador(NfHandler(), estadoCliente, estadoServidor, DELAY)
    observador.observar()


init()
