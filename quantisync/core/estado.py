from core.arquivo import PropriedadesArquivo
from lib.util import ArquivoUtil
import glob
import pickle
import os


class Cliente:

    """
    É uma pasta que contém um conjunto de propriedades de arquivos
    que determinam o estado do cliente
    """

    def __init__(self, path, extensao):
        self._path = path
        self._extensao = extensao
        self.carregaEstado()

    def carregaEstado(self):
        arquivos = glob.glob('{}/*.{}'.format(self._path, self._extensao))
        self._estado = {PropriedadesArquivo(ArquivoUtil.nomeBase(a),
                                            ArquivoUtil.dataModificacaoSegundos(a)).getEstado()
                        for a in arquivos}

    def setExtensao(self, extensao):
        self._extensao = extensao
        self.carregaEstado()

    def getEstado(self):
        return self._estado

    def getPath(self):
        return self._path

    def getExtensao(self):
        return self._extensao


class Servidor:
    """
    É um pickle que caracteriza o estado do servidor
    """

    def __init__(self, path):
        self._path = path
        self.carregaEstado()

    def carregaEstado(self):
        if not os.path.isfile(self._path):
            self._criaPickleVazio()
        elif os.path.getsize(self._path) > 0:
            self._estado = pickle.load(open(self._path, "rb"))

    def _criaPickleVazio(self):
        with open(self._path, 'wb') as file:
            self._estado = set()
            pickle.dump(self._estado, file, pickle.HIGHEST_PROTOCOL)

    def setEstado(self, estado):
        self._estado = set(estado)
        self._serializaEstado()

    def _serializaEstado(self):
        with open(self._path, "wb") as file:
            pickle.dump(self._estado, file, pickle.HIGHEST_PROTOCOL)

    def getEstado(self):
        return self._estado

    def getPath(self):
        return self._path


class Observador:
    """
    Detecta mudanças de estado entre Cliente e Servidor
    """

    def __init__(self, cliente, servidor):
        self.cliente = cliente
        self.servidor = servidor
        self._insercoes = {}
        self._remocoes = {}

    def observar(self):
        self.cliente.carregaEstado()
        self._detectaInsercoes()
        self._detectaRemocoes()

    def _detectaInsercoes(self):
        self._insercoes = self.cliente.getEstado() - self.servidor.getEstado()

    def _detectaRemocoes(self):
        self._remocoes = self.servidor.getEstado() - self.cliente.getEstado()

    def possuiMudancas(self):
        return self.possuiInsercoes() or self.possuiRemocoes()

    def possuiInsercoes(self):
        return len(self._insercoes) > 0

    def possuiRemocoes(self):
        return len(self._remocoes) > 0

    def getInsercoes(self):
        return self._insercoes

    def getRemocoes(self):
        return self._remocoes
