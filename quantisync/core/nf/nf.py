from copy import deepcopy


class NfInvalida(Exception):
    pass


class Nf:
    """
    Estrutura de dados que descreve uma Nota Fiscal
    """

    def __init__(self, propriedadesArquivo, conteudo):
        self.propriedadesArquivo = propriedadesArquivo
        self.conteudo = conteudo

    def toDict(self):
        selfCopy = deepcopy(self)
        selfCopy.propriedadesArquivo = selfCopy.propriedadesArquivo.toDict()
        return vars(selfCopy)
