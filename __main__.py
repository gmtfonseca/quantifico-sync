from classes.observador import Observador
from classes.estado import Cliente, Servidor
from classes.nf_handler import NfHandler
import os

NF_PATH = os.path.abspath('nf')
PICKLE_PATH = os.path.abspath('serverstate.file')
DELAY = 5.0


def main():
    cliente = Cliente(NF_PATH)
    servidor = Servidor(PICKLE_PATH)
    observador = Observador(NfHandler(), cliente, servidor, DELAY)
    observador.observar()


if __name__ == "__main__":
    main()
