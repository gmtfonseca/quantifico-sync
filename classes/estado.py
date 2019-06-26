import glob
from .arquivo import Arquivo
from lib.util import ArquivoUtil
import pickle
import os


class Cliente:

    def __init__(self, path):
        self._path = path
        self.atualizar()

    def atualizar(self):
        arquivosPath = glob.glob('{}/*.XML'.format(self._path))
        self.arquivos = {Arquivo(ArquivoUtil.nomeBase(a),
                                 ArquivoUtil.dataModificacaoSegundos(a))
                         for a in arquivosPath}
        return self.arquivos

    def getEstado(self):
        return {a.getEstado() for a in self.arquivos}

    def getPath(self):
        return self._path


class Servidor:

    def __init__(self, path):
        self._path = path
        self.carregaEstado()

    def carregaEstado(self):
        if not os.path.isfile(self._path):
            with open(self._path, 'wb') as file:
                self.estado = set()
                pickle.dump(self.estado, file, pickle.HIGHEST_PROTOCOL)
        else:
            self.estado = pickle.load(open(self._path, "rb"))

    def setEstado(self, estado):
        self.estado = set(estado)
        self._serializaEstado()

    def getEstado(self):
        return self.estado

    def _serializaEstado(self):
        with open(self._path, "wb") as file:
            pickle.dump(self.estado, file, pickle.HIGHEST_PROTOCOL)

    def getPath(self):
        return self._path
