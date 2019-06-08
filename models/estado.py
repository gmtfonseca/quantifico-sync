import glob
from .arquivo import Arquivo
from lib.util import ArquivoUtil
import pickle


class Cliente:

    def __init__(self, path):
        self.path = path
        self.arquivos = []

    def atualizar(self):
        arquivosPath = glob.glob('{}/*.XML'.format(self.path))
        self.arquivos = {Arquivo(ArquivoUtil.nomeBase(a),
                                 ArquivoUtil.dataUltimaModificacao(a))
                         for a in arquivosPath}
        return self.arquivos

    def getEstado(self):
        return {a.getEstado() for a in self.arquivos}

    def getPath(self):
        return self.path


class Servidor:

    def __init__(self, path):
        self.path = path
        self.estado = set()

    def atualizar(self):
        with open(self.path, "rb") as f:
            self.estado = pickle.load(f)

    def getEstado(self):
        return self.estado

    def getPath(self):
        return self.path
