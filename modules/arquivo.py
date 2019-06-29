class Arquivo:

    def __init__(self, nome, dataModificacaoSegundos, conteudo={}):
        self.nome = nome
        self.dataModificacaoSegundos = dataModificacaoSegundos
        self.conteudo = conteudo

    @classmethod
    def fromEstado(cls, estado):
        nomeDataModificacaoSegundos = estado.split('/')
        nome = nomeDataModificacaoSegundos[0]
        dataModificacaoSegundos = float(nomeDataModificacaoSegundos[1])
        return cls(nome, dataModificacaoSegundos)

    def getEstado(self):
        return '{}/{}'.format(self.nome, self.dataModificacaoSegundos)

    def toDict(self):
        return vars(self)
