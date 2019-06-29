class PropriedadesArquivo:
    """
    Estrutura de dados que descreve as propriedades e estado de um arquivo
    """

    def __init__(self, nome, dataModificacaoSegundos):
        self.nome = nome
        self.dataModificacaoSegundos = dataModificacaoSegundos

    @classmethod
    def fromEstado(cls, estado):
        """
        Estado é uma string composta por '${nome}/${dataModificacaoSegundos}'
        """
        nomeDataModificacaoSegundos = estado.split('/')
        nome = nomeDataModificacaoSegundos[0]
        dataModificacaoSegundos = float(nomeDataModificacaoSegundos[1])
        return cls(nome, dataModificacaoSegundos)

    def getEstado(self):
        return '{}/{}'.format(self.nome, self.dataModificacaoSegundos)


class Nf:
    """
    Estrutura de dados que descreve uma Nota Fiscal
    """

    def __init__(self, propriedadesArquivo, conteudo):
        self.propriedadesArquivo = propriedadesArquivo
        self.conteudo = conteudo

    def toDict(self):
        return vars(self)
