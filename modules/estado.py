import glob
from .arquivo import PropriedadesArquivo
from lib.util import ArquivoUtil
import pickle
import os


class Cliente:

    """
    É uma pasta que contém um conjunto de propriedades de arquivos
    que determinam o estado do cliente
    """

    def __init__(self, path, extensao):
        self._path = path
        self.atualizar()

    def atualizar(self):
        arquivosPath = glob.glob('{}/*.{}'.format(self._path, self.extensao))
        self.propriedadesArquivos = {PropriedadesArquivo(ArquivoUtil.nomeBase(a),
                                                         ArquivoUtil.dataModificacaoSegundos(a))
                                     for a in arquivosPath}
        return self.propriedadesArquivos

    def getEstado(self):
        return {p.getEstado() for p in self.propriedadesArquivos}

    def getPath(self):
        return self._path


class Servidor:
    """
    É um pickle que caracteriza o estado do servidor
    """

    def __init__(self, path):
        self._path = path
        self.carregaEstado()

    def carregaEstado(self):
        if not os.path.isfile(self._path):
            with open(self._path, 'wb') as file:
                self._estado = set()
                pickle.dump(self.estado, file, pickle.HIGHEST_PROTOCOL)
        else:
            self._estado = pickle.load(open(self._path, "rb"))

    def setEstado(self, estado):
        self._estado = set(estado)
        self._serializaEstado()

    def getEstado(self):
        return self._estado

    def _serializaEstado(self):
        with open(self._path, "wb") as file:
            pickle.dump(self._estado, file, pickle.HIGHEST_PROTOCOL)

    def getPath(self):
        return self._path
