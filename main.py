from models.observador import Observador
from models.estado import Cliente, Servidor
from models.nf_handler import NfHandler
import os

NF_PATH = os.path.abspath('nf')
PICKLE_PATH = os.path.abspath('serverstate.file')
DELAY = 5.0


def init():
    cliente = Cliente(NF_PATH)
    servidor = Servidor(PICKLE_PATH)
    observador = Observador(NfHandler(), cliente, servidor, DELAY)
    observador.observar()


init()
